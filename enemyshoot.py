import pygame
from gameconfig import GameConfig
from sprite import SpriteManager


class EnemyShoot(pygame.sprite.Sprite):
    def __init__(self, coord):
        shoot_xcoord = coord[0]
        shoot_ycoord = coord[1]
        pygame.sprite.Sprite.__init__(self)

        data = GameConfig.get_others('enemy_shoot')
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]
        self.image, self.rect = SpriteManager.load_all(sprite_x, sprite_y, width, height)

        self.rect.topleft = (shoot_xcoord + 30), shoot_ycoord + 30
        self.move = 10

    def update(self):
        self._move()

    def _move(self):
        new_pos = self.rect.move((0, self.move))
        self.rect = new_pos
        if self.rect.top > 600:
            self.kill()
