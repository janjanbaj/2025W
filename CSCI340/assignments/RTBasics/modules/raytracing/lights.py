from abc import ABC, abstractmethod
import numpy as np


class AbstractLight(ABC):
    def __init__(self, color):
        self.color = color

    def getColor(self):
        """Returns the color of the light"""
        return self.color

    @abstractmethod
    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        pass

    @abstractmethod
    def getDistance(self, point):
        """Returns the distance to the light"""
        pass


class PointLight(AbstractLight):
    def __init__(self, point, color):
        super().__init__(color)
        self.point = np.array(point)

    def getVectorToLight(self, point):
        return self.point - np.array(point)

    def getDistance(self, point):
        return np.linalg.norm(point - self.point)


class DirectionalLight(AbstractLight):
    def __init__(self, ray, color):
        super().__init__(color)
        self.ray = ray

    def getVectorToLight(self):
        return self.ray * -1

    def getDistance(self):
        return 0
