import pygame
from pygame.locals import *
from pang.lib.menu.menu import Menu
from pang.lib.world.settings import *

class ScoreBoard:
    
    def __init__(self):
        self.menu = Menu(y_position=580)
        self.music_path = '../music/Menu.wav'
        self.adding_score = False
        self.records = []
        self.load_scores()
        self.current_score = 0
        self.current_level = 0
        self.current_name = ''
        self.current_id = 0
        self.dimmer_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),
                                                  pygame.SRCALPHA, 32)
        self.dimmer_rect.fill((0, 0, 0, 192))
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
                        self.current_name.append(chr(event.key))
        else:
            self.menu.process_event(event)
    
    def draw(self, screen):
        if self.adding_score:
            screen.blit(self.dimmer_rect, (0, 0))
            # draw new high score text
            # draw enter name
            # draw blackened box
            # draw name string
        else:
            self.menu.draw(screen)
            # draw Scoreboard text
            # draw Name, Score, Level headers
            # for 1 to 10 draw id, name, score, level

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
        #add code
        pass
    
    def save_scores(self):
        #add code
        pass
    
    def add_score(self):
        if len(self.records) < 10:
            self.records.append((self.current_name, self.current_score,
                                 self.current_level))
        else:
            self.records[self.current_id] = (self.current_name,
                                             self.current_score,
                                             self.current_level)
        self.adding_score = False

    def add_option(self, caption, function, arg=None):
        self.menu.add_option(caption, function, arg)

    def get_text(self, string):
        text = self.text_cache.get(string)
        if text == None:
            text = self.font.render(string, True, (255, 255, 255))
            self.text_cache[string] = text
        return text
