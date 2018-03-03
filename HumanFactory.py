from random import random

from pygame.math import Vector2

from Human import Human


class HumanFactory:
    def __init__(self, gridSize, tileLoader, tileSize):
        self.tileSize = tileSize
        self.gridSize = gridSize
        self.tileLoader = tileLoader

    def initCreatureRandomPos(self, task):
        x = random() * self.gridSize.x * self.tileSize.x
        y = random() * self.gridSize.y * self.tileSize.y
        targetPos = Vector2(int(random() * self.gridSize.x) * self.tileSize.x,
                            int(random() * self.gridSize.y) * self.tileSize.y)
        return Human(x, y, self.tileLoader, self.tileSize, targetPos, task)

    def initCreatureAtPos(self, pos, task, target):
        return Human(pos.x, pos.y, self.tileLoader, self.tileSize, target, task)
