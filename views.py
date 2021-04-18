import properties
from graphics import ImageHandler, window, is_point_in_rect
from os import path
import pygame
from pygame.sprite import Sprite
from pygame import Rect
from controller import KeyController

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

    def get_apply_point(self, point: tuple):
        return point[0] + self.delta[0], point[1] + self.delta[1]

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

    def __init__(self, sheet, columns, rows):
        super().__init__()
        self.animation_delta = 1
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

    def update(self, delta_time, camera, key_controller):
        self.cur_frame_time += delta_time
        if self.cur_frame_time >= self.FRAME_DURATION:
            self.cur_frame_time = 0
            self.cur_frame_x = (self.cur_frame_x + self.animation_delta) % len(self.frames[self.cur_frame_y])
            self.image = self.frames[self.cur_frame_y][self.cur_frame_x]

    def set_frame_y(self, y):
        self.cur_frame_y = y
        self.cur_frame_x = 0


class UnitView(AnimatedSpriteView):
    PIXELS_PER_SECOND = 60
    DELTA_X = 20

    def __init__(self, unit):
        super().__init__(
            UNITS_IMAGES[unit.type][unit.player.turn],
            properties.UNITS[unit.type]["sprite"]["column"],
            properties.UNITS[unit.type]["sprite"]["row"]
        )
        self.unit = unit
        self.frames.append([self.frames[1].pop(), self.frames[1].pop()])
        self.frames.append([pygame.transform.flip(frame, True, False) for frame in self.frames[1]])
        self.do_animation_stay()
        self.target_position = None
        self.delta_move = [0, 0]

    def move_towards(self, target_position):
        self.target_position = target_position

    def do_animation_move(self, is_right=True):
        self.animation_delta = -1
        if is_right:
            self.cur_frame_y = 3
        else:
            self.cur_frame_y = 1

    def do_animation_stay(self):
        self.cur_frame_y = 2
        self.animation_delta = 1

    def do_animation_work(self):
        self.cur_frame_y = 0
        self.animation_delta = 1

    def update_move(self, delta_time, camera):
        if self.target_position is not None:
            self.target_position = camera.get_apply_point(self.target_position)
            if abs((self.target_position[0] - self.rect.x) ** 2 - (self.target_position[1] - self.rect.y) ** 2) > 1:

                dif_x = self.target_position[0] - self.rect.x
                dif_y = self.target_position[1] - self.rect.y

                dist_x = self.PIXELS_PER_SECOND * delta_time * (1 if dif_x > 0 else -1 if dif_x < 0 else 0)
                dist_y = self.PIXELS_PER_SECOND * delta_time * (1 if dif_y > 0 else -1 if dif_y < 0 else 0)

                self.delta_move = [self.delta_move[0] + dist_x, self.delta_move[1] + dist_y]

                new_x = self.rect.x
                new_y = self.rect.y

                if self.delta_move[0] >= 1:
                    new_x += self.delta_move[0]
                    self.delta_move[0] -= 1
                elif self.delta_move[0] <= -1:
                    new_x -= self.delta_move[0]
                    self.delta_move[0] += 1

                if self.delta_move[1] >= 1:
                    new_y += self.delta_move[1]
                    self.delta_move[1] -= 1
                elif self.delta_move[1] <= -1:
                    new_y -= self.delta_move[1]
                    self.delta_move[1] += 1

                if self.delta_move[0] > 0:
                    self.do_animation_move(is_right=True)
                else:
                    self.do_animation_move(is_right=False)

                self.rect = Rect(new_x, new_y, self.rect.width, self.rect.height)
            else:
                self.target_position = None
                self.do_animation_stay()

    def update(self, delta_time, camera, key_controller):
        super().update(delta_time, camera, key_controller)
        camera.apply(self)
        self.update_move(delta_time, camera)


class FieldView(SpriteView):
    def __init__(self, field):
        super().__init__()

        self.field = field
        self.image = FIELDS_IMAGES[self.field.type]
        self.rect = self.image.get_rect()

    def update(self, delta_time, camera: Camera, key_controller: KeyController):
        camera.apply(self)


class BoardView:
    LINES_COLOR = (150, 150, 150)
    BORDER_COLOR = (255, 0, 0)

    DY = 30
    DX = 20

    def __init__(self, game_board):
        super().__init__()

        self.board = game_board

        self.fields_sprite_group = pygame.sprite.Group()
        self.units_sprite_group = pygame.sprite.Group()

        self.rect = Rect(0, 0, self.board.size[0] * GROUND_TILE_SIZE, self.board.size[1] * GROUND_TILE_SIZE)

        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                row = x * GROUND_TILE_SIZE
                col = y * GROUND_TILE_SIZE
                self.board.fields[y][x].view.rect = Rect(row, col, GROUND_TILE_SIZE, GROUND_TILE_SIZE)
                self.fields_sprite_group.add(self.board.fields[y][x].view)

    def get_field(self, pos):
        if not is_point_in_rect(self.rect, pos):
            return None
        return self.board.fields[(pos[1] - self.rect.y) // GROUND_TILE_SIZE][(pos[0] - self.rect.x) // GROUND_TILE_SIZE]

    def update(self, delta_time, camera: Camera, key_controller):
        self.fields_sprite_group.update(delta_time, camera, key_controller)
        self.units_sprite_group.update(delta_time, camera, key_controller)
        camera.apply(self)

    def draw(self):
        self.fields_sprite_group.draw(window.screen)
        for y in range(len(self.board.fields)):
            for x in range(len(self.board.fields[y])):
                pygame.draw.rect(window.screen, self.LINES_COLOR, self.board.fields[y][x].view.rect, 1)
        pygame.draw.rect(window.screen, self.BORDER_COLOR, self.rect, 1)
        self.units_sprite_group.draw(window.screen)

    def add_unit_view(self, unit_view, field):
        unit_view.rect = Rect(field.view.rect.x + self.DX, field.view.rect.y + self.DY * (len(field.units) - 2),
                              UNIT_TILE_SIZE, UNIT_TILE_SIZE)
        self.units_sprite_group.add(unit_view)


class PlayerView:
    def __init__(self, player):
        self.player = player
        self.color = (0, 0, 0)
        if player.turn == 0:
            self.color = (180, 0, 0)
        elif player.turn == 1:
            self.color = (0, 0, 220)
        elif player.turn == 2:
            self.color = (0, 130, 0)
        else:
            self.color = (200, 200, 200)
        self.rect = Rect(0, 0, window.width, 100)

    def draw(self):
        pass


class GameView:
    SELECT_FIELD_COLOR = (255, 255, 0)
    SELECT_UNIT_COLOR = (0, 255, 0)

    def __init__(self, game):
        self.game = game
        self.selected_field = None
        self.selected_unit = None

    def update(self, delta_time, camera: Camera, key_controller: KeyController):
        self.game.board.view.update(delta_time, camera, key_controller)

    def draw(self):
        self.game.board.view.draw()
        for player in self.game.players:
            player.view.draw()
        if self.selected_unit is not None:
            pygame.draw.rect(window.screen, self.SELECT_UNIT_COLOR, self.selected_unit.view.rect, 1)
        if self.selected_field is not None:
            pygame.draw.rect(window.screen, self.SELECT_UNIT_COLOR, self.selected_field.view.rect, 1)
