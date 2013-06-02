import pygame
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D


class Obstacle(Object2D):

    def __init__(self, size, position, image_name=None):
        Object2D.__init__(self, size, position)
        if image_name:
            tile_image = pygame.image.load('../graphics/' + image_name)
            tile = Vec2D(tile_image.get_size())
            self.image = pygame.Surface([self.width, self.height])
            for x in range(0, self.width + 1, tile.width):
                for y in range(0, self.height + 1, tile.height):
                    self.image.blit(tile_image, (x, y))

    def draw(self, screen):
        screen.blit(self.image, self.position)
