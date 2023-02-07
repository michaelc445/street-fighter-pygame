import pygame
from game.fighter import Fighter
from game.projectile import Projectile

class Nomad(Fighter):
    def __init__(self, player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls):
        super().__init__(player, x, y, width, height, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls)

            
        #load nomad sheet
        self.nomadSheet = pygame.image.load("game/assets/nomad/nomad_spritesheet.png")

        self.spriteSheet = self.nomadSheet
        self.sizeX = self.nomadSheetX = 126
        self.sizeY = self.nomadSheetY = 126
        self.scale = self.nomadScale = 2.2
        self.offset = [55, 35]
        self.animationSteps = [10, 7, 6, 11, 8, 3, 3, 3]
        self.animationList = self.loadImages(self.nomadSheet, self.animationSteps)
        self.img = self.animationList[self.action][self.frame]


    def attack(self, surface, target):
        # self.attacking = True
        if self.attack_type == 1:
            if self.attack1_cooldown == 0:
                self.punch_sound.play()
                damage = 10
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                2 * self.rect.width, self.rect.height // 2)
                self.attack1_cooldown = 20

                if attacking_rect.colliderect(target.rect) and not target.blocking:
                    target.take_hit(damage, self.flip)
                    #target.hit = True

                pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

        if self.attack_type == 2:
            if self.attack2_cooldown == 0:
                self.projectile_sound.play()
                self.projectiles.append(
                    Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                                self.rect.height // 2, 10, self, 10 - (20 * self.flip)))
                self.attack2_cooldown = 100