import pygame


class SpriteSheet:
    def __init__(self, image_name):
        self.texture = pygame.image.load(image_name)

    def get_sub(self, x, y):
        return pygame.transform.smoothscale(self.texture, )


class