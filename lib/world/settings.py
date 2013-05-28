import os
import pygame

GRAVITY = 9.8 * 10
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
MIN_BALL_RADIUS = 5
GAME_SPEED = 1.7
FPS = 60
PLAYER_SPEED = 100
PLAYER_ANIM_SPEED = 8
HOOK_SPEED = 200
HOOK_RELOAD_TIME = 0.5 #number of seconds needed to reload the hook
HOOK_DURATION = 5 #number of seconds the chain hook remains after it attaches
PAUSE_ON_LEVEL_LOAD = 2.99 #number of seconds to pause the game after it loads
BONUS_SPAWN_CHANCE = 0.15 #0.2 #number between 0 and 1
MENU_LABEL_FONT_SIZE = 35
MENU_LABEL_MARGIN = 20
BONUS_DURATION = 5
os.environ['SDL_VIDEO_CENTERED'] = '1'
