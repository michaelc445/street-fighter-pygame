import pygame, asyncio, pygame_textinput
from pygame import mixer
from game.fighter import Fighter
from game.fighter_Bot import Fighter_Bot
from game.online_fighter import OnlineFighter
from game.characters.nomad import createNomad
from game.characters.warrior import createWarrior
from game.characters.wizard import createWizard
from game.obstacle import Obstacle
from game.button import Button
from game.network.game_client import GameClient
import sys, os
import time


def draw_bg(scaled_bg_image):

    screen.blit(scaled_bg_image, (0, 0))

def draw_text(text, font, color, surface, x, y):
    text = font.render(text, True, color)
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)

# draw health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def draw_scores(p1_score, p2_score):
    score = " - "
    draw_text(score, font(30), WHITE, screen, SCREEN_WIDTH / 2, 35)
    draw_text(str(p1_score), font(30), WHITE, screen, SCREEN_WIDTH / 2 - 50, 35)
    draw_text(str(p2_score), font(30), WHITE, screen, SCREEN_WIDTH / 2 + 50, 35)
# font size
def font(size):
    return pygame.font.Font(resource_path("game/assets/menu/font.ttf"), size)

def locateFighter(fighter):
    print(fighter.rect.x, fighter.rect.y)

# when a button is pressed, it should change the key that is assigned to that action
def control_handling(keys, key):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in player1_controls.values():
                    return
                elif event.key in player2_controls.values():
                    return
                keys[key] = event.key
                return


def sfx_change(level):
    if level == 0:
        punch_fx.set_volume(0)
        projectile_fx.set_volume(0)
        hit_fx.set_volume(0)
    elif level == 1:
        punch_fx.set_volume(0.1)
        projectile_fx.set_volume(0.25)
        hit_fx.set_volume(0.25)
    elif level == 2:
        punch_fx.set_volume(0.15)
        projectile_fx.set_volume(0.5)
        hit_fx.set_volume(0.5)
    elif level == 3:
        punch_fx.set_volume(0.2)
        projectile_fx.set_volume(0.75)
        hit_fx.set_volume(0.75)
    elif level == 4:
        punch_fx.set_volume(0.3)
        projectile_fx.set_volume(1)
        hit_fx.set_volume(1)
