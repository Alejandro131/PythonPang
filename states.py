import pygame
from pygame.locals import *
from pang.world import World
from pang.scoreboard import ScoreBoard
from pang.menu import Menu
from pang.settings import *


class StateManager:

    def __init__(self, main_menu_func):
        self.states = []
        self.main_menu_func = main_menu_func
        self.dimmer_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),
                                          pygame.SRCALPHA, 32)
        self.dimmer_rect.fill((0, 0, 0, 192))

    def push(self, state):
        if type(state) == World:
            self.states = []
            pygame.mixer.music.load(state.music_path)
            pygame.mixer.music.play(-1)
        else:
            if len(self.states):
                if state.music_path != self.states[-1].music_path:
                    pygame.mixer.music.load(state.music_path)
                    pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(state.music_path)
                pygame.mixer.music.play(-1)
        self.states.append(state)

    def pop(self):
        if len(self.states) > 1:
            if self.states[-2].music_path != self.states[-1].music_path:
                pygame.mixer.music.load(self.states[-2].music_path)
                pygame.mixer.music.play(-1)
        self.states.pop()

    def process_event(self, event):
        self.states[-1].process_event(event)
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            if type(self.states[-1]) == World:
                self.main_menu_func()
            else:
                self.pop()

    def draw(self, screen):
        world = self.get_world()
        if world:
            world.draw(screen)
            if world != self.states[-1]:
                screen.blit(self.dimmer_rect, (0, 0))
                self.states[-1].draw(screen)
        else:
            self.states[-1].draw(screen)

    def update(self, time_passed):
        self.states[-1].update(time_passed)

    def get_world(self):
        for state in self.states:
            if type(state) == World:
                return state
