import pygame
from pygame.locals import *
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D
from pang.lib.world.object2d import Object2D


class Ball(Object2D):

    def __init__(self, radius, position, force, load_image=True):
        Object2D.__init__(self, Vec2D(radius * 2, radius * 2), position)
        self.radius = radius
        self.position = position
        self.force = force
        self.falling = True
        if force.y < 0:
            self.falling = False
        self.max_height = SCREEN_HEIGHT - 150 - radius*4
        if load_image:
            self.image = pygame.image.load('../Graphics/' + str(radius) +
                                           '.png')

    def update(self, time_passed):
        self.force += (0, GRAVITY * time_passed)
        self.position += self.force * time_passed
        if self.x < self.radius or self.x > SCREEN_WIDTH - self.radius:
            self.force = Vec2D(-self.force.x, self.force.y)
            if self.x < self.radius:
                self.position = Vec2D(2*self.radius - self.x, self.y)
            else:
                self.position = Vec2D(2*(SCREEN_WIDTH-self.radius) - self.x,
                                      self.y)
        if self.y > SCREEN_HEIGHT - self.radius:
            self.position = Vec2D(self.x,
                                  2*(SCREEN_HEIGHT-self.radius) - self.y)
            self.force = Vec2D(self.force.x, -(((self.y-self.max_height) *
                                                2*GRAVITY) ** .5))
        if self.force.y > 0:
            self.falling = True
        else:
            self.falling = False

    def calculate_force(self, force):
        """Function takes as a parameter the Vec2D object returned from the
        collision function and changes the x/y direction if the force isn't 0
        """
        if force.x:
            self.force = Vec2D(-self.force.x, self.force.y)
        if force.y:
            if self.y < self.max_height:
                self.force = Vec2D(self.force.x, 0)
            else:
                if self.falling:
                    self.force = Vec2D(self.force.x,
                                       -(abs((self.y-self.max_height)*2 *
                                             GRAVITY) ** .5))
                else:
                    self.force = Vec2D(self.force.x, -self.force.y)

    def draw(self, screen):
        screen.blit(self.image, self.position - self.radius)
