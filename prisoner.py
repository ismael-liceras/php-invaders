import pygame
from random import randint
from gameconfig import GameConfig
from sprite import SpriteManager


class Prisoner(pygame.sprite.Sprite):
    def __init__(self, start_position):
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_image()
        self.rect = self.image.get_rect()

        self.rect.topleft = start_position
        self.move = 1
        if randint(0, 100) < 50:
            self.move = -self.move
        self.ini_walked = self.walked = 30

    def update(self):
        self.rect.move_ip((self.move, 0))
        self.walked -= 1
        if self.walked == 0:
            self.walked = self.ini_walked
            self.move = -self.move

    @staticmethod
    def get_image():
        data = GameConfig.get_others('prisoner')
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]
        return SpriteManager.load(sprite_x, sprite_y, width, height)