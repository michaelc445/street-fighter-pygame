import pygame

class Projectile():
    def __init__(self, x, y, width, height, damage, knockback, owner, dx):
        self.rect = pygame.Rect((x,y,width,height))
        self.color = (0,255,0)
        self.exists = True
        self.damage = damage
        self.knockback = knockback
        self.owner = owner
        self.dx = dx

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, target, screen_width):
        #keep projectile on screen
        if (self.rect.left + self.dx < 0) or (self.rect.right + self.dx > screen_width):
            self.exists = False
            

        self.rect.x += self.dx
        if self.rect.colliderect(target.rect):
            if not target.blocking:
                target.take_hit(self.damage, self.knockback, self.owner.flip)
            self.exists = False







        