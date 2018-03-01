import math
from builtins import int
from enum import Enum
from random import random

from pygame.math import Vector2

from TaskList import TaskList, Task
from Brain.FSM import FSM
from ClergyRobotClasses.ClergyRobotNeeds import Needs
from Collection.PointOfInterest import PointOfInterest
from Creature import Creature
from Map import Map
from Node import Node


class AIStates(Enum):
    ROAMING = 1
    GOINGTO = 2
    AT = 3


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


class ClergyRobot(Creature):
    """"Structure to store the AI information and to make the AI move intelligently """

    def __init__(self, x, y, tileLoader, tileSize, taskList: TaskList):
        Creature.__init__(self, x, y, tileLoader, tileSize)
        self.pos: Vector2 = Vector2(x, y)
        self.path = []
        self.tileSize = tileSize
        self.target = self.pos
        self.roamNode = None
        self.movingTo = False
        self.zoneToGoTo = 0

        self.speed = 3

        # Creature stats, used in the tamgotchi life thing
        self.needs = Needs()
        self.brain = FSM()
        self.brain.pushState(self.roaming)

        # Flags for FSM stuff
        self.foundFoodPOI: PointOfInterest = None
        self.foundBedPOI: PointOfInterest = None

        self.time = 0

        self.taskList = taskList

        self.currentTask: Task = None

        self.currentState = None

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

    def Update(self, level: Map, dt: int):
        """Update the AI. Brain and needs"""
        self.time += dt
        if self.time > 300:
            self.time = 0
            self.needs.stepNeeds()
        self.brain.update(level)

    def moveToNode(self, level: Map, goal: Node):
        """If no path is known, find a new one otherwise continue on this path"""
        if not self.movingTo:
            self.movingTo = True
            self.path = self.aStar(level,
                                   level.map[int(self.pos.y / self.tileSize.y)][int(self.pos.x / self.tileSize.x)],
                                   goal)
        if len(self.path) >= 0:
            dis = self.pos.distance_squared_to(self.target)
            if dis < 5 and len(self.path) > 0:
                self.target = self.path.pop().pos
            self.setPosNorm(self.target)
            if len(self.path) == 0 and dis < 2:
                self.movingTo = False

    """Brain state functions"""

    def roaming(self, level):
        self.currentState = "Roaming"
        """Free roaming state"""
        """Check trigger functions"""
        if len(self.taskList.listOfTasks) > 0:
            self.brain.pushState(self.taskingState)
            self.movingTo = False
        elif self.needs.hunger < 30:
            self.brain.pushState(self.hungryState)
            self.movingTo = False
        elif self.needs.sleep < 40:
            self.brain.pushState(self.tiredState)
            self.movingTo = False

        """Resolve the state"""
        if not self.movingTo:
            angle = random() * 360
            radius = random() * 6

            x = int(self.pos.x / self.tileSize.x + radius * math.cos(math.radians(angle)))  # random() * level.width
            y = int(self.pos.y / self.tileSize.y + radius * math.sin(math.radians(angle)))  # random() * level.height

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

    def taskingState(self, level):
        self.currentState = "Tasking"
        """State function for the AI to do player or system assigned tasks"""
        """If all the tasks are done, go back
           if the creature is hungry, go eat and come back later 
           if the creature is tired, go sleep and come back later
           (Might make these a setting in the task for uninterruptable task)"""
        if self.currentTask is None and len(self.taskList.listOfTasks) <= 0:
            self.brain.popState()
        elif self.needs.isTired():
            self.brain.pushState(self.tiredState)
        elif self.needs.isHungry():
            self.brain.pushState(self.hungryState)
        else:
            """If there is no current task, choose one"""
            if self.currentTask is None:
                # Get new task
                if len(self.taskList.listOfTasks) > 0:
                    print("Take task")
                    self.currentTask = self.taskList.dequeueTask()

            """If the task is not set, don't do anything"""
            if self.currentTask is not None:
                # Go to the task
                disToTask = self.pos.distance_to(self.currentTask.placeToGo)
                if disToTask > 5:
                    gridSpaceGoTo = Vector2(self.currentTask.placeToGo.x/self.tileSize.x, self.currentTask.placeToGo.y/self.tileSize.y)
                    self.moveToNode(level, level.getTileAt(gridSpaceGoTo))
                else:
                    # if there, do the task
                    self.currentTask.workOnTask(1)
                    if self.currentTask.taskFinished:
                        print("Task done")
                        self.currentTask = None


    def hungryState(self, level):
        self.currentState = "Hungry"
        """Hungry state"""
        if self.needs.hunger > 100:
            self.brain.popState()
            self.foundFoodPOI = None
        else:
            if self.foundFoodPOI is not None:
                pos = Vector2(self.pos.x / self.tileSize.x, self.pos.y / self.tileSize.y)
                distanceToFood = self.foundFoodPOI.pos.distance_to(pos)
                if distanceToFood < 1:
                    self.eatFood()
                else:
                    self.moveToNode(level, level.getTileAt(self.foundFoodPOI.pos))
            else:
                self.findFood(level)
            # Get distance to food

    def tiredState(self, level: Map):
        self.currentState = "Tired"
        """Tired state"""
        if self.needs.sleep > 70:
            self.brain.popState()
        else:
            if self.foundBedPOI is not None:
                pos = Vector2(self.pos.x / self.tileSize.x, self.pos.y / self.tileSize.y)
                distanceToBed = self.foundBedPOI.pos.distance_to(pos)
                if distanceToBed < 1:
                    self.sleep()
                else:
                    self.moveToNode(level, level.getTileAt(self.foundBedPOI.pos))
            else:
                self.findBed(level)

    """Roaming functions"""

    """Hungry functions"""

    def findFood(self, level):
        foodLocations = level.getFoodZones(self.pos)
        if foodLocations is not None and len(foodLocations) > 0:
            if len(foodLocations) == 1:
                self.foundFoodPOI = foodLocations[0]
            else:
                closest = foodLocations[0].pos.distance_squared_to(self.pos)
                index = 0
                for i in range(1, len(foodLocations)):
                    dis = foodLocations[i].pos.distance_squared_to(self.pos)
                    if dis < closest:
                        closest = dis
                        index = i
                self.foundFoodPOI = foodLocations[index]
        else:
            print("There is no food! You will die!")

    def eatFood(self):
        self.needs.hunger += 1

    """Tired functions"""

    def findBed(self, level):
        bedLocations = level.getBedZones(self.pos)
        if bedLocations is not None and len(bedLocations) > 0:
            if len(bedLocations) == 1:
                self.foundBedPOI = bedLocations[0]
            else:
                closest = bedLocations[0].pos.distance_squared_to(self.pos)
                index = 0
                for i in range(1, len(bedLocations)):
                    dis = bedLocations[i].pos.distance_squared_to(self.pos)
                    if dis < closest:
                        closest = dis
                        index = i
                self.foundBedPOI = bedLocations[index]
        else:
            print("There is no food! You will die!")

    def sleep(self):
        self.needs.sleep += 1

    def aStar(self, level: Map, start: Node, goal: Node):
        if goal.isSolid():
            print("You can't go here, it is solid")
            self.movingTo = False
            return []

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