#local game loop
# game loop
def game_loop():
    if map == "mountain":
        p1_spawn = [100, 134]
        p2_spawn = [850, 134]
        map_chosen = "game/assets/maps/mountain.png"
        # mountain obstacles
        middle_ground1 = Obstacle(270, 410, 465, 60)
        middle_ground2 = Obstacle(290, 470, 425, 60)
        left_cliff1 = Obstacle(0, 235, 240, 60)
        left_cliff2 = Obstacle(0, 295, 205, 60)
        left_cliff3 = Obstacle(0, 355, 150, 60)
        left_cliff4 = Obstacle(0, 405, 125, 300)
        right_cliff1 = Obstacle(760, 235, 240, 60)
        right_cliff2 = Obstacle(800, 295, 205, 60)
        right_cliff3 = Obstacle(850, 355, 150, 60)
        right_cliff4 = Obstacle(875, 405, 125, 300)

        obstacles = [middle_ground1, middle_ground2, left_cliff1, left_cliff2, left_cliff3, left_cliff4, right_cliff1,
                     right_cliff2, right_cliff3, right_cliff4]

    elif map == "church":
        p1_spawn = [56, 286]
        p2_spawn = [900, 286]
        map_chosen = "game/assets/maps/church.png"
        # church obstacles
        middle_floor = Obstacle(150, 530, 700, 80)
        left_side = Obstacle(0, 387, 142, 160)
        right_side = Obstacle(860, 387, 142, 160)
        middle_top = Obstacle(235, 240, 525, 40)

        obstacles = [middle_floor, left_side, right_side, middle_top]

    elif map == "cliffs":
        p1_spawn = [135, 254]
        p2_spawn = [870, 45]
        map_chosen = "game/assets/maps/cliffs.png"
        # cliffs obstacles
        left_island1 = Obstacle(107, 355, 90, 20)
        left_island2 = Obstacle(120, 355, 60, 45)
        middle_island1 = Obstacle(325, 275, 400, 25)
        middle_island2 = Obstacle(350, 295, 350, 27)
        right_cliff1 = Obstacle(797, 145, 300, 50)
        right_cliff2 = Obstacle(810, 195, 200, 40)
        right_cliff3 = Obstacle(830, 235, 200, 35)
        right_cliff4 = Obstacle(850, 265, 200, 35)
        right_cliff5 = Obstacle(870, 285, 200, 35)
        right_cliff6 = Obstacle(225, 500, 570, 80)

        obstacles = [left_island1, left_island2, middle_island1, middle_island2, right_cliff1, right_cliff2,
                     right_cliff3, right_cliff4, right_cliff5, right_cliff6]

    if p1 == "wizard":
        fighter_1 = createWizard(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx,
                                 player1_controls)

    elif p1 == "nomad":
        fighter_1 = createNomad(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx,
                                player1_controls)

    elif p1 == "warrior":
        fighter_1 = createWarrior(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx,
                                  player1_controls)

    if p2 == "wizard":
        fighter_2 = createWizard(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                 player2_controls)

    elif p2 == "nomad":
        fighter_2 = createNomad(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                player2_controls)

    elif p2 == "warrior":
        fighter_2 = createWarrior(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                  player2_controls)

    # load map
    bg_image = pygame.image.load(resource_path(map_chosen)).convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    scores = [0, 0]
    # round variables
    intro = 3
    over = False
    round_cd = 1500
    last_tick_update = pygame.time.get_ticks()

    while run:

        # cap frame rate
        clock.tick(GAME_FPS)

        # draw background
        draw_bg(scaled_bg)

        # draw health bars
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)

        draw_scores(scores[0], scores[1])

        # move fighters
        if intro <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles)
        else:
            draw_text(str(intro), font(80), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            # reduce intro by 1 every second using pygame.time.get_ticks()
            if pygame.time.get_ticks() - last_tick_update >= 1000:
                intro -= 1
                last_tick_update = pygame.time.get_ticks()

        if over == False:
            if not fighter_1.alive:
                scores[1] += 1
                over = True
                over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                scores[0] += 1
                over = True
                over_time = pygame.time.get_ticks()
        else:
            if scores[0] == 3 or scores[1] == 3:
                break
            if fighter_1.alive:
                draw_text("PLAYER 1 WINS", font(50), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            elif fighter_2.alive:
                draw_text("PLAYER 2 WINS", font(50), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            if pygame.time.get_ticks() - over_time >= round_cd:
                over = False
                fighter_1.reset()
                fighter_2.reset()

        # update pulse
        fighter_1.frameUpdate()
        fighter_2.frameUpdate()

        # draw fighters
        p1_name = "P1"
        p1_colour = (0, 0, 255)
        p2_name = "P2"
        p2_colour = (255, 0, 0)

        fighter_1.draw(screen, p1_name, p1_colour)
        fighter_2.draw(screen, p2_name, p2_colour)

        # draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # if fighter 1 or 2 punches, play the punch.wav sound effect
        # print coordinates of player 1
        # locateFighter(fighter_1)
        # update display
        pygame.display.update()
    mixer.music.load(resource_path("game/assets/audio/background-menu.wav"))
    mixer.music.play(-1)
    # mixer.music.set_volume(0)

# single player game loop
def single_game_loop():
    if map == "mountain":
        p1_spawn = [100, 134]
        p2_spawn = [850, 134]
        map_chosen = "game/assets/maps/mountain.png"
        # mountain obstacles
        middle_ground1 = Obstacle(270, 410, 465, 60)
        middle_ground2 = Obstacle(290, 470, 425, 60)
        left_cliff1 = Obstacle(0, 235, 240, 60)
        left_cliff2 = Obstacle(0, 295, 205, 60)
        left_cliff3 = Obstacle(0, 355, 150, 60)
        left_cliff4 = Obstacle(0, 405, 125, 300)
        right_cliff1 = Obstacle(760, 235, 240, 60)
        right_cliff2 = Obstacle(800, 295, 205, 60)
        right_cliff3 = Obstacle(850, 355, 150, 60)
        right_cliff4 = Obstacle(875, 405, 125, 300)

        obstacles = [middle_ground1, middle_ground2, left_cliff1, left_cliff2, left_cliff3, left_cliff4, right_cliff1,
                     right_cliff2, right_cliff3, right_cliff4]

    elif map == "church":
        p2_spawn = [900, 286]
        p1_spawn = [56, 286]
        map_chosen = "game/assets/maps/church.png"
        # church obstacles
        middle_floor = Obstacle(150, 530, 700, 80)
        left_side = Obstacle(0, 387, 142, 160)
        right_side = Obstacle(860, 387, 142, 160)
        middle_top = Obstacle(235, 240, 525, 40)

        obstacles = [middle_floor, left_side, right_side, middle_top]

    elif map == "cliffs":
        p1_spawn = [135, 254]
        p2_spawn = [870, 45]
        map_chosen = "game/assets/maps/cliffs.png"
        # cliffs obstacles
        left_island1 = Obstacle(107, 355, 90, 20)
        left_island2 = Obstacle(120, 355, 60, 45)
        middle_island1 = Obstacle(325, 275, 400, 25)
        middle_island2 = Obstacle(350, 295, 350, 27)
        right_cliff1 = Obstacle(797, 145, 300, 50)
        right_cliff2 = Obstacle(810, 195, 200, 40)
        right_cliff3 = Obstacle(830, 235, 200, 35)
        right_cliff4 = Obstacle(850, 265, 200, 35)
        right_cliff5 = Obstacle(870, 285, 200, 35)
        right_cliff6 = Obstacle(225, 500, 570, 80)

        obstacles = [left_island1, left_island2, middle_island1, middle_island2, right_cliff1, right_cliff2, right_cliff3, right_cliff4, right_cliff5, right_cliff6]

    if p1 == "wizard":
        fighter_1 = createWizard(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)

    elif p1 == "nomad":
        fighter_1 = createNomad(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)

    elif p1 == "warrior":
        fighter_1 = createWarrior(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)


    if p2 == "wizard":
        fighter_2 = createWizard(Fighter_Bot, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                 player2_controls)

    elif p2 == "nomad":
        fighter_2 = createNomad(Fighter_Bot, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                player2_controls)

    elif p2 == "warrior":
        fighter_2 = createWarrior(Fighter_Bot, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,
                                  player2_controls)


    #load map
    bg_image = pygame.image.load(resource_path(map_chosen)).convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    scores = [0,0]
    #round variables
    intro = 3
    over = False
    round_cd = 1500
    last_tick_update = pygame.time.get_ticks()

    while run:

        player_state = fighter_1.return_state()

        fighter_2.set_moves(player_state)
        # cap frame rate
        clock.tick(GAME_FPS)

        # draw background
        draw_bg(scaled_bg)

        # draw health bars
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)

        draw_scores(scores[0], scores[1])


        # move fighters
        if intro <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles)
        else:
            draw_text(str(intro), font(80), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            #reduce intro by 1 every second using pygame.time.get_ticks()
            if pygame.time.get_ticks() - last_tick_update >= 1000:
                intro -= 1
                last_tick_update = pygame.time.get_ticks()


        if over == False:
            if not fighter_1.alive:
                scores[1] += 1
                over = True
                over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                scores[0] +=1
                over = True
                over_time = pygame.time.get_ticks()
        else:
            if fighter_1.alive:
                draw_text(p1_name + " WINS", font(50), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            elif fighter_2.alive:
                draw_text(p2_name + " WINS", font(50), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
            if pygame.time.get_ticks() - over_time >= round_cd:
                over = False
                if scores[0] == 3 or scores[1] == 3:
                    if scores[0] == 3:
                        winner = p1_name
                    else:
                        winner = p2_name
                    #victory_screen(screen, winner, scaled_bg)
                    if victory_screen(screen, winner, scaled_bg, fighter_1, fighter_2) == "rematch":
                        scores = [0,0]
                    else:
                        break
                fighter_1.flip = False
                fighter_1.reset()
                fighter_2.reset()




        # update pulse
        fighter_1.frameUpdate()
        fighter_2.frameUpdate()

        # draw fighters
        p1_name = "Player 1"
        p1_colour = (0, 0, 255)
        p2_name = "Player 2"
        p2_colour = (255, 0, 0)

        fighter_1.draw(screen, p1_name,p1_colour)
        fighter_2.draw(screen, p2_name, p2_colour)





        # draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # if fighter 1 or 2 punches, play the punch.wav sound effect
        #print coordinates of player 1
        #locateFighter(fighter_1)
        # update display
        pygame.display.update()

    mixer.music.load(resource_path("game/assets/audio/background-menu.wav"))
    mixer.music.play(-1)
    #mixer.music.set_volume(0)


# victory screen
def victory_screen(screen, winner, scaled_bg, fighter1, fighter2):
    leave_menu = False
    run = True	
    victory_back = Button(image=None, pos=(500, 405),
                    text_input="Back", font=font(35),
                    base_color="White", hovering_color="Grey")

    victory_rematch = Button(image=None, pos=(500, 475),
                    text_input="Rematch", font=font(35),
                    base_color="White", hovering_color="Grey") 
    idk = " "
    while run:
        # set background
        mouse = pygame.mouse.get_pos()
        screen.blit(scaled_bg, (0, 0))
        # draw text

        draw_text("VICTORY", font(80), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 3)
        draw_text(str(winner) + " WINS", font(50), RED, screen, (SCREEN_WIDTH / 2), SCREEN_HEIGHT / 2)


        fighter1.draw(screen, "", (0, 0, 255))
        fighter2.draw(screen , "", (255, 0, 0))
        
        for button in [victory_back, victory_rematch]:
            button.hover(mouse)
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
                if victory_back.check_for_input(mouse):
                    leave_menu = True
                    idk = "back"
                    return idk
                if victory_rematch.check_for_input(mouse):
                    leave_menu = True
                    idk = "rematch"
                    return idk
        if leave_menu:
            return idk
        pygame.display.update()

async def update_enemy(game_client, local_player, enemy_character):
    for message in game_client.get_updates():
        local_player.health = message.enemyHealth
        enemy_character.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, local_player, obstacles,

                                   message.keys, message.x, message.y)


def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()


def multi_player_game_loop(game_client):
    # gameKeys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t]
    pygame.init()
    if game_client.map_choice == 1:
        p1_spawn = [100, 100]
        p2_spawn = [850, 100]
        map_chosen = "game/assets/maps/mountain.png"
        # mountain obstacles
        middle_ground1 = Obstacle(270, 410, 465, 60)
        middle_ground2 = Obstacle(290, 470, 425, 60)
        left_cliff1 = Obstacle(0, 235, 240, 60)
        left_cliff2 = Obstacle(0, 295, 205, 60)
        left_cliff3 = Obstacle(0, 355, 150, 60)
        left_cliff4 = Obstacle(0, 405, 125, 300)
        right_cliff1 = Obstacle(760, 235, 240, 60)
        right_cliff2 = Obstacle(800, 295, 205, 60)
        right_cliff3 = Obstacle(850, 355, 150, 60)
        right_cliff4 = Obstacle(875, 405, 125, 300)
        obstacles = [middle_ground1, middle_ground2, left_cliff1, left_cliff2, left_cliff3, left_cliff4, right_cliff1,
                     right_cliff2, right_cliff3, right_cliff4]
    elif game_client.map_choice == 0:
        p1_spawn = [80, 100]
        p2_spawn = [900, 100]
        map_chosen = "game/assets/maps/church.png"
        # church obstacles
        middle_floor = Obstacle(150, 530, 700, 80)
        left_side = Obstacle(0, 387, 142, 160)
        right_side = Obstacle(860, 387, 142, 160)
        middle_top = Obstacle(235, 240, 525, 40)

        obstacles = [middle_floor, left_side, right_side, middle_top]
    elif game_client.map_choice == 2:
        p1_spawn = [500, 100]
        p2_spawn = [500, 400]
        map_chosen = "game/assets/maps/cliffs.png"
        # cliffs obstacles
        left_island1 = Obstacle(107, 355, 90, 20)
        left_island2 = Obstacle(120, 355, 60, 45)
        middle_island1 = Obstacle(325, 275, 400, 25)
        middle_island2 = Obstacle(350, 295, 350, 27)
        right_cliff1 = Obstacle(797, 145, 300, 50)
        right_cliff2 = Obstacle(810, 195, 200, 40)
        right_cliff3 = Obstacle(830, 235, 200, 35)
        right_cliff4 = Obstacle(850, 265, 200, 35)
        right_cliff5 = Obstacle(870, 285, 200, 35)
        right_cliff6 = Obstacle(225, 500, 570, 80)

        obstacles = [left_island1, left_island2, middle_island1, middle_island2, right_cliff1, right_cliff2,
                     right_cliff3, right_cliff4, right_cliff5, right_cliff6]
    else:
        game_client.quit_game()
        print("failed to load map ", game_client.map_choice)
        return

    pygame.display.set_caption("Team 5 Project")
    char_dict = {0: createNomad, 1: createWizard, 2: createWarrior}
    if game_client.player_id == 0:
        # create fighters
        f1 = char_dict[game_client.local_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx,
                                               projectile_fx, hit_fx, player1_controls)
        f2 = char_dict[game_client.enemy_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx,
                                               projectile_fx, hit_fx, player1_controls)
    else:
        f1 = char_dict[game_client.enemy_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx,
                                               projectile_fx, hit_fx, player1_controls)
        f2 = char_dict[game_client.local_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx,
                                               projectile_fx, hit_fx, player1_controls)

    fighters = [f1, f2]
    pick = int(game_client.player_id)

    local_player = fighters[pick]
    local_player.game_client = game_client
    enemy = (pick + 1) % 2
    enemy_character = fighters[enemy]

    bg_image = pygame.image.load(resource_path(map_chosen)).convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    loop = asyncio.get_event_loop()
    quit_game_to_menu = False
    scores = [0, 0]
    local_name = game_client.player_name
    if local_name == "":
        local_name = "YOU"
    local_colour = (0, 0, 255)
    enemy_name = game_client.enemy_name
    if enemy_name == "":
        enemy_name = "ENEMY"
    while run:

        # cap frame rate
        clock.tick(GAME_FPS)

        # draw background
        draw_bg(scaled_bg)

        # draw health bars
        draw_health_bar(fighters[0].health, 20, 20)
        draw_health_bar(fighters[1].health, 580, 20)

        draw_scores(scores[0],scores[1])
        # move fighters

        message = local_player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, enemy_character, obstacles, game_client)
        loop.create_task(local_player.game_client.send_update(message))
        loop.create_task(game_client.get_update())

        for message in game_client.messages:
            if message.quit:
                local_player.game_client.quit_game()
                quit_game_to_menu = True
            local_player.health = message.enemyHealth
            if message.restart:
                # when message.restart is true, the id value will contain the winner
                scores[message.id] +=1
                local_player.reset()
                enemy_character.reset()

                break

            enemy_character.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, local_player, obstacles, message.keys,
                                       message.x, message.y)
            enemy_character.obstacle_collision(screen, obstacles)



        if quit_game_to_menu:
            break
        enemy_character.draw_projectile(local_player, screen.get_width(), screen)
        local_player.frameUpdate()
        enemy_character.frameUpdate()
        # draw fighters
        local_player.draw(screen,local_name,local_colour)
        enemy_character.draw(screen,enemy_name,RED)

        # draw obstacles
        for obstacle in obstacles:
            obstacle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                local_player.game_client.quit_game()

                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # if fighter 1 or 2 punches, play the punch.wav sound effect

        # update display
        pygame.display.update()
        run_once(loop)
    mixer.music.load(resource_path("game/assets/audio/background-game.wav"))
    mixer.music.play(-1)
    mixer.music.set_volume(background_music_volume)



# controls
def controls():
    leave_menu = False
    clock = pygame.time.Clock()

    # make player 1 controls with a button
    controls_player1 = Button(image=pygame.image.load(button_med), pos=(500, 175),
                                text_input="Player 1", font=font(35), base_color="#daf7d7", hovering_color="White")

    controls_player2 = Button(image=pygame.image.load(button_med), pos=(500, 325),
                                text_input="Player 2", font=font(35), base_color="#daf7d7", hovering_color="White")

    controls_back = Button(image=pygame.image.load(button_med), pos=(500, 475),
                            text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")


    while True:

        controls_mouse = pygame.mouse.get_pos()
        screen.blit(menu_scaled, (0, 0))

        controls_text = font(50).render("CONTROLS", True, "#b88d37")
        controls_rect = controls_text.get_rect(center=(500, 65))
        screen.blit(controls_text, controls_rect)


        for button in [controls_back, controls_player1, controls_player2]:
            button.hover(controls_mouse)
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
                if controls_back.check_for_input(controls_mouse):
                    leave_menu = True
                    break
                if controls_player1.check_for_input(controls_mouse):
                    player1()
                if controls_player2.check_for_input(controls_mouse):
                    player2()
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# fighter1 controls displayed and mutable
def player1():
    global player1_controls
    # player1_keys = {"left": "a", "right": "d", "jump": "w", "block": "s", "attack1": "r", "attack2": "t"}
    leave_menu = False
    clock = pygame.time.Clock()
    while True:

        player1_mouse = pygame.mouse.get_pos()

        screen.blit(menu_scaled, (0, 0))

        player1_text = font(50).render("PLAYER 1", True, "#b88d37")
        player1_rect = player1_text.get_rect(center=(500, 65))
        screen.blit(player1_text, player1_rect)

        # make player 1 controls with a button
        player1_up = Button(image=None, pos=(500, 150),
                            text_input="Jump : " + pygame.key.name(player1_controls["jump"]), font=font(15),
                            base_color="#daf7d7", hovering_color="White")

        player1_down = Button(image=None, pos=(500, 200),
                              text_input="Block : " + pygame.key.name(player1_controls["block"]),
                              font=font(15), base_color="#daf7d7", hovering_color="White")

        player1_left = Button(image=None, pos=(500, 250),
                              text_input="Left : " + pygame.key.name(player1_controls["left"]), font=font(15),
                              base_color="#daf7d7", hovering_color="White")

        player1_right = Button(image=None, pos=(500, 300),
                               text_input="Right : " + pygame.key.name(player1_controls["right"]),
                               font=font(15), base_color="#daf7d7", hovering_color="White")

        player1_attack1 = Button(image=None, pos=(500, 350),
                                 text_input="Attack1 : " + pygame.key.name(player1_controls["attack1"]),
                                 font=font(15), base_color="#daf7d7", hovering_color="White")

        player1_attack2 = Button(image=None, pos=(500, 400),
                                 text_input="Attack2 : " + pygame.key.name(player1_controls["attack2"]),
                                 font=font(15), base_color="#daf7d7", hovering_color="White")

        player1_back = Button(image=pygame.image.load(button_med), pos=(500, 475),
                              text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")

        for button in [player1_back, player1_up, player1_down, player1_left, player1_right, player1_attack1,
                       player1_attack2]:
            button.hover(player1_mouse)
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
                if player1_back.check_for_input(player1_mouse):
                    leave_menu = True
                    break
                if player1_up.check_for_input(player1_mouse):
                    control_handling(player1_controls, "jump")
                if player1_down.check_for_input(player1_mouse):
                    control_handling(player1_controls, "block")
                if player1_left.check_for_input(player1_mouse):
                    control_handling(player1_controls, "left")
                if player1_right.check_for_input(player1_mouse):
                    control_handling(player1_controls, "right")
                if player1_attack1.check_for_input(player1_mouse):
                    control_handling(player1_controls, "attack1")
                if player1_attack2.check_for_input(player1_mouse):
                    control_handling(player1_controls, "attack2")
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# fighter2 controls displayed and mutable
def player2():
    global player2_controls
    leave_menu = False
    clock = pygame.time.Clock()
    while True:
        player2_mouse = pygame.mouse.get_pos()

        screen.blit(menu_scaled, (0, 0))

        player2_text = font(50).render("PLAYER 2", True, "#b88d37")
        player2_rect = player2_text.get_rect(center=(500, 65))
        screen.blit(player2_text, player2_rect)

        # make player 2 controls with a button
        player2_up = Button(image=None, pos=(500, 150),
                            text_input="Jump : " + pygame.key.name(player2_controls["jump"]), font=font(15),
                            base_color="#daf7d7", hovering_color="White")

        player2_down = Button(image=None, pos=(500, 200),
                              text_input="Block : " + pygame.key.name(player2_controls["block"]),
                              font=font(15), base_color="#daf7d7", hovering_color="White")

        player2_left = Button(image=None, pos=(500, 250),
                              text_input="Left : " + pygame.key.name(player2_controls["left"]), font=font(15),
                              base_color="#daf7d7", hovering_color="White")

        player2_right = Button(image=None, pos=(500, 300),
                               text_input="Right : " + pygame.key.name(player2_controls["right"]),
                               font=font(15), base_color="#daf7d7", hovering_color="White")

        player2_attack1 = Button(image=None, pos=(500, 350),
                                 text_input="Attack1 : " + pygame.key.name(player2_controls["attack1"]),
                                 font=font(15), base_color="#daf7d7", hovering_color="White")

        player2_attack2 = Button(image=None, pos=(500, 400),
                                 text_input="Attack2 : " + pygame.key.name(player2_controls["attack2"]),
                                 font=font(15), base_color="#daf7d7", hovering_color="White")

        player2_back = Button(image=pygame.image.load(button_med), pos=(500, 475),
                              text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")

        for button in [player2_back, player2_up, player2_down, player2_left, player2_right, player2_attack1,
                       player2_attack2]:
            button.hover(player2_mouse)
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
                if player2_back.check_for_input(player2_mouse):
                    leave_menu = True
                    break
                if player2_up.check_for_input(player2_mouse):
                    control_handling(player2_controls, "jump")
                if player2_down.check_for_input(player2_mouse):
                    control_handling(player2_controls, "block")
                if player2_left.check_for_input(player2_mouse):
                    control_handling(player2_controls, "left")
                if player2_right.check_for_input(player2_mouse):
                    control_handling(player2_controls, "right")
                if player2_attack1.check_for_input(player2_mouse):
                    control_handling(player2_controls, "attack1")
                if player2_attack2.check_for_input(player2_mouse):
                    control_handling(player2_controls, "attack2")
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# options
def opt():
    leave_menu = False
    clock = pygame.time.Clock()


    opt_controls = Button(image=pygame.image.load(button_med), pos=(500, 175),
                            text_input="CONTROLS", font=font(35), base_color="#daf7d7", hovering_color="White")
    opt_audio = Button(image=pygame.image.load(button_med), pos=(500, 325),
                        text_input="AUDIO", font=font(35), base_color="#daf7d7", hovering_color="White")
    opt_back = Button(image=pygame.image.load(button_med), pos=(500, 475),
                        text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")

    while True:
        opt_mouse = pygame.mouse.get_pos()

        screen.blit(menu_scaled, (0, 0))

        opt_text = font(50).render("OPTIONS", True, "#b88d37")
        opt_rect = opt_text.get_rect(center=(500, 65))
        screen.blit(opt_text, opt_rect)

        opt_controls = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 175),
                              text_input="CONTROLS", font=font(35), base_color="#daf7d7", hovering_color="White")
        opt_audio = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 325),
                           text_input="AUDIO", font=font(35), base_color="#daf7d7", hovering_color="White")
        opt_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")

        for button in [opt_controls, opt_audio, opt_back]:
            button.hover(opt_mouse)
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
                if opt_back.check_for_input(opt_mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
                if opt_controls.check_for_input(opt_mouse):
                    pygame.display.set_caption("Controls")
                    controls()
                if opt_audio.check_for_input(opt_mouse):
                    pygame.display.set_caption("Audio")
                    audio()
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# create a function to handle audio levels using buttons for sound effects and music
def audio():
    leave_menu = False
    clock = pygame.time.Clock()
    global background_music_volume


    audio_back = Button(image=pygame.image.load(button_med), pos=(500, 475),
                        text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")
    # make 4 buttons for music volume, 1 for each quarter
    music_0 = Button(image=None, pos=(400, 175),
                        text_input="0%", font=font(25), base_color="#daf7d7", hovering_color="White")
    music_1 = Button(image=None, pos=(510, 175),
                        text_input="25%", font=font(25), base_color="#daf7d7", hovering_color="White")
    music_2 = Button(image=None, pos=(620, 175),
                        text_input="50%", font=font(25), base_color="#daf7d7", hovering_color="White")
    music_3 = Button(image=None, pos=(730, 175),
                        text_input="75%", font=font(25), base_color="#daf7d7", hovering_color="White")
    music_4 = Button(image=None, pos=(840, 175),
                        text_input="100%", font=font(25), base_color="#daf7d7", hovering_color="White")

    sfx_0 = Button(image=None, pos=(400, 325),
                    text_input="0%", font=font(25), base_color="#daf7d7", hovering_color="White")
    sfx_1 = Button(image=None, pos=(510, 325),
                    text_input="25%", font=font(25), base_color="#daf7d7", hovering_color="White")
    sfx_2 = Button(image=None, pos=(620, 325),
                    text_input="50%", font=font(25), base_color="#daf7d7", hovering_color="White")
    sfx_3 = Button(image=None, pos=(730, 325),
                    text_input="75%", font=font(25), base_color="#daf7d7", hovering_color="White")
    sfx_4 = Button(image=None, pos=(840, 325),
                    text_input="100%", font=font(25), base_color="#daf7d7", hovering_color="White")

    while True:
        audio_mouse = pygame.mouse.get_pos()
        screen.blit(menu_scaled, (0, 0))

        audio_text = font(50).render("AUDIO VOLUME", True, "#b88d37")
        audio_rect = audio_text.get_rect(center=(500, 65))
        screen.blit(audio_text, audio_rect)


        # create a button for music volume
        music_text = font(40).render("MUSIC", True, "#b88d37")
        music_rect = music_text.get_rect(center=(200, 175))
        screen.blit(music_text, music_rect)




        # create same buttons as music for sound effects
        sfx_text = font(40).render("SFX", True, "#b88d37")
        sfx_rect = sfx_text.get_rect(center=(200, 325))
        screen.blit(sfx_text, sfx_rect)


        for button in [audio_back, music_0, music_1, music_2, music_3, music_4, sfx_0, sfx_1, sfx_2, sfx_3, sfx_4]:
            button.hover(audio_mouse)
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
                if audio_back.check_for_input(audio_mouse):
                    pygame.display.set_caption("Options")
                    leave_menu = True
                    break
                if music_0.check_for_input(audio_mouse):
                    background_music_volume = 0
                    mixer.music.set_volume(background_music_volume)
                if music_1.check_for_input(audio_mouse):
                    background_music_volume = 0.25
                    mixer.music.set_volume(background_music_volume)
                if music_2.check_for_input(audio_mouse):
                    background_music_volume = 0.5
                    mixer.music.set_volume(background_music_volume)
                if music_3.check_for_input(audio_mouse):
                    background_music_volume = 0.75
                    mixer.music.set_volume(background_music_volume)
                if music_4.check_for_input(audio_mouse):
                    background_music_volume = 1
                    mixer.music.set_volume(background_music_volume)
                if sfx_0.check_for_input(audio_mouse):
                    sfx_change(0)
                if sfx_1.check_for_input(audio_mouse):
                    sfx_change(1)
                if sfx_2.check_for_input(audio_mouse):
                    sfx_change(2)
                if sfx_3.check_for_input(audio_mouse):
                    sfx_change(3)
                if sfx_4.check_for_input(audio_mouse):
                    sfx_change(4)
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


def multi_map_select(game_client):
    map = "mountain"
    leave_menu = False
    clock = pygame.time.Clock()

    #church map preview
    image1 = pygame.image.load(resource_path("game/assets/maps/church.png"))
    image1 = pygame.transform.scale(image1, (250, 125))
    #image_position = (100, 200)
    #mountain map preview
    image2 = pygame.image.load(resource_path("game/assets/maps/mountain.png"))
    image2 = pygame.transform.scale(image2, (250, 125))
    #image_position2 = (400, 200)
    #cliffs map preview
    image3 = pygame.image.load(resource_path("game/assets/maps/cliffs.png"))
    image3 = pygame.transform.scale(image3, (250, 125))

    locked_in = False
    loop = asyncio.get_event_loop()
    p_choice = 1
    locked_in = False
    BLACK = (0, 0, 0)
    while True:
        loop.create_task(game_client.get_map_choice())
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()
        if game_client.map_select_done:
            return True

        if not game_client.continue_map_select:
            game_client.socket.close()
            return False
        text = font(35).render("MAP SELECT", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)


        #church text
        text = font(25).render("Church", True, "White")
        rect = text.get_rect(center=(200, 180))
        screen.blit(text, rect)
        #mountain text
        text = font(25).render("Mountain", True, "White")
        rect = text.get_rect(center=(500, 180))
        screen.blit(text, rect)
        #cliffs text
        text = font(25).render("Cliffs", True, "White")
        rect = text.get_rect(center=(800, 180))
        screen.blit(text, rect)

        if map == "church":
            pygame.draw.rect(screen, WHITE, (72,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (72,235,256,131), width=3)
        if map == "mountain":
            pygame.draw.rect(screen, WHITE, (372,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (372,235,256,131), width=3)
        if map == "cliffs":
            pygame.draw.rect(screen, WHITE, (672,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (672,235,256,131), width=3)

        play = Button(image=pygame.image.load(button_med), pos=(700, 525),
                      text_input="PLAY", font=font(35), base_color="White", hovering_color="Yellow")
        #map select buttons
        map1 = Button(image=image1, pos=(200, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")
        map2 = Button(image=image2, pos=(500, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")
        map3 = Button(image=image3, pos=(800, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")

        back = Button(image=pygame.image.load(button_med), pos=(300, 525),
                      text_input="BACK", font=font(35), base_color="White", hovering_color="Yellow")

        for button in [back, play, map1, map2, map3]:
            button.hover(mouse)
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
                # make it so that when you click play, it goes to the game loop
                if play.check_for_input(mouse):
                    pygame.display.set_caption("Game")
                    locked_in = True
                if back.check_for_input(mouse):
                    pygame.display.set_caption("Map Select")
                    return False
                if map1.check_for_input(mouse):
                    p_choice = 0
                    map= "church"
                if map2.check_for_input(mouse):
                    p_choice = 1
                    map = "mountain"
                if map3.check_for_input(mouse):
                    p_choice = 2
                    map = "cliffs"

        game_client.send_map_choice(p_choice, locked_in)
        clock.tick(MENU_FPS)
        pygame.display.update()
        run_once(loop)


def multi_lobby_menu(game_client):
    leave_menu = False
    clock = pygame.time.Clock()

    lobby_code_input = pygame_textinput.TextInputVisualizer()
    name_input = pygame_textinput.TextInputVisualizer()
    locked_in = False
    loop = asyncio.get_event_loop()
    p_choice = 0
    locked_in = False
    lobby_searching = False
    lobby_in = False
    name_in = False
    lobby_pos = (500, 350)
    name_pos = (500, 200)


    lobby_code_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=lobby_pos,
                               text_input="lobby code", font=font(25), base_color="White", hovering_color="White")

    name_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=name_pos,
                         text_input="name", font=font(25), base_color="White", hovering_color="White")



    while True:
        events = pygame.event.get()
        if game_client.lobby_ready:
            return True

        if game_client.lobby_searching:

            loop.create_task(game_client.check_game_ready())

        screen.blit(menu_scaled, (0, 0))

        mouse = pygame.mouse.get_pos()

        text = font(35).render("Lobby Menu", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)


        text = font(15).render("Player Name", True, "#b88d37")
        rect = text.get_rect(center=(500, 125))
        screen.blit(text, rect)

        text = font(15).render("Lobby Code", True, "#b88d37")
        rect = text.get_rect(center=(500, 275))
        screen.blit(text, rect)

        play = Button(image=pygame.image.load(button_med), pos=(700, 525),
                      text_input="PLAY", font=font(35), base_color="White", hovering_color="Yellow")

        back = Button(image=pygame.image.load(button_med), pos=(300, 525),
                      text_input="BACK", font=font(35), base_color="White", hovering_color="Yellow")

        if lobby_in:
            lobby_code_input.update(events)


            if len(lobby_code_input.value) > 6:
                lobby_code_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=lobby_pos,
                            text_input=lobby_code_input.value[:13], font=font(25), base_color="White", hovering_color="White")
            else:
                lobby_code_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=lobby_pos,
                            text_input=lobby_code_input.value, font=font(35), base_color="White", hovering_color="White")

        if name_in:
            name_input.update(events)
            if len(name_input.value) > 6:
                name_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=name_pos,
                            text_input=name_input.value[:13], font=font(25), base_color="White", hovering_color="White")
            else:
                name_button = Button(image=pygame.image.load(resource_path("game/assets/menu/small.png")), pos=name_pos,
                            text_input=name_input.value, font=font(35), base_color="White", hovering_color="White")

        for button in [back, play, name_button, lobby_code_button]:
            button.hover(mouse)
            button.update(screen)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # make it so that when you click play, it goes to the game loop
                if play.check_for_input(mouse):
                    pygame.display.set_caption("Game")
                    if game_client.lobby_searching:
                        continue
                    game_client.lobby_searching = True
                    game_client.player_name = name_input.value
                    loop.create_task(game_client.join_lobby("176.61.91.52", 1234,
                                                            lobby_code_input.value,name_input.value))

                if back.check_for_input(mouse):
                    pygame.display.set_caption("Map Select")
                    return False
                if lobby_code_button.check_for_input(mouse):
                    lobby_in = True
                    name_in = False
                if name_button.check_for_input(mouse):
                    #check if backspace was clicked, if yes, delete last character from name_input.value
                    lobby_in = False
                    name_in = True

        clock.tick(MENU_FPS)
        pygame.display.update()
        run_once(loop)


# new menu for when you click play, it should have a "local multiplayer" and a "singleplayer" button
def menu_play():

    single_player = Button(image=pygame.image.load(button_long), pos=(500, 150),
                           text_input="SINGLEPLAYER", font=font(35), base_color="#daf7d7", hovering_color="White")

    local = Button(image=pygame.image.load(button_long), pos=(500, 275),
                   text_input="LOCAL", font=font(35), base_color="#daf7d7", hovering_color="White")

    multiplayer = Button(image=pygame.image.load(button_long), pos=(500, 400),
                         text_input="MULTIPLAYER", font=font(35), base_color="#daf7d7", hovering_color="White")

    back = Button(image=pygame.image.load(button_med), pos=(500, 525),
                  text_input="BACK", font=font(35), base_color="#daf7d7", hovering_color="White")
    leave_menu = False

    clock = pygame.time.Clock()

    while True:

        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(70).render("GAME MODE", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        for button in [single_player, local, multiplayer, back]:
            button.hover(mouse)
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
                if single_player.check_for_input(mouse):
                    pygame.display.set_caption("Single Player")
                    menu_char("Single Player")
                if local.check_for_input(mouse):
                    pygame.display.set_caption("Local Multiplayer")
                    menu_char("Local")
                if multiplayer.check_for_input(mouse):
                    pygame.display.set_caption("Multi Player Menu")
                    game_client = GameClient(1234)
                    game_client.socket.setblocking(False)
                    if not multi_lobby_menu(game_client):
                        game_client.socket.close()
                        return
                    time.sleep(2)

                    game_client.join_game("176.61.91.52", game_client.game_port, game_client.player_name)

                    # print("connecting to server")
                    # game_client.connect("192.168.0.33", 1234, "m")
                    # print(game_client.player_id)
                    # game_client.socket.setblocking(False)
                    multi_char_select(game_client)
                    if not multi_map_select(game_client):
                        break
                    mixer.music.load(resource_path("game/assets/audio/background-game.wav"))
                    mixer.music.play(-1)
                    mixer.music.set_volume(background_music_volume)
                    multi_player_game_loop(game_client)
                    mixer.music.load(resource_path("game/assets/audio/background-menu.wav"))
                    mixer.music.play(-1)
                    mixer.music.set_volume(background_music_volume)
                if back.check_for_input(mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


#character select menu
def menu_char(mode):
    global p1
    global p2

    p1_color_wizard = "#daf7d7"
    p1_color_warrior = "#daf7d7"
    p1_color_nomad = "#daf7d7"

    p2_color_wizard = "#daf7d7"
    p2_color_warrior = "#daf7d7"
    p2_color_nomad = "#daf7d7"

    # draw player 1 characters
    wizard1 = createWizard(Fighter, 1, 285, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    nomad1 = createNomad(Fighter, 1, 275, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    warrior1 = createWarrior(Fighter, 1, 265, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)

    # draw player 2 characters
    wizard2 = createWizard(Fighter, 1, 685, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    nomad2 = createNomad(Fighter, 1, 675, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    warrior2 = createWarrior(Fighter, 1, 665, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)


    leave_menu = False
    clock = pygame.time.Clock()

    play = Button(image=pygame.image.load(button_med), pos=(700, 525),
                    text_input="PLAY", font=font(35), base_color="Black", hovering_color="Yellow")

    #character select buttons for player 1
    p1_wizard = Button(image=None, pos=(175, 350),
                    text_input="wizard", font=font(16), base_color=p1_color_wizard, hovering_color="Yellow")
    p1_warrior = Button(image=None, pos=(300, 350),
                    text_input="warrior", font=font(16), base_color=p1_color_warrior, hovering_color="Yellow")
    p1_nomad = Button(image=None, pos=(425, 350),
                    text_input="nomad", font=font(16), base_color=p1_color_nomad, hovering_color="Yellow")

    #character select buttons for player 2
    p2_wizard = Button(image=None, pos=(575, 350),
                    text_input="wizard", font=font(16), base_color=p2_color_wizard, hovering_color="Blue")
    p2_warrior = Button(image=None, pos=(700, 350),
                    text_input="warrior", font=font(16), base_color=p2_color_warrior, hovering_color="Blue")
    p2_nomad = Button(image=None, pos=(825, 350),
                    text_input="nomad", font=font(16), base_color=p2_color_nomad, hovering_color="Blue")

    back = Button(image=pygame.image.load(button_med), pos=(300, 525),
                    text_input="BACK", font=font(35), base_color="Black", hovering_color="Yellow")


    while True:

        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(35).render("CHARACTER SELECT", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        # draw wizard
        if p1 == "wizard":
            wizard1.frameUpdate()
            wizard1.draw(screen, "", RED)
        # draw warrior
        if p1 == "warrior":
            warrior1.frameUpdate()
            warrior1.draw(screen, "", RED)
        # draw nomad
        if p1 == "nomad":
            nomad1.frameUpdate()
            nomad1.draw(screen, "", RED)

        # draw wizard
        if p2 == "wizard":
            wizard2.frameUpdate()
            wizard2.draw(screen, "", RED)
        # draw warrior
        if p2 == "warrior":
            warrior2.frameUpdate()
            warrior2.draw(screen, "", RED)
        # draw nomad
        if p2 == "nomad":
            nomad2.frameUpdate()
            nomad2.draw(screen, "", RED)

            # player 1
        text = font(15).render("PLAYER 1", True, "#b88d37")
        rect = text.get_rect(center=(300, 125))
        screen.blit(text, rect)

        # player 2
        text = font(15).render("PLAYER 2", True, "#b88d37")
        rect = text.get_rect(center=(700, 125))
        screen.blit(text, rect)


        for button in [back, play, p1_wizard, p1_warrior, p1_nomad, p2_wizard, p2_warrior, p2_nomad]:
            button.hover(mouse)
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
                # make it so that when you click play, it goes to the game loop
                if play.check_for_input(mouse):
                    pygame.display.set_caption("Map Select")
                    map_select(mode)
                if back.check_for_input(mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
                if p1_wizard.check_for_input(mouse):
                    p1_color_warrior = "#daf7d7"
                    p1_color_wizard = "Yellow"
                    p1_color_nomad = "#daf7d7"
                    p1 = "wizard"
                if p1_warrior.check_for_input(mouse):
                    p1_color_warrior = "Yellow"
                    p1_color_wizard = "#daf7d7"
                    p1_color_nomad = "#daf7d7"
                    p1 = "warrior"
                if p1_nomad.check_for_input(mouse):
                    p1_color_nomad = "Yellow"
                    p1_color_wizard = "#daf7d7"
                    p1_color_warrior = "#daf7d7"
                    p1 = "nomad"
                if p2_wizard.check_for_input(mouse):
                    p2_color_wizard = "Blue"
                    p2_color_warrior = "#daf7d7"
                    p2_color_nomad = "#daf7d7"
                    p2 = "wizard"
                if p2_warrior.check_for_input(mouse):
                    p2_color_warrior = "Blue"
                    p2_color_nomad = "#daf7d7"
                    p2_color_wizard = "#daf7d7"
                    p2 = "warrior"
                if p2_nomad.check_for_input(mouse):
                    p2_color_nomad = "Blue"
                    p2_color_wizard = "#daf7d7"
                    p2_color_warrior = "#daf7d7"
                    p2 = "nomad"

        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


#create a map select screen
def map_select(mode):
    global map
    leave_menu = False
    clock = pygame.time.Clock()
    mode=mode
    #church map preview
    image1 = pygame.image.load(resource_path("game/assets/maps/church.png"))
    image1 = pygame.transform.scale(image1, (250, 125))
    #image_position = (100, 200)
    #mountain map preview
    image2 = pygame.image.load(resource_path("game/assets/maps/mountain.png"))
    image2 = pygame.transform.scale(image2, (250, 125))
    #image_position2 = (400, 200)
    #cliffs map preview
    image3 = pygame.image.load(resource_path("game/assets/maps/cliffs.png"))
    image3 = pygame.transform.scale(image3, (250, 125))
    #image_position3 = (700, 200)

    BLACK = (0, 0, 0)

    while True:
        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(35).render("MAP SELECT", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        #church text
        text = font(25).render("Church", True, "White")
        rect = text.get_rect(center=(200, 180))
        screen.blit(text, rect)
        #mountain text
        text = font(25).render("Mountain", True, "White")
        rect = text.get_rect(center=(500, 180))
        screen.blit(text, rect)
        #cliffs text
        text = font(25).render("Cliffs", True, "White")
        rect = text.get_rect(center=(800, 180))
        screen.blit(text, rect)

        if map == "church":
            pygame.draw.rect(screen, WHITE, (72,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (72,235,256,131), width=3)
        if map == "mountain":
            pygame.draw.rect(screen, WHITE, (372,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (372,235,256,131), width=3)
        if map == "cliffs":
            pygame.draw.rect(screen, WHITE, (672,235,256,131), width=3)
        else:
            pygame.draw.rect(screen, BLACK, (672,235,256,131), width=3)

        play = Button(image=pygame.image.load(button_med), pos=(700, 525),
                        text_input="PLAY", font=font(35), base_color="White", hovering_color="Yellow")
        #map select buttons
        map1 = Button(image=image1, pos=(200, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")
        map2 = Button(image=image2, pos=(500, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")
        map3 = Button(image=image3, pos=(800, 300),
                        text_input="", font=font(25), base_color="#daf7d7", hovering_color="Yellow")

        back = Button(image=pygame.image.load(button_med), pos=(300, 525),
                      text_input="BACK", font=font(35), base_color="White", hovering_color="Yellow")

        for button in [back, play, map1, map2, map3]:
            button.hover(mouse)
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
                # make it so that when you click play, it goes to the game loop
                if play.check_for_input(mouse):
                    pygame.display.set_caption("Game")
                    mixer.music.load(resource_path("game/assets/audio/background-game.wav"))
                    mixer.music.play(-1)
                    mixer.music.set_volume(background_music_volume)
                    if mode == "Single Player":
                        single_game_loop()
                    else:
                        game_loop()

                if back.check_for_input(mouse):
                    pygame.display.set_caption("Character Select")
                    leave_menu = True
                    break
                if map1.check_for_input(mouse):
                    map = "church"
                if map2.check_for_input(mouse):
                    map = "mountain"
                if map3.check_for_input(mouse):
                    map = "cliffs"
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


def multi_char_select(game_client):
    global p1, p2
    default_colour = "#daf7d7"
    p2_wiz = "#daf7d7"
    p2_war = "#daf7d7"
    p2_nom = "#daf7d7"

    #draw player 1 characters
    wizard1 = createWizard(Fighter, 1, 285, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    nomad1 = createNomad(Fighter, 1, 275, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    warrior1 = createWarrior(Fighter, 1, 265, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)


    #draw player 2 characters
    wizard2 = createWizard(Fighter, 1, 685, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    nomad2 = createNomad(Fighter, 1, 675, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)
    warrior2 = createWarrior(Fighter, 1, 665, 175, False, punch_fx, projectile_fx, hit_fx, player1_controls)

    p1_color_wizard = "#daf7d7"
    p2_color_wizard = "Blue"

    p1_color_warrior = "#daf7d7"
    p1_color_nomad = "Yellow"

    play = Button(image=pygame.image.load(button_med), pos=(700, 525),
                  text_input="PLAY", font=font(35), base_color="Black", hovering_color="Yellow")
    # character select buttons for player 1
    p1_wizard = Button(image=None, pos=(175, 350),
                       text_input="wizard", font=font(16), base_color=p1_color_wizard, hovering_color="Yellow")
    p1_warrior = Button(image=None, pos=(300, 350),
                        text_input="warrior", font=font(16), base_color=p1_color_warrior, hovering_color="Yellow")
    p1_nomad = Button(image=None, pos=(425, 350),
                      text_input="nomad", font=font(16), base_color=p1_color_nomad, hovering_color="Yellow")

    back = Button(image=pygame.image.load(button_med), pos=(300, 525),
                  text_input="BACK", font=font(35), base_color="Black", hovering_color="Yellow")

    characters = [p1_nomad, p1_wizard, p1_warrior]

    p_choice = 0
    locked_in = False
    loop = asyncio.get_event_loop()
    l_count = 0
    clock = pygame.time.Clock()
    enemy_choice = wizard2
    p1 = "nomad"
    p2 = "wizard"

    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(menu_scaled, (0, 0))
        if game_client.enemy_quit_game == 0:
            try:
                game_client.socket.close()
            except:
                pass

            break
            # draw wizard
        if p1 == "wizard":
            wizard1.frameUpdate()
            wizard1.draw(screen, "", RED)
            # draw warrior
        elif p1 == "warrior":
            warrior1.frameUpdate()
            warrior1.draw(screen, "", RED)
        # draw nomad
        elif p1 == "nomad":
            nomad1.frameUpdate()
            nomad1.draw(screen, "", RED)

        for button in [back, play, p1_wizard, p1_warrior, p1_nomad]:
            button.hover(mouse)
            button.update(screen)
            # character select buttons for player 2
        p2_wizard = Button(image=None, pos=(575, 350),
                        text_input="wizard", font=font(16), base_color=p2_wiz, hovering_color="Blue")
        p2_warrior = Button(image=None, pos=(700, 350),
                        text_input="warrior", font=font(16), base_color=p2_war, hovering_color="Blue")
        p2_nomad = Button(image=None, pos=(825, 350),
                        text_input="nomad", font=font(16), base_color=p2_nom, hovering_color="Blue")
        enemy_chars = [p2_nomad, p2_wizard, p2_warrior]
        loop.create_task(game_client.get_enemy_character())

        if game_client.enemy_resp is not None:
            if game_client.enemy_char == 0:
                p2_nom = "Blue"
                p2_wiz = default_colour
                p2_war = default_colour
                enemy_choice = nomad2
            elif game_client.enemy_char == 1:
                p2_wiz = "Blue"
                p2_nom = default_colour
                p2_war = default_colour
                enemy_choice = wizard2
            else:
                p2_war = "Blue"
                p2_wiz = default_colour
                p2_nom = default_colour
                enemy_choice= warrior2
            if game_client.enemy_resp.start:

                break

            game_client.enemy_resp = None

        enemy_choice.frameUpdate()
        enemy_choice.draw(screen,"",RED)
        for button in enemy_chars:
            button.update(screen)

        text = font(35).render("CHARACTER SELECT", True, "#b88d37")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        # player 1
        text = font(15).render("YOUR PICK", True, "#b88d37")
        rect = text.get_rect(center=(300, 100))
        screen.blit(text, rect)

        # player 2
        text = font(15).render("ENEMY PICK", True, "#b88d37")
        rect = text.get_rect(center=(700, 100))
        screen.blit(text, rect)
        if l_count == 0:
            game_client.send_character_choice(p_choice, locked_in)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # make it so that when you click play, it goes to the game loop
                if play.check_for_input(mouse):
                    locked_in = True

                    game_client.local_char = p_choice
                    # pygame.display.set_caption("Game")

                if back.check_for_input(mouse):
                    pygame.display.set_caption("Main Menu")
                    main_menu()
                if locked_in:
                    continue
                for i, button in enumerate(characters):
                    if button.check_for_input(mouse):
                        game_client.send_character_choice(i, False)
                        button.base_color = "Yellow"
                        p_choice = i
                        p1 = button.text_input
                        for j in [z for z in range(0, 3) if z != i]:
                            characters[j].base_color = default_colour

        l_count = (l_count + 1) % 20
        pygame.display.update()
        run_once(loop)
        clock.tick(MENU_FPS)


async def update_lobby(game_client):
    loop = asyncio.get_event_loop()
    loop.create_task(game_client.get_enemy_character())


# main menu
def main_menu():
    play = Button(image=pygame.image.load(button_long), pos=(500, 180),
                  text_input="PLAY", font=font(55), base_color="#daf7d7", hovering_color="White")

    options = Button(image=pygame.image.load(button_long), pos=(500, 325),
                     text_input="OPTIONS", font=font(55), base_color="#daf7d7", hovering_color="White")

    quit = Button(image=pygame.image.load(button_med), pos=(500, 470),
                  text_input="QUIT", font=font(55), base_color="#daf7d7", hovering_color="White")

    text = font(75).render("Main Menu", True, "#b88d37")
    rect = text.get_rect(center=(500, 50))
    clock = pygame.time.Clock()

    screen.blit(menu_scaled, (0, 0))

    while True:
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        screen.blit(text, rect)

        for button in [play, options, quit]:
            button.hover(mouse)
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
                if play.check_for_input(mouse):
                    pygame.display.set_caption("Game Mode")
                    menu_play()
                if options.check_for_input(mouse):
                    pygame.display.set_caption("Options")
                    opt()
                if quit.check_for_input(mouse):
                    pygame.quit()
                    sys.exit()
        clock.tick(MENU_FPS)
        pygame.display.update()


# https://stackoverflow.com/a/51266275
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    map = ""
    p1 = ""
    p2 = ""
    player1_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "attack1": pygame.K_r,
                        "attack2": pygame.K_t, "block": pygame.K_s}

    player2_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP,
                        "attack1": pygame.K_n, "attack2": pygame.K_m, "block": pygame.K_DOWN}

    mixer.init
    pygame.init()
    # create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    # default characters
    p1 = "wizard"
    p2 = "wizard"

    # default map
    map = "mountain"
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    # cap frame rate
    clock = pygame.time.Clock()
    MENU_FPS = 45
    GAME_FPS = 60

    # define colors
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # load bg images
    bg_image = pygame.image.load(resource_path("game/assets/maps/background.png")).convert_alpha()
    menu_bg = pygame.image.load(resource_path("game/assets/menu/main_menu_bg.png")).convert_alpha()

    # use mixer to load music and sounds
    background_music_volume = 0.5
    mixer.music.load(resource_path("game/assets/audio/background-menu.wav"))
    mixer.music.play(-1)
    mixer.music.set_volume(background_music_volume)

    punch_fx = mixer.Sound(resource_path("game/assets/audio/punch.wav"))
    projectile_fx = mixer.Sound(resource_path("game/assets/audio/proj.wav"))
    hit_fx = mixer.Sound(resource_path("game/assets/audio/hit.wav"))
    punch_fx.set_volume(0.15)
    projectile_fx.set_volume(0.5)
    hit_fx.set_volume(0.5)

    obstacles = []

    # load buttons
    button_long = resource_path("game/assets/menu/long.png")
    button_med = resource_path("game/assets/menu/medium.png")

    #scale the menu background to fit the screen resolution
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


    main_menu()
