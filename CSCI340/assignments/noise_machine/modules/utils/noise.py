"""
Author: Liz Matthews, Geoff Matthews
Noise manager class
"""

import numpy as np
from .vector import smerp, lerp
from .definitions import COLORS


class NoiseMachine:
    def __init__(
        self, noctaves=5, octaveDilation=2, minimum=0, maximum=1, nvalues=256, seed=1234
    ):
        self.noctaves = noctaves
        self.octaveDilation = octaveDilation
        self.nvalues = nvalues
        self.values = np.linspace(minimum, maximum, nvalues)
        self.permutations = np.arange(0, nvalues, 1)
        np.random.seed(seed)
        np.random.shuffle(self.values)
        np.random.shuffle(self.permutations)

    # One-dimensional noise
    def intNoise(self, i):
        return self.values[int(i) % self.nvalues]

    def smerpNoise(self, x):
        a = self.intNoise(np.floor(x))
        b = self.intNoise(np.ceil(x))
        xFrac = x - np.floor(x)
        return smerp(a, b, xFrac)

    def noise(self, x):
        s = 0.0
        for i in range(self.noctaves):
            s += self.smerpNoise(x * self.octaveDilation**i) / 2**i
        return s * 0.5

    # Two-dimensional noise
    def intNoise2d(self, i, j):
        """Given i and j, return a pseudo-random value.
        Uses permutations to shift i/j."""
        a = self.permutations[j % self.nvalues]
        b = self.permutations[(i + a) % self.nvalues]
        return self.values[b % self.nvalues]

    def smerpNoise2d(self, x, y):
        """Smoothly interpolate given two dimensional points."""
        i = int(np.floor(x))
        j = int(np.floor(y))
        xFrac = x - i
        yFrac = y - j

        # randoms at four corners:
        n00 = self.intNoise2d(i, j)
        n10 = self.intNoise2d(i + 1, j)
        n01 = self.intNoise2d(i, j + 1)
        n11 = self.intNoise2d(i + 1, j + 1)

        # smerp along x
        nx0 = smerp(n00, n10, xFrac)
        nx1 = smerp(n01, n11, xFrac)
        # smerp along y
        return smerp(nx0, nx1, yFrac)

    def noise2d(self, x, y):
        """Cumulative noise at x and y using smerp."""
        s = 0.0
        for i in range(self.noctaves):
            s += (
                self.smerpNoise2d(
                    x * self.octaveDilation**i, y * self.octaveDilation**i
                )
                / 2**i
            )
        return s * 0.5

    def noise2dTiled(self, x, y, xMod, yMod):
        """Cumulative noise at x and y using smerp, tilable."""
        s = 0.0
        for i in range(self.noctaves):
            s += (
                self.smerpNoise2dTiled(
                    x * self.octaveDilation**i,
                    y * self.octaveDilation**i,
                    xMod * self.octaveDilation**i,
                    yMod * self.octaveDilation**i,
                )
                / 2**i
            )
        return s * 0.5

    def smerpNoise2dTiled(self, x, y, xMod, yMod):
        """Smoothly interpolate given two dimensional points, tilable."""
        i = int(np.floor(x))
        j = int(np.floor(y))
        xFrac = x - i
        yFrac = y - j

        # randoms at four corners:
        n00 = self.intNoise2d(i % xMod, j % yMod)
        n10 = self.intNoise2d((i + 1) % xMod, j % yMod)
        n01 = self.intNoise2d(i % xMod, (j + 1) % yMod)
        n11 = self.intNoise2d((i + 1) % xMod, (j + 1) % yMod)

        # smerp along x
        nx0 = smerp(n00, n10, xFrac)
        nx1 = smerp(n01, n11, xFrac)
        # smerp along y
        return smerp(nx0, nx1, yFrac)


class NoisePatterns(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = NoisePatterns()
        return cls._instance

    def __init__(self):
        self.noiseId = 0
        self.scale = 50
        self.nms = [NoiseMachine(seed=i) for i in range(5)]

    def next(self):
        self.noiseId += 1
        self.noiseId %= len(self.nms)

    def previous(self):
        self.noiseId -= 1
        self.noiseId %= len(self.nms)

    def clouds(self, x, y, c1=COLORS["blue"], c2=COLORS["white"]):
        noise = self.nms[self.noiseId].noise2d(x, y)
        return lerp(c1, c2, noise)

    def cloudsTiled(self, x, y, xMod, yMod, c1=COLORS["blue"], c2=COLORS["white"]):
        noise = self.nms[self.noiseId].noise2dTiled(x, y, xMod, yMod)
        return lerp(c1, c2, noise)

    def marble(
        self, x, y, c1=COLORS["marble1"], c2=COLORS["marble2"], noiseStrength=0.2
    ):
        noise = self.nms[self.noiseId].noise2d(x, y)
        value = np.sin(x + y + (noise * noiseStrength * self.scale)) * 0.5 + 0.5
        return lerp(c1, c2, value)

    def wood(self, x, y, c1=COLORS["wood1"], c2=COLORS["wood2"], noiseStrength=0.2):
        noise = self.nms[self.noiseId].noise2d(x, y)
        radius = np.sqrt(x * x + y * y) * 10
        value = np.sin(radius + noise * noiseStrength * self.scale) * 0.5 + 0.5
        return lerp(c1, c2, value)

    def fire(self, x, y, c1=COLORS["red"], c2=COLORS["yellow"], noiseStrength=0.6):
        # divide the y-axis by 2
        y /= 2

        # get noise @ x^2,y^2 and interpolate between c1 and c2.
        color = lerp(c1, c2, self.nms[self.noiseId].noise2d(x * x, y * y))

        # calc the radius about a midpoint (4,3)
        radius = np.sqrt((x - 4) ** 2 + (y - 3) ** 2) / 4

        noise = self.nms[self.noiseId].noise2d(x + np.sin(y * 2) * 0.5, y)
        radius += (noise - 0.5) * noiseStrength
        colorMultiplier = 1.0 - smerp(0.1, 1.0, radius)

        return colorMultiplier * color
