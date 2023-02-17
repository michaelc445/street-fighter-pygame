import pygame

class Projectile():
    def __init__(self, x, y, width, height, damage, knockback, owner, dx, projectile_img):
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
        self.projectile_img = self.loadImage(projectile_img)


    def loadImage(self, img):
       #images = []
       #for img in imgs:
       #    temp_img = pygame.image.load(img)
       #    temp_img = pygame.transform.scale(temp_img, (self.rect.width, self.rect.height))
       #    images.append(temp_img)

        image = pygame.image.load(img)
        image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        return image
    def draw(self, surface):
        # Load the image

        # Create a new surface from a rectangular portion of the image
        #img = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        img = self.projectile_img
        # Center the image on the rectangle
        img_rect = img.get_rect(center=self.rect.center)

        pygame.draw.rect(surface, self.color, self.rect)
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







        