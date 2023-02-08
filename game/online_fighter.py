import pygame
from game.fighter import Fighter
from proto import game_pb2 as pb


class OnlineFighter(Fighter):

    def __init__(self, player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls):
        super().__init__(player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls)
        self.game_client = None
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t]

    def _create_update_message(self, key, target):
        t = {z: True for z in self.game_keys if key[z]}
        message = pb.Update(keys=t)
        message.health = self.health
        message.enemyMove = 0
        message.moving = False
        message.enemyHealth = target.health
        message.enemyAttack = 0
        message.x = self.rect.x
        message.y = self.rect.y
        message.id = self.game_client.player_id
        return message

    def move(self, screen_width, screen_height, surface, target, obstacles, game_client):
        GRAVITY = 2
        self.dx = 0
        self.dy = 0
        # check player movement
        keys = pygame.key.get_pressed()
        self.keybinds(self.player1_controls, surface, target, keys)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        #keep player from phasing through obstacles
        self.obstacle_collision(surface, obstacles)

        # count attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1

        # count projectile cooldown
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1

        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)

        message = self._create_update_message(keys, target)
        self.game_client.send_update(message)

    def move_enemy(self, screen_width, screen_height, surface, target, obstacles, key,x,y):
        GRAVITY = 2
        self.dx = 0
        self.dy = 0
        self.x = x
        self.y = y

        #check player movement
        self.keybinds(self.player1_controls, surface, target, key)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        #keep player from phasing through obstacles
        self.obstacle_collision(surface, obstacles)

        # count attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1

        # count projectile cooldown
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1

        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)


    def keybinds(self, player_controls, surface, target, key):
        self.running = False
        #self.jump = False  # uncomment this to fly :)

        if not self.blocking and not self.attacking:
            # move left
            if key[player_controls["left"]]:
                self.dx = -self.speed
                #        self.actionUpdate(4)
                self.running = True
                self.flip = True
            # move right
            if key[player_controls["right"]]:
                self.dx = self.speed
                #       self.actionUpdate(4)
                self.running = True

                self.flip = False

            # jump
            if key[player_controls["jump"]] and not self.jump:
                self.vel_y = -30
                self.jump = True
                #self.actionUpdate(5)

            # attack
            if key[player_controls["attack1"]] or key[player_controls["attack2"]]:
                # determine attack type
                if key[player_controls["attack1"]]:
                    self.attack_type = 1
                if key[player_controls["attack2"]]:
                    self.attack_type = 2


                self.attack(surface, target)

        # block
        if key[player_controls["block"]]:
            self.color = (0, 0, 255)
            self.blocking = True
        else:
            self.blocking = False