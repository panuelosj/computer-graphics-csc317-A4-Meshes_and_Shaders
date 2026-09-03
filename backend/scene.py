"""Load and evaluate A4 scene files.

A *scene file* is a small, human-readable ``.json`` document describing what to
build and how to shade it. Everything it describes is produced by **your**
``src/`` functions -- the geometry comes from your ``sphere``/``cube``/
``catmull_clark``, the placement from your ``translate``/``uniform_scale``/
``rotate_about_y``, and the colour from your ``procedural_color`` /
``blinn_phong`` / bump-mapping code. Writing a scene is therefore a way to use
your own renderer, and new scenes are what the bonus marks are for.

See ``data/scenes/README.md`` for the format, and the sample scenes next to it.

This module is backend code: you do not need to edit it.
"""

from __future__ import annotations

import json
import math
import os

import numpy as np


class SceneError(Exception):
    """Raised when a scene file is malformed, with a message worth reading."""


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #

def _vec(value, n=3, what="vector"):
    arr = np.asarray(value, dtype=float).reshape(-1)
    if arr.size != n:
        raise SceneError(f"{what} must have {n} numbers, got {list(value)}")
    return arr


def load_scene(path: str, detail: float = 1.0) -> dict:
    """Read a scene file and return it as a validated dict."""
    if not os.path.isfile(path):
        raise SceneError(f"no scene file at {path}")
    try:
        with open(path) as f:
            scene = json.load(f)
    except json.JSONDecodeError as exc:
        raise SceneError(f"{os.path.basename(path)} is not valid JSON: {exc}")

    if not isinstance(scene, dict):
        raise SceneError("a scene file must be a JSON object")
    objects = scene.get("objects")
    if not isinstance(objects, list) or not objects:
        raise SceneError("a scene needs a non-empty \"objects\" list")

    scene.setdefault("name", os.path.splitext(os.path.basename(path))[0])
    scene.setdefault("description", "")
    scene.setdefault("view", [0.0, 0.0, 1.0])
    # Optional static camera. Without one the renderer re-fits the frame to
    # whatever is on screen, which makes an animation zoom and drift; with one
    # the camera holds still for the whole sequence.
    cam = scene.get("camera")
    if cam is not None:
        if not isinstance(cam, dict):
            raise SceneError('"camera" must be an object with "center" and "extent"')
        if "center" not in cam or "extent" not in cam:
            raise SceneError('"camera" needs both "center" [x,y,z] and "extent"')
        cam["center"] = _vec(cam["center"], 3, "camera center").tolist()
        cam["extent"] = float(cam["extent"])
        if cam["extent"] <= 0:
            raise SceneError('"camera" extent must be positive')
    scene.setdefault("light", {"type": "orbiting", "period": 8.0,
                               "elevation": 0.6})
    scene["_dir"] = os.path.dirname(os.path.abspath(path))
    scene["_path"] = path
    for i, obj in enumerate(objects):
        if not isinstance(obj, dict):
            raise SceneError(f"object {i} must be a JSON object")
        obj.setdefault("name", f"object{i}")
        if "geometry" not in obj:
            raise SceneError(f"object {obj['name']!r} has no \"geometry\"")
        obj.setdefault("shading", {"type": "procedural"})
        obj.setdefault("transform", [])
        # `detail` multiplies every sphere's tessellation. Procedural colour is
        # evaluated per *vertex* and interpolated across each quad, so a coarse
        # sphere smears the pattern no matter how many pixels it is drawn into:
        # sharpening the texture means more vertices, not a bigger image. The
        # scene files stay modest so the interactive viewer keeps up; still
        # renders can ask for more.
        if detail != 1.0 and obj["geometry"].get("type", "sphere") == "sphere":
            g = obj["geometry"]
            g["nu"] = max(3, int(round(g.get("nu", 48) * detail)))
            g["nv"] = max(2, int(round(g.get("nv", 32) * detail)))
    return scene


# --------------------------------------------------------------------------- #
# Geometry, built from the student's functions
# --------------------------------------------------------------------------- #

def build_geometry(spec: dict, fns: dict, scene_dir: str):
    """Return ``(V, F, analytic_normals_or_None)`` for one geometry spec."""
    kind = spec.get("type", "sphere")
    if kind == "sphere":
        nu = int(spec.get("nu", 48))
        nv = int(spec.get("nv", 32))
        if nu < 3 or nv < 2:
            raise SceneError(f"sphere needs nu>=3 and nv>=2 (got {nu}, {nv})")
        V, F = fns["sphere"](nu, nv)
        V = np.asarray(V, dtype=float)
        # sphere() returns the unit sphere, so the normals are exact.
        return V, np.asarray(F), V / np.linalg.norm(V, axis=1, keepdims=True)
    if kind == "cube":
        V, F = fns["cube"]()
        return np.asarray(V, dtype=float), np.asarray(F), None
    if kind == "obj":
        rel = spec.get("path")
        if not rel:
            raise SceneError('an "obj" geometry needs a "path"')
        full = rel if os.path.isabs(rel) else os.path.join(scene_dir, rel)
        if not os.path.isfile(full):
            raise SceneError(f"obj file not found: {rel}")
        V, F = fns["read_obj"](full)
        return np.asarray(V, dtype=float), F, None
    raise SceneError(f"unknown geometry type {kind!r} "
                     "(expected sphere, cube or obj)")


