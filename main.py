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

x_difference = 350
clock = pygame.time.Clock()
fps = 60
generation_size = 10

run = True
players = []
for i in generation_size:
    players.append(Player())

pipes = [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]
while True:
    SCREEN.blit(BACKGROUND, [0, 0])
    for pipe in pipes:
        pipe.move()
        pipe.draw(SCREEN)
        if pipe.x <= -20:
            pipes = pipes[1:]
            pipes.append(Pipe(x_difference))

    for player in players:
        player.move(pipes[0])
        player.draw()

    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

pygame.time.delay(1000)
