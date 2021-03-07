import pygame as pg


class Text(object):
    def __init__(self, text_font, size, message, color, centerx, ypos):
        self.font = pg.font.Font(text_font, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(centerx=centerx, top=ypos)

    def draw(self, surface):
        surface.blit(self.surface, self.rect)