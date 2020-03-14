import pygame
from random import randint

dwidth = 640
dheight = 480

class Pipe():
    def __init__(self, initx: int ):
        self.image = pygame.transform.scale2x(
            pygame.image.load('./static/pipe.png'))
        self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))

        self.top_pipe = self.image.convert()
        self.bottom_pipe = pygame.transform.flip(
            self.image, False, True).convert()

        self.rect = self.image.get_rect()
        self.height = self.image.get_height()
        self.width = self.image.get_width()

        self.top_y = 40
        self.bottom_y = 470
        self.difference = 0
        self.centery = 240
        self.x = 630 + initx
        self.set_dimensions()
        self.speed = 5

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.top_y - self.height))
        win.blit(self.bottom_pipe, (self.x, self.bottom_y))

    def set_dimensions(self):
        half = dheight/2
        self.centery = randint(half - 140, half + 140)
        self.difference = randint(60, 150)
        self.top_y = self.centery - self.difference/2
        self.bottom_y = self.centery + self.difference/2

    def move(self):
        self.x -= self.speed
