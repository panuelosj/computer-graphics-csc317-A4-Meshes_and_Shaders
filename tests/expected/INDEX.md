# Public test data: A4-Meshes_and_Shaders

These are the exact arrays the public unit checks compare your
functions against — the inputs they feed in and the outputs they
expect back. Everything here is generated from
`a4_golden.npz`; nothing here is secret, and you
are meant to look at it when a check fails.

* `arrays/<name>.txt` — the values, in readable form.
* `images/<name>.png` — the same array as a viewable image, for
  the entries that are pictures.

To load an array yourself:

```python
import numpy as np
g = np.load('tests/golden/a4_golden.npz')
print(g.files)          # every available name
img = g['<name>']       # one array
```

Regenerate this folder with `python export_expected.py <assignment>` from the repository root.

| entry | what it is | values | picture |
|---|---|---|---|
| `blinn_phong` | shape (4, 3), dtype float64, range [0.0853197, 1.88] | [blinn_phong.txt](arrays/blinn_phong.txt) | — |
| `bp_ka` | shape (3,), dtype float64, range [0.2, 0.8] | [bp_ka.txt](arrays/bp_ka.txt) | — |
| `bp_kd` | shape (3,), dtype float64, range [0.2, 0.8] | [bp_kd.txt](arrays/bp_kd.txt) | — |
| `bp_ks` | shape (3,), dtype float64, range [1, 1] | [bp_ks.txt](arrays/bp_ks.txt) | — |
| `bp_l` | shape (4, 3), dtype float64, range [0, 1] | [bp_l.txt](arrays/bp_l.txt) | — |
| `bp_n` | shape (4, 3), dtype float64, range [-0.4, 1] | [bp_n.txt](arrays/bp_n.txt) | — |
| `bp_p` | shape (), dtype float64, range [50, 50] | [bp_p.txt](arrays/bp_p.txt) | — |
| `bp_v` | shape (4, 3), dtype float64, range [-0.1, 1] | [bp_v.txt](arrays/bp_v.txt) | — |
| `bump_height` | shape (40,), dtype float64, range [-0.0297535, 0.0280986] | [bump_height.txt](arrays/bump_height.txt) | — |
| `bump_position` | shape (40, 3), dtype float64, range [-0.969237, 0.998259] | [bump_position.txt](arrays/bump_position.txt) | — |
| `cc1_F` | shape (24, 4), dtype int64, range [0, 25] | [cc1_F.txt](arrays/cc1_F.txt) | — |
| `cc1_V` | shape (26, 3), dtype float64, range [0, 1] | [cc1_V.txt](arrays/cc1_V.txt) | — |
| `cc_F` | shape (96, 4), dtype int64, range [0, 97] | [cc_F.txt](arrays/cc_F.txt) | — |
| `cc_V` | shape (98, 3), dtype float64, range [0.0607639, 0.939236] | [cc_V.txt](arrays/cc_V.txt) | — |
| `cc_ctrl_F` | shape (6, 4), dtype int64, range [0, 7] | [cc_ctrl_F.txt](arrays/cc_ctrl_F.txt) | — |
| `cc_ctrl_V` | shape (8, 3), dtype float64, range [0, 1] | [cc_ctrl_V.txt](arrays/cc_ctrl_V.txt) | — |
| `cr_expected` | shape (10, 3), dtype float64, range [-10, 40] | [cr_expected.txt](arrays/cr_expected.txt) | — |
| `cr_query` | shape (10,), dtype float64, range [-0.5, 4.5] | [cr_query.txt](arrays/cr_query.txt) | — |
| `cr_times` | shape (5,), dtype float64, range [0, 4] | [cr_times.txt](arrays/cr_times.txt) | — |
| `cr_vals` | shape (5, 3), dtype float64, range [-10, 40] | [cr_vals.txt](arrays/cr_vals.txt) | — |
| `cube_F` | shape (6, 4), dtype int64, range [0, 7] | [cube_F.txt](arrays/cube_F.txt) | — |
| `cube_V` | shape (8, 3), dtype float64, range [0, 1] | [cube_V.txt](arrays/cube_V.txt) | — |
| `improved_smooth_step` | shape (11,), dtype float64, range [0, 1] | [improved_smooth_step.txt](arrays/improved_smooth_step.txt) | — |
| `mesh_F` | shape (8, 3), dtype int64, range [0, 5] | [mesh_F.txt](arrays/mesh_F.txt) | — |
| `mesh_V` | shape (6, 3), dtype float64, range [-1, 1] | [mesh_V.txt](arrays/mesh_V.txt) | — |
| `model_view_projection` | shape (7, 4), dtype float64, range [-0.650944, 3.03481] | [model_view_projection.txt](arrays/model_view_projection.txt) | — |
| `mvp_model` | shape (4, 4), dtype float64, range [-0.14776, 1] | [mvp_model.txt](arrays/mvp_model.txt) | — |
| `mvp_proj` | shape (4, 4), dtype float64, range [-2.02, 2] | [mvp_proj.txt](arrays/mvp_proj.txt) | — |
| `mvp_pts` | shape (7, 3), dtype float64, range [-0.838328, 0.968306] | [mvp_pts.txt](arrays/mvp_pts.txt) | — |
| `mvp_view` | shape (4, 4), dtype float64, range [-3, 1] | [mvp_view.txt](arrays/mvp_view.txt) | — |
| `pc_light` | shape (3,), dtype float64, range [0.3, 0.8] | [pc_light.txt](arrays/pc_light.txt) | — |
| `pc_view` | shape (3,), dtype float64, range [0, 1] | [pc_view.txt](arrays/pc_view.txt) | — |
| `pcn_threshold` | shape (), dtype float64, range [20, 20] | [pcn_threshold.txt](arrays/pcn_threshold.txt) | — |
| `per_corner_normals_20` | shape (24, 3), dtype float64, range [-0.57735, 0.57735] | [per_corner_normals_20.txt](arrays/per_corner_normals_20.txt) | — |
| `per_face_normals` | shape (8, 3), dtype float64, range [-0.57735, 0.57735] | [per_face_normals.txt](arrays/per_face_normals.txt) | — |
| `per_vertex_normals` | shape (6, 3), dtype float64, range [-1, 1] | [per_vertex_normals.txt](arrays/per_vertex_normals.txt) | — |
| `perturbed_normal` | shape (40, 3), dtype float64, range [-0.962799, 0.988104] | [perturbed_normal.txt](arrays/perturbed_normal.txt) | — |
| `procedural_color` | shape (40, 3), dtype float64, range [0.0109721, 0.529113] | [procedural_color.txt](arrays/procedural_color.txt) | — |
| `rotate_a` | shape (), dtype float64, range [0.7, 0.7] | [rotate_a.txt](arrays/rotate_a.txt) | — |
| `rotate_about_y` | shape (4, 4), dtype float64, range [-0.644218, 1] | [rotate_about_y.txt](arrays/rotate_about_y.txt) | — |
| `scale_s` | shape (), dtype float64, range [2.5, 2.5] | [scale_s.txt](arrays/scale_s.txt) | — |
| `smooth_step` | shape (11,), dtype float64, range [0, 1] | [smooth_step.txt](arrays/smooth_step.txt) | — |
| `sphere_F` | shape (24, 4), dtype int64, range [0, 19] | [sphere_F.txt](arrays/sphere_F.txt) | — |
| `sphere_V` | shape (20, 3), dtype float64, range [-1, 1] | [sphere_V.txt](arrays/sphere_V.txt) | — |
| `sphere_check_nu` | shape (), dtype int64, range [8, 8] | [sphere_check_nu.txt](arrays/sphere_check_nu.txt) | — |
| `sphere_check_nv` | shape (), dtype int64, range [5, 5] | [sphere_check_nv.txt](arrays/sphere_check_nv.txt) | — |
| `ss_in` | shape (11,), dtype float64, range [0, 1] | [ss_in.txt](arrays/ss_in.txt) | — |
| `surf_pts` | shape (40, 3), dtype float64, range [-0.963911, 0.989763] | [surf_pts.txt](arrays/surf_pts.txt) | — |
| `tan_a` | shape (3,), dtype float64, range [0, 0] | [tan_a.txt](arrays/tan_a.txt) | — |
| `tan_b` | shape (3,), dtype float64, range [0, 2] | [tan_b.txt](arrays/tan_b.txt) | — |
| `tan_c` | shape (3,), dtype float64, range [0, 3] | [tan_c.txt](arrays/tan_c.txt) | — |
| `tangent_B` | shape (40, 3), dtype float64, range [-0.997166, 0.99999] | [tangent_B.txt](arrays/tangent_B.txt) | — |
| `tangent_T` | shape (40, 3), dtype float64, range [-0.951395, 1] | [tangent_T.txt](arrays/tangent_T.txt) | — |
| `translate` | shape (4, 4), dtype float64, range [-2, 3] | [translate.txt](arrays/translate.txt) | — |
| `translate_v` | shape (3,), dtype float64, range [-2, 3] | [translate_v.txt](arrays/translate_v.txt) | — |
| `triangle_area_normal` | shape (3,), dtype float64, range [0, 3] | [triangle_area_normal.txt](arrays/triangle_area_normal.txt) | — |
| `uniform_scale` | shape (4, 4), dtype float64, range [0, 2.5] | [uniform_scale.txt](arrays/uniform_scale.txt) | — |
| `vf_len` | shape (6,), dtype int64, range [4, 4] | [vf_len.txt](arrays/vf_len.txt) | — |
| `vf_pad` | shape (6, 4), dtype int64, range [0, 7] | [vf_pad.txt](arrays/vf_pad.txt) | — |
