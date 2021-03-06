import os
import re
from datetime import datetime

import pygame
from pygame.locals import *

from pang.world import World
from pang.scoreboard import ScoreBoard
from pang.menu import Menu
from pang.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_SPEED, FPS
from pang.states import StateManager


class Game:

    def __init__(self):
        #pre initialize mixer so that there isn't a delay when playing sounds
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pang')
        pygame.mouse.set_visible(0)
        self.states = StateManager(self.enable_main_menu)
        self.enable_main_menu()
        self.running = True

    def enable_score_board(self):
        score_board = ScoreBoard()
        score_board.add_option('Clear Scores', score_board.clear_scores)
        score_board.add_option('Back', self.states.pop)
        self.states.push(score_board)

    def enable_main_menu(self):
        menu = Menu('Pang')
        menu.add_option('New Game', self.start_game)
        menu.add_option('Load Game', self.enable_load_menu)
        menu.add_option('Save Game', self.enable_save_menu)
        menu.add_option('High Scores', self.enable_score_board)
        menu.add_option('Exit', self.close)
        self.states.push(menu)

    def enable_save_menu(self):
        save_menu = Menu('Save Game')
        for save_index in range(1, 11):
            file_path = 'assets/save/' + str(save_index) + '.save'
            label = str(save_index)
            if os.path.isfile(file_path):
                file = open(file_path, 'r')
                lines = file.readlines()
                lines = list(map(str.rstrip, lines))
                match = re.match(r'level (\d+)', lines[0])
                level_id = list(map(int, match.groups()))[0]
                date = datetime.fromtimestamp(os.path.getmtime(file_path))
                label += ' - ' + date.strftime('%H:%M:%S %d.%m.%Y')
                label += ' - level ' + str(level_id)
            else:
                label += ' - empty'
            if self.states.get_world():
                save_menu.add_option(label, self.save_game, save_index)
            else:
                save_menu.add_option(label, None)
        save_menu.add_option('Back', self.states.pop)
        self.states.push(save_menu)

    def enable_load_menu(self):
        load_menu = Menu('Load Game')
        for load_index in range(1, 11):
            file_path = 'assets/save/' + str(load_index) + '.save'
            label = str(load_index)
            if os.path.isfile(file_path):
                file = open(file_path, 'r')
                lines = file.readlines()
                lines = list(map(str.rstrip, lines))
                match = re.match(r'level (\d+)', lines[0])
                level_id = list(map(int, match.groups()))[0]
                date = datetime.fromtimestamp(os.path.getmtime(file_path))
                label += ' - ' + date.strftime('%H:%M:%S %d.%m.%Y')
                label += ' - level ' + str(level_id)
            else:
                label += ' - empty'
            if os.path.isfile(file_path):
                load_menu.add_option(label, self.load_game, load_index)
            else:
                load_menu.add_option(label, None)
        load_menu.add_option('Back', self.states.pop)
        self.states.push(load_menu)

    def load_game(self, file_name):
        world = World(self.screen)
        world.load_game(file_name)
        self.states.push(world)

    def save_game(self, file_name):
        world = self.states.get_world()
        world.save_game(file_name)
        self.states.pop()

    def start_game(self):
        world = World(self.screen)
        world.load_level(1)
        self.states.push(world)

    def close(self):
        self.running = False

    def process_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        self.states.process_event(event)

    def update(self, time_passed):
        self.states.update(time_passed)
        world = self.states.get_world()
        if world:
            if world.game_over:
                score_board = ScoreBoard()
                score_board.add_option('Clear Scores',
                                       score_board.clear_scores)
                score_board.add_option('Back', self.states.pop)
                score_board.check_score(world.score, world.current_level)
                self.states.states = []
                self.enable_main_menu()
                self.states.push(score_board)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.states.draw(self.screen)
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()

    def main(self):
        clock = pygame.time.Clock()
        while self.running:
            time_passed = clock.tick(FPS)
            time_passed *= GAME_SPEED
            for event in pygame.event.get():
                self.process_event(event)
                if not len(self.states.states):
                    break
            if not len(self.states.states):
                break
            self.update(time_passed / 1000.)
            self.render()
        self.cleanup()
