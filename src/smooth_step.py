import numpy as np


def smooth_step(f):
    """Cubic smooth-step ``3f^2 - 2f^3``.

    Maps ``smooth_step(0) = 0`` and ``smooth_step(1) = 1`` with zero first
    derivative at both ends, giving an S-shaped ease between 0 and 1. Works on
    scalars or arrays.
    """
    # TODO: return f*f*(3 - 2f).
    raise NotImplementedError("Implement smooth_step")


def improved_smooth_step(f):
    """Quintic smooth-step ``6f^5 - 15f^4 + 10f^3`` (Perlin 2002).

    Like :func:`smooth_step` but with zero first *and* second derivatives at
    ``f = 0`` and ``f = 1``, which removes the second-derivative discontinuity
    that produces visible artifacts in gradient noise.
    """
    # TODO: return 6f^5 - 15f^4 + 10f^3.
    raise NotImplementedError("Implement improved_smooth_step")
