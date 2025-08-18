import pygame
from pygame.math import Vector2
from physicObject import PhysicObject
from math import sqrt
from animator import Animator

class Player:
    states = {
        "idle" : 0,
        "move" : 1,
        "jump" : 2,
        "fall" : 3
    }
    def __init__(self,startPos,size):
        self.physicObject = PhysicObject(startPos,size)
        self.image = self.physicObject.surface
        self.direction = Vector2(0)
        self.maxSpeed = 300
        self.acc = 5000
        self.deAcc = 900
        self.jumpSpeed = 500
        self.jumpHeight = 175
        self.currentState = Player.states["idle"]
        self.facingLeft = True
        self.events = []
        self.setAnimationClips()

    def setAnimationClips(self):
        self.idleAnimation = Animator("CoachMaster/playerIdleFrames",10,[32,64],"Idle")
        self.runAnimation = Animator("CoachMaster/playerRunFrames",10,[48,64],"Run")
        self.runAnimation.animationSpeed = 2
        self.jumpAnimation = Animator("CoachMaster/playerJumpFrames",7,[48,64],"Jump",loop = False)
        self.fallAnimation = Animator("CoachMaster/playerFallFrames",3,[48,64],"Fall", loop=False)

    def update(self,dt,collisionObjects,events):
        # self.direction = self.getInput()
        # self.moveX(dt)
        #print(self.currentState)
        self.events = events
        if self.currentState == Player.states["idle"]:
            self.idleUpdate(dt)
        elif self.currentState == Player.states["move"]:
            self.moveUpdate(dt)
        elif self.currentState == Player.states["jump"]:
            self.jumpUpdate(dt)
        elif self.currentState == Player.states["fall"]:
            self.fallUpdate(dt)
        self.physicObject.update(dt,collisionObjects)

    def draw(self,screen):
        if self.currentState == Player.states["idle"]:
            self.idleAnimation.draw(screen,self.physicObject.rect,self.facingLeft)
        if self.currentState == Player.states["move"]:
            self.runAnimation.draw(screen,self.physicObject.rect,self.facingLeft)
        if self.currentState == Player.states["jump"]:
            self.jumpAnimation.draw(screen,self.physicObject.rect,self.facingLeft)
        if self.currentState == Player.states["fall"]:
            self.fallAnimation.draw(screen,self.physicObject.rect,self.facingLeft)
        #screen.blit(self.image,self.physicObject.rect)

    def getInput(self):
        inputVector = Vector2(0,0)
        keys = pygame.key.get_pressed()
        keysClicked = pygame.key.get_just_pressed()
        if keys[pygame.K_a]:
            self.facingLeft = True
            inputVector.x = -1
        if keys[pygame.K_d]:
            self.facingLeft = False
            inputVector.x = 1
        if keysClicked[pygame.K_w]:
            inputVector.y = -1
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
        #self.image.fill("green")
        inputVector = self.getInput()
        if inputVector != Vector2(0):
            if inputVector.y == -1 and self.physicObject.onGround:
                self.idleAnimation.reset()
                currentState = Player.states["jump"]
            else:
                self.idleAnimation.reset()
                currentState = Player.states["move"]
            self.direction = self.getInput()
        if self.physicObject.vel.y > PhysicObject.TOLERANCE:
            #print("changing to fall")
            self.idleAnimation.reset()
            currentState = Player.states["fall"]

        self.moveX(dt)
        self.idleAnimation.update(dt)
        self.currentState = currentState

    def moveUpdate(self,dt):
        currentState = self.currentState
        #self.image.fill("red")
        self.direction = self.getInput()
        self.moveX(dt)
        if self.direction == Vector2(0):
            self.runAnimation.reset()
            currentState = Player.states["idle"]
        elif self.direction.y == -1 and self.physicObject.onGround:
            self.runAnimation.reset()
            currentState = Player.states["jump"]
        if self.physicObject.vel.y > PhysicObject.TOLERANCE:
            self.runAnimation.reset()
            #print("changing to fall")
            currentState = Player.states["fall"]
        self.runAnimation.update(dt)
        self.currentState = currentState

    def jumpUpdate(self,dt):
        currentState = self.currentState
        self.direction = self.getInput()
        if self.physicObject.onGround:
            #print("trying to jump")
            self.jump()
            self.moveX(dt)
        elif self.physicObject.vel.y < 0:
            #print("currently jumping")
            self.moveX(dt)
        elif self.physicObject.vel.y >= 0:
            #print("changing to fall")
            self.jumpAnimation.reset()
            currentState = Player.states["fall"]
        self.jumpAnimation.update(dt)
        self.currentState = currentState

    def fallUpdate(self,dt):
        currentState = self.currentState
        self.direction = self.getInput()
        if not self.physicObject.onGround:
            self.moveX(dt)
        else:
            self.moveX(dt)
            if self.direction.x != 0:
                self.fallAnimation.reset()
                currentState = Player.states["move"]
            else:
                self.fallAnimation.reset()
                currentState = Player.states["idle"]
        self.fallAnimation.update(dt)
        self.currentState = currentState

    def jump(self):
        jumpSpeed = sqrt(2 * self.physicObject.GRAVITY * self.jumpHeight)
        self.physicObject.vel.y = -jumpSpeed
