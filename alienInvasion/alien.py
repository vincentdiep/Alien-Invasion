import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
from bullet import BulletFromAlien
from random import randint


class Aliens:
    def __init__(self, ship_height, game, barriers):
        self.settings = game.settings
        self.screen = game.screen
        self.ship_height = ship_height
        self.game = game
        self.barriers = barriers
        self.alien_group = Group()
        self.ship_group = Group()
        self.create_fleet()
        self.bullet_group_that_kill_ship = Group()
        self.last_bullet_shot = pg.time.get_ticks()
        self.ship = None
        self.total_aliens = 0

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        alien = Alien(parent=self, game=self.game, row=None)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        aliens_per_row = self.aliens_per_row(settings=settings, alien_width=alien_width)
        rows_per_screen = self.rows_per_screen()
        self.total_aliens = aliens_per_row * rows_per_screen

        for y in range(rows_per_screen):
            for x in range(aliens_per_row):
                alien = Alien(parent=self, game=self.game, number=y // 2, x=alien_width * (4 + 1.5 * x),
                              y=alien_height * (1 + y), row=y)
                self.alien_group.add(alien)

    # noinspection PyMethodMayBeStatic
    def aliens_per_row(self, settings, alien_width):
        space_x = settings.screen_width - 2 * alien_width
        return int(space_x / (2 * alien_width))

    # noinspection PyMethodMayBeStatic
    def rows_per_screen(self): return 6

    def add_bullet(self, game, x, y):
        self.bullet_group_that_kill_ship.add(BulletFromAlien(game=game, x=x, y=y))

    def add(self, alien): self.alien_group.add(alien)

    def add_ship(self, ship):
        self.ship = ship
        self.ship_group.add(self.ship)

    def empty(self): self.alien_group.empty()

    def group(self): return self.alien_group

    def remove(self, alien): self.alien_group.remove(alien)

    def change_direction(self):
        for alien in self.alien_group:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for alien in self.alien_group.sprites():
            if alien.check_edges():
                return True
        return False

    def check_aliens_bottom(self):
        r = self.screen.get_rect()
        for alien in self.alien_group.sprites():
            if alien.rect.bottom > r.bottom:
                return True
        return False

    def one_alien_shoots_if_time(self):
        now = pg.time.get_ticks()
        if now > self.last_bullet_shot + self.settings.alien_bullets_every:
            li = self.alien_group.sprites()
            length = len(li)
            shooter = li[randint(0, length - 1)]
            self.add_bullet(game=self.game, x=shooter.x + 34, y=shooter.y)
            self.last_bullet_shot = now

    def update(self):
        bullet_bullet_collisions = pg.sprite.groupcollide(self.bullet_group_that_kill_ship,
                                                          self.ship.bullet_group(),
                                                          True, False)
        if bullet_bullet_collisions:
            for bullet in bullet_bullet_collisions:
                self.bullet_group_that_kill_ship.remove(bullet)

        self.alien_group.update()

        self.bullet_group_that_kill_ship.update()
        bullet_ship_collisions = pg.sprite.groupcollide(self.bullet_group_that_kill_ship,
                                                        self.ship.group(), True, False)
        if bullet_ship_collisions:
            self.ship.dead = True
            self.ship.killed()

        bullet_barrier_collisions = pg.sprite.groupcollide(self.barriers.group(),
                                                           self.bullet_group_that_kill_ship,
                                                           False, True)
        if bullet_barrier_collisions:
            for barrier_block in bullet_barrier_collisions:
                barrier_block.damaged()

        for bullet in self.bullet_group_that_kill_ship.copy():
            if bullet.rect.bottom <= 0:
                self.bullet_group_that_kill_ship.remove(bullet)

        self.one_alien_shoots_if_time()
        if self.check_edges():
            self.change_direction()
        if self.check_aliens_bottom() or pg.sprite.spritecollideany(self.game.ship, self.alien_group):
            self.game.reset()
            return
        for alien in self.alien_group.copy():
            alien.update()
            if alien.rect.bottom <= 0 or alien.reallydead:
                self.alien_group.remove(alien)

    def draw(self):
        for alien in self.alien_group:
            alien.draw()
        for bullet in self.bullet_group_that_kill_ship:
            bullet.draw()


class Alien(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/alien' + str(number) + str(i) + '.png') for i in range(2)] for number in range(3)]
    images_boom = [pg.image.load('images/alien_boom' + str(i) + '.png') for i in range(3)]

    timers = []
    for i in range(3):
        timers.append(Timer(frames=images[i], wait=300))
    timer_boom = Timer(frames=images_boom, wait=100, looponce=True)

    def __init__(self, game, parent, row, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.parent = parent
        self.number = number
        self.update_requests = 0
        self.dead, self.reallydead, self.timer_switched = False, False, False

        self.timer = Alien.timers[number]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.speed = speed
        self.row = row

    # noinspection PyMethodMayBeStatic
    def alien_score(self, row):
        scores = {0: 90,
                  1: 90,
                  2: 70,
                  3: 70,
                  4: 50,
                  5: 50
                  }
        return scores[row]

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def killed(self):
        if self.dead and not self.timer_switched:
            self.timer = Timer(frames=Alien.images_boom, wait=100, looponce=True)
            self.timer_switched = True
            self.game.stats.score += self.alien_score(self.row)
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()

    def update(self):
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Alien.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.parent.remove(self)
                self.timer.reset()
        delta = self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x += delta
        self.x = self.rect.x

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
