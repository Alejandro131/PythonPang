import pygame
import os
import re
import datetime
from pygame.locals import *
from pang.lib.world.world import World
from pang.lib.score.scoreboard import ScoreBoard
from pang.lib.menu.menu import Menu
from pang.lib.world.settings import *

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pang')
        pygame.mouse.set_visible(0)
        
        self.world = World()
        
        self.menu = Menu('Pang')
        self.menu.add_option('New Game', self.start_game)
        self.menu.add_option('Load Game', self.enable_load_menu)
        self.menu.add_option('Save Game', self.enable_save_menu)
        self.menu.add_option('Exit', self.close)
        self.menu.active = True
        
        self.scoreboard = ScoreBoard()
        
        self.running = True
        
        self.save_menu = Menu('Save Game')
        self.load_menu = Menu('Load Game')
    
    def back_to_main_menu(self):
        self.menu.active = True
        
    def enable_save_menu(self):
        self.save_menu = Menu('Save Game')
        for save_index in range(1, 11):
            file_path = '../save/' + str(save_index) + '.save'
            label = str(save_index)
            if os.path.isfile(file_path):
                file = open(file_path, 'r')
                lines = file.readlines()
                lines = list(map(str.rstrip, lines))
                match = re.match(r'level (\d+)', lines[0])
                level_id = list(map(int, match.groups()))[0]
                label += ' - ' + datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S %d.%m.%Y')
                label += ' - level ' + str(level_id)
            else:
                label += ' - empty'
            if self.world.active:
                self.save_menu.add_option(label, self.world.save_game, save_index)
            else:
                self.save_menu.add_option(label, None)
        self.save_menu.add_option('Back', self.back_to_main_menu)        
        self.save_menu.active = True
    
    def enable_load_menu(self):
        self.load_menu = Menu('Load Game')
        for load_index in range(1, 11):
            file_path = '../save/' + str(load_index) + '.save'
            label = str(load_index)
            if os.path.isfile(file_path):
                file = open(file_path, 'r')
                lines = file.readlines()
                lines = list(map(str.rstrip, lines))
                match = re.match(r'level (\d+)', lines[0])
                level_id = list(map(int, match.groups()))[0]
                label += ' - ' + datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%H:%M:%S %d.%m.%Y')
                label += ' - level ' + str(level_id)
            else:
                label += ' - empty'
            if os.path.isfile(file_path):
                self.load_menu.add_option(label, self.world.load_game, load_index)
            else:
                self.load_menu.add_option(label, None)
        self.load_menu.add_option('Back', self.back_to_main_menu)
        self.load_menu.active = True
        
    def close(self):
        self.running = False
         
    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            if self.world.active:
                if self.menu.active:
                    self.menu.active = False
                else:
                    self.menu.active = True
                    self.menu.selected_option = 0

        if self.world.active and not (self.menu.active or\
                                      self.load_menu.active or\
                                      self.save_menu.active):
            self.world.process_events()
        if self.menu.active:
            self.menu.process_events()        
        elif self.load_menu.active:
            self.load_menu.process_events()
        elif self.save_menu.active:
            self.save_menu.process_events()        

    def update(self, time_passed):
        if self.world.active and not (self.menu.active or\
                                      self.load_menu.active or\
                                      self.save_menu.active):
            self.world.update(time_passed)

    def render(self):
        self.screen.fill((0, 0, 0))
        if self.world.active:
            self.world.draw(self.screen)
        if self.menu.active:
            self.menu.draw(self.screen)
        elif self.load_menu.active:
            self.load_menu.draw(self.screen)
        elif self.save_menu.active:
            self.save_menu.draw(self.screen)        
        pygame.display.flip()
    
    def cleanup(self):
        pygame.quit()
    
    def start_game(self):
        self.world.load_level(1)     
    
    def main(self):        
        clock = pygame.time.Clock()
        
        while self.running:
            time_passed = clock.tick(FPS)
            time_passed *= GAME_SPEED
            
            for event in pygame.event.get():
                self.process_event(event)
            
            self.update(time_passed / 1000.)

            self.render()
            
        self.cleanup()
