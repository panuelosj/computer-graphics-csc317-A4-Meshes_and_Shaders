import numpy as np

from backend.noise import perlin_noise


def bump_height(s):
    """Procedural bump height (displacement along the normal) at points ``s``.

    Sum several octaves of Perlin noise into a small signed elevation (values
    roughly in ``[-0.1, 0.1]``). Accept a single ``(3,)`` point or a ``(k, 3)``
    array and return a scalar or ``(k,)`` accordingly.

    Use exactly this octave combination (the unit checks compare against it)::

        height = 0.08 * (  0.6   * perlin_noise( 2 * s)
                         + 0.2   * perlin_noise( 4 * s)
                         + 0.2   * perlin_noise( 8 * s)
                         - 0.005 * perlin_noise(64 * s) )

    (The weights are fixed here so the result can be
    auto-graded. Feel free to play with them in ``main.py --mode shade`` after
    the checks pass.)
    """
    # TODO: implement the octave sum documented above.
    raise NotImplementedError("Implement bump_height")


def bump_position(s):
    """Displace surface points ``s`` along their (unit-sphere) normal.

    For a point on the unit sphere the position equals its normal, so the
    displaced position is ``s + bump_height(s) * s``.
    """
    # TODO: return s + bump_height(s)[:, None] * s.
    raise NotImplementedError("Implement bump_position")


def tangent(N):
    """Build an orthonormal tangent frame ``(T, B)`` for unit normals ``N``.

    ``T`` is ``x = (1,0,0)`` projected onto the tangent plane and normalized;
    ``B = N x T``. Where ``N`` is (nearly) parallel to ``x`` (if |N·x| > 0.99), 
    use ``y = (0,1,0)`` instead so the frame stays well-defined. 
    Accept ``(3,)`` or ``(k, 3)``.

    Returns
    -------
    (T, B) : tuple of ndarray
        Orthonormal tangent and bitangent, same shape as ``N``.
    """
    # TODO: T = normalize(a - dot(N, a) N) for a reference axis a; B = cross(N, T).
    raise NotImplementedError("Implement tangent")


def perturbed_normal(points, eps=1e-4):
    """Normals of the bumped surface, via finite differences of ``bump_position``.

    For each surface point (assumed on the unit sphere, so position == normal)
    step a tiny amount ``eps`` along the two tangent directions, displace both
    stepped points with :func:`bump_position`, and take the normalized cross
    product of the resulting edge vectors as the perceived normal::

        n = normalize( (bp(p + eps*T) - bp(p)) x (bp(p + eps*B) - bp(p)) )

    Parameters
    ----------
    points : (k, 3) array_like  (a single ``(3,)`` point is also accepted)
    eps : float
        Finite-difference step.

    Returns
    -------
    (k, 3) float ndarray  (or ``(3,)`` for a single point)
        Unit perturbed normals.
    """
    # TODO: build the tangent frame, displace p, p+eps*T, p+eps*B with
    #       bump_position, and return the normalized cross product of the two
    #       finite-difference edge vectors.
    raise NotImplementedError("Implement perturbed_normal")
