#!/usr/bin/env python3
"""Assignment 4 demo backend (Meshes and Shaders).

Runs your ``src/`` functions end-to-end and opens an interactive viewer; add
``--headless`` to any mode to skip the viewer and save output images instead.

Modes:
    python main.py --mode normals   # switch per-face/vertex/corner normals
    python main.py --mode generate  # build + view the cube and sphere
    python main.py --mode subdiv    # Catmull-Clark: press "subdivide"/"reset"
    python main.py --mode shade     # animated planet + moon, procedural shading
    python main.py --scene three-moons     # build a scene from a .json file

Interactive controls:
    normals   radio buttons choose which normals are shown; a slider sets the
              per-corner crease threshold (recomputed live).
    subdiv    "subdivide" applies one Catmull-Clark iteration in place
              (like [space] in the original); "reset" restores the control mesh.
    shade     the moon orbits using YOUR translate/uniform_scale/rotate_about_y
              matrices; the light orbits over time; toggle bump mapping on/off.
"""

import argparse
import os
import sys
import math

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# `cgcommon` (shared helpers) normally sits next to this file. If several
# assignments are checked out together it lives two levels up instead.
if not os.path.isdir(os.path.join(HERE, "cgcommon")):
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))

from cgcommon import viewer
from cgcommon.objio import read_obj, triangulate
from cgcommon.image import save_png

from src.triangle_area_normal import triangle_area_normal  # noqa: F401
from src.per_face_normals import per_face_normals
from src.per_vertex_normals import per_vertex_normals
from src.per_corner_normals import per_corner_normals
from src.cube import cube
from src.sphere import sphere
from src.write_obj import write_obj
from src.catmull_clark import catmull_clark
from src.model_view_projection import translate, uniform_scale, rotate_about_y
from src.procedural_color import procedural_color
from src.bump_mapping import bump_position, perturbed_normal

OUT = os.path.join(HERE, "out")


def out_dir():
    os.makedirs(OUT, exist_ok=True)
    return OUT


def _try_viewer():
    try:
        viewer.ensure_init()
        return True
    except viewer.ViewerUnavailable as exc:
        print(f"  (no display: {exc}); falling back to headless save")
        return False


def _show(max_frames):
    """Enter the render loop (or tick a few frames when smoke-testing)."""
    import polyscope as ps
    if max_frames is not None:
        for _ in range(max_frames):
            ps.frame_tick()
    else:
        viewer.show()


