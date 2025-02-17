from render import ProgressiveRenderer, ShowTypes
from modules.utils.noise import NoisePatterns
from modules.utils.vector import lerp, smerp
import numpy as np
import pygame
import random


class RandomRenderer(ProgressiveRenderer):
    def __init__(
        self,
        width=640,
        height=480,
        showTime=True,
        show=ShowTypes.PerColumn,
        minimumPixel=0,
        startPixelSize=256,
    ):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height, showTime, show, minimumPixel, startPixelSize)

    def getColor(self, x, y):
        """Gives a random color per pixel."""
        return np.array((random.random(), random.random(), random.random()))

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            type(self).restart()


class RainbowRenderer(ProgressiveRenderer):
    def __init__(
        self,
        width=640,
        height=480,
        showTime=True,
        show=ShowTypes.PerColumn,
        minimumPixel=0,
        startPixelSize=256,
    ):
        super().__init__(width, height, showTime, show, minimumPixel, startPixelSize)

        # list of lambda functions that have the render behaviors in order.

        self.renderMethods = [
            lambda x, y: x / self.width,
            lambda x, y: y / self.height,
            lambda x, y: 1 - x / self.width,
            lambda x, y: 1 - y / self.height,
        ]

        # (R,G,B) states in an array. Initialized to be consistent with lab requirements
        self.renderStates = [0, 1, 2]

    def getColor(self, x, y):
        return np.array([self.renderMethods[i](x, y) for i in self.renderStates])

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                type(self).restart()
            elif event.key == pygame.K_1:
                # add to state variable at the correct index such that index is within
                # the length of the list.
                self.renderStates[0] = (self.renderStates[0] + 1) % len(
                    self.renderMethods
                )
                type(self).restart()
            elif event.key == pygame.K_2:
                self.renderStates[1] = (self.renderStates[1] + 1) % len(
                    self.renderMethods
                )
                type(self).restart()
            elif event.key == pygame.K_3:
                self.renderStates[2] = (self.renderStates[2] + 1) % len(
                    self.renderMethods
                )
                type(self).restart()


class NoiseRenderer(ProgressiveRenderer):
    def __init__(
        self,
        width=640,
        height=480,
        showTime=True,
        show=ShowTypes.PerColumn,
        minimumPixel=0,
        startPixelSize=256,
    ):
        super().__init__(width, height, showTime, show, minimumPixel, startPixelSize)

        self.id = 0
        self.noiseMachine = NoisePatterns.getInstance()
        self.patterns = [
            self.noiseMachine.clouds,
            lambda x, y: self.noiseMachine.cloudsTiled(x, y, 3, 3),
            lambda x, y: self.noiseMachine.wood3D(x, y, 10, axis=2),
            lambda x, y: self.noiseMachine.wood(x, y, noiseStrength=0),
            lambda x, y: self.noiseMachine.fire(x, y, noiseStrength=0.6),
        ]

    def getColor(self, x, y, scale=64):
        x /= scale
        y /= scale
        noise = self.patterns[self.id](x, y)
        return noise

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                type(self).restart()
            elif event.key == pygame.K_q:
                self.id = (self.id - 1) % len(self.patterns)
                type(self).restart()
            elif event.key == pygame.K_w:
                self.id = (self.id + 1) % len(self.patterns)
                type(self).restart()
            elif event.key == pygame.K_e:
                self.noiseMachine.previous()
                type(self).restart()
            elif event.key == pygame.K_r:
                self.noiseMachine.next()
                type(self).restart()


# Calls the 'main' function when this script is executed
if __name__ == "__main__":
    try:
        # RandomRenderer.main()

        # RainbowRenderer.main()

        NoiseRenderer.main()

    finally:
        pygame.quit()
