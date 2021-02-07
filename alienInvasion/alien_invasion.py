import pygame as pg

from settings import Settings

from ship import Ship

import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen objects.
    pg.init()
    ai_settings = Settings()
    screen = pg.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pg.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings=ai_settings, screen=screen)

    # Start the main loop for the game.
    while True:
        gf.check_events(ship=ship)
        ship.update()
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship)


def main():
    run_game()


if __name__ == '__main__':
    main()
