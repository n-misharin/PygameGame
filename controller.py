import pygame
from graphics import is_point_in_rect


class KeyController:
    def __init__(self):
        self.running = True

        self.is_mouse_down = False
        self.is_mouse_motion = False

        self.mouse_down_key = None
        self.mouse_pos = (0, 0)
        self.mouse_delta = (0, 0)
        self.mouse_down_pos = (None, None)

        self.is_key_pressed = False
        self.pressed_key = None

    def update(self, events, gui):
        self.is_mouse_motion = False
        self.mouse_down_pos = (None, None)

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self.is_key_pressed = True
                self.pressed_key = event.key

            if event.type == pygame.KEYUP:
                self.is_key_pressed = False
                self.pressed_key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.is_mouse_down = True
                self.mouse_down_pos = event.pos
                self.mouse_down_key = event.button

            if event.type == pygame.MOUSEBUTTONUP:
                self.is_mouse_down = False

            if event.type == pygame.MOUSEMOTION:
                self.is_mouse_motion = True
                self.mouse_delta = event.pos[0] - self.mouse_pos[0], event.pos[1] - self.mouse_pos[1]
                self.mouse_pos = event.pos

            gui.process_events(event)

    def is_drag(self, obj_view):
        return self.is_mouse_motion and self.is_mouse_down and \
               self.mouse_down_key == pygame.BUTTON_RIGHT and \
               is_point_in_rect(obj_view.rect, self.mouse_pos)

    def is_key_down(self, key):
        return self.is_key_pressed and key == self.pressed_key

    def is_click_on(self, obj_view):
        return self.is_mouse_down and is_point_in_rect(obj_view.rect, self.mouse_down_pos) and \
               self.mouse_down_key == pygame.BUTTON_LEFT
