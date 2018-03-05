import os
from random import random

import pygame
from pygame.math import Vector2

from Camera import Camera
from ClergyRobot import ClergyRobot
from Human import Human
from MapHolder import MapHolder
from Player import Player
from HumanFactory import HumanFactory
from TaskList import TaskList, Task
from TimedEvents import TimedEvents
from Window import Window


class Gameloop:
    def __init__(self):
        # Create the game camera
        self.tileSize = Vector2(40, 40)
        self.screenSize = Vector2(800, 800)
        pygame.font.init()

        self.font_renderer = pygame.font.Font(os.path.join("fonts", 'Millennium-Regular_0.ttf'), 24)
        self.window = Window(self.screenSize, "Robot Clergy", self.tileSize, self.font_renderer)
        self.camera = Camera(Vector2(20, 20), self.tileSize, self.screenSize)
        self.mapHolder = MapHolder(["Church"], self.tileSize, self.window.tileLoader)

        # Init the player class
        playerImage = self.window.tileLoader.getImageByName("player", 0, 0)
        self.player = Player(playerImage, self.screenSize)

        # Timing and delta time stuff
        self.clock = pygame.time.Clock()
        self.deltaTime = 0

        self.taskList = TaskList()
        self.timedEventHandler = TimedEvents()

        self.humanSpawner = HumanFactory(self.mapHolder.getCurrentMap().gridSize,
                                         self.window.tileLoader, self.tileSize)
        self.humans = []
        self.timedEventHandler.addTimedEvent(1000, self.peopleStartComingForService)
        self.nmbrOfCreatures = 5
        self.AICreatures = [ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y,
                                       self.window.tileLoader, self.tileSize, self.taskList) for i in range(self.nmbrOfCreatures)]
        self.timedEventHandler.addTimedEvent(10000, self.addToTimedEvent)

    def getInputs(self):
        """Return the events corresponding to each button press"""
        events = pygame.event.get([pygame.KEYDOWN, pygame.KEYUP])
        return events

    def preach(self):
        self.timedEventHandler.addTimedEvent(2000, self.peopleStartComingForService)

    def peopleStartComingForService(self):
        task = Task(Vector2(11*self.tileSize.x, 5*self.tileSize.y), self.preach, 250, "Preach")
        self.taskList.enqueueTask(task)
        x = self.tileSize.x
        y = self.tileSize.y

        entranceLists = [Vector2(19*x, 5*y),
                         Vector2(19*x, 6*y)]

        seating = [Vector2(18*x, 1*y),
                   Vector2(18 * x, 2 * y),
                   Vector2(18 * x, 3 * y),
                   Vector2(18 * x, 4 * y),
                   Vector2(18 * x, 7 * y),
                   Vector2(18 * x, 8 * y),
                   Vector2(18 * x, 9 * y),
                   Vector2(18 * x, 10 * y),

                   Vector2(16 * x, 1 * y),
                   Vector2(16 * x, 2 * y),
                   Vector2(16 * x, 3 * y),
                   Vector2(16 * x, 4 * y),
                   Vector2(16 * x, 7 * y),
                   Vector2(16 * x, 8 * y),
                   Vector2(16 * x, 9 * y),
                   Vector2(16 * x, 10 * y),

                   Vector2(14 * x, 1 * y),
                   Vector2(14 * x, 2 * y),
                   Vector2(14 * x, 3 * y),
                   Vector2(14 * x, 4 * y),
                   Vector2(14 * x, 7 * y),
                   Vector2(14 * x, 8 * y),
                   Vector2(14 * x, 9 * y),
                   Vector2(14 * x, 10 * y),
                   ]
        randomAmountOfHumans = int(random() * len(seating))
        for i in range(randomAmountOfHumans):
            chair = seating[int(random() * len(seating))]
            seating.remove(chair)
            self.humans.append(self.humanSpawner.initCreatureAtPos(entranceLists[int(random()*2)], task, chair))

    def handleEvents(self):
        """Handle the events thrown by the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def taskListEventCallback(self):
        print("A task was just finished")

    def addToTimedEvent(self):
        taskPos = self.mapHolder.getCurrentMap().getRandomEmptyNode().pos
        self.taskList.enqueueTask(Task(taskPos, self.taskListEventCallback, 30, "RandomTask"))
        self.timedEventHandler.addTimedEvent(self.timedEventHandler.elapsedTime + 5000, self.addToTimedEvent)

    def startLoop(self):
        """The main function that runs the whole game."""
        # Game loop
        while pygame.display.get_init():
            currentMap = self.mapHolder.getCurrentMap()
            self.deltaTime = self.clock.get_time()
            self.timedEventHandler.updateTimer(self.deltaTime)
            self.player.updateMouse(currentMap, self.tileSize)
            if len(self.humans) > 0:
                for human in self.humans:
                    if not human.alive:
                        self.humans.remove(human)
                    human.update(currentMap, self.deltaTime)
            for ai in self.AICreatures:
                ai.Update(currentMap, self.deltaTime)

            npcs = [human for human in self.humans]
            npcs.extend(self.AICreatures)

            self.camera.drawScreen(self.window.screen, currentMap, self.player,
                                   npcs)
            debugInfo = [len(self.taskList.listOfTasks)]
            debugArray = [task.taskName for task in self.taskList.listOfTasks]
            debugInfo.extend(debugArray)
            self.camera.drawDebug(self.window.screen, debugInfo)
            self.handleEvents()
            if pygame.display.get_init():
                pygame.event.pump()

            try:
                pygame.display.update()
            except:
                print("Display not initialised")

            self.clock.tick(60)
