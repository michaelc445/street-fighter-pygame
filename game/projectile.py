import pygame

class Projectile():
    def __init__(self, x, y, width, height, damage, knockback, owner, dx, projectileImgs, animationCooldown, projectileSteps):
        self.rect = pygame.Rect((x, y, width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0,255,0)
        self.exists = True
        self.damage = damage
        self.knockback = knockback
        self.owner = owner
        self.dx = dx
        self.direction = self.owner.flip
        self.projectileImgs = projectileImgs
        self.animationCooldown = animationCooldown
        self.numFrames = projectileSteps
        self.updateFrame = pygame.time.get_ticks()
        self.frame = 0

    def draw(self, surface):

        # draw hit boxes
        #pygame.draw.rect(surface, self.color, self.rect)
        if pygame.time.get_ticks() - self.updateFrame > self.animationCooldown:
            if self.frame >= self.numFrames-1:
                self.frame = 0
            self.frame += 1
            self.updateFrame = pygame.time.get_ticks()
        img = self.projectileImgs[self.frame]
        img = pygame.transform.flip(img, self.direction, False)
        img_rect = img.get_rect(center=self.rect.center)
        surface.blit(img, img_rect)
        



    def move(self, target, screen_width):
        #keep projectile on screen
        if (self.rect.left + self.dx < 0) or (self.rect.right + self.dx > screen_width):
            self.exists = False
            
        self.rect.x += self.dx
        if self.rect.colliderect(target.rect):
            if not target.blocking:
                target.take_hit(self.damage, self.knockback, self.direction)
            self.exists = False