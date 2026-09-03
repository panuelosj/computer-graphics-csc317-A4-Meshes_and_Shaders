import numpy as np


def triangle_area_normal(a, b, c):
    """Area-weighted normal of the triangle with corners ``a``, ``b``, ``c``.

    Returns ``0.5 * (b - a) x (c - a)``: a vector whose *direction* is the
    triangle's (right-hand-rule) unit normal and whose *length* equals the
    triangle's area.

    Parameters
    ----------
    a, b, c : (3,) array_like
        The three corner positions of the triangle (in order).

    Returns
    -------
    (3,) float ndarray
    """
    # TODO: return half the cross product of the two edge vectors (b-a), (c-a).
    raise NotImplementedError("Implement triangle_area_normal")
