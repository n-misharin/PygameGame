from models.main import Field, properties, Board
from views.graphics import ImageHandler, Sprite, Rect
from mmm import os, PROJECT_PATH

TILE_SIZE = 94

img_handler = ImageHandler(os.path.join(PROJECT_PATH, "images"))

FIELDS_IMAGES = {
    prop["type"]: img_handler.load_image(prop["sprite"]["name"]).subsurface(
        Rect(prop["sprite"]["pos"], prop["sprite"]["size"])) for prop in properties.FIELDS
}


class GameField(Field):
    def __init__(self, field_type):
        super().__init__(field_type)

        self.sprite = Sprite()
        self.sprite.image = FIELDS_IMAGES[field_type]
        self.sprite.rect = self.sprite.image.get_rect()

    def refresh_image(self):
        pass

    def refresh(self, current_player):
        super().refresh(current_player)


class GameBoard(Board):
    def __init__(self):
        super().__init__()
