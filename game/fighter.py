import pygame

class Fighter():
    def __init__(self, player, x, y, width, height, flip):
        self.player = player
        self.flip = flip
        self.rect = pygame.Rect((x,y, width, height))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
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

        #cannot move if attacking
        if self.attacking == False:

        #check player 1 movement
            if self.player == 1:

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
            #check player 2 controls
            if self.player == 2:
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


        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

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

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        #update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + dx , self.rect.y , self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x , self.rect.y + dy , self.rect.width, self.rect.height))
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height , self.rect.width, 10))
        pygame.draw.rect(surface, (230, 176, 30), standing_on_platform_check)
        for obstacle in obstacles:
            if x_collision_check.colliderect(obstacle.rect):
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
            

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            # self.attacking = True
            if self.attack_type == 1:
                damage = 10
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2*self.rect.width, self.rect.height // 2)
                self.attack_cooldown = 30

            if self.attack_type == 2:
                damage = 20
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) , self.rect.centery, 2*self.rect.width, self.rect.height // 2)
                self.attack_cooldown = 100

            if attacking_rect.colliderect(target.rect):
                target.health -= damage
                target.color = (255,255,255)

            pygame.draw.rect(surface, (0,255,0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.color = (255,0,0)

    