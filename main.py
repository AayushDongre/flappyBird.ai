import pygame
from Pipe import Pipe
from Player import Player

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
player = Player()
pipes = [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]
while True:
    SCREEN.blit(BACKGROUND, [0, 0])
    player.draw(SCREEN)
    for pipe in pipes:
        pipe.move()
        pipe.draw(SCREEN)
        if pipe.x <= -20:
            pipes = pipes[1:]
            pipes.append(Pipe(0))

    pygame.display.update()
    clock.tick(fps)


pygame.time.delay(1000)
