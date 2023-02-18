import pygame, asyncio
from pygame import mixer
from game.fighter import Fighter
from game.online_fighter import OnlineFighter
from game.characters.nomad import createNomad
from game.characters.warrior import createWarrior
from game.characters.wizard import createWizard
from game.obstacle import Obstacle
from game.button import Button
from game.network.game_client import GameClient
import sys,os


def draw_bg(scaled_bg_image):

    screen.blit(scaled_bg_image, (0, 0))


# draw health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 3, y - 3, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# font size
def font(size):
    return pygame.font.Font(resource_path("game/assets/menu/font.ttf"), size)


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


# game loop
def game_loop():
    if map == "mountain":
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

    elif map == "church":
        p1_spawn = [80, 100]
        p2_spawn = [900, 100]
        map_chosen = "game/assets/maps/church.png"
        # church obstacles
        middle_floor = Obstacle(150, 530, 700, 80)
        left_side = Obstacle(0, 387, 142, 160)
        right_side = Obstacle(860, 387, 142, 160)
        middle_top = Obstacle(235, 240, 525, 40)

        obstacles = [middle_floor, left_side, right_side, middle_top]

    elif map == "cliffs":
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

        obstacles = [left_island1, left_island2, middle_island1, middle_island2, right_cliff1, right_cliff2, right_cliff3, right_cliff4, right_cliff5, right_cliff6]

    if p1 == "wizard":
        fighter_1 = createWizard(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)

    elif p1 == "nomad":
        fighter_1 = createNomad(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)

    elif p1 == "warrior":
        fighter_1 = createWarrior(Fighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)

    if p2 == "wizard":
        fighter_2 = createWizard(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx, player2_controls)

    elif p2 == "nomad":
        fighter_2 = createNomad(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx, player2_controls)

    elif p2 == "warrior":
        fighter_2 = createWarrior(Fighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx, player2_controls)


    #load map
    bg_image = pygame.image.load(resource_path(map_chosen)).convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    run = True
    scores = [0,0]
    while run:

        # cap frame rate
        clock.tick(GAME_FPS)

        # draw background
        draw_bg(scaled_bg)

        # draw health bars
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)

        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, obstacles)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, obstacles)

        if fighter_1.health <=0 or fighter_2.health <=0:
            if fighter_1.health <=0:
                scores[1] +=1
            else:
                scores[0] +=1

            if scores[0] ==3 or scores[1]==3:
                break

            fighter_1.reset()
            fighter_2.reset()



        # update frames
        fighter_1.frameUpdate()
        fighter_2.frameUpdate()

        # draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)



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

        # update display
        pygame.display.update()

async def update_enemy(game_client,local_player,enemy_character):
    for message in game_client.get_updates():
        local_player.health = message.enemyHealth
        enemy_character.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, local_player, obstacles,

                                   message.keys, message.x, message.y)
def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()

def multi_player_game_loop(game_client):
    #gameKeys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t]
    pygame.init()

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

    pygame.display.set_caption("Team 5 Project")
    char_dict = {0: createNomad, 1: createWizard, 2: createWarrior}
    if game_client.player_id == 0:
    # create fighters
        f1 = char_dict[game_client.local_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx,player1_controls)
        f2 = char_dict[game_client.enemy_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx,player1_controls)
    else:
        f1 = char_dict[game_client.enemy_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, punch_fx, projectile_fx, hit_fx, player1_controls)
        f2 = char_dict[game_client.local_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, punch_fx, projectile_fx, hit_fx, player1_controls)

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
    while run:

        # cap frame rate
        clock.tick(GAME_FPS)

        # draw background
        draw_bg(scaled_bg)

        # draw health bars
        draw_health_bar(fighters[0].health, 20, 20)
        draw_health_bar(fighters[1].health, 580, 20)

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
                local_player.reset()
                enemy_character.reset()

                break

            enemy_character.move_enemy(SCREEN_WIDTH,SCREEN_HEIGHT,screen,local_player,obstacles,message.keys,message.x,message.y)
            enemy_character.obstacle_collision(screen, obstacles)
        if quit_game_to_menu:
            break
        enemy_character.draw_projectile(local_player,screen.get_width(),screen)
        local_player.frameUpdate()
        enemy_character.frameUpdate()
        # draw fighters
        local_player.draw(screen)
        enemy_character.draw(screen)



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



