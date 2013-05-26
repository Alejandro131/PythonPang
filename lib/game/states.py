from pang.lib.world.world import World
from pang.lib.score.scoreboard import ScoreBoard
from pang.lib.menu.menu import Menu
import pygame
from pygame.locals import *

class StateManager:
    def __init__(self, main_menu_func):
        self.states = []
        self.main_menu_func = main_menu_func
    
    def push(self, state):
        if type(state) == World:
            self.states = []
            pygame.mixer.music.load(state.music_path)
            pygame.mixer.music.play(-1)
        else:
            if len(self.states):
                if type(state) != type(self.states[-1]):
                    pygame.mixer.music.load(state.music_path)
                    pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(state.music_path)
                pygame.mixer.music.play(-1)                

        self.states.append(state)
    
    def pop(self):
        if type(self.states[-2]) != type(self.states[-1]):
            pygame.mixer.music.load(self.states[-2].music_path)
            pygame.mixer.music.play(-1)              

        self.states.pop()
    
    def process_events(self):        
        self.states[-1].process_events()
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
                self.states[-1].draw(screen)
        else:
            self.states[-1].draw(screen)

    def update(self, time_passed):
        self.states[-1].update(time_passed)
        
    def get_world(self):
        for state in self.states:
            if type(state) == World:
                return state
