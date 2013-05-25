import pygame
from pygame.locals import *
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D

class BonusType:
    stop_time = 0
    extra_hook = 1
    chain_hook = 2
    break_balls_once = 3
    break_balls_max = 4
    def __len__(self):
        return 5   

class Bonus(Object2D):
    def __init__(self, position, bonus_type):
        self.bonus_type = bonus_type
        if bonus_type == BonusType.stop_time:
            self.image = pygame.image.load('../graphics/BonusStopTime.png')
        elif bonus_type == BonusType.extra_hook:
            self.image = pygame.image.load('../graphics/BonusExtraHook.png')
        elif bonus_type == BonusType.chain_hook:
            self.image = pygame.image.load('../graphics/BonusChainHook.png')
        elif bonus_type == BonusType.break_balls_once:
            self.image = pygame.image.load('../graphics/BonusBreakBallsOnce.png')
        elif bonus_type == BonusType.break_balls_max:
            self.image = pygame.image.load('../graphics/BonusBreakBallsMax.png')
        Object2D.__init__(self, Vec2D(self.image.get_size()), position)
        self.force = Vec2D()
        self.to_kill = False
        self.fall = True
        self.timer = BONUS_DURATION

    def update(self, time_passed):
        if not self.fall:
            self.timer -= time_passed
            if self.timer < 0:
                self.to_kill = True
        else:
            self.force += (0, GRAVITY * time_passed)
            self.position += (0, self.force.y * time_passed)
            if self.y > SCREEN_HEIGHT - self.height:
                self.position = Vec2D(self.x, SCREEN_HEIGHT - self.height)
                self.fall = False

    def draw(self, screen):
        screen.blit(self.image, self.position)
