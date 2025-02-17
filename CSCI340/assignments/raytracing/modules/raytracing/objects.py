"""
Author: Liz Matthews, Geoff Matthews
"""

import numpy as np
from abc import ABC, abstractmethod

from ..raytracing.materials import Material3D

from ..utils.definitions import EPSILON

from .ray import Ray
from ..utils.vector import normalize, rotate, vec
from numpy import cos, sin


def rotZ(x, y, z, theta):
    return (x * cos(theta) - y * sin(theta), x * sin(theta) + y * cos(theta), z)


def rotY(x, y, z, theta):
    return (x * cos(theta) - z * sin(theta), y, x * sin(theta) + z * cos(theta))


def rotX(x, y, z, theta):
    return (x, y * cos(theta) - z * sin(theta), y * sin(theta) + z * cos(theta))


def rot(x, y, z, xa, ya, za):
    rXx, rXy, rXz = rotX(x, y, z, xa)
    rYx, rYy, rYz = rotY(rXx, rXy, rXz, ya)
    return rotZ(rYx, rYy, rYz, za)


def invR(x, y, z, xa, ya, za):
    rZx, rZy, rZz = rotZ(x, y, z, -za)
    rYx, rYy, rYz = rotY(rZx, rZy, rZz, -ya)
    return rotX(rYx, rYy, rYz, -xa)


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
        # Citations/References:
        # https://stackoverflow.com/questions/28081247/print-real-roots-only-in-numpy
        # https://numpy.org/doc/2.2/reference/generated/numpy.where.html
        # https://stackoverflow.com/questions/59801341/how-to-use-np-max-for-empty-numpy-array-without-valueerror-zero-size-array-to-r
        p = ray.position - self.position
        v = ray.direction

        b = 2 * (p.dot(v))
        c = p.dot(p) - self.radius * self.radius

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


class SphereTextured3D(Sphere):
    def __init__(self, radius, pos, material: Material3D):
        self.position = pos
        self.radius = radius
        self.material = material

    def getAmbient(self, intersection):
        x, y, z = intersection
        return self.material.getAmbient(x, y, z)


class Plane(Object3D):
    def __init__(self, normal, pos, material):
        super().__init__(pos, material)
        self.normal = normalize(normal)

    def intersect(self, ray):
        dot = np.dot(ray.direction, self.normal)
        # if abs(dot) > 0.000000001:
        # return np.inf
        intersect = ((self.position - ray.position).dot(self.normal)) / (
            ray.direction.dot(self.normal)
        )
        if abs(intersect) > EPSILON:
            return intersect
        return np.inf

    def getNormal(self, intersection):
        return self.normal


class Ellipsoids(Object3D):
    def __init__(self, radius, pos, stretch, angle, material):
        super().__init__(pos, material)
        self.stretch = np.array(stretch)
        self.angle = np.array(angle)
        self.radius = radius

    def intersect(self, ray: Ray):
        p = ray.position - self.position
        p = invR(p[0], p[1], p[2], self.angle[0], self.angle[1], self.angle[2])
        v = invR(
            ray.direction[0],
            ray.direction[1],
            ray.direction[2],
            self.angle[0],
            self.angle[1],
            self.angle[2],
        )
        s = self.stretch

        vs = v / s
        ps = p / s

        a = vs.dot(vs)
        b = 2 * (vs.dot(ps))
        c = ps.dot(ps) - self.radius**2

        disc = (b * b) - (4 * a * c)

        sqrt_disc = np.sqrt(np.maximum(0, disc))

        sol_1 = (-b - sqrt_disc) / 2
        sol_2 = (-b + sqrt_disc) / 2

        hit_point = np.where((sol_1 > 0) & (sol_2 > sol_1), sol_1, sol_2)
        hit_bool = (disc > 0) & (hit_point > 0)
        return np.where(hit_bool, hit_point, np.inf)

    def getNormal(self, intersection):
        ax, ay, az = self.angle
        x, y, z = np.array(intersection - self.position)
        x, y, z = invR(x, y, z, ax, ay, az)
        x, y, z = np.array(
            [
                2 * [x, y, z][i] / ((self.radius**2) * (self.stretch[i] ** 2))
                for i in range(3)
            ]
        )
        # derivative = [
        #    2
        #    * (intersection[i] - self.position[i])
        #    / ((self.radius**2) * (self.stretch[i] ** 2))
        #    for i in range(3)
        # ]
        # return normalize(derivative)
        return normalize(rot(x, y, z, ax, ay, az))

        normal = np.array(
            [
                (2 * intersection[i] - self.position[i])
                / ((self.radius**2) * (self.stretch[i] ** 2))
                for i in range(3)
            ]
        )
        return normalize(normal)


class Cube(Object3D):
    def __init__(self, pos, forward, up, length, material):
        super().__init__(pos, material)
        self.last_intersection = None
        hl = length / 2
        self.length = length
        self.max_bounds = np.array([pos[i] + length / 2 for i in range(3)])
        self.min_bounds = np.array([pos[i] - length / 2 for i in range(3)])

        # Create orthogonal basis
        z_axis = normalize(up)
        y_axis = normalize(np.cross(up, forward))
        x_axis = normalize(forward)

        self.planes = [
            Plane(x_axis, pos + x_axis * hl, material),
            Plane(-x_axis, pos - x_axis * hl, material),
            Plane(y_axis, pos + y_axis * hl, material),
            Plane(-y_axis, pos - y_axis * hl, material),
            Plane(z_axis, pos + z_axis * hl, material),
            Plane(-z_axis, pos - z_axis * hl, material),
        ]

    def intersect(self, ray: Ray):
        entries = []
        maxEntry = -np.inf
        minExit = np.inf

        for surface in self.planes:
            # does the ray intersect with the given plane
            intersect = surface.intersect(ray)
            intersect_point = ray.getPositionAt(intersect)
            # if it doesnt we dont need to do the follows
            if intersect == np.inf:
                continue
            # check if exiting
            if surface.getNormal(intersect).dot(ray.direction) > EPSILON:
                # if exiting add to exit
                if intersect < minExit:
                    minExit = intersect
            else:
                entries.append(intersect)
                if intersect > maxEntry:
                    maxEntry = intersect
                    self.last_intersection = surface

        if len(entries) == 0:
            return np.inf
        if maxEntry < minExit:
            return maxEntry

        return np.inf

    def getNormal(self, intersection):
        return self.last_intersection.getNormal(intersection)
