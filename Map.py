import json
import os
from random import random
from typing import List

import pygame
from pygame.math import Vector2

from Collection.PointOfInterest import PointOfInterest
from Node import Node
from Player.UserAction import UserAction


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

        self.zoneOfInterest: List(PointOfInterest) = []
        self.beds: List(PointOfInterest) = []
        self.food: List(PointOfInterest) = []
        self.alters = []

        self.map, self.width, self.height = self.readMap("maps", mapName, tileLoader, "mapTiles",
                                                         {0: False, 1: False, 2: False, 3: True, 4: False, 5: False,
                                                          6: False, 7: False, 8: False})
        self.gridSize = Vector2(self.width, self.height)
        self.tileSize = tileSize

    def getRandomEmptyNode(self) -> Node:
        x = random() * self.width
        y = random() * self.height
        emptyNode: Node = self.getTileAt(Vector2(x, y))
        while emptyNode.isSolid():
            x = random() * self.width
            y = random() * self.height
            emptyNode: Node = self.getTileAt(Vector2(x, y))
        return emptyNode

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getTileAt(self, pos):
        return self.map[int(pos.y)][int(pos.x)]

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

    def addZoneOfInterest(self, pos, name, node, interestType):
        self.zoneOfInterest.append(PointOfInterest(pos, name, node, interestType))

    def addFoodZone(self, pos, name, node):
        self.food.append(PointOfInterest(pos, name, node, 2))

    def addAlterZone(self, pos, name, node):
        self.alters.append(PointOfInterest(pos, name, node, 0))

    def addBedZone(self, pos, name, node):
        self.beds.append(PointOfInterest(pos, name, node, 1))

    def getBedZones(self):
        return self.beds

    def getFoodZones(self):
        return self.food

    def getFoodZoneAtIndex(self, index) -> PointOfInterest:
        if index < len(self.food):
            self.food[index].isUsed = True
            return self.food[index]
        else:
            return None

    def getBedZoneAtIndex(self, index) -> PointOfInterest:
        if index < len(self.beds):
            self.beds[index].isUsed = True
            return self.beds[index]
        else:
            return None

    def unuseBedZone(self, index):
        if index < len(self.beds):
            self.beds[index].isUsed = False

    def unuseFoodZone(self, index):
        if index < len(self.food):
            self.food[index].isUsed = False

    def getNearestFood(self, pos: Vector2):
        if len(self.food) > 0:
            pos = Vector2(pos.x / self.tileSize.x, pos.y / self.tileSize.y)
            closest = pos.distance_squared_to(self.food[0].pos)
            poi = self.food[0]
            for PoI in self.food:
                dis = pos.distance_squared_to(PoI.pos)
                if closest > dis:
                    closest = dis
                    poi = PoI
            return poi
        return None

    def getNearestBed(self, pos: Vector2):
        if len(self.beds) > 0:
            pos = Vector2(pos.x / self.tileSize.x, pos.y / self.tileSize.y)
            closest = pos.distance_squared_to(self.beds[0].pos)
            poi = self.beds[0]
            for PoI in self.beds:
                dis = pos.distance_squared_to(PoI.pos)
                if closest > dis:
                    closest = dis
                    poi = PoI
            return poi
        return None

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
                node = Node(Vector2(j * tileLoader.tileSize.x, i * tileLoader.tileSize.y), isSolid, value)
                if random() > 0.5:
                    node.addUserAction(UserAction("Something", self.callback))
                node.setImage(tileLoader.getTileFromName("mapTiles", value))
                level[i].append(node)
                if isSolid:
                    self.solidObjectGroup.add(node)
                else:
                    self.notSolidObjectGroup.add(node)

        file.close()

        for i in range(width):
            for j in range(height):
                if 0 <= i + 1 < height and not level[j][i + 1].wall:
                    level[j][i].addNeighbors(level[j][i + 1])
                if 0 <= i - 1 < height and not level[j][i - 1].wall:
                    level[j][i].addNeighbors(level[j][i - 1])
                if 0 <= j + 1 < width and not level[j + 1][i].wall:
                    level[j][i].addNeighbors(level[j + 1][i])
                if 0 <= j - 1 < width and not level[j - 1][i].wall:
                    level[j][i].addNeighbors(level[j - 1][i])

        file = open(os.path.join("data", "PointsOfInterest.json"), 'r')
        parsedJson = json.loads(file.read())
        positions = parsedJson["points"]
        for interest in positions:
            pos = Vector2(int(interest["pos"]["x"]), int(interest["pos"]["y"]))
            self.addZoneOfInterest(pos, interest["name"], level[int(pos.y)][int(pos.x)], interest["type"])
            if interest["type"] == 0:
                self.addAlterZone(pos, interest["name"], level[int(pos.y)][int(pos.x)])
            if interest["type"] == 1:
                self.addBedZone(pos, interest["name"], level[int(pos.y)][int(pos.x)])
            if interest["type"] == 2:
                self.addFoodZone(pos, interest["name"], level[int(pos.y)][int(pos.x)])
            # level[int(interest["pos"]["y"])][int(interest["pos"]["x"])].image = tileLoader.getTileFromName("mapTiles",
            #                                                                                                       4)
        return level, width, height

    def draw(self, surface):
        self.cameraViewGroup.draw(surface)

    def callback(self):
        print("this is a callback")