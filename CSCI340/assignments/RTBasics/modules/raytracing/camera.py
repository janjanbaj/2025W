"""
Author: Liz Matthews, Geoff Matthews
"""

from numpy.linalg import norm

from CSCI340.assignments.RTBasics.modules.raytracing.ray import Ray

from ..utils.vector import lerp, vec


class Camera(object):
    """Camera object for raytracing.
    Initialization camera pointing
    at an arbitrary plane focus. Can get position
    and obtain a ray based on a percentage along
    the x and y of the focus plane."""

    def set(
        self,
        focus=vec(0, 0, 0),
        fwd=vec(0, 0, -1),
        up=vec(0, 1, 0),
        fov=90.0,
        distance=2.5,
        aspect=4 / 3,
    ):
        """Sets up the camera given the parameters.
        Calculates position, ul, ur, ll, and lr."""

        self.position = vec(0, 0, 0)
        self.ul = vec(0, 0, 0)
        self.ur = vec(0, 0, 0)
        self.ll = vec(0, 0, 0)
        self.lr = vec(0, 0, 0)

    def __init__(
        self,
        focus=vec(0, 0, 0),
        fwd=vec(0, 0, -1),
        up=vec(0, 1, 0),
        fov=45.0,
        distance=2.5,
        aspect=4 / 3,
    ):
        self.set(focus, fwd, up, fov, distance, aspect)

    def getRay(self, xPercent, yPercent):
        """Returns a ray based on a percentage for the x and y coordinate."""
        p0 = lerp(self.ul, self.ur, xPercent)
        p1 = lerp(self.ll, self.lr, yPercent)
        worldPos = lerp(p0, p1, yPercent)

        return Ray(worldPos, worldPos - self.position)

    def getPosition(self):
        """Getter method for position."""
        return self.position

    def getDistanceToFocus(self, point):
        """Getter method for distance from the given point to the center of focus."""
        focus = (self.ul + self.ur + self.ll + self.lr) / 4
        return norm(point - focus)
