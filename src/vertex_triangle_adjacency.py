import numpy as np


def vertex_triangle_adjacency(F, num_vertices):
    """Build the vertex-to-face adjacency list of a mesh.

    Parameters
    ----------
    F : (m, k) int array
        Face vertex indices (triangles, quads, ... — any fixed arity ``k``).
    num_vertices : int
        Number of vertices in the mesh.

    Returns
    -------
    list of list of int
        ``VF[v]`` is the list of face indices incident on vertex ``v``, in the
        order the faces are visited. Vertices with no incident face get ``[]``.
    """
    # TODO: start with an empty list per vertex, then for every corner of every
    #       face append that face's index to the corner vertex's list.
    raise NotImplementedError("Implement vertex_triangle_adjacency")
