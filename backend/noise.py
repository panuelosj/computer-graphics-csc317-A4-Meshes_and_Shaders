"""Gradient ("Perlin") noise, provided for you to use in your shaders.

Procedural shading needs a source of smooth, repeatable randomness: a function
that looks noisy but returns the *same* value every time you ask for the same
point, so a surface does not shimmer as the camera moves. That is what gradient
noise gives you, and it is the raw material for marble veins, wood grain,
weathering and bumps.

Use it from any function in ``src/``::

    from backend.noise import perlin_noise

    n = perlin_noise(P)                 # P is (k, 3); returns (k,)

Layering several frequencies is what makes noise look like a material -- each
octave adds finer detail at lower amplitude::

    n = (0.5 * perlin_noise(P)
         + 0.25 * perlin_noise(2.0 * P)
         + 0.125 * perlin_noise(4.0 * P))

Backend code: no assignment asks you to implement this. It is deliberately
self-contained, so it behaves the same whether or not your own ``src/``
functions are finished yet.
"""

from __future__ import annotations

import numpy as np


def _smooth_step(f):
    """Cubic smooth-step ``3f^2 - 2f^3``, used to ease between lattice corners.

    Kept private here rather than imported from ``src/`` so that this module
    never depends on unfinished student code.
    """
    f = np.asarray(f, dtype=float)
    return f * f * (3.0 - 2.0 * f)


def _random2(st):
    """Pseudorandom 2D vector in [0,1)^2 from a 3D seed (hash, deterministic)."""
    st = np.asarray(st, dtype=float)
    s0 = st @ np.array([127.1, 311.7, 783.089])
    s1 = st @ np.array([269.5, 183.3, 173.542])
    S = np.stack([s0, s1], axis=-1)
    val = np.sin(S) * 43758.5453123
    return val - np.floor(val)  # fractional part


def _random_direction(seed):
    """Pseudorandom unit 3D vector (uniform on the sphere) from a 3D seed."""
    r2 = _random2(seed)
    z = 2.0 * r2[..., 0] - 1.0
    a = r2[..., 1] * 2.0 * np.pi
    r = np.sqrt(np.maximum(1.0 - z * z, 0.0))
    return np.stack([z, r * np.cos(a), r * np.sin(a)], axis=-1)


def perlin_noise(points):
    """Gradient ("Perlin") noise sampled at 3D ``points``.

    Each integer lattice corner is assigned a pseudorandom gradient direction
    (hashed deterministically from its coordinates). The noise value is the
    smooth-step-weighted trilinear interpolation of the dot products of those
    gradients with the offset to the sample point, yielding a smooth value in
    roughly ``[-1, 1]``.

    Parameters
    ----------
    points : (k, 3) array_like  (a single ``(3,)`` point is also accepted)

    Returns
    -------
    (k,) float ndarray  (or scalar for a single point)
    """
    pts = np.asarray(points, dtype=float)
    scalar = pts.ndim == 1
    pts = np.atleast_2d(pts)

    i = np.floor(pts)
    f = pts - i
    u = _smooth_step(f)  # (k, 3)

    def grad_dot(corner):
        c = np.asarray(corner, dtype=float)
        g = _random_direction(i + c)         # (k, 3)
        return np.sum(g * (f - c), axis=-1)  # (k,)

    def mix(a, b, t):
        return a + (b - a) * t

    ux, uy, uz = u[:, 0], u[:, 1], u[:, 2]
    n000 = grad_dot((0, 0, 0)); n100 = grad_dot((1, 0, 0))
    n010 = grad_dot((0, 1, 0)); n110 = grad_dot((1, 1, 0))
    n001 = grad_dot((0, 0, 1)); n101 = grad_dot((1, 0, 1))
    n011 = grad_dot((0, 1, 1)); n111 = grad_dot((1, 1, 1))

    x00 = mix(n000, n100, ux)
    x10 = mix(n010, n110, ux)
    x01 = mix(n001, n101, ux)
    x11 = mix(n011, n111, ux)
    y0 = mix(x00, x10, uy)
    y1 = mix(x01, x11, uy)
    out = mix(y0, y1, uz)

    return float(out[0]) if scalar else out
