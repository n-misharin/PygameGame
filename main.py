from views import graphics
import pygame
import pygame_gui
from board import Board, FieldTypes
from GUI import UnitInfoPanel
from camera import Camera

camera = Camera()
TILE_SIZE = 94
changed_field = None


def board_draw(game_board: Board, cam: Camera):
    tile_size = TILE_SIZE
    board_sprites = graphics.SpriteGroup()
    for j in range(len(game_board.fields)):
        for i in range(len(game_board.fields[j])):
            field = game_board.fields[j][i]

            field_sprite = pygame.sprite.Sprite()

            file_name = "empty"
            if field.type == FieldTypes.TUNNEL:
                file_name = "tunnel"
            else:
                if i > 0 and game_board.fields[j][i - 1].type == FieldTypes.TUNNEL or \
                        i + 1 < len(game_board.fields[j]) and game_board.fields[j][i + 1].type == FieldTypes.TUNNEL or \
                        j > 0 and game_board.fields[j - 1][i].type == FieldTypes.TUNNEL or \
                        j + 1 < len(game_board.fields) and game_board.fields[j + 1][i].type == FieldTypes.TUNNEL:
                    if field.type == FieldTypes.DIAMOND:
                        file_name = "diamond"
                    elif field.type == FieldTypes.GOLD:
                        file_name = "gold"
                    elif field.type == FieldTypes.WATER:
                        file_name = "magma"
                    elif field.type == FieldTypes.STONE:
                        file_name = "stone"
                    elif field.type == FieldTypes.OIL:
                        file_name = "oil"
                    elif field.type == FieldTypes.SOIL:
                        file_name = "soil"

            field_sprite.image = graphics.ImageHandler().load_image(file_name + ".jpg")
            field_sprite.rect = field_sprite.image.get_rect()
            field_sprite.rect.x = tile_size * i
            field_sprite.rect.y = tile_size * j
            board_sprites.add(field_sprite)
    for sprite in board_sprites:
        cam.apply(sprite)
    board_sprites.draw_on_screen()


if __name__ == '__main__':
    board = Board.get_random((10, 10))

    clock = pygame.time.Clock()
    running = True

    window_surface = pygame.display.set_mode(graphics.size)
    manager = pygame_gui.UIManager(graphics.size)
    panel = UnitInfoPanel(manager=manager, position=(0, 0))

    is_mouse_key_pressed = False
    mouseDownPos = (0, 0)

    while running:
        delta_time = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if event.type == pygame.USEREVENT:
            #     if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            #         if event.ui_element == hello_button:
            #             print('Hello World!')
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_key_pressed = True
                mouseDownPos = event.pos[0] - camera.dx, event.pos[1] - camera.dy

            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_key_pressed = False

            if event.type == pygame.MOUSEMOTION:
                if is_mouse_key_pressed:
                    camera.dx = event.pos[0] - mouseDownPos[0]
                    camera.dy = event.pos[1] - mouseDownPos[1]

            if event.type == pygame.KEYDOWN:
                if pygame.K_a == event.key:
                    camera.move(camera.STEP_SIZE, 0)
                if pygame.K_d == event.key:
                    camera.move(-camera.STEP_SIZE, 0)
                if pygame.K_w == event.key:
                    camera.move(0, camera.STEP_SIZE)
                if pygame.K_s == event.key:
                    camera.move(0, -camera.STEP_SIZE)

            manager.process_events(event)

        graphics.screen.fill((0, 0, 0))
        manager.update(delta_time)
        board_draw(board, camera)
        for j in range(len(board.fields)):
            for i in range(len(board.fields[j])):
                pygame.draw.rect(graphics.screen, (150, 150, 150),
                                 (i * TILE_SIZE + camera.dx, j * TILE_SIZE + camera.dy,
                                  TILE_SIZE, TILE_SIZE), 1)
        manager.draw_ui(window_surface)
        pygame.display.flip()
    pygame.quit()
