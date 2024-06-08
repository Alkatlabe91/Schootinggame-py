import pygame

width, height = 800, 432
screen = pygame.display.set_mode((width, height))

class Missile():
    def __init__(self):
        self.x = 0
        self.y = 1000
        self.dx = 0
        self.surface = pygame.image.load('img/missile/missile.png').convert()
        self.state = "ready"


    def fire(self,player):
        self.state = "firing"
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = 10

    def move(self):
        if self.state == "firing":
            self.x = self.x + self.dx
        if self.x > 800:
            self.state = "ready"
            self.y = 1000


    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))

