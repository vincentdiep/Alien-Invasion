import sys
import pygame as pg
from scoreboard import Scoreboard as sb


def check_keydown_events(event, sound, ship):
    if event.key == pg.K_RIGHT: ship.moving_right = True
    elif event.key == pg.K_LEFT: ship.moving_left = True
    elif event.key == pg.K_SPACE: ship.shooting_bullets = True
    elif event.key == pg.K_q: sys.exit()

def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT: ship.moving_right = False
    elif event.key == pg.K_LEFT: ship.moving_left = False
    elif event.key == pg.K_SPACE: ship.shooting_bullets = False

def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

def check_score_button(stats, score_button, mouse_x, mouse_y, score_menu):
    if score_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = False
        if score_menu.show_scores_menu:
            score_menu.show_scores_menu = False
        elif not score_menu.show_scores_menu:
            score_menu.show_scores_menu = True

def check_events(sound, stats, play_button, ship, score_button, score_menu):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_score_button(stats=stats, score_button=score_button, mouse_x=mouse_x, mouse_y=mouse_y, score_menu=score_menu)
            check_play_button(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN: check_keydown_events(event=event, sound=sound,
                                                            ship=ship)
        elif event.type == pg.KEYUP: check_keyup_events(event=event, ship=ship)
