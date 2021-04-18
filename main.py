import pygame
from graphics import window, ImageHandler
from model import Board, Unit, Player, Game
from views import FieldView, BoardView, Camera
from controller import KeyController
import pygame_gui
from GUI import GameGUI


if __name__ == '__main__':

    clock = pygame.time.Clock()
    running = True

    game = Game(4, (10, 10))

    camera = Camera()

    key_controller = KeyController()
    # game.board.get_field((0, 5)).units[0].view.move_towards((94 + 20, 5 * 94 - 30))

    panel = GameGUI(position=(window.width - 250, 0), player=game.players[3])

    while key_controller.running:
        delta_time = clock.tick(60) / 1000
        key_controller.update(pygame.event.get(), panel)

        if key_controller.is_drag(game.board.view):
            camera.move(key_controller.mouse_delta)
        else:
            camera.move((0, 0))

        window.screen.fill((0, 0, 0))

        if key_controller.is_mouse_down and \
                key_controller.mouse_down_key == pygame.BUTTON_LEFT and \
                key_controller.mouse_down_pos != (None, None):
            panel.field_panel.set_field(game.board.view.get_field(key_controller.mouse_down_pos))
            #panel.field_panel.labels["name"].

        panel.update(delta_time)

        game.view.update(delta_time, camera, key_controller)
        game.view.draw()

        panel.draw_ui()

        pygame.display.flip()
    pygame.quit()
