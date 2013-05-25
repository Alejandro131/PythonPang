import pygame
from pygame.locals import *
from collections import OrderedDict
from pang.lib.world.settings import *
from pang.lib.world.vec2d import Vec2D

class Menu:
    def __init__(self, title):
        self.labels = OrderedDict()
        self.font_size = MENU_LABEL_FONT_SIZE
        self.font = pygame.font.SysFont(None, self.font_size)
        self.selected_color = (255, 0, 0)
        self.color = (255, 255, 255)
        self.selected_option = None
        self.active = False
        self.title_text = self.font.render(title, True, self.color)
        self.dimmer_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),
                                          pygame.SRCALPHA, 32)
        self.dimmer_rect.fill((0, 0, 0, 192))      
        pygame.mixer.music.load('../music/Menu.wav')
        pygame.mixer.music.play(-1)
        
    def process_events(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]: #enter -> invoke the function attached to the currently selected label
            if self.labels[self.selected_option][2]:
                if len(self.labels[self.selected_option]) == 4:
                    self.labels[self.selected_option][2](self.labels[self.selected_option][3])
                else:
                    self.labels[self.selected_option][2]()
                self.active = False
        if key[pygame.K_UP]:
            if self.selected_option:
                self.selected_option -= 1
        if key[pygame.K_DOWN]:
            if self.selected_option < len(self.labels) - 1:
                self.selected_option += 1
        
    def add_option(self, caption, function, arg=None):
        text = self.font.render(caption, True, self.color)
        text_selected = self.font.render('-> '+caption+' <-', True, 
                                         self.selected_color)
        if arg:
            self.labels[len(self.labels.items())] = (text, text_selected, function, arg)
        else:
            self.labels[len(self.labels.items())] = (text, text_selected, function)
        if len(self.labels.items()) == 1:
            self.selected_option = 0
            
    def draw(self, screen):
        screen.blit(self.dimmer_rect, (0, 0))
        max_height = self.title_text.get_rect().height
        items = len(self.labels.items()) + 2
        for key, value in self.labels.items():
            text_height = value[0].get_rect().height
            if text_height > max_height:
                max_height = text_height
        current_y_pos = (SCREEN_HEIGHT - (items * max_height + (items - 1) * \
                                          MENU_LABEL_MARGIN))//2
        position = Vec2D((SCREEN_WIDTH - self.title_text.get_rect().width)//2, 
                                     current_y_pos + (max_height - \
                                                      self.title_text.get_rect().height)//2)
        screen.blit(self.title_text, position)
        current_y_pos += 2 * (max_height + MENU_LABEL_MARGIN)
        for key, value in self.labels.items():
            position = Vec2D((SCREEN_WIDTH - value[0].get_rect().width)//2, 
                             current_y_pos + (max_height - \
                                              value[0].get_rect().height)//2)
            if self.selected_option == key:
                position -= ((value[1].get_rect().width - \
                              value[0].get_rect().width)//2, 0)
                screen.blit(value[1], position)
            else:
                screen.blit(value[0], position)
            current_y_pos += max_height + MENU_LABEL_MARGIN
