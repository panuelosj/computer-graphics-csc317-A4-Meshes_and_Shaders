import numpy as np

from backend.noise import perlin_noise
from .blinn_phong import blinn_phong
from .bump_mapping import bump_height, perturbed_normal


def planet_color(positions, normals, view, light, time=0.0):
    """Your procedural planet. **Be creative.**

    This is the one open-ended function in the assignment. There is no fixed
    recipe and no reference image to match: your planet does not need to look
    like Earth, or like the example in the README. Build something.

    Everything you have written is available to you here, and so is the
    provided noise:

    * ``perlin_noise(P)`` -- gradient noise (from ``backend/noise.py``).
    * ``bump_height(s)`` -- your layered-noise height field. It doubles nicely
      as an **elevation** map: pick a sea level and everything below it is
      ocean, everything above it is land.
    * ``perturbed_normal(s)`` -- your bump-mapped normals, if you want the
      lighting to react to the terrain.
    * ``blinn_phong(ka, kd, ks, p, n, v, l)`` -- shading. ``ka``, ``kd`` and
      ``ks`` may be ``(k, 3)`` arrays, so different materials can have
      different colours *and* different shininess (water glossy, rock matte).

    Ideas, not requirements: continents and oceans, beaches at the waterline,
    snow above an altitude, polar ice caps, a second layer of noise for
    clouds, city lights on the night side, a gas giant with banded latitudes,
    rings, lava. ``time`` is the scene's animation clock -- offset your noise
    input by it to make clouds drift or seasons turn.

    > **Hint:** sprinkle noise on *everything* -- diffuse colour, specular
    > colour, normals, specular exponent, and colour over time.

    Parameters
    ----------
    positions : (k, 3) array_like
        Object-space surface points (on the unit sphere) to colour.
    normals : (k, 3) array_like
        Surface normals for shading.
    view, light : (3,) or (k, 3) array_like
        View and light directions.
    time : float
        Scene time in seconds, for animated effects. May be ignored.

    Returns
    -------
    (k, 3) float ndarray
        RGB colour per point, each channel in [0, 1].

    Grading
    -------
    Unlike every other function here, this one is **not** checked against a
    reference. The automatic check only confirms you attempted it: that it
    runs, returns one ``(k, 3)`` finite colour per point, and actually varies
    across the surface rather than returning a flat colour. The rest of the
    marks are awarded by a human looking at your render, so make it worth
    looking at.

    See your planet with::

        python main.py --scene planet-and-moon
    """
    # TODO: build a planet. Delete the line below and make something.
    raise NotImplementedError("Implement planet_color")
