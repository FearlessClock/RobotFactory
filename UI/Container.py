import pygame
from pygame.math import Vector2
from pygame.rect import Rect

from UI.Button import Button


class Container:
    """ Position in screen space
        menuSize in screen space"""
    def __init__(self, position: Vector2, menuSize: Vector2):
        self.size = menuSize
        self.position = position
        self.buttons = []

    """Buttons in the list have to be placed in relation to the container and not the screen"""
    def addButton(self, button: Button):
        self.buttons.append(button);

    def drawContainer(self, surface, fontRenderer):
        pygame.draw.rect(surface, (0, 255, 0), Rect(self.position.x, self.position.y, self.size.x, self.size.y))
        for i in range(len(self.buttons)):
            self.buttons[i].draw(surface, self.position, fontRenderer)

    def getButtonPressed(self, clickPos):
        relativePos = clickPos - self.position
        for button in self.buttons:
            if button.rect.x < relativePos.x < button.rect.topright[0] and button.rect.y < relativePos.y < button.rect.bottomright[1]:
                button.click()