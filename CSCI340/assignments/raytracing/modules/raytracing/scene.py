"""
Author: Liz Matthews, Geoff Matthews
"""

import numpy as np

from .objects import Sphere, Plane
from .camera import Camera
from ..utils.vector import vec
from .materials import Material
from .lights import PointLight


class Scene(object):
    """A class to contain all items in a scene.
    Contains a camera.
    Contains a list of lights.
    Contains a list of objects."""

    def __init__(
        self,
        focus=vec(0, 0.2, 0),
        direction=vec(0, 0, -1),
        up=vec(0, 1, 0),
        fov=45.0,
        distance=2.5,
        aspect=4 / 3,
    ):
        # Set up lights, spheres,  and planes here
        self.objects = []
        self.lights = []
        self.camera = Camera(focus, direction, up, fov, distance, aspect)

    def nearestObject(self, ray):
        """Returns the nearest collision object and the distance to the object."""
        distances = [o.intersect(ray) for o in self.objects]
        nearestObj = None
        minDistance = np.inf

        for i in range(len(distances)):
            if distances[i] < minDistance:
                nearestObj = self.objects[i]
                minDistance = distances[i]

        return nearestObj, minDistance

    def shadowed(self, obj, ray):
        """Returns the nearest collision object and the distance to the object,
        excluding obj."""
        distances = [o.intersect(ray) for o in self.objects if o is not obj]
        minDistance = np.inf
        for i in range(len(distances)):
            if distances[i] < minDistance:
                minDistance = distances[i]

        return minDistance
