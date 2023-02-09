import pygame
from game.projectile import Projectile

def createNomad(inherit_from, player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls):
    class Nomad(inherit_from):
        def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls):
            super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls)

            #hitbox
            height = 100
            width = 70
            self.rect = pygame.Rect((x, y, width, height))

            #character attributes
            self.speed = 10

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
            if self.attack_type == 1:
                if self.attack1_cooldown == 0:
                    self.attacking = True
                    self.punch_sound.play()
                    damage = 10
                    knockback = 10
                    attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                                    2 * self.rect.width, self.rect.height // 2)
                    self.attack1_cooldown = 20

                    if attacking_rect.colliderect(target.rect) and not target.blocking:
                        target.take_hit(damage, knockback, self.flip)

                    pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

            if self.attack_type == 2:
                if self.attack2_cooldown == 0:
                    self.attacking = True
                    damage = 10
                    knockback = 10
                    self.projectile_sound.play()
                    self.projectiles.append(
                        Projectile(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width,
                                    self.rect.height // 2, damage, knockback, self, 10 - (20 * self.flip)))
                    self.attack2_cooldown = 100

    return Nomad(player, x, y, flip, punch_sound, projectile_sound, hit_sound, controls)