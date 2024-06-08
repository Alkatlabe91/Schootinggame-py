import pygame
import random

width, height = 800, 432
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((width, height))




class Enemy():
    def __init__(self):
        self.x = 800
        self.y = random.randint(0, 320)
        # print( self.y, self.x)
        self.dy =  random.randint(10, 50) / -10

        self.dx = random.randint(10, 50) / -10
        self.surface = pygame.image.load('img/enemies/enemy.png')
       

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        # Border check
        if self.x < 0:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 320)

        # Check for border collision
        if self.y < 0:
            self.y = 0
            self.dy *= -1
            
        elif self.y > 380 :
            self.y = 380    
            self.dy *= -1

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))