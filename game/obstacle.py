import pygame

class Obstacle():
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect((x,y,width,height))
        self.color = (0,0,0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
    
