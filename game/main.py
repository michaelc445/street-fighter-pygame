import pygame, asyncio
from pygame import mixer
from fighter import Fighter
from fighter_ai import Fighter_ai
#from online_fighter import OnlineFighter
from nomad import createNomad
from warrior import createWarrior
from wizard import createWizard
from obstacle import Obstacle
from button import Button
#from network.game_client import GameClient
import sys,os

class Main:
    def __init__(self):
        self.map = ""
        self.p1 = ""
        self.p2 = ""
        self.player1_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "attack1": pygame.K_r,
                            "attack2": pygame.K_t, "block": pygame.K_s}

        self.player2_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP,
                            "attack1": pygame.K_n, "attack2": pygame.K_m, "block": pygame.K_DOWN}

        mixer.init
        pygame.init()
        # create game window
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600

        # default characters
        self.p1 = "wizard"
        self.p2 = "wizard"

        # default map
        self.map = "mountain"
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Main Menu")

        # cap frame rate
        self.clock = pygame.time.Clock()
        self.MENU_FPS = 20
        self.GAME_FPS = 60
        # define colors
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)

        # load bg image
        self.bg_image = pygame.image.load(self.resource_path("assets/maps/background.png")).convert_alpha()

        self.menu_bg = pygame.image.load(self.resource_path("assets/menu/main_menu_bg.png")).convert_alpha()

        # use mixer to load music and sounds
        self.punch_fx = mixer.Sound(self.resource_path("assets/audio/punch.wav"))
        self.projectile_fx = mixer.Sound(self.resource_path("assets/audio/proj.wav"))
        self.hit_fx = mixer.Sound(self.resource_path("assets/audio/hit.wav"))
        self.punch_fx.set_volume(0.15)
        self.projectile_fx.set_volume(0.5)
        self.hit_fx.set_volume(0.5)

        self.obstacles = []
        mixer.music.load(self.resource_path("assets/audio/background-menu.wav"))
        mixer.music.play(-1)
        # mixer.music.set_volume(0)
        self.game_state = "main_menu"
        self.single_player = False
        self.p1_spawn = [100, 134]
        self.p2_spawn = [850, 134]
        self.fighter_1 = createWizard(Fighter, 1, self.p1_spawn[0], self.p1_spawn[1], False, self.punch_fx,
                                      self.projectile_fx, self.hit_fx, self.player1_controls)
        self.fighter_2 = createWizard(Fighter, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx,
                                      self.projectile_fx, self.hit_fx, self.player2_controls)
        self.run = True
        self.scores = [0, 0]
        # round variables
        self.intro = 3
        self.over = False
        self.round_cd = 1500
        self.last_tick_update = pygame.time.get_ticks()
        self.scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))





    def draw_bg(self, scaled_bg_image):

        self.screen.blit(scaled_bg_image, (0, 0))

    def draw_text(self,text, font, color, surface, x, y):
        text = font.render(text, True, color)
        rect = text.get_rect(center=(x, y))
        self.screen.blit(text, rect)

    # draw health bars
    def draw_health_bar(self,health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 3, y - 3, 406, 36))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    def draw_scores(self,p1_score, p2_score):
        score = " - "
        self.draw_text(score, self.font(30), self.WHITE, self.screen, self.SCREEN_WIDTH / 2, 35)
        self.draw_text(str(p1_score), self.font(30), self.WHITE, self.screen, self.SCREEN_WIDTH / 2 - 50, 35)
        self.draw_text(str(p2_score), self.font(30), self.WHITE, self.screen, self.SCREEN_WIDTH / 2 + 50, 35)
    # font size
    def font(self,size):
        return pygame.font.Font(self.resource_path("assets/menu/font.ttf"), size)

    def locateFighter(self,fighter):
        print(fighter.rect.x, fighter.rect.y)

    # when a button is pressed, it should change the key that is assigned to that action
    def control_handling(self,keys, key):
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


    def sfx_change(self,level):
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
        if self.map == "mountain":
            self.p1_spawn = [100, 134]
            self.p2_spawn = [850, 134]
            map_chosen = "assets/maps/mountain.png"
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

            self.obstacles = [middle_ground1, middle_ground2, left_cliff1, left_cliff2, left_cliff3, left_cliff4, right_cliff1,
                         right_cliff2, right_cliff3, right_cliff4]

        elif self.map == "church":
            self.p1_spawn = [900, 286]
            self.p2_spawn = [56, 286]
            map_chosen = "assets/maps/church.png"
            # church obstacles
            middle_floor = Obstacle(150, 530, 700, 80)
            left_side = Obstacle(0, 387, 142, 160)
            right_side = Obstacle(860, 387, 142, 160)
            middle_top = Obstacle(235, 240, 525, 40)

            self.obstacles = [middle_floor, left_side, right_side, middle_top]

        elif self.map == "cliffs":
            self.p1_spawn = [135, 254]
            self.p2_spawn = [870, 45]
            map_chosen = "assets/maps/cliffs.png"
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

            self.obstacles = [left_island1, left_island2, middle_island1, middle_island2, right_cliff1, right_cliff2, right_cliff3, right_cliff4, right_cliff5, right_cliff6]
        if self.p1 == "wizard":
            self.fighter_1 = createWizard(Fighter, 1, self.p1_spawn[0], self.p1_spawn[1], False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        elif self.p1 == "nomad":
            self.fighter_1 = createNomad(Fighter, 1, self.p1_spawn[0], self.p1_spawn[1], False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        elif self.p1 == "warrior":
            self.fighter_1 = createWarrior(Fighter, 1, self.p1_spawn[0], self.p1_spawn[1], False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        if self.single_player:
            if self.p2 == "wizard":
                self.fighter_2 = createWizard(Fighter_ai, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx,
                                         self.player2_controls)

            elif self.p2 == "nomad":
                print("single nomad")
                self.fighter_2 = createNomad(Fighter_ai, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx,
                                        self.player2_controls)

            elif self.p2 == "warrior":
                self.fighter_2 = createWarrior(Fighter_ai, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx,
                                          self.player2_controls)
        else:
            if self.p2 == "wizard":
                self.fighter_2 = createWizard(Fighter, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)

            elif self.p2 == "nomad":
                self.fighter_2 = createNomad(Fighter, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)

            elif self.p2 == "warrior":
                self.fighter_2 = createWarrior(Fighter, 2, self.p2_spawn[0], self.p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player2_controls)


        #load map
        self.bg_image = pygame.image.load(self.resource_path(map_chosen)).convert_alpha()
        self.scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.run = True
        self.scores = [0,0]
        #round variables
        self.intro = 3
        self.over = False
        self.round_cd = 1500
        self.last_tick_update = pygame.time.get_ticks()
        self.game_state="game_run"

    def game_run(self):
        if self.single_player:
            player_state = self.fighter_1.return_state()
            self.fighter_2.set_moves(player_state)
        # cap frame rate
        self.clock.tick(self.GAME_FPS)

        # draw background
        self.draw_bg(self.scaled_bg)

        # draw health bars
        self.draw_health_bar(self.fighter_1.health, 20, 20)
        self.draw_health_bar(self.fighter_2.health, 580, 20)

        self.draw_scores(self.scores[0], self.scores[1])


        # move fighters
        if self.intro <= 0:
            self.fighter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_2, self.obstacles)
            self.fighter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_1, self.obstacles)
        else:
            self.draw_text(str(self.intro), self.font(80), self.RED, self.screen, (self.SCREEN_WIDTH / 2), self.SCREEN_HEIGHT / 3)
            #reduce intro by 1 every second using pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.last_tick_update >= 1000:
                self.intro -= 1
                self.last_tick_update = pygame.time.get_ticks()


        if self.over == False:
            if not self.fighter_1.alive:
                self.scores[1] += 1
                self.over = True
                self.over_time = pygame.time.get_ticks()
            elif not self.fighter_2.alive:
                self.scores[0] +=1
                self.over = True
                self.over_time = pygame.time.get_ticks()
        else:
            if self.scores[0] == 3 or self.scores[1] == 3:
                if self.scores[0] == 3:
                    self.draw_text("PLAYER 1 WINS", self.font(50), self.RED, self.screen, (self.SCREEN_WIDTH / 2),
                                   self.SCREEN_HEIGHT / 3)
                else:
                    self.draw_text("PLAYER 2 WINS", self.font(50), self.RED, self.screen, (self.SCREEN_WIDTH / 2),
                                   self.SCREEN_HEIGHT / 3)
            if self.fighter_1.alive:
                self.draw_text("PLAYER 1 WINS", self.font(50), self.RED, self.screen, (self.SCREEN_WIDTH / 2), self.SCREEN_HEIGHT / 3)
            elif self.fighter_2.alive:
                self.draw_text("PLAYER 2 WINS", self.font(50), self.RED, self.screen, (self.SCREEN_WIDTH / 2), self.SCREEN_HEIGHT / 3)
            if pygame.time.get_ticks() - self.over_time >= self.round_cd:
                self.over = False
                self.fighter_1.reset()
                self.fighter_2.reset()




        # update pulse
        self.fighter_1.frameUpdate()
        self.fighter_2.frameUpdate()

        # draw fighters
        p1_name = "P1"
        p1_colour = (0, 0, 255)
        p2_name = "P2"
        p2_colour = (255, 0, 0)

        self.fighter_1.draw(self.screen, p1_name,p1_colour)
        self.fighter_2.draw(self.screen, p2_name, p2_colour )





        # draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False

        # if fighter 1 or 2 punches, play the punch.wav sound effect
        #print coordinates of player 1
        #locateFighter(fighter_1)
        # update display
        pygame.display.update()
        mixer.music.load(self.resource_path("assets/audio/background-menu.wav"))
        mixer.music.play(-1)
        mixer.music.set_volume(1)

    async def update_enemy(self,game_client,local_player,enemy_character):
        for message in game_client.get_updates():
            local_player.health = message.enemyHealth
            enemy_character.move_enemy(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, local_player, self.obstacles,

                                       message.keys, message.x, message.y)


    def run_once(self,loop):
        loop.call_soon(loop.stop)
        loop.run_forever()

    def multi_player_game_loop(self,game_client):
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
            f1 = char_dict[game_client.local_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, self.punch_fx, self.projectile_fx, self.hit_fx,self.player1_controls)
            f2 = char_dict[game_client.enemy_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx,self.player1_controls)
        else:
            f1 = char_dict[game_client.enemy_char](OnlineFighter, 1, p1_spawn[0], p1_spawn[1], False, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)
            f2 = char_dict[game_client.local_char](OnlineFighter, 2, p2_spawn[0], p2_spawn[1], True, self.punch_fx, self.projectile_fx, self.hit_fx, self.player1_controls)

        fighters = [f1, f2]
        pick = int(game_client.player_id)

        local_player = fighters[pick]
        local_player.game_client = game_client
        enemy = (pick + 1) % 2
        enemy_character = fighters[enemy]



        self.bg_image = pygame.image.load(self.resource_path(map_chosen)).convert_alpha()
        scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        run = True
        clock = pygame.time.Clock()
        loop = asyncio.get_event_loop()
        quit_game_to_menu = False
        while run:

            # cap frame rate
            clock.tick(self.GAME_FPS)

            # draw background
            self.draw_bg(scaled_bg)

            # draw health bars
            self.draw_health_bar(fighters[0].health, 20, 20)
            self.draw_health_bar(fighters[1].health, 580, 20)

            # move fighters
            message = local_player.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, enemy_character, obstacles, game_client)
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

                enemy_character.move_enemy(self.SCREEN_WIDTH,self.SCREEN_HEIGHT,self.screen,local_player,obstacles,message.keys,message.x,message.y)
                enemy_character.obstacle_collision(self.screen, obstacles)
            if quit_game_to_menu:
                break
            enemy_character.draw_projectile(local_player,self.screen.get_width(),self.screen)
            local_player.frameUpdate()
            enemy_character.frameUpdate()
            # draw fighters
            local_player.draw(self.screen)
            enemy_character.draw(self.screen)



            # draw obstacles
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

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
            self.run_once(loop)



    # controls
    def controls(self):
        leave_menu = False
        clock = pygame.time.Clock()
        while True:

            controls_mouse = pygame.mouse.get_pos()

            menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(menu_scaled, (0, 0))

            controls_text = self.font(50).render("CONTROLS", True, "#b68f40")
            controls_rect = controls_text.get_rect(center=(500, 65))
            self.screen.blit(controls_text, controls_rect)

            # make player 1 controls with a button
            controls_player1 = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 175),
                                      text_input="Player 1", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            controls_player2 = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 325),
                                      text_input="Player 2", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            controls_back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 475),
                                   text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [controls_back, controls_player1, controls_player2]:
                button.hover(controls_mouse)
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
                    if controls_back.checkForInput(controls_mouse):
                        leave_menu = True
                        break
                    if controls_player1.checkForInput(controls_mouse):
                        self.player1()
                    if controls_player2.checkForInput(controls_mouse):
                        self.player2()
            if leave_menu:
                break
            self.clock.tick(self.MENU_FPS)
            pygame.display.update()


    # fighter1 controls displayed and mutable
    def player1(self):
        global player1_controls
        # player1_keys = {"left": "a", "right": "d", "jump": "w", "block": "s", "attack1": "r", "attack2": "t"}
        leave_menu = False
        clock = pygame.time.Clock()
        while True:

            player1_mouse = pygame.mouse.get_pos()

            menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(menu_scaled, (0, 0))

            player1_text = self.font(50).render("PLAYER 1", True, "#b68f40")
            player1_rect = player1_text.get_rect(center=(500, 65))
            self.screen.blit(player1_text, player1_rect)

            # make player 1 controls with a button
            player1_up = Button(image=None, pos=(500, 150),
                                text_input="Jump : " + pygame.key.name(player1_controls["jump"]), font=self.font(15),
                                base_color="#d7fcd4", hovering_color="White")

            player1_down = Button(image=None, pos=(500, 200),
                                  text_input="Block : " + pygame.key.name(player1_controls["block"]),
                                  font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player1_left = Button(image=None, pos=(500, 250),
                                  text_input="Left : " + pygame.key.name(player1_controls["left"]), font=self.font(15),
                                  base_color="#d7fcd4", hovering_color="White")

            player1_right = Button(image=None, pos=(500, 300),
                                   text_input="Right : " + pygame.key.name(player1_controls["right"]),
                                   font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player1_attack1 = Button(image=None, pos=(500, 350),
                                     text_input="Punch : " + pygame.key.name(player1_controls["attack1"]),
                                     font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player1_attack2 = Button(image=None, pos=(500, 400),
                                     text_input="Projectile : " + pygame.key.name(player1_controls["attack2"]),
                                     font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player1_back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 475),
                                  text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [player1_back, player1_up, player1_down, player1_left, player1_right, player1_attack1,
                           player1_attack2]:
                button.hover(player1_mouse)
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
                    if player1_back.checkForInput(player1_mouse):
                        leave_menu = True
                        break
                    if player1_up.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "jump")
                    if player1_down.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "block")
                    if player1_left.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "left")
                    if player1_right.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "right")
                    if player1_attack1.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "attack1")
                    if player1_attack2.checkForInput(player1_mouse):
                        self.control_handling(player1_controls, "attack2")
            if leave_menu:
                break
            clock.tick(self.MENU_FPS)
            pygame.display.update()


    # fighter2 controls displayed and mutable
    def player2(self):
        global player2_controls
        leave_menu = False
        clock = pygame.time.Clock()
        while True:
            player2_mouse = pygame.mouse.get_pos()

            menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(menu_scaled, (0, 0))

            player2_text = self.font(50).render("PLAYER 2", True, "#b68f40")
            player2_rect = player2_text.get_rect(center=(500, 65))
            self.screen.blit(player2_text, player2_rect)

            # make player 2 controls with a button
            player2_up = Button(image=None, pos=(500, 150),
                                text_input="Jump : " + pygame.key.name(player2_controls["jump"]), font=self.font(15),
                                base_color="#d7fcd4", hovering_color="White")

            player2_down = Button(image=None, pos=(500, 200),
                                  text_input="Block : " + pygame.key.name(player2_controls["block"]),
                                  font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player2_left = Button(image=None, pos=(500, 250),
                                  text_input="Left : " + pygame.key.name(player2_controls["left"]), font=self.font(15),
                                  base_color="#d7fcd4", hovering_color="White")

            player2_right = Button(image=None, pos=(500, 300),
                                   text_input="Right : " + pygame.key.name(player2_controls["right"]),
                                   font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player2_attack1 = Button(image=None, pos=(500, 350),
                                     text_input="Punch : " + pygame.key.name(player2_controls["attack1"]),
                                     font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player2_attack2 = Button(image=None, pos=(500, 400),
                                     text_input="Projectile : " + pygame.key.name(player2_controls["attack2"]),
                                     font=self.font(15), base_color="#d7fcd4", hovering_color="White")

            player2_back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 475),
                                  text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [player2_back, player2_up, player2_down, player2_left, player2_right, player2_attack1,
                           player2_attack2]:
                button.hover(player2_mouse)
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
                    if player2_back.checkForInput(player2_mouse):
                        leave_menu = True
                        break
                    if player2_up.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "jump")
                        self.control_handling(player2_controls, "jump")
                    if player2_down.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "block")
                    if player2_left.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "left")
                    if player2_right.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "right")
                    if player2_attack1.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "attack1")
                    if player2_attack2.checkForInput(player2_mouse):
                        self.control_handling(player2_controls, "attack2")
            if leave_menu:
                break
            clock.tick(self.MENU_FPS)
            pygame.display.update()


    # options
    def opt(self):
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        leave_menu = False
        clock = pygame.time.Clock()
        while True:
            opt_mouse = pygame.mouse.get_pos()


            self.screen.blit(menu_scaled, (0, 0))

            opt_text = self.font(50).render("OPTIONS", True, "#b68f40")
            opt_rect = opt_text.get_rect(center=(500, 65))
            self.screen.blit(opt_text, opt_rect)

            opt_controls = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 175),
                                  text_input="CONTROLS", font=self.font(35), base_color="#d7fcd4", hovering_color="White")
            opt_audio = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 325),
                               text_input="AUDIO", font=self.font(35), base_color="#d7fcd4", hovering_color="White")
            opt_back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 475),
                              text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

            for button in [opt_controls, opt_audio, opt_back]:
                button.hover(opt_mouse)
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
                    if opt_back.checkForInput(opt_mouse):
                        pygame.display.set_caption("Main Menu")
                        leave_menu = True
                        break
                    if opt_controls.checkForInput(opt_mouse):
                        pygame.display.set_caption("Controls")
                        self.controls()
                    if opt_audio.checkForInput(opt_mouse):
                        pygame.display.set_caption("Audio")
                        self.audio()
            if leave_menu:
                break
            clock.tick(self.MENU_FPS)
            pygame.display.update()


    # create a function to handle audio levels using buttons for sound effects and music
    def audio(self):
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.CREEN_WIDTH, self.SCREEN_HEIGHT))
        leave_menu = False
        clock = pygame.time.Clock()
        while True:
            audio_mouse = pygame.mouse.get_pos()
            self.screen.blit(menu_scaled, (0, 0))

            audio_text = self.font(50).render("AUDIO VOLUME", True, "#b68f40")
            audio_rect = audio_text.get_rect(center=(500, 65))
            self.screen.blit(audio_text, audio_rect)
            music_text = self.font(40).render("MUSIC", True, "#b68f40")
            music_rect = music_text.get_rect(center=(200, 175))
            self.screen.blit(music_text, music_rect)
            audio_back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 475),
                                text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")
            # make 4 buttons for music volume, 1 for each quarter
            music_0 = Button(image=None, pos=(400, 175),
                             text_input="0%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            music_1 = Button(image=None, pos=(510, 175),
                             text_input="25%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            music_2 = Button(image=None, pos=(620, 175),
                             text_input="50%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            music_3 = Button(image=None, pos=(730, 175),
                             text_input="75%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            music_4 = Button(image=None, pos=(840, 175),
                             text_input="100%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")

            # create same buttons as music for sound effects
            sfx_text = self.font(40).render("SFX", True, "#b68f40")
            sfx_rect = sfx_text.get_rect(center=(200, 325))
            self.screen.blit(sfx_text, sfx_rect)
            sfx_0 = Button(image=None, pos=(400, 325),
                           text_input="0%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            sfx_1 = Button(image=None, pos=(510, 325),
                           text_input="25%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            sfx_2 = Button(image=None, pos=(620, 325),
                           text_input="50%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            sfx_3 = Button(image=None, pos=(730, 325),
                           text_input="75%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")
            sfx_4 = Button(image=None, pos=(840, 325),
                           text_input="100%", font=self.font(25), base_color="#d7fcd4", hovering_color="White")

            for button in [audio_back, music_0, music_1, music_2, music_3, music_4, sfx_0, sfx_1, sfx_2, sfx_3, sfx_4]:
                button.hover(audio_mouse)
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
                        self.sfx_change(0)
                    if sfx_1.checkForInput(audio_mouse):
                        self.sfx_change(1)
                    if sfx_2.checkForInput(audio_mouse):
                        self.sfx_change(2)
                    if sfx_3.checkForInput(audio_mouse):
                        self.sfx_change(3)
                    if sfx_4.checkForInput(audio_mouse):
                        self.sfx_change(4)
            if leave_menu:
                break
            clock.tick(self.MENU_FPS)
            pygame.display.update()


    #new menu for when you click play, it should have a "local multiplayer" and a "singleplayer" button
    def menu_play(self):
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        single_player = Button(image=pygame.image.load(self.resource_path("assets/menu/long.png")), pos=(500, 150),
                               text_input="SINGLEPLAYER", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        local = Button(image=pygame.image.load(self.resource_path("assets/menu/long.png")), pos=(500, 275),
                       text_input="LOCAL", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        multiplayer = Button(image=pygame.image.load(self.resource_path("assets/menu/long.png")), pos=(500, 400),
                             text_input="MULTIPLAYER", font=self.font(35), base_color="#d7fcd4", hovering_color="White")

        back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 525),
                      text_input="BACK", font=self.font(35), base_color="#d7fcd4", hovering_color="White")
        leave_menu = False
        #clock = pygame.time.Clock()

        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(70).render("GAME MODE", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        self.screen.blit(text, rect)


        for button in [single_player, local, multiplayer, back]:
            button.hover(mouse)
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
                    self.game_state="menu_char"
                    self.single_player=True
                if local.checkForInput(mouse):
                    pygame.display.set_caption("Local Multiplayer")
                    self.game_state = "menu_char"
                if multiplayer.checkForInput(mouse):
                    pygame.display.set_caption("Multi Player Menu")
                    game_client = GameClient(1234)
                    print("connecting to server")
                    game_client.connect("project.michaelc445.container.netsoc.cloud", 17023, "m")
                    print(game_client.player_id)
                    game_client.socket.setblocking(False)
                    self.multi_char_select(game_client)
                    self.multi_player_game_loop(game_client)
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    self.game_state = "main_menu"
            if leave_menu:
                break
            #clock.tick(self.MENU_FPS)

    #character select menu
    def menu_char(self):
        global p1
        global p2

        p1_color_wizard= "#d7fcd4"
        p1_color_warrior= "#d7fcd4"
        p1_color_nomad= "#d7fcd4"

        p2_color_wizard= "#d7fcd4"
        p2_color_warrior= "#d7fcd4"
        p2_color_nomad= "#d7fcd4"
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        leave_menu = False
        #clock = pygame.time.Clock()

        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(35).render("CHARACTER SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        self.screen.blit(text, rect)

        #player 1
        text = self.font(15).render("PLAYER 1", True, "#b68f40")
        rect = text.get_rect(center=(300, 100))
        self.screen.blit(text, rect)

        #player 2
        text = self.font(15).render("PLAYER 2", True, "#b68f40")
        rect = text.get_rect(center=(700, 100))
        self.screen.blit(text, rect)

        play = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(700, 525),
                      text_input="PLAY", font=self.font(35), base_color="Black", hovering_color="Yellow")
        #character select buttons for player 1
        p1_wizard = Button(image=None, pos=(300, 275),
                        text_input="wizard", font=self.font(25), base_color=p1_color_wizard, hovering_color="Yellow")
        p1_warrior = Button(image=None, pos=(300, 400),
                        text_input="warrior", font=self.font(25), base_color=p1_color_warrior, hovering_color="Yellow")
        p1_nomad = Button(image=None, pos=(300, 150),
                        text_input="nomad", font=self.font(25), base_color=p1_color_nomad, hovering_color="Yellow")
        #character select buttons for player 2
        p2_wizard = Button(image=None, pos=(700, 275),
                        text_input="wizard", font=self.font(25), base_color=p2_color_wizard, hovering_color="Blue")
        p2_warrior = Button(image=None, pos=(700, 400),
                        text_input="warrior", font=self.font(25), base_color=p2_color_warrior, hovering_color="Blue")
        p2_nomad = Button(image=None, pos=(700, 150),
                        text_input="nomad", font=self.font(25), base_color=p2_color_nomad, hovering_color="Blue")

        back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(300, 525),
                      text_input="BACK", font=self.font(35), base_color="Black", hovering_color="Yellow")

        for button in [back, play, p1_wizard, p1_warrior, p1_nomad, p2_wizard, p2_warrior, p2_nomad]:
            button.hover(mouse)
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
                #make it so that when you click play, it goes to the game loop
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Map Select")
                    self.game_state = "map_select"
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Main Menu")
                    leave_menu = True
                    break
                if p1_wizard.checkForInput(mouse):
                    p1_color_warrior = "#d7fcd4"
                    p1_color_wizard = "Yellow"
                    p1_color_nomad = "#d7fcd4"
                    self.p1= "wizard"
                if p1_warrior.checkForInput(mouse):
                    p1_color_warrior = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_nomad = "#d7fcd4"
                    self.p1= "warrior"
                if p1_nomad.checkForInput(mouse):
                    p1_color_nomad = "Yellow"
                    p1_color_wizard = "#d7fcd4"
                    p1_color_warrior = "#d7fcd4"
                    self.p1= "nomad"
                if p2_wizard.checkForInput(mouse):
                    p2_color_wizard = "Blue"
                    p2_color_warrior = "#d7fcd4"
                    p2_color_nomad = "#d7fcd4"
                    self.p2= "wizard"
                if p2_warrior.checkForInput(mouse):
                    p2_color_warrior = "Blue"
                    p2_color_nomad = "#d7fcd4"
                    p2_color_wizard = "#d7fcd4"
                    self.p2= "warrior"
                if p2_nomad.checkForInput(mouse):
                    p2_color_nomad = "Blue"
                    p2_color_wizard = "#d7fcd4"
                    p2_color_warrior = "#d7fcd4"
                    self.p2= "nomad"

            if leave_menu:
                break
            #clock.tick(self.MENU_FPS)



    #create a map select screen
    def map_select(self):
        global map
        leave_menu = False
        clock = pygame.time.Clock()
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        text = self.font(35).render("MAP SELECT", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        self.screen.blit(text, rect)

        play = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(700, 525),
                      text_input="PLAY", font=self.font(35), base_color="White", hovering_color="Yellow")
        #map select buttons
        map1 = Button(image=None, pos=(500, 150),
                        text_input="MOUNTAIN", font=self.font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map2 = Button(image=None, pos=(500, 250),
                        text_input="CLIFFS", font=self.font(25), base_color="#d7fcd4", hovering_color="Yellow")
        map3 = Button(image=None, pos=(500, 350),
                        text_input="CHURCH", font=self.font(25), base_color="#d7fcd4", hovering_color="Yellow")

        back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(300, 525),
                      text_input="BACK", font=self.font(35), base_color="White", hovering_color="Yellow")

        for button in [back, play, map1, map2, map3]:
            button.hover(mouse)
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
                #make it so that when you click play, it goes to the game loop
                if play.checkForInput(mouse):
                    pygame.display.set_caption("Game")
                    mixer.music.load(self.resource_path("assets/audio/background-game.wav"))
                    mixer.music.play(-1)
                    #mixer.music.set_volume(0)
                    self.game_state = "game_loop"
                if back.checkForInput(mouse):
                    pygame.display.set_caption("Character Select")
                    leave_menu = True
                    break
                if map1.checkForInput(mouse):
                    self.map = "mountain"
                if map2.checkForInput(mouse):
                    self.map = "cliffs"
                if map3.checkForInput(mouse):
                    self.map = "church"
            if leave_menu:
                break
        clock.tick(self.MENU_FPS)
    def multi_char_select(self,game_client):
        global p1, p2
        default_colour = "#d7fcd4"
        p2_wiz = "#d7fcd4"
        p2_war=  "#d7fcd4"
        p2_nom = "#d7fcd4"
        play = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(700, 525),
                      text_input="PLAY", font=self.font(35), base_color="Black", hovering_color="Yellow")
        # character select buttons for player 1
        p1_wizard = Button(image=None, pos=(300, 275),
                           text_input="wizard", font=self.font(25), base_color=default_colour, hovering_color="Yellow")
        p1_warrior = Button(image=None, pos=(300, 400),
                            text_input="warrior", font=self.font(25), base_color=default_colour, hovering_color="Yellow")
        p1_nomad = Button(image=None, pos=(300, 150),
                          text_input="nomad", font=self.font(25), base_color="Yellow", hovering_color="Yellow")


        back = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(300, 525),
                      text_input="BACK", font=self.font(35), base_color="Black", hovering_color="Yellow")


        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        characters = [p1_nomad,p1_wizard, p1_warrior]

        p_choice = 0
        locked_in = False
        loop = asyncio.get_event_loop()
        l_count=0
        clock = pygame.time.Clock()
        while True:
            mouse = pygame.mouse.get_pos()
            self.screen.blit(menu_scaled, (0, 0))
            if game_client.enemy_quit_game==0:
                try:
                    game_client.socket.close()
                except:
                    pass

                break

            for button in [ back, play, p1_wizard, p1_warrior, p1_nomad]:
                button.hover(mouse)
                button.update(self.screen)
                # character select buttons for player 2
            p2_wizard = Button(image=None, pos=(700, 275),
                                   text_input="wizard", font=self.font(25), base_color=p2_wiz, hovering_color="Blue")
            p2_warrior = Button(image=None, pos=(700, 400),
                                    text_input="warrior", font=self.font(25), base_color=p2_war, hovering_color="Blue")
            p2_nomad = Button(image=None, pos=(700, 150),
                                  text_input="nomad", font=self.font(25), base_color=p2_nom, hovering_color="Blue")
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
                button.update(self.screen)

            text = self.font(35).render("CHARACTER SELECT", True, "#b68f40")
            rect = text.get_rect(center=(500, 50))
            self.screen.blit(text, rect)

            # player 1
            text = self.font(15).render("YOUR PICK", True, "#b68f40")
            rect = text.get_rect(center=(300, 100))
            self.screen.blit(text, rect)

            # player 2
            text = self.font(15).render("ENEMY PICK", True, "#b68f40")
            rect = text.get_rect(center=(700, 100))
            self.screen.blit(text, rect)
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
                        self.main_menu()
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
            self.run_once(loop)
            clock.tick(self.MENU_FPS)

    async def update_lobby(self,game_client):
        loop = asyncio.get_event_loop()
        loop.create_task(game_client.get_enemy_character())

    # main menu
    def main_menu(self):
        menu_scaled = pygame.transform.scale(self.menu_bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        play = Button(image=pygame.image.load(self.resource_path("assets/menu/long.png")), pos=(500, 180),
                      text_input="PLAY", font=self.font(55), base_color="#d7fcd4", hovering_color="White")

        options = Button(image=pygame.image.load(self.resource_path("assets/menu/long.png")), pos=(500, 325),
                         text_input="OPTIONS", font=self.font(55), base_color="#d7fcd4", hovering_color="White")
        quit = Button(image=pygame.image.load(self.resource_path("assets/menu/medium.png")), pos=(500, 470),
                      text_input="QUIT", font=self.font(55), base_color="#d7fcd4", hovering_color="White")
        text = self.font(75).render("Main Menu", True, "#b68f40")
        rect = text.get_rect(center=(500, 50))
        clock = pygame.time.Clock()
        self.screen.blit(menu_scaled, (0, 0))
        mouse = pygame.mouse.get_pos()

        self.screen.blit(text, rect)

        for button in [play, options, quit]:
            button.hover(mouse)
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
        clock.tick(self.MENU_FPS)
        #pygame.display.update()

    #https://stackoverflow.com/a/51266275
    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    async def main(self):
        pygame.init()
        state_map = {"main_menu": self.main_menu, "menu_play": self.menu_play,
                     "menu_char": self.menu_char, "game_loop": self.game_loop, "map_select":self.map_select,"game_run":self.game_run}
        self.run = True
        while self.run:
            draw_func = state_map[self.game_state]
            draw_func()
            await asyncio.sleep(0)
            pygame.display.flip()



app= Main()
asyncio.run(app.main())