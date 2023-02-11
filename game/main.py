import pygame, asyncio
from pygame import mixer

import game.main
from game.fighter import Fighter
from game.online_fighter import OnlineFighter
from game.characters.nomad import createNomad
from game.characters.warrior import createWarrior
from game.characters.wizard import createWizard
from game.obstacle import Obstacle
from game.button import Button
from game.network.game_client import GameClient
import sys




class StreetFighter:
    def __init__(self):
        self.p1 = ""
        self.p2 = ""
        self.player1_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "attack1": pygame.K_r,
                            "attack2": pygame.K_t, "block": pygame.K_s}

        self.player2_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP,
                            "attack1": pygame.K_n, "attack2": pygame.K_m, "block": pygame.K_DOWN}

        mixer.init()
        pygame.init()
        # create game window
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600

        # default characters
        self.p1 = "wizard"
        self.p2 = "wizard"

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Main Menu")

        # cap frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # define colors
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)

        # load bg image
        self.bg_image = pygame.image.load("game/assets/maps/background.png").convert_alpha()
        self.menu_bg = pygame.image.load("game/assets/menu/main_menu_bg.png").convert_alpha()

        # use mixer to load music and sounds
        # mixer.music.load("game/assets/audio/main.mp3")
        # mixer.music.play(-1)
        mixer.music.set_volume(0)
        self.punch_fx = mixer.Sound("game/assets/audio/punch.wav")
        self.projectile_fx = mixer.Sound("game/assets/audio/proj.wav")
        self.hit_fx = mixer.Sound("game/assets/audio/hit.wav")
        self.punch_fx.set_volume(0.15)
        self.projectile_fx.set_volume(0.5)
        self.hit_fx.set_volume(0.5)

        # create obstacles
        # obstacle_1 = Obstacle(400, 300, 100, 300)
        self.obstacle_2 = Obstacle(700, 200, 200, 50)
        self.obstacle_3 = Obstacle(100, 300, 100, 50)
        self.obstacles = [self.obstacle_2, self.obstacle_3]

        # current game state

        self.game_state = "main_menu"



    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))


    # draw health bars
    def draw_health_bar(self,health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 3, y - 3, 406, 36))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))


    # font size
    def font(self,size):
        return pygame.font.Font("game/assets/menu/font.ttf", size)


    # when a button is pressed, it should change the key that is assigned to that action
    def control_handling(self, keys, key):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in self.player1_controls.values():
                        return
                    elif event.key in self.player2_controls.values():
                        return
                    keys[key] = event.key
                    return


    def sfx_change(self, level):
        if level == 0:
            self.punch_fx.set_volume(0)
            self.projectile_fx.set_volume(0)
            self.hit_fx.set_volume(0)
        elif level == 1:
            self.punch_fx.set_volume(0.1)
            self.projectile_fx.set_volume(0.25)
            self.hit_fx.set_volume(0.25)
        elif level == 2:
            self.punch_fx.set_volume(0.15)
            self.projectile_fx.set_volume(0.5)
            self.hit_fx.set_volume(0.5)
        elif level == 3:
            self.punch_fx.set_volume(0.2)
            self.projectile_fx.set_volume(0.75)
            self.hit_fx.set_volume(0.75)
        elif level == 4:
            self.punch_fx.set_volume(0.3)
            self.projectile_fx.set_volume(1)
            self.hit_fx.set_volume(1)


    # game loop
    def game_loop(self):
        if self.p1 == "wizard":
            fighter_1 = createWizard(Fighter, 1, 200, 310, False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        elif self.p1 == "nomad":
            fighter_1 = createNomad(Fighter, 1, 200, 310, False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        elif self.p1 == "warrior":
            fighter_1 = createWarrior(Fighter, 1, 200, 310, False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        if self.p2 == "wizard":
            fighter_2 = createWizard(Fighter, 2, 700, 310, True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)

        elif self.p2 == "nomad":
            fighter_2 = createNomad(Fighter, 2, 700, 310, True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)

        elif self.p2 == "warrior":
            fighter_2 = createWarrior(Fighter, 2, 700, 310, True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)

        run = True
        while run:

            # cap frame rate
            self.clock.tick(self.FPS)

            # draw background
            self.draw_bg()

            # draw health bars
            self.draw_health_bar(fighter_1.health, 20, 20)
            self.draw_health_bar(fighter_2.health, 580, 20)

            # move fighters
            fighter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, fighter_2, self.obstacles)
            fighter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, fighter_1, self.obstacles)

            # update frames
            fighter_1.frameUpdate()
            fighter_2.frameUpdate()

            # draw fighters
            fighter_1.draw(self.screen)
            fighter_2.draw(self.screen)

            # draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            # if fighter 1 or 2 punches, play the punch.wav sound effect

            # update display
            pygame.display.update()
        pygame.quit()
        sys.exit()


    async def update_enemy(self, game_client, local_player, enemy_character):
        for message in game_client.get_updates():
            local_player.health = message.enemyHealth
            enemy_character.move_enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, local_player, self.obstacles,

                                       message.keys, message.x, message.y)


    def run_once(loop):
        loop.call_soon(loop.stop)
        loop.run_forever()


    def multi_player_game_loop(game_client):
        # gameKeys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t]
        pygame.init()

        pygame.display.set_caption("Team 5 Project")

        # create fighters
        f1 = createWizard(OnlineFighter, 1, 200, 310, False, punch_fx, projectile_fx, hit_fx, player1_controls)
        f2 = createWarrior(OnlineFighter, 2, 700, 310, True, punch_fx, projectile_fx, hit_fx, player1_controls)

        fighters = [f1, f2]
        pick = int(game_client.player_id)

        local_player = fighters[pick]
        local_player.game_client = game_client
        enemy = (pick + 1) % 2
        enemy_character = fighters[enemy]
        obstacle_1 = Obstacle(400, 300, 100, 300)
        obstacle_2 = Obstacle(700, 200, 200, 50)
        obstacles = [obstacle_1, obstacle_2]
        run = True
        clock = pygame.time.Clock()
        FPS = 60
        loop = asyncio.get_event_loop()
        while run:

            # cap frame rate
            clock.tick(FPS)

            # draw background
            # draw background
            draw_bg()

            # draw health bars
            draw_health_bar(fighters[0].health, 20, 20)
            draw_health_bar(fighters[1].health, 580, 20)

            # move fighters
            message = local_player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, enemy_character, obstacles, game_client)
            loop.create_task(local_player.game_client.send_update(message))
            loop.create_task(game_client.get_update())

            for message in game_client.messages:
                if message.quit:
                    run = False
                local_player.health = message.enemyHealth
                enemy_character.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, local_player, obstacles, message.keys,
                                           message.x, message.y)
                enemy_character.obstacle_collision(screen, obstacles)

            enemy_character.draw_projectile(local_player, screen.get_width(), screen)
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

            # make player 1 controls with a button
            controls_player1 = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 175),
                                      text_input="Player 1", font=font(35), base_color="#d7fcd4", hovering_color="White")

            controls_player2 = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 325),
                                      text_input="Player 2", font=font(35), base_color="#d7fcd4", hovering_color="White")

            controls_back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 475),
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


    # fighter1 controls displayed and mutable
    def player1():
        global player1_controls
        # player1_keys = {"left": "a", "right": "d", "jump": "w", "block": "s", "attack1": "r", "attack2": "t"}
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

            player1_back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 475),
                                  text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [player1_back, player1_up, player1_down, player1_left, player1_right, player1_attack1,
                           player1_attack2]:
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

            pygame.display.update()


    # fighter2 controls displayed and mutable
    def player2():
        global player2_controls
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

            player2_back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 475),
                                  text_input="BACK", font=font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [player2_back, player2_up, player2_down, player2_left, player2_right, player2_attack1,
                           player2_attack2]:
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

            opt_controls = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 175),
                                  text_input="CONTROLS", font=font(35), base_color="#d7fcd4", hovering_color="White")
            opt_audio = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 325),
                               text_input="AUDIO", font=font(35), base_color="#d7fcd4", hovering_color="White")
            opt_back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 475),
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
                    if opt_audio.checkForInput(opt_mouse):
                        pygame.display.set_caption("Audio")
                        audio()

            pygame.display.update()


    # create a function to handle audio levels using buttons for sound effects and music
    def audio():
        while True:
            audio_mouse = pygame.mouse.get_pos()

            menu_scaled = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(menu_scaled, (0, 0))

            audio_text = font(50).render("AUDIO VOLUME", True, "#b68f40")
            audio_rect = audio_text.get_rect(center=(500, 65))
            screen.blit(audio_text, audio_rect)
            music_text = font(40).render("MUSIC", True, "#b68f40")
            music_rect = music_text.get_rect(center=(200, 175))
            screen.blit(music_text, music_rect)
            audio_back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 475),
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
                button.changeColor(audio_mouse)
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
                        opt()
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

            pygame.display.update()


    # new menu for when you click play, it should have a "local multiplayer" and a "singleplayer" button
    def menu_play(self):
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(70).render("GAME MODE", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        self.screen.blit(text, rect)

        single_player = Button(image=pygame.image.load("game/assets/menu/long.png"), pos=(500, 150),
                               text_input="SINGLEPLAYER", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        local = Button(image=pygame.image.load("game/assets/menu/long.png"), pos=(500, 275),
                       text_input="LOCAL MULTI", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        multiplayer = Button(image=pygame.image.load("game/assets/menu/long.png"), pos=(500, 400),
                             text_input="MULTIPLAYER", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 525),
                      text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        for button in [single_player, local, multiplayer, back]:
            button.changeColor(mouse)
            button.update(self.screen)

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
                    self.game_state = "menu_char"
                if local.checkForInput(mouse):
                    pygame.display.set_caption("Local Multiplayer")
                    self.menu_char()
                if multiplayer.checkForInput(mouse):
                    pygame.display.set_caption("Multi Player")
                    game_client = GameClient(1234)
                    game_client.connect("project.michaelc445.container.netsoc.cloud", 17023, "m")
                    print(game_client.player_id)
                    game_client.socket.setblocking(False)
                    self.multi_player_game_loop(game_client)
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    self.main_menu()




    # character select menu
    def menu_char(self):
        global p1
        global p2

        p1_color_wizard = "#d7fcd4"
        p1_color_warrior = "#d7fcd4"
        p1_color_nomad = "#d7fcd4"

        p2_color_wizard = "#d7fcd4"
        p2_color_warrior = "#d7fcd4"
        p2_color_nomad = "#d7fcd4"

        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(35).render("CHARACTER SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        self.screen.blit(text, rect)

        # player 1
        text = self.font(15).render("PLAYER 1", True, "#b68f40")
        rect = text.get_rect(center=(300, 100))
        self.screen.blit(text, rect)

        # player 2
        text = self.font(15).render("PLAYER 2", True, "#b68f40")
        rect = text.get_rect(center=(700, 100))
        self.screen.blit(text, rect)

        play = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(700, 525),
                      text_input="PLAY", font=self.font(35), base_color="Black", hovering_color="Yellow")
        # character select buttons for player 1
        p1_wizard = Button(image=None, pos=(300, 275),
                           text_input="wizard", font=self.font(25), base_color=p1_color_wizard, hovering_color="Yellow")
        p1_warrior = Button(image=None, pos=(300, 400),
                            text_input="warrior", font=self.font(25), base_color=p1_color_warrior, hovering_color="Yellow")
        p1_nomad = Button(image=None, pos=(300, 150),
                          text_input="nomad", font=self.font(25), base_color=p1_color_nomad, hovering_color="Yellow")
        # character select buttons for player 2
        p2_wizard = Button(image=None, pos=(700, 275),
                           text_input="wizard", font=self.font(25), base_color=p2_color_wizard, hovering_color="Blue")
        p2_warrior = Button(image=None, pos=(700, 400),
                            text_input="warrior", font=self.font(25), base_color=p2_color_warrior, hovering_color="Blue")
        p2_nomad = Button(image=None, pos=(700, 150),
                          text_input="nomad", font=self.font(25), base_color=p2_color_nomad, hovering_color="Blue")

        back = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(300, 525),
                      text_input="BACK", font=self.font(35), base_color="Black", hovering_color="Yellow")

        for button in [back, play, p1_wizard, p1_warrior, p1_nomad, p2_wizard, p2_warrior, p2_nomad]:
            button.changeColor(mouse)
            button.update(self.screen)

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
                    self.game_loop()
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    self.main_menu()
                if p1_wizard.checkForInput(mouse):
                    p1_color_wizard = "Yellow"
                    p1_color_warrior = "#d7fcd4"
                    p1_color_nomad = "#d7fcd4"
                    p1 = "wizard"
                if p1_warrior.checkForInput(mouse):
                    p1_color_warrior = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_nomad = "#d7fcd4"
                    p1 = "warrior"
                if p1_nomad.checkForInput(mouse):
                    p1_color_nomad = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_warrior = "#d7fcd4"
                    p1 = "nomad"
                if p2_wizard.checkForInput(mouse):
                    p2_color_wizard = "Blue"
                    p2_color_warrior = "#d7fcd4"
                    p2_color_nomad = "#d7fcd4"
                    p2 = "wizard"
                if p2_warrior.checkForInput(mouse):
                    p2_color_warrior = "Blue"
                    p2_color_nomad = "#d7fcd4"
                    p2_color_wizard = "#d7fcd4"
                    p2 = "warrior"
                if p2_nomad.checkForInput(mouse):
                    p2_color_nomad = "Blue"
                    p2_color_wizard = "#d7fcd4"
                    p2_color_warrior = "#d7fcd4"
                    p2 = "nomad"




    # main menu
    def main_menu(self):


        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(75).render("Main Menu", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))

        play = Button(image=pygame.image.load("game/assets/menu/long.png"), pos=(500, 180),
                      text_input="PLAY", font=self.font(55), base_color="#d7fcd4", hovering_color="White")

        # multi_player = Button(image=pygame.image.load("game/assets/Options Rect.png"), pos=(500, 275),
        # text_input="MULTI-PLAYER", font=font(45), base_color="#d7fcd4", hovering_color="White")

        options = Button(image=pygame.image.load("game/assets/menu/long.png"), pos=(500, 325),
                         text_input="OPTIONS", font=self.font(55), base_color="#d7fcd4", hovering_color="White")
        quit = Button(image=pygame.image.load("game/assets/menu/medium.png"), pos=(500, 470),
                      text_input="QUIT", font=self.font(55), base_color="#d7fcd4", hovering_color="White")

        self.screen.blit(text, rect)

        for button in [play, options, quit]:
            button.changeColor(mouse)
            button.update(self.screen)

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
                    self.game_state = "menu_play"
                if options.checkForInput(mouse):
                    pygame.display.set_caption("Options")
                    self.opt()
                if quit.checkForInput(mouse):
                    pygame.quit()
                    sys.exit()


    async def main(self):

        state_map = {"main_menu": self.main_menu, "menu_play": self.menu_play,
                     "menu_char" : self.menu_char}
        run = True
        while run:
            draw_func = state_map[self.game_state]
            print(self.game_state)
            draw_func()
            print("yeah go on")
            print("would you go way")
            pygame.display.update()
            await asyncio.sleep(1)

app = StreetFighter()
asyncio.run(app.main())

