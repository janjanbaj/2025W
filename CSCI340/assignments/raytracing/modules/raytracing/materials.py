"""
Author: Liz Matthews, Geoff Matthews
"""

from typing_extensions import override
from ..utils.vector import vec


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


class Material3D(Material):
    def __init__(self, pattern, ambient, diffuse, specular, shine=100, specCoeff=1.0):
        super().__init__(ambient, diffuse, specular, shine, specCoeff)
        self.pattern = pattern

    def getAmbient(self, x, y, z):
        return self.pattern(x, y, z)
