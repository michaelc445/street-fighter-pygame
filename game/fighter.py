import pygame
from game.projectile import Projectile
from proto import game_pb2 as pb


class Fighter(object):
    def __init__(self, player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound):
        self.player = player
        self.flip = flip
        self.rect = pygame.Rect((x, y, width, height))
        self.vel_y = 0
        self.vel_x = 0
        self.dx = 0
        self.dy = 0
        self.jump = False
        self.attacking = False
        self.blocking = False
        self.shooting_projectile = False
        self.projectiles = []
        self.projectile_cooldown = 0
        self.attack_type = 0
        self.health = 100
        self.attack_cooldown = 0
        self.color = (255, 0, 0)
        self.punch_sound = punch_sound
        self.projectile_sound = projectile_sound
        self.hit_sound = hit_sound
        self.player1_controls = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "attack1": pygame.K_r,
                                 "attack2": pygame.K_t, "block": pygame.K_s}
        self.player2_controls = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP,
                                 "attack1": pygame.K_n, "attack2": pygame.K_m, "block": pygame.K_DOWN}

    def move(self, screen_width, screen_height, surface, target, obstacles):
        SPEED = 10
        GRAVITY = 2
        self.dx = 0
        self.dy = 0

        # check player 1 movement
        if self.player == 1:
            self.keybinds(self.player1_controls, surface, target, SPEED)

        # check player 2 movement
        if self.player == 2:
            self.keybinds(self.player2_controls, surface, target, SPEED)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # count projectile cooldown
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        self.feet(surface, obstacles)

        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)

    def attack(self, surface, target):
        # self.attacking = True
        if self.attack_type == 1:
            if self.attack_cooldown == 0:
                self.punch_sound.play()
                damage = 10
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                             2 * self.rect.width, self.rect.height // 2)
                self.attack_cooldown = 20

                if attacking_rect.colliderect(target.rect) and not target.blocking:
                    target.take_hit(damage, self)

                pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

        if self.attack_type == 2:
            if self.projectile_cooldown == 0:
                self.projectile_sound.play()
                self.projectiles.append(
                    Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                               self.rect.height // 2, 5, self, 10 - (20 * self.flip)))
                self.projectile_cooldown = 100

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.color = (255, 0, 0)

    def take_hit(self, damage, target):
        self.hit_sound.play()
        self.health -= damage
        self.color = (255, 255, 255)
        self.vel_x += (damage - 2 * damage * target.flip)
        self.vel_y -= damage

    def keybinds(self, player_controls, surface, target, speed):
        # get keypresses
        key = pygame.key.get_pressed()

        if not self.blocking:
            # face direction of other player
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # movement
            # move left
            if key[player_controls["left"]]:
                self.dx = -speed
            # move right
            if key[player_controls["right"]]:
                self.dx = speed

            # jump
            if key[player_controls["jump"]] and not self.jump:
                self.vel_y = -30
                self.jump = True

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

    def grav(self, gravity):
        self.vel_y += gravity
        if self.vel_x != 0:
            self.vel_x += (0.5 - (1 * self.flip))
        self.dy += self.vel_y
        self.dx += self.vel_x

    def feet(self, surface, obstacles):
        # update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height))

        # draw feet of character
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, 10))
        pygame.draw.rect(surface, (230, 176, 30), standing_on_platform_check)
        for obstacle in obstacles:
            if x_collision_check.colliderect(obstacle.rect):
                self.vel_x = 0
                updatex = False

            if y_collision_check.colliderect(obstacle.rect):
                updatey = False
                self.vel_y = 0

            if standing_on_platform_check.colliderect(obstacle.rect):
                self.jump = False

        if updatex:
            self.rect.x += self.dx
        if updatey:
            self.rect.y += self.dy

    def bounds(self, screen_width, screen_height):
        # keep players on screen
        if self.rect.left + self.dx < 0:
            self.dx = -self.rect.left
            self.vel_x = 0

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right
            self.vel_x = 0

        if self.rect.bottom + self.dy > screen_height - 100:
            self.vel_y = 0
            self.dy = screen_height - 100 - self.rect.bottom
            self.jump = False


class OnlineFighter(Fighter):

    def __init__(self, player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound):
        super().__init__(player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound)
        self.game_client = None
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t,pygame.K_s]

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
        message.quit=False
        return message

    def move(self, screen_width, screen_height, surface, target, obstacles, game_client):
        SPEED = 10
        GRAVITY = 2
        self.dx = 0
        self.dy = 0
        # check player 1 movement
        keys = pygame.key.get_pressed()
        self.keybinds(self.player1_controls, surface, target, SPEED, keys)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # count projectile cooldown
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1

        self.feet(surface, obstacles)
        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)
        return self._create_update_message(keys, target)


    def move_enemy(self, screen_width, screen_height, surface, target, obstacles, key,x,y):
        speed = 10
        gravity = 2
        self.dx = 0
        self.dy = 0
        self.x=x
        self.y=y
        self.keybinds(self.player1_controls, surface, target, speed, key)

        self.grav(gravity)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # count projectile cooldown
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -= 1


        # update projectiles


    def draw_projectile(self,target,screen_width,surface):

        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)
    def keybinds(self, player_controls, surface, target, speed, key):
        # get keypresses
        if not self.blocking:
            # face direction of other player
            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # movement
            # move left
            if key[player_controls["left"]]:
                self.dx = -speed
            # move right
            if key[player_controls["right"]]:
                self.dx = speed

            # jump
            if key[player_controls["jump"]] and not self.jump:
                self.vel_y = -30
                self.jump = True

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
