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


def movementCollider(sprite, otherSprite):
    if sprite._id is not otherSprite._id:
        spritecollide = sprite.rect.colliderect
        if spritecollide(otherSprite.rect):
            return otherSprite
    else:
        return False


class Creature(Sprite):
    """The base class for the interacting candidates"""

    def __init__(self, _id, x, y, tileLoader: TileLoader, tileSize, speed):
        Sprite.__init__(self)
        self._id = _id
        self.rect = Rect(x, y, tileSize.x, tileSize.y)
        self.image = None
        self.pos = Vector2(x, y)
        self.target = self.pos
        self.speed = speed

        self.tileSize = tileSize

        self.movingTo = False

        self.brain = FSM()

        self.currentState = ""

        self.movingCreatures: pygame.sprite.Group = None

    def moveToNode(self, level: Map, goal: Node):
        """If no path is known, find a new one otherwise continue on this path"""
        if not self.movingTo:
            self.movingTo = True
            self.path = []
            self.path = aStar(level,
                              level.map[int((self.pos.y+self.tileSize.y/2) / self.tileSize.y)][int((self.pos.x+self.tileSize.y/2) / self.tileSize.x)],
                              goal, self.tileSize)
            if len(self.path) > 0:
                self.movingTo = True

            if len(self.path) > 0:
                self.target = self.path[len(self.path) - 1].pos

        if len(self.path) >= 0:
            dis = self.pos.distance_squared_to(self.target)
            if dis < 5 and len(self.path) > 0:
                self.target = self.path.pop().pos
            oldPos = Vector2(self.pos)
            self.setPosNorm(self.target)

            if self.movingCreatures is not None:
                collision = pygame.sprite.spritecollide(self, self.movingCreatures, False, movementCollider)

                if collision:
                    pushAway = Vector2(0,0)
                    for coll in collision:
                        vec = self.pos - coll.pos
                        pushAway = pushAway + vec
                    pushAway.normalize_ip()
                    self.pos += pushAway

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
        self.pos = self.setPos(self.pos.lerp(pos, 0.2))


    def setPosNorm(self, pos: Vector2):
        vecDis: Vector2 = pos - self.pos
        length = vecDis.length_squared()
        if not length == 0:
            vecDis.normalize_ip()
        self.setPos(self.pos + vecDis * self.speed)
