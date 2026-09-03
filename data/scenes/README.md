# Scene files

A **scene file** is a small `.json` document that says what to build and how to
shade it. Everything in it is produced by the functions *you* write in `src/`:

| what the scene asks for | which of your functions does it |
|---|---|
| `"geometry": {"type": "sphere"}` / `"cube"` | `sphere`, `cube` |
| `"subdivide": n` | `catmull_clark` |
| `"transform": [...]` | `translate`, `uniform_scale`, `rotate_about_y` |
| `{"translate_keys": [...]}` | `catmull_rom_interpolation` |
| `"shading": {"type": "procedural"}` | `procedural_color` (→ `blinn_phong`, and the provided `backend.noise.perlin_noise`) |
| `"shading": {"type": "planet"}` | `planet_color` — your open-ended planet; also receives the scene time |
| `"shading": {"type": "blinn_phong"}` | `blinn_phong` |
| `"bump": true` | `bump_position`, `perturbed_normal` (→ `bump_height`, `tangent`) |
| `"geometry": {"type": "obj"}` | `per_vertex_normals` (for its normals) |

So a scene will only look right once the functions it uses are correct — which
also makes scenes a pleasant way to *see* whether your code works.

## Running one

```bash
python main.py --scene three-moons              # interactive viewer
python main.py --scene three-moons --headless   # save a .png + .obj files
python main.py --scene my-scene.json            # your own file, any path
python main.py --scene three-moons --time 2.5   # jump to t = 2.5 s
```

A bare name (`three-moons`) is looked up in this folder; anything else is
treated as a path.

## The format

```jsonc
{
  "name": "Three moons",
  "description": "shown in the console when the scene loads",

  // Direction the camera looks from, toward the origin.
  "view": [0, 0.2, 1],

  // Static camera: what the frame is centred on, and how much of the world
  // fits across it. Optional, but see below.
  "camera": { "center": [0, 0.19, -0.04], "extent": 3.96 },

  // "orbiting" circles the scene; "fixed" stays put.
  "light": { "type": "orbiting", "period": 10.0, "elevation": 0.35 },
  // "light": { "type": "fixed", "direction": [0.4, 0.8, 0.6] },

  "objects": [
    {
      "name": "planet",
      "geometry": { "type": "sphere", "nu": 40, "nv": 26 },
      "shading":  { "type": "procedural", "bump": true },
      "transform": [ { "scale": 0.9 } ]
    }
  ]
}
```

### `camera`

| field | meaning |
|---|---|
| `center` | the world-space point the frame is centred on |
| `extent` | half the width of the visible square, in world units |

Leave `camera` out and the renderer fits the frame to whatever is on screen.
That is fine for a single still, but it re-fits **every frame**, so an animated
scene appears to zoom and drift as objects move — the camera chases the
content. Giving a fixed `center` and `extent` pins it: the objects move and the
camera does not.

Every sample scene here ships a camera fitted across its whole animation, with
about 10% margin, so nothing leaves the frame at any point in the loop. If you
add a fast-moving object to a scene, widen `extent` to suit.

### `geometry`

| field | meaning |
|---|---|
| `"type": "sphere"` | unit sphere; `nu` (longitude) × `nv` (latitude) resolution |
| `"type": "cube"` | the unit cube from your `cube()` |
| `"type": "obj"` | load a mesh; `"path"` is relative to the scene file |
| `"subdivide": n` | apply `n` rounds of Catmull-Clark (any all-quad mesh: the sphere, the cube, or a quad `.obj` such as `bob.obj`) |

### `shading`

| field | meaning |
|---|---|
| `"type": "procedural"` | your `procedural_color` marble/planet shader |
| `"type": "blinn_phong"` | `ka`, `kd`, `ks`, `phong_exponent` |
| `"type": "solid"` | a flat `color` — handy while debugging geometry |
| `"bump": true` | displace the surface and perturb its normals (spheres only) |

Colour is computed from **object-space** positions, so a procedural pattern
stays painted on a surface as it moves rather than swimming across it.

### `transform`

A list of steps, multiplied **left to right**, so the first entry is the
outermost transform — the same `R @ T @ S` ordering used in lecture:

```json
"transform": [
  { "rotate_about_y": 0, "period": 4.0 },
  { "translate": [2.0, 0.0, 0.0] },
  { "scale": 0.3 }
]
```

reads as "shrink to 0.3, push out 2 units along x, then spin the whole thing
about the y-axis" — an orbit.

| step | value |
|---|---|
| `{"translate": [x, y, z]}` | move |
| `{"scale": s}` | uniform scale |
| `{"rotate_about_y": degrees}` | rotate |
| `{"translate_keys": [[t, [x,y,z]], ...]}` | move along a keyframed path |

`translate_keys` is the interesting one: give a position at a few key times and
your `catmull_rom_interpolation` produces the smooth path between them. Add
`"loop": T` to wrap time around, so the motion repeats every `T` seconds:

```json
{
  "translate_keys": [
    [0.0, [ 2.2, 0.0,  0.0]],
    [2.0, [ 0.0, 0.0,  2.2]],
    [4.0, [-2.2, 0.0,  0.0]],
    [6.0, [ 0.0, 0.0, -2.2]],
    [8.0, [ 2.2, 0.0,  0.0]]
  ],
  "loop": 8.0
}
```

`keyframed-orbit.json` is a worked example: both paths use evenly spaced keys
and carry a wrap-around key at each end, so the loop closes without a seam.
Because a correct Catmull-Rom curve is C¹ — smooth in velocity, not just
position — the motion should glide through every key. A kink or a lurch exactly
at a key means a tangent is wrong, which makes this a quick visual check on
your interpolation.

Add `"period": seconds` to any step to animate it: `rotate_about_y` sweeps a
full turn each period, and `translate` travels a circle of the same radius in
the xz-plane.

## Making your own (bonus marks)

Copy one of the samples here, rename it, and edit. Some directions worth
trying:

* a moon that orbits a moon — nest the orbit by chaining more transform steps;
* a subdivided cube next to an un-subdivided one, to show what `catmull_clark`
  is doing;
* one object shaded three ways side by side (`procedural`, `blinn_phong`,
  `solid`) to compare the shading models;
* a `fixed` light placed to skim the surface, which makes the bump mapping much
  easier to see than a head-on light does.

If a scene is malformed the loader says which object and which field is at
fault rather than throwing a traceback, so iterating is quick.
