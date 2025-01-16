import random

import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Screen Size
WIDTH, HEIGHT = 900,500

# making window / screen
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# title of game
pygame.display.set_caption("Jujutsu Kaisen")

# color
GRAY = (130,140,150)
BLACK = (0,0,0)
WHITE = (255,255,255)

# Bullet color
RED = (255,0,0)
YELLOW = (255,255,0)

# FPS
FPS = 60

# font
HEALTH_FONT = pygame.font.SysFont('monospace', 30)
WINNER_FONT = pygame.font.SysFont('monospace', 100,50)

# if player got hit by any bullets
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Velocity
VEL = 5
BULLET_VEL = 6

# Bullets Maximum Number
MAX_BULLET = 5

# player
PLAYER_HEIGHT = 60
PLAYER_WIDTH = 40

SUKUNA_HEIGHT = 100
SUKUNA_WIDTH = 55

# BORDER
BORDER = pygame.Rect((WIDTH//2)-5,0,10,HEIGHT)

# player image load
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","sukuna.png"))
# resizing the image and rotate it
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SUKUNA_WIDTH,SUKUNA_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","gojo.png"))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT))

# space background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets",'JJKBG.jpg')),(WIDTH,HEIGHT))
SUKUNAVSGOJO = pygame.transform.scale(pygame.image.load(os.path.join("Assets",'sukunaVsGojo.png')),(WIDTH,HEIGHT))

# sound effect
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

SUKUNA_DOMAIN = pygame.mixer.Sound(os.path.join("Assets","sukunas_domain.mp3"))
GOJO_DOMAIN = pygame.mixer.Sound(os.path.join("Assets","gojo_domain.mp3"))

SUKUNA_WIN = pygame.mixer.Sound(os.path.join("Assets","ganbare_sukuna.mp3"))
GOJO_WIN = pygame.mixer.Sound(os.path.join("Assets","yowai_mo.mp3"))

# draw function
def draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # background
    #WIN.fill(GRAY)
    WIN.blit(SPACE,(0,0))

    # border
    pygame.draw.rect(WIN, BLACK, BORDER)

    # drawing players
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))

    # Health bar
    red_health_text = HEALTH_FONT.render("HEALTH: "+str(red_health), 1, BLACK)
    yellow_health_text = HEALTH_FONT.render("HEALTH: "+str(yellow_health), 1, BLACK)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text,(10, 10))

    # bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    # update screen after doing things
    pygame.display.update()

def yellow_moves(keys_pressed,yellow):
    # checking what key is pressed
    # for yellow
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Left
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Right
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Up
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # Down
        yellow.y += VEL

def red_moves(keys_pressed, red) :
    # checking what key is pressed
    # for red
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Left
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Right
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Up
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # if red was hit
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x >  WIDTH:
            yellow_bullets.remove(bullet)

    # if yellow was hit
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(winner):
    win = WINNER_FONT.render(winner, 1, WHITE)
    WIN.blit(win, (WIDTH//2 - win.get_width()/2, HEIGHT//2 - win.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def starting_screen():
    WIN.blit(SUKUNAVSGOJO,(0,0))
    win = WINNER_FONT.render("Saturu Gojo VS Royman Sukuna", 1, WHITE)
    WIN.blit(win, (WIDTH // 2 - win.get_width() / 2, HEIGHT // 2 - win.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main function
def main():
    # two rect for players
    red = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    yellow = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    # bullets
    red_bullets = []
    yellow_bullets = []

    # health
    red_health = 100
    yellow_health = 100

    # setting clock for how much is the game frame rate
    clocks = pygame.time.Clock()

    # for the game loop
    run = True

    start_screen = True

    # game loop
    while run:
        if start_screen:
            starting_screen()
            start_screen = False
        else:
            # setting up the FPS / control the while loop
            clocks.tick(FPS)

            # this for loop is for getting all the events
            for event in pygame.event.get():
                # this checks if user quit the game screen
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break

                # bullet fire
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and  len(yellow_bullets) < MAX_BULLET: # for left control
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL and  len(red_bullets) < MAX_BULLET: # for right control
                        bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                # finding hit events
                if event.type == RED_HIT:
                    if random.randint(0,5) == 3:
                        red_health -= 30
                        SUKUNA_DOMAIN.play()
                    else:
                        red_health -= 10
                        BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    if random.randint(0,5) == 3:
                        red_health -= 30
                        GOJO_DOMAIN.play()
                    else:
                        yellow_health -= 10
                        BULLET_HIT_SOUND.play()

            # If any of the players health reaches 0
            winner_text = ""
            if red_health <= 0:
                winner_text = "SUKUNA WINS!"
                SUKUNA_DOMAIN.stop()
                SUKUNA_WIN.play()

            if yellow_health <= 0:
                winner_text = "GOJO WINS!"
                GOJO_DOMAIN.stop()
                GOJO_WIN.play()

            if winner_text != "":
                draw_winner(winner_text)
                break

            # moves for yellow (W, A, S, D)
            # get what key is pressed
            keys_pressed = pygame.key.get_pressed()

            # calling movement function
            yellow_moves(keys_pressed, yellow)
            red_moves(keys_pressed,red)

            # to shoot bullet and collision
            handle_bullets(yellow_bullets, red_bullets, yellow, red)

            # calling function to draw something and update screen
            draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health)

    # closing the py game
    #pygame.quit()

    # if we want to restart
    main()

# the main function is not imported from other files
if __name__ == "__main__":
    main()