"""
Author: Liz Matthews, Geoff Matthews
"""

from numpy import cross, radians, tan
from numpy.linalg import norm

from .ray import Ray

from ..utils.vector import lerp, normalize, vec

from enum import Enum


class ProjectionType(Enum):
    Perspective = 1
    Orthographic = 2


class Camera(object):
    """Camera object for raytracing.
    Initialization camera pointing
    at an arbitrary plane focus. Can get position
    and obtain a ray based on a percentage along
    the x and y of the focus plane."""

    def set(
        self,
        focus=vec(0, 0.2, 0),
        fwd=vec(0, 0, -1),
        up=vec(0, 2, 0),
        fov=90.0,
        distance=2.5,
        aspect=4 / 3,
    ):
        """Sets up the camera given the parameters.
        Calculates position, ul, ur, ll, and lr."""
        # as per the slides
        fwd = self.fwd = normalize(fwd)
        up = normalize(up)
        right = normalize(cross(fwd, up))
        up = self.up = normalize(cross(right, fwd))

        # half because top down view
        width = 2 * distance * tan(radians(fov) / 2)
        height = width / aspect

        center = focus
        self.position = focus - distance * fwd
        self.distance = distance

        self.ul = center + height / 2 * up - (width / 2) * right
        self.ur = center + height / 2 * up + (width / 2) * right
        self.ll = center - height / 2 * up - (width / 2) * right
        self.lr = center - height / 2 * up + (width / 2) * right

    def __init__(
        self,
        focus=vec(0, 0, 0),
        fwd=vec(0, 0, -1),
        up=vec(0, 2, 0),
        fov=45.0,
        distance=2.5,
        aspect=4 / 3,
    ):
        self.set(focus, fwd, up, fov, distance, aspect)

    def getRay(self, xPercent, yPercent, projection=ProjectionType.Perspective):
        """Returns a ray based on a percentage for the x and y coordinate."""
        p0 = lerp(self.ul, self.ur, xPercent)
        p1 = lerp(self.ll, self.lr, xPercent)
        rayEndPoint = lerp(p0, p1, yPercent)
        if projection == ProjectionType.Perspective:
            return Ray(self.position, rayEndPoint - self.position)
        else:
            return Ray(self.position, rayEndPoint)

    def getPosition(self):
        """Getter method for position."""
        return self.position

    def getDistanceToFocus(self, point):
        """Getter method for distance from the given point to the center of focus."""
        focus = (self.ul + self.ur + self.ll + self.lr) / 4
        return norm(point - focus)
