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

#when a button is pressed, it should change the key that is assigned to that action
def control_handling(keys, key):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in fighter_1.player1_controls.values():
                    return
                elif event.key in fighter_2.player2_controls.values():
                    return
                keys[key] = event.key
                return
    

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




# controls
def controls():
    while True:
        controls_mouse = pygame.mouse.get_pos()

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        controls_text = font(50).render("CONTROLS", True, "#b68f40")
        controls_rect = controls_text.get_rect(center=(500, 65))
        screen.blit(controls_text, controls_rect)

        #make player 1 controls with a button
        controls_player1 = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 175),
                          text_input="Player 1", font=font(35), base_color="#d7fcd4", hovering_color="White")                  

        
        controls_player2 = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 325),
                          text_input="Player 2", font=font(35), base_color="#d7fcd4", hovering_color="White")    

        controls_back = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

        for button in [controls_back, controls_player1, controls_player2]:
            button.changeColor(controls_mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if controls_back.checkForInput(controls_mouse):
                    opt()
                if controls_player1.checkForInput(controls_mouse):
                    player1()
                if controls_player2.checkForInput(controls_mouse):
                    player2()

        pygame.display.update()

#fighter1 controls displayed and mutable
def player1():
    #player1_keys = {"left": "a", "right": "d", "jump": "w", "block": "s", "attack1": "r", "attack2": "t"}
    while True:
        player1_mouse = pygame.mouse.get_pos()

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        player1_text = font(50).render("PLAYER 1", True, "#b68f40")
        player1_rect = player1_text.get_rect(center=(500, 65))
        screen.blit(player1_text, player1_rect)

        #make player 1 controls with a button
        player1_up = Button(image=None, pos=(500, 150),
                          text_input="Jump : " + pygame.key.name(fighter_1.player1_controls["jump"]), font=font(15), base_color="#d7fcd4", hovering_color="White")
        
        player1_down = Button(image=None, pos=(500, 200),
                          text_input="Block : " + pygame.key.name(fighter_1.player1_controls["block"]), font=font(15), base_color="#d7fcd4", hovering_color="White")    

        player1_left = Button(image=None, pos=(500, 250),
                          text_input="Left : " + pygame.key.name(fighter_1.player1_controls["left"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_right = Button(image=None, pos=(500, 300),
                          text_input="Right : " + pygame.key.name(fighter_1.player1_controls["right"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_attack1 = Button(image=None, pos=(500, 350),
                          text_input="Punch : " + pygame.key.name(fighter_1.player1_controls["attack1"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_attack2 = Button(image=None, pos=(500, 400),
                          text_input="Projectile : " + pygame.key.name(fighter_1.player1_controls["attack2"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_back = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")


        for button in [player1_back, player1_up, player1_down, player1_left, player1_right, player1_attack1, player1_attack2]:
            button.changeColor(player1_mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1_back.checkForInput(player1_mouse):
                    controls()
                if player1_up.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "jump")
                if player1_down.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "block")
                if player1_left.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "left")
                if player1_right.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "right")
                if player1_attack1.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "attack1")
                if player1_attack2.checkForInput(player1_mouse):
                    control_handling(fighter_1.player1_controls, "attack2")

        pygame.display.update()

#fighter2 controls displayed and mutable
def player2():
    while True:
        player2_mouse = pygame.mouse.get_pos()

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        player2_text = font(50).render("PLAYER 2", True, "#b68f40")
        player2_rect = player2_text.get_rect(center=(500, 65))
        screen.blit(player2_text, player2_rect)

        #make player 2 controls with a button
        player2_up = Button(image=None, pos=(500, 150),
                          text_input="Jump : " + pygame.key.name(fighter_2.player2_controls["jump"]), font=font(15), base_color="#d7fcd4", hovering_color="White")
        
        player2_down = Button(image=None, pos=(500, 200),
                          text_input="Block : " + pygame.key.name(fighter_2.player2_controls["block"]), font=font(15), base_color="#d7fcd4", hovering_color="White")    

        player2_left = Button(image=None, pos=(500, 250),
                          text_input="Left : " + pygame.key.name(fighter_2.player2_controls["left"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_right = Button(image=None, pos=(500, 300),
                          text_input="Right : " + pygame.key.name(fighter_2.player2_controls["right"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_attack1 = Button(image=None, pos=(500, 350),
                          text_input="Punch : " + pygame.key.name(fighter_2.player2_controls["attack1"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_attack2 = Button(image=None, pos=(500, 400),
                          text_input="Projectile : " + pygame.key.name(fighter_2.player2_controls["attack2"]), font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_back = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")
        
        for button in [player2_back, player2_up, player2_down, player2_left, player2_right, player2_attack1, player2_attack2]:
            button.changeColor(player2_mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player2_back.checkForInput(player2_mouse):
                    controls()
                if player2_up.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "jump")
                if player2_down.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "block")
                if player2_left.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "left")
                if player2_right.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "right")
                if player2_attack1.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "attack1")
                if player2_attack2.checkForInput(player2_mouse):
                    control_handling(fighter_2.player2_controls, "attack2")

        pygame.display.update()


# options
def opt():
    while True:
        opt_mouse = pygame.mouse.get_pos()

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        opt_text = font(50).render("OPTIONS", True, "#b68f40")
        opt_rect = opt_text.get_rect(center=(500, 65))
        screen.blit(opt_text, opt_rect)


        opt_controls = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 175),
                          text_input="CONTROLS", font=font(35), base_color="#d7fcd4", hovering_color="White")
        opt_audio = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 325),
                          text_input="AUDIO", font=font(35), base_color="#d7fcd4", hovering_color="White")                  
        opt_back = Button(image=pygame.image.load("game/assets/Play Rect.png"), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

        for button in [opt_controls, opt_audio, opt_back]:
            button.changeColor(opt_mouse)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if opt_back.checkForInput(opt_mouse):
                    pygame.display.set_caption("Main Menu")
                    main_menu()
                if opt_controls.checkForInput(opt_mouse):
                    pygame.display.set_caption("Controls")
                    controls()
                #if opt_audio.checkForInput(opt_mouse):
                #    pygame.display.set_caption("Audio")
                #    audio()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
