import pygame

from pang.vec2d import Vec2D
from pang.object2d import Object2D


class Obstacle(Object2D):

    def __init__(self, size, position):
        Object2D.__init__(self, size, position)
