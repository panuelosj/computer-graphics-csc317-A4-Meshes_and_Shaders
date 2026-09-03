import numpy as np


def write_obj(filename, V, F):
    """Write a pure-triangle or pure-quad mesh to a Wavefront ``.obj`` file.

    Parameters
    ----------
    filename : str
        Output path.
    V : (n, 3) float array
        Vertex positions, written as ``v x y z`` lines.
    F : (m, 3) or (m, 4) int array (or list of equal-length index lists)
        Faces, written as ``f i j k[ l]`` lines. Indices are stored
        **1-indexed** as the ``.obj`` format requires.

    Returns
    -------
    bool
        ``True`` on success.
    """
    # TODO: write one "v x y z" line per vertex, then one "f ..." line per face
    #       with each index incremented by 1 (.obj is 1-indexed). Support both
    #       triangle and quad faces.
    raise NotImplementedError("Implement write_obj")
