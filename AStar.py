import math

from pygame.math import Vector2
import heapq

from Map import Map
from Node import Node

from timeit import default_timer as timer

def aStar(level: Map, start: Node, goal: Node, tileSize: Vector2):
    # startTimer = timer()
    if goal.isSolid():
        print("You can't go here, it is solid")
        return []

    if start.equal(goal):
        return []
    """Reset all the maze information"""
    for i in range(level.getWidth()):
        for j in range(level.getHeight()):
            level.map[i][j].g = -1
            level.map[i][j].f = 0
            level.map[i][j].parent = None
            level.map[i][j].floor = 0

    # Already visited nodes
    closedSet = set()

    start.g = 0
    start.f = 0  # getManhattenDistance(start, goal)

    # Possible nodes to visit, Priority queue
    openHeap = []
    openComparer = set()
    heapq.heappush(openHeap, (0, start))
    openComparer.add(start)

    while len(openHeap) > 0:
        # Find the best node to go to next
        current = heapq.heappop(openHeap)[1]

        # When the algo reaches the goal, quit
        if current.equal(goal):
            # endTimer = timer()
            # print("Time taken", endTimer - startTimer)
            return reconstructPath(current)

        openComparer.remove(current)
        closedSet.add(current)

        neighs = current.getNeighbors()
        # For each neighbor, check if it is an interesting candidate
        for i in range(0, len(neighs)):
            curNeigh = neighs[i]
            if curNeigh in closedSet:
                continue

            tentativeGScore = current.g + curNeigh.weight
            if curNeigh.g != -1 and tentativeGScore >= curNeigh.g:
                continue  # It's not a better score

            curNeigh.parent = current
            curNeigh.g = tentativeGScore
            curNeigh.f = curNeigh.g + GetHScore(curNeigh, goal, tileSize)
            curNeigh.floor = 255

            if curNeigh not in openComparer:
                openComparer.add(curNeigh)
                heapq.heappush(openHeap, (curNeigh.f, curNeigh))



    print("Error No path found")
    return []


def reconstructPath(node):
    path = [node]
    while node.parent is not None:
        path.append(node)
        node = node.parent
    path.append(node)
    return path


def GetHScore(curNeigh, goal, tileSize):
    return distanceToNode(curNeigh, goal, tileSize)


def distanceToNode(start: Node, goal, tileSize):
    return math.sqrt(math.pow(start.pos.x / tileSize.x - goal.pos.x / tileSize.x, 2) + math.pow(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y, 2))


def getManhattenDistance(start: Node, goal: Node, tileSize):
    return abs(start.pos.x / tileSize.x - goal.pos.x / tileSize.x) + abs(
        start.pos.y / tileSize.y - goal.pos.y / tileSize.y)
