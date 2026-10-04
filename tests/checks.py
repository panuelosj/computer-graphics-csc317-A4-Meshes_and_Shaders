"""Unit checks for Assignment 4 (Meshes and Shaders).

Each check exercises one function in ``src/`` against the golden fixtures in
``tests/golden/a4_golden.npz``. The same checks are used by ``run_tests.py``
(for students) and by the grader. Marks per check mirror the marking scheme.
"""

import os
import tempfile

import numpy as np

from cgcommon.testkit import Check, fixture_path

_GOLDEN = None


def golden():
    global _GOLDEN
    if _GOLDEN is None:
        path = fixture_path(
            os.path.join(os.path.dirname(__file__), "golden", "a4_golden.npz")
        )
        _GOLDEN = np.load(path)
    return _GOLDEN


def _param(g, key, default):
    """Read a scalar test parameter from the fixture, if it carries one.

    The public and private fixtures use *different* parameter values (crease
    threshold, sphere resolution, ...), so an implementation tuned to the
    published numbers will not survive grading.
    """
    return type(default)(g[key]) if key in g.files else default


# --- Part 1: meshes ---------------------------------------------------------

def check_triangle_area_normal():
    from src.triangle_area_normal import triangle_area_normal
    g = golden()
    got = np.asarray(triangle_area_normal(g["tan_a"], g["tan_b"], g["tan_c"]))
    assert got.shape == (3,), f"triangle_area_normal: wrong shape {got.shape}"
    assert np.allclose(got, g["triangle_area_normal"]), (
        "triangle_area_normal: should be 0.5 * (b-a) x (c-a)"
    )
    # the vector's length must equal the triangle's area
    a, b, c = g["tan_a"], g["tan_b"], g["tan_c"]
    area = 0.5 * np.linalg.norm(np.cross(b - a, c - a))
    assert np.isclose(np.linalg.norm(got), area), (
        "triangle_area_normal: length should equal the triangle area"
    )


def check_per_face_normals():
    from src.per_face_normals import per_face_normals
    g = golden()
    got = np.asarray(per_face_normals(g["mesh_V"], g["mesh_F"]))
    exp = g["per_face_normals"]
    assert got.shape == exp.shape, f"per_face_normals: wrong shape {got.shape}"
    assert np.allclose(np.linalg.norm(got, axis=1), 1.0), (
        "per_face_normals: each normal must be unit length"
    )
    assert np.allclose(got, exp, atol=1e-8), "per_face_normals: values differ"


def check_vertex_triangle_adjacency():
    from src.vertex_triangle_adjacency import vertex_triangle_adjacency
    g = golden()
    VF = vertex_triangle_adjacency(g["mesh_F"], int(g["mesh_V"].shape[0]))
    assert len(VF) == g["mesh_V"].shape[0], "vertex_triangle_adjacency: wrong length"
    pad, lens = g["vf_pad"], g["vf_len"]
    for v, lst in enumerate(VF):
        lst = list(lst)
        assert len(lst) == int(lens[v]), (
            f"vertex_triangle_adjacency: vertex {v} has {len(lst)} faces, "
            f"expected {int(lens[v])}"
        )
        assert sorted(lst) == sorted(pad[v, : int(lens[v])].tolist()), (
            f"vertex_triangle_adjacency: wrong incident faces for vertex {v}"
        )


def check_per_vertex_normals():
    from src.per_vertex_normals import per_vertex_normals
    g = golden()
    got = np.asarray(per_vertex_normals(g["mesh_V"], g["mesh_F"]))
    exp = g["per_vertex_normals"]
    assert got.shape == exp.shape, f"per_vertex_normals: wrong shape {got.shape}"
    assert np.allclose(np.linalg.norm(got, axis=1), 1.0), (
        "per_vertex_normals: each normal must be unit length"
    )
    assert np.allclose(got, exp, atol=1e-8), "per_vertex_normals: values differ"


def check_per_corner_normals():
    from src.per_corner_normals import per_corner_normals
    g = golden()
    thresh = _param(g, "pcn_threshold", 20.0)
    got = np.asarray(per_corner_normals(g["mesh_V"], g["mesh_F"], thresh))
    exp = g["per_corner_normals_20"]
    assert got.shape == exp.shape, f"per_corner_normals: wrong shape {got.shape}"
    assert np.allclose(got, exp, atol=1e-8), "per_corner_normals: values differ"


