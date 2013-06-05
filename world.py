import re
import os
import random

import pygame
from pygame.locals import *

from pang.settings import *
from pang.obstacle import Obstacle
from pang.player import Player
from pang.bonus import *
from pang.ball import Ball
from pang.collision import *
from pang.hook import *
from pang.ladder import Ladder
from pang.vec2d import Vec2D
from pang.object2d import Object2D


class World:

    def __init__(self):
        self.balls = []
        self.bonuses = []
        self.hooks = []
        self.obstacles = []
        self.ladders = []
        self.player = None
        self.background = None
        self.balls_paused = False
        self.balls_timer = 0
        self.current_level = -1
        self.level_pause = False
        self.pause_remaining = 0
        self.active = False
        self.sound_library = {}
        self.text_cache = {}
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, MENU_LABEL_FONT_SIZE)
        self.game_over = False

    def process_event(self, event):
        key = pygame.key.get_pressed()
        direction = Vec2D()
        if key[pygame.K_LEFT]:
            direction -= (1, 0)
        if key[pygame.K_RIGHT]:
            direction += (1, 0)
        if key[pygame.K_UP]:
            direction -= (0, 1)
        if key[pygame.K_DOWN]:
            direction += (0, 1)
        self.player.set_direction(direction)
        if key[pygame.K_SPACE]:
            self.player_shoot()

    def update(self, time_passed):
        if not self.level_pause:

            if not self.balls_paused:
                for ball in self.balls:
                    ball.update(time_passed)
            else:
                self.balls_timer -= time_passed
                if self.balls_timer < 0:
                    self.balls_paused = False
            for hook in self.hooks:
                hook.update(time_passed)
            for bonus in self.bonuses:
                bonus.update(time_passed)
            self.player.update(time_passed)

            self.check_collisions()

            if not len(self.balls):
                self.play_sound('LevelFinish.wav')
                self.current_level += 1
                if not self.load_level(self.current_level):
                    self.game_over = True
                    self.current_level -= 1

        else:
            self.pause_remaining -= time_passed
            if self.pause_remaining <= 0:
                self.level_pause = False

    def check_collisions(self):
        for ball in self.balls:
            for obstacle in self.obstacles:
                result = ball_to_box(ball, obstacle, True)
                if result:
                    ball.calculate_force(result)

        if self.player.invulnerable:
            for ball in self.balls:
                result = ball_to_box(ball, self.player, True)
                if result:
                    ball.calculate_force(result)

        self.player.can_climb = False
        for ladder in self.ladders:
            if player_to_ladder(self.player, ladder):
                self.player.can_climb = True
                self.player.ladder_span = Vec2D(ladder.y, ladder.y +
                                                ladder.height)

        if not self.player.is_climbing:
            for obstacle in self.obstacles:
                box_to_box(self.player, obstacle, player=True)

        for hook in self.hooks:
            for obstacle in self.obstacles:
                if box_to_box(hook, obstacle, hook=True):
                    break

        for hook_index in range(len(self.hooks) - 1, -1, -1):
            hook = self.hooks[hook_index]
            if hook.to_kill:
                del self.hooks[hook_index]
            else:
                for ball_index in range(len(self.balls) - 1, -1, -1):
                    ball = self.balls[ball_index]
                    if ball_to_box(ball, hook):
                        self.split_ball(ball)
                        del self.balls[ball_index]
                        del self.hooks[hook_index]
                        break

        for bonus_index in range(len(self.bonuses) - 1, -1, -1):
            bonus = self.bonuses[bonus_index]
            if bonus.to_kill:
                del self.bonuses[bonus_index]
            elif box_to_box(bonus, self.player):
                self.activate_bonus(bonus)
                del self.bonuses[bonus_index]

        for bonus_index in range(len(self.bonuses) - 1, -1, -1):
            bonus = self.bonuses[bonus_index]
            for obstacle in self.obstacles:
                box_to_box(bonus, obstacle, bonus=True)

        for ball in self.balls:
            if ball_to_box(ball, self.player):
                self.lives -= 1
                if self.lives:
                    self.load_level(self.current_level)
                    break
                else:
                    self.game_over = True
                    break

    def player_shoot(self):
        if not self.player.is_climbing and \
           self.player.max_hooks > len(self.hooks) and self.player.can_shoot:
            self.play_sound('HookShoot.wav')
            self.hooks.append(Hook(20, Vec2D(self.player.x +
                                             self.player.width/2,
                                             self.player.y +
                                             self.player.height - 20),
                                   self.player.hook_type))
            self.player.last_shooting = HOOK_RELOAD_TIME
            self.player.can_shoot = False

    def split_ball(self, ball):
        self.play_sound('BallPop.wav')
        if ball.radius > MIN_BALL_RADIUS:
            self.balls.append(Ball(ball.radius//2,
                                   Vec2D(ball.x - ball.radius//2, ball.y),
                                   Vec2D(-abs(ball.force.x), -GRAVITY)))
            self.balls.append(Ball(ball.radius//2,
                                   Vec2D(ball.x + ball.radius//2, ball.y),
                                   Vec2D(abs(ball.force.x), -GRAVITY)))
        self.spawn_bonus(ball.position)
        self.score += ball.radius

    def spawn_bonus(self, position):
        if random.randint(1, 100) / 100. < BONUS_SPAWN_CHANCE:
            bonus_type = random.randint(0, len(BonusType()) - 1)
            self.bonuses.append(Bonus(position, bonus_type))

    def activate_bonus(self, bonus):
        self.play_sound('Bonus.wav')
        if bonus.bonus_type == BonusType.stop_time:
            self.balls_paused = True
            self.balls_timer = 3
        elif bonus.bonus_type == BonusType.extra_hook:
            self.player.max_hooks += 1
        elif bonus.bonus_type == BonusType.chain_hook:
            self.player.hook_type = HookType.chain
        elif bonus.bonus_type == BonusType.break_balls_once:
            for ball_index in range(len(self.balls) - 1, -1, -1):
                ball = self.balls[ball_index]
                if ball.radius > MIN_BALL_RADIUS:
                    self.split_ball(ball)
                    del self.balls[ball_index]
        elif bonus.bonus_type == BonusType.break_balls_max:
            big_ballz = True
            while big_ballz:
                big_ballz = False
                for ball_index in range(len(self.balls) - 1, -1, -1):
                    ball = self.balls[ball_index]
                    if ball.radius > MIN_BALL_RADIUS:
                        big_ballz = True
                        self.split_ball(ball)
                        del self.balls[ball_index]
        elif bonus.bonus_type == BonusType.invulnerability:
            self.player.invulnerable = True
            self.player.invulnerability_timer = INVULNERABILITY_DURATION

    def play_sound(self, file_name):
        sound = self.sound_library.get(file_name)
        if sound is None:
            sound = pygame.mixer.Sound('assets/sfx/' + file_name)
            self.sound_library[file_name] = sound
        sound.play()

    def get_text(self, string):
        text = self.text_cache.get(string)
        if text is None:
            text = self.font.render(string, True, (255, 0, 0))
            self.text_cache[string] = text
        return text

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for ladder in self.ladders:
            ladder.draw(screen)
        for hook in self.hooks:
            hook.draw(screen)
        self.player.draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        for bonus in self.bonuses:
            bonus.draw(screen)
        lives_text = self.get_text('Lives: ' + str(self.lives))
        screen.blit(lives_text, (20, 20))
        score_text = self.get_text('Score: ' + str(self.score))
        screen.blit(score_text,
                    (SCREEN_WIDTH - score_text.get_rect().width - 20, 20))
        if self.level_pause:
            pause_text = self.get_text(str(int(self.pause_remaining + 1)))
            screen.blit(pause_text,
                        ((SCREEN_WIDTH-pause_text.get_rect().width) / 2,
                         (SCREEN_HEIGHT-pause_text.get_rect().height) / 2))

    def load_level(self, level_index, scene_only=False, keep_score=True):
        self.active = True
        file_path = 'assets/levels/' + str(level_index) + '.pang'
        if not os.path.isfile(file_path):
            return None
        self.balls = []
        self.bonuses = []
        self.hooks = []
        self.obstacles = []
        self.ladders = []
        self.sound_library = {}
        self.text_cache = {}
        self.balls_paused = False
        self.balls_timer = 0
        if not keep_score:
            self.score = 0
        self.current_level = level_index
        self.level_pause = True
        self.pause_remaining = PAUSE_ON_LEVEL_LOAD
        file = open(file_path, 'r')
        lines = file.readlines()
        lines = list(map(str.rstrip, lines))
        match = re.match(r'background (\S+)', lines[0])
        background = list(map(str, match.groups()))[0]
        self.background = pygame.image.load('assets/gfx/' + background)
        tile_name = ''
        ball_regex = (r'ball radius (\d+) pos (\d+), ' +
                      '(\d+) force (-?\d+), (-?\d+)')
        obstacle_regex = r'obstacle size (\d+), (\d+) pos (\d+), (\d+)'
        for line in lines[1:]:
            if not scene_only and re.match(ball_regex, line):
                match = re.match(ball_regex, line)
                radius, x, y, force_x, force_y = list(map(int, match.groups()))
                self.balls.append(Ball(radius, Vec2D(x, y),
                                       Vec2D(force_x, force_y)))
            elif re.match(obstacle_regex, line):
                match = re.match(obstacle_regex, line)
                width, height, x, y = list(map(int, match.groups()))
                self.obstacles.append(Obstacle(Vec2D(width, height),
                                               Vec2D(x, y), tile_name))
            elif not scene_only and re.match(r'player pos (\d+), (\d+)', line):
                match = re.match(r'player pos (\d+), (\d+)', line)
                point_x, point_y = list(map(int, match.groups()))
                point = Vec2D(point_x, point_y)
                self.player = Player(point)
            elif re.match(r'ladder height (\d+) pos (\d+), (\d+)', line):
                match = re.match(r'ladder height (\d+) pos (\d+), (\d+)', line)
                height, point_x, point_y = list(map(int, match.groups()))
                point = Vec2D(point_x, point_y)
                self.ladders.append(Ladder(height, point))
            elif re.match(r'music (\S+)', line):
                match = re.match(r'music (\S+)', line)
                music = list(map(str, match.groups()))[0]
                self.music_path = 'assets/music/' + music
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(-1)
            elif re.match(r'bricktile (\S+)', line):
                match = re.match(r'bricktile (\S+)', line)
                tile_name = list(map(str, match.groups()))[0]
        return True

    def load_game(self, file_name):
        file_path = 'assets/save/' + str(file_name) + '.save'
        if not os.path.isfile(file_path):
            return None
        file = open(file_path, 'r')
        lines = file.readlines()
        lines = list(map(str.rstrip, lines))
        match = re.match(r'level (\d+)', lines[0])
        level_id = list(map(int, match.groups()))[0]
        self.load_level(level_id, scene_only=True, keep_score=False)
        ball_regex = (r'ball radius (\d+) pos (\d+), ' +
                      '(\d+) force (-?\d+), (-?\d+)')
        player_regex = (r'player pos (\d+), (\d+) hooktype (\d+) maxhooks ' +
                        '(\d+) force (-?\d+), (-?\d+)')
        bonus_regex = (r'bonus pos (\d+), (\d+) bonustype (\d+) duration ' +
                       '(\d+.\d+|\d+) force (-?\d+), (-?\d+) fall (\d+) ' +
                       'tokill (\d+)')
        hook_regex = (r'hook pos (\d+), (\d+) hooktype (\d+) height (\d+) ' +
                      'duration (\d+.\d+|\d+) expand (\d+) tokill (\d+)')
        world_regex = r'world ballstimer (\d+.\d+|\d+) score (\d+) lives (\d+)'
        for line in lines[1:]:
            if re.match(ball_regex, line):
                match = re.match(ball_regex, line)
                radius, x, y, force_x, force_y = list(map(int, match.groups()))
                self.balls.append(Ball(radius, Vec2D(x, y),
                                       Vec2D(force_x, force_y)))
            elif re.match(player_regex, line):
                match = re.match(player_regex, line)
                pos_x = int(match.group(1))
                pos_y = int(match.group(2))
                hook_type = int(match.group(3))
                max_hooks = int(match.group(4))
                force_x = int(match.group(5))
                force_y = int(match.group(6))
                self.player = Player(Vec2D(pos_x, pos_y))
                self.player.hook_type = hook_type
                self.player.max_hooks = max_hooks
                self.player.force = Vec2D(force_x, force_y)
            elif re.match(bonus_regex, line):
                match = re.match(bonus_regex, line)
                pos_x = int(match.group(1))
                pos_y = int(match.group(2))
                bonus_type = int(match.group(3))
                duration = float(match.group(4))
                force_x = int(match.group(5))
                force_y = int(match.group(6))
                fall = bool(int(match.group(7)))
                to_kill = bool(int(match.group(8)))
                bonus = Bonus(Vec2D(pos_x, pos_y), bonus_type)
                bonus.timer = duration
                bonus.force = Vec2D(force_x, force_y)
                bonus.fall = fall
                bonus.to_kill = to_kill
                self.bonuses.append(bonus)
            elif re.match(hook_regex, line):
                match = re.match(hook_regex, line)
                pos_x = int(match.group(1))
                pos_y = int(match.group(2))
                hook_type = int(match.group(3))
                height = int(match.group(4))
                duration = float(match.group(5))
                expand = bool(int(match.group(6)))
                to_kill = bool(int(match.group(7)))
                hook = Hook(height, Vec2D(pos_x, pos_y), hook_type)
                hook.timer = duration
                hook.expand = expand
                hook.to_kill = to_kill
                self.hooks.append(hook)
            elif re.match(world_regex, line):
                match = re.match(world_regex, line)
                balls_timer, score, lives = list(map(float, match.groups()))
                self.balls_timer = balls_timer
                if balls_timer > 0:
                    self.balls_paused = True
                else:
                    self.balls_paused = False
                self.score = int(score)
                self.lives = int(lives)

    def save_game(self, file_name):
        if not self.active:
            return None
        file_path = 'assets/save/' + str(file_name) + '.save'
        file = open(file_path, 'w')
        file.write('level ' + str(self.current_level) + '\n')
        for ball in self.balls:
            file.write('ball radius ' + str(ball.radius) + ' pos ' +
                       str(int(ball.x)) + ', ' + str(int(ball.y)) + ' force ' +
                       str(int(ball.force.x)) + ', ' + str(int(ball.force.y)) +
                       '\n')
        file.write('player pos ' + str(int(self.player.x)) + ', ' +
                   str(int(self.player.y)) + ' hooktype ' +
                   str(self.player.hook_type) + ' maxhooks ' +
                   str(self.player.max_hooks) + ' force ' +
                   str(int(self.player.force.x)) + ', ' +
                   str(int(self.player.force.y)) + '\n')
        for bonus in self.bonuses:
            file.write('bonus pos ' + str(int(bonus.x)) + ', ' +
                       str(int(bonus.y)) + ' bonustype ' +
                       str(int(bonus.bonus_type)) + ' duration ' +
                       str(bonus.timer) + ' force ' + str(int(bonus.force.x)) +
                       ', ' + str(int(bonus.force.y)) + ' fall ' +
                       str(int(bonus.fall)) + ' tokill ' +
                       str(int(bonus.to_kill)) + '\n')
        for hook in self.hooks:
            file.write('hook pos ' + str(int(hook.x)) + ', ' +
                       str(int(hook.y)) + ' hooktype ' +
                       str(int(hook.hook_type)) + ' height ' +
                       str(int(hook.height)) + ' duration ' + str(hook.timer) +
                       ' expand ' + str(int(hook.expand)) + ' tokill ' +
                       str(int(hook.to_kill)) + '\n')
        file.write('world ballstimer ' + str(self.balls_timer) + ' score ' +
                   str(self.score) + ' lives ' + str(self.lives) + '\n')
