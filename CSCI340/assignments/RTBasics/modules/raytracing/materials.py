"""
Author: Liz Matthews, Geoff Matthews
"""

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
        return self.ambient

    def getDiffuse(self):
        """Getter method for diffuse color."""
        return self.diffuse

    def getSpecular(self):
        """Getter method for specular color."""
        return self.specular

    def getShine(self):
        """Getter method for shininess factor."""
        return self.shine

    def getSpecularCoefficient(self):
        """Getter method for specular coefficient."""
        return self.specCoeff
