import pygame
from graphics import window
from model import Board, Unit
from views import FieldView, BoardView, Camera

TILE_SIZE = 94

if __name__ == '__main__':

    clock = pygame.time.Clock()
    running = True

    b = Board.get_random((10, 10))
    b.add_unit(Unit(0, (0, 0)), (0, 0))
    board = BoardView(b)
    camera = Camera()

    print(board.board.get_field((0, 0)).units[0].view.rect)

    is_mouse_down = False
    mouse_pos = (0, 0)
    mouse_delta = (0, 0)

    while running:
        is_mouse_motion = False
        delta_time = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_down = False

            if event.type == pygame.MOUSEMOTION:
                is_mouse_motion = True
                mouse_delta = event.pos[0] - mouse_pos[0], event.pos[1] - mouse_pos[1]
                mouse_pos = event.pos

        if is_mouse_motion and is_mouse_down:
            if mouse_pos in board:
                camera.move(mouse_delta)
        else:
            camera.move((0, 0))

        board.update(delta_time, camera)

        window.screen.fill((0, 0, 0))
        board.draw()

        pygame.display.flip()
    pygame.quit()
