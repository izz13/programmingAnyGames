import pygame
from pygame.math import Vector2
from animator import Animator
from physicObject import PhysicObject

class Enemy:
    def __init__(self,startPos,size,name):
        self.states = {
            "idle" : 0,
            "move" : 1,
            "fall" : 2
        }
        self.pos = Vector2(startPos)
        self.size = Vector2(size)
        self.name = name
        self.physicObject = PhysicObject(self.pos,self.size)
        self.maxSpeed = 300
        self.acc = 5000
        self.deAcc = 2000
        self.currentState = self.states["idle"]
        self.facingLeft = True
        self.setAnimationClips()
        self.currentAnimation = self.idleAnimation

    def setAnimationClips(self):
        self.idleAnimation = Animator("Prototyping/Aiden/robotIdleFrames",[64,64],"idle")
        self.moveAnimation = Animator("Prototyping/Aiden/robotRunFrames", [64,64], "move")
        self.fallAnimation = Animator("Prototyping/Aiden/robotFallFrames",[64,64], "fall", loop = False)

    def update(self,dt,collisionObjects):
        if self.currentState == self.states["idle"]:
            self.idleUpdate(dt)
        if self.currentState == self.states["move"]:
            self.moveUpdate(dt)
        if self.currentState == self.states["fall"]:
            self.fallUpdate(dt)
        self.physicObject.update(dt,collisionObjects)

    def draw(self,screen):
        if self.currentState == self.states["idle"]:
            self.currentAnimation = self.idleAnimation
        if self.currentState == self.states["move"]:
            self.currentAnimation = self.moveAnimation
        if self.currentState == self.states["fall"]:
            self.currentAnimation = self.fallAnimation
        if self.currentAnimation != None:
            rect = self.getDrawRect()
            self.currentAnimation.draw(screen,rect,self.facingLeft)
        else:
            screen.blit(self.physicObject.surface,self.physicObject.rect)

    def getDrawRect(self):
        currentImage = self.currentAnimation.frames[self.currentAnimation.frameNumber]
        if self.facingLeft:
            flippedCurrentImage = pygame.transform.flip(currentImage,True,False)
            drawRect = flippedCurrentImage.get_rect()
            drawRect.topright = self.physicObject.rect.topright
        else:
            drawRect = currentImage.get_rect()
            drawRect.topleft = self.physicObject.rect.topleft
        return drawRect
    
    def idleUpdate(self,dt):
        currentState = self.currentState
        if self.physicObject.vel.y > PhysicObject.TOLERANCE:
            currentState = self.states["fall"]
        if self.idleAnimation != None:
            self.idleAnimation.update(dt)
            if currentState != self.currentState:
                self.idleAnimation.reset()
        self.currentState = currentState

    def moveUpdate(self,dt):
        self.currentState = self.states["idle"]

    def fallUpdate(self,dt):
        currentState = self.currentState
        if self.physicObject.onGround:
            currentState = self.states["idle"]
        if self.fallAnimation != None:
            self.fallAnimation.update(dt)
            if self.currentState != currentState:
                self.fallAnimation.reset()
        self.currentState = currentState