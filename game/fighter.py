import pygame
from game.projectile import Projectile
from proto import game_pb2 as pb

class Fighter():
    #wizardData = ["game/assets/wizard/", 231, 190, 7]

    def __init__(self, player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls):
        # self.animationList = self.loadImages(spriteSheet, 5)
        self.updateFrame = pygame.time.get_ticks()
        self.action = 0  # 0=idle, 1=attack1, 2=attack2, 3=dying, 4=running, 5=jumping, 6=falling, 7=hit
        self.frame = 0
        self.player = player
        self.flip = flip
        self.rect = pygame.Rect((x, y, width, height))
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.running = False
        self.attacking = False
        self.blocking = False
        self.hit = False
        self.shooting_projectile = False
        self.projectiles = []
        self.attack2_cooldown = 0
        self.attack_type = 0
        self.health = 100
        self.attack1_cooldown = 0
        self.color = (255, 0, 0)
        self.punch_sound = punch_sound
        self.projectile_sound = projectile_sound
        self.hit_sound = hit_sound
        self.alive = True
        self.player1_controls = player1_controls
        self.player2_controls = player2_controls


    def loadImages(self, spriteSheet, animationSteps):
        # extract images from sprite sheet
        y = 0
        animationList = []
        for animation in animationSteps:
            tempImageList = []
            for x in range(animation):
                tempImage = spriteSheet.subsurface(x * self.sizeX, y * self.sizeY, self.sizeX, self.sizeY)
                tempImage = pygame.transform.scale(tempImage, (self.sizeX * self.scale, self.sizeY * self.scale))
                tempImageList.append(tempImage)
            animationList.append(tempImageList)
            y += 1
        return animationList

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

    def frameUpdate(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.actionUpdate(3)
        elif self.running:
            self.actionUpdate(4)
        elif self.jump:
            self.actionUpdate(5)
        elif self.hit:
            self.actionUpdate(7)
        elif self.attacking:
            if self.attack_type == 1:
                self.actionUpdate(1)
            else:
                self.actionUpdate(2)
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
                    self.attack_cooldown = 20
                #check if damage was taken
                if self.action == 7:
                    self.hit = False
                        #if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
                    self.frame = 0

    def actionUpdate(self, newAction):

        if newAction != self.action:
            self.frame = 0
            self.action = newAction
            self.updateFrame = pygame.time.get_ticks()



    def draw(self, surface):
        #draw hitbox of player
        pygame.draw.rect(surface, self.color, self.rect)
        self.color = (255, 0, 0)

        #draw player
        img = pygame.transform.flip(self.img, self.flip, False)
        surface.blit(img, (self.rect.x - self.offset[0] * self.scale, self.rect.y - self.offset[1] * self.scale))

    def take_hit(self, damage, direction):
        self.hit = True
        self.hit_sound.play()
        self.health -= damage
        self.color = (255, 255, 255)
        self.vel_x += (damage - 2 * damage * direction)
        self.vel_y -= damage

    def keybinds(self, player_controls, surface, target, speed):
        # get keypresses
        key = pygame.key.get_pressed()
        self.running = False
        #self.jump = False  # uncomment this to fly :)

        if not self.blocking:
            # move left
            if key[player_controls["left"]]:
                self.dx = -speed
                #        self.actionUpdate(4)
                self.running = True
                self.flip = True
            # move right
            if key[player_controls["right"]]:
                self.dx = speed
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
                    self.attacking = True
                if key[player_controls["attack2"]]:
                    self.attack_type = 2
                    self.attacking = True


                self.attack(surface, target)

        # block
        if key[player_controls["block"]]:
            self.color = (0, 0, 255)
            self.blocking = True
        else:
            self.blocking = False

    def grav(self, gravity):
        self.vel_y += gravity
        if self.vel_x > 0:
            self.vel_x -= 0.5
        if self.vel_x < 0:
            self.vel_x += 0.5
        self.dy += self.vel_y
        self.dx += self.vel_x

    def feet(self, surface, obstacles):
        # update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height))

        # draw feet of character
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, 10))
        #pygame.draw.rect(surface, (230, 176, 30), standing_on_platform_check)
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
        message = self._create_update_message(keys, target)
        self.game_client.send_update(message)

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

        self.feet(surface, obstacles)
        # update projectiles
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