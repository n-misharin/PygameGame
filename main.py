import pygame
from graphics import window, ImageHandler
from model import Board, Unit, Player
from views import FieldView, BoardView, Camera


if __name__ == '__main__':

    clock = pygame.time.Clock()
    running = True

    b = Board.get_random((10, 10))

    print(-10 % 3)

    pl1 = Player("Nik1", 0, b, (0, 4))
    pl2 = Player("Nik2", 1, b, (4, 9))
    pl3 = Player("Nik3", 2, b, (9, 5))
    pl4 = Player("Nik4", 3, b, (5, 0))

    u = Unit(0, player=pl1)
    b.add_unit(u, (0, 0))
    b.add_unit(Unit(0, player=pl1), (0, 0))
    b.add_unit(Unit(0, player=pl1), (0, 0))
    b.add_unit(Unit(0, player=pl4), (1, 0))
    b.add_unit(Unit(0, player=pl4), (0, 2))
    b.add_unit(Unit(0, player=pl2), (3, 7))
    b.add_unit(Unit(0, player=pl2), (3, 7))
    b.add_unit(Unit(0, player=pl3), (9, 9))
    b.add_unit(Unit(0, player=pl1), (9, 9))
    b.add_unit(Unit(0, player=pl4), (9, 9))
    b.add_unit(Unit(0, player=pl1), (7, 2))
    b.add_unit(Unit(0, player=pl3), (4, 5))
    b.add_unit(Unit(0, player=pl3), (4, 5))

    board = BoardView(b)
    camera = Camera()

    is_mouse_down = False
    mouse_down_key = None
    mouse_pos = (0, 0)
    mouse_delta = (0, 0)

    is_move = False

    while running:
        is_mouse_motion = False
        delta_time = clock.tick(60) / 1000
        mouse_down_pos = (None, None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    is_move = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    is_move = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_down = True
                mouse_down_pos = event.pos
                mouse_down_key = event.button

            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_down = False

            if event.type == pygame.MOUSEMOTION:
                is_mouse_motion = True
                mouse_delta = event.pos[0] - mouse_pos[0], event.pos[1] - mouse_pos[1]
                mouse_pos = event.pos

        if is_mouse_motion and is_mouse_down and mouse_down_key == pygame.BUTTON_RIGHT:
            if mouse_pos in board:
                camera.move(mouse_delta)
        else:
            camera.move((0, 0))

        if is_move and is_mouse_down and mouse_down_key == pygame.BUTTON_LEFT and mouse_down_pos != (None, None):
            board.board.move_unit(u, board.get_field(mouse_down_pos))
        board.update(delta_time, camera, mouse_down_pos, mouse_down_key)

        window.screen.fill((0, 0, 0))
        board.draw()

        pygame.display.flip()
    pygame.quit()
