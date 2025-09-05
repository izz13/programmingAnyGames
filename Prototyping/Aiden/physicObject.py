import pygame
from pygame.math import Vector2


#PhysicObject Class will only handle collisions and gravity
class PhysicObject:
    GRAVITY = 2000
    TOLERANCE = 1
    MAX_MOVEMENT = 32
    MAX_Y_VELOCITY = 16
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
        if dy > PhysicObject.MAX_Y_VELOCITY:
            dy = PhysicObject.MAX_Y_VELOCITY
        dx = self.vel.x*dt
        dx,dy = self.checkCollision(dt,dx,dy)
        #dx,dy = self.new_checkCollision(dt,dx,dy)
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
        currentRect = self.rect
        futureRectY = self.getNextRect(0,dy,currentRect)
        futureRectX = self.getNextRect(dx,0,currentRect)
        for obj in self.collisionObjects:
            if obj.rect.colliderect(futureRectX) and dx < 0:
                if abs(currentRect.left - obj.rect.right) < PhysicObject.MAX_MOVEMENT:
                    self.vel.x = 0
                    new_dx = 0
                    currentRect.left = obj.rect.right
                    futureRectY = self.getNextRect(0,dy,currentRect)
                    futureRectX = self.getNextRect(dx,0,currentRect)
            if obj.rect.colliderect(futureRectX) and dx > 0:
                if abs(currentRect.right - obj.rect.left) < PhysicObject.MAX_MOVEMENT:
                    self.vel.x = 0
                    new_dx = 0
                    currentRect.right = obj.rect.left
                    futureRectY = self.getNextRect(0,dy,currentRect)
                    futureRectX = self.getNextRect(dx,0,currentRect)
            if obj.rect.colliderect(futureRectY) and dy < 0:
                if abs(currentRect.top - obj.rect.bottom) < PhysicObject.MAX_MOVEMENT:
                    self.vel.y = 0
                    new_dy = 0
                    currentRect.top = obj.rect.bottom + PhysicObject.TOLERANCE
                    futureRectY = self.getNextRect(0,dy,currentRect)
                    futureRectX = self.getNextRect(dx,0,currentRect)
            if obj.rect.colliderect(futureRectY) and dy > 0:
                if abs(currentRect.bottom - obj.rect.top) < PhysicObject.MAX_MOVEMENT:
                    self.vel.y = 0
                    new_dy = 0
                    currentRect.bottom = obj.rect.top
                    onGround = True
                    futureRectY = self.getNextRect(0,dy,currentRect)
                    futureRectX = self.getNextRect(dx,0,currentRect)
        distance = Vector2.distance_to(Vector2(currentRect.center),Vector2(self.rect.center))
        if distance < PhysicObject.MAX_MOVEMENT:
            self.pos = Vector2(currentRect.center)
            self.rect = currentRect
        self.onGround = onGround
        return new_dx,new_dy

    def getNormal(self):
        self.normal = Vector2(0,-1)
        return self.normal

    def getNextRect(self,dx,dy,rect):
        if abs(dy) < PhysicObject.TOLERANCE:
            if dy > 0:
                dy = PhysicObject.TOLERANCE
            else:
                dy = -1*PhysicObject.TOLERANCE
        return pygame.Rect(rect.x + dx, rect.y + dy, rect.width,rect.height)