import os
from datetime import datetime as dt
import pygame
from Pipe import Pipe
from Player import Player
from Game import Game
import numpy as np
import random

now = dt.now()

pygame.init()

run = True
font = pygame.font.Font('freesansbold.ttf', 32) 

class Train:
    def __init__(self, generation_size=10, mutation_ratio = 0.15):
        self.generation_size = generation_size
        self.generation_number = 1
        self.new_gen_weights = []
        self.mutation_ratio = mutation_ratio

        self.game = Game()
        
        self.best_player = Player(initial_fitness=1)
        
        #Create first generation randomly
        for i in range(self.generation_size):
            self.game.generation.append(Player())

        self.models_dir = os.path.join('models', f'{now.day}-{now.month}_{now.hour}:{now.minute}:{now.second}')
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)

    #Mutate random genes
    def mutate(self, weights):
        for i in range(len(weights)):
            for j in range(len(weights[i])):
                if random.uniform(0, 1) > 1 - self.mutation_ratio:
                    noise = random.uniform(-1/self.best_player.fitness, 1/self.best_player.fitness)
                    weights[i][j] += noise
        return weights
    
    def crossover(self):
        #sort chromosomes according to their fitnesses
        self.game.dead.sort(key=lambda x: x.fitness, reverse=True)
    
        #if new chromosome does better, use it, else use previous best chromosome
        parent1 = self.game.dead[0] if self.game.dead[0].fitness > self.best_player.fitness else self.best_player
        # parent1 = dead[0]
        parent2 = self.game.dead[1] if self.game.dead[1].fitness > self.best_player.fitness else self.best_player

        new_weight1 = parent1.model.get_weights()
        new_weight2 = parent2.model.get_weights()
        gene = random.randint(0, len(new_weight1) -1 )
        new_weight1[gene] = parent2.model.get_weights()[gene]
        new_weight2[gene] = parent1.model.get_weights()[gene]

        return np.asarray([new_weight1, new_weight2])

    def run(self):
        while True:
            self.game.SCREEN.blit(self.game.BACKGROUND, [0, 0])
            self.game.text = font.render(f'{self.game.score}', True, (255, 255, 255), (0, 0, 0)) 
            self.game.SCREEN.blit(self.game.text, self.game.text.get_rect())

            self.game.move_player()
            self.game.draw_pipes()

            #On generation end
            if len(self.game.generation) == 0:
                self.new_gen_weights.clear()
                for i in range(self.generation_size//2):
                    self.new_weights = self.crossover() 
                    self.new_gen_weights.append(self.mutate(self.new_weights[0]))
                    self.new_gen_weights.append(self.mutate(self.new_weights[1]))
                #Populate new generation
                for i in self.new_gen_weights:
                    self.game.generation.append(Player(inital_weights=i))


                
                if self.generation_number%5 == 0:
                    self.best_player.model.save(os.path.join(self.models_dir, f'generation-{self.generation_number}_fitness:{round(self.best_player.fitness)}.h5'))

                replace = random.randint(0, self.generation_size)-1
                self.game.generation[replace] = self.best_player
                self.game.generation[replace].fitness = 0
                
                print(f'Generation:{self.generation_number}, Best fitness={self.game.dead[0].fitness}, Score={self.game.score}')
                self.generation_number += 1
                self.game.reset()
                self.game.score = 0

                if self.game.dead[0].fitness > self.best_player.fitness:
                    self.best_player = self.game.dead[0]

                self.game.dead.clear()
                self.new_gen_weights.clear()
            
            if self.game.score == 150:
                self.best_player.model.save(os.path.join(self.models_dir, f'Winner-generation-{self.generation_number}.h5'))
                run = False

            pygame.display.update()
            self.game.clock.tick(self.game.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.generation[0].jump()


if __name__ == '__main__':
    train = Train()
    train.run()



# import keras
# model = keras.models.load_model('models/16-3_1:31:53/Winner-generation-7.h5')
# SCREEN = pygame.display.set_mode((640, 480))
# player = Player(model=model)

# game = Game(generation=[player])
# run = True
# while run:
#     game.SCREEN.blit(game.BACKGROUND, [0, 0])
#     game.text = font.render(f'{game.score}', True, (255, 255, 255), (0, 0, 0)) 
#     game.SCREEN.blit(game.text, game.text.get_rect())
#     game.draw_pipes()
#     run = game.move_player()

#     pygame.display.update()
#     game.clock.tick(game.fps)
