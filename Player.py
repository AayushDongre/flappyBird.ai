import pygame

class Player:
    def __init__(self):
        self.images = [pygame.image.load(f'static/bird{i}.png').convert() for i in range(3)]
        self.image = self.images[0]
        self.x = 50
        self.y = 240
        self.index = 0
        self.velocity = 0
        self.gravity = 6
        self.ticks = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.index = (self.index + 1)%3
        self.image = self.images[self.index]

    def jump(self):
        self.velocity = -10
        self.ticks = 0


    def move(self):
        self.ticks += 1
        distance = self.velocity*self.ticks + 1.5*self.ticks**2

        if distance >= 6:
            distance = 6
        if distance < 0:
            distance -= 5
        self.y = self.y + distance