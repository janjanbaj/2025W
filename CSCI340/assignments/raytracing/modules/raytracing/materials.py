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


class Material3D(object):
    def __init__(self, ambient, diffuse, specular, shine=100, specCoeff=1.0):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shine = shine
        self.specCoeff = specCoeff
        self.ambient = ambient

    def getAmbient(self, x, y, z):
        return self.ambient(x, y, z)

    def getDiffuse(self, x, y, z):
        """Getter method for diffuse color."""
        return self.diffuse(x, y, z)

    def getSpecular(self, x, y, z):
        """Getter method for specular color."""
        return self.specular(x, y, z)

    def getShine(self):
        """Getter method for shininess factor."""
        return vec(self.shine)

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return vec(self.specCoeff)
