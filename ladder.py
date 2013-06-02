import pygame
from pang.settings import *
from pang.vec2d import Vec2D
from pang.object2d import Object2D


class Ladder(Object2D):

    def __init__(self, height, position):
        tile_image = pygame.image.load('assets/gfx/Ladder.png')
        tile = Vec2D(tile_image.get_size())
        Object2D.__init__(self, Vec2D(tile.width, height), position)
        self.image = pygame.Surface([self.width, self.height],
                                    flags=pygame.SRCALPHA)
        for y in range(0, self.height + 1, tile.height):
            self.image.blit(tile_image, (0, y))

    def draw(self, screen):
        screen.blit(self.image, self.position)
