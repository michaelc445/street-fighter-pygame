import pygame
from game.projectile import Projectile
from game.fighter import Fighter
from proto import game_pb2 as pb
class OnlineFighter(Fighter):

    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)
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
        self.keybinds(self.controls, surface, target, SPEED, keys)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1

        # count projectile cooldown
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1

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
        self.keybinds(self.controls, surface, target, speed, key)

        self.grav(gravity)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1

        # count projectile cooldown
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1


        # update projectiles



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