def apply_subdivision(V, F, spec: dict, fns: dict):
    """Optionally run the student's Catmull-Clark on a quad mesh.

    Works for any all-quad geometry -- the built-in sphere and cube, and a
    loaded .obj whose faces are quads.
    """
    n = int(spec.get("subdivide", 0))
    if n <= 0:
        return V, F
    F = np.asarray(F)
    if F.ndim != 2 or F.shape[1] != 4:
        raise SceneError('"subdivide" needs an all-quad mesh '
                         '(the sphere, the cube, or a quad .obj)')
    V, F = fns["catmull_clark"](V, F, n)
    return np.asarray(V, dtype=float), np.asarray(F)


# --------------------------------------------------------------------------- #
# Transforms, composed from the student's matrices
# --------------------------------------------------------------------------- #

def model_matrix(transform: list, t: float, fns: dict) -> np.ndarray:
    """Compose a 4x4 model matrix from a list of transform steps.

    Steps are multiplied left to right, so the first entry is the outermost
    transform -- the same convention as ``R @ T @ S`` in the course notes.
    Any step may carry a ``"period"`` (seconds) to animate it, and
    ``translate_keys`` animates a position through keyframes using **your**
    ``catmull_rom_interpolation``.
    """
    M = np.eye(4)
    for step in transform:
        if not isinstance(step, dict) or len(step) == 0:
            raise SceneError(f"bad transform step: {step!r}")
        # JSON has no comments, so keys beginning with "_" are ignored and
        # can be used for notes; "period"/"loop" are modifiers, not operations.
        ops = [k for k in step
               if k not in ("period", "loop") and not k.startswith("_")]
        if not ops:
            raise SceneError(f"transform step has no operation: {step!r}")
        op = ops[0]
        value = step[op]
        period = float(step.get("period", 0.0))
        phase = (2.0 * math.pi * t / period) if period else 0.0

        if op == "translate_keys":
            # A keyframed position: [[time, [x, y, z]], ...]. The path between
            # keys comes from the student's Catmull-Rom interpolation, so this
            # step only works once that function is implemented.
            try:
                keys = [(float(kt), _vec(kv, 3, "translate_keys value"))
                        for kt, kv in value]
            except (TypeError, ValueError):
                raise SceneError(
                    'translate_keys must be a list of [time, [x, y, z]] pairs'
                )
            if len(keys) < 2:
                raise SceneError("translate_keys needs at least two keyframes")
            loop = float(step.get("loop", 0.0))
            tt = (t % loop) if loop > 0.0 else t
            pos = fns["catmull_rom_interpolation"](keys, tt)
            M = M @ fns["translate"](np.asarray(pos, dtype=float).reshape(3))
        elif op == "translate":
            v = _vec(value, 3, "translate")
            if period:
                # travel around a circle of radius |v| in the xz-plane
                r = float(np.linalg.norm([v[0], v[2]])) or float(v[0])
                v = np.array([r * math.cos(phase), v[1], r * math.sin(phase)])
            M = M @ fns["translate"](v)
        elif op == "scale":
            s = float(value)
            M = M @ fns["uniform_scale"](s)
        elif op == "rotate_about_y":
            angle = math.radians(float(value)) if not period else phase
            M = M @ fns["rotate_about_y"](angle)
        else:
            raise SceneError(f"unknown transform {op!r} (expected translate, "
                             "translate_keys, scale or rotate_about_y)")
    return M


def transform_points(M: np.ndarray, P: np.ndarray) -> np.ndarray:
    """Apply a 4x4 model matrix to (k,3) points."""
    P = np.asarray(P, dtype=float)
    homog = np.hstack([P, np.ones((P.shape[0], 1))])
    out = homog @ np.asarray(M, dtype=float).T
    return out[:, :3] / out[:, 3:4]


# --------------------------------------------------------------------------- #
# Lighting and shading
# --------------------------------------------------------------------------- #

def light_direction(light: dict, t: float) -> np.ndarray:
    """The scene's light direction at time ``t``."""
    kind = light.get("type", "orbiting")
    if kind == "fixed":
        return _vec(light.get("direction", [0.0, 1.0, 1.0]), 3, "light direction")
    if kind == "orbiting":
        period = float(light.get("period", 8.0)) or 8.0
        elev = float(light.get("elevation", 0.6))
        theta = 2.0 * math.pi * t / period
        return np.array([math.cos(theta), elev, math.sin(theta)])
    raise SceneError(f"unknown light type {kind!r} (expected fixed or orbiting)")


