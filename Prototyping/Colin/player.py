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
        "sliding" : 5,
        "jumpAttack" : 6
    }
    def __init__(self,startPos,size):
        self.physicObject = PhysicObject(startPos,size)
        self.image = self.physicObject.surface
        self.direction = Vector2(0)
        self.maxSpeed = 300
        self.acc = 5000
        self.deAcc = 2000
        self.jumpSpeed = 500
        self.jumpMinHeight = 175
        self.jumpMaxHeight = 250
        self.jumpHeight = self.jumpMinHeight
        self.jumpAttackHeight = 30
        self.jumpAttackSpeed = 750
        self.currentState = Player.states["idle"]
        self.facingLeft = True
        self.tryAttack = False
        self.attackCombo = 0
        self.slidingSpeed = 750
        self.slideDirection = 0
        self.fullTotalSlideDistance = 300
        self.totalSlideDistance = self.fullTotalSlideDistance
        self.currentSlideDistance = 0
        self.setAnimationClips()
        self.currentAnimation = self.idleAnimation

    def setAnimationClips(self):
        self.idleAnimation = Animator("Prototyping/Colin/playerIdleFrames",10,[32,64],"Idle")
        self.runAnimation = Animator("Prototyping/Colin/playerRunFrames",10,[48,64],"Run")
        self.runAnimation.animationSpeed = 2
        self.jumpAnimation = Animator("Prototyping/Colin/playerJumpFrames",7,[48,64],"Jump",loop = False)
        self.fallAnimation = Animator("Prototyping/Colin/playerFallFrames",3,[48,64],"Fall",loop = False)
        self.attackAnimation = Animator("Prototyping/Colin/playerAttackFrames0",10,[64,72],"Attack",loop = False)
        self.attackAnimation.animationSpeed = 2
        self.jumpAttackAnimation = Animator("Prototyping/Colin/playerAttackFrames1",10,[64,72],"Jump_Attack",loop = False)
        self.jumpAttackAnimation.animationSpeed = 1
        self.slideAnimation = Animator("Prototyping/Colin/playerSlidingFrames",10,[48,48],"Slide",loop = False)

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
        elif self.currentState == Player.states["jumpAttack"]:
            self.jumpAttackUpdate(dt)
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
        if self.currentState == Player.states["jumpAttack"]:
            self.currentAnimation = self.jumpAttackAnimation
        rect = self.getDrawRect()
        # if self.physicObject.sliding:
        #     pygame.draw.rect(screen,"blue",self.physicObject.slideRect)
        # else:
        #     pygame.draw.rect(screen,"blue",self.physicObject.rect)
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
                #self.totalSlideDistance = self.checkSlideDistance()
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
            #self.totalSlideDistance = self.checkSlideDistance()
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
        elif self.physicObject.vel.y < 0 and not self.tryAttack:
            #print("currently jumping")
            self.moveX(dt)
        elif self.physicObject.vel.y < 0 and self.tryAttack:
            self.setJumpAttack(dt)
            currentState = Player.states["jumpAttack"]
            self.jumpAnimation.reset()
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
        elif self.tryAttack and not self.physicObject.onGround:
            self.setJumpAttack(dt)
            currentState = Player.states["jumpAttack"]
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
        if self.attackAnimation.frameNumber >= 3 and self.attackCombo < 1:
            self.getInput()
            if self.tryAttack:
                self.attackCombo += 1
        if self.attackAnimation.frameNumber >= self.attackAnimation.totalFrames - 1:
            if self.attackCombo >= 1:
                self.setJumpAttack(dt)
                self.attackAnimation.reset()
                currentState = Player.states["jumpAttack"]
            else:
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
            rect = self.physicObject.rect
            checkRect = pygame.Rect(rect.x,rect.y - 5,rect.w,rect.h)
            collidedObject = self.physicObject.checkIfInCollisionObject(checkRect)
            if collidedObject:
                if self.slideDirection == -1:
                    self.physicObject.rect.right = collidedObject.rect.left
                    self.physicObject.pos = Vector2(self.physicObject.rect.center)
                else:
                    self.physicObject.rect.left = collidedObject.rect.right
                    self.physicObject.pos = Vector2(self.physicObject.rect.center)
            self.physicObject.sliding = False
            #self.physicObject.vel.x = 0
            self.direction = self.getInput()
            self.slideAnimation.reset()
            if self.direction == Vector2(0):
                currentState = Player.states["idle"]
            elif self.direction.y == -1 and self.physicObject.onGround:
                currentState = Player.states["jump"]
            elif self.direction.x != 0 and self.direction.y == 0 or self.direction.y == 1:
                currentState = Player.states["move"]
            self.currentSlideDistance = 0
        self.slideAnimation.update(dt)
        self.currentState = currentState

    def jump(self,height):
        jumpSpeed = sqrt(2 * self.physicObject.GRAVITY * height)
        self.physicObject.vel.y = -jumpSpeed

    def checkSlideDistance(self):
        totalSlideDistance = self.fullTotalSlideDistance
        rect = self.physicObject.rect
        slideEndRect = pygame.Rect(rect.x + self.fullTotalSlideDistance*self.slideDirection,rect.y - 5,rect.w,rect.h)
        collidedObject = self.physicObject.checkIfInCollisionObject(slideEndRect)
        if collidedObject:
            if self.slideDirection == -1:
                totalSlideDistance = abs(collidedObject.rect.right - self.physicObject.rect.left)
            else:
                totalSlideDistance = abs(collidedObject.rect.left - self.physicObject.rect.right)
        return totalSlideDistance
    
    def jumpAttackUpdate(self,dt):
        currentState = self.currentState
        self.direction = Vector2(0)
        self.moveX(dt)
        if self.jumpAttackAnimation.frameNumber >= self.jumpAttackAnimation.totalFrames - 1:
            if self.attackCombo >= 1:
                self.attackCombo = 0
            if not self.physicObject.onGround:
                currentState = Player.states["fall"]
            else:
                currentState = Player.states["idle"]
        self.jumpAttackAnimation.update(dt)
        if self.currentState != currentState:
            self.jumpAttackAnimation.reset()
        self.currentState = currentState

    def setJumpAttack(self,dt):
        direction = 1
        if self.facingLeft:
            direction = -1
        self.physicObject.vel.x = direction*self.jumpAttackSpeed
        self.jump(self.jumpAttackHeight)


