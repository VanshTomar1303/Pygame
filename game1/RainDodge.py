import pygame
import time
import random
pygame.font.init()

# set up the screen
WIDTH, HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

# title of the game
pygame.display.set_caption("RAIN DODGE")

# background image
# BG = pygame.image.load("bg.jpeg")
# if image is not fitting
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"),(WIDTH,HEIGHT))

# Constant Variable
# player
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

# ENEMY
ENEMY_WIDTH = 10
ENEMY_HEIGHT = 20

# Player Velocity
PLAYER_VEL = 5

# ENEMY Velocity
ENEMY_VEL = 3

# Setting Font
FONT = pygame.font.SysFont("monospace",30)

# To draw image
def draw(player, elapsed_time,enemies):
    WIN.blit(BG,(0,0))

    # draw timer
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text,(10,10))

    # draw character
    pygame.draw.rect(WIN,"purple",player)

    # draw enemies
    for enemy in enemies:
        pygame.draw.rect(WIN, "pink", enemy)

    pygame.display.update()

def main():
    run = True

    # player
    player = pygame.Rect(400,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)

    # clock for how fast player moves
    clock = pygame.time.Clock()

    # timer
    start_time = time.time()
    elapsed_time = 0

    # enemy
    enemy_add_increment = 2000
    enemy_count = 0
    enemies = []

    # if enemy hit us
    hit = False

    # game loop
    while run:
        # set fps and enemy
        enemy_count += clock.tick(60)

        # set timer
        elapsed_time = time.time() - start_time

        # enemy setup
        if enemy_count > enemy_add_increment:
            for _ in range(3):
                # making enemy x coordinate
                enemy_x = random.randint(0,WIDTH - ENEMY_WIDTH)
                # define where is enemy
                enemy = pygame.Rect(enemy_x,-ENEMY_HEIGHT,ENEMY_WIDTH,ENEMY_HEIGHT)
                # adding enemy to list
                enemies.append(enemy)

            # faster enemy generation
            enemy_add_increment = max(50,enemy_add_increment-50)
            enemy_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # player moves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and  player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and  player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and  player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and  player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        # movement of enemies and collision
        for enemy in enemies[:]:
            enemy.y += ENEMY_VEL
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            elif enemy.y  + enemy.height >= player.y and enemy.colliderect(player):
                enemies.remove(enemy)
                hit = True
                break

        # if player is hit GAME OVER
        if hit:
            lost_text = FONT.render("GAME OVER!",1,"white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2,HEIGHT/2 - lost_text.get_height()/2,))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player,elapsed_time,enemies)

    pygame.quit()

# if we're directly running this file without importing it
if __name__ == "__main__":
    main()