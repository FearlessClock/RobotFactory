import os

import pygame
from pygame.math import Vector2
from pygame.rect import Rect

from Map import Map

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

    def drawScreen(self, surface, level: Map, player, npcList):
        """Draw the player, creatures and tiles with the camera movement"""
        if player is not None:
            self.MoveCameraToPlayerLocation(player.rect)

        if level is not None:
            self.setVisibleSprites(level)

        sprites = self.sprites()
        surface_blit = surface.blit
        rect = Rect(0, 0, 0, 0)
        # Move every sprite so as to be well placed with the camera
        self.drawMap(surface_blit, sprites)
        self.drawSprites(surface_blit, npcList, surface)

        if player is not None:
            rect = Rect(player.rect)
            rect.x -= self.screenRect.x
            rect.y -= self.screenRect.y
            player.drawAt(rect, surface, self.fontRendererMedium)
            # pointList = []
            # for i in range(len(player.path) - 1, 0, -1):
            #     pointList.append([player.path[i].rect.x + self.tileSize.x / 2, player.path[i].rect.y + self.tileSize.y / 2])
            # if len(pointList) > 1:
            #     pygame.draw.lines(surface, (100,100,100), False, pointList, 5)

        # Draw debug info to screen
        rect.x = 0
        rect.y = 13
        # surface_blit(self.fontRendererMedium.render("Nmbr Of tasks: " + str(len(npcList[0].taskList.listOfTasks)), False, (0, 0, 0)), rect)

        self.lostsprites = []

    def drawSprites(self, surface_blit, AI, screen):
        if AI is not None:
            for npc in AI:
                rect = Rect(npc.rect.x - self.screenRect.x, npc.rect.y - self.screenRect.y, 0, 0)
                surface_blit(npc.image, rect)
                surface_blit(self.fontRendererSmall.render("C:" + str(npc.converted), False, (0, 0, 0)), rect)
                # # rect.y += self.fontRendererMedium.size("P")[1]
                # # surface_blit(self.fontRendererMedium.render(str(npc.needs.thirst), False, (0, 0, 0)), rect)
                # rect.y += self.fontRendererSmall.size("P")[1]
                # surface_blit(self.fontRendererSmall.render("S:" + str(npc.needs.sleep), False, (0, 0, 0)), rect)
                # # rect.y += self.fontRendererMedium.size("P")[1]
                # # surface_blit(self.fontRendererMedium.render(str(npc.needs.boredom), False, (0, 0, 0)), rect)
                rect.y += self.fontRendererSmall.size("P")[1]
                surface_blit(self.fontRendererBig.render(str(npc.currentState), False, (0, 0, 0)), rect)
                pointList = []
                if npc.target is not None:
                    pointList.append(npc.target+self.tileSize/2)
                for i in range(len(npc.path)-1, 0, -1):
                    pointList.append([npc.path[i].rect.x+self.tileSize.x/2, npc.path[i].rect.y+self.tileSize.y/2])
                # if npc.roamNode is not None:
                #     pygame.draw.rect(screen, (0, 0, 0), Rect(npc.roamNode.pos.x+10,npc.roamNode.pos.y+10, 30, 30), 5)
                #     pointList.append(npc.roamNode.pos+self.tileSize/2)
                if len(pointList) > 1:
                    pygame.draw.lines(screen, (0,0,0), False, pointList, 5)
                # if npc.roamNode is not None:
                #     pygame.draw.rect(screen, (0, 0, 0), Rect(npc.roamNode.pos.x+10,npc.roamNode.pos.y+10, 30, 30), 5)

    def drawMap(self, surface_blit, tiles):
        for spr in tiles:
            rect = Rect(spr.rect.x - self.screenRect.x, spr.rect.y - self.screenRect.y, 0, 0)
            self.spritedict[spr] = surface_blit(spr.image, rect)
            surface_blit(self.fontRendererSmall.render(str(spr.f), False, (0, 0, 0)), rect)
            for action in spr.userActions:
                rect.move_ip(0, 10)
                surface_blit(self.fontRendererSmall.render(str(action), False, (0, 0, 0)), rect)


    def drawDebug(self, surface, debugInfo):
        rect = Rect(0, 0, 10, 10)
        for arg in debugInfo:
            rect.y += self.fontRendererMedium.size("P")[1]
            surface.blit(self.fontRendererMedium.render(str(arg), False, (0, 0, 0)), rect)
