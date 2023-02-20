import pygame
from game.projectile import Projectile

def createWizard(inherit_from, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
    class Wizard(inherit_from):
        def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls):
            super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)

            #hitbox
            height = 100
            width = 60
            self.rect = pygame.Rect((x, y, width, height))




            #character attributes
            self.speed = 8

            #load wizard sheet
            self.wizardSheet = pygame.image.load(inherit_from.resource_path("game/assets/wizard/wizard_spritesheet.png"))
            self.spriteSheet = self.wizardSheet
            self.sizeX = self.wizardSheetX = 231
            self.sizeY = self.wizardSheetY = 190
            self.scale = self.wizardScale = 1.2
            self.offset = [100, 55]
            self.animationSteps = [5, 7, 7, 6, 7, 1, 1, 3]
            self.animationList = self.loadImages(self.wizardSheet, self.animationSteps)
            self.img = self.animationList[self.action][self.frame]

        def attack(self, surface, target):
            #animation = [ file, number of frames, x, y, animation cooldown ]
            crossed = ["game/assets/projectiles/crossedSpritesheet.png", 5, 32, 32, 40]
            pulse = ["game/assets/projectiles/pulseSpritesheet.png", 3, 63, 32, 120]
            orbSpell = ["game/assets/projectiles/17_felspell_spritesheet.png", 7, 100, 100, 50]

            if self.attack_type == 1:
                if self.attack1_cooldown == 0:
                    self.attacking = True
                    damage = 5
                    knockback = 5
                    self.projectile_sound.play()
                    self.projectiles.append(
                        Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, self.rect.width,
                                self.rect.height // 2, damage, knockback, self, 10 - (20 * self.flip), pulse))
                    self.attack1_cooldown = 50

            if self.attack_type == 2:
                if self.attack2_cooldown == 0:
                    self.attacking = True
                    damage = 15
                    knockback = 10
                    self.projectile_sound.play()
                    self.projectiles.append(
                        Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                                self.rect.height, damage, knockback, self, 5 - (10 * self.flip), orbSpell))
                    self.attack2_cooldown = 150

    return Wizard(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)