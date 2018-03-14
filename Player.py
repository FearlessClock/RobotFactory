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
    def __init__(self, image: pygame.Surface, screenSize: Vector2, taskList: TaskList):
        self.mousePosition: Vector2 = Vector2(0, 0)
        self.image = image
        self.rect = Rect(0, 0, image.get_width(), image.get_height())
        self.screenSize: Vector2 = screenSize
        self.path = []
        self.taskList = taskList
        self.button1PressedState = False

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

    def updateMouse(self, level: Map, tileSize):
        self.updateMousePosition()
        self.path = aStar(level,
                          level.map[int(5)][int(5)],
                          level.map[int(self.rect.y / tileSize.y)][int(self.rect.x / tileSize.x)], tileSize)

        if pygame.mouse.get_pressed()[0] and not self.button1PressedState:
            self.button1PressedState = True
            taskPosition = Vector2(self.mousePosition)
            taskPosition.x = (taskPosition.x // tileSize.x)
            taskPosition.y = (taskPosition.y // tileSize.y)
            if not level.getTileAt(taskPosition).isSolid():
                taskPosition.x *= tileSize.x
                taskPosition.y *= tileSize.y
                self.taskList.enqueueTask(Task(taskPosition, self.mouseClick, 100, "Player Move to"))
        elif not pygame.mouse.get_pressed()[0] and self.button1PressedState:
            self.button1PressedState = False

    def mouseClick(self):
        print("Button click task completed")