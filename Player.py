import pygame
from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np

class Player:
    def __init__(self, inital_weights=False ):
        self.images = [pygame.image.load(f'static/bird{i}.png').convert() for i in range(3)]
        self.image = self.images[0]
        self.x = 50
        self.y = 240
        self.index = 0
        self.velocity = 0
        self.gravity = 6
        self.ticks = 0

        self.fitness = 0

        self.model = Sequential()
        self.model.add(Dense(3, input_shape=(3, )))
        self.model.add(Activation('relu'))
        self.model.add(Dense(7, input_shape=(3, )))
        self.model.add(Activation('relu'))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        # print(self.model.get_weights())
        if not inital_weights == False:
            # print('using new weights')
            self.model.set_weights(inital_weights)
        self.model.compile(loss='mse',
              optimizer='adam',
              metrics=['accuracy'])


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.index = (self.index + 1) % 3
        self.image = self.images[self.index]

    def jump(self):
        self.velocity = -10
        self.ticks = 0

    def move(self, nextpipe):
        self.ticks += 1
        self.fitness += 0.1
        distance = self.velocity*self.ticks + 1.5*self.ticks**2
        result = self.model.predict(np.atleast_2d([self.y, nextpipe.x, nextpipe.centery]))[0][0]
        # print(result)
        if result > .50:
            self.jump()

        if distance >= 6:
            distance = 6
        if distance < 0:
            distance -= 5
        if self.y <= 5 :
            self.velocity = 0

        self.y = self.y + distance
