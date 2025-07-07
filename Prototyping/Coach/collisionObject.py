import pygame
from pygame.math import Vector2

class CollisionObject:
    def __init__(self,pos,size):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill("blue")
        self.rect = self.surface.get_rect(center = self.pos)
    
    def draw(self,screen):
        screen.blit(self.surface,self.rect)

    def update(self):
        self.pos = self.rect.center
    

