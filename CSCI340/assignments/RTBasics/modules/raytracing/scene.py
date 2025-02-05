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
        light = PointLight(vec(1, 3, 0), vec(1, 1, 1))

        plane = Plane(
            vec(0, 1, 0),
            vec(0, -1, 0),
            Material(
                vec(0.3, 0.3, 0.3),
                vec(0.7, 0.7, 0.7),
                vec(1, 1, 1),
                5,
                0.1,
            ),
        )

        sphere1 = Sphere(
            0.7,
            vec(0, 1, -3),
            Material(vec(0.2, 0.2, 0.4), vec(0.2, 0.2, 1), (0.8, 0.8, 1), 5, 0.1),
        )
        sphere2 = Sphere(
            0.7,
            vec(-1, -0.2, -4),
            Material(vec(0.2, 0.4, 0.2), vec(0.2, 1, 0.2), (0.8, 1, 0.8), 100, 1.0),
        )
        sphere3 = Sphere(
            0.7,
            vec(1, 0, -2.3),
            Material(vec(0.4, 0.2, 0.2), vec(1.0, 0.2, 0.2), (1, 0.8, 0.8), 100, 1.0),
        )

        self.objects = [sphere3, sphere1, sphere2, plane]
        self.lights = [light]
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
