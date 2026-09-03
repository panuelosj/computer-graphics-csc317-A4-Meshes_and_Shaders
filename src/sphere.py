import numpy as np


def sphere(num_u, num_v):
    """Construct a latitude-longitude quad mesh of the unit sphere.

    The sphere is swept with ``num_u`` quads around the equator (longitude) and
    ``num_v`` quads from pole to pole (latitude). Longitudinal seams are sewn
    shut by wrapping the ``u`` index, and the top/bottom rings collapse to a
    single pole vertex each, so the result is a closed (watertight) surface
    whose vertices all lie exactly on the unit sphere.

    Parameters
    ----------
    num_u : int
        Number of faces around the equator (>= 3).
    num_v : int
        Number of faces from pole to pole (>= 2).

    Returns
    -------
    V : (1 + num_u*(num_v-1) + 1, 3) float ndarray
        Vertex positions on the unit sphere: the bottom pole ``(0,-1,0)`` at
        index 0, then the interior latitude rings, then the top pole
        ``(0,+1,0)`` at the last index.
    F : (num_u*num_v, 4) int ndarray
        Quad faces.

    Notes
    -----
    For a parameter point ``(u/num_u, v/num_v)`` use the angles
    ``phi = 2*pi - 2*(u/num_u)*pi`` and ``theta = pi - (v/num_v)*pi`` and the
    point ``(sin(theta)cos(phi), cos(theta), sin(theta)sin(phi))``. Wrap the
    ``u`` index modulo ``num_u`` and clamp the pole rings to the single bottom
    (index 0) and top (last index) vertices.
    """
    # TODO: build the (num_u*num_v, 4) face array (wrapping u, clamping poles)
    #       and place each referenced vertex on the unit sphere using the
    #       phi/theta formulas above.
    raise NotImplementedError("Implement sphere")
