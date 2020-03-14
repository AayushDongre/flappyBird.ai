import pygame

class Player:
    def __init__(self):
        self.images = [pygame.image.load(f'static/bird{i}.png').convert() for i in range(3)]
        self.image = self.images[0]
        self.x = 50
        self.y = 240
        self.index = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.index = (self.index + 1)%3
        self.image = self.images[self.index]