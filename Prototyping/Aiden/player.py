import pygame
from pygame.math import Vector2
from physicObject import PhysicObject

class Player:
    states = {
        "idle" : 0,
        "move" : 1,
        "jump" : 2
    }
    def __init__(self,startPos,size):
        self.physicObject = PhysicObject(startPos,size)
        self.image = self.physicObject.surface
        self.direction = Vector2(0)
        self.maxSpeed = 300
        self.acc = 700
        self.deAcc = 700
        self.currentState = Player.states["idle"]

    def update(self,dt,collisionObjects):
        # self.direction = self.getInput()
        # self.moveX(dt)
        if self.currentState == Player.states["idle"]:
            self.idleUpdate(dt)
        elif self.currentState == Player.states["move"]:
            self.moveUpdate(dt)
        self.physicObject.update(dt,collisionObjects)

    def draw(self,screen):
        screen.blit(self.image,self.physicObject.rect)

    def getInput(self):
        inputVector = Vector2(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            inputVector.x = -1
        if keys[pygame.K_d]:
            inputVector.x = 1
        return inputVector
    
    def moveX(self,dt):
        if self.direction.x == 0:
            speedChange = self.deAcc*dt
        else:
            speedChange = self.acc*dt
        currentXVel = Vector2(self.physicObject.vel.x, 0)
        desiredXVel = Vector2(self.maxSpeed*self.direction.x,0)
        currentXVel.move_towards_ip(desiredXVel,speedChange)
        self.physicObject.vel.x = currentXVel.x

    def idleUpdate(self,dt):
        currentState = self.currentState
        self.image.fill("green")
        if self.getInput() != Vector2(0):
            currentState = Player.states["move"]
            self.direction = self.getInput()
        self.moveX(dt)
        self.currentState = currentState

    def moveUpdate(self,dt):
        currentState = self.currentState
        self.image.fill("red")
        self.direction = self.getInput()
        self.moveX(dt)
        if self.direction == Vector2(0):
            currentState = Player.states["idle"]
        self.currentState = currentState

        