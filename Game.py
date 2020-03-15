import pygame
from Pipe import Pipe
from Player import Player

class Game:
    def __init__(self, dwidth = 640, dheight = 480, screen = None, x_difference = 350, generation = []):
        self.dwidth = dwidth
        self.dheight = dheight

        self.SCREEN = screen if not screen == None else pygame.display.set_mode((self.dwidth, self.dheight))
        self.BACKGROUND = pygame.image.load('static/background.png').convert()
        self.SCREEN.blit(self.BACKGROUND, [0, 0])
        pygame.display.update()


        self.x_difference = x_difference
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.pipes = [Pipe(0), Pipe(self.x_difference), Pipe(self.x_difference*2)]
        self.generation = generation
        self.dead = []
        self.nextpipe = self.pipes[0]
        self.score = 0


    def draw_pipes(self):
        for pipe in self.pipes:
            pipe.move()
            pipe.draw(self.SCREEN)
            if pipe.x <= -20:
                self.pipes = self.pipes[1:]
                self.score += 1
                self.pipes.append(Pipe(self.x_difference))
        self.nextpipe = self.pipes[0]        


    def reset(self):
        self.pipes.clear()
        [self.pipes.append(i) for i in [Pipe(0), Pipe(self.x_difference), Pipe(self.x_difference*2)]]


    def move_player(self):
        for player in self.generation:
            player.move(self.nextpipe)
            player.draw(self.SCREEN)

        #If player touches ground
            if player.y > self.dheight and player in self.generation:
                self.dead.append(player)
                self.generation.remove(player)
                return False

        #Collision with bottom pipe
            if player.y > self.nextpipe.bottom_y and player.x > self.nextpipe.x and player.x < self.nextpipe.x + self.nextpipe.width and player in self.generation:
                player.fitness += (1 - abs(self.nextpipe.centery - player.y)/self.nextpipe.centery)
                self.dead.append(player)
                self.generation.remove(player)
                return False


            #Collision with top pipe
            if player.y < self.nextpipe.top_y and player.x > self.nextpipe.x and player.x < self.nextpipe.x + self.nextpipe.width and player in self.generation:
                player.fitness += (1 - abs(self.nextpipe.centery - player.y)/self.nextpipe.centery)
                self.dead.append(player)
                self.generation.remove(player)
                return False

        
            #If successfully crossed a pipe, increase fitness
            if player.x > self.nextpipe.x + self.nextpipe.width:
                player.fitness += 3
        return True


