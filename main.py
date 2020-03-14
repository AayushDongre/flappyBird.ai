import pygame
from Pipe import Pipe

pygame.init()
dwidth = 640
dheight = 480

STATIC_PATH = 'static'
SCREEN = pygame.display.set_mode((dwidth, dheight))
BACKGROUND = pygame.image.load('static/background.png').convert()
SCREEN.blit(BACKGROUND, [0, 0])
pygame.display.update()

x_difference = 200
clock = pygame.time.Clock()
fps = 60

run = True
pipes = [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]
while True:
    SCREEN.blit(BACKGROUND, [0, 0])
    for pipe in pipes:
        pipe.move()
        pipe.draw(SCREEN)
        if pipe.x <= 0:
            pipes = pipes[1:]
            pipes.append(Pipe(0))

    pygame.display.update()
    clock.tick(fps)


pygame.time.delay(1000)
