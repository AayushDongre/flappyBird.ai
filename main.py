import os
from datetime import datetime as dt
import pygame
from Pipe import Pipe
from Player import Player
import numpy as np
import random

now = dt.now()
models_dir = os.path.join('models', f'{now.day}-{now.month}_{now.hour}:{now.minute}:{now.second}')
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

pygame.init()

dwidth = 640
dheight = 480

SCREEN = pygame.display.set_mode((dwidth, dheight))
BACKGROUND = pygame.image.load('static/background.png').convert()
SCREEN.blit(BACKGROUND, [0, 0])
pygame.display.update()

#Distance between consecutive pipes
x_difference = 350

clock = pygame.time.Clock()
fps = 60

generation_size = 10
generation_number = 1
generation = []
dead = []
new_gen_weights = []
best_player = Player()
mutation_ratio = .15

pipes = [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]

run = True
score = 0
font = pygame.font.Font('freesansbold.ttf', 32) 
text = font.render(f'{score}', True, (255, 255, 255), (0, 0, 0)) 

#Create first generation randomly
for i in range(generation_size):
    generation.append(Player())

def crossover():
    #sort chromosomes according to their fitnesses
    dead.sort(key=lambda x: x.fitness, reverse=True)
 
    #if new chromosome does better, use it, else use previous best chromosome
    parent1 = dead[0] if dead[0].fitness > best_player.fitness else best_player
    # parent1 = dead[0]
    parent2 = dead[1] if dead[1].fitness > best_player.fitness else best_player

    new_weight1 = parent1.model.get_weights()
    new_weight2 = parent2.model.get_weights()
    gene = random.randint(0, len(new_weight1) -1 )
    new_weight1[gene] = parent2.model.get_weights()[gene]
    new_weight2[gene] = parent1.model.get_weights()[gene]

    return np.asarray([new_weight1, new_weight2])

#Mutate random genes
def mutate(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.uniform(0, 1) > 1 - mutation_ratio:
                noise = random.uniform(-0.7, 0.7)
                weights[i][j] += noise
    return weights

#Reset screen after generation over
def reset():
    pipes.clear()
    [pipes.append(i) for i in [Pipe(0), Pipe(x_difference), Pipe(x_difference*2)]]

while True:
    SCREEN.blit(BACKGROUND, [0, 0])
    text = font.render(f'{score}', True, (255, 255, 255), (0, 0, 0)) 
    SCREEN.blit(text, text.get_rect())
    
    #Draw the pipes
    for pipe in pipes:
        pipe.move()
        pipe.draw(SCREEN)
        if pipe.x <= -20:
            pipes = pipes[1:]
            score += 1
            pipes.append(Pipe(x_difference))
    nextpipe = pipes[0]

    for player in generation:
        player.move(nextpipe)
        player.draw(SCREEN)

        #If player touches ground
        if player.y > dheight and player in generation:
            dead.append(player)
            generation.remove(player)

        #Collision with bottom pipe
        if player.y > nextpipe.bottom_y and player.x > nextpipe.x and player.x < nextpipe.x + nextpipe.width and player in generation:
            player.fitness += (1 - abs(nextpipe.centery - player.y)/nextpipe.centery)
            dead.append(player)
            generation.remove(player)

        #Collision with top pipe
        if player.y < nextpipe.top_y and player.x > nextpipe.x and player.x < nextpipe.x + nextpipe.width and player in generation:
            player.fitness += (1 - abs(nextpipe.centery - player.y)/nextpipe.centery)
            dead.append(player)
            generation.remove(player)
    
        #If successfully crossed a pipe, increase fitness
        if player.x > nextpipe.x + nextpipe.width:
            player.fitness += 3

    #On generation end
    if len(generation) == 0:
        score = 0
        new_gen_weights.clear()
        for i in range(generation_size//2):
            new_weights = crossover() 
            new_gen_weights.append(mutate(new_weights[0]))
            new_gen_weights.append(mutate(new_weights[1]))
        #Populate new generation
        for i in new_gen_weights:
            generation.append(Player(inital_weights=i))

        replace = random.randint(0, generation_size)-1
        generation[replace] = best_player
        generation[replace].fitness = 0
        
        if generation_number%5 == 0:
            best_player.model.save(os.path.join(models_dir, f'generation-{generation_number}_fitness:{round(best_player.fitness)}.h5'))

        generation_number += 1
        reset()
        print(f'Generation:{generation_number}, Best fitness={dead[0].fitness}, Score={score}')

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

