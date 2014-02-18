import pygame
from enemyshoot import EnemyShoot
from specialitem import SpecialItem
from random import randint
from sprite import SpriteManager
from gameconfig import GameConfig


class Enemy(pygame.sprite.Sprite):
    def __init__(self, etype, drop_item, start_position, enemy_shoots):
        self.enemy_shoots = enemy_shoots
        self.drop_item = drop_item
        self.time_to_death = -1
        pygame.sprite.Sprite.__init__(self)

        self.image = self.get_image(etype)
        self.rect = self.image.get_rect()

        self.data = GameConfig.get_enemy_type(etype)

        self.rect.topleft = start_position
        self.enemy_box = None
        self.time_to_shoot = None
        self.reset_time_to_shoot()

    def reset_time_to_shoot(self):
        self.time_to_shoot = self.data['shoot_timer']
        self.time_to_shoot += randint(1, 60)

    def update(self):
        if self.time_to_death == -1:
            self._move()

        #TODO Hacer que el fuego se apague lentamente
        # Dying enemy
        if self.time_to_death > -1:
            self.time_to_death -= 1
        if self.time_to_death == 0:
            self.kill()

        # Shooting enemy
        if self.time_to_shoot > -1:
            self.time_to_shoot -= 1
        if self.time_to_shoot == 0:
            self.do_shoot()
            self.reset_time_to_shoot()

    def _move(self):
        pos = self.rect.move((self.enemy_box.get_move(), 0))
        self.rect = pos

    def get_score(self):
        return self.data['score']

    def get_rect(self):
        return self.rect

    def set_enemy_box(self, enemy_box):
        self.enemy_box = enemy_box

    def kill_enemy(self):
        self.time_to_shoot = -1
        self.time_to_death = 25

        data = GameConfig.get_others('fire')
        (sprite_x, sprite_y) = data[0]
        (width, heigth) = data[1]
        self.image = SpriteManager.load(sprite_x, sprite_y, width, heigth)

    def do_shoot(self):
        shoot = EnemyShoot(self.rect.topleft)
        shoot.add(self.enemy_shoots)
        return shoot

    def drop_special_item(self):
        specialitem = None
        if self.drop_item > 0:
            specialitem = SpecialItem(self.rect.topleft, self.drop_item)
        return specialitem

    @staticmethod
    def get_image(etype):
        data = GameConfig.get_enemy_type(etype)
        (sprite_x, sprite_y) = data['image'][0]
        (width, height) = data['image'][1]
        return SpriteManager.load(sprite_x, sprite_y, width, height)