def render_points_png(path, points, colors, size=400, extent=None):
    """Tiny orthographic point splat so headless runs still produce an image.

    ``extent`` is the half-width of the square view in world units; when it is
    None the points are auto-fitted (so multi-object scenes are not cropped).
    """
    P = np.asarray(points, dtype=float)
    C = np.clip(np.asarray(colors, dtype=float), 0, 1)
    if extent is None:
        extent = float(np.abs(P[:, :2]).max()) * 1.1 if P.size else 1.2
        extent = max(extent, 1e-6)
    img = np.zeros((size, size, 3), dtype=np.float64)
    depth = np.full((size, size), -np.inf)
    # map x,y in [-extent, extent] to pixels; z is depth (larger = nearer).
    span = 2.0 * extent
    xs = ((P[:, 0] + extent) / span * (size - 1)).astype(int)
    ys = ((extent - P[:, 1]) / span * (size - 1)).astype(int)
    order = np.argsort(P[:, 2])
    rad = max(1, size // 120)
    for idx in order:
        x, y, z = xs[idx], ys[idx], P[idx, 2]
        for dx in range(-rad, rad + 1):
            for dy in range(-rad, rad + 1):
                px, py = x + dx, y + dy
                if 0 <= px < size and 0 <= py < size and z > depth[py, px]:
                    depth[py, px] = z
                    img[py, px] = C[idx]
    save_png(path, (img * 255).astype(np.uint8))


def load_triangle_mesh():
    """Load bob.obj and triangulate it for the normal demos."""
    path = os.path.join(HERE, "data", "bob.obj")
    V, F = read_obj(path)
    Ftri = triangulate(F)
    return V, Ftri


# --- normals ------------------------------------------------------------------

def mode_normals(headless, max_frames=None):
    V, F = load_triangle_mesh()
    print(f"  loaded {V.shape[0]} verts, {F.shape[0]} triangles")
    FN = per_face_normals(V, F)
    VN = per_vertex_normals(V, F)
    CN = per_corner_normals(V, F, 20.0)
    print(f"  per-face {FN.shape}, per-vertex {VN.shape}, per-corner {CN.shape}")

    if headless or not _try_viewer():
        np.savez(os.path.join(out_dir(), "normals.npz"),
                 V=V, F=F, face_normals=FN, vertex_normals=VN, corner_normals=CN)
        print("  saved out/normals.npz")
        return

    import polyscope as ps
    import polyscope.imgui as psim

    m = ps.register_surface_mesh("bob", V, F)
    corners = V[F].reshape(-1, 3)
    corner_pc = ps.register_point_cloud("corners", corners, radius=0.0)

    state = {"which": 0, "threshold": 20.0, "CN": CN}

    def apply():
        which = state["which"]
        m.remove_all_quantities()
        corner_pc.remove_all_quantities()
        corner_pc.set_enabled(which == 2)
        if which == 0:
            m.add_vector_quantity("per-face normals", FN,
                                  defined_on="faces", enabled=True)
        elif which == 1:
            m.add_vector_quantity("per-vertex normals", VN,
                                  defined_on="vertices", enabled=True)
        else:
            corner_pc.add_vector_quantity("per-corner normals", state["CN"],
                                          enabled=True)

    apply()

    def callback():
        clicked = False
        for i, label in enumerate(("per-face (1)", "per-vertex (2)",
                                   "per-corner (3)")):
            if psim.RadioButton(label, state["which"] == i):
                state["which"] = i
                clicked = True
        changed, state["threshold"] = psim.SliderFloat(
            "corner threshold (deg)", state["threshold"], 0.0, 90.0)
        if changed and state["which"] == 2:
            state["CN"] = per_corner_normals(V, F, state["threshold"])
            clicked = True
        if clicked:
            apply()

    ps.set_user_callback(callback)
    _show(max_frames)


# --- generate -------------------------------------------------------------------

def mode_generate(headless, max_frames=None):
    cV, cF = cube()
    sV, sF = sphere(24, 16)
    write_obj(os.path.join(out_dir(), "cube.obj"), cV, cF)
    write_obj(os.path.join(out_dir(), "sphere.obj"), sV, sF)
    print(f"  wrote out/cube.obj ({cV.shape[0]} v, {cF.shape[0]} f)")
    print(f"  wrote out/sphere.obj ({sV.shape[0]} v, {sF.shape[0]} f)")

    if not headless and _try_viewer():
        import polyscope as ps
        ps.register_surface_mesh("cube", cV, cF, edge_width=1.0)
        ps.register_surface_mesh("sphere", sV + np.array([3.0, 0, 0]), sF,
                                 edge_width=1.0)
        _show(max_frames)


# --- subdivision ----------------------------------------------------------------

def mode_subdiv(headless, max_frames=None):
    V, F = read_obj(os.path.join(HERE, "data", "bob.obj"))
    F = np.asarray(F)
    print(f"  control mesh: {V.shape[0]} verts, {F.shape[0]} quads")

    if headless or not _try_viewer():
        levels = {0: (V, F)}
        for it in (1, 2, 3):
            SV, SF = catmull_clark(V, F, it)
            levels[it] = (SV, SF)
            print(f"  iter {it}: {SV.shape[0]} verts, {SF.shape[0]} quads")
        SV, SF = levels[2]
        write_obj(os.path.join(out_dir(), "subdiv2.obj"), SV, SF)
        print("  wrote out/subdiv2.obj")
        return

    import polyscope as ps
    import polyscope.imgui as psim
    from cgcommon.interact import key_pressed

    MAX_LEVEL = 3
    state = {"level": 0, "V": V, "F": F}
    ps.register_surface_mesh("mesh", V, F, edge_width=1.0)

    def set_level(level):
        level = max(0, min(MAX_LEVEL, level))
        if level == 0:
            state["V"], state["F"] = V, F
        else:
            state["V"], state["F"] = catmull_clark(V, F, level)
        state["level"] = level
        ps.register_surface_mesh("mesh", state["V"], state["F"], edge_width=1.0)

    def callback():
        psim.TextUnformatted(
            f"level {state['level']}: {state['V'].shape[0]} verts, "
            f"{len(state['F'])} quads")
        if psim.Button("subdivide (space)") or key_pressed("Space"):
            set_level(state["level"] + 1)
        psim.SameLine()
        if psim.Button("reset (R)") or key_pressed("R"):
            set_level(0)

    ps.set_user_callback(callback)
    print("  press 'subdivide' to apply one Catmull-Clark iteration, "
          "'reset' to go back")
    _show(max_frames)


# --- shading --------------------------------------------------------------------

def moon_model_matrix(t):
    """The moon's model transform, built from YOUR matrices:
    orbit about y over a 4-second period, offset by 2 units, scaled to 0.3."""
    theta = 2.0 * math.pi * t / 4.0
    return rotate_about_y(theta) @ translate([2.0, 0.0, 0.0]) @ uniform_scale(0.3)


def orbiting_light(t):
    """A light direction that circles the scene (like the original lit.fs)."""
    theta = 2.0 * math.pi * t / 8.0
    return np.array([math.cos(theta), 0.6, math.sin(theta)])


def mode_shade(headless, max_frames=None):
    # Build a sphere; shade per-vertex with procedural_color and displace with
    # the bump map. Interactively, a moon orbits using the student's matrices.
    V, F = sphere(48, 32)
    N = V / np.linalg.norm(V, axis=1, keepdims=True)
    view = np.array([0.0, 0.0, 1.0])

    displaced = bump_position(V)
    bumped_normals = perturbed_normal(V)
    colors0 = np.clip(procedural_color(V, N, view, orbiting_light(0.0)), 0, 1)
    print(f"  shaded {V.shape[0]} vertices")

    if headless or not _try_viewer():
        write_obj(os.path.join(out_dir(), "planet.obj"), displaced, F)
        render_points_png(os.path.join(out_dir(), "planet.png"),
                          displaced, colors0)
        print("  wrote out/planet.obj and out/planet.png")
        return

    import polyscope as ps
    import polyscope.imgui as psim

    planet = ps.register_surface_mesh("planet", displaced, F, smooth_shade=True)
    planet.add_color_quantity("procedural colour", colors0, enabled=True)
    moon = ps.register_surface_mesh("moon", displaced, F, smooth_shade=True)
    moon.set_color((0.55, 0.55, 0.58))
    moon.set_transform(moon_model_matrix(0.0))

    state = {"t": 0.0, "playing": True, "bump": True}

    def callback():
        _, state["playing"] = psim.Checkbox("animate (A)", state["playing"])
        psim.SameLine()
        changed_b, state["bump"] = psim.Checkbox("bump mapping", state["bump"])

        if state["playing"]:
            state["t"] += 1.0 / 60.0
        if state["playing"] or changed_b:
            P = displaced if state["bump"] else V
            Nn = bumped_normals if state["bump"] else N
            colors = np.clip(
                procedural_color(V, Nn, view, orbiting_light(state["t"])), 0, 1)
            planet.update_vertex_positions(P)
            planet.add_color_quantity("procedural colour", colors, enabled=True)
            moon.update_vertex_positions(P)
            moon.set_transform(moon_model_matrix(state["t"]))

    ps.set_user_callback(callback)
    print("  the moon orbits via your rotate_about_y/translate/uniform_scale; "
          "the light circles the planet")
    _show(max_frames)


def _scene_functions():
    """The student functions a scene file is allowed to drive."""
    from src.per_vertex_normals import per_vertex_normals
    from src.blinn_phong import blinn_phong
    from src.catmull_rom_interpolation import catmull_rom_interpolation
    from cgcommon.objio import read_obj as _read_obj, triangulate

    def read_obj_native(path):
        """Load a mesh keeping its own faces.

        Quads are left as quads so a quad .obj can still be subdivided; the
        scene triangulates later, wherever triangles are actually needed.
        """
        return _read_obj(path)

    from src.planet_color import planet_color

    return {
        "sphere": sphere,
        "cube": cube,
        "catmull_clark": catmull_clark,
        "translate": translate,
        "uniform_scale": uniform_scale,
        "rotate_about_y": rotate_about_y,
        "procedural_color": procedural_color,
        "planet_color": planet_color,
        "blinn_phong": blinn_phong,
        "catmull_rom_interpolation": catmull_rom_interpolation,
        "bump_position": bump_position,
        "perturbed_normal": perturbed_normal,
        "per_vertex_normals": per_vertex_normals,
        "read_obj": read_obj_native,
        "triangulate": triangulate,
    }


def mode_scene(headless, max_frames=None, scene_path=None, t0=0.0,
               size=400, out_name=None, detail=1.0):
    """Build and shade a scene described by a .json scene file."""
    from backend.scene import load_scene, evaluate, describe, SceneError

    if scene_path is None:
        scene_path = os.path.join(HERE, "data", "scenes", "planet-and-moon.json")
    if not os.path.isabs(scene_path) and not os.path.isfile(scene_path):
        # allow a bare scene name: --scene three-moons
        cand = os.path.join(HERE, "data", "scenes", scene_path)
        for guess in (cand, cand + ".json"):
            if os.path.isfile(guess):
                scene_path = guess
                break

    try:
        scene = load_scene(scene_path, detail=detail)
        fns = _scene_functions()
        parts = evaluate(scene, fns, t=t0)
    except SceneError as exc:
        print(f"  scene error: {exc}")
        return 2
    print(describe(scene))

    if headless or not _try_viewer():
        # Merge every object into one mesh so the z-buffer resolves occlusion
        # between them, then rasterise.
        from cgcommon.softrender import render_mesh_png
        Vs, Fs, Cs, offset = [], [], [], 0
        for p in parts:
            Vp = np.asarray(p["V"], dtype=float)
            Fp = np.asarray(p["F"])
            Vs.append(Vp)
            Cs.append(np.asarray(p["colors"], dtype=float))
            Fs.append([[int(i) + offset for i in np.asarray(f).ravel()]
                       for f in Fp])
            offset += Vp.shape[0]
        allV = np.vstack(Vs)
        allC = np.vstack(Cs)
        allF = [f for grp in Fs for f in grp]
        stem = os.path.splitext(os.path.basename(scene_path))[0]
        png = out_name or os.path.join(out_dir(), f"scene_{stem}.png")
        os.makedirs(os.path.dirname(os.path.abspath(png)), exist_ok=True)
        cam = scene.get("camera")
        render_mesh_png(png, allV, allF, allC, size=size,
                        view=np.asarray(scene["view"], dtype=float),
                        center=(cam["center"] if cam else None),
                        extent=(cam["extent"] if cam else None))
        if out_name:
            print(f"  wrote {png}")
        else:
            for p in parts:
                write_obj(os.path.join(out_dir(),
                                       f"scene_{stem}_{p['name']}.obj"),
                          p["V"], p["F"])
            print(f"  wrote out/scene_{stem}.png (+ one .obj per object)")
        return 0

    import polyscope as ps
    import polyscope.imgui as psim

    handles = {}
    for p in parts:
        h = ps.register_surface_mesh(p["name"], p["V"], p["F"], smooth_shade=True)
        h.add_color_quantity("shading", p["colors"], enabled=True)
        handles[p["name"]] = h

    state = {"t": t0, "playing": True}

    def callback():
        _, state["playing"] = psim.Checkbox("animate (A)", state["playing"])
        if not state["playing"]:
            return
        state["t"] += 1.0 / 60.0
        for q in evaluate(scene, _scene_functions(), t=state["t"]):
            h = handles[q["name"]]
            h.update_vertex_positions(q["V"])
            h.add_color_quantity("shading", q["colors"], enabled=True)

    ps.set_user_callback(callback)
    print("  everything here is built and shaded by YOUR src/ functions")
    _show(max_frames)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="A4 Meshes and Shaders demo.")
    parser.add_argument(
        "--mode",
        choices=["normals", "generate", "subdiv", "shade", "scene"],
        default="generate",
    )
    parser.add_argument(
        "--scene",
        default=None,
        metavar="FILE",
        help="a .json scene file to build and shade (implies --mode scene); "
             "a bare name like 'three-moons' is looked up in data/scenes/",
    )
    parser.add_argument("--time", type=float, default=0.0, metavar="T",
                        help="evaluate the scene at time T seconds "
                             "(animated transforms and lights move with it)")
    parser.add_argument("--detail", type=float, default=1.0, metavar="X",
                        help="multiply every sphere's tessellation by X. The "
                             "procedural colour is computed per vertex, so "
                             "this — not --size — is what sharpens the "
                             "texture. Try --detail 3 for a still image.")
    parser.add_argument("--size", type=int, default=400, metavar="PX",
                        help="headless render size in pixels")
    parser.add_argument("--out", default=None, metavar="PNG",
                        help=argparse.SUPPRESS)  # explicit headless output path
    parser.add_argument("--headless", action="store_true",
                        help="skip the interactive viewer; save data/images instead")
    parser.add_argument("--frames", type=int, default=None,
                        help=argparse.SUPPRESS)  # debug: tick N frames and exit
    args = parser.parse_args(argv)

    if args.scene is not None:
        args.mode = "scene"
    if args.mode == "scene":
        return mode_scene(args.headless, args.frames, args.scene,
                          args.time, args.size, args.out, args.detail)

    {
        "normals": mode_normals,
        "generate": mode_generate,
        "subdiv": mode_subdiv,
        "shade": mode_shade,
    }[args.mode](args.headless, args.frames)


if __name__ == "__main__":
    main()
