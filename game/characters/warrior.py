import pygame
from game.fighter import Fighter
from game.projectile import Projectile

class Warrior(Fighter):
    def __init__(self, player, x, y, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls):
        super().__init__(player, x, y, flip, punch_sound, projectile_sound, hit_sound, player1_controls, player2_controls)


        #hitbox
        height = 100
        width = 60
        self.rect = pygame.Rect((x, y, width, height))

        #character attributes
        self.speed = 8


        #load warrior sheet
        self.warriorSheet = pygame.image.load("game/assets/warrior/warrior_spritesheet.png")

        self.spriteSheet = self.warriorSheet
        self.sizeX = self.warriorSheetX = 135
        self.sizeY = self.warriorSheetY = 135
        self.scale = self.warriorScale = 2.4
        self.offset = [55, 45]
        self.animationSteps = [10, 4, 4, 9, 6, 2, 2, 3]
        self.animationList = self.loadImages(self.warriorSheet, self.animationSteps)
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
                self.attack1_cooldown = 25

                if attacking_rect.colliderect(target.rect) and not target.blocking:
                    target.take_hit(damage, knockback, self.flip)
                    #target.hit = True

                pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

        if self.attack_type == 2:
            if self.attack2_cooldown == 0:
                self.attacking = True
                self.punch_sound.play()
                damage = 20
                knockback = 15
                attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y,
                                             3 * self.rect.width, self.rect.height)
                self.attack2_cooldown = 50

                if attacking_rect.colliderect(target.rect) and not target.blocking:
                    target.take_hit(damage, knockback, self.flip)
                    #target.hit = True

                pygame.draw.rect(surface, (0, 255, 0), attacking_rect)