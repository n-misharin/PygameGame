import graphics
import pygame
import pygame_gui
from Map import Board, FieldTypes
from GUI import UnitInfoPanel

TILE_SIZE = 50


def board_draw(_board: Board):
    tile_size = TILE_SIZE
    board_sprites = graphics.SpriteGroup()
    for j in range(len(_board._fields)):
        line = _board._fields[j]
        for i in range(len(line)):
            field = line[i]
            field_sprite = pygame.sprite.Sprite()

            file_name = "soil"
            if field.type == FieldTypes.OIL:
                file_name = "oil"
            elif field.type == FieldTypes.DIAMOND:
                file_name = "diamond"
            elif field.type == FieldTypes.GOLD:
                file_name = "gold"
            elif field.type == FieldTypes.WATER:
                file_name = "water"
            elif field.type == FieldTypes.STONE:
                file_name = "stone"
            elif field.type == FieldTypes.TUNNEL:
                file_name = "soil"

            field_sprite.image = graphics.ImageHandler().load_image(file_name + ".png")
            field_sprite.rect = field_sprite.image.get_rect()
            field_sprite.rect.x = tile_size * i
            field_sprite.rect.y = tile_size * j
            board_sprites.add(field_sprite)
    board_sprites.draw_on_screen()


if __name__ == '__main__':
    board = Board.get_random((10, 10))

    clock = pygame.time.Clock()
    running = True

    window_surface = pygame.display.set_mode(graphics.size)
    manager = pygame_gui.UIManager(graphics.size)
    panel = UnitInfoPanel(manager=manager, position=(0, 0))

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
                panel.set_unit_parameters(["1", "2", "3"])

            manager.process_events(event)

        manager.update(delta_time)
        board_draw(board)
        manager.draw_ui(window_surface)
        pygame.display.flip()
    pygame.quit()
