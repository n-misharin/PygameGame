import pygame
import random
from Map import Field, Board, FieldTypes, get_field_types, FieldsProperties


if __name__ == '__main__':
    t = set(get_field_types()) - {FieldTypes.TUNNEL}
    print(list(t))
    # pygame.init()
    # size = width, height = 800, 400
    # screen = pygame.display.set_mode(size)
    #
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     pygame.display.flip()
    # pygame.quit()
