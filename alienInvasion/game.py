import pygame as pg
from settings import Settings
import game_functions as gf

from ship import Ship
from alien import Aliens
from game_stats import GameStats
from scoreboard import Scoreboard
from sound import Sound
from barrier import Barriers

from button import Button, HighScoreMenu
from displayscores import DisplayScores

import time

score_path = 'scores/scores.txt'


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        ship_image = pg.image.load('images/ship.png')
        self.ship_height = ship_image.get_rect().height
        self.hs = 0
        self.sound = Sound(bg_music="sounds/black_fury_bgm.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.aliens = self.stats = self.sb = self.ship = self.score_button = self.score_menu = None
        self.barriers = None
        self.restart()

    def restart(self):
        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play Game")
        self.score_button = HighScoreMenu(screen=self.screen, msg="High Scores")
        self.score_menu = DisplayScores(settings=self.settings)
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(game=self, sound=self.sound)

        self.settings.init_dynamic_settings()
        self.barriers = Barriers(game=self)
        self.aliens = Aliens(ship_height=self.ship_height, game=self, barriers=self.barriers)
        self.ship = Ship(game=self, aliens=self.aliens, sound=self.sound, barriers=self.barriers)
        self.aliens.add_ship(ship=self.ship)

        self.stats.high_score = self.hs
        self.sb.read_scores(score_path)
        self.sb.prep_high_score()

    def play(self):
        while True:
            gf.check_events(stats=self.stats, play_button=self.play_button, ship=self.ship,
                            score_button=self.score_button, score_menu=self.score_menu, sound=self.sound)

            if self.stats.game_active:
                self.ship.update()
                self.aliens.update()

            self.screen.fill(self.settings.bg_color)
            self.ship.draw()
            self.aliens.draw()
            self.barriers.draw()
            self.sb.show_score()

            if not self.stats.game_active:
                self.play_button.draw()
                self.score_button.draw()
                self.sound.pause_bg()
                if self.score_menu.show_scores_menu:
                    self.sb.prep_score_display(score_path)

            else:
                if not self.sound.playing_bg:
                    self.sound.unpause_bg()
            pg.display.flip()

    def reset(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.center_ship()
            time.sleep(0.5)
            self.ship.timer = Ship.timer
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            f = open('scores/scores.txt', 'a')
            f.write(str(self.stats.score))
            f.write('\n')
            f.close()
            self.restart()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
