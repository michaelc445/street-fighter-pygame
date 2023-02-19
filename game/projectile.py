import pygame

class Projectile():
    def __init__(self, x, y, width, height, damage, knockback, owner, dx, projectile_data, ):
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
        self.animate = True
        if projectile_data == False:
            self.animate = False
        else:
            self.numFrames = projectile_data[1]
            self.imgX = projectile_data[2]
            self.imgY = projectile_data[3]
            self.projectile_imgs = self.loadImages(projectile_data[0], self.numFrames)



        self.updateFrame = pygame.time.get_ticks()
        self.frame = 0

    def loadImages(self, spriteSheet, numFrames):
        print(self.numFrames)
        spriteSheet = pygame.image.load(spriteSheet)
        animationList = []
        for frame in range(numFrames):
            tempImage = spriteSheet.subsurface(frame * self.imgX, 0 * self.imgY, self.imgX, self.imgY)
            tempImage = pygame.transform.scale(tempImage, (self.rect.height, self.rect.width))
            animationList.append(tempImage)
        return animationList
    def draw(self, surface):

        animation_cooldown = 80
        if self.animate == True:
            if pygame.time.get_ticks() - self.updateFrame > animation_cooldown:
                if self.frame == self.numFrames:
                    self.frame = 0
                img = self.projectile_imgs[self.frame]
                self.frame += 1
                #print(self.frame)
                img_rect = img.get_rect(center=self.rect.center)
                surface.blit(img, img_rect)
                self.updateFrame = pygame.time.get_ticks()

    def move(self, target, screen_width):
        #keep projectile on screen
        if (self.rect.left + self.dx < 0) or (self.rect.right + self.dx > screen_width):
            self.exists = False
            
        self.rect.x += self.dx
        if self.rect.colliderect(target.rect):
            if not target.blocking:
                target.take_hit(self.damage, self.knockback, self.direction)
            self.exists = False







        