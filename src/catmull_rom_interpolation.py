import numpy as np


def catmull_rom_interpolation(keyframes, t):
    """Catmull-Rom interpolation of vec3 keyframes at time ``t``.

    ``keyframes`` is a list of ``(time, vec3)`` pairs, sorted by time. Find the
    keyframes ``k1`` (last one with ``time < t``) and ``k2 = k1 + 1`` that
    bracket ``t``. Outside the range (before the first keyframe or at/after the
    last) return the nearest endpoint value.

    With ``s`` the normalised parameter between ``k1`` and ``k2``, build the
    tangents as **centred differences** across each key's neighbours, scaled by
    ``tau = 0.5``::

        m_i = tau * (P_{i+1} - P_{i-1})

    which for this segment means::

        D1 = tau * (P_{k2}   - P_{k1-1})
        D2 = tau * (P_{k2+1} - P_{k1})

    At the ends of the sequence the missing neighbour is taken to be the
    endpoint itself (i.e. duplicate it), so the tangent becomes the one-sided
    ``tau * (P_{k2} - P_{k1})``: use that for ``D1`` when ``k1`` is the first
    keyframe, and for ``D2`` when ``k2`` is the last.

    Then evaluate the Hermite cubic with endpoints ``P1, P2`` and tangents
    ``D1, D2``::

        h00 = 2s^3 - 3s^2 + 1      h10 = s^3 - 2s^2 + s
        h01 = -2s^3 + 3s^2         h11 = s^3 - s^2

        p(s) = h00*P1 + h10*D1 + h01*P2 + h11*D2

    Return the interpolated 3-vector.

    Note both segments meeting at an interior key must derive that key's
    tangent the *same* way. That is what makes the curve C1 there -- position
    and velocity are both continuous -- so the motion is genuinely smooth
    rather than merely joined up. A one-sided tangent on either side would
    still pass through every key but would put a visible corner at each one.
    """
    # TODO: locate the bracketing keyframes, build the centred-difference
    # tangents, and evaluate the Hermite cubic.
    raise NotImplementedError("Implement catmull_rom_interpolation")
