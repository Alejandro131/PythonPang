import pygame

from pang.settings import SCREEN_HEIGHT, BONUS_DURATION, GRAVITY, BONUS_SIZE
from pang.vec2d import Vec2D
from pang.object2d import Object2D


class BonusType:
    stop_time = 0
    extra_hook = 1
    chain_hook = 2
    break_balls_once = 3
    break_balls_max = 4
    invulnerability = 5

    def __len__(self):
        return 6


class Bonus(Object2D):

    def __init__(self, position, bonus_type):
        self.bonus_type = bonus_type
        Object2D.__init__(self, Vec2D(BONUS_SIZE, BONUS_SIZE), position)
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
