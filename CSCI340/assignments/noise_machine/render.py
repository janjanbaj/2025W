# -*- coding: utf-8 -*-
"""
Authors: Liz Matthews, Geoff Matthews

Code to progressively render an image with smaller and smaller pixels.
To use for a different project, extend ProgressivePixelRenderer and
override getColor().
"""

import os, pygame, time, random
import numpy as np
from pygame.locals import *
from enum import Enum
from abc import ABC, abstractmethod

class ShowTypes(Enum):
    """Control for how the progressive pixel renderer shows images.
    More showing will be slower, NoShow doesn't show the image until
    done."""

    PerPixel = 0
    PerColumn = 1
    PerImage = 2
    FinalShow = 3
    NoShow = 4

class ProgressiveRenderer(ABC):
    """Abstract base class for renderers."""       
    @classmethod
    def main(cls, caption="Renderer"):
        """General main loop for the progressive renderer.
        Sets up pygame and everything necessary."""

        # Initialize Pygame
        pygame.init()

        # Set up renderer        
        cls.renderer = cls()
        cls.renderer.startPygame(caption)
        cls.stepper = cls.renderer.render()

        # Main loop
        while cls.renderer.isRunning():
            # If the renderer has work to do, let it
            if not cls.renderer.done:
                next(cls.stepper)

    @classmethod
    def restart(cls):
        """Used to restart the progressive rendering from the
        initial pixel size."""
        
        cls.stepper.close()
        cls.renderer.restartRender()
        cls.stepper = cls.renderer.render()
        
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256): 
            
        self.width = width
        self.height = height
        self.showTime = showTime
        self.minimumPixel = minimumPixel        
        self.screen = None
        self.fillColor = (64, 128, 255)
        
     
        self.show = show
        
        # Set up pixel size to minimum if NoShow or FinalShow are selected
        if self.show in [ShowTypes.NoShow, ShowTypes.FinalShow]:
            self.startPixelSize = max(1, minimumPixel * 2)
        else:
            self.startPixelSize = startPixelSize
            
        # Find file name for image if NoShow is selected
        if self.show == ShowTypes.NoShow:
            self.fileName = input("File name?: ")
        else:
            self.fileName = None
    
    @abstractmethod
    def getColor(self, x, y):
        """Must return a color in a np.array() in 255 mode."""
        return np.array((0,0,255))
    
    def handleExitInput(self, event):
        """For exiting the program."""
        if event.type == QUIT:
            return True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
        return False

    def handleSaveInput(self, event):
        """The key s will save the file."""
        if event.type == KEYDOWN and event.key == K_s:
            self.save()

    def handleOtherInput(self, event):
        """For handling other inputs, override for new behaviors"""
        pass

    def handleInput(self):
        """Checks the event queue."""
        for event in pygame.event.get():
            exitRender = self.handleExitInput(event)
            if exitRender:
                return True

            self.handleSaveInput(event)
            self.handleOtherInput(event)

    def save(self):
        """All images are saved in the images folder."""
        pygame.event.set_blocked(KEYDOWN|KEYUP)
        fname = input("File name?:  ")
        pygame.event.set_blocked(0)
        pygame.image.save(self.image,os.path.join("images",fname))

    def startPygame(self, caption):
        """Sets up the PyGame properties."""
        
        if self.show != ShowTypes.NoShow:
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption(caption)
            
        else:
            self.screen = None

        #Create the image
        self.image = pygame.Surface((self.width,
                                     self.height))
        self.image.fill(self.fillColor)

        #Prepare Game Objects
        self.clock = pygame.time.Clock()
        
        # Start rendering
        self.restartRender()

    def isRunning(self):
        return not self.handleInput() and \
               not (self.done and self.show == ShowTypes.NoShow)

    def restartRender(self):
        self.pixelSize = self.startPixelSize
        self.done = False

    def showProgress(self, fps=60):
        """Method to draw the background to the screen and flip."""
        # Let the clock tick
        self.clock.tick(fps)
        if self.show != ShowTypes.NoShow:
            # Draw background into screen and show
            self.screen.blit(self.image, (0,0))
            pygame.display.flip()
         
        
    def render(self):
        """The main loop of rendering the image.
        Will create pixels of progressively smaller sizes. Stops rendering
        when the pixel size is 0."""

        startTime = time.time()

        # First progress is to fill entire image with one color
        color = self.getColor(0, 0)
        self.image.fill(color, ((0, 0), (self.width, self.height)))

        # Show the progress
        self.showProgress()

        yield

        # Until the pixel size gets too small
        while self.pixelSize > self.minimumPixel:
            print(f"Pixel Size: {self.pixelSize:3}")

            # For each pixel in the image, jumping by pixel size
            for x in range(0, self.width, self.pixelSize):
                for y in range(0, self.height, self.pixelSize):
                    # Get color
                    color = list(map(round, self.getColor(x, y) * 255))

                    self.image.fill(color, ((x, y), (self.pixelSize,
                                                     self.pixelSize)))

                    if self.show == ShowTypes.PerPixel:
                        self.showProgress(256 * 60 // self.pixelSize)

                    yield

                if self.show == ShowTypes.PerColumn:
                    self.showProgress(60)


            # Reduce pixel size
            self.pixelSize //= 2

            if self.show == ShowTypes.PerImage:
                self.showProgress(30)

        # Done rendering
        self.done = True

        endTime = time.time()

        print()

        print(f"Completed in {(endTime - startTime):.4f} seconds", flush=True)
            
        if self.show == ShowTypes.FinalShow:
            self.showProgress(30)
            
        elif self.show == ShowTypes.NoShow:
            pygame.image.save(self.image,os.path.join("images", self.fileName))
            

        yield
