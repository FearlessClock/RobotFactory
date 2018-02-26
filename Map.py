import os

import pygame
from pygame.math import Vector2

from Node import Node


class Map:
    """Map of the world"""

    def __init__(self, mapName, tileSize, tileLoader):
        """Init the map and read the map from the csv"""
        self.id = 0
        self.neighbors = []

        # Used for collision detection
        self.solidObjectGroup = pygame.sprite.Group()
        self.notSolidObjectGroup = pygame.sprite.Group()
        # Used to show the correct blocks on screen
        self.cameraViewGroup = pygame.sprite.Group()

        self.map, self.width, self.height = self.readMap("maps", mapName, tileLoader, "mapTiles",
                                                         {0: False, 1: True, 2: False, 3: True, 4: True})
        self.tileSize = tileSize

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getTileAt(self, pos):
        return self.map[pos.iy()][pos.ix()]

    def getTilesInRect(self, rect, screenTileSize):
        """Return all the tiles inside a rect"""
        tiles = []
        rectY = max(0, rect.y - 1)
        rectYMax = min(self.height, rectY + rect.height + 3)
        rectY = max(0, rectYMax - 3 - screenTileSize.height)

        rectX = max(0, rect.x - 1)
        rectXMax = min(self.width, rectX + rect.width + 3)
        rectX = max(0, rectXMax - 3 - screenTileSize.width)

        for i in range(rectY, rectYMax):
            for j in range(rectX, rectXMax):
                tiles.append(self.map[i][j])
        return tiles

    def setVisibleTiles(self, rect):
        """Set the camera view group to the tiles in a rect"""
        tiles = self.getTilesInRect(rect)
        self.cameraViewGroup.empty()
        self.cameraViewGroup.add(tiles)

    def isObstacle(self, x, y):
        """Check if the cell at x, y is solid"""
        if self.map[int(y)][int(x)].solid:
            return True
        return False

    def readMap(self, filelocation, mapName, tileLoader, spriteSheetName, tileSignificanceDict):
        """Return:
                Tile size, level size and the level
        """

        # Read the file containing the level
        file = open(os.path.join(filelocation, str(mapName) + '.csv'), 'r')

        # Get the id
        self.id = int(file.readline())

        # Get the size of the level
        mapSize = file.readline().split(',')
        mapSize = [line.rstrip('\n') for line in mapSize]  # Strip all the trailling newlines

        width = int(mapSize[0])
        height = int(mapSize[1])

        level = []

        """ Fill the level with the contents of the level text"""
        for i in range(height):
            level.append([])
            fileRead = file.readline().split(',')
            # If the line is empty
            if len(fileRead) == 1:
                continue
            for j in range(width):
                value = int(fileRead[j])
                isSolid = tileSignificanceDict.get(value)
                node = Node(Vector2(j * tileLoader.tileSize.x, i * tileLoader.tileSize.y), isSolid)
                node.setImage(tileLoader.getTileFromName("mapTiles", value))
                level[i].append(node)
                if isSolid:
                    self.solidObjectGroup.add(node)
                else:
                    self.notSolidObjectGroup.add(node)

        file.close()

        for i in range(width):
            for j in range(height):
                if 0 < i + 1 < height and not level[j][i + 1].wall:
                    level[j][i].addNeighbors(level[j][i + 1])
                if 0 < i - 1 < height and not level[j][i - 1].wall:
                    level[j][i].addNeighbors(level[j][i - 1])
                if 0 < j + 1 < width and not level[j + 1][i].wall:
                    level[j][i].addNeighbors(level[j + 1][i])
                if 0 < j - 1 < width and not level[j - 1][i].wall:
                    level[j][i].addNeighbors(level[j - 1][i])

        return level, width, height

    def draw(self, surface):
        self.cameraViewGroup.draw(surface)
