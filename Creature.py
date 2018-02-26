import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import TileLoader


class Creature(Sprite):
    """The base class for the interacting candidates"""

    def __init__(self, x, y, tileLoader: TileLoader, tileSize):
        Sprite.__init__(self)
        self.rect = Rect(x, y, tileSize.x, tileSize.y)
        self.image = tileLoader.getTileFromName("mapTiles", 3)
        self.pos = Vector2(x, y)

    def isOnItem(self, maze):
        x = self.pos.x
        y = self.pos.y
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload == 2:
            return True;
        return False;

    def loadImage(self, filename, tileSize):
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, (tileSize, tileSize))

    @staticmethod
    def checkEmpty(x, y, maze):
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].wall != 1:
            return True
        return False
