import pygame
from pygame import mouse
from pygame.math import Vector2
from pygame.rect import Rect

from AStar import aStar
from Map import Map
from TaskList import TaskList
from UI.Button import Button
from UI.Container import Container


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
        self.buttonContainer = Container(Vector2(0, 0))
        self.buttonContainer.addButton(Button(Rect(10, 10, 80, 20), (255, 0, 0)))
        self.buttonContainer.addButton(Button(Rect(10, 40, 80, 20), (255, 0, 0)))
        self.buttonContainer.addButton(Button(Rect(10, 70, 80, 20), (255, 0, 0)))

    def getMousePosition(self):
        return self.mousePosition

    def updateMousePosition(self):
        self.mousePosition = self.mousePosition + Vector2(mouse.get_rel())
        if self.mousePosition.x < 0:
            self.mousePosition.x = 0
        elif self.mousePosition.x > self.screenSize.x - self.rect.width:
            self.mousePosition.x = self.screenSize.x - self.rect.width
        if self.mousePosition.y < 0:
            self.mousePosition.y = 0
        elif self.mousePosition.y > self.screenSize.y - self.rect.h:
            self.mousePosition.y = self.screenSize.y - self.rect.h
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
            screenPosition = Vector2(self.mousePosition)
            clickPosition = Vector2()
            clickPosition.x = (screenPosition.x / self.tilesize.x)
            clickPosition.y = (screenPosition.y / self.tilesize.y)
            self.spawnMenu(clickPosition, screenPosition)
        elif not pygame.mouse.get_pressed()[0] and self.button1PressedState:
            self.button1PressedState = False

    def mouseClick(self):
        print("Button click task completed")

    def spawnMenu(self, gridPos, screenPos):
        if not self.menuSpawned:
            self.menuPosition = gridPos
            self.menuSpawned = True
        else:
            if self.menuPosition.x + 100 > gridPos.x > self.menuPosition.x and self.menuPosition.y + 100 > gridPos.y > self.menuPosition.y:
                self.buttonContainer.getButtonPressed(screenPos)
            else:
                self.menuSpawned = False

    def drawAt(self, rect, surface):
        if self.menuSpawned:
            screenRef = Vector2(self.menuPosition.x * self.tilesize.x, self.menuPosition.y * self.tilesize.y)
            self.buttonContainer.position = screenRef
            self.buttonContainer.drawContainer(surface)

        surface.blit(self.image, rect)
