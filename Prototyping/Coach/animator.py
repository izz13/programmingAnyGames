import pygame
from pygame.math import Vector2


class Animator:
    frameTime = 1/15
    def __init__(self,folderPath,numOfFrames,size,name,loop = True):
        self.name = name
        self.frames = []
        self.size = size
        for i in range(numOfFrames):
            path = folderPath + "/" + name + "__00" + str(i) + ".png"
            image = pygame.image.load(path)
            image = pygame.transform.scale(image,self.size)
            self.frames.append(image)
        self.loop = loop
        self.frameNumber = 0
        self.frameDelta = 0
        self.totalFrames = numOfFrames
        self.animationSpeed = 1

    def draw(self,screen,rect,flipped):
        image = self.frames[self.frameNumber]
        if flipped:
            image = pygame.transform.flip(image,True,False)
        screen.blit(image,rect)

    def update(self,dt):
        if self.frameDelta > Animator.frameTime / self.animationSpeed:
            self.frameNumber += 1
            if self.frameNumber < self.totalFrames:
                self.frameDelta = 0
            else:
                if self.loop:
                    self.frameNumber = 0
                    self.frameDelta = 0
                else:
                    self.frameNumber = self.totalFrames - 1
                    self.frameDelta = 0
        else:
            self.frameDelta += dt
    
    def reset(self):
        self.frameNumber = 0
        self.frameDelta = 0
        




if __name__ == "__main__":
    pygame.init()

    WIDTH,HEIGHT = 800,600
    screen = pygame.display.set_mode([WIDTH,HEIGHT])
    clock = pygame.time.Clock()
    fps = 60
    pygame.display.set_caption("TEST ANIMATION")

    idle = Animator("Prototyping/Coach/playerIdleFrames",10,[48,64],"Idle")
    idleRect = pygame.Rect(15,15,48,64)

    run = Animator("Prototyping/Coach/playerRunFrames",10,[48,64],"Run")
    run.animationSpeed = 2
    runRect = pygame.Rect(15,100,48,64)

    jump = Animator("Prototyping/Coach/playerJumpFrames",7,[48,64],"Jump")
    jumpRect = pygame.Rect(15,175,48,64)

    fall = Animator("Prototyping/Coach/playerFallFrames",3,[48,64],"Fall")
    fallRect = pygame.Rect(15,250,48,64)

    dt = 0

    isRunning = True
    while isRunning:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                isRunning = False
        
        screen.fill("black")
        idle.update(dt)
        idle.draw(screen,idleRect,False)
        run.update(dt)
        run.draw(screen,runRect,False)
        jump.update(dt)
        jump.draw(screen,jumpRect,False)
        fall.update(dt)
        fall.draw(screen,fallRect,False)
        dt = clock.tick(fps)/1000
        pygame.display.update()

    


