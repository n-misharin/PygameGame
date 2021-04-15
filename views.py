import properties
from graphics import ImageHandler, window, is_point_in_rect
from os import path
import pygame
from pygame.sprite import Sprite
from pygame import Rect

MAX_PLAYER_COUNT = 4
GROUND_TILE_SIZE = 94
UNIT_TILE_SIZE = 64

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
    imgs = prop["sprite"]["name"]
    img = None
    UNITS_IMAGES[prop["type"]] = []
    for i in range(MAX_PLAYER_COUNT):
        img = img_handler.load_image(imgs[i])
        pos = prop["sprite"]["pos"]
        size = prop["sprite"]["size"]
        coord = (pos[0] * size[0], pos[1] * size[1])
        crop_img = img.subsurface(Rect(coord, size))
        UNITS_IMAGES[prop["type"]].append(crop_img)


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


class AnimatedSpriteView(SpriteView):

    FRAME_DURATION = 0.1

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cur_frame_time = 0
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame_x = 0
        self.cur_frame_y = 0
        self.image = self.frames[self.cur_frame_y][self.cur_frame_y]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[j].append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, delta_time, camera, mouse_down_pos):
        self.cur_frame_time += delta_time
        if self.cur_frame_time >= self.FRAME_DURATION:
            self.cur_frame_time = 0
            self.cur_frame_x = (self.cur_frame_x + 1) % len(self.frames[self.cur_frame_y])
            self.image = self.frames[self.cur_frame_y][self.cur_frame_x]

    def set_frame_y(self, y):
        self.cur_frame_y = y
        self.cur_frame_x = 0


class UnitView(AnimatedSpriteView):
    def __init__(self, unit):
        super().__init__(
            UNITS_IMAGES[unit.type][unit.player.turn],
            properties.UNITS[unit.type]["sprite"]["column"],
            properties.UNITS[unit.type]["sprite"]["row"], 0, 0
        )

        self.unit = unit
        self.image = UNITS_IMAGES[self.unit.type][unit.player.turn]
        self.rect = self.image.get_rect()

    def update(self, delta_time, camera, mouse_down_pos):
        super().update(delta_time, camera, mouse_down_pos)
        camera.apply(self)


class FieldView(SpriteView):
    def __init__(self, field):
        super().__init__()

        self.field = field
        self.image = FIELDS_IMAGES[self.field.type]
        self.rect = self.image.get_rect()

        self.sprite_group = pygame.sprite.Group()
        self.refresh_unit_rect()

    def refresh_unit_rect(self):
        space_y = 30
        space_x = 20

        for x in range(len(self.field.units)):
            unit = self.field.units[x]
            unit.view.rect = Rect(
                self.field.view.rect.x + space_x,
                self.field.view.rect.y + (x - 1) * space_y,
                UNIT_TILE_SIZE, UNIT_TILE_SIZE)
            self.sprite_group.add(unit.view)

    def update(self, delta_time, camera: Camera, mouse_down_pos):
        self.image = FIELDS_IMAGES[self.field.type]
        camera.apply(self)


class BoardView(SpriteView):
    LINES_COLOR = (150, 150, 150)
    BORDER_COLOR = (255, 0, 0)
    SELECT_COLOR = (255, 255, 0)

    def __init__(self, game_board):
        super().__init__()

        self.board = game_board
        self.sprite_group = pygame.sprite.Group()
        self.rect = Rect(0, 0, self.board.size[0] * GROUND_TILE_SIZE, self.board.size[1] * GROUND_TILE_SIZE)
        self.selected_field = None

        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                row = x * GROUND_TILE_SIZE
                col = y * GROUND_TILE_SIZE
                self.board.fields[y][x].view.rect = Rect(row, col, GROUND_TILE_SIZE, GROUND_TILE_SIZE)
                self.sprite_group.add(self.board.fields[y][x].view)

        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                for unit in self.board.fields[y][x].units:
                    self.board.fields[y][x].view.refresh_unit_rect()
                    self.sprite_group.add(unit.view)

    def update(self, delta_time, camera: Camera, mouse_down_pos, mouse_key):
        self.sprite_group.update(delta_time, camera, mouse_down_pos)
        camera.apply(self)

        if mouse_key == pygame.BUTTON_LEFT and mouse_down_pos != (None, None) and\
                is_point_in_rect(self.rect, mouse_down_pos):
            prev_selected_field = self.selected_field

            for y in range(len(self.board.fields)):
                for x in range(len(self.board.fields[y])):
                    if is_point_in_rect(self.board.fields[y][x].view.rect, mouse_down_pos):
                        self.selected_field = self.board.fields[y][x]
            if self.selected_field == prev_selected_field:
                self.selected_field = None

    def draw(self):
        self.sprite_group.draw(window.screen)
        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                pygame.draw.rect(window.screen, self.LINES_COLOR, self.board.fields[y][x].view.rect, 1)
        if self.selected_field is not None:
            pygame.draw.rect(window.screen, self.SELECT_COLOR, self.selected_field.view.rect, 2)
        pygame.draw.rect(window.screen, self.BORDER_COLOR, self.rect, 1)
