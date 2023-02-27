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
            #self.spriteSheet = self.wizardSheet
            self.sizeX = self.wizardSheetX = 231
            self.sizeY = self.wizardSheetY = 190
            self.scale = self.wizardScale = 1.2
            self.offset = [100, 55]
            self.animationSteps = [5, 7, 7, 6, 7, 1, 1, 3]
            self.animationList = self.loadImages(self.wizardSheet, self.animationSteps)
            self.img = self.animationList[self.action][self.frame]

            self.blockAnimation = pygame.image.load(inherit_from.resource_path("game/assets/blocking2.png"))
            self.blockingSizeX = 100
            self.blockingSizeY = 100
            self.blockingScale = 1.7
            self.blockingSteps = 5
            self.blockingOffset = [85, 40]
            self.blockingList = self.loadBlockingImages(self.blockAnimation, self.blockingSteps)

            # attack 1 animation
            self.projectileAnimation1 = pygame.image.load(inherit_from.resource_path("game/assets/projectiles/pulseSpritesheet.png"))
            self.projectileSteps1 = 3
            self.imgWidth1 = 63
            self.imgHeight1 = 32
            self.offSetX1 = 0
            self.offSetY1 = 0
            self.projectileRect1 = pygame.Rect( self.getProjectile1X(), self.getProjectile1Y(), self.getProjectile1Width(), self.getProjectile1Height())
            self.projectile_imgs1 = self.loadProjectileImages(self.projectileAnimation1, self.projectileSteps1, self.imgWidth1, self.imgHeight1, self.projectileRect1, self.offSetX1, self.offSetY1)
            self.animationCooldown1 = 100
            # attack 2 animation
            self.projectileX = (self.rect.centerx - (2 * self.rect.width * self.flip))
            self.projectileAnimation2 = pygame.image.load(inherit_from.resource_path("game/assets/projectiles/17_felspell_spritesheet.png"))
            self.projectileSteps2 = 7
            self.imgWidth2 = 100
            self.imgHeight2 = 100
            self.offSetX2 = 0
            self.offSetY2 = 0
            self.projectileRect2 = pygame.Rect(self.getProjectile2X(), self.getProjectile2Y(), self.getProjectile2Width(), self.getProjectile2Height())
            self.projectile_imgs2 = self.loadProjectileImages(self.projectileAnimation2, self.projectileSteps2, self.imgWidth2, self.imgHeight2, self.projectileRect2, self.offSetX2, self.offSetY2)
            self.animationCooldown2 = 50



        def getProjectile1X(self):
            return self.rect.centerx - (2 * self.rect.width * self.flip)
        def getProjectile1Y(self):
            return self.rect.y
        def getProjectile1Width(self):
            return self.rect.width
        def getProjectile1Height(self):
            return self.rect.height // 2

        def getProjectile2X(self):
            return self.rect.centerx - (2 * self.rect.width * self.flip)
        def getProjectile2Y(self):
            return self.rect.y
        def getProjectile2Width(self):
            return 2 * self.rect.width
        def getProjectile2Height(self):
            return self.rect.height


        def attack(self, surface, target):

            if self.attack_type == 1:
                if self.attack1_cooldown == 0:
                    self.attacking = True
                    damage = 5
                    knockback = 5
                    self.projectile_sound.play()
                    self.projectiles.append(
                        Projectile(self.getProjectile1X(), self.getProjectile1Y(), self.getProjectile1Width(), self.getProjectile1Height(), damage, knockback, self, 10 - (20 * self.flip), self.projectile_imgs1,  self.animationCooldown1, self.projectileSteps1))
                    self.attack1_cooldown = 50

            if self.attack_type == 2:
                if self.attack2_cooldown == 0:
                    self.attacking = True
                    damage = 15
                    knockback = 10
                    self.projectile_sound.play()
                    self.projectiles.append(
                        Projectile(self.getProjectile2X(), self.getProjectile2Y(), self.getProjectile2Width(), self.getProjectile2Height(), damage, knockback, self, 5 - (10 * self.flip), self.projectile_imgs2, self.animationCooldown2, self.projectileSteps2))
                    self.attack2_cooldown = 150

    return Wizard(player, x, y, flip, punch_sound, projectile_sound, hit_sound,controls)