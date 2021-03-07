import pygame as pg
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, game, sound):
        self.screen = game.screen
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.sound = sound
        self.ships = Group()

        self.text_color = (230, 230, 230)
        self.score_font = pg.font.SysFont(None, 80)
        self.font = pg.font.SysFont(None, 40)
        self.score_image, self.score_rect = None, None
        self.high_score_image, self.high_score_rect = None, None
        self.level_image, self.level_rect = None, None
        self.level_label, self.score_label, self.high_score_label = None, None, None
        self.level_label_rect, self.score_label_rect, self.high_score_label_rect = None, None, None
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.right_corner_box = pg.Surface((200, 80), pg.SRCALPHA, 32)
        self.high_scores_image, self.hs_rect = None, None
        self.top_scores = None
        self.array = []

    def read_scores(self, filename):
        self.array = []
        with open(filename) as f:
            for line in f:
                self.array.append(int(line))
        f.close()
        self.array.sort(reverse=True)
        self.stats.high_score = self.array[0]

    def prep_score(self):
        self.score_label = self.font.render('SCORE: ', True, self.text_color)
        self.score_label_rect = self.score_label.get_rect()
        self.score_label_rect.left = self.screen_rect.left + 20
        self.score_label_rect.top = 10

        rounded_score = int(round(self.stats.score))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.score_label_rect.right + 5
        self.score_rect.top = 10

    def check_high_score(self, score):
        if score > self.stats.high_score:
            self.stats.high_score = score
            self.prep_high_score()

    def prep_high_score(self):
        self.high_score_label = self.font.render('HIGH SCORE:', True, self.text_color, self.settings.bg_color)
        self.high_score_label_rect = self.high_score_label.get_rect()
        self.high_score_label_rect.centerx = self.screen_rect.centerx - 60
        self.high_score_label_rect.top = self.score_rect.top

        rounded_score = int(round(self.stats.high_score))
        score_str = "{:,}".format(rounded_score)
        self.high_score_image = self.font.render(score_str, True, self.text_color,
                                                 self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.high_score_label_rect.right + 10
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        self.level_label = self.font.render('LEVEL:  ', True, self.text_color)
        self.level_label_rect = self.level_label.get_rect()
        self.level_label_rect.left = self.screen_rect.left + 20
        self.level_label_rect.top = self.score_rect.bottom + 10

        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                            self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.level_label_rect.right + 5
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            ship = Ship(game=self.game, sound=self.sound)
            ship.rect.x = (self.screen_rect.width - ship.rect.width * self.settings.ship_limit) + i * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score_display(self, filename):
        self.high_scores_image = self.score_font.render('~~~ HIGH SCORES ~~~', True, self.text_color,
                                                        self.settings.barrier_color)
        self.hs_rect = self.high_scores_image.get_rect()
        self.hs_rect.centerx, self.hs_rect.y = self.screen_rect.centerx, self.screen_rect.y + 10

        self.screen.fill(self.settings.barrier_color)
        self.screen.blit(self.high_scores_image, self.hs_rect)
        self.top_scores = Group()
        self.read_scores(filename)
        length = len(self.array)

        if length > 10:
            length = 10
        i = 0
        while i < length:
            number = self.score_font.render(f"{str(i+1)+'.' :>3}", True, self.text_color,
                                            self.settings.barrier_color)
            number_rect = number.get_rect()
            number_rect.right = round(self.screen_rect.centerx * 3 / 4)
            number_rect.y = self.screen_rect.y + 100 + i * number_rect.height
            self.screen.blit(number, number_rect)
            score = self.score_font.render(str(self.array[i]), True, self.text_color, self.settings.barrier_color)
            score_rect = score.get_rect()
            score_rect.left = number_rect.right + 10
            score_rect.y = number_rect.y
            self.screen.blit(score, score_rect)
            i += 1

        exit_prompt = self.font.render('Click High Scores Button to Go Back to Start', True, self.text_color,
                                       self.settings.barrier_color)
        ep_rect = exit_prompt.get_rect()
        ep_rect.centerx, ep_rect.y = self.screen_rect.centerx, self.screen_rect.bottom - ep_rect.height
        self.screen.blit(exit_prompt, ep_rect)

    def show_score(self):
        self.screen.blit(self.high_score_label, self.high_score_label_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.level_label, self.level_label_rect)
        self.screen.blit(self.score_label, self.score_label_rect)
        self.ships.draw(self.screen)
