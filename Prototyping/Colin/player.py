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
        "fall" : 3,
        "attack" : 4,
        "sliding" : 5
    }
    def __init__(self,startPos,size):
        self.physicObject = PhysicObject(startPos,size)
        self.image = self.physicObject.surface
        self.direction = Vector2(0)
        self.maxSpeed = 300
        self.acc = 5000
        self.deAcc = 900
        self.jumpSpeed = 500
        self.jumpMinHeight = 175
        self.jumpMaxHeight = 250
        self.jumpHeight = self.jumpMinHeight
        self.currentState = Player.states["idle"]
        self.facingLeft = True
        self.tryAttack = False
        self.slidingSpeed = 750
        self.slideDirection = 0
        self.totalSlideDistance = 200
        self.currentSlideDistance = 0
        self.setAnimationClips()
        self.currentAnimation = self.idleAnimation

    def setAnimationClips(self):
        self.idleAnimation = Animator("Prototyping/Coach/playerIdleFrames",10,[32,64],"Idle")
        self.runAnimation = Animator("Prototyping/Coach/playerRunFrames",10,[48,64],"Run")
        self.runAnimation.animationSpeed = 2
        self.jumpAnimation = Animator("Prototyping/Coach/playerJumpFrames",7,[48,64],"Jump",loop = False)
        self.fallAnimation = Animator("Prototyping/Coach/playerFallFrames",3,[48,64],"Fall",loop = False)
        self.attackAnimation = Animator("Prototyping/Coach/playerAttackFrames",10,[64,72],"Attack",loop = False)
        self.attackAnimation.animationSpeed = 2
        self.slideAnimation = Animator("Prototyping/Coach/playerSlidingFrames",10,[48,48],"Slide",loop = False)

    def update(self,dt,collisionObjects):
        # self.direction = self.getInput()
        # self.moveX(dt)
        #print(self.currentState)
        if self.currentState == Player.states["idle"]:
            self.idleUpdate(dt)
        elif self.currentState == Player.states["move"]:
            self.moveUpdate(dt)
        elif self.currentState == Player.states["jump"]:
            self.jumpUpdate(dt)
        elif self.currentState == Player.states["fall"]:
            self.fallUpdate(dt)
        elif self.currentState == Player.states["attack"]:
            self.attackUpdate(dt)
        elif self.currentState == Player.states["sliding"]:
            self.slidingUpdate(dt)
        self.physicObject.update(dt,collisionObjects)

    def draw(self,screen):
        if self.currentState == Player.states["idle"]:
            self.currentAnimation = self.idleAnimation
        if self.currentState == Player.states["move"]:
            self.currentAnimation = self.runAnimation
        if self.currentState == Player.states["jump"]:
            self.currentAnimation = self.jumpAnimation
        if self.currentState == Player.states["fall"]:
            self.currentAnimation = self.fallAnimation
        if self.currentState == Player.states["attack"]:
            self.currentAnimation = self.attackAnimation
        if self.currentState == Player.states["sliding"]:
            self.currentAnimation = self.slideAnimation
        rect = self.getDrawRect()
        if self.physicObject.sliding:
            pygame.draw.rect(screen,"blue",self.physicObject.slideRect)
        else:
            pygame.draw.rect(screen,"blue",self.physicObject.rect)
        # pygame.draw.rect(screen,"red",rect)
        self.currentAnimation.draw(screen,rect,self.facingLeft)
        #screen.blit(self.image,self.physicObject.rect)

    def getDrawRect(self):
        currentImage = self.currentAnimation.frames[self.currentAnimation.frameNumber]
        if self.facingLeft:
            flippedCurrentImage = pygame.transform.flip(currentImage,True,False)
            drawRect = flippedCurrentImage.get_rect()
            if self.currentState == Player.states["sliding"]:
                drawRect.bottomright = self.physicObject.rect.bottomright
            else:
                drawRect.topright = self.physicObject.rect.topright
        else:
            drawRect = currentImage.get_rect()
            if self.currentState == Player.states["sliding"]:
                drawRect.bottomleft = self.physicObject.rect.bottomleft
            else:
                drawRect.topleft = self.physicObject.rect.topleft
        return drawRect

    def getInput(self):
        inputVector = Vector2(0,0)
        self.tryAttack = False
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
        if keysClicked[pygame.K_s]:
            inputVector.y = 1
        if keysClicked[pygame.K_SPACE]:
            self.tryAttack = True
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
            self.idleAnimation.reset()
            if inputVector.y == -1 and self.physicObject.onGround:
                currentState = Player.states["jump"]
            elif inputVector.y == 1 and self.physicObject.onGround:
                currentState = Player.states["sliding"]
            else:
                currentState = Player.states["move"]
            self.direction = self.getInput()
        elif self.tryAttack:
            self.idleAnimation.reset()
            currentState = Player.states["attack"]
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
        elif self.tryAttack:
            self.runAnimation.reset()
            currentState = Player.states["attack"]
        elif self.direction.y == -1 and self.physicObject.onGround:
            self.runAnimation.reset()
            currentState = Player.states["jump"]
        elif self.direction.y == 1 and self.physicObject.onGround:
            self.runAnimation.reset()
            currentState = Player.states["sliding"]
        if self.physicObject.vel.y > PhysicObject.TOLERANCE:
            #print("changing to fall")
            self.runAnimation.reset()
            currentState = Player.states["fall"]
        self.runAnimation.update(dt)
        self.currentState = currentState

    def jumpUpdate(self,dt):
        currentState = self.currentState
        self.direction = self.getInput()
        if self.physicObject.onGround:
            #print("trying to jump")
            self.jump(self.jumpMinHeight)
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

    def attackUpdate(self,dt):
        currentState= self.currentState
        self.direction = Vector2(0)
        self.moveX(dt)
        if self.attackAnimation.frameNumber >= self.attackAnimation.totalFrames - 1:
            self.attackAnimation.reset()
            currentState = Player.states["idle"]
        self.attackAnimation.update(dt)
        self.currentState = currentState

    def slidingUpdate(self,dt):
        currentState = self.currentState
        if self.facingLeft:
            self.slideDirection = -1
        else:
            self.slideDirection = 1
        vel_x = self.slideDirection*self.slidingSpeed
        if self.currentSlideDistance + abs(vel_x*dt) < self.totalSlideDistance:
            self.physicObject.sliding = True
            self.currentSlideDistance += abs(vel_x*dt)
            self.physicObject.vel.x = vel_x
        else:
            self.physicObject.sliding = False
            self.physicObject.vel.x = 0
            self.direction = Vector2(0)
            self.slideAnimation.reset()
            currentState = Player.states["idle"]
            self.currentSlideDistance = 0
        self.slideAnimation.update(dt)
        self.currentState = currentState

    def jump(self,height):
        jumpSpeed = sqrt(2 * self.physicObject.GRAVITY * height)
        self.physicObject.vel.y = -jumpSpeed
