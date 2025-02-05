"""
Author: Liz Matthews, Geoff Matthews
"""

import numpy as np
from abc import ABC, abstractmethod

from .ray import Ray
from ..utils.vector import normalize, vec


class Object3D(ABC):
    """Abstract base class for all objects in the raytraced scene.
    Has a position, material.
    Has getter methods for all material properties.
    Has abstract methods intersect and getNormal."""

    def __init__(self, pos, material):
        self.position = np.array(pos)
        self.material = material

    def getAmbient(self, intersection=None):
        """Getter method for the material's ambient color.
        Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getAmbient()

    def getDiffuse(self, intersection=None):
        """Getter method for the material's diffuse color.
        Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getDiffuse()

    def getSpecular(self, intersection=None):
        """Getter method for the material's specular color.
        Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getSpecular()

    def getShine(self):
        """Getter method for the material's shininess factor."""
        return self.material.getShine()

    def getSpecularCoefficient(self, intersection=None):
        """Getter method for the material's specular coefficient.
        Intersection parameter is unused for Ray Tracing Basics."""
        return self.material.getSpecularCoefficient()

    @abstractmethod
    def intersect(self, ray):
        """Find the intersection for the given object. Must override."""
        pass

    @abstractmethod
    def getNormal(self, intersection):
        """Find the normal for the given object. Must override."""
        pass


class Sphere(Object3D):
    def __init__(self, radius, pos, material):
        super().__init__(pos, material)
        self.radius = radius

    def intersect(self, ray: Ray):
        p = ray.position - self.position
        v = ray.direction

        b = 2 * (p.dot(v))
        c = p.dot(p) - self.radius * self.radius

        # numpy wizardy commences:

        # discriminant b^2-4ac
        disc = (b * b) - (4 * c)

        # sqrt_discriminant for calculations. if disc is lt 0 then disc is zero.
        sqrt_disc = np.sqrt(np.maximum(0, disc))

        # plus-minus
        sol_1 = (-b - sqrt_disc) / 2
        sol_2 = (-b + sqrt_disc) / 2

        # the following is an optimization on the if conditions. we first check if the subtracted solution that is sol_1 is negative, if so we will pick the other one which we deal with later. if sol1 is smaller than sol2, pick sol1 because it is closer
        hit_point = np.where((sol_1 > 0) & (sol_2 > sol_1), sol_1, sol_2)
        # if discriminant is non zero then there is for sure an intersection. if not then we did not hit the sphere. if the hit point is not positive then we basically hit it tangentially and can return inf
        hit_bool = (disc > 0) & (hit_point > 0)
        return np.where(hit_bool, hit_point, np.inf)

    def getNormal(self, intersection):
        return normalize(vec(intersection - self.position))


class Plane(Object3D):
    def __init__(self, normal, pos, material):
        super().__init__(pos, material)
        self.normal = normalize(normal)

    def intersect(self, ray):
        dot = np.dot(ray.direction, self.normal)
        if dot > 0.000000001:
            return np.inf
        return ((self.position - ray.position).dot(self.normal)) / (
            ray.direction.dot(self.normal)
        )

    def getNormal(self, intersection):
        return self.normal
