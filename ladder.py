import pygame

from pang.vec2d import Vec2D
from pang.object2d import Object2D
from pang.settings import LADDER_WIDTH


class Ladder(Object2D):

    def __init__(self, height, position):
        Object2D.__init__(self, Vec2D(LADDER_WIDTH, height), position)
