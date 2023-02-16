import pygame
from game.projectile import Projectile
from game.fighter import Fighter
from game.proto import game_pb2 as pb
class OnlineFighter(Fighter):

    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)
        self.game_client = None
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t,pygame.K_s]


    def _create_update_message(self, key, target):
        t = {z: True for z in self.game_keys if key[z]}
        message = pb.Update(keys=t,
                            health=self.health,
                            moving=False,
                            enemyHealth=target.health,
                            enemyAttack=0,
                            enemyMove=0,
                            x=self.rect.x,
                            y=self.rect.y,
                            id=self.game_client.player_id,
                            quit=False,
                            restart=False)

        return message

    def move(self, screen_width, screen_height, surface, target, obstacles, game_client):
        SPEED = 10
        GRAVITY = 2
        self.dx = 0
        self.dy = 0
        # check player 1 movement
        keys = pygame.key.get_pressed()
        self.keybinds(self.controls, surface, target, keys)

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



        self.obstacle_collision(surface, obstacles)
        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)


        return self._create_update_message(keys, target)

    def frameUpdate(self):
        if self.health < 0:
            self.health = 0
            self.alive = False
            self.actionUpdate(3)
        elif self.hit:
            self.actionUpdate(7)
        elif self.attacking:
            if self.attack_type == 1:
                self.actionUpdate(1)
            elif self.attack_type == 2:
                self.actionUpdate(2)
        elif self.jump:
            self.actionUpdate(5)
        elif self.running:
            self.actionUpdate(4)
        else:
            self.actionUpdate(0)

        animation_cooldown = 30
        #update image
        self.img = self.animationList[self.action][self.frame]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.updateFrame > animation_cooldown:
            self.frame += 1
            self.updateFrame = pygame.time.get_ticks()
        #check if the animation has finished
        if self.frame >= len(self.animationList[self.action]):
            #if the player is dead then end the animation
            if self.alive == False:
                self.frame = len(self.animationList[self.action]) - 1
            else:
                self.frame = 0
                    #check if an attack was executed
                if self.action == 1 or self.action == 2:
                    self.attacking = False
                #check if damage was taken
                if self.action == 7:
                    self.hit = False
                        #if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.frame = 0

    def move_enemy(self, screen_width, screen_height, surface, target, obstacles, key,x,y):
        speed = 10
        gravity = 2
        self.dx = 0
        self.dy = 0
        self.x=x
        self.y=y
        self.keybinds(self.controls, surface, target, key)

        self.grav(gravity)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # count attack cooldown
        if self.attack1_cooldown > 0:
            self.attack1_cooldown -= 1

        # count projectile cooldown
        if self.attack2_cooldown > 0:
            self.attack2_cooldown -= 1

        # check if they fell off the map
        if self.rect.y > 1000:
            self.health = -1


