import properties
from graphics import ImageHandler, window, is_point_in_rect
from os import path
import pygame
from pygame.sprite import Sprite
from pygame import Rect

TILE_SIZE = 94

img_folder = path.join("", "images") if __name__ == "__main__" else "images"
img_handler = ImageHandler(img_folder)

FIELDS_IMAGES = dict()
UNITS_IMAGES = dict()

for prop in properties.FIELDS:
    img = img_handler.load_image(prop["sprite"]["name"])
    pos = prop["sprite"]["pos"]
    size = prop["sprite"]["size"]
    coord = (pos[0] * size[0], pos[1] * size[1])
    crop_img = img.subsurface(Rect(coord, size))
    FIELDS_IMAGES[prop["type"]] = crop_img

for prop in properties.UNITS:
    img = img_handler.load_image(prop["sprite"]["name"])
    pos = prop["sprite"]["pos"]
    size = prop["sprite"]["size"]
    coord = (pos[0] * size[0], pos[1] * size[1])
    crop_img = img.subsurface(Rect(coord, size))
    UNITS_IMAGES[prop["type"]] = crop_img


class Camera:
    def __init__(self):
        self.pos = 0, 0
        self.delta = 0, 0

    def apply(self, obj):
        obj.rect.x += self.delta[0]
        obj.rect.y += self.delta[1]

    def move(self, mouse_pos):
        self.delta = mouse_pos[0], mouse_pos[1]
        self.pos = self.pos[0] + self.delta[0], self.pos[1] + self.delta[1]


class SpriteView(Sprite):
    def __init__(self):
        super().__init__()

    def __contains__(self, point: tuple):
        return is_point_in_rect(self.rect, point)


class UnitView(SpriteView):
    def __init__(self, unit):
        super().__init__()

        self.unit = unit
        self.image = UNITS_IMAGES[self.unit.type]
        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs):
        pass


class FieldView(SpriteView):
    def __init__(self, field):
        super().__init__()

        self.field = field
        self.image = FIELDS_IMAGES[self.field.type]
        self.rect = self.image.get_rect()

        self.sprite_group = pygame.sprite.Group()

        for x in range(len(self.field.units)):
            unit = self.field.units[x]
            unit.view.rect = Rect(300, 100, 20, 20)
            self.sprite_group.add(unit.view)

    def update(self, delta_time, camera: Camera):
        self.image = FIELDS_IMAGES[self.field.type]
        camera.apply(self)


class BoardView(SpriteView):
    LINES_COLOR = (150, 150, 150)
    BORDER_COLOR = (255, 0, 0)

    def __init__(self, game_board):
        super().__init__()

        self.board = game_board
        self.sprite_group = pygame.sprite.Group()
        self.rect = Rect(0, 0, self.board.size[0] * TILE_SIZE, self.board.size[1] * TILE_SIZE)
        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                row = x * TILE_SIZE
                col = y * TILE_SIZE
                self.board.fields[y][x].view.rect = Rect(row, col, TILE_SIZE, TILE_SIZE)
                self.sprite_group.add(self.board.fields[y][x].view)
                for unit in self.board.fields[y][x].units:
                    unit.view.rect = Rect(self.board.fields[y][x].view.rect.x + 20, self.board.fields[y][x].view.rect.y + 20, 20, 20)
                    self.sprite_group.add(unit.view)

    def update(self, delta_time, camera: Camera):
        self.sprite_group.update(delta_time, camera)
        camera.apply(self)

    def draw(self):
        self.sprite_group.draw(window.screen)
        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                #self.board.fields[x][y].view.sprite_group.draw(window.screen)
                pygame.draw.rect(window.screen, self.LINES_COLOR, self.board.fields[x][y].view.rect, 1)
        pygame.draw.rect(window.screen, self.BORDER_COLOR, self.rect, 1)
