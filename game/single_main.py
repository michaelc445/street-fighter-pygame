import pygame
from fighter import Fighter
from obstacle import Obstacle
from button import Button
import sys

pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#cap frame rate
clock = pygame.time.Clock()
FPS = 60

#define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#load bg image
bg_image = pygame.image.load("game/assets/background.png").convert_alpha()
menu_bg = pygame.image.load("game/assets/main_menu_bg.png").convert_alpha()

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
obstacle_3  = Obstacle(100,300, 100, 50)
obstacles = [obstacle_1, obstacle_2, obstacle_3]

# font size
def font(size):
    return pygame.font.Font("game/assets/font.ttf", size)

#game loop
def gameLoop():
    run = True
    while run:

        #cap frame rate
        clock.tick(FPS)

        #draw background
        draw_bg()

        #draw health bars
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # update display
        pygame.display.update()
    pygame.quit()
    sys.exit()


# options
def opt():
    while True:
        opt_mouse = pygame.mouse.get_pos()

        screen.fill("white")

        opt_text = font(35).render("This is the OPTIONS screen.", True, "Black")
        opt_rect = opt_text.get_rect(center=(500, 160))
        screen.blit(opt_text, opt_rect)

        opt_back = Button(image=None, pos=(500, 360),
                          text_input="BACK", font=font(50), base_color="Black", hovering_color="Red")

        opt_back.changeColor(opt_mouse)
        opt_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if opt_back.checkForInput(opt_mouse):
                    pygame.display.set_caption("Main Menu")
                    main_menu()

        pygame.display.update()


# main menu
def main_menu():
    while True:
        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(75).render("Main Menu", True, "#b68f40")
        rect = text.get_rect(center=(500, 65))

        play = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 200),
                      text_input="PLAY", font=font(55), base_color="#d7fcd4", hovering_color="White")
        options = Button(image=pygame.image.load("game/assets/Options Rect.png"), pos=(500, 350),
                         text_input="OPTIONS", font=font(55), base_color="#d7fcd4", hovering_color="White")
        quit = Button(image=pygame.image.load("game/assets/Quit Rect.png"), pos=(500, 500),
                      text_input="QUIT", font=font(55), base_color="#d7fcd4", hovering_color="White")

        screen.blit(text, rect)

        for button in [play, options, quit]:
            button.changeColor(mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Game")
                    gameLoop()
                if options.checkForInput(mouse):
                    pygame.display.set_caption("Options")
                    opt()
                if quit.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
