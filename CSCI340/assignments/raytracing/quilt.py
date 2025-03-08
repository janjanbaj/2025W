import pygame, os, time
from render import ProgressiveRenderer, ShowTypes
import subprocess
import platform, psutil
from tqdm import tqdm, trange
from multiprocessing import Pool

try:
    if platform.system() == "Windows":
        proc = psutil.Process(os.getpid())
        proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    else:
        niceness = os.nice(0)
        if niceness < 19:
            os.nice(19)
except Exception as e:
    print("Unable to adjust priority of process.")
    print(e)

QUILT_SUBFOLDER = "quilt"


def stitch(folderName):
    path = os.path.join(QUILT_SUBFOLDER, folderName)
    info = open(os.path.join(path, "info.txt"), "r")
    width, height = [int(x) for x in info.read().split()]
    finalImage = pygame.Surface((width, height))

    images = [x for x in os.listdir(path) if x.endswith(".png")]
    total = len(images)

    percent = 0.1
    printAt = [int(x * percent * total) for x in range(1, int(1 / percent))]

    print("Starting...")

    for i in range(total):
        imageName = images[i]
        imageSurface = pygame.image.load(os.path.join(path, imageName))
        trim = imageName.split(".")[0]
        coords = [int(x) for x in trim.split("_")]
        finalImage.blit(imageSurface, coords)

        if i in printAt:
            print(f"{(printAt.index(i) + 1) * percent * 100:2.0f}% completed!")

    pygame.image.save(finalImage, path + "_FINISHED.png")

    print("All done!")


class QuiltRenderer(ProgressiveRenderer):
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

    def __init__(
        self,
        width=None,
        height=None,
        show=None,
        showTime=True,
        startPixelSize=1,
        chunkSize=100,
        displayUpdates=False,
    ):
        print("Enter a folder name for the QuiltRenderer")
        super().__init__(
            width,
            height,
            showTime,
            ShowTypes.NoShow,
            minimumPixel=startPixelSize // 2,
            startPixelSize=startPixelSize,
        )

        self.displayUpdates = displayUpdates

        self.chunkSize = chunkSize
        self.chunkStartX = 0
        self.chunkStartY = 0
        self.chunkEndX = self.width
        self.chunkEndY = self.height

        if not os.path.exists(QUILT_SUBFOLDER):
            os.mkdir(QUILT_SUBFOLDER)

        self.quiltFolder = os.path.join(QUILT_SUBFOLDER, self.fileName)

        if not os.path.exists(self.quiltFolder):
            os.mkdir(self.quiltFolder)

    def setChunkStart(x, y):
        self.chunkStartX = x
        self.chunkStartY = y

    def setChunkEnd(x, y):
        self.chunkEndX = x
        self.chunkEndY = y

    def render(self):
        """The main loop of rendering the image.
        Will create pixels of progressively smaller sizes. Stops rendering
        when the pixel size is 0."""

        startTime = time.time()

        # First progress is to fill entire image with one color
        color = self.getColor(0, 0)
        self.image.fill(color, ((0, 0), (self.width, self.height)))
        info = open(os.path.join(self.quiltFolder, "info.txt"), "w")
        info.write(f"{self.width} {self.height}")
        info.close()

        # For each pixel in the image, jumping by pixel size
        for x in trange(self.chunkStartX, self.chunkEndX, self.chunkSize):
            for y in range(self.chunkStartY, self.chunkEndY, self.chunkSize):
                chunkWidth = min(self.width - x, self.chunkSize)
                chunkHeight = min(self.height - y, self.chunkSize)

                chunkImage = pygame.Surface((chunkWidth, chunkHeight))

                chunkFileName = f"{x}_{y}.png"

                if self.displayUpdates:
                    print(f"{chunkFileName} starting.")

                for ix in range(x, x + self.chunkSize):
                    for iy in range(y, y + self.chunkSize):
                        # Get color
                        color = self.getColor(ix, iy) * 255

                        chunkImage.fill(color, ((ix - x, iy - y), (1, 1)))

                pygame.image.save(
                    chunkImage, os.path.join(self.quiltFolder, chunkFileName)
                )

                if self.displayUpdates:
                    print(f"{chunkFileName} completed.")
                    print("===============================")

        # Done rendering
        self.done = True

        endTime = time.time()

        if self.displayUpdates:
            print()

            print(f"Completed in {(endTime - startTime):.4f} seconds", flush=True)


if __name__ == "__main__":
    folder = input("Enter folder name to stitch: ")
    stitch(folder)
