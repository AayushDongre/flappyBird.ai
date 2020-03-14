import pygame
from Pipe import Pipe

pygame.init()

STATIC_PATH = 'static'
SCREEN = pygame.display.set_mode((640, 480))

BACKGROUND = pygame.image.load('static/background.png')

SCREEN.blit(BACKGROUND, [0, 0])

print(SCREEN)
print(BACKGROUND)

pygame.display.update()
pipe = Pipe()
pipe.draw(SCREEN)

pygame.display.update()


pygame.time.delay(5000)