def check_cube():
    from src.cube import cube
    V, F = cube()
    V = np.asarray(V)
    F = np.asarray(F)
    assert V.shape == (8, 3), f"cube: V should be (8,3), got {V.shape}"
    assert F.shape == (6, 4), f"cube: F should be (6,4), got {F.shape}"
    # all 8 vertices referenced, each face has 4 distinct corners
    assert set(F.ravel().tolist()) == set(range(8)), "cube: faces must use all 8 verts"
    for f in F:
        assert len(set(f.tolist())) == 4, "cube: each quad must have 4 distinct corners"
    # vertices are the 8 corners of an axis-aligned unit box
    assert np.allclose(np.sort(np.unique(V)), [0.0, 1.0]), (
        "cube: coordinates should be the corners of a unit box"
    )
    # faces wind consistently outward (first triangle's normal points away
    # from the cube centre), as promised in the docstring
    centre = np.array([0.5, 0.5, 0.5])
    for f in F:
        a, b, c = V[f[0]], V[f[1]], V[f[2]]
        n = np.cross(b - a, c - a)
        face_centre = V[f].mean(axis=0)
        assert float(n @ (face_centre - centre)) > 0, (
            "cube: quad wound inward (its normal should point out of the box)"
        )


def check_sphere():
    from src.sphere import sphere
    g = golden()
    nu = _param(g, "sphere_check_nu", 8)
    nv = _param(g, "sphere_check_nv", 5)
    V, F = sphere(nu, nv)
    V = np.asarray(V)
    F = np.asarray(F)
    assert F.shape == (nu * nv, 4), \
        f"sphere: F should be ({nu * nv},4), got {F.shape}"
    assert V.shape == (1 + nu * (nv - 1) + 1, 3), f"sphere: wrong V shape {V.shape}"
    assert np.allclose(np.linalg.norm(V, axis=1), 1.0, atol=1e-9), (
        "sphere: every vertex must lie on the unit sphere"
    )
    assert F.min() >= 0 and F.max() < V.shape[0], "sphere: face indices out of range"
    assert set(F.ravel().tolist()) == set(range(V.shape[0])), (
        "sphere: every vertex should be referenced by some face"
    )
    # poles sit where the docstring promises them
    assert np.allclose(V[0], [0.0, -1.0, 0.0], atol=1e-9), (
        "sphere: index 0 should be the bottom pole (0,-1,0)"
    )
    assert np.allclose(V[-1], [0.0, 1.0, 0.0], atol=1e-9), (
        "sphere: the last vertex should be the top pole (0,+1,0)"
    )
    # each interior ring lies at one of the expected latitudes
    expected_y = np.cos(np.pi - np.arange(1, nv) * np.pi / float(nv))
    ring_y = np.unique(np.round(V[1:-1, 1], 9))
    assert np.allclose(np.sort(ring_y), np.sort(np.round(expected_y, 9)), atol=1e-6), (
        "sphere: interior rings are not at the theta = pi - v*pi/num_v latitudes"
    )


def check_write_obj():
    from src.write_obj import write_obj
    from cgcommon.objio import read_obj
    g = golden()
    with tempfile.TemporaryDirectory() as d:
        # quad mesh (cube) round-trip
        qpath = os.path.join(d, "quad.obj")
        write_obj(qpath, g["cube_V"], g["cube_F"])
        V2, F2 = read_obj(qpath)
        assert np.allclose(V2, g["cube_V"], atol=1e-6), "write_obj: quad verts differ"
        assert np.array_equal(np.asarray(F2), g["cube_F"]), "write_obj: quad faces differ"
        # triangle mesh round-trip
        tpath = os.path.join(d, "tri.obj")
        write_obj(tpath, g["mesh_V"], g["mesh_F"])
        V3, F3 = read_obj(tpath)
        assert np.allclose(V3, g["mesh_V"], atol=1e-6), "write_obj: tri verts differ"
        assert np.array_equal(np.asarray(F3), g["mesh_F"]), "write_obj: tri faces differ"


