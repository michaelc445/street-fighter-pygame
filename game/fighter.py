import pygame
import sys,os
class Fighter(object):
    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
        self.updateFrame = pygame.time.get_ticks()
        self.action = 0  # 0=idle, 1=attack1, 2=attack2, 3=dying, 4=running, 5=jumping, 6=falling, 7=hit
        self.frame = 0
        self.player = player
        self.flip = flip
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.running = False
        self.attacking = False
        self.blocking = False
        #self.blockAnimation = pygame.image.load(self.resource_path("game/assets/projectiles/Wind_Projectile.png"))
        #self.blockingData = [32, 32]
        #self.blockingList = self.loadBlockingImages(self.blockAnimation, 5)
        self.hit = False
        self.shooting_projectile = False
        self.projectiles = []
        self.attack_type = 0
        self.health = 100
        self.attack1_cooldown = 0
        self.attack2_cooldown = 0
        self.color = (255, 0, 0)
        self.punch_sound = punch_sound
        self.projectile_sound = projectile_sound
        self.hit_sound = hit_sound
        self.alive = True
        self.controls = controls
        self._start_x = x
        self._start_y = y

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
        return animationList#

    def loadBlockingImages(self, spriteSheet, animationSteps):
        y = 0
        animationList = []

        for x in range(animationSteps):
            tempImage = spriteSheet.subsurface(x * self.blockingSizeX, 4 * self.blockingSizeY, self.blockingSizeX, self.blockingSizeX)
            tempImage = pygame.transform.scale(tempImage, (self.sizeX * self.blockingScale, self.sizeY * self.blockingScale))
            animationList.append(tempImage)
        return animationList
    def reset(self):
        self.rect.x = self._start_x
        self.rect.y = self._start_y
        self.health = 100
        self.alive = True
        self.vel_x = 0
        self.vel_y = 0
        self.attack1_cooldown = 0
        self.attack2_cooldown = 0
        self.projectiles = []
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def move(self, screen_width, screen_height, surface, target, obstacles):
        GRAVITY = 2
        self.dx = 0
        self.dy = 0

        # check player 1 movement

        self.keybinds(self.controls, surface, target,None)

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

        if self.rect.y > 1000:
            self.health = -1
        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)

    def frameUpdate(self):
        if self.health <= 0:
            # death
            self.health = 0
            self.alive = False
            self.actionUpdate(3)
            animation_cooldown = 250
        elif self.hit:
            # hit
            self.actionUpdate(7)
            animation_cooldown = 120

        elif self.attacking:
            # attack 1
            if self.attack_type == 1:
                self.actionUpdate(1)
                animation_cooldown = 30
            # attack 2
            elif self.attack_type == 2:
                self.actionUpdate(2)
                animation_cooldown = 30

        elif self.jump:
            #jumping
            self.actionUpdate(5)
            animation_cooldown = 30
        elif self.running:
            # running
            self.actionUpdate(4)
            animation_cooldown = 40

        #elif self.blocking:
        #    self.drawBlockAnimation(surface)
        #    animation_cooldown = 40

        else:
            self.actionUpdate(0)
            animation_cooldown = 80

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

    def actionUpdate(self, newAction):
        if newAction != self.action:
            self.frame = 0
            self.action = newAction
            self.updateFrame = pygame.time.get_ticks()

    def drawBlockAnimation(self,surface):
        animationCooldown = 80
        if pygame.time.get_ticks() - self.updateFrame > animationCooldown:
            if self.frame >= self.blockingFrames - 1:
                self.frame = 0
            self.frame += 1
            self.updateFrame = pygame.time.get_ticks()
        surface.blit(self.blockingList[self.frame], (self.rect.x - self.blockingOffset[0] * self.scale, self.rect.y - self.blockingOffset[1] * self.scale))


        return
    def draw(self, surface, player_name, player_colour):
        #draw player

        font = pygame.font.SysFont("impact", 20)
        text_surface = font.render(player_name , True, player_colour)
        surface.blit(text_surface, (self.rect.x, self.rect.y - 20))

        img = pygame.transform.flip(self.img, self.flip, False)
        surface.blit(img, (self.rect.x - self.offset[0] * self.scale, self.rect.y - self.offset[1] * self.scale))

        if self.blocking:
            self.drawBlockAnimation(surface)


    def take_hit(self, damage, knockback, direction):
        self.hit = True
        self.hit_sound.play()
        self.health -= damage
        self.color = (255, 255, 255)
        self.vel_x += (knockback - 2 * knockback * direction)
        self.vel_y -= knockback
    def draw_projectile(self,target,screen_width,surface):

        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)

    def keybinds(self, player_controls, surface, target,key):
        # get keypresses
        if key is None:
            key = pygame.key.get_pressed()
        self.running = False
        #self.jump = False  # uncomment this to fly :)

        if not self.blocking and not self.attacking and self.alive:
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

    def grav(self, gravity):
        self.vel_y += gravity
        if self.vel_x > 0:
            self.vel_x -= 0.5
        if self.vel_x < 0:
            self.vel_x += 0.5
        self.dy += self.vel_y
        self.dx += self.vel_x

    def obstacle_collision(self, surface, obstacles):
        # update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height))

        # draw feet of character
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, 10))
        #pygame.draw.rect(surface, (230, 176, 30), standing_on_platform_check)
        for obstacle in obstacles:
            if x_collision_check.colliderect(obstacle.rect):
                self.vel_x = -self.vel_x
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
            # bounce off wall if knocked into it
            self.vel_x = -self.vel_x

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right
            # bounce off wall if knocked into it
            self.vel_x = -self.vel_x

        #if self.rect.bottom + self.dy > screen_height - 100:
        #    self.vel_y = 0
        #   self.dy = screen_height - 100 - self.rect.bottom
        #    self.jump = False

        
