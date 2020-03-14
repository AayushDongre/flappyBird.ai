import pygame

class Pipe():
    def __init__(self):
        self.image = pygame.transform.scale2x(pygame.image.load('./static/pipe.png'))
        self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.top_pipe = self.image.convert()
        self.bottom_pipe = pygame.transform.flip(self.image, False, True).convert()

        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.top_y = 0
        self.bottom_y = 300
        self.difference = 0
        self.x = 500

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top_y - self.height))
        win.blit(self.bottom_pipe, (self.x, self.bottom_y - self.height))

        

