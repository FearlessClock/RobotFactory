import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

import TileLoader
from AStar import aStar
from Brain.FSM import FSM
from ClergyRobotClasses.ClergyRobotNeeds import Needs
from Map import Map
from Node import Node


class Creature(Sprite):
    """The base class for the interacting candidates"""

    def __init__(self, x, y, tileLoader: TileLoader, tileSize, speed):
        Sprite.__init__(self)
        self.rect = Rect(x, y, tileSize.x, tileSize.y)
        self.image = None
        self.pos = Vector2(x, y)
        self.target = self.pos
        self.speed = speed

        self.tileSize = tileSize

        self.movingTo = False

        self.brain = FSM()

        self.currentState = ""


    def moveToNode(self, level: Map, goal: Node):
        """If no path is known, find a new one otherwise continue on this path"""
        if not self.movingTo:
            self.movingTo = True
            self.path = []
            self.path = aStar(level,
                              level.map[int(self.pos.y / self.tileSize.y)][int(self.pos.x / self.tileSize.x)],
                              goal, self.tileSize)
            if len(self.path) > 0:
                self.movingTo = True

            if len(self.path) > 0:
                self.target = self.path[len(self.path) - 1].pos

        if len(self.path) >= 0:
            dis = self.pos.distance_squared_to(self.target)
            if dis < 5 and len(self.path) > 0:
                self.target = self.path.pop().pos
            self.setPosNorm(self.target)
            if len(self.path) == 0 and dis < 2:
                self.movingTo = False

    def isOnItem(self, maze):
        x = self.pos.x
        y = self.pos.y
        if len(maze) > x >= 0 and len(maze) > y >= 0 and maze[x][y].payload == 2:
            return True
        return False

    def loadImage(self, filename, tileSize):
        image = pygame.image.load(filename)
        return pygame.transform.scale(image, (tileSize, tileSize))

    def setPos(self, pos):
        self.pos = pos
        self.rect.x = pos.x
        self.rect.y = pos.y

    def setPosLerp(self, pos):
        self.pos = self.pos.lerp(pos, 0.2)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def setPosNorm(self, pos: Vector2):
        vecDis: Vector2 = pos - self.pos
        length = vecDis.length_squared()
        if not length == 0:
            vecDis.normalize_ip()
        self.pos += vecDis * self.speed

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

