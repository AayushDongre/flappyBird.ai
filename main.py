import pygame
from Pipe import Pipe
from Player import Player
import numpy as np
import random

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
pipes = [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]

run = True
generation_number = 1
generation = []
dead = []
new_gen_weights = []
best_player = Player()



for i in range(generation_size):
    generation.append(Player())

def crossover():
    dead.sort(key=lambda x: x.fitness, reverse=True)
 
    parent1 = dead[0] if dead[0].fitness > best_player.fitness else best_player
    parent2 = dead[1] if dead[1].fitness > best_player.fitness else best_player

    new_weight1 = parent1.model.get_weights()
    new_weight2 = parent2.model.get_weights()
    gene = random.randint(0, len(new_weight1) -1 )
    new_weight1[gene] = parent2.model.get_weights()[gene]
    new_weight2[gene] = parent1.model.get_weights()[gene]

    return np.asarray([new_weight1, new_weight2])

def mutate(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.uniform(0, 1) > 0.85:
                noise = random.uniform(-0.5, 0.5)
                weights[i][j] += noise
    return weights

def reset():
    pipes.clear()
    [pipes.append(i) for i in [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]]

while True:
    SCREEN.blit(BACKGROUND, [0, 0])
    for pipe in pipes:
        pipe.move()
        pipe.draw(SCREEN)
        if pipe.x <= -20:
            pipes = pipes[1:]
            pipes.append(Pipe(x_difference))

    nextpipe = pipes[0]

    for player in generation:
        player.move(nextpipe)
        player.draw(SCREEN)

        if player.y > dheight:
            dead.append(player)
            generation.remove(player)

        if player.y > nextpipe.bottom_y and player.x > nextpipe.x and player.x < nextpipe.x + nextpipe.width:
            player.fitness += (1 - abs(nextpipe.centery - player.y)/nextpipe.centery)
            dead.append(player)
            generation.remove(player)

        if player.y < nextpipe.top_y and player.x > nextpipe.x and player.x < nextpipe.x + nextpipe.width:
            player.fitness += (1 - abs(nextpipe.centery - player.y)/nextpipe.centery)
            dead.append(player)
            generation.remove(player)
    
        if player.x > nextpipe.x + nextpipe.width:
            player.fitness += 1

    if len(generation) == 0:
        new_gen_weights.clear()
        for i in range(generation_size//2):
            new_weights = crossover()
            new_gen_weights.append(mutate(new_weights[0]))
            new_gen_weights.append(mutate(new_weights[1]))

        for i in new_gen_weights:
            generation.append(Player(inital_weights=i))
            
        generation_number += 1
        reset()
        print(f'Generation number:{generation_number}, highest={dead[0].fitness}')

        if dead[0].fitness > best_player.fitness:
            best_player = dead[0]

        dead.clear()
        new_gen_weights.clear()
    


    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                generation[0].jump()

pygame.time.delay(1000)