# controls
def controls():
    leave_menu = False
    clock = pygame.time.Clock()
    while True:

        controls_mouse = pygame.mouse.get_pos()

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        controls_text = font(50).render("CONTROLS", True, "#b68f40")
        controls_rect = controls_text.get_rect(center=(500, 65))
        screen.blit(controls_text, controls_rect)

        # make player 1 controls with a button
        controls_player1 = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 175),
                                  text_input="Player 1", font=font(35), base_color="#d7fcd4", hovering_color="White")

        controls_player2 = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 325),
                                  text_input="Player 2", font=font(35), base_color="#d7fcd4", hovering_color="White")

        controls_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                               text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

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
                if controls_back.checkForInput(controls_mouse):
                    leave_menu = True
                    break
                if controls_player1.checkForInput(controls_mouse):
                    player1()
                if controls_player2.checkForInput(controls_mouse):
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

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        player1_text = font(50).render("PLAYER 1", True, "#b68f40")
        player1_rect = player1_text.get_rect(center=(500, 65))
        screen.blit(player1_text, player1_rect)

        # make player 1 controls with a button
        player1_up = Button(image=None, pos=(500, 150),
                            text_input="Jump : " + pygame.key.name(player1_controls["jump"]), font=font(15),
                            base_color="#d7fcd4", hovering_color="White")

        player1_down = Button(image=None, pos=(500, 200),
                              text_input="Block : " + pygame.key.name(player1_controls["block"]),
                              font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_left = Button(image=None, pos=(500, 250),
                              text_input="Left : " + pygame.key.name(player1_controls["left"]), font=font(15),
                              base_color="#d7fcd4", hovering_color="White")

        player1_right = Button(image=None, pos=(500, 300),
                               text_input="Right : " + pygame.key.name(player1_controls["right"]),
                               font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_attack1 = Button(image=None, pos=(500, 350),
                                 text_input="Punch : " + pygame.key.name(player1_controls["attack1"]),
                                 font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_attack2 = Button(image=None, pos=(500, 400),
                                 text_input="Projectile : " + pygame.key.name(player1_controls["attack2"]),
                                 font=font(15), base_color="#d7fcd4", hovering_color="White")

        player1_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                              text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

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
                if player1_back.checkForInput(player1_mouse):
                    leave_menu = True
                    break
                if player1_up.checkForInput(player1_mouse):
                    control_handling(player1_controls, "jump")
                if player1_down.checkForInput(player1_mouse):
                    control_handling(player1_controls, "block")
                if player1_left.checkForInput(player1_mouse):
                    control_handling(player1_controls, "left")
                if player1_right.checkForInput(player1_mouse):
                    control_handling(player1_controls, "right")
                if player1_attack1.checkForInput(player1_mouse):
                    control_handling(player1_controls, "attack1")
                if player1_attack2.checkForInput(player1_mouse):
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

        menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(menu_scaled, (0, 0))

        player2_text = font(50).render("PLAYER 2", True, "#b68f40")
        player2_rect = player2_text.get_rect(center=(500, 65))
        screen.blit(player2_text, player2_rect)

        # make player 2 controls with a button
        player2_up = Button(image=None, pos=(500, 150),
                            text_input="Jump : " + pygame.key.name(player2_controls["jump"]), font=font(15),
                            base_color="#d7fcd4", hovering_color="White")

        player2_down = Button(image=None, pos=(500, 200),
                              text_input="Block : " + pygame.key.name(player2_controls["block"]),
                              font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_left = Button(image=None, pos=(500, 250),
                              text_input="Left : " + pygame.key.name(player2_controls["left"]), font=font(15),
                              base_color="#d7fcd4", hovering_color="White")

        player2_right = Button(image=None, pos=(500, 300),
                               text_input="Right : " + pygame.key.name(player2_controls["right"]),
                               font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_attack1 = Button(image=None, pos=(500, 350),
                                 text_input="Punch : " + pygame.key.name(player2_controls["attack1"]),
                                 font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_attack2 = Button(image=None, pos=(500, 400),
                                 text_input="Projectile : " + pygame.key.name(player2_controls["attack2"]),
                                 font=font(15), base_color="#d7fcd4", hovering_color="White")

        player2_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                              text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

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
                if player2_back.checkForInput(player2_mouse):
                    leave_menu = True
                    break
                if player2_up.checkForInput(player2_mouse):
                    control_handling(player2_controls, "jump")
                if player2_down.checkForInput(player2_mouse):
                    control_handling(player2_controls, "block")
                if player2_left.checkForInput(player2_mouse):
                    control_handling(player2_controls, "left")
                if player2_right.checkForInput(player2_mouse):
                    control_handling(player2_controls, "right")
                if player2_attack1.checkForInput(player2_mouse):
                    control_handling(player2_controls, "attack1")
                if player2_attack2.checkForInput(player2_mouse):
                    control_handling(player2_controls, "attack2")
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# options
def opt():
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    leave_menu = False
    clock = pygame.time.Clock()
    while True:
        opt_mouse = pygame.mouse.get_pos()


        screen.blit(menu_scaled, (0, 0))

        opt_text = font(50).render("OPTIONS", True, "#b68f40")
        opt_rect = opt_text.get_rect(center=(500, 65))
        screen.blit(opt_text, opt_rect)

        opt_controls = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 175),
                              text_input="CONTROLS", font=font(35), base_color="#d7fcd4", hovering_color="White")
        opt_audio = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 325),
                           text_input="AUDIO", font=font(35), base_color="#d7fcd4", hovering_color="White")
        opt_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                          text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

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
                if opt_back.checkForInput(opt_mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
                if opt_controls.checkForInput(opt_mouse):
                    pygame.display.set_caption("Controls")
                    controls()
                if opt_audio.checkForInput(opt_mouse):
                    pygame.display.set_caption("Audio")
                    audio()
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


# create a function to handle audio levels using buttons for sound effects and music
def audio():
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    leave_menu = False
    clock = pygame.time.Clock()
    while True:
        audio_mouse = pygame.mouse.get_pos()
        screen.blit(menu_scaled, (0, 0))

        audio_text = font(50).render("AUDIO VOLUME", True, "#b68f40")
        audio_rect = audio_text.get_rect(center=(500, 65))
        screen.blit(audio_text, audio_rect)
        music_text = font(40).render("MUSIC", True, "#b68f40")
        music_rect = music_text.get_rect(center=(200, 175))
        screen.blit(music_text, music_rect)
        audio_back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 475),
                            text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")
        # make 4 buttons for music volume, 1 for each quarter
        music_0 = Button(image=None, pos=(400, 175),
                         text_input="0%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        music_1 = Button(image=None, pos=(510, 175),
                         text_input="25%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        music_2 = Button(image=None, pos=(620, 175),
                         text_input="50%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        music_3 = Button(image=None, pos=(730, 175),
                         text_input="75%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        music_4 = Button(image=None, pos=(840, 175),
                         text_input="100%", font=font(25), base_color="#d7fcd4", hovering_color="White")

        # create same buttons as music for sound effects
        sfx_text = font(40).render("SFX", True, "#b68f40")
        sfx_rect = sfx_text.get_rect(center=(200, 325))
        screen.blit(sfx_text, sfx_rect)
        sfx_0 = Button(image=None, pos=(400, 325),
                       text_input="0%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        sfx_1 = Button(image=None, pos=(510, 325),
                       text_input="25%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        sfx_2 = Button(image=None, pos=(620, 325),
                       text_input="50%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        sfx_3 = Button(image=None, pos=(730, 325),
                       text_input="75%", font=font(25), base_color="#d7fcd4", hovering_color="White")
        sfx_4 = Button(image=None, pos=(840, 325),
                       text_input="100%", font=font(25), base_color="#d7fcd4", hovering_color="White")

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
                if audio_back.checkForInput(audio_mouse):
                    pygame.display.set_caption("Options")
                    leave_menu = True
                    break
                if music_0.checkForInput(audio_mouse):
                    mixer.music.set_volume(0)
                if music_1.checkForInput(audio_mouse):
                    mixer.music.set_volume(0.25)
                if music_2.checkForInput(audio_mouse):
                    mixer.music.set_volume(0.5)
                if music_3.checkForInput(audio_mouse):
                    mixer.music.set_volume(0.75)
                if music_4.checkForInput(audio_mouse):
                    mixer.music.set_volume(1)
                if sfx_0.checkForInput(audio_mouse):
                    sfx_change(0)
                if sfx_1.checkForInput(audio_mouse):
                    sfx_change(1)
                if sfx_2.checkForInput(audio_mouse):
                    sfx_change(2)
                if sfx_3.checkForInput(audio_mouse):
                    sfx_change(3)
                if sfx_4.checkForInput(audio_mouse):
                    sfx_change(4)
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()

def multi_map_select(game_client):
    leave_menu = False
    clock = pygame.time.Clock()
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    p_choice = 0
    locked_in = False
    loop = asyncio.get_event_loop()
    map_choice = 0
    locked_in = False
    while True:
        loop.create_task(game_client.get_map_choice())
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()
        if game_client.map_select_done:
            break




        text = font(35).render("MAP SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        play = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(700, 525),
                      text_input="PLAY", font=font(35), base_color="White", hovering_color="Yellow")
        # map select buttons
        map1 = Button(image=None, pos=(300, 150),
                      text_input="map1", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map2 = Button(image=None, pos=(500, 150),
                      text_input="map2", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map3 = Button(image=None, pos=(700, 150),
                      text_input="map3", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")

        back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(300, 525),
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
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Game")
                    locked_in = True
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Map Select")
                    leave_menu = True
                    break
                if map1.checkForInput(mouse):
                    p_choice=0
                if map2.checkForInput(mouse):
                    p_choice = 1
                if map3.checkForInput(mouse):
                    p_choice = 2
        if leave_menu:
            break

        game_client.send_map_choice(map_choice, locked_in)
        clock.tick(MENU_FPS)
        pygame.display.update()
        run_once(loop)

#new menu for when you click play, it should have a "local multiplayer" and a "singleplayer" button
def menu_play():
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    single_player = Button(image=pygame.image.load(resource_path("game/assets/menu/long.png")), pos=(500, 150),
                           text_input="SINGLEPLAYER", font=font(35), base_color="#d7fcd4", hovering_color="White")

    local = Button(image=pygame.image.load(resource_path("game/assets/menu/long.png")), pos=(500, 275),
                   text_input="LOCAL MULTI", font=font(35), base_color="#d7fcd4", hovering_color="White")

    multiplayer = Button(image=pygame.image.load(resource_path("game/assets/menu/long.png")), pos=(500, 400),
                         text_input="MULTIPLAYER", font=font(35), base_color="#d7fcd4", hovering_color="White")

    back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 525),
                  text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")
    leave_menu = False
    clock = pygame.time.Clock()
    while True:

        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(70).render("GAME MODE", True, "#b68f40")
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
                if single_player.checkForInput(mouse):
                    pygame.display.set_caption("Single Player")
                    menu_char()
                if local.checkForInput(mouse):
                    pygame.display.set_caption("Local Multiplayer")
                    menu_char()
                if multiplayer.checkForInput(mouse):
                    pygame.display.set_caption("Multi Player Menu")
                    game_client = GameClient(1234)
                    print("connecting to server")
                    game_client.connect("192.168.0.33", 1234, "m")
                    print(game_client.player_id)
                    game_client.socket.setblocking(False)
                    multi_char_select(game_client)
                    multi_map_select(game_client)
                    multi_player_game_loop(game_client)
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()

#character select menu
def menu_char():
    global p1
    global p2

    p1_color_wizard= "#d7fcd4"
    p1_color_warrior= "#d7fcd4"
    p1_color_nomad= "#d7fcd4"

    p2_color_wizard= "#d7fcd4"
    p2_color_warrior= "#d7fcd4"
    p2_color_nomad= "#d7fcd4"
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    leave_menu = False
    clock = pygame.time.Clock()
    while True:

        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(35).render("CHARACTER SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        #player 1
        text = font(15).render("PLAYER 1", True, "#b68f40")
        rect = text.get_rect(center=(300, 100))
        screen.blit(text, rect)

        #player 2
        text = font(15).render("PLAYER 2", True, "#b68f40")
        rect = text.get_rect(center=(700, 100))
        screen.blit(text, rect)

        play = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(700, 525),
                        text_input="PLAY", font=font(35), base_color="Black", hovering_color="Yellow")
        #character select buttons for player 1
        p1_wizard = Button(image=None, pos=(300, 275),
                        text_input="wizard", font=font(25), base_color=p1_color_wizard, hovering_color="Yellow")
        p1_warrior = Button(image=None, pos=(300, 400),
                        text_input="warrior", font=font(25), base_color=p1_color_warrior, hovering_color="Yellow")
        p1_nomad = Button(image=None, pos=(300, 150),
                        text_input="nomad", font=font(25), base_color=p1_color_nomad, hovering_color="Yellow")
        #character select buttons for player 2
        p2_wizard = Button(image=None, pos=(700, 275),
                        text_input="wizard", font=font(25), base_color=p2_color_wizard, hovering_color="Blue")
        p2_warrior = Button(image=None, pos=(700, 400),
                        text_input="warrior", font=font(25), base_color=p2_color_warrior, hovering_color="Blue")
        p2_nomad = Button(image=None, pos=(700, 150),
                        text_input="nomad", font=font(25), base_color=p2_color_nomad, hovering_color="Blue")

        back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(300, 525),
                      text_input="BACK", font=font(35), base_color="Black", hovering_color="Yellow")

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
                #make it so that when you click play, it goes to the game loop
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Map Select")
                    map_select()
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
                if p1_wizard.checkForInput(mouse):
                    p1_color_warrior = "#d7fcd4"
                    p1_color_wizard = "Yellow"
                    p1_color_nomad = "#d7fcd4"
                    p1= "wizard"
                if p1_warrior.checkForInput(mouse):
                    p1_color_warrior = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_nomad = "#d7fcd4"
                    p1= "warrior"
                if p1_nomad.checkForInput(mouse):
                    p1_color_nomad = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_warrior = "#d7fcd4"
                    p1= "nomad"
                if p2_wizard.checkForInput(mouse):
                    p2_color_wizard = "Blue"
                    p2_color_warrior = "#d7fcd4"
                    p2_color_nomad = "#d7fcd4"
                    p2= "wizard"
                if p2_warrior.checkForInput(mouse):
                    p2_color_warrior = "Blue"
                    p2_color_nomad = "#d7fcd4"
                    p2_color_wizard = "#d7fcd4"
                    p2= "warrior"
                if p2_nomad.checkForInput(mouse):
                    p2_color_nomad = "Blue"
                    p2_color_wizard = "#d7fcd4"
                    p2_color_warrior = "#d7fcd4"
                    p2= "nomad"
                
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()


#create a map select screen
def map_select():
    global map
    leave_menu = False
    clock = pygame.time.Clock()
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = font(35).render("MAP SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        play = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(700, 525),
                        text_input="PLAY", font=font(35), base_color="White", hovering_color="Yellow")
        #map select buttons
        map1 = Button(image=None, pos=(300, 150),
                        text_input="map1", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map2 = Button(image=None, pos=(500, 150),
                        text_input="map2", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map3 = Button(image=None, pos=(700, 150),
                        text_input="map3", font=font(25), base_color="#d7fcd4", hovering_color="Yellow")

        back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(300, 525),
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
                #make it so that when you click play, it goes to the game loop
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Game")
                    game_loop()
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Character Select")
                    leave_menu = True
                    break
                if map1.checkForInput(mouse):
                    map = "mountain"
                if map2.checkForInput(mouse):
                    map = "cliffs"
                if map3.checkForInput(mouse):
                    map = "church"
        if leave_menu:
            break
        clock.tick(MENU_FPS)
        pygame.display.update()
def multi_char_select(game_client):
    global p1, p2
    default_colour = "#d7fcd4"
    p2_wiz = "#d7fcd4"
    p2_war=  "#d7fcd4"
    p2_nom = "#d7fcd4"
    play = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(700, 525),
                  text_input="PLAY", font=font(35), base_color="Black", hovering_color="Yellow")
    # character select buttons for player 1
    p1_wizard = Button(image=None, pos=(300, 275),
                       text_input="wizard", font=font(25), base_color=default_colour, hovering_color="Yellow")
    p1_warrior = Button(image=None, pos=(300, 400),
                        text_input="warrior", font=font(25), base_color=default_colour, hovering_color="Yellow")
    p1_nomad = Button(image=None, pos=(300, 150),
                      text_input="nomad", font=font(25), base_color="Yellow", hovering_color="Yellow")


    back = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(300, 525),
                  text_input="BACK", font=font(35), base_color="Black", hovering_color="Yellow")


    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    characters = [p1_nomad,p1_wizard, p1_warrior]

    p_choice = 0
    locked_in = False
    loop = asyncio.get_event_loop()
    l_count=0
    clock = pygame.time.Clock()
    while True:
        mouse = pygame.mouse.get_pos()
        screen.blit(menu_scaled, (0, 0))
        if game_client.enemy_quit_game==0:
            try:
                game_client.socket.close()
            except:
                pass

            break

        for button in [ back, play, p1_wizard, p1_warrior, p1_nomad]:
            button.hover(mouse)
            button.update(screen)
            # character select buttons for player 2
        p2_wizard = Button(image=None, pos=(700, 275),
                               text_input="wizard", font=font(25), base_color=p2_wiz, hovering_color="Blue")
        p2_warrior = Button(image=None, pos=(700, 400),
                                text_input="warrior", font=font(25), base_color=p2_war, hovering_color="Blue")
        p2_nomad = Button(image=None, pos=(700, 150),
                              text_input="nomad", font=font(25), base_color=p2_nom, hovering_color="Blue")
        enemy_chars = [p2_nomad, p2_wizard, p2_warrior]
        loop.create_task(game_client.get_enemy_character())
        if game_client.enemy_resp is not None:
            if game_client.enemy_char==0:
                p2_nom = "Blue"
                p2_wiz = default_colour
                p2_war = default_colour
            elif game_client.enemy_char==1:
                p2_wiz = "Blue"
                p2_nom = default_colour
                p2_war = default_colour
            else:
                p2_war = "Blue"
                p2_wiz = default_colour
                p2_nom = default_colour

            if game_client.enemy_resp.start:

                break

            game_client.enemy_resp = None

        for button in enemy_chars:
            button.update(screen)

        text = font(35).render("CHARACTER SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        screen.blit(text, rect)

        # player 1
        text = font(15).render("YOUR PICK", True, "#b68f40")
        rect = text.get_rect(center=(300, 100))
        screen.blit(text, rect)

        # player 2
        text = font(15).render("ENEMY PICK", True, "#b68f40")
        rect = text.get_rect(center=(700, 100))
        screen.blit(text, rect)
        if l_count ==0:
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
                if play.checkForInput(mouse):
                    locked_in = True

                    game_client.local_char = p_choice
                    #pygame.display.set_caption("Game")

                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    main_menu()
                if locked_in:
                    continue
                for i, button in enumerate(characters):
                    if button.checkForInput(mouse):
                        game_client.send_character_choice(i,False)
                        button.base_color = "Yellow"
                        p_choice = i
                        p1 = button.text_input
                        for j in [z for z in range(0,3) if z !=i]:
                            characters[j].base_color=default_colour


        l_count = (l_count+1)%20
        pygame.display.update()
        run_once(loop)
        clock.tick(MENU_FPS)

async def update_lobby(game_client):
    loop = asyncio.get_event_loop()
    loop.create_task(game_client.get_enemy_character())

# main menu
def main_menu():
    menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    play = Button(image=pygame.image.load(resource_path("game/assets/menu/long.png")), pos=(500, 180),
                  text_input="PLAY", font=font(55), base_color="#d7fcd4", hovering_color="White")

    options = Button(image=pygame.image.load(resource_path("game/assets/menu/long.png")), pos=(500, 325),
                     text_input="OPTIONS", font=font(55), base_color="#d7fcd4", hovering_color="White")
    quit = Button(image=pygame.image.load(resource_path("game/assets/menu/medium.png")), pos=(500, 470),
                  text_input="QUIT", font=font(55), base_color="#d7fcd4", hovering_color="White")
    text = font(75).render("Main Menu", True, "#b68f40")
    rect = text.get_rect(center=(500, 50))
    clock = pygame.time.Clock()
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
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Game Mode")
                    menu_play()
                if options.checkForInput(mouse):
                    pygame.display.set_caption("Options")
                    opt()
                if quit.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()
        clock.tick(MENU_FPS)
        pygame.display.update()

#https://stackoverflow.com/a/51266275
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



if __name__ == "__main__":
    map = ""
    p1=""
    p2=""
    player1_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "attack1": pygame.K_r,
                                    "attack2": pygame.K_t, "block": pygame.K_s}

    player2_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP,
                                    "attack1": pygame.K_n, "attack2": pygame.K_m, "block": pygame.K_DOWN}

    mixer.init
    pygame.init()
    # create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    #default characters
    p1="wizard"
    p2="wizard"

    #default map
    map = "mountain"
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    # cap frame rate
    clock = pygame.time.Clock()
    MENU_FPS = 20
    GAME_FPS = 60
    # define colors
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # load bg image

    bg_image = pygame.image.load(resource_path("game/assets/maps/background.png")).convert_alpha()

    menu_bg = pygame.image.load(resource_path("game/assets/menu/main_menu_bg.png")).convert_alpha()

    # use mixer to load music and sounds
    #mixer.music.load("game/assets/audio/main.mp3")
    #mixer.music.play(-1)
    mixer.music.set_volume(0)
    punch_fx = mixer.Sound(resource_path("game/assets/audio/punch.wav"))
    projectile_fx = mixer.Sound(resource_path("game/assets/audio/proj.wav"))
    hit_fx = mixer.Sound(resource_path("game/assets/audio/hit.wav"))
    punch_fx.set_volume(0.15)
    projectile_fx.set_volume(0.5)
    hit_fx.set_volume(0.5)

    obstacles = []
    main_menu()
