from pygame.sprite import Sprite, Group
from pygame.rect import Rect


class LayerSprite(Sprite):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)


class SelectableSprite(LayerSprite):
    def __init__(self):
        super().__init__()
        self._is_selected = False

    @property
    def select(self):
        return self._is_selected

    @select.setter
    def select(self, value: bool):
        self._is_selected = value

    def update(self, *args, **kwargs):
        if 'selected' in kwargs.keys():
            if self in kwargs['selected']:
                self.select = True
            else:
                self.select = False

        super().update(*args, **kwargs)


class AnimatedSprite(SelectableSprite):



class LayerController:
    def __init__(self):
        self.layers = [Group()]

    def add_sprite(self, sprite: LayerSprite, layer_number: int = 0):
        if layer_number < 0 or len(self.layers) >= layer_number:
            raise Exception('Недопустимый номер слоя')
        self.layers[layer_number].add(sprite)

    def add_layer(self):
        self.layers.append(Group())

    def get_layer_num(self, sprite: LayerSprite):
        for i in range(len(self.layers)):
            if sprite in self.layers[i]:
                return i
        return None

    def update(self, *args, **kwargs):
        for i in range(len(self.layers) - 1, -1, -1):
            self.layers[i].update(*args, **kwargs)


class GameLayerController(LayerController):
    GROUND_LAYER = 0
    GROUND_UNDER_LAYER = 1
    UNIT_UNDER_LAYER = 2
    UNIT_LAYER = 3
    UNIT_ABOVE_LAYER = 4
    GUI_LAYER = 5

    def __init__(self):
        super().__init__()
        for _ in range(6):
            self.add_layer()

    def add(self, sprite: LayerSprite, layer_num: int = GROUND_LAYER):
        self.add_sprite(sprite, layer_num)


