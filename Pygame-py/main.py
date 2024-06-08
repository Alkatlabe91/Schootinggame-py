import pygame
import random
import sys
from pygame import mixer
from lib.player.player import Player
from lib.enemy.enemy import Enemy
from lib.missile.missile import Missile
from lib.powerup.powerUp import Powerup
from database.database import load_highest_score,save_highest_score


pygame.init()
pygame.display.set_caption("Sidescrolling Shooter by @Alaa Alkatlabe")


clock = pygame.time.Clock()


FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
running = True
game_state = 'game'


#Create screen window
width, height = 800, 432
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('AlienBlaster')

pygame.time.delay(1000)

# Icon
icon = pygame.image.load('icons/ufo.png')
pygame.display.set_icon(icon)

#define game variabelen
scroll = 0
ground_image = pygame.image.load("img/background/ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()


# Background
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"img/background/plx-{i}.png").convert_alpha()
    bg_images.append(bg_image)
    bg_width = bg_images[0].get_width()

def draw_bg():
    for x in range(5):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2

def draw_ground():
    for x in range(15):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.2, height - ground_height))


# Create sounds
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)
missile_sound = pygame.mixer.Sound("sounds/laser.wav")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

# Create font
font = pygame.font.SysFont("comicsansms", 24)

# Create objects
player = Player()
powerUp = Powerup()
missiles = [Missile(), Missile(), Missile()]
enemies = []
for _ in range(5):
    enemies.append(Enemy())

powerups = []
for _ in range(1):
    powerups.append(Powerup())


#Create new missile
def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.fire(player)
            missile_sound.play()
            break

#Show score
def show_score (x,y):
    score = font.render("Score : " + str(player.score),True,(255, 255, 255))
    screen.blit(score, (x,y))


#Background events
def background_events(scroll):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 1
    if key[pygame.K_RIGHT] and scroll < 1500:
        scroll += 1
    if scroll == 1500:
        scroll = 0
    

def start_game(): 
    global scroll, game_state
    scroll += 0.5


    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= .2
    if key[pygame.K_RIGHT] and scroll < 1500:
        scroll += 0.5

    
    if scroll >= 1500:
        scroll = 0
    

    #evenhandler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


    # Keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()



# Update objects
    player.move()
    powerUp.move()
    for missile in missiles:
        missile.move()
    for enemy in enemies:
        enemy.move()

        for missile in missiles:
            if enemy.distance(missile) < 20:
                enemy.x = random.randint(800, 900)
                enemy.y = random.randint(-350, 350)
                # enemy.dx *= 0.8
                missile.dx = 0
                missile.x = 0
                missile.y = 1000
                missile.state = "ready"
                player.score += 5
                explosion_sound.play()

        # Check for powerup
        if powerUp.distance(player) < 20:
            if player.health < player.max_health:
                player.health += 5
            else:
                player.score = 0    
            powerUp.x = random.randint(800, 900)
            powerUp.y = random.randint(-350, 350)


        # Check for collision(
        if enemy.distance(player) < 20:
            player.health -= random.randint(5, 10)
            enemy.x = random.randint(800, 900)
            enemy.y = random.randint(-350, 350)
            if player.health <= 0:
                save_highest_score(player.score)
                game_state = 'game_over'
                # print("Game over!")
                # pygame.quit()
                # exit()





    # Render objects
    player.render()
    powerUp.render()
    show_score(10, 400)
    for missile in missiles:
        missile.render()
    for enemy in enemies:
        enemy.render()
        
    ammo = 0
    for missile in missiles:
        if missile.state == "ready":
            ammo += 1
    for x in range(ammo):
        screen.blit(missile.surface, ( 700 + 20 * x , 20))

#Game over screen
def game_over_screen (): 
    font = pygame.font.SysFont('comicsansms', 20)
    highest_score = load_highest_score()
    title = font.render(f'Game Over, Your Score is {player.score}, Your highest score is {highest_score}', True, (255, 255, 255))
    restart = font.render('Press R to Restart', True, (255, 255, 255))
    quit = font.render('Press Q to Quit', True, (255, 255, 255))
    screen.blit(title, (width/2 - title.get_width()/2, width/2 - title.get_height()/3))
    screen.blit(restart, (width/2 - restart.get_width()/2, height/1.9 + restart.get_height()))
    screen.blit(quit, (width/2 - quit.get_width()/2, height/2 + quit.get_height()/2))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            sys.exit()

# Main Game loop
        
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

#draw world
    draw_bg()
    draw_ground()
    if game_state == 'game': 
     start_game()
    else:
       game_over_screen()
       keys = pygame.key.get_pressed()
       if keys[pygame.K_r]:
           player.setMaximumPlayerHealth()
           player.setPlayerScore(0)
           game_state = "game"
       if keys[pygame.K_q]:
           pygame.quit()
           quit()
    pygame.display.flip()


