import pygame
import sys,os
from game.fighter import Fighter

class Fighter_Bot(Fighter):
    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls)
        self.moves=[0,0,0,0,0,0]
        self.jumping = True

    def set_moves(self,enemy_state):
        enemy_state = enemy_state
        player_move = [0, 0, 0, 0, 0, 0]
        current_state = [self.player_x,self.player_y,self.vel_x,self.vel_y, self.shooting_projectile, self.attacking,
                        self.running , self.jump , self.blocking]

        player_move[4] = 1
        if -150 < (enemy_state[0] - current_state[0]) < 150:  # enemy close
            if -50 < enemy_state[0] - current_state[0] < 50:  # enemy next to
                player_move[4] = 1
                if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                    opponent_up = 1
                    player_move[2] = 1
                if enemy_state[7]:  # enemy attacking
                    player_move[3] = 1  # block
                else:
                    player_move[4] = 1
            elif enemy_state[0] < current_state[0]:  # enemy left
                player_move[0] = 1
                if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                    opponent_up = 1
                    player_move[2] = 1
                if enemy_state[7]:  # enemy attacking
                    player_move[3] = 1  # block
                else:
                    player_move[4] = 1
            else:
                if enemy_state[0] > current_state[0]:
                    opponent_left = 0
                    player_move[1] = 1
                    if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                        opponent_up = 1
                        player_move[2] = 1
                    if enemy_state[7]:  # enemy attacking
                        player_move[3] = 1  # block
                    else:
                        player_move[5] = 1
                else:
                    player_move[0] = 1
                    if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                        opponent_up = 1
                        player_move[2] = 1
                    if enemy_state[7]:  # enemy attacking
                        player_move[3] = 1  # block
                    else:
                        player_move[4] = 1


        else:
            if enemy_state[0] > current_state[0]:
                opponent_left = 0
                player_move[1] = 1
                if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                    opponent_up = 1
                    player_move[2] = 1
                if enemy_state[7]:  # enemy attacking
                    player_move[3] = 1  # block
                else:
                    player_move[5] = 1
            else:
                player_move[0] = 1
                if enemy_state[1] < current_state[1] and (current_state[1] - enemy_state[1]) > 100:  # jump
                    opponent_up = 1
                    player_move[2] = 1
                    if enemy_state[7]:  # enemy attacking
                        player_move[3] = 1  # block
                    else:
                        player_move[4] = 1

        self.moves=player_move
    def move(self, screen_width, screen_height, surface, target, obstacles):
        GRAVITY = 1
        self.dx = 0
        self.dy = 0

        # check player 1 movement

        self.keyBot( surface, target, None)

        # apply gravity
        self.grav(GRAVITY)

        # keep player on screen
        self.bounds(screen_width, screen_height)

        # keep player from phasing through obstacles
        self.obstacle_collision(surface, obstacles)

        # count down cooldowns
        self.tick_cooldowns()

        # die if not on the map
        if self.rect.y > 1000:
            self.health = -1
        # update projectiles
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.move(target, screen_width)
                projectile.draw(surface)
                if not projectile.exists:
                    self.projectiles.remove(projectile)

    def keyBot(self, surface, target,key):
        if key is None:
            key = pygame.key.get_pressed()
        self.running = False

        if not self.blocking and not self.attacking and self.alive:
            # move left
            if self.moves[0] == 1:
                self.dx = -self.speed
                #        self.actionUpdate(4)
                self.running = True
                self.flip = True
            # move right
            if self.moves[1]==1:
                self.dx = self.speed

                self.running = True

                self.flip = False

            # jump
            if self.moves[2]==1 and not self.jump:
                self.vel_y = -self.jump_height
                self.jump = True


            # attack
            elif self.moves[4] ==1 or self.moves[5]==1:
                # determine attack type
                if self.moves[4] ==1 :
                    self.attack_type = 1
                if self.moves[4] ==1 :
                    self.attack_type = 2


                self.attack(surface, target)

        # block
        if self.moves[3]:
            self.color = (0, 0, 255)
            self.blocking = True
        else:
            self.blocking = False


        
