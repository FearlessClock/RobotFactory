import math
from builtins import int
from random import random

from pygame.math import Vector2

from AStar import aStar
from Brain.FSM import FSM
from ClergyRobotClasses.ClergyRobotNeeds import Needs
from Collection.PointOfInterest import PointOfInterest
from Creature import Creature
from Map import Map
from Node import Node
from TaskList import TaskList, Task


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
            print("Recalculate path")
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
        else:
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

    def taskingState(self, level):
        self.currentState = "Tasking"
        """State function for the AI to do player or system assigned tasks"""
        """If all the tasks are done, go back
           if the creature is hungry, go eat and come back later 
           if the creature is tired, go sleep and come back later
           (Might make these a setting in the task for un-interruptable task)"""
        if self.currentTask is None and len(self.taskList.listOfTasks) <= 0:
            self.brain.popState()
        elif self.needs.isTired():
            self.brain.pushState(self.tiredState)
            self.movingTo = False
        elif self.needs.isHungry():
            self.brain.pushState(self.hungryState)
            self.movingTo = False
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
                    gridSpaceGoTo = Vector2(self.currentTask.placeToGo.x / self.tileSize.x,
                                            self.currentTask.placeToGo.y / self.tileSize.y)
                    self.roamNode = level.getTileAt(gridSpaceGoTo)
                    self.moveToNode(level, self.roamNode)
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
                pos = Vector2(self.foundFoodPOI.pos.x * self.tileSize.x, self.foundFoodPOI.pos.y * self.tileSize.y)
                distanceToFood = pos.distance_to(self.pos)
                if distanceToFood < 5:
                    self.eatFood()
                else:
                    self.roamNode = level.getTileAt(self.foundFoodPOI.pos)
                    self.moveToNode(level, self.roamNode)
            else:
                self.findRandomFood(level)
            # Get distance to food

    def tiredState(self, level: Map):
        self.currentState = "Tired"
        """Tired state"""
        if self.needs.sleep > 100:
            self.brain.popState()
        else:
            if self.foundBedPOI is not None:
                pos = Vector2(self.foundBedPOI.pos.x * self.tileSize.x, self.foundBedPOI.pos.y * self.tileSize.y)
                distanceToBed = pos.distance_to(self.pos)
                if distanceToBed < 5:
                    self.sleep()
                else:
                    self.roamNode = level.getTileAt(self.foundBedPOI.pos)
                    self.moveToNode(level, self.roamNode)
            else:
                self.findRandomBed(level)

    """Roaming functions"""

    """Hungry functions"""

    def findRandomFood(self, level):
        foodLocations = level.getFoodZones(self.pos)
        if foodLocations is not None and len(foodLocations) > 0:
            if len(foodLocations) == 1:
                self.foundFoodPOI = foodLocations[0]
            else:
                randomFoodIndex = int(random() * len(foodLocations))
                self.foundFoodPOI = foodLocations[randomFoodIndex]
        else:
            print("There is no bed! You will die!")

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

    def findRandomBed(self, level):
        bedLocations = level.getBedZones(self.pos)
        if bedLocations is not None and len(bedLocations) > 0:
            if len(bedLocations) == 1:
                self.foundBedPOI = bedLocations[0]
            else:
                randomBedIndex = int(random() * len(bedLocations))
                self.foundBedPOI = bedLocations[randomBedIndex]
        else:
            print("There is no bed! You will die!")

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
