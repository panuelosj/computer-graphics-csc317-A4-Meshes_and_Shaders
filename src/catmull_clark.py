import numpy as np


def catmull_clark(V, F, num_iters):
    """Catmull-Clark subdivision of a pure-quad mesh.

    Each iteration:

    1. **Face points** -- the centroid of every quad.
    2. **Edge points** -- for an interior edge, the average of the edge's two
       endpoints and the two adjacent face points; for a boundary edge, the
       edge midpoint.
    3. **Updated vertex points** -- for an original vertex with valence ``k``::

           P' = (Q + 2R + (k - 3) P) / k

       where ``Q`` is the average of incident face points and ``R`` is the
       average of incident edge midpoints.
    4. **New faces** -- every quad becomes four quads, each joining an original
       (updated) corner, the next edge point, the face point, and the previous
       edge point.

    Repeating converges to a smooth limit surface.

    Parameters
    ----------
    V : (n, 3) float array
        Vertex positions.
    F : (m, 4) int array
        Quad faces.
    num_iters : int
        Number of subdivision iterations (``0`` returns the input unchanged).

    Returns
    -------
    SV : (N, 3) float ndarray
    SF : (4**num_iters * m, 4) int ndarray

    Notes
    -----
    The unit checks accept **any valid vertex/face ordering** — they compare
    sorted vertex coordinates and topology invariants, not raw array order.
    (For reference, the instructor solution orders each iteration's vertices
    as ``[updated originals | face points | edge points]``, with edge points
    indexed in order of first encounter and the four child quads of face ``f``
    stored at rows ``4f .. 4f+3``.)
    """
    # TODO: implement one subdivision step (face points, edge points, updated
    #       vertices, four child quads per face) and apply it num_iters times.
    raise NotImplementedError("Implement catmull_clark")