def check_catmull_clark():
    from src.catmull_clark import catmull_clark
    g = golden()
    # control mesh for subdivision (the public fixture uses the unit cube; the
    # private grading fixture uses a different closed quad mesh)
    cV = g["cc_ctrl_V"] if "cc_ctrl_V" in g.files else g["cube_V"]
    cF = g["cc_ctrl_F"] if "cc_ctrl_F" in g.files else g["cube_F"]
    n_quads = cF.shape[0]

    # num_iters = 0 returns the input unchanged.
    V0, F0 = catmull_clark(cV, cF, 0)
    assert np.allclose(np.asarray(V0), cV) and np.array_equal(np.asarray(F0), cF), (
        "catmull_clark: 0 iterations should return the input unchanged"
    )

    # one iteration: 4x faces, predictable vertex count (V + F + E).
    V1, F1 = catmull_clark(cV, cF, 1)
    V1 = np.asarray(V1, dtype=float)
    F1 = np.asarray(F1, dtype=int)
    assert F1.shape == (4 * n_quads, 4), (
        f"catmull_clark: expected {4 * n_quads} quads, got {F1.shape}"
    )
    assert V1.shape == g["cc1_V"].shape, "catmull_clark: wrong vertex count after 1 iter"
    assert np.allclose(np.sort(V1, axis=0), np.sort(g["cc1_V"], axis=0), atol=1e-8), (
        "catmull_clark: vertices differ from reference after 1 iteration"
    )

    # two iterations: same geometry as the reference, in ANY vertex/face order.
    V2, F2 = catmull_clark(cV, cF, 2)
    V2 = np.asarray(V2, dtype=float)
    F2 = np.asarray(F2, dtype=int)
    assert F2.shape == g["cc_F"].shape, "catmull_clark: wrong face count after 2 iters"
    assert V2.shape == g["cc_V"].shape, "catmull_clark: wrong vertex count after 2 iters"
    assert np.allclose(np.sort(V2, axis=0), np.sort(g["cc_V"], axis=0), atol=1e-8), (
        "catmull_clark: vertex positions differ from reference after 2 iterations"
    )
    # topology invariants: well-formed quads over exactly these vertices, and a
    # closed surface with the cube's sphere topology (V - E + F == 2).
    assert F2.min() >= 0 and F2.max() < V2.shape[0], "catmull_clark: face index range"
    assert set(F2.ravel().tolist()) == set(range(V2.shape[0])), (
        "catmull_clark: every vertex should be used by some face"
    )
    for f in F2:
        assert len(set(f.tolist())) == 4, "catmull_clark: quads need 4 distinct corners"
    edges = set()
    for f in F2:
        for i in range(4):
            a, bb = int(f[i]), int(f[(i + 1) % 4])
            edges.add((a, bb) if a < bb else (bb, a))
    euler = V2.shape[0] - len(edges) + F2.shape[0]
    assert euler == 2, f"catmull_clark: expected closed sphere topology, Euler {euler}"

    # convergence: subdivision pulls vertices toward a rounded shape, so the
    # result stays inside the control mesh's bounding box.
    lo, hi = cV.min(axis=0) - 1e-6, cV.max(axis=0) + 1e-6
    assert np.all(V2 >= lo) and np.all(V2 <= hi), (
        "catmull_clark: subdivided mesh should stay within the control "
        "mesh's bounding box"
    )


# --- Part 2: software shaders -----------------------------------------------

def check_model_view_projection():
    from src.model_view_projection import (
        translate, uniform_scale, rotate_about_y, model_view_projection,
    )
    g = golden()
    tv = g["translate_v"] if "translate_v" in g.files else np.array([1.0, -2.0, 3.0])
    ss = _param(g, "scale_s", 2.5)
    ra = _param(g, "rotate_a", 0.7)
    assert np.allclose(translate(tv), g["translate"]), "translate wrong"
    assert np.allclose(uniform_scale(ss), g["uniform_scale"]), "uniform_scale wrong"
    assert np.allclose(rotate_about_y(ra), g["rotate_about_y"]), "rotate_about_y wrong"
    got = np.asarray(
        model_view_projection(g["mvp_model"], g["mvp_view"], g["mvp_proj"], g["mvp_pts"])
    )
    assert got.shape == g["model_view_projection"].shape, "mvp: wrong shape"
    assert np.allclose(got, g["model_view_projection"], atol=1e-9), (
        "model_view_projection: projected positions differ"
    )


