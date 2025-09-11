import pygame,sys
from player import Player
from collisionObject import CollisionObject
from camera import Camera
from random import randint
import math


pygame.init()
WIDTH,HEIGHT = 2000,1200
SCREEN_WIDTH,SCREEN_HEIGHT = 800,640


screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = .2

world = pygame.Surface([WIDTH,HEIGHT])
cam = Camera([SCREEN_WIDTH,SCREEN_HEIGHT])

testObject = Player([WIDTH/2,32],[42,64])



platforms = []
for i in range(3):
    p = CollisionObject([WIDTH/2 - WIDTH*i/4,HEIGHT -16 - i*32],[WIDTH - WIDTH*i/4,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + WIDTH*i/4,HEIGHT -200 - i*32],[WIDTH - WIDTH*i/4 - 150,32])
    platforms.append(p)
leftWall = CollisionObject([-250,HEIGHT/2],[500,HEIGHT])
rightWall = CollisionObject([WIDTH + 250, HEIGHT/2],[500,HEIGHT])
slideTestWall = CollisionObject([200,HEIGHT/2],[64,HEIGHT*4/5 - 264])
platforms.append(leftWall)
platforms.append(rightWall)
platforms.append(slideTestWall)

# for i in range(32):
#     width = WIDTH/16
#     p = CollisionObject([width/2 + i*width/2, HEIGHT - 32],[width,64])
#     platforms.append(p)

# for i in range(20):
#     width = WIDTH/16
#     p = CollisionObject([width/2 + i*width/2, HEIGHT - 200],[width,64])
#     platforms.append(p)

# for i in range(32):
#     height = HEIGHT/16
#     p = CollisionObject([32,height/2 + i*height/2],[64,height])
#     platforms.append(p)


#platforms.append(CollisionObject([WIDTH - 1000,600],[1000,HEIGHT]))


def update(dt,world):
    cam.update(world,dt,testObject.physicObject)
    testObject.update(dt,platforms)
    for platform in platforms:
        platform.update()
    if not world.get_rect().collidepoint(testObject.physicObject.rect.center):
        print(testObject.physicObject.rect.center)
        print(testObject.physicObject.vel)
        pygame.quit()
t = 0
startColor = pygame.math.Vector3(randint(0,255),randint(0,255),randint(0,255))
endColor = pygame.math.Vector3(255 - startColor.x,255 - startColor.y,255 - startColor.z)
ballStartColor = pygame.math.Vector3(randint(0,255),randint(0,255),randint(0,255))
ballEndColor = pygame.math.Vector3(255 - ballStartColor.x,255 - ballStartColor.y,255 - ballStartColor.z)
def draw(world : pygame.Surface):
    global t,startColor,endColor
    t+=dt
    world.fill("black")
    iteration = abs(math.sin((2*math.pi *t)/(2)))
    color = startColor.lerp(endColor,pygame.math.clamp(iteration,0,1))  
    numDrawnPoints = 0
    for i in range(0,WIDTH,100):
        for j in range(0,HEIGHT,100):
            if cam.rect.collidepoint(i,j):
                pygame.draw.circle(world,color,[i ,j],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
                #pygame.draw.circle(world,"white",[i ,j],3)
                numDrawnPoints += 1
    testObject.draw(world)
    for platform in platforms:
        platform.draw(world)
    playerPos = testObject.physicObject.rect.center
    #pygame.draw.circle(world,color,[75* math.sin((2*math.pi *t)/(10)) + playerPos[0] ,75 * math.cos((2*math.pi *t)/(1)) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    #pygame.draw.circle(world,ballColor,[-75* math.sin((2*math.pi *t)/(1)) + playerPos[0] ,55 * math.cos((2*math.pi *t)/(10)) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    


isRunning = True

while isRunning:
    pygame.display.set_caption(str(testObject.totalSlideDistance))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    update(dt,world)
    draw(world)
    pygame.display.set_icon(testObject.currentAnimation.frames[testObject.currentAnimation.frameNumber])
    screen.blit(cam.surface,[0,0])
    dt = min(clock.tick(fps)/1000  ,max_dt)
    pygame.display.flip()

pygame.quit()
sys.exit(1)