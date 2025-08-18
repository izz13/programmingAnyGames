import pygame
from pygame.math import Vector2
from random import randint

class CollisionObject:
    def __init__(self,pos,size):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill([randint(0,255),randint(0,255),randint(0,255)])
        self.rect = self.surface.get_rect(center = self.pos)
    
    def draw(self,screen):
        screen.blit(self.surface,self.rect)

    def update(self):
        self.pos = self.rect.center
    

