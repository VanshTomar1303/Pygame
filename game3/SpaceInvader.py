import pygame
import os
import time
import random

pygame.font.init()

# Screen Height And Width
HEIGHT, WIDTH = 750,750

# Screen
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
# GAME TITLE
pygame.display.set_caption("SPACE INVADER")

# FPS
FPS = 60

# velocity
VEL = 5
ENEMY_VEL = 1

# Font setup
MAIN_FONT = pygame.font.SysFont("monospace",30,"bold")

# colors
WHITE = (255,255,255)

# lazer image
RED_LAZER = pygame.image.load(os.path.join('Assets','pixel_laser_red.png'))
BLUE_LAZER = pygame.image.load(os.path.join('Assets','pixel_laser_blue.png'))
GREEN_LAZER = pygame.image.load(os.path.join('Assets','pixel_laser_green.png'))
YELLOW_LAZER = pygame.image.load(os.path.join('Assets','pixel_laser_yellow.png'))

# enemy ship image
RED_SHIP = pygame.image.load(os.path.join('Assets','pixel_ship_red_small.png'))
BLUE_SHIP = pygame.image.load(os.path.join('Assets','pixel_ship_blue_small.png'))
GREEN_SHIP = pygame.image.load(os.path.join('Assets','pixel_ship_green_small.png'))

# main ship image
YELLOW_SHIP = pygame.image.load(os.path.join('Assets','pixel_ship_yellow.png'))

# background image
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background-black.png')),(WIDTH,HEIGHT))

# character class
class Ship:
    def __init__(self,x,y,health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img,(self.x,self.y))

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LAZER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP,RED_LAZER),
        "blue": (BLUE_SHIP,BLUE_LAZER),
        "green": (GREEN_SHIP,GREEN_LAZER)
    }
    def __init__(self, x, y,color,health=100):
        super().__init__(x, y,health)
        self.ship_img,self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

# main function
def main():
    # game loop variable
    run = True

    # level
    level = 0

    # lives
    lives = 5

    # setting clock for fps
    clock = pygame.time.Clock()

    player = Player(300,650)

    # enemies
    enemies = []
    wave_length = 5

    if len(enemies) == 0:
        level += 1
        wave_length += random.randint(wave_length, wave_length+5)
        for i in range(wave_length):
            enemy = Enemy(random.randrange(50,WIDTH-100),random.randrange(-700*level,-100),random.choice(["red","blue","green"]))
            enemies.append(enemy)

    def redraw_window():
        # background image
        WIN.blit(BG,(0,0))

        # draw lives and level
        lives_label = MAIN_FONT.render(f"LIVES: {lives}",1, WHITE)
        WIN.blit(lives_label,(0,0))
        level_label = MAIN_FONT.render(f"LEVEL: {level}",1, WHITE)
        WIN.blit(level_label,(WIDTH-level_label.get_width(),0))

        for enemie in enemies:
            enemie.draw(WIN)

        player.draw(WIN)

        # update when this function called
        pygame.display.update()

    # game loop
    while run:
        # setting FPS
        clock.tick(FPS)

        # check if user want to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # player moves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - VEL > 0:
            player.x -= VEL
        if keys[pygame.K_RIGHT] and player.x + VEL + player.get_width() < WIDTH:
            player.x += VEL
        if keys[pygame.K_UP] and player.y - VEL > 0:
            player.y -= VEL
        if keys[pygame.K_DOWN] and player.y + VEL + player.get_height() < HEIGHT:
            player.y += VEL

        for enemy in enemies:
            enemy.move(ENEMY_VEL)

        # draw images
        redraw_window()

    # close the game
    pygame.quit()

# the main function is not imported from other files
if __name__ == "__main__":
    main()