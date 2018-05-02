import math
from builtins import int
from random import random

import pygame
from pygame.math import Vector2

from ClergyRobotClasses.ClergyRobotNeeds import Needs
from ClergyRobotClasses.ClergyRobotSkills import ClergyRobotSkills
from Collection.PointOfInterest import PointOfInterest
from Creature import Creature
from Map import Map
from TaskList import TaskList, Task


class ClergyRobot(Creature):
    """"Structure to store the AI information and to make the AI move intelligently """

    def __init__(self, id, x, y, tileLoader, tileSize, taskList: TaskList):
        Creature.__init__(self, id, x, y, tileLoader, tileSize, 3)
        self.image = tileLoader.getTileFromName("mapTiles", 3)
        self.pos: Vector2 = Vector2(x, y)
        self.path = []
        self.tileSize = tileSize
        self.roamNode = None
        self.zoneToGoTo = 0

        # Creature stats, used in the tamgotchi life thing
        self.needs = Needs()
        self.brain.pushState(self.roaming)

        #Creature skills. Used to calculate how good a creature is at something
        self.skills = ClergyRobotSkills()

        # Flags for FSM stuff
        self.foundFoodPOI: PointOfInterest = None
        self.foundPoIIndex = -1
        self.foundBedPOI: PointOfInterest = None

        self.time = 0

        self.taskList = taskList

        self.currentTask: Task = None

        self.converted = True # Can be romoved, just to debug humans

    def Update(self, level: Map, dt: int, movingAIGroup: pygame.sprite.Group):
        """Update the AI. Brain and needs"""
        self.time += dt
        if self.time > 500:
            self.time = 0
            self.needs.stepNeeds()
        self.movingCreatures = movingAIGroup
        self.brain.update(level)

    """Brain state functions"""

    def roaming(self, level):
        self.currentState = "Roaming"
        """Free roaming state"""
        """Check trigger functions"""
        if len(self.taskList.listOfTasks) > 0:
            self.brain.pushState(self.taskingState)
            self.movingTo = False
            self.movingTo = False
        elif self.needs.hunger < 30:
            self.brain.pushState(self.hungryState)
            self.movingTo = False
        elif self.needs.tired < 40:
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
                    self.currentTask = self.taskList.dequeueTask()

            """If the task is set"""
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
                    self.currentTask.workOnTask(1, self.skills)
                    if self.currentTask.taskFinishedFlag:
                        self.currentTask = None

    def hungryState(self, level):
        self.currentState = "Hungry"
        """Hungry state"""
        if self.needs.hunger > 100:
            self.brain.popState()
            self.foundFoodPOI = None
            level.unuseFoodZone(self.foundPoIIndex)
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
        if self.needs.tired > 100:
            self.brain.popState()
            self.foundBedPOI = None
            level.unuseBedZone(self.foundPoIIndex)
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
        foodLocations = level.getFoodZones()
        if foodLocations is not None and len(foodLocations) > 0:
            self.foundPoIIndex = 0
            if len(foodLocations) > 1:
                self.foundPoIIndex = int(random() * len(foodLocations))
                count = 0
                while foodLocations[self.foundPoIIndex].isUsed and count < 100:
                    count += 1
                    self.foundPoIIndex = int(random() * len(foodLocations))
                if count >= 100:
                    self.foundPoIIndex  = -1
            if self.foundPoIIndex >= 0:
                self.foundFoodPOI = level.getFoodZoneAtIndex(self.foundPoIIndex)
        else:
            print("There is no bed! You will die!")

    def findFood(self, level):
        foodLocations = level.getFoodZones()
        if foodLocations is not None and len(foodLocations) > 0:
            self.foundPoIIndex = 0
            if len(foodLocations) > 1:
                closest = 9999999999
                self.foundPoIIndex = -1
                for i in range(0, len(foodLocations)):
                    if not foodLocations[i].isUsed:
                        dis = foodLocations[i].pos.distance_squared_to(self.pos)
                        if dis < closest:
                            closest = dis
                            self.foundPoIIndex = i
                if self.foundPoIIndex >= 0:
                    self.foundFoodPOI = level.getFoodZoneAtIndex(self.foundPoIIndex)
        else:
            print("There is no food! You will die!")

    def eatFood(self):
        self.needs.eat(1)

    """Tired functions"""

    def findRandomBed(self, level):
        bedLocations = level.getBedZones()
        if bedLocations is not None and len(bedLocations) > 0:
            self.foundPoIIndex = 0
            if len(bedLocations) > 1:
                self.foundPoIIndex = int(random() * len(bedLocations))
                count = 0
                while bedLocations[self.foundPoIIndex].isUsed and count < 100:
                    count += 1
                    self.foundPoIIndex = int(random() * len(bedLocations))

                self.foundBedPOI = level.getBedZoneAtIndex(self.foundPoIIndex)
        else:
            print("There is no bed! You will die!")

    def findBed(self, level):
        bedLocations = level.getBedZones()
        if bedLocations is not None and len(bedLocations) > 0:
            self.foundPoIIndex = 0
            if len(bedLocations) > 1:
                closest = 9999999999
                self.foundPoIIndex = -1
                for i in range(0, len(bedLocations)):
                    if not bedLocations[i].isUsed:
                        dis = bedLocations[i].pos.distance_squared_to(self.pos)
                        if dis < closest:
                            closest = dis
                            self.foundPoIIndex = i
                if self.foundPoIIndex >= 0:
                    self.foundBedPOI = level.getBedZoneAtIndex(self.foundPoIIndex)
        else:
            print("There is no food! You will die!")

    def sleep(self):
        self.needs.sleep(1)
