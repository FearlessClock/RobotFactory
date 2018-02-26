import math

from pygame.math import Vector2

from Creature import Creature
from Map import Map
from Node import Node


def distanceToNode(start: Node, goal, tileSize):
    return math.sqrt(math.pow(start.pos.x / tileSize.x - goal.pos.x / tileSize.x, 2) + math.pow(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y, 2))


def getManhattenDistance(start: Node, goal: Node, tileSize):
    return abs(start.pos.x / tileSize.x - goal.pos.x / tileSize.x) + abs(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y)


def GetHScore(curNeigh, goal, tileSize):
    return getManhattenDistance(curNeigh, goal, tileSize)


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

    def setPos(self, pos):
        self.pos = pos
        self.rect.x = pos.x
        self.rect.y = pos.y

    def moveToNode(self, level, goal):
        """If no path is known, find a new one otherwise continue on this path"""
        if len(self.path) == 0:
            self.path = self.aStar(level,
                                   level.map[int(self.pos.x / self.tileSize.x)][int(self.pos.y / self.tileSize.y)],
                                   goal)
        if len(self.path) > 0:
            self.setPos(self.path.pop().pos)

    def aStar(self, level: Map, start, goal):
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
        return []
