import pygame
from pygame import mouse

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite

from AStar import aStar
from Map import Map
from Node import Node
from TaskList import TaskList, Task


class Player:
    """Class handling all the user input"""
    def __init__(self, image: pygame.Surface, screenSize: Vector2, taskList: TaskList, tilesize):
        self.mousePosition: Vector2 = Vector2(0, 0)
        self.image = image
        self.rect = Rect(0, 0, image.get_width(), image.get_height())
        self.screenSize: Vector2 = screenSize
        self.path = []
        self.taskList = taskList
        self.button1PressedState = False
        self.tilesize = tilesize

        # Menu stuff
        self.menuSpawned = False
        self.menuPosition = Vector2(0, 0)

    def getMousePosition(self):
        return self.mousePosition

    def updateMousePosition(self):
        self.mousePosition = self.mousePosition + Vector2(mouse.get_rel())
        if self.mousePosition.x < 0:
            self.mousePosition.x = 0
        elif self.mousePosition.x > self.screenSize.x-self.rect.width:
            self.mousePosition.x = self.screenSize.x-self.rect.width
        if self.mousePosition.y < 0:
            self.mousePosition.y = 0
        elif self.mousePosition.y > self.screenSize.y-self.rect.h:
            self.mousePosition.y = self.screenSize.y-self.rect.h
        self.rect.x = self.mousePosition.x
        self.rect.y = self.mousePosition.y

    def updateMouse(self, level: Map):
        self.updateMousePosition()
        self.path = aStar(level,
                          level.map[int(5)][int(5)],
                          level.map[int(self.rect.y / self.tilesize.y)][int(self.rect.x / self.tilesize.x)],
                          self.tilesize)

        if pygame.mouse.get_pressed()[0] and not self.button1PressedState:
            # Create a menu from where the player can chose what they want to do
            # On mouse click
            # Spawn menu if it isn't already spawned
            # Close menu if it isn't spawned
            self.button1PressedState = True
            clickPosition = Vector2(self.mousePosition)
            clickPosition.x = (clickPosition.x / self.tilesize.x)
            clickPosition.y = (clickPosition.y / self.tilesize.y)
            self.spawnMenu(clickPosition)
        elif not pygame.mouse.get_pressed()[0] and self.button1PressedState:
            self.button1PressedState = False

    def mouseClick(self):
        print("Button click task completed")

    def spawnMenu(self, clickPos):
        if not self.menuSpawned:
            self.menuPosition = clickPos
            self.menuSpawned = True
        else:
            self.menuSpawned = False

    def drawAt(self, rect, surface):
        if self.menuSpawned:
            pygame.draw.rect(surface, (0, 255, 0), Rect(self.menuPosition.x*self.tilesize.x, self.menuPosition.y*self.tilesize.y, 100, 100))
            pygame.draw.rect(surface, (255, 0, 0), Rect(self.menuPosition.x*self.tilesize.x+10, self.menuPosition.y*self.tilesize.y+10, 80, 20))
            pygame.draw.rect(surface, (0, 255, 255), Rect(self.menuPosition.x*self.tilesize.x+10, self.menuPosition.y*self.tilesize.y+40, 80, 20))
            pygame.draw.rect(surface, (0, 0, 255), Rect(self.menuPosition.x*self.tilesize.x+10, self.menuPosition.y*self.tilesize.y+70, 80, 20))

        surface.blit(self.image, rect)