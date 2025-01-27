import pygame
import numpy as np


def makeColor(name):
    pyColor = pygame.Color(name)
    npColor = np.array(pyColor[:-1]) / 255
    return npColor


COLORS = {
    "blue": makeColor("blue"),
    "white": makeColor("white"),
    "black": makeColor("black"),
    "red": makeColor("red"),
    "yellow": makeColor("yellow"),
    "marble1": makeColor("seagreen1"),
    "marble2": makeColor("seagreen4"),
    "wood1": makeColor("sienna1"),
    "wood2": makeColor("sienna4"),
}

EPSILON = 1e-11
