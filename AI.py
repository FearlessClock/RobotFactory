import math
from enum import Enum
from random import random

from pygame.math import Vector2

from Creature import Creature
from Map import Map
from Node import Node


class AIStates(Enum):
    ROAMING = 1
    GOINGTO = 2


def distanceToNode(start: Node, goal, tileSize):
    return math.sqrt(math.pow(start.pos.x / tileSize.x - goal.pos.x / tileSize.x, 2) + math.pow(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y, 2))


def getManhattenDistance(start: Node, goal: Node, tileSize):
    return abs(start.pos.x / tileSize.x - goal.pos.x / tileSize.x) + abs(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y)


def GetHScore(curNeigh, goal, tileSize):
    return distanceToNode(curNeigh, goal, tileSize)


def reconstructPath(node):
    path = []
    while node.parent is not None:
        path.append(node)
        node = node.parent
    return path


class AI(Creature):
    """"Structure to store the AI information and to make the AI move intelligently """

    def __init__(self, x, y, tileLoader, tileSize):
        Creature.__init__(self, x, y, tileLoader, tileSize)
        self.pos = Vector2(x, y)
        self.path = []
        self.tileSize = tileSize
        self.target = self.pos
        self.roamNode = None
        self.movingTo = False
        self.zoneToGoTo = 0
        self.state = AIStates.ROAMING

    def setPos(self, pos):
        self.pos = pos
        self.rect.x = pos.x
        self.rect.y = pos.y

    def setPosLerp(self, pos):
        self.pos = self.pos.lerp(pos, 0.2)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def Update(self, level: Map):
        if self.state == AIStates.ROAMING:
            if not self.movingTo:
                angle = random() * 360
                radius = random() * 6

                x = int(self.pos.x / self.tileSize.x + radius * math.cos(math.radians(angle)))  # random() * level.width
                y = int(
                    self.pos.y / self.tileSize.y + radius * math.sin(math.radians(angle)))  # random() * level.height

                if x >= level.width:
                    x = level.width - 1
                elif x < 0:
                    x = 0

                if y >= level.height:
                    y = level.height - 1
                elif y < 0:
                    y = 0

                self.roamNode = level.getTileAt(Vector2(x, y))
            self.moveToNode(level, self.roamNode)

        elif self.state == AIStates.GOINGTO:
            if not self.movingTo:
                self.zoneToGoTo += 1
                if self.zoneToGoTo > len(level.zoneOfInterest) - 1:
                    self.zoneToGoTo = 0
            self.moveToNode(level, level.zoneOfInterest[self.zoneToGoTo].node)

    def moveToNode(self, level, goal):
        """If no path is known, find a new one otherwise continue on this path"""
        if not self.movingTo:
            self.movingTo = True
            self.path = self.aStar(level,
                                   level.map[int(self.pos.y / self.tileSize.y)][int(self.pos.x / self.tileSize.x)],
                                   goal)
        if len(self.path) > 0:
            dis = self.pos.distance_squared_to(self.target)
            if dis < 2:
                self.target = self.path.pop().pos
            self.setPosLerp(self.target)
            if len(self.path) == 0:
                self.movingTo = False

    def aStar(self, level: Map, start, goal):
        if start.equal(goal):
            self.movingTo = False
            return []
        """Reset all the maze information"""
        for i in range(level.getWidth()):
            for j in range(level.getHeight()):
                level.map[i][j].g = -1
                level.map[i][j].f = 0
                level.map[i][j].parent = None
                level.map[i][j].floor = 0

        # Already visited nodes
        closedSet = []

        start.g = 0
        start.f = 0  # getManhattenDistance(start, goal)

        # Possible nodes to visit
        openSet = [start]

        while len(openSet) > 0:
            index = 0
            best = openSet[index].f
            # Find the best node to go to next
            for i in range(0, len(openSet)):
                if openSet[i].f < best:
                    best = openSet[i].f
                    index = i
            current = openSet.pop(index)

            # When the algo reaches the goal, quit
            if current.equal(goal):
                return reconstructPath(current)

            closedSet.append(current)

            neighs = current.getNeighbors()
            # For each neighbor, check if it is an interesting candidate
            for i in range(0, len(neighs)):
                curNeigh = neighs[i]
                if closedSet.__contains__(curNeigh):
                    continue

                if not openSet.__contains__(curNeigh):
                    openSet.append(curNeigh)

                tentativeGScore = current.g + 1
                if curNeigh.g != -1 and tentativeGScore >= curNeigh.g:
                    continue  # It's not a better score

                curNeigh.parent = current
                curNeigh.g = tentativeGScore
                curNeigh.f = curNeigh.g + GetHScore(curNeigh, goal, self.tileSize)
                curNeigh.floor = 255

        print("Error No path found")
        self.movingTo = False
        return []
