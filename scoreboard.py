import re
import os

import pygame
from pygame.locals import *

from pang.menu import Menu
from pang.settings import MENU_LABEL_FONT_SIZE, SCREEN_WIDTH, MENU_LABEL_MARGIN


class ScoreBoard:

    def __init__(self):
        self.menu = Menu(y_position=580)
        self.music_path = 'assets/music/Menu.wav'
        self.adding_score = False
        self.records = []
        self.load_scores()
        self.current_score = 0
        self.current_level = 0
        self.current_name = ''
        self.current_id = 0
        self.font = pygame.font.SysFont(None, MENU_LABEL_FONT_SIZE)
        self.text_cache = {}

    def process_event(self, event):
        if self.adding_score:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if len(self.current_name) > 0:
                        self.current_name = self.current_name[0:-1]
                elif event.key == K_RETURN:
                    if len(self.current_name) > 0:
                        self.add_score()
                elif event.key <= 127:
                    if len(self.current_name) < 10:
                        new_character = '' + chr(event.key)
                        if bool(event.mod & KMOD_SHIFT) ^\
                           bool(event.mod & KMOD_CAPS):
                            new_character = new_character.upper()
                        self.current_name += new_character
        else:
            self.menu.process_event(event)

    def draw(self, screen):
        if self.adding_score:
            hscore_text = self.get_text('New High Score')
            screen.blit(hscore_text,
                        ((SCREEN_WIDTH-hscore_text.get_rect().width) // 2,
                         200))
            ename_text = self.get_text('Enter Name:')
            screen.blit(ename_text, (200, 300))
            screen.blit(self.get_text(self.current_name),
                        (220 + ename_text.get_rect().width, 300))
        else:
            self.menu.draw(screen)
            sboard_text = self.get_text('Score Board')
            screen.blit(sboard_text,
                        ((SCREEN_WIDTH-sboard_text.get_rect().width) // 2, 30))
            screen.blit(self.get_text('Name'), (150, 100))
            screen.blit(self.get_text('Score'), (450, 100))
            screen.blit(self.get_text('Level'), (750, 100))
            y_pos = 150
            for index, record in enumerate(self.records):
                screen.blit(self.get_text(str(index + 1)), (100, y_pos))
                screen.blit(self.get_text(record[0]), (150, y_pos))
                score_text = self.get_text(str(record[1]))
                screen.blit(score_text, (450, y_pos))
                screen.blit(self.get_text(str(record[2])), (750, y_pos))
                y_pos += MENU_LABEL_MARGIN + score_text.get_rect().height

    def update(self, time_passed):
        self.menu.update(time_passed)

    def check_score(self, score, level):
        if len(self.records) < 10:
            self.current_score = score
            self.current_level = level
            self.current_name = ''
            self.current_id = 0
            self.adding_score = True
        else:
            higher_scores = len(filter(lambda x: x[1] > score, self.records))
            if higher_scores < 10:
                self.current_score = score
                self.current_level = level
                self.current_name = ''
                self.current_id = higher_scores
                self.adding_score = True

    def clear_scores(self):
        self.records = []
        self.save_scores()

    def load_scores(self):
        file_path = 'assets/highscore/scores.pang'
        if not os.path.isfile(file_path):
            return None
        file = open(file_path, 'r')
        lines = file.readlines()
        lines = list(map(str.rstrip, lines))
        for line in lines:
            if re.match(r'(\S+) (\d+) (\d+)', line):
                match = re.match(r'(\S+) (\d+) (\d+)', line)
                name, score, level = list(map(str, match.groups()))
                score = int(score)
                level = int(level)
                self.records.append((name, score, level))

    def save_scores(self):
        file_path = 'assets/highscore/scores.pang'
        file = open(file_path, 'w')
        for record in self.records:
            file.write(str(record[0]) + ' ' + str(record[1]) + ' ' +
                       str(record[2]) + '\n')

    def add_score(self):
        if len(self.records) < 10:
            self.records.append((self.current_name, self.current_score,
                                 self.current_level))
        else:
            self.records[self.current_id] = (self.current_name,
                                             self.current_score,
                                             self.current_level)
        self.adding_score = False
        self.records.sort(reverse=True, key=lambda x: x[1])
        self.save_scores()

    def add_option(self, caption, function, arg=None):
        self.menu.add_option(caption, function, arg)

    def get_text(self, string):
        text = self.text_cache.get(string)
        if text is None:
            text = self.font.render(string, True, (255, 255, 255))
            self.text_cache[string] = text
        return text
