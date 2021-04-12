import pygame
import os

pygame.init()

pygame.display.set_caption("Game")

size = width, height = 1152, 720
screen = pygame.display.set_mode(size)

background = pygame.Surface(size)
background.fill(pygame.Color('#000000'))


class ImageHandler:

    DEFAULT_COLORKEY = -1

    def __init__(self, path="images"):
        self.path = path

    def load_image(self, image_name, colorkey=None):
        fullname = os.path.join(self.path, image_name)
        if not os.path.isfile(fullname):
            raise Exception(f"Файл {fullname} не найден")
            #return None
        else:
            return self.convert_alpha(pygame.image.load(fullname), colorkey)

    def convert_alpha(self, image, colorkey=None):
        if colorkey is not None:
            image = image.convert()
            if colorkey == self.DEFAULT_COLORKEY:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image


class AnimatedSprite(pygame.sprite.Sprite):

    FRAME_DURATION = 1

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cur_frame_time = 0
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame_x = 0
        self.cur_frame_y = 0
        self.image = self.frames[self.cur_frame_y][self.cur_frame_y]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

        for j in range(rows):
            self.frames.append([])
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames[j].append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, delta_time=0.001):
        self.cur_frame_time += delta_time
        if self.cur_frame_time >= self.FRAME_DURATION:
            self.cur_frame_time = 0
            self.cur_frame_x = (self.cur_frame_x + 1) % len(self.frames[self.cur_frame_y])
            self.image = self.frames[self.cur_frame_y][self.cur_frame_x]

    def set_frame_y(self, y):
        self.cur_frame_y = y
        self.cur_frame_x = 0


class SpriteGroup(pygame.sprite.Group):
    def draw_on_screen(self):
        self.draw(screen)
