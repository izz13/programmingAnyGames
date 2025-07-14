import pygame
from pygame.math import Vector2


#PhysicObject Class will only handle collisions and gravity
class PhysicObject:
    GRAVITY = 1000
    TOLERANCE = 1
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

    def update(self,dt,collisionObjects):
        self.collisionObjects = collisionObjects
        self.move(dt)
        self.rect.center = self.pos
        #print(self.onGround)

    def draw(self,screen):
        screen.blit(self.surface,self.rect)

    def move(self,dt):
        #self.onGround = False
        if not self.onGround:
            self.acc.y = PhysicObject.GRAVITY
        else:
            self.acc.y = 0
        self.vel += self.acc*dt
        #self.pos += self.vel*dt
        dy = self.vel.y*dt
        dx = self.vel.x*dt
        self.checkIfOnGround(dt,dy)
        if abs(dx) < PhysicObject.TOLERANCE:
            dx = 0
        if abs(dy) < PhysicObject.TOLERANCE:
            dy = 0
        self.pos.x += dx
        self.pos.y += dy
        

    def checkIfOnGround(self,dt,dy):
        onGround = False
        if abs(dy) < PhysicObject.TOLERANCE:
            fallStep = PhysicObject.GRAVITY * dt
        else:
            fallStep = dy
        futureRect = pygame.Rect(self.rect.x, self.rect.y + fallStep, self.rect.width,self.rect.height)
        for obj in self.collisionObjects:
            if obj.rect.colliderect(futureRect):
                dy = 0
                self.vel.y = 0
                self.rect.bottom = obj.rect.top
                self.pos = Vector2(self.rect.center)
                onGround = True
                break
        self.onGround = onGround
