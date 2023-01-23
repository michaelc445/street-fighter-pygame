import pygame

class Projectile():
    def __init__(self, x, y, width, height, damage, owner):
        self.rect = pygame.Rect((x,y,width,height))
        self.color = (0,255,0)
        self.exists = True
        self.damage = damage
        self.owner = owner

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx, target, screen_width):
        #keep projectile on screen
        if (self.rect.left + dx < 0) or (self.rect.right + dx > screen_width):
            self.exists = False
            

        self.rect.x += dx
        if self.rect.colliderect(target.rect):
            if not target.blocking:
                target.take_hit(self.damage, self.owner)
            self.exists = False







        