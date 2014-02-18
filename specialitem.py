import pygame
from gameconfig import GameConfig
from sprite import SpriteManager


class SpecialItem(pygame.sprite.Sprite):
    def __init__(self, coord, typecode):
        self.type = typecode
        shoot_xcoord = coord[0]
        shoot_ycoord = coord[1]
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_image(typecode)
        self.rect = self.image.get_rect()

        self.rect.topleft = (shoot_xcoord + 30), shoot_ycoord + 30
        self.move = 4

    def update(self):
        self._move()

    def _move(self):
        new_pos = self.rect.move((0, self.move))
        self.rect = new_pos
        if self.rect.top > 600:
            self.kill()

    def do_action(self, ge):
        if self.type == "extra_life":
            ge.player.make_happy(15)
            ge.game_status.set_lives(ge.game_status.get_lives() + 1)
        elif self.type == "super_shoot":
            ge.player.make_happy(15)
            ge.player.get_super_shoot()
        elif self.type == "invincible":
            ge.player.make_happy(15)
            ge.player.make_invincible()

    @staticmethod
    def get_image(itemtype):
        data = GameConfig.get_special_items(itemtype)
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]
        return SpriteManager.load(sprite_x, sprite_y, width, height)