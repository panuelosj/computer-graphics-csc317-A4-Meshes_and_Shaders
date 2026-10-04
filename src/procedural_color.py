import numpy as np

from backend.noise import perlin_noise
from .blinn_phong import blinn_phong


def procedural_color(positions, normals, view, light):
    """A marble/planet-like procedural colour, computed per surface point.

    Layer Perlin noise at several frequencies to drive a vein-like brightness
    pattern, then shade the result with Blinn-Phong. The colour pattern depends
    only on the (object-space) surface ``positions`` -- not on the view or light
    -- so it stays "painted on" the surface as the scene moves.

    Parameters
    ----------
    positions : (k, 3) array_like
        Object-space surface points used to seed the noise.
    normals : (k, 3) array_like
        Surface normals used for shading.
    view : (3,) or (k, 3) array_like
        View direction(s).
    light : (3,) or (k, 3) array_like
        Light direction(s).

    Returns
    -------
    (k, 3) float ndarray
        RGB colour per point.

    Recipe
    ------
    Implement exactly this composition (the unit checks compare against it;
    with ``P = positions`` and ``perlin_noise``)::

        s  = sin(20 * (P[:, 1] + perlin_noise(P)))          # marble veins
        s2 = 0.25 * perlin_noise(1 * P) + 0.25 * perlin_noise(4 * P)
           + 0.25 * perlin_noise(8 * P) + 0.25 * perlin_noise(16 * P)
        b  = 1 - clip(0.1 * (0.5*s + 0.5)**20 + 0.7 * (0.5*s2 + 0.5), 0, 1)
        base = b[:, None] * [0.2, 0.3, 0.8]                 # deep blue
        return blinn_phong(base, base, [1, 1, 1], 1000.0, normals, view, light)

    (The recipe is fixed so the result can be checked automatically. Once the
    checks pass, do experiment with your own patterns in
    ``main.py --mode shade``.)
    """
    # TODO: implement the recipe documented above.
    raise NotImplementedError("Implement procedural_color")
