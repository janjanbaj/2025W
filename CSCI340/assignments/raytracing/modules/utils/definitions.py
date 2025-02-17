import pygame
import numpy as np
    
def makeColor(name):
    pyColor = pygame.Color(name)
    npColor = np.array(pyColor[:-1]) / 255
    return npColor

def safeMultiply(vector, multiplier):
    newVector = vector * multiplier
    for index in range(len(newVector)):
        self[index] = max(0, min(1.0, newVector[index]))
    
    return newVector

COLORS = {
    "blue"    : makeColor("blue"),
    "white"   : makeColor("white"),
    "black"   : makeColor("black"),
    "red"     : makeColor("red"),
    "yellow"  : makeColor("yellow"),
    "marble1" : makeColor("seagreen1"),
    "marble2" : makeColor("seagreen4"),
    "wood1"   : makeColor("sienna1"),
    "wood2"   : makeColor("sienna4")
    
}

EPSILON = 1e-11
SHIFT_EPSILON = EPSILON * 100000
