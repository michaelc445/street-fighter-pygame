import pygame
from fighter import Fighter
from obstacle import Obstacle

pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Team 5 Project")

#cap frame rate
clock = pygame.time.Clock()
FPS = 60

#define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#load bg image
bg_image = pygame.image.load("game/assets/background.png").convert_alpha()

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#draw health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-3, y-3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#create fighters
fighter_1 = Fighter(1, 200, 310, 40, 100, False)
fighter_2 = Fighter(2, 700, 310, 40, 100, True)

#create obstacles
obstacle_1 = Obstacle(400, 300, 100, 300)
obstacle_2 = Obstacle(700, 200, 200, 50)
obstacles = [obstacle_1, obstacle_2]

#game loop
run = True
while run:

    #next frame
    clock.tick(FPS)

    #draw background
    draw_bg()

    #draw player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles)

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()
pygame.quit()