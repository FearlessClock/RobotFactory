# https://www.pygame.org/wiki/Spritesheet

# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame


class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print(('Unable to load spritesheet image:', filename))
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, scale, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        image = pygame.transform.scale(image, (int(scale.x), int(scale.y)))
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, scale, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, scale, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, scale, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, scale, colorkey)

    def load_grid(self, rect, image_count, row_count, scale, colorkey=None):
        strips = [(rect[0], rect[1] + rect[3] * y, rect[2], rect[3]) for y in range(row_count)]
        return [self.load_strip(strip, image_count, scale, colorkey) for strip in strips]
