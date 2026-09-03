import numpy as np

from .triangle_area_normal import triangle_area_normal


def per_face_normals(V, F):
    """Unit normal of every triangular face.

    Parameters
    ----------
    V : (n, 3) float array
        Vertex positions.
    F : (m, 3) int array
        Triangle vertex indices.

    Returns
    -------
    (m, 3) float ndarray
        ``N[f]`` is the unit normal of face ``f`` (the area-weighted normal
        ``triangle_area_normal`` produces, normalized to unit length).
    """
    # TODO: for each face, compute triangle_area_normal of its 3 corners and
    #       normalize it to unit length.
    raise NotImplementedError("Implement per_face_normals")
