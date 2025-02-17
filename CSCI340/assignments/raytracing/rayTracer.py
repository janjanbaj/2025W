"""
Author: Liz Matthews, Geoff Matthews
"""

import numpy as np
import pygame

from modules.utils.definitions import COLORS
from modules.utils.noise import NoisePatterns
from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.objects import Cube, Ellipsoids, Sphere, Plane, SphereTextured3D
from modules.raytracing.lights import PointLight
from modules.raytracing.materials import Material, Material3D
from modules.raytracing.scene import Scene
from modules.utils.vector import normalize, vec
from modules.raytracing.ray import Ray


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=900, height=700, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.7, 0.9, 1.0)
        self.scene = Scene(aspect=width / height, fov=45)

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
        nm = NoisePatterns()

        cube1 = Cube(
            vec(-1.3, 1.4, -4),
            vec(0, 0, 1),
            0.02,
            Material(vec(0.2, 0.2, 0.4), vec(0.2, 0.2, 1), (0.8, 0.8, 1), 5, 0.1),
        )
        ellipsoid = Ellipsoids(
            0.4,
            vec(-1.3, 1.4, -4),
            vec(1.58, 1, 1),
            vec(0.1, 0.2, 0.3),
            Material(vec(0.2, 0.4, 0.2), vec(0.2, 1, 0.2), (0.8, 1, 0.8), 100, 1.0),
        )
        sphere1 = SphereTextured3D(
            0.7,
            vec(0, 1, -3),
            Material3D(
                nm.clouds3D,
                COLORS["blue"],
                COLORS["blue"] * 1.10,
                (0.8, 0.8, 1),
                1,
                0.5,
            ),
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
        self.scene.objects = [ellipsoid, cube1, sphere1, sphere2, sphere3, plane]
        self.scene.lights = [light]

    def getColorR(self, ray: Ray):
        # Find any objects it collides with and calculate color
        obj, distance_to_obj = self.scene.nearestObject(ray)

        # Return fog if doesn't hit anything
        if obj is None:
            return self.fog

        intersection = ray.getPositionAt(distance_to_obj)

        # implement lambertian diffuse
        # the light energy given off ie. the diffuse amt is proportional to the cosine
        if type(obj == SphereTextured3D):
            color = obj.getAmbient(intersection)
        else:
            color = obj.getAmbient()

        object_normal = obj.getNormal(intersection)

        for l in self.scene.lights:
            light_vector = l.getVectorToLight(intersection)

            if self.scene.shadowed(obj, Ray(l.point, -light_vector)) >= l.getDistance(
                intersection
            ):
                # only do this if not blocked
                diffuse = (obj.getDiffuse() - color) * max(
                    np.dot(object_normal, light_vector), 1e-13
                )

                color += diffuse
                reflection_vector = normalize(light_vector - ray.direction)

                specular = (obj.getSpecular() - color) * (
                    (np.dot(reflection_vector, object_normal) ** obj.getShine())
                    * obj.getSpecularCoefficient()
                )

                color += specular

        return color

        # return (
        #    obj.getShine() * (obj.getAmbient() - obj.getDiffuse())
        # ) + obj.getDiffuse()

    def getColor(self, x, y):
        # Calculate the percentages for x and y

        xPercent = x / self.width
        yPercent = y / self.height

        # Get the ray from the camera
        cameraRay = self.scene.camera.getRay(xPercent, yPercent)

        # Get the color based on the ray
        color = self.getColorR(cameraRay)

        # Fixing any NaNs in numpy, clipping to 0, 1.
        color = np.nan_to_num(np.clip(color, 0, 1), 0)

        return color


# Calls the 'main' function when this script is executed
if __name__ == "__main__":
    RayTracer.main("Ray Tracer Basics")
    pygame.quit()
