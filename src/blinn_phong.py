import numpy as np


def blinn_phong(ka, kd, ks, p, n, v, l):
    """Blinn-Phong shading for a white light with low ambient intensity.

        color = ka * 0.1
              + kd * max(dot(l, n), 0)
              + ks * max(dot(normalize(v + l), n), 0) ** p

    All of ``n``, ``v``, ``l`` may be single ``(3,)`` directions or ``(k, 3)``
    arrays of directions (normalize them internally). The material colours
    ``ka``, ``kd``, ``ks`` may be ``(3,)`` or ``(k, 3)``. The result broadcasts
    to ``(k, 3)`` (or ``(3,)`` for single-vector input).

    Parameters
    ----------
    ka, kd, ks : array_like
        Ambient, diffuse and specular RGB colours.
    p : float
        Specular exponent (shininess).
    n, v, l : array_like
        Unit surface normal, view and light directions.

    Returns
    -------
    ndarray
        RGB colour(s).
    """
    # TODO: normalize n, v, l; form the half vector h = normalize(v + l); and
    #       combine ambient (ka*0.1), diffuse (kd*max(dot(l,n),0)) and specular
    #       (ks*max(dot(h,n),0)**p) terms. Dot products are over the last axis.
    raise NotImplementedError("Implement blinn_phong")
