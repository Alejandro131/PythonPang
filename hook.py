import pygame

from pang.settings import HOOK_DURATION, HOOK_SPEED
from pang.vec2d import Vec2D
from pang.object2d import Object2D


class HookType:
    rope = 0
    chain = 1


class Hook(Object2D):

    def __init__(self, height, position, hook_type):
        self.hook_type = hook_type
        self.to_kill = False
        if hook_type == HookType.rope:
            self.image = pygame.image.load('assets/gfx/HookRope.png')
        elif hook_type == HookType.chain:
            self.image = pygame.image.load('assets/gfx/HookChain.png')
        Object2D.__init__(self, Vec2D(self.image.get_width(), height),
                          position)
        self.expand = True
        self.timer = HOOK_DURATION

    def update(self, time_passed):
        if not self.expand:
            self.timer -= time_passed
            if self.timer < 0:
                self.to_kill = True
        if self.y > 0 and self.expand:
            increment = HOOK_SPEED * time_passed
            self.size += (0, increment)
            self.position -= (0, increment)
        if self.y < 0:
            if self.hook_type == HookType.rope:
                self.to_kill = True
            elif self.hook_type == HookType.chain:
                self.size += (0, self.y)
                self.position = Vec2D(self.x, 0)
                self.expand = False

    def draw(self, screen):
        screen.blit(self.image, self.position, ((0, 0), self.size))
