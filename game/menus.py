from button import Button
import pygame
import sys
import single_main
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
menu_bg = pygame.image.load("assets/main_menu_bg.png").convert_alpha()
def font(size):
    return pygame.font.Font("assets/font.ttf", size)


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
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(75).render("Main Menu", True, "#b68f40")
        rect = text.get_rect(center=(500, 65))

        play = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 200),
                      text_input="PLAY", font=font(55), base_color="#d7fcd4", hovering_color="White")
        options = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 350),
                         text_input="OPTIONS", font=font(55), base_color="#d7fcd4", hovering_color="White")
        quit = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 500),
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
                    single_main.gameLoop()
                if options.checkForInput(mouse):
                    opt()
                if quit.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()