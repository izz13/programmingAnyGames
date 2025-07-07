import pygame
from pygame.math import Vector2

class PhysicObject:
    GRAVITY = 1000
    def __init__(self,startPos,size):
        self.pos = Vector2(startPos)
        self.size = Vector2(size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill("red")
        self.rect = self.surface.get_rect(center = self.pos)
        self.vel = Vector2(0)
        self.acc = Vector2(0)
        self.onGround = False

    def update(self,dt):
        self.move(dt)
        self.rect.center = self.pos

    def draw(self,screen):
        screen.blit(self.surface,self.rect)

    def move(self,dt):
        self.checkIfOnGround(dt)
        if not self.onGround:
            self.acc.y = PhysicObject.GRAVITY
        else:
            self.acc.y = 0
        self.vel += self.acc*dt
        self.pos += self.vel*dt
        self.onGround = False

    def checkIfOnGround(self,dt):
        fallStep = PhysicObject.GRAVITY * dt
        if self.rect.bottom + fallStep > 600:
            self.rect.bottom = 600
            self.pos = self.rect.center
            self.vel.y = 0
            self.onGround = True
