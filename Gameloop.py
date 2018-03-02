import os

import pygame
from pygame.math import Vector2

from ClergyRobot import ClergyRobot
from Camera import Camera
from MapHolder import MapHolder
from Player import Player
from TaskList import TaskList, Task
from TimedEvents import TimedEvents
from Window import Window


class Gameloop:
    def __init__(self):
        # Create the game camera
        self.tileSize = Vector2(30, 30)
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

        self.AICreature  = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y,
                                            self.window.tileLoader, self.tileSize, self.taskList)
        self.AICreature1 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y,
                                            self.window.tileLoader, self.tileSize, self.taskList)
        self.AICreature2 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y,
                                            self.window.tileLoader, self.tileSize, self.taskList)
        self.AICreature3 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y,
                                            self.window.tileLoader, self.tileSize, self.taskList)
        self.timedEventHandler.addTimedEvent(10000, self.addToTimedEvent)

    def getInputs(self):
        """Return the events corresponding to each button press"""
        events = pygame.event.get([pygame.KEYDOWN, pygame.KEYUP])
        return events

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
        print("Timed event ran, next timed event at" ,self.timedEventHandler.elapsedTime+1000)
        taskPos = self.mapHolder.getCurrentMap().getRandomEmptyNode().pos # Vector2(6*self.tileSize.x, 15*self.tileSize.y)
        self.taskList.enqueueTask(Task(taskPos, self.taskListEventCallback, 30))
        self.timedEventHandler.addTimedEvent(self.timedEventHandler.elapsedTime+5000, self.addToTimedEvent)

    def startLoop(self):
        """The main function that runs the whole game."""
        # Game loop
        while pygame.display.get_init():
            self.deltaTime = self.clock.get_time()
            self.timedEventHandler.updateTimer(self.deltaTime)
            self.player.updateMouse(self.mapHolder.getCurrentMap(), self.tileSize)
            self.AICreature.Update (self.mapHolder.getCurrentMap(), self.deltaTime)
            # self.AICreature1.Update(self.mapHolder.getCurrentMap(), self.deltaTime)
            # self.AICreature2.Update(self.mapHolder.getCurrentMap(), self.deltaTime)
            # self.AICreature3.Update(self.mapHolder.getCurrentMap(), self.deltaTime)

            self.camera.drawScreen(self.window.screen, self.mapHolder.getCurrentMap(), self.player,
                                   [self.AICreature])
            self.handleEvents()
            pygame.event.pump()

            try:
                pygame.display.update()
            except:
                print("Error")

            self.clock.tick(60)
