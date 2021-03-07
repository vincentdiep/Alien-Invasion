import pygame as pg
import pygame.font
from settings import Settings


class Button:
    def __init__(self, settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.width, self.height = 200, 50
        self.button_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.msg_image = self.msg_image_rect = None
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.settings.bg_color)
        self.settings.title1.draw(self.screen)
        self.settings.title2.draw(self.screen)
        self.settings.alien0_text.draw(self.screen)
        self.settings.alien1_text.draw(self.screen)
        self.settings.alien2_text.draw(self.screen)
        self.settings.alien3_text.draw(self.screen)
        self.screen.blit(self.settings.alien0, (468, 430))
        self.screen.blit(self.settings.alien1, (468, 500))
        self.screen.blit(self.settings.alien2, (468, 570))
        self.screen.blit(self.settings.alien3, (468, 620))
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class HighScoreMenu:
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = Settings()

        self.width, self.height = 200, 50
        self.button_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 80)
        self.msg_image = self.msg_image_rect = None

        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.centerx, self.rect.y = self.screen_rect.centerx, 10
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.rect.width, self.rect.height = self.msg_image_rect.width, self.msg_image_rect.height
        self.rect.centerx = self.screen_rect.centerx

    def draw(self):
        self.screen.blit(self.msg_image, self.rect)
