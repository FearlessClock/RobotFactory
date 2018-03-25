import pygame
from pygame.rect import Rect


class Container:
    def __init__(self, position):
        self.position = position
        self.buttons = []

    """Buttons in the list have to be placed in relation to the container and not the screen"""
    def addButton(self, button):
        self.buttons.append(button);

    def drawContainer(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), Rect(self.position.x, self.position.y, 100, 100))
        for i in range(len(self.buttons)):
            self.buttons[i].draw(surface, self.position)

    def getButtonPressed(self, clickPos):
        relativePos = clickPos - self.position
        for button in self.buttons:
            if button.rect.x < relativePos.x < button.rect.topright[0] and button.rect.y < relativePos.y < button.rect.bottomright[1]:
                print("Clicked button")