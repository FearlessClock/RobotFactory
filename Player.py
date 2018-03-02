import pygame
from pygame import mouse

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite


class Player:
    """Class handling all the user input"""
    def __init__(self, image: pygame.Surface, screenSize: Vector2):
        self.mousePosition = Vector2(0, 0)
        self.image = image
        self.rect = Rect(0, 0, image.get_width(), image.get_height())
        self.screenSize: Vector2 = screenSize

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
