import pygame,sys,os
from fighter import Fighter
from obstacle import Obstacle
from network import game_client
from proto import game_pb2 as pb
1
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def draw_bg(screen, bg_image,SCREEN_WIDTH, SCREEN_HEIGHT):
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#draw health bars
def draw_health_bar(screen, health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-3, y-3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))



#game loop
def gameLoop(SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image = pygame.image.load("assets/background.png").convert_alpha()
    pygame.display.set_caption("Team 5 Project")

    # cap frame rate
    # define colors
    # load bg image

    # create fighters
    fighter_1 = Fighter(1, 200, 310, 40, 100, False,10,2)
    fighter_2 = Fighter(2, 700, 310, 40, 100, True,10,2)

    # create obstacles
    obstacle_1 = Obstacle(400, 300, 100, 300)
    obstacle_2 = Obstacle(700, 200, 200, 50)
    obstacles = [obstacle_1, obstacle_2]
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    while run:

        #cap frame rate
        clock.tick(FPS)

        #draw background
        draw_bg(screen,bg_image,SCREEN_WIDTH,SCREEN_HEIGHT)

        #draw health bars
        draw_health_bar(screen,fighter_1.health, 20, 20)
        draw_health_bar(screen,fighter_2.health, 580, 20)

        #move fighters
        fighter_1.move_new(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles)
        fighter_2.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles,None)

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


def multiGameLoop(SCREEN_WIDTH,SCREEN_HEIGHT,game_client):
    gameKeys = [pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_r,pygame.K_t]
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image = pygame.image.load("assets/background.png").convert_alpha()
    pygame.display.set_caption("Team 5 Project")

    # cap frame rate
    # define colors
    # load bg image

    # create fighters
    fighter_1 = Fighter(1, 200, 310, 40, 100, False, 10, 2)
    fighter_2 = Fighter(2, 700, 310, 40, 100, True, 10, 2)

    # create obstacles
    obstacle_1 = Obstacle(400, 300, 100, 300)
    obstacle_2 = Obstacle(700, 200, 200, 50)
    obstacles = [obstacle_1, obstacle_2]
    run = True
    clock = pygame.time.Clock()
    FPS = 60
    while run:

        # cap frame rate
        clock.tick(FPS)

        # draw background
        draw_bg(screen, bg_image, SCREEN_WIDTH, SCREEN_HEIGHT)

        # draw health bars
        draw_health_bar(screen, fighter_1.health, 20, 20)
        draw_health_bar(screen, fighter_2.health, 580, 20)

        # move fighters
        fighter_1.move_new(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles,game_client)
        for message in game_client.get_updates():
            fighter_1.health = message.enemyHealth

            fighter_2.move_enemy2(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles, game_client,message.keys)

        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update display
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    game_client = game_client.GameClient(1234)
    choice = int(input("host: 0, join: 1"))
    if choice == 0:
        host = True
        try:
            game_client.host_game()
        except ConnectionAbortedError:
            print("failed to host game")
            sys.exit(1)
    else:
        try:
            game_client.join_game("192.168.0.33", 1234)

        except ConnectionAbortedError:
            print("failed to join game")
            sys.exit(1)
        game_client.character_select()
        game_client.socket.setblocking(False)

    # create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    multiGameLoop(SCREEN_WIDTH, SCREEN_HEIGHT,game_client)