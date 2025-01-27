"""
Author: Liz Matthews
Some interpolations and numpy-vector making functions.
"""

import numpy as np
from math import sqrt
from .definitions import EPSILON


def lerp(a, b, percent):
    """Linearly interpolate between a and b given a percent."""
    return (1.0 - percent)*a + percent*b

def smerp(a, b, percent):
    """Smooth interpolation."""
    percent = min(1.0, max(0.0, percent))
    smoothPercent = 3*percent**2 - 2*percent**3
    return a + smoothPercent*(b-a)

def vec(x, y=None, z=None):
    """Make a numpy vector of x, y, z."""
    if not(y is None) and not(z is None):
        return np.array((x,y,z), dtype=np.float32)
    else:
        return np.array(x, dtype=np.float32)
