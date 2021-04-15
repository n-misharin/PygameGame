import pygame
import os


SCREEN_SIZE = (1152, 720)
IMAGE_FOLDER_PATH = "images"


def is_point_in_rect(rect: pygame.Rect, point: tuple):
    #print("rect", rect.left, rect.right, rect.bottom, rect.top)
    return rect.x < point[0] < rect.x + rect.width and rect.y < point[1] < rect.y + rect.height


def is_rect_in_rect(rect1: pygame.Rect, rect2: pygame.Rect):
    return is_point_in_rect(rect1, rect2.topleft) and is_point_in_rect(rect1, rect2.bottomright)


class Screen:
    CAPTION = "Diggers"
    BG_COLOR = (0, 0, 0)

    def __init__(self, screen_size):
        pygame.init()

        pygame.display.set_caption(self.CAPTION)

        self.size = self.width, self.height = screen_size
        self.screen = pygame.display.set_mode(self.size)

        background = pygame.Surface(self.size)
        background.fill(pygame.Color(self.BG_COLOR))


window = Screen(SCREEN_SIZE)


class ImageHandler:

    DEFAULT_COLORKEY = -1

    def __init__(self, path=IMAGE_FOLDER_PATH):
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


class SpriteGroup(pygame.sprite.Group):
    def draw_on_screen(self):
        self.draw(window.screen)


if __name__ == '__main__':
    pass
