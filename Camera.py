import os

import pygame
from pygame.math import Vector2
from pygame.rect import Rect


class Camera(pygame.sprite.Group):
    """Camera class. Follow the player on the screen"""

    # Position of the camera is the top left corner
    def __init__(self, nmbrOfTilesOnScreen, tileSize, screenSize):
        """Basic camera information"""
        pygame.sprite.Group.__init__(self)
        self.tileSize = tileSize
        self.nmbrOfTilesOnScreen = nmbrOfTilesOnScreen
        self.screenRect = Rect(0, 0, screenSize.x, screenSize.y)
        self.tileRect = Rect(0, 0, nmbrOfTilesOnScreen.x, nmbrOfTilesOnScreen.y)
        self.levelSize = Vector2(0, 0)
        self.fontRendererBig = pygame.font.Font(os.path.join("fonts", 'Millennium-Regular_0.ttf'), 18)
        self.fontRendererMedium = pygame.font.Font(os.path.join("fonts", 'Millennium-Regular_0.ttf'), 12)
        self.fontRendererSmall = pygame.font.Font(os.path.join("fonts", 'Millennium-Regular_0.ttf'), 8)


    def setPosition(self, x, y):
        """Set the position of the camera"""
        x = x - self.tileRect.x - self.tileRect.width / 2
        y = y - self.tileRect.y - self.tileRect.height / 2

        self.tileRect = self.tileRect.move(x, y)

    def setVisibleSprites(self, level):
        """Get the tiles that fall inside the screen and show them"""
        tiles = level.getTilesInRect(self.tileRect, self.tileRect)
        self.levelSize = Vector2(level.width, level.height)
        self.empty()
        self.add(tiles)

    def MoveCameraToPlayerLocation(self, player):
        """Move the camera so that it is centered on the player but doesn't go past the side"""
        self.screenRect.x = max(player.x - self.screenRect.width / 2, 0)
        self.screenRect.x = min(max(0, (self.levelSize.x * self.tileSize.x - self.screenRect.width)), self.screenRect.x)
        self.screenRect.y = max(player.y - self.screenRect.height / 2, 0)
        self.screenRect.y = min(max(0, (self.levelSize.y * self.tileSize.y - self.screenRect.height)),
                                self.screenRect.y)

    def draw(self, surface, level, player, npcList):
        """Draw the player, creatures and tiles with the camera movement"""
        if player is not None:
            self.MoveCameraToPlayerLocation(player.rect)

        if level is not None:
            self.setVisibleSprites(level)

        sprites = self.sprites()
        surface_blit = surface.blit
        # Move every sprite so as to be well placed with the camera
        for spr in sprites:
            rect = Rect(spr.rect.x - self.screenRect.x, spr.rect.y - self.screenRect.y, 0, 0)
            self.spritedict[spr] = surface_blit(spr.image, rect)
            surface_blit(self.fontRendererMedium.render(str(spr.f), False, (0, 0, 0)), rect)
        if npcList is not None:
            for npc in npcList:
                rect = Rect(npc.rect.x - self.screenRect.x, npc.rect.y - self.screenRect.y, 0, 0)
                surface_blit(npc.image, rect)
                surface_blit(self.fontRendererBig.render("H:" + str(npc.needs.hunger), False, (0, 0, 0)), rect)
                # rect.y += self.fontRendererMedium.size("P")[1]
                # surface_blit(self.fontRendererMedium.render(str(npc.needs.thirst), False, (0, 0, 0)), rect)
                rect.y += self.fontRendererBig.size("P")[1] - 6
                surface_blit(self.fontRendererBig.render("S:" + str(npc.needs.sleep), False, (0, 0, 0)), rect)
                # rect.y += self.fontRendererMedium.size("P")[1]
                # surface_blit(self.fontRendererMedium.render(str(npc.needs.boredom), False, (0, 0, 0)), rect)

        if player is not None:
            rect = Rect(player.rect)
            rect.x -= self.screenRect.x
            rect.y -= self.screenRect.y
            player.net.draw(surface_blit, self.screenRect)
            surface_blit(player.image, rect)

        self.lostsprites = []
