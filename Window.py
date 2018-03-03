import os

import pygame
from pygame.math import Vector2

from TileLoader import TileLoader


class Window:
    """Class used to render the screen and hold all the window information"""

    def __init__(self, windowSize, caption, TILE_SIZE, font_renderer):
        self.width = int(windowSize.x)
        self.height = int(windowSize.y)

        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        # pygame.event.set_grab(True)

        self.font_renderer = font_renderer
        self.TILE_SIZE = TILE_SIZE

        self.screens = []
        self.activeScreen = 0
        self.screenDictionary = {}

        self.tileLoader = TileLoader(TILE_SIZE, windowSize)

        """Load all the images and spritesheets"""
        self.tileLoader.addSpriteSheet("mapTiles", os.path.join('images', "TileSheet.png"), Vector2(16, 16),
                                       Vector2(self.TILE_SIZE.x, self.TILE_SIZE.y), 3, 3)
        self.tileLoader.addSpriteSheet("player", os.path.join('images', "hand.png"), Vector2(16, 16),
                                       Vector2(self.TILE_SIZE.x, self.TILE_SIZE.y), 4, 4)

    def addScreenToRender(self, screenToImport, screenName):
        """Add an interactive screen or game screen to the render for easy and unified access."""
        self.screenDictionary.update({screenName: len(self.screens)})
        self.screens.append(screenToImport)

    def updateScreenFromRender(self, screenName, screenToImport):
        index = self.screenDictionary.get(screenName)
        self.screens[index] = screenToImport

    def getScreen(self, screenName):
        """Get a screen from its name."""
        return self.screens[self.screenDictionary[screenName]]

    def getSize(self):
        """Get the screen size."""
        return self.screen.get_size()

    def clearScreen(self):
        """Clear everything on the screen."""
        background = pygame.Surface(self.getSize())
        background = background.convert()
        background.fill((0, 0, 0))
        self.screen.blit(background, (0, 0))

    def drawScreen(self, screenName):
        """Draw the screen by name"""
        self.screens[self.screenDictionary[screenName]].drawScreen(self)

    def updateScreen(self, screenName, deltaTime):
        """Update the screen with delta time"""
        self.screens[self.screenDictionary[screenName]].updateScreen(deltaTime)
