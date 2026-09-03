import numpy as np


def cube():
    """Construct the quad mesh of a unit cube.

    Returns
    -------
    V : (8, 3) float ndarray
        The eight corner positions of the cube ``[0,1]^3``.
    F : (6, 4) int ndarray
        The six quad faces, each a 0-indexed quadruple of corner indices wound
        consistently (so that ``triangle_area_normal`` of the first triangle of
        each quad points outward).

    Notes
    -----
    Draw the cube on paper and label the 8 corners; the unit tests check that
    the 6 quad faces are well-formed (no repeated corner, all 8 vertices used).
    """
    # TODO: return the 8 corner positions and 6 outward-wound quad faces.
    raise NotImplementedError("Implement cube")
