import numpy as np

from .triangle_area_normal import triangle_area_normal
from .vertex_triangle_adjacency import vertex_triangle_adjacency


def per_corner_normals(V, F, threshold_degrees):
    """Per-corner normals for a triangle mesh with crease detection.

    For every corner ``(f, c)`` we average the area-weighted normals of all
    faces incident on that corner's vertex *whose unit normal is within
    ``threshold_degrees`` of this face's unit normal*. This blends smooth
    regions like ``per_vertex_normals`` while keeping sharp creases crisp like
    ``per_face_normals``.

    Parameters
    ----------
    V : (n, 3) float array
    F : (m, 3) int array
    threshold_degrees : float
        Maximum angle (degrees) between two face normals for them to be
        averaged together.

    Returns
    -------
    (3*m, 3) float ndarray
        Row ``3*f + c`` is the unit normal at corner ``c`` of face ``f``.
    """
    # TODO: build the vertex-triangle adjacency and per-face area-weighted
    #       normals; for each corner, sum the area-weighted normals of incident
    #       faces whose UNIT normal has dot product > cos(threshold) with this
    #       face's unit normal, then normalize. Row index is 3*f + c.
    raise NotImplementedError("Implement per_corner_normals")
