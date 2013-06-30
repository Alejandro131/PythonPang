import pygame

from pang.bonus import *
from pang.hook import *
from pang.vec2d import Vec2D
from pang.ball import Ball
from pang.ladder import Ladder
from pang.obstacle import Obstacle


class GUIDrawer:

    def __init__(self, screen, obstacle_image):
        self.screen = screen
        self.image_cache = {}
        self.ladder_cache = {}
        self.obstacle_cache = {}
        self.obstacle_image = obstacle_image

    def get_ladder_image(self, string, width, height):
        image_library = self.ladder_cache.get(string)
        size_string = str(width) + 'x' + str(height)
        image = None
        if image_library is None:
            image_library = {}
            self.ladder_cache[string] = image_library

        image = image_library.get(size_string)
        if image is None:
            tile_image = pygame.image.load(string)
            tile = Vec2D(tile_image.get_size())
            image = pygame.Surface([width, height], flags=pygame.SRCALPHA)
            for y in range(0, height + 1, tile.height):
                image.blit(tile_image, (0, y))
            self.ladder_cache[string][size_string] = image
        return image

    def get_obstacle_image(self, string, width, height):
        image_library = self.obstacle_cache.get(self.obstacle_image)
        size_string = str(width) + 'x' + str(height)
        image = None
        if image_library is None:
            image_library = {}
            self.obstacle_cache[string] = image_library

        image = image_library.get(size_string)
        if image is None:
            tile_image = pygame.image.load(self.obstacle_image)
            tile = Vec2D(tile_image.get_size())
            image = pygame.Surface([width, height])
            for x in range(0, width + 1, tile.width):
                for y in range(0, height + 1, tile.height):
                    image.blit(tile_image, (x, y))
            self.obstacle_cache[string][size_string] = image
        return image

    def get_image(self, string):
        image = self.image_cache.get(string)
        if image is None:
            image = pygame.image.load(string)
            self.image_cache[string] = image
        return image

    def draw(self, entity):
        image = None

        if type(entity) == Ball:

            image = self.get_image('assets/gfx/' + str(entity.radius) + '.png')
            self.screen.blit(image, entity.position - entity.radius)

        elif type(entity) == Bonus:

            if entity.bonus_type == BonusType.stop_time:
                image = self.get_image('assets/gfx/BonusStopTime.png')
            elif entity.bonus_type == BonusType.extra_hook:
                image = self.get_image('assets/gfx/BonusExtraHook.png')
            elif entity.bonus_type == BonusType.chain_hook:
                image = self.get_image('assets/gfx/BonusChainHook.png')
            elif entity.bonus_type == BonusType.break_balls_once:
                image = self.get_image('assets/gfx/BonusBreakBallsOnce.png')
            elif entity.bonus_type == BonusType.break_balls_max:
                image = self.get_image('assets/gfx/BonusBreakBallsMax.png')
            elif entity.bonus_type == BonusType.invulnerability:
                image = self.get_image('assets/gfx/BonusShield.png')
            self.screen.blit(image, entity.position)

        elif type(entity) == Hook:

            if entity.hook_type == HookType.rope:
                image = self.get_image('assets/gfx/HookRope.png')
            elif entity.hook_type == HookType.chain:
                image = self.get_image('assets/gfx/HookChain.png')
            self.screen.blit(image, entity.position, ((0, 0), entity.size))

        elif type(entity) == Ladder:

            image = self.get_ladder_image('assets/gfx/Ladder.png',
                                          entity.width, entity.height)
            self.screen.blit(image, entity.position)

        elif type(entity) == Obstacle:

            image = self.get_obstacle_image(self.obstacle_image,
                                            entity.width, entity.height)
            self.screen.blit(image, entity.position)
