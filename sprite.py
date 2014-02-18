import pygame


class SpriteManager():

    @staticmethod
    def load(sprite_x, sprite_y, width, height):
        sprites = pygame.image.load("sprites.data")
        rect = pygame.Rect((sprite_x, sprite_y, width, height))
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(sprites, (0, 0), rect)
        return image

    @staticmethod
    def load_all(sprite_x, sprite_y, width, height):
        image = SpriteManager.load(sprite_x, sprite_y, width, height)
        rect = image.get_rect()
        return image, rect