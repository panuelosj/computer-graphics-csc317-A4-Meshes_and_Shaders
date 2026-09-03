import numpy as np


def translate(t):
    """4x4 homogeneous matrix that translates a 3D point by ``t``."""
    # TODO: return a 4x4 identity with t placed in the last column (rows 0..2).
    raise NotImplementedError("Implement translate")


def uniform_scale(s):
    """4x4 homogeneous matrix that scales all three axes by ``s``."""
    # TODO: return diag(s, s, s, 1).
    raise NotImplementedError("Implement uniform_scale")


def rotate_about_y(theta):
    """4x4 homogeneous matrix that rotates about the y-axis by ``theta`` radians.

        R_y = [[ cos, 0, sin, 0],
               [   0, 1,   0, 0],
               [-sin, 0, cos, 0],
               [   0, 0,   0, 1]]
    """
    # TODO: return the y-axis rotation matrix shown above.
    raise NotImplementedError("Implement rotate_about_y")


def model_view_projection(model, view, proj, positions):
    """Project vertex positions through the model-view-projection pipeline.

    Computes ``proj @ view @ model @ [x, y, z, 1]`` for every input position,
    leaving the result in homogeneous clip coordinates (no perspective
    division), exactly as a vertex shader does.

    Parameters
    ----------
    model, view, proj : (4, 4) array_like
        The model, view and projection matrices.
    positions : (k, 3) array_like
        Vertex positions in object space.

    Returns
    -------
    (k, 4) float ndarray
        Homogeneous clip-space positions.
    """
    # TODO: form M = proj @ view @ model, append a 1 to each position, and
    #       return the (k, 4) homogeneous result (no division by w).
    raise NotImplementedError("Implement model_view_projection")
