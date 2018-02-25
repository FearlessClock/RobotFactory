from pygame.math import Vector2

from Spritesheet import SpriteSheet


class TileLoader:
    """Holder for all the different spritsheets in the game"""

    def __init__(self, tileSize, screenSize):
        """Set the basic attributes and initialise the arrays"""
        self.screenSize = screenSize
        self.tileSize = tileSize

        self.loadedAnimations = {}
        self.loadedImages = {}
        self.lastAnimation = None
        self.playerKeyframe = 0
        self.time = 0
        self.animationTime = 200

        self.lastNPCAnimation = None
        self.NPCKeyframe = 0
        self.NPCTime = 0
        self.currentAnimationLength = 0

    def addSpriteSheet(self, spriteName, filename, realSpriteSize, scaledSpriteSize, rowCount, columeCount):
        """Create a spritesheet and add it to the list of loaded images

        Real Sprite Size: The actual size of the image on disk
        Scaled Sprite Size: The size we want to scale the sprite to for the game"""
        spriteSheet = SpriteSheet(filename)
        self.loadedImages.update({spriteName: spriteSheet.load_grid((0, 0, realSpriteSize.x, realSpriteSize.y),
                                                                    columeCount, rowCount,
                                                                    Vector2(scaledSpriteSize.x, scaledSpriteSize.y),
                                                                    (255, 0, 255))})

    def addAnimation(self, animationName, animationController):
        """Add an animation controller to the list of animations"""
        self.loadedAnimations.update({animationName: animationController})

    def getAnimationController(self, animationName):
        """Return a named animation"""
        return self.loadedAnimations.get(animationName)

    def getAnimationFrameByName(self, animationName):
        """Return the current animation from from a certain animation controller"""
        return self.loadedAnimations.get(animationName).getCurrentAnimationFrame()

    def setAnimationForNameToName(self, animationControllerName, animationName):
        """Change the currently running animation for a certain animation controller"""
        self.loadedAnimations.get(animationControllerName).changeCurrentAnimationTo(animationName)

    def getImageByName(self, imageName, row, colume):
        """Return the sprite from a certain position in a grid"""
        return self.loadedImages.get(imageName)[row][colume]

    def getImageStripByName(self, imageName, row):
        """Return the sprite strip from a certain row"""
        return self.loadedImages.get(imageName)[row]

    def getImageGridByName(self, imageName):
        """Return the sprite sheet for a certain image"""
        return self.loadedImages.get(imageName)

    def getTileFromName(self, imageName, nmbr):
        """Get a sprite sheet, determine where a certain tile is on the grid and return it"""
        grid = self.getImageGridByName(imageName)
        if grid is not None:
            return grid[int(nmbr / len(grid))][nmbr % len(grid)]
        else:
            print("ERROR: Image grid tile not found")
            return None
