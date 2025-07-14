import pygame
from pygame.math import Vector2


#PhysicObject Class will only handle collisions and gravity
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
        self.collisionObjects = []

    def update(self, dt, collisionObjects):
        self.collisionObjects = collisionObjects
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
        futureRect = pygame.Rect(self.rect.x, self.rect.y + fallStep, self.rect.width, self.rect.height)
        for obj in self.collisionObjects:
            if obj.rect.colliderect(futureRect):
                self.vel.y = 0
                self.rect.bottom = obj.rect.top
                self.pos = self.rect.center
                self.onGround = True
                break
