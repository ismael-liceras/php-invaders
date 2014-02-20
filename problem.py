import pygame
from PIL import Image

sprites = Image.open('sprites.data')
pygameImage = pygame.image.fromstring(sprites.tostring(), (760, 166), 'RGB', False)

background = pygame.Surface((800, 600))
rect = pygame.Rect((0, 0, 150, 200))
background.blit(pygameImage, (0, 0), rect)