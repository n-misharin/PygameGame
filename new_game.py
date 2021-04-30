from pygame.sprite import Sprite, Group
from pygame.surface import Surface
from pygame.color import Color
from pygame.rect import Rect
import pygame
import animation_controller


pygame.init()

screen = pygame.display.set_mode((1154, 780))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

running = True

sp = animation_controller.SpriteDecorator(Sprite())
sp.image = Surface((100, 100))
sp.rect = Rect(0, 0, 100, 100)
sp.image.fill(Color('blue'), sp.rect)
sp.image.fill(Color('red'), sp.rect, special_flags=pygame.BLE)
gr = Group()
gr.add(sp)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    gr.update()
    gr.draw(screen)
    pygame.display.flip()

pygame.quit()
