import pygame as pg
from os.path import abspath, dirname
from text import Text
from random import randint

FONT = abspath(dirname(__file__)) + '/fonts/' + 'space_invaders.ttf'

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Dynamic Settings
        self.ship_speed_factor = 4
        self.alien_bullet_speed_factor = 1
        self.ship_bullet_speed_factor = 3
        self.alien_speed = 1
        self.ufo_speed = 2
        self.fleet_direction = 1
        self.ufo_direction = 1
        self.speedup_scale = 1.1

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.title1 = Text(FONT, 80, 'ALIEN', WHITE, self.screen_width / 2, self.screen_height / 4)
        self.title2 = Text(FONT, 50, 'INVASION', GREEN, self.screen_width / 2, self.screen_height / 4 + 80)

        self.ship_limit = 3
        self.alien_bullet_width = 2
        self.alien_bullet_height = 30
        self.alien_bullets_every = randint(200, 700)

        self.ship_bullet_height = 50
        self.ship_bullet_width = 5
        self.ship_bullets_every = 1
        self.ship_bullets_allowed = 3

        self.fleet_drop_speed = 7
        self.debounce = 0.0001

        self.score_scale = 1.5

        self.init_dynamic_settings()

        self.barrier_color = 66, 66, 66

        self.alien0 = pg.image.load('images/alien00.png')
        self.alien1 = pg.image.load('images/alien10.png')
        self.alien2 = pg.image.load('images/alien20.png')
        self.alien3 = pg.image.load('images/alien30.png')

        self.alien0_text = Text(FONT, 25, '     =   90 pts', PINK, self.screen_width / 2,
                                self.screen_height * 57 / 100)
        self.alien1_text = Text(FONT, 25, '     =   70 pts', BLUE, self.screen_width / 2,
                                self.screen_height * 57 / 100 + 60)
        self.alien2_text = Text(FONT, 25, '     =   50 pts', GREEN, self.screen_width / 2,
                                self.screen_height * 57 / 100 + 120)
        self.alien3_text = Text(FONT, 25, '     =   ?????', RED, self.screen_width / 2,
                                self.screen_height * 57 / 100 + 180)

    def init_dynamic_settings(self):
        self.ship_speed_factor = 4
        self.alien_bullet_speed_factor = 1
        self.ship_bullet_speed_factor = 3
        self.alien_speed = 1
        self.ufo_speed = 2
        self.fleet_direction = 1
        self.ufo_direction = 1
        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.alien_speed *= scale
