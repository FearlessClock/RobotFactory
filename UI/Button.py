import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class Button:

    """ rect = Rect object, Position and size of the button
        color = Color of the button in RGB (R,G,B)
    """
    def __init__(self, rect, color):
        self.rect: Rect = rect
        self.color = color

    def draw(self, surface, offset):
        posRect = self.rect.move(offset.x, offset.y)
        posRect.top
        pygame.draw.rect(surface, self.color, posRect)