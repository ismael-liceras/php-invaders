import pygame
from shoot import Shoot
from sprite import SpriteManager
from gameconfig import GameConfig


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.shoot_type = None
        self.alive = None
        self.move = None
        self.time_to_back2normal = None
        self.time_to_back2shootnormal = None
        self.time_to_back2noinvincible = None
        self.waiting_sprites = []

        self.reset()
        self.rect = self.image.get_rect()

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 432, 510

    def reset(self):
        self.set_sprite("normal")
        self.set_shoot_type('shoot')
        self.alive = True
        self.time_to_back2normal = -1
        self.time_to_back2shootnormal = -1
        self.time_to_back2noinvincible = -1
        self.move = 0

    def set_shoot_type(self, shoottype, time=None):
        if time is not None:
            self.time_to_back2shootnormal = time
        self.shoot_type = shoottype

    def update(self):
        self._fly()

        # sprite managment
        if len(self.waiting_sprites) > 0 and self.time_to_back2normal == -1:
            sprite = self.waiting_sprites.pop(0)
            self.set_sprite(sprite[0], sprite[1])
        if self.time_to_back2normal > -1:
            self.time_to_back2normal -= 1
        if self.time_to_back2normal == 0:
            self.set_sprite("normal")
            self.time_to_back2normal = -1

        # special_shoot
        if self.time_to_back2shootnormal > -1:
            self.time_to_back2shootnormal -= 1
        if self.time_to_back2shootnormal == 0:
            self.set_shoot_type('shoot')
            self.set_sprite("normal")
            self.time_to_back2shootnormal = -1

        # invincible
        if self.time_to_back2noinvincible > -1:
            self.time_to_back2noinvincible -= 1
        if self.time_to_back2noinvincible == 0:
            self.set_sprite("normal")
            self.time_to_back2noinvincible = -1

    def get_shooter_coordinates(self):
        return self.rect.topleft

    def go_left(self):
        if self.alive:
            self.move = -9

    def go_right(self):
        if self.alive:
            self.move = 9

    def stop_flying(self):
        self.move = 0

    def _fly(self):
        new_pos = self.rect.move((self.move, 0))
        if new_pos.left < self.area.left or \
           new_pos.right > self.area.right:
            self.move = 0
        else:
            self.rect = new_pos

    def do_shoot(self):
        shoot = Shoot(self.rect.topleft[0], self.shoot_type)
        return shoot

    def get_direction(self):
        if self.move < 0:
            ret_val = 'left'
        elif self.move > 0:
            ret_val = 'right'
        else:
            ret_val = ''
        return ret_val

    def kill_player(self):
        self.alive = False
        self.stop_flying()
        self.set_sprite('crying')

    def shocked(self):
        self.set_sprite("shocked", 15)

    def set_sprite(self, typesprite, time=None):
        if time is not None:
            self.time_to_back2normal = time
        data = GameConfig.get_player(typesprite)
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]

        #Loads sprite
        self.image = SpriteManager.load(sprite_x, sprite_y, width, height)

    def make_happy(self, time=None):
        self.waiting_sprites.append(("money", time))

    def make_angry(self, time=None):
        self.waiting_sprites.append(("anger", time))

    def get_super_shoot(self):
        self.set_shoot_type('super_shoot', 200)
        self.make_angry()

    def make_winner(self):
        self.alive = False
        self.stop_flying()
        self.set_sprite('victory')

    def make_invincible(self):
        self.time_to_back2noinvincible = 200
        self.make_angry()

    def is_invincible(self):
        return self.time_to_back2noinvincible > -1