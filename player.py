import pygame

from pang.hook import HookType
from pang.settings import (SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, PLAYER_SPEED,
                           PLAYER_ANIM_SPEED, GAME_SPEED)
from pang.vec2d import Vec2D
from pang.object2d import Object2D


class Player(Object2D):

    def __init__(self, position):
        self.can_climb = False
        self.is_climbing = False
        self.hook_type = HookType.rope
        self.max_hooks = 1
        self.image = pygame.image.load('assets/gfx/Player.png')
        self.sheet_size = Vec2D(self.image.get_width(),
                                self.image.get_height())
        Object2D.__init__(self, Vec2D(self.image.get_width()/4,
                                      self.image.get_height()/2), position)
        self.rect = (0, 0, self.width, self.height)
        self.force = Vec2D()
        self.direction = Vec2D()
        self.frame_left = 0
        self.frame_right = 0
        self.last_direction = 0
        self.last_shooting = 0
        self.can_shoot = True
        self.ladder_span = Vec2D()

    def set_direction(self, direction):
        self.direction = direction
        if direction.x:
            self.last_direction = direction.x

    def update(self, time_passed):
        if not self.is_climbing:
            if self.y < SCREEN_HEIGHT - self.height:
                self.force += (0, GRAVITY * time_passed)
                self.position += (0, self.force.y * time_passed)
            if self.direction.x:
                self.position += ((self.direction.x * time_passed *
                                   PLAYER_SPEED), 0)
                if self.direction.x > 0:
                    self.frame_right += time_passed
                    self.frame_left = 0
                else:
                    self.frame_left += time_passed
                    self.frame_right = 0
            else:
                self.frame_right = 0
                self.frame_left = 0
            if self.x < 0:
                self.position = Vec2D(0, self.y)
            elif self.x > SCREEN_WIDTH - self.width:
                self.position = Vec2D(SCREEN_WIDTH - self.width, self.y)
        else:
            self.force = Vec2D(self.force.x, 0)

        if self.can_climb:
            if self.direction.y:
                self.position += (0, (self.direction.y * time_passed *
                                      PLAYER_SPEED))
                self.is_climbing = True
                if self.y + self.height <= self.ladder_span[0]:
                    self.position = Vec2D(self.x, self.ladder_span[0] -
                                          self.height)
                    self.can_climb = True
                    self.is_climbing = False
                elif self.y + self.height >= self.ladder_span[1]:
                    self.position = Vec2D(self.x, self.ladder_span[1] -
                                          self.height)
                    self.can_climb = True
                    self.is_climbing = False
                self.frame_right = 0
                self.frame_left = 0
        else:
            self.is_climbing = False
        if self.y > SCREEN_HEIGHT - self.height:
            self.position = Vec2D(self.x, SCREEN_HEIGHT - self.height)
            self.is_climbing = False

        #calculate animation to display
        update_speed = 1. / PLAYER_ANIM_SPEED * GAME_SPEED
        if self.frame_right:
            self.frame_right %= 4 * update_speed
            frame = int(self.frame_right/update_speed) % 4
            self.rect = (frame * self.width, 0, self.width, self.height)
        elif self.frame_left:
            self.frame_left %= 4 * update_speed
            frame = int(self.frame_left/update_speed) % 4
            self.rect = (frame * self.width, self.height, self.width,
                         self.height)
        else:
            if self.last_direction == -1:
                self.rect = (0, self.height, self.width, self.height)
            else:
                self.rect = (0, 0, self.width, self.height)

        if not self.can_shoot:
            self.last_shooting -= time_passed
            if self.last_shooting <= 0:
                self.can_shoot = True

    def draw(self, screen):
        screen.blit(self.image, self.position, self.rect)
