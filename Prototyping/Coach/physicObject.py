import pygame
from pygame.math import Vector2


#PhysicObject Class will only handle collisions and gravity
class PhysicObject:
    GRAVITY = 2000
    TOLERANCE = 1
    def __init__(self,startPos,size):
        self.pos = Vector2(startPos)
        self.size = Vector2(size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill("red")
        self.rect = self.surface.get_rect(center = self.pos)
        self.vel = Vector2(0)
        self.acc = Vector2(0)
        self.normal = Vector2(0)
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
        self.acc.y = PhysicObject.GRAVITY
        self.vel += self.acc*dt
        dy = self.vel.y*dt
        dx = self.vel.x*dt
        dx,dy = self.checkCollision(dt,dx,dy)
        if abs(dx) < PhysicObject.TOLERANCE:
            dx = 0
        if abs(dy) < PhysicObject.TOLERANCE:
            dy = 0
        self.pos.x += dx
        self.pos.y += dy
              
    def checkCollision(self,dt,dx,dy):
        new_dy = dy
        new_dx = dx
        onGround = False
        futureRectY = self.getNextRect(0,dy)
        futureRectX = self.getNextRect(dx,0)
        for obj in self.collisionObjects:
            if obj.rect.colliderect(futureRectY) and dy < 0:
                self.vel.y = 0
                new_dy = 0
                self.rect.top = obj.rect.bottom + PhysicObject.TOLERANCE
                self.pos = Vector2(self.rect.center)
            if obj.rect.colliderect(futureRectY) and dy > 0:
                self.vel.y = 0
                new_dy = 0
                self.rect.bottom = obj.rect.top
                self.pos = Vector2(self.rect.center)
                onGround = True
            if obj.rect.colliderect(futureRectX) and dx < 0:
                self.vel.x = 0
                new_dx = 0
                self.rect.left = obj.rect.right
                self.pos = Vector2(self.rect.center)    
            if obj.rect.colliderect(futureRectX) and dx > 0:
                self.vel.x = 0
                new_dx = 0
                self.rect.right = obj.rect.left
                self.pos = Vector2(self.rect.center)
            
        self.onGround = onGround
        return new_dx,new_dy

    def getNormal(self):
        self.normal = Vector2(0,-1)
        return self.normal

    def getNextRect(self,dx,dy):
        if abs(dy) < PhysicObject.TOLERANCE:
            if dy > 0:
                dy = PhysicObject.TOLERANCE
            else:
                dy = -1*PhysicObject.TOLERANCE
        return pygame.Rect(self.rect.x + dx, self.rect.y + dy, self.rect.width,self.rect.height)