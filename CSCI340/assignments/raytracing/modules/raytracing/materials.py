"""
Author: Liz Matthews, Geoff Matthews
"""

from numpy import clip
from typing_extensions import override
from ..utils.vector import vec

from pygame import image

# Must be less than 1
AMBIENT_MULTIPLE = 0.45

# Greater than 1
SPECULAR_MULTIPLE = 1.6


class Material(object):
    """A class to contain all properties of a material.
    Contains ambient, diffuse, specular colors.
    Contains shininess property.
    Contains specular coefficient."""

    def __init__(self, ambient, diffuse, specular, shine=100, specCoeff=1.0):
        self.ambient = vec(*ambient)
        self.diffuse = vec(*diffuse)
        self.specular = vec(*specular)
        self.shine = shine
        self.specCoeff = specCoeff

    def getAmbient(self):
        """Getter method for ambient color."""
        return vec(self.ambient)

    def getDiffuse(self):
        """Getter method for diffuse color."""
        return vec(self.diffuse)

    def getSpecular(self):
        """Getter method for specular color."""
        return vec(self.specular)

    def getShine(self):
        """Getter method for shininess factor."""
        return vec(self.shine)

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return vec(self.specCoeff)

    def getRecursiveRay(self):
        return False

    def getRefractive(self):
        return False


class MaterialMirror(Material):
    def __init__(
        self,
        ambient,
        diffuse,
        specular,
        reflective_factor=1.0,
        shine=100,
        specCoeff=1.0,
    ):
        super().__init__(ambient, diffuse, specular, shine, specCoeff)
        self.reflective_factor = reflective_factor

    def getRecursiveRay(self):
        return True


class MaterialRefractive(Material):
    def __init__(
        self,
        ambient,
        diffuse,
        specular,
        refractive_index=1.0,
        transparency_factor=1.0,
        shine=100,
        specCoeff=1.0,
    ):
        super().__init__(ambient, diffuse, specular, shine, specCoeff)
        self.refractive_index = refractive_index
        self.transparency_factor = transparency_factor

    def getRecursiveRay(self):
        return True

    def getRefractive(self):
        return True


class Material3D(object):
    def __init__(self, pattern, shine=100, specCoeff=1.0):
        self.pattern = pattern
        self.shine = shine
        self.specCoeff = specCoeff

    def getAmbient(self, x, y, z):
        return self.pattern(x, y, z) * AMBIENT_MULTIPLE

    def getDiffuse(self, x, y, z):
        """Getter method for diffuse color."""
        return self.pattern(x, y, z)

    def getSpecular(self, x, y, z):
        """Getter method for specular color."""
        return clip(self.pattern(x, y, z) * SPECULAR_MULTIPLE, 0.0, 1.0)

    def getShine(self):
        """Getter method for shininess factor."""
        return vec(self.shine)

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return vec(self.specCoeff)

    def getRecursiveRay(self):
        return False
