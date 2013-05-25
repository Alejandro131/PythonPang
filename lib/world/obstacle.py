import pygame
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D

class Obstacle(Object2D):
    def __init__(self, size, position, image_name=None):
        Object2D.__init__(self, size, position)
        if image_name:
            #Vec2D(self.image.get_size())
            brick_tile = pygame.image.load('../graphics/' + image_name)
            brick_width = brick_tile.get_width()
            brick_height = brick_tile.get_height()
            self.image = pygame.Surface([self.width, self.height])
            for x in range(0, self.width + 1, brick_width):
                for y in range(0, self.height + 1, brick_height):
                    self.image.blit(brick_tile, (x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.position)
