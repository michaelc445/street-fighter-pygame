import pygame, os
from network import game_client
from proto import game_pb2 as pb

print(os.getcwd())


class Fighter():
    def __init__(self, player, x, y, width, height, flip,speed,gravity):
        self.player = player
        self.flip = flip
        self.rect = pygame.Rect((x, y, width, height))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.attack_cooldown = 0
        self.color = (255, 0, 0)
        self.SPEED = speed
        self.GRAVITY= gravity
        self.dx=0
        self.dy=0
        self.game_keys = [pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_r,pygame.K_t]

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
    def move_new(self, screen_width, screen_height, surface, target, obstacles,game_client):
        self.dx=0
        self.dy=0
        # get keypresses
        key = pygame.key.get_pressed()
        t = {z: True for z in self.game_keys if key[z]}
        message = pb.Update(keys=t)
        message.health = self.health
        message.enemyMove=0
        message.moving=False
        message.enemyHealth = target.health
        message.enemyAttack = 0
        message.x = self.rect.x
        message.y = self.rect.y
        # cannot move if attacking

        if self.attacking == False:
            # check player 1 movement
            # movement
            if pygame.K_a in t:
                self.dx = -self.SPEED
                message.enemyMove =1
                ##game_client.send_update(message)

            if pygame.K_d in t:
                self.dx = self.SPEED
                message.enemyMove = 2
                ##game_client.send_update(message)

            # jump
            if pygame.K_w in t and not self.jump:
                self.vel_y = -30
                self.jump = True
                message.enemyMove= 3
                ##game_client.send_update(message)
            # attack
            if pygame.K_r in t or pygame.K_t in t:
                # determine attack type
                if pygame.K_r in t:
                    self.attack_type = 1
                    message.enemyAttack = 1
                if pygame.K_t in t:
                    self.attack_type = 2
                    message.enemyAttack = 2
                ##game_client.send_update(message)
                self.attack(surface, target)

        # apply gravity
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # keep players on screen
        if self.rect.left + self.dx < 0:
            self.dx = -self.rect.left

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right

        if self.rect.bottom + self.dy > screen_height - 100:
            self.vel_y = 0
            self.dy = screen_height - 100 - self.rect.bottom
            self.jump = False

        # face direction of other player
        self.face_enemy(target)
        # update player position
        message.x = self.rect.x
        message.y = self.rect.y
        game_client.send_update(message)
        self.update_player(self.dx, self.dy, obstacles, surface)

    def move_enemy2(self, screen_width, screen_height, surface, target, obstacles,game_client,key):
        self.dx=0
        self.dy=0
        # get keypresses

        message = pb.Update()
        message.health = self.health
        message.enemyMove=0
        message.moving=False
        message.enemyHealth = target.health
        message.enemyAttack = 0
        message.x = self.rect.x
        message.y = self.rect.y
        # cannot move if attacking
        if self.attacking == False:
            # check player 1 movement
            # movement
            if key[pygame.K_a]:
                self.dx = -self.SPEED
                message.enemyMove =1
                game_client.send_update(message)

            if key[pygame.K_d]:
                self.dx = self.SPEED
                message.enemyMove = 2
                game_client.send_update(message)

            # jump
            if key[pygame.K_w] and not self.jump:
                self.vel_y = -30
                self.jump = True
                message.enemyMove= 3
                game_client.send_update(message)
            # attack
            if key[pygame.K_r] or key[pygame.K_t]:
                # determine attack type
                if key[pygame.K_r]:
                    self.attack_type = 1
                    message.enemyAttack = 1
                if key[pygame.K_t]:
                    self.attack_type = 2
                    message.enemyAttack = 2
                game_client.send_update(message)
                self.attack(surface, target)

        # apply gravity
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # keep players on screen
        if self.rect.left + self.dx < 0:
            self.dx = -self.rect.left

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right

        if self.rect.bottom + self.dy > screen_height - 100:
            self.vel_y = 0
            self.dy = screen_height - 100 - self.rect.bottom
            self.jump = False

        # face direction of other player
        self.face_enemy(target)
        # update player position
        message.x = self.rect.x
        message.y = self.rect.y
        ##game_client.send_update(message)
        self.update_player(self.dx, self.dy, obstacles, surface)
    def move_enemy(self,screen_width, screen_height, surface, target, obstacles,message):
        self.dx = 0
        self.dy = 0

        # get keypresses
        key = pygame.key.get_pressed()
        # cannot move if attacking

        if not message.enemyAttack:
            # check player 1 movement
            # movement
            if message.enemyMove == 1:
                self.dx = -self.SPEED

            if message.enemyMove == 2:
                self.dx = self.SPEED

            # jump
            if message.enemyMove == 3 and not self.jump:
                self.vel_y = -30
                self.jump = True
            # attack
            if message.enemyAttack != 0:
                # determine attack type
                self.attack_type = message.enemyAttack
                self.attack(surface, target)

        # apply gravity
        self.vel_y += self.GRAVITY
        self.dy += self.vel_y

        # keep players on screen
        if self.rect.left + self.dx < 0:
            self.dx = -self.rect.left

        if self.rect.right + self.dx > screen_width:
            self.dx = screen_width - self.rect.right

        if self.rect.bottom + self.dy > screen_height - 100:
            self.vel_y = 0
            self.dy = screen_height - 100 - self.rect.bottom
            self.jump = False

        # face direction of other player
        self.face_enemy(target)
        # update player position
        self.rect.x = message.x
        self.rect.y = message.y
        self.update_player(self.dx, self.dy, obstacles, surface)

    def face_enemy(self, target):
        # face direction of other player
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def update_player(self, dx, dy, obstacles, surface):
        # update player position
        updatex, updatey = True, True
        x_collision_check = pygame.Rect((self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height))
        y_collision_check = pygame.Rect((self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height))
        standing_on_platform_check = pygame.Rect((self.rect.x, self.rect.y + self.rect.height, self.rect.width, 10))
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
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                             2 * self.rect.width, self.rect.height // 2)
                self.attack_cooldown = 0

            if self.attack_type == 2:
                damage = 20
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.centery,
                                             2 * self.rect.width, self.rect.height // 2)
                self.attack_cooldown = 0

            if attacking_rect.colliderect(target.rect):
                target.health -= damage
                target.color = (255, 255, 255)

            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        self.color = (255, 0, 0)
