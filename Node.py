from typing import List

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

from Player.UserAction import UserAction


class Node(Sprite):
    """Node structure to represent the graph of the maze. Allows us to know a lot of information about the maze in one position"""

    def __init__(self, pos: Vector2, wall: bool, weight):
        Sprite.__init__(self)
        self.rect = Rect(pos.x, pos.y, 40, 40)
        self.pos = pos
        self.floor = 0
        self.image = None
        self.weight = weight
        self.wall = wall
        self.payload = 0
        self.neighbors = []
        self.parent = None
        self.g = -1
        self.f = -1

        # User actions associated with this position
        self.userActions: List(UserAction) = []

    def addUserAction(self, action: UserAction):
        self.userActions.append(action)

    def setImage(self, Image):
        self.image = Image

    def addNeighbors(self, node):
        self.neighbors.append(node)

    def removeNeighbors(self, node):
        self.neighbors.remove(node)

    def getPayload(self):
        return self.payload

    def setPayload(self, val):
        self.payload = val

    def getNeighbors(self):
        return self.neighbors

    def equal(self, other):
        return other.pos.x == self.pos.x and other.pos.y == self.pos.y

    def __str__(self):
        return "(" + str(self.pos.x) + " : " + str(self.pos.y) + ')'

    def isSolid(self):
        return self.wall
