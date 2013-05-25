from pang.lib.world.hook import HookType
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D
import pygame

class Player(Object2D):
    def __init__(self, position):
        self.can_climb = False
        self.is_climbing = False
        self.hook_type = HookType.rope
        self.max_hooks = 1
        self.image = pygame.image.load('../graphics/Player.png')
        self.sheet_size = Vec2D(self.image.get_width(), self.image.get_height())
        Object2D.__init__(self, Vec2D(self.image.get_width()/4, self.image.get_height()/2), position)
        self.rect = (0, 0, self.width, self.height)
        #maybe have separate collision box for player than his image but we will think later on
        self.force = Vec2D()
        self.direction = Vec2D()
        self.frame_left = 0
        self.frame_right = 0
        self.last_direction = 0
        self.last_shooting = 0
        self.can_shoot = True
        self.ladder_span = Vec2D()
    
    def move(self, direction):
        """
        direction - Point containing x and y orientation
                    represented by -1, 0 or 1
        """
        self.direction = direction
        if direction.x:
            self.last_direction = direction.x
        #pass
    
    def update(self, time_passed):
        '''if self.can_climb:
            if self.direction.y:
                self.position += (0, self.direction.y * time_passed * PLAYER_SPEED)
                self.is_climbing = True
                self.frame_right = 0 #с цел ако отидеш на стълба в друг фрейм
                self.frame_left = 0 #да се върнеш на основния
                y_pos = int(self.y + self.height)
                if y_pos <= self.ladder_span[0]:
                    self.is_climbing = False
                    #self.can_climb = False
                    self.position = Vec2D(self.x, self.ladder_span[0] - self.height)
                elif y_pos >= self.ladder_span[1]:
                    self.is_climbing = False
                    #self.can_climb = False
                    #self.position = Vec2D(self.x, self.ladder_span[1] - self.height)'''
        
        if not self.is_climbing:
            if self.y < SCREEN_HEIGHT - self.height:
                self.force += (0, GRAVITY * time_passed)
                self.position += (0, self.force.y * time_passed)
            if self.direction.x:
                self.position += (self.direction.x * time_passed * PLAYER_SPEED,
                                  0)
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
        
        #self.ladder_span 
        if self.can_climb:
            if self.direction.y:
                self.position += (0, 
                                  self.direction.y * time_passed * PLAYER_SPEED)
                self.is_climbing = True
                self.frame_right = 0 #с цел ако отидеш на стълба в друг фрейм
                self.frame_left = 0 #да се върнеш на основния
        else:
            self.is_climbing = False
        if self.y > SCREEN_HEIGHT - self.height:
            self.position = Vec2D(self.x, SCREEN_HEIGHT - self.height)
            self.is_climbing = False

        #calculate animation to display
        update_speed = 1. / PLAYER_ANIM_SPEED# * GAME_SPEED
        if self.frame_right:
            self.frame_right %= 4 * update_speed
            frame = int(self.frame_right / update_speed) % 4
            self.rect = (frame * self.width, 0, self.width, self.height)
        elif self.frame_left:
            self.frame_left %= 4 * update_speed
            frame = int(self.frame_left / update_speed) % 4
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