import os

import pygame
from pygame.math import Vector2

from ClergyRobot import ClergyRobot
from Camera import Camera
from MapHolder import MapHolder
from Window import Window


class Gameloop:
    def __init__(self):
        # Create the game camera
        self.tileSize = Vector2(40, 40)
        self.screenSize = Vector2(600, 600)
        pygame.font.init()

        self.font_renderer = pygame.font.Font(os.path.join("fonts", 'Millennium-Regular_0.ttf'), 24)
        self.window = Window(self.screenSize, "Robot Clergy", self.tileSize, self.font_renderer)
        self.camera = Camera(Vector2(15, 15), self.tileSize, self.screenSize)
        self.mapHolder = MapHolder(["map1"], self.tileSize, self.window.tileLoader)

        # Timing and delta time stuff
        self.clock = pygame.time.Clock()
        self.deltaTime = 0

        self.AICreature = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y, self.window.tileLoader, self.tileSize)
        self.AICreature1 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y, self.window.tileLoader, self.tileSize)
        self.AICreature2 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y, self.window.tileLoader, self.tileSize)
        self.AICreature3 = ClergyRobot(5 * self.tileSize.y, 5 * self.tileSize.y, self.window.tileLoader, self.tileSize)

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

    def startLoop(self):
        """The main function that runs the whole game."""
        # Game loop
        while pygame.display.get_init():
            self.deltaTime = self.clock.get_time()
            self.AICreature.Update(self.mapHolder.getCurrentMap(), self.deltaTime)
            # self.AICreature1.Update(self.mapHolder.getCurrentMap())
            # self.AICreature2.Update(self.mapHolder.getCurrentMap())
            # self.AICreature3.Update(self.mapHolder.getCurrentMap())

            self.camera.draw(self.window.screen, self.mapHolder.getCurrentMap(), None,
                             [self.AICreature, self.AICreature1, self.AICreature2, self.AICreature3])
            self.handleEvents()
            pygame.event.pump()

            try:
                pygame.display.update()
            except:
                print("Error")

            self.clock.tick(60)
