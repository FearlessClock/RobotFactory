import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class Button:

    """ rect = Rect object, Position and size of the button
        color = Color of the button in RGB (R,G,B)
    """
    def __init__(self, rect, color, text, callback):
        self.rect: Rect = rect
        self.color = color
        self.text = text
        self.callback = callback

    def draw(self, surface, offset, fontRenderer):
        posRect = self.rect.move(offset.x, offset.y)
        pygame.draw.rect(surface, self.color, posRect)
        surface.blit(fontRenderer.render(self.text, False, (0, 0, 0)), posRect)

    def click(self):
        self.callback()
