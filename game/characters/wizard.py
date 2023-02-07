import pygame
from game.fighter import Fighter
from game.projectile import Projectile

class Wizard(Fighter):
    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls)


        height = 100
        width = 60
        self.rect = pygame.Rect((x, y, width, height))

        #load wizard sheet
        self.wizardSheet = pygame.image.load("game/assets/wizard/wizard_spritesheet.png")

        self.spriteSheet = self.wizardSheet
        self.sizeX = self.wizardSheetX = 231
        self.sizeY = self.wizardSheetY = 190
        self.scale = self.wizardScale = 1.2
        self.offset = [100, 55]
        self.animationSteps = [5, 7, 7, 6, 7, 1, 1, 3]
        self.animationList = self.loadImages(self.wizardSheet, self.animationSteps)
        self.img = self.animationList[self.action][self.frame]

    def attack(self, surface, target):
        # self.attacking = True
        if self.attack_type == 1:
            if self.attack1_cooldown == 0:
                self.projectile_sound.play()
                self.projectiles.append(
                    Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                               self.rect.height // 2, 5, self, 10 - (20 * self.flip)))
                self.attack1_cooldown = 50

        if self.attack_type == 2:
            if self.attack2_cooldown == 0:
                self.projectile_sound.play()
                self.projectiles.append(
                    Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                               self.rect.height, 15, self, 10 - (20 * self.flip)))
                self.attack2_cooldown = 100