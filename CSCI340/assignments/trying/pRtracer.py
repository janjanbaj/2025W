import matplotlib.pyplot as plt

import numpy as np
import numba
from numba import jit, prange, float32
from numba.experimental import jitclass

# Define Sphere struct for Numba compatibility
spec = [
    ("center", float32[:]),
    ("radius", float32),
    ("color", float32[:]),
    ("reflection", float32),
]


@jitclass(spec)
class Sphere:
    def __init__(self, center, radius, color, reflection=0.5):
        self.center = np.array(center, dtype=np.float32)
        self.radius = radius
        self.color = np.array(color, dtype=np.float32)
        self.reflection = reflection


@jit(nopython=True)
def intersect_sphere(origin, direction, sphere):
    oc = origin - sphere.center
    a = np.dot(direction, direction)
    b = 2.0 * np.dot(oc, direction)
    c = np.dot(oc, oc) - sphere.radius * sphere.radius
    discriminant = b * b - 4 * a * c
    if discriminant > 0:
        t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)
        if t1 > 0:
            return t1
        if t2 > 0:
            return t2
    return np.inf


@jit(nopython=True)
def compute_lighting(point, normal, light_pos):
    light_dir = light_pos - point
    light_dir /= np.linalg.norm(light_dir)
    return max(np.dot(normal, light_dir), 0.0)


@jit(nopython=True)
def is_in_shadow(point, light_pos, spheres):
    light_dir = light_pos - point
    light_dir /= np.linalg.norm(light_dir)

    for sphere in spheres:
        if intersect_sphere(
            point + light_dir * 0.001, light_dir, sphere
        ) < np.linalg.norm(light_pos - point):
            return True
    return False


@jit(nopython=True, parallel=True)
def render_scene(spheres, width, height, camera, light_pos):
    aspect_ratio = width / height
    image = np.zeros((height, width, 3), dtype=np.float32)

    for y in prange(height):
        for x in range(width):
            px = (2 * (x + 0.5) / width - 1) * aspect_ratio
            py = 1 - 2 * (y + 0.5) / height
            ray_dir = np.array([px, py, -1], dtype=np.float32)
            ray_dir /= np.linalg.norm(ray_dir)

            min_t = np.inf
            hit_color = np.array([0, 0, 0], dtype=np.float32)
            hit_point = None
            hit_normal = None

            for sphere in spheres:
                t = intersect_sphere(camera, ray_dir, sphere)
                if t < min_t:
                    min_t = t
                    hit_point = camera + t * ray_dir
                    hit_normal = (hit_point - sphere.center) / sphere.radius
                    hit_color = sphere.color

            if hit_point is not None:
                if is_in_shadow(hit_point, light_pos, spheres):
                    hit_color *= 0.2  # Darken if in shadow
                else:
                    lighting = compute_lighting(hit_point, hit_normal, light_pos)
                    hit_color *= lighting

            image[y, x] = hit_color

    return image


class RayTracer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.spheres = []
        self.camera = np.array([0, 0, 0], dtype=np.float32)
        self.light_pos = np.array([5, 5, -5], dtype=np.float32)  # Single light source

    def add_sphere(self, center, radius, color, reflection=0.5):
        self.spheres.append(Sphere(center, radius, color, reflection))

    def render(self):
        return render_scene(
            self.spheres, self.width, self.height, self.camera, self.light_pos
        )


# Create a RayTracer instance
tracer = RayTracer(800, 600)

# Add spheres to the scene
tracer.add_sphere(center=[0, 0, -5], radius=1, color=[1, 0, 0])  # Red sphere
tracer.add_sphere(center=[2, 0, -5], radius=1, color=[0, 1, 0])  # Green sphere
tracer.add_sphere(center=[-2, 0, -5], radius=1, color=[0, 0, 1])  # Blue sphere

# Render the image
image = tracer.render()

# Display the image using Matplotlib
plt.imshow(image)
plt.axis("off")  # Hide axes
plt.show()
