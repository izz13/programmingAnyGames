import pygame
from pygame.math import Vector2

class Camera:
    TOLERANCE = 1
    def __init__(self,size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.rect = self.surface.get_rect()
        self.pos = Vector2(self.rect.center)
        self.vel = Vector2(0)
        self.maxSpeed = 200

    def update(self,world,dt,sprite):
        #self.moveByKeys()
        self.moveByPoint(sprite.rect.center)
        self.move(world,dt)
        self.surface.blit(world,area = self.rect)

    def move(self,world : pygame.Surface,dt):
        if self.vel.magnitude() < Camera.TOLERANCE:
            self.vel = Vector2(0)
        dx = self.vel.x 
        dy = self.vel.y 
        if self.rect.left + dx < world.get_rect().left:
            self.rect.left = world.get_rect().left
            self.vel.x = 0
            dx = 0
            self.pos.x = self.rect.centerx
            self.pos.y = self.rect.centery
        if self.rect.right + dx > world.get_rect().right:
            self.rect.right = world.get_rect().right
            self.vel.x = 0
            dx = 0
            self.pos.x = self.rect.centerx
            self.pos.y = self.rect.centery
        if self.rect.top + dy < world.get_rect().top:
            self.rect.top = world.get_rect().top
            self.vel.y = 0
            dy = 0
            self.pos.x = self.rect.centerx
            self.pos.y = self.rect.centery
        if self.rect.bottom + dy > world.get_rect().bottom:
            self.rect.bottom = world.get_rect().bottom
            self.vel.y = 0
            dy = 0
            self.pos.x = self.rect.centerx
            self.pos.y = self.rect.centery
        self.pos.x += dx
        self.pos.y += dy
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

    def moveByKeys(self):
        self.vel = Vector2(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.maxSpeed
        if keys[pygame.K_LEFT]:
            self.vel.x = -self.maxSpeed
        if keys[pygame.K_UP]:
            self.vel.y = -self.maxSpeed
        if keys[pygame.K_DOWN]:
            self.vel.y = self.maxSpeed
        
        if self.vel != Vector2(0):
            self.vel.clamp_magnitude_ip(self.maxSpeed)

    def moveByPoint(self,point):
        direction = Vector2(point) - self.pos
        distance = direction.magnitude()
        if direction != Vector2(0):
            direction.normalize_ip()
        if distance > Camera.TOLERANCE:
            self.vel = direction*distance
        else:
            self.vel = Vector2(0)
