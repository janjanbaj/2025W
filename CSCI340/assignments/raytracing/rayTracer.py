"""
Author: Liz Matthews, Geoff Matthews

"""

import numpy as np
import pygame

from modules.utils.definitions import COLORS, EPSILON
from modules.utils.noise import NoisePatterns
from render import ProgressiveRenderer, ShowTypes

from modules.raytracing.objects import (
    Cube,
    Ellipsoids,
    EllipsoidsTextured3D,
    PlaneTextured3D,
    Sphere,
    Plane,
    SphereTextured3D,
    CubeTextured3D,
    TexturedCube,
    TexturedPlane,
    TexturedSphere,
)
from modules.raytracing.lights import DirectionalLight, PointLight
from modules.raytracing.materials import (
    Material,
    Material3D,
    MaterialMirror,
    MaterialRefractive,
)
from modules.raytracing.scene import Scene
from modules.utils.vector import lerp, normalize, vec
from modules.raytracing.ray import Ray
from quilt import *

RECURSIVE_RAY_LIMIT = 9


class RayTracer(ProgressiveRenderer):
    def __init__(self, width=800, height=800, show=ShowTypes.PerColumn):
        super().__init__(width, height, show=show)
        self.fog = vec(0.627, 0.827, 0.929)
        self.scene = Scene(aspect=width / height, fov=35.0)
        self.enter_index = 1.0

        self.nm = nm = NoisePatterns()

        light = PointLight(vec(1, 2, 0), vec(1, 1, 1))

        floor = TexturedPlane(
            vec(0, 1, 0),
            vec(0, -1, 0),
            "./textures/floor.jpg",
            scale_u=6.0,
            scale_v=6.0,
        )

        sky = PlaneTextured3D(
            vec(0, -21, 0),
            vec(0, 5, -1),
            Material3D(lambda x, y, z: nm.clouds3D(x, y, z, c1=self.fog * 1.0), 0, 0),
        )
        sky.hittable = False

        cube1 = Cube(
            vec(-1.5, 2, -4),
            vec(-0.3, 1, 0),
            vec(0.3, 0, 0),
            0.5,
            Material(vec(0.4, 0.2, 0.2), vec(1.0, 0.2, 0.2), (1, 0.8, 0.8), 100, 1.0),
        )

        # sphere1 = SphereTextured3D(
        #    0.7,
        #    vec(0, 1, -3),
        #    Material3D(
        #        lambda x, y, z: nm.marble3D(x, z, y, noiseStrength=0.6) * 0.5,
        #        1,
        #        0.5,
        #    ),
        # )
        # sphere3 = SphereTextured3D(
        #     0.7,
        #     vec(1, 0, -4.3),
        #     Material3D(
        #         lambda x, y, z: nm.wood3D(x, y, z, axis=3, noiseStrength=0.7),
        #         1,
        #         1.0,
        #     ),
        # )

        earth = TexturedSphere(
            5.0,
            self.scene.camera.getPosition()
            + (2 * self.scene.camera.fwd)
            + (9 * self.scene.camera.up),
            "./textures/earth.png.jpg",
            vec(0, -1, 0),
            vec(0, -1, 0),
        )

        dice = TexturedCube(
            vec(-1, 1.2, -5),
            vec(0.3, 2, 0),
            vec(0.5, 0, 1),
            1.0,
            "./die/die1.png",
            "./die/die2.png",
            "./die/die3.png",
            "./die/die4.png",
            "./die/die5.png",
            "./die/die6.png",
        )

        eye = TexturedSphere(
            2.0,
            self.scene.camera.getPosition()
            - (2 * self.scene.camera.fwd)
            + (1 * self.scene.camera.up),
            "./textures/eye.webp",
            vec(0, -1, 0),
            vec(42, 0, 3),
        )

        sphere_mirror = Sphere(
            0.65,
            vec(1.2, 1, -3),
            MaterialMirror(
                vec(0.5, 0.5, 0.5),
                vec(0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5),
            ),
        )

        refractive_sphere = Sphere(
            0.35,
            vec(0, 0.4, -3),
            MaterialRefractive(
                vec(0.5, 0.5, 0.5),
                vec(0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5),
                refractive_index=1.23,
            ),
        )
        floor.hittable = True

        self.scene.objects = [sky, floor, refractive_sphere, sphere_mirror, eye, dice]
        self.scene.lights = [light]

    def getColorR(self, ray: Ray, r_level=0):
        # Find any objects it collides with and calculate color

        obj, distance_to_obj = self.scene.nearestObject(ray)

        # Return fog if doesn't hit anything
        if obj is None:
            return self.fog

        intersection = ray.getPositionAt(distance_to_obj)

        object_normal = normalize(obj.getNormal(intersection))

        # the light energy given off ie. the diffuse amt is proportional to the cosine

        if not obj.hittable:
            return obj.getDiffuse(intersection)

        color = obj.getAmbient(intersection)

        for l in self.scene.lights:
            light_vector = l.getVectorToLight(intersection)

            if self.scene.shadowed(obj, Ray(l.point, -light_vector)) >= l.getDistance(
                intersection
            ):
                # only do this if not blocked
                diffuse = (obj.getDiffuse(intersection) - color) * max(
                    np.dot(object_normal, light_vector), 1e-13
                )

                color += diffuse
                reflection_vector = normalize(light_vector - ray.direction)

                specular = (obj.getSpecular(intersection) - color) * (
                    (np.dot(reflection_vector, object_normal) ** obj.getShine())
                    * obj.getSpecularCoefficient()
                )

                color += specular

        if obj.material.getRecursiveRay() and r_level < RECURSIVE_RAY_LIMIT:
            # per the slides simplified because j = a -i and j -i = a -2 i:
            reflection_vector = (
                ray.direction - 2 * np.dot(ray.direction, object_normal) * object_normal
            )

            # bigger epsilon
            reflection_ray = Ray(
                (intersection + (0.001 * reflection_vector)), reflection_vector
            )
            reflecton_color = self.getColorR(reflection_ray, r_level + 1)

            if obj.material.getRefractive():
                n_r = 1.0
                n_t = obj.material.refractive_index

                u_r = ray.direction
                n = object_normal

                entering_exiting = np.dot(u_r, n)

                # check if we are entering something or leaving something:
                if entering_exiting > 0.001:
                    # if we are leaving the object then the current object is the
                    # transimitting medium
                    n_r, n_t = n_t, n_r
                    n = -n

                cos_theta = np.dot(-u_r, n)
                n_ratio = n_r / n_t

                cos_phi = 1 - (n_ratio * n_ratio) * (1 - (cos_theta) ** 2)

                if cos_phi < 0.001:
                    # Total internal reflection occurs so just reflection.

                    reflection_vector = u_r - 2 * np.dot(u_r, n) * n
                    new_ray = Ray(
                        (intersection + (EPSILON * reflection_vector)),
                        reflection_vector,
                    )

                else:
                    u_t = (n_ratio * cos_theta - np.sqrt(cos_phi)) * n + n_ratio * u_r

                    new_ray = Ray(intersection + (0.01 * u_t), u_t)

                refractive_color = self.getColorR(new_ray, r_level=r_level + 1)

                refractive_color = lerp(
                    obj.getAmbient(), refractive_color, obj.material.transparency_factor
                )

                # cos_theta = max(
                #    [np.dot(u_r, -n), np.dot(new_ray.direction, -n)],
                #    key=lambda x: np.arccos(x),
                # )

                R_0 = ((n_r - n_t) / (n_r + n_t)) ** 2

                R_theta = R_0 + (
                    (1 - R_0)
                    * ((1 - np.abs(np.dot(ray.direction, object_normal))) ** 5)
                )

                return lerp(refractive_color, reflecton_color, R_theta)
            else:
                return lerp(color, reflecton_color, obj.material.reflective_factor)

        return color

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


# Calls the 'main' function when this script is execute
if __name__ == "__main__":
    RayTracer.main("Ray Tracer Basics")
    pygame.quit()
