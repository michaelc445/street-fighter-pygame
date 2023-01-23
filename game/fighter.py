import pygame
from projectile import Projectile

class Fighter():
    def __init__(self, player, x, y, width, height, flip):
        self.player = player
        self.flip = flip
        self.rect = pygame.Rect((x,y, width, height))
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.attacking = False
        self.blocking = False
        self.shooting_projectile = False
        self.projectiles = []
        self.projectile_cooldown = 0
        self.attack_type = 0
        self.health = 100
        self.attack_cooldown = 0
        self.color = (255,0,0)

    def move(self, screen_width, screen_height, surface, target, obstacles):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #check player 1 movement
        if self.player == 1:

            if not self.blocking:
                #movement
                if key[pygame.K_a]:
                    dx = -SPEED

                if key[pygame.K_d]:
                    dx = SPEED

                #jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                #attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    #determine attack type
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

                    self.attack(surface, target)

            #block
            if key[pygame.K_s]:
                self.blocking = True
            else:
                self.blocking = False

            

        #check player 2 controls
        if self.player == 2:

            if not self.blocking:

                #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED

                if key[pygame.K_RIGHT]:
                    dx = SPEED

                #jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                #attack
                if key[pygame.K_n] or key[pygame.K_m]:
                    #determine attack type
                    if key[pygame.K_n]:
                        self.attack_type = 1
                    if key[pygame.K_m]:
                        self.attack_type = 2

                    self.attack(surface, target)


            #block
            if key[pygame.K_DOWN]:
                self.blocking = True
            else:
                self.blocking = False

            

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_x != 0:
            self.vel_x += (0.5 - (1 * self.flip))
        dy += self.vel_y
        dx += self.vel_x

        #change color if blocking
        if self.blocking:
            self.color = (0,0,255)

        #keep players on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom +  dy > screen_height - 100:
            self.vel_y = 0
            dy = screen_height - 100 - self.rect.bottom
            self.jump = False

        #face direction of other player
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #count attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #count projectile cooldown
        if self.projectile_cooldown > 0:
            self.projectile_cooldown -=1
        
        #update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + dx , self.rect.y , self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x , self.rect.y + dy , self.rect.width, self.rect.height))

        #draw feet of character
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height , self.rect.width, 10))
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
            self.rect.x += dx
        if updatey:
            self.rect.y += dy

        #update projectiles
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
                    damage = 10
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height // 2)
                    self.attack_cooldown = 20

                    if attacking_rect.colliderect(target.rect) and not target.blocking:
                        target.take_hit(damage, self)

                    pygame.draw.rect(surface, (0,255,0), attacking_rect)

            if self.attack_type == 2:
                if self.projectile_cooldown == 0:
                    self.projectiles.append(Projectile(self.rect.centerx - (2 * self.rect.width * self.flip) , self.rect.y, 2*self.rect.width, self.rect.height // 2, 5, self, 5 - (10 * self.flip)))
                    self.projectile_cooldown = 100


    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.color = (255,0,0)

    def take_hit(self, damage, target):
        self.health -= damage
        self.color = (255,255,255)
        self.vel_x += (damage - 2*damage * target.flip)
        self.vel_y -= damage

    