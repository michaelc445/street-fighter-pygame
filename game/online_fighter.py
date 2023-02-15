import pygame
from game.projectile import Projectile
from game.fighter import Fighter
from proto import game_pb2 as pb
class OnlineFighter(Fighter):

    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)
        self.game_client = None
        self.game_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t,pygame.K_s]
        self._start_x = x
        self._start_y = y
    def reset(self):
        self.rect.x = self._start_x
        self.rect.y = self._start_y
        self.health = 100
        self.alive = True
        self.jump = False
        self.running = False
        self.attacking = False
        self.blocking = False
        self.hit = False
        self.vel_x = 0
        self.vel_y = 0
        self.attack1_cooldown = 0
        self.attack2_cooldown = 0
        self.frame = 0
        self.projectiles = []

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


