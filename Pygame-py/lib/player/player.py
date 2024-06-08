import pygame

width, height = 800, 432
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((width, height))

# Create the player surfcae
class Player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dy = 0
        self.dx = 0
        self.surface = pygame.image.load("img/player/craft.png").convert_alpha()
        player_width = self.surface.get_width()
        player_height = self.surface.get_height()
        self.score = 0
        self.max_health = 20
        self.health = self.max_health
        




    def up(self):
        self.dy = -4

    def down(self):
        self.dy = 4

    def left(self):
        self.dx = -4

    def right(self):
        self.dx = 4
    # def stop(self):
    #     self.dx = 0
    #     self.dy = 0

    def move(self):
        self.y = self.y + self.dy
        self.x = self.x + self.dx

        # Check for border collision
        if self.y < 0:
            self.y = 0
            self.dy = 0

        elif self.y > 320:
            self.y = 320
            self.dy = 0

        if self.x < 0:
            self.x = 0
            self.dx = 0

        elif self.x > 150:
            self.x = 150
            self.dx = 0

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def setMaximumPlayerHealth(self):
        self.health = self.max_health

    def setPlayerScore(self,score):
        self.score = score

    def render(self):
        screen.blit(self.surface, (self.x, self.y))
        # Draw health meter
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)),
                         (int(self.x + (50 * (self.health / self.max_health))), int(self.y)), 2)
