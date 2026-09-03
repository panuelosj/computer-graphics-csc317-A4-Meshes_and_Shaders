import numpy as np

from .triangle_area_normal import triangle_area_normal


def per_vertex_normals(V, F):
    """Area-weighted per-vertex normals of a triangle mesh.

    Each vertex normal is the sum of the *area-weighted* normals of its
    incident faces, normalized to unit length::

        N_i = normalize( sum_{f in faces(i)} area(f) * normal(f) )

    Because ``triangle_area_normal`` already returns an area-weighted normal,
    accumulating those vectors at each incident corner and normalizing at the
    end yields exactly this weighting.

    Parameters
    ----------
    V : (n, 3) float array
    F : (m, 3) int array

    Returns
    -------
    (n, 3) float ndarray
    """
    # TODO: accumulate each face's triangle_area_normal at its 3 corner
    #       vertices, then normalize each vertex's accumulated vector.
    raise NotImplementedError("Implement per_vertex_normals")
