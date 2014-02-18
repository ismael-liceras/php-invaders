import pygame
from sprite import SpriteManager
from gameconfig import GameConfig

class Option(pygame.sprite.Sprite):
    def __init__(self, index, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.type_id = index
        data = GameConfig.get_menu_items(index)
        (sprite_x, sprite_y) = data[0]
        (width, height) = data[1]

        #Loads sprite
        self.image, self.rect = SpriteManager.load_all(sprite_x, sprite_y, width, height)
        self.rect.topleft = xpos, ypos

    def get_type_id(self):
        return self.type_id