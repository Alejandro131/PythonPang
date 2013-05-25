import pygame
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D

class Ladder(Object2D):
    def __init__(self, height, position):
        ladder_tile = pygame.image.load('../graphics/Ladder.png')
        ladder_width = ladder_tile.get_width()
        ladder_height = ladder_tile.get_height()
        #Vec2D(self.image.get_size())
        Object2D.__init__(self, Vec2D(ladder_width, height), position)
        self.image = pygame.Surface([self.width, self.height], 
                                    flags=pygame.SRCALPHA)
        for y in range(0, self.height + 1, ladder_height):
            self.image.blit(ladder_tile, (0, y))        
    
    def draw(self, screen):
        screen.blit(self.image, self.position)
