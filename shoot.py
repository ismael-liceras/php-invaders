import pygame
from sprite import SpriteManager
from gameconfig import GameConfig


class Shoot(pygame.sprite.Sprite):
    def __init__(self, shoot_xcoord, shoottype):
        pygame.sprite.Sprite.__init__(self)

        data = GameConfig.get_others(shoottype)
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]
        self.image, self.rect = SpriteManager.load_all(sprite_x, sprite_y, width, height)

        if shoottype == 'shoot':
            # Ojos, disparo normal, velocidad normal
            self.rect.topleft = (shoot_xcoord + 30), 530
            self.move = -10
        elif shoottype == 'super_shoot':
            self.rect.topleft = (shoot_xcoord + 10), 530
            self.move = -15

    def update(self):
        self._move()

    def _move(self):
        new_pos = self.rect.move((0, self.move))
        self.rect = new_pos
        if self.rect.top < 0:
            self.kill()