def _normalize_rows(x):
    """Unit-length each row of an ``(n,3)`` array (zero rows are left alone)."""
    n = np.linalg.norm(x, axis=-1, keepdims=True)
    return x / np.where(n == 0, 1.0, n)


def shade(obj: dict, V, N, view, light, fns: dict, t: float = 0.0) -> np.ndarray:
    """Colour one object's vertices using the student's shading functions."""
    spec = obj["shading"]
    kind = spec.get("type", "procedural")
    if kind == "procedural":
        rgb = fns["procedural_color"](V, N, view, light)
    elif kind == "planet":
        # The open-ended one: it also gets the clock, for drifting clouds and
        # anything else that should change over time.
        rgb = fns["planet_color"](V, N, view, light, t)
    elif kind == "blinn_phong":
        rgb = fns["blinn_phong"](
            _vec(spec.get("ka", [0.1, 0.1, 0.1]), 3, "ka"),
            _vec(spec.get("kd", [0.6, 0.6, 0.6]), 3, "kd"),
            _vec(spec.get("ks", [0.3, 0.3, 0.3]), 3, "ks"),
            float(spec.get("phong_exponent", 50.0)),
            N, view, light,
        )
    elif kind == "solid":
        rgb = np.tile(_vec(spec.get("color", [0.7, 0.7, 0.7]), 3, "color"),
                      (np.asarray(V).shape[0], 1))
    else:
        raise SceneError(f"unknown shading type {kind!r} "
                         "(expected procedural, planet, blinn_phong or solid)")
    return np.clip(np.asarray(rgb, dtype=float).reshape(-1, 3), 0.0, 1.0)


# --------------------------------------------------------------------------- #
# Evaluating a whole scene
# --------------------------------------------------------------------------- #

def evaluate(scene: dict, fns: dict, t: float = 0.0) -> list:
    """Evaluate every object at time ``t``.

    Returns a list of dicts with keys ``name``, ``V`` (world-space positions),
    ``F``, ``colors`` and ``M`` (the model matrix used).
    """
    view = _vec(scene["view"], 3, "view")
    light = light_direction(scene["light"], t)
    out = []
    for obj in scene["objects"]:
        V, F, analytic_N = build_geometry(obj["geometry"], fns, scene["_dir"])
        V, F = apply_subdivision(V, F, obj["geometry"], fns)
        if analytic_N is not None and np.asarray(analytic_N).shape[0] != V.shape[0]:
            analytic_N = None   # subdivision changed the vertex count

        shading = obj["shading"]
        # Bump mapping displaces the surface and perturbs its normals. It is
        # defined on the unit sphere, so it only applies to sphere geometry.
        if shading.get("bump") and obj["geometry"].get("type", "sphere") == "sphere":
            P_local = np.asarray(fns["bump_position"](V), dtype=float)
            N_local = np.asarray(fns["perturbed_normal"](V), dtype=float)
        else:
            P_local = V
            N_local = analytic_N if analytic_N is not None else _mesh_normals(V, F, fns)

        M = model_matrix(obj["transform"], t, fns)
        # The *pattern* is sampled from the object-space surface, so it stays
        # painted on as the object moves. The *lighting* is not: the light is a
        # world-space direction, so the normals it is dotted against have to be
        # rotated into world space too. Without this an object with a spinning
        # transform carries its lit side around with it and turns black when
        # the transform points that side away from the camera.
        N_world = _normalize_rows(np.asarray(N_local, dtype=float)
                                  @ np.asarray(M[:3, :3], dtype=float).T)
        colors = shade(obj, V, N_world, view, light, fns, t)

        out.append({
            "name": obj["name"],
            "V": transform_points(M, P_local),
            "F": F,
            "colors": colors,
            "M": M,
        })
    return out


def _mesh_normals(V, F, fns):
    """Per-vertex normals for a general mesh, via the student's function."""
    F = np.asarray(F)
    tri = fns["triangulate"](F) if F.ndim != 2 or F.shape[1] != 3 else F
    N = np.asarray(fns["per_vertex_normals"](V, tri), dtype=float)
    return N


def describe(scene: dict) -> str:
    """A short human summary of a loaded scene, for the console."""
    lines = [f"  scene: {scene['name']}"]
    if scene.get("description"):
        lines.append(f"    {scene['description']}")
    for obj in scene["objects"]:
        g = obj["geometry"]
        geo = g.get("type", "sphere")
        if geo == "sphere":
            geo += f"({g.get('nu', 48)}x{g.get('nv', 32)})"
        elif geo == "obj":
            geo += f"({os.path.basename(g.get('path', '?'))})"
        if g.get("subdivide"):
            geo += f" +{g['subdivide']} catmull-clark"
        sh = obj["shading"].get("type", "procedural")
        if obj["shading"].get("bump"):
            sh += "+bump"
        lines.append(f"    - {obj['name']}: {geo}, {sh}")
    return "\n".join(lines)
