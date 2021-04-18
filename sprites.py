from pygame.sprite import Sprite
from pygame.rect import Rect


class SpriteViewDecorator:
    def __init__(self, sprite):
        self._sprite = sprite
        self._rect = self._sprite.rect

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect):
        self._rect = Rect(rect)

    def update(self, *args, **kwargs):
        self._sprite.update(args, kwargs)


if __name__ == '__main__':
    sp = SpriteViewDecorator(Sprite())