def check_blinn_phong():
    from src.blinn_phong import blinn_phong
    g = golden()
    got = np.asarray(
        blinn_phong(g["bp_ka"], g["bp_kd"], g["bp_ks"], float(g["bp_p"]),
                    g["bp_n"], g["bp_v"], g["bp_l"])
    )
    assert got.shape == g["blinn_phong"].shape, f"blinn_phong: wrong shape {got.shape}"
    assert np.allclose(got, g["blinn_phong"], atol=1e-9), "blinn_phong: values differ"
    # hand case: light = view = normal => diffuse 1, specular 1, ambient 0.1.
    e = np.array([0.0, 0.0, 1.0])
    one = blinn_phong(np.ones(3), np.ones(3), np.ones(3), 10.0, e, e, e)
    assert np.allclose(one, 0.1 + 1.0 + 1.0), "blinn_phong: head-on case should be 2.1"


def check_smooth_step():
    from src.smooth_step import smooth_step, improved_smooth_step
    g = golden()
    ss = np.asarray(smooth_step(g["ss_in"]))
    iss = np.asarray(improved_smooth_step(g["ss_in"]))
    assert np.allclose(ss, g["smooth_step"]), "smooth_step: values differ"
    assert np.allclose(iss, g["improved_smooth_step"]), "improved_smooth_step: values differ"
    # endpoints and midpoint are exact for both.
    assert np.isclose(smooth_step(0.0), 0.0) and np.isclose(smooth_step(1.0), 1.0)
    assert np.isclose(smooth_step(0.5), 0.5), "smooth_step(0.5) should be 0.5"
    assert np.isclose(improved_smooth_step(0.0), 0.0) and np.isclose(improved_smooth_step(1.0), 1.0)
    assert np.isclose(improved_smooth_step(0.5), 0.5), "improved_smooth_step(0.5) should be 0.5"


def check_procedural_color():
    from src.procedural_color import procedural_color
    g = golden()
    got = np.asarray(
        procedural_color(g["surf_pts"], g["surf_pts"], g["pc_view"], g["pc_light"])
    )
    assert got.shape == g["procedural_color"].shape, "procedural_color: wrong shape"
    assert np.allclose(got, g["procedural_color"], atol=1e-6), (
        "procedural_color: colours differ from reference"
    )


def check_bump_mapping():
    from src.bump_mapping import bump_height, bump_position, tangent, perturbed_normal
    g = golden()
    s = g["surf_pts"]

    bh = np.asarray(bump_height(s))
    assert bh.shape == g["bump_height"].shape, "bump_height: wrong shape"
    assert np.allclose(bh, g["bump_height"], atol=1e-6), "bump_height: values differ"

    bp = np.asarray(bump_position(s))
    assert np.allclose(bp, g["bump_position"], atol=1e-6), "bump_position: values differ"

    T, B = tangent(s)
    T = np.asarray(T)
    B = np.asarray(B)
    N = s / np.linalg.norm(s, axis=1, keepdims=True)
    assert np.allclose(np.linalg.norm(T, axis=1), 1.0, atol=1e-6), "tangent: T not unit"
    assert np.allclose(np.linalg.norm(B, axis=1), 1.0, atol=1e-6), "tangent: B not unit"
    assert np.allclose(np.sum(T * N, axis=1), 0.0, atol=1e-6), "tangent: T not perpendicular to N"
    assert np.allclose(np.sum(B * N, axis=1), 0.0, atol=1e-6), "tangent: B not perpendicular to N"
    assert np.allclose(np.sum(T * B, axis=1), 0.0, atol=1e-6), "tangent: T,B not orthogonal"

    pn = np.asarray(perturbed_normal(s))
    assert pn.shape == g["perturbed_normal"].shape, "perturbed_normal: wrong shape"
    assert np.allclose(np.linalg.norm(pn, axis=1), 1.0, atol=1e-6), (
        "perturbed_normal: normals must be unit length"
    )
    assert np.allclose(pn, g["perturbed_normal"], atol=1e-5), (
        "perturbed_normal: values differ from reference"
    )


def check_planet_color():
    """Was it attempted at all?

    This one function is open-ended: there is no reference to match, so the
    automatic mark is for producing *something*. A human looks at the render
    for the rest. We therefore only confirm it runs, returns one finite colour
    per point, and is not a flat fill.
    """
    from src.planet_color import planet_color
    g = golden()
    P = g["surf_pts"]
    N = P / np.linalg.norm(P, axis=1, keepdims=True)
    view = np.asarray(g["pc_view"], dtype=float)
    light = np.asarray(g["pc_light"], dtype=float)

    got = np.asarray(planet_color(P, N, view, light, 0.0), dtype=float)
    assert got.shape == (P.shape[0], 3), (
        f"planet_color: expected one RGB per point ({P.shape[0]}, 3), got {got.shape}"
    )
    assert np.all(np.isfinite(got)), "planet_color: produced NaN or infinity"

    shown = np.clip(got, 0.0, 1.0)
    assert shown.max() > 0.02, (
        "planet_color: the whole surface is black -- nothing would be visible"
    )
    # A flat fill is not an attempt at a *procedural* planet.
    assert shown.std(axis=0).max() > 1e-3, (
        "planet_color: every point came out the same colour. Vary it across "
        "the surface -- drive it from `positions` through the noise."
    )
    # Deterministic: the same surface must shade the same way twice.
    again = np.asarray(planet_color(P, N, view, light, 0.0), dtype=float)
    assert np.allclose(got, again), "planet_color: must be deterministic"


def check_catmull_rom_interpolation():
    from src.catmull_rom_interpolation import catmull_rom_interpolation
    g = golden()
    times, vals = g["cr_times"], g["cr_vals"]
    keyframes = [(float(times[k]), vals[k]) for k in range(len(times))]
    # Passes exactly through every knot.
    for k in range(len(times)):
        out = np.asarray(catmull_rom_interpolation(keyframes, float(times[k])))
        assert np.allclose(out, vals[k], atol=1e-9), (
            f"catmull_rom_interpolation: must pass through keyframe {k}"
        )
    # Matches the reference between knots (and on the clamped extremes).
    for q, exp in zip(g["cr_query"], g["cr_expected"]):
        out = np.asarray(catmull_rom_interpolation(keyframes, float(q)))
        assert np.allclose(out, exp, atol=1e-9), (
            f"catmull_rom_interpolation: wrong value at t={float(q)}"
        )


def get_checks():
    """Return the ordered list of checks for this assignment."""
    return [
        # Part 1: meshes (57)
        Check("write_obj", 7, check_write_obj, "writes valid 1-indexed .obj files"),
        Check("cube", 7, check_cube, "8-vertex / 6-quad unit cube"),
        Check("sphere", 7, check_sphere, "lat-long quad sphere on the unit sphere"),
        Check("triangle_area_normal", 7, check_triangle_area_normal, "area-weighted triangle normal"),
        Check("per_face_normals", 7, check_per_face_normals, "unit normal per face"),
        Check("per_vertex_normals", 6, check_per_vertex_normals, "area-weighted vertex normals"),
        Check("vertex_triangle_adjacency", 6, check_vertex_triangle_adjacency, "incident faces per vertex"),
        Check("per_corner_normals", 5, check_per_corner_normals, "crease-aware corner normals"),
        Check("catmull_clark", 5, check_catmull_clark, "Catmull-Clark quad subdivision"),
        # Part 2: software shaders (43)
        Check("model_view_projection", 7, check_model_view_projection, "MVP transform matrices"),
        Check("blinn_phong", 7, check_blinn_phong, "Blinn-Phong shading"),
        Check("smooth_step", 5, check_smooth_step, "cubic + quintic smooth-step"),
        Check("procedural_color", 6, check_procedural_color, "layered-noise surface colour"),
        Check("catmull_rom_interpolation", 6, check_catmull_rom_interpolation,
              "Catmull-Rom interpolation of vec3 keyframes"),
        Check("bump_mapping", 6, check_bump_mapping, "bump height + perturbed normals"),
        Check("planet_color", 6, check_planet_color,
              "your own procedural planet (open-ended; graded by eye)"),
    ]
