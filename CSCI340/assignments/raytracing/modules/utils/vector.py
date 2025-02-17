"""
Author: Liz Matthews, Geoff Matthews
"""

import numpy as np
from math import sqrt


def magnitude(vector):
    """Give the magnitude of a vector."""
    return np.linalg.norm(vector)


def normalize(vector):
    """Normalize a numpy array."""
    mag = magnitude(vector)
    if mag == 0.0:
        return vec(1, 0, 0)
    return vector / mag


def lerp(a, b, percent):
    """Linearly interpolate between a and b given a percent."""
    return (1.0 - percent) * a + percent * b


def smerp(a, b, percent):
    """Smooth interpolation."""
    percent = min(1.0, max(0.0, percent))
    smoothPercent = 3 * percent**2 - 2 * percent**3
    return a + smoothPercent * (b - a)


def vec(x, y=None, z=None):
    """Make a numpy vector of x, y, z."""
    if not (y is None) and not (z is None):
        return np.array((x, y, z), dtype=np.float32)
    else:
        return np.array(x, dtype=np.float32)


def posDot(v, w):
    dot = np.dot(v, w)
    return max(0.0, dot)


def rotate(v, axis, radians):
    R = rotation_matrix(axis, radians)
    return np.dot(R, v)


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array(
        [
            [aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc],
        ]
    )
