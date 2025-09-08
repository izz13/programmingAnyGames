import pygame,sys
from player import Player
from collisionObject import CollisionObject
from camera import Camera
import math


pygame.init()
WIDTH,HEIGHT = 2000, 2000
SWIDTH, SHEIGHT = 800, 640


screen = pygame.display.set_mode([SWIDTH,SHEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = .2

world = pygame.Surface([WIDTH, HEIGHT])
cam = Camera([SWIDTH, SHEIGHT])

testObject = Player([WIDTH/2,32],[42,64])

platforms = []
for i in range(3):
    p = CollisionObject([WIDTH/2 - WIDTH*i/4,HEIGHT -16 - i*32],[WIDTH - WIDTH*i/4,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + WIDTH*i/4,HEIGHT -200 - i*32],[WIDTH - WIDTH*i/4 - 150,32])
    platforms.append(p)

p = CollisionObject([WIDTH + 16, HEIGHT], [ 32, HEIGHT + 600])
platforms.append(p)

p = CollisionObject([-16, HEIGHT], [ 32, HEIGHT + 600])
platforms.append(p)

p = CollisionObject([1200, 1550], [100, 20])
platforms.append(p)

p = CollisionObject([1370, 1400], [100, 20])
platforms.append(p)

p = CollisionObject([1100, 1200], [100, 20])
platforms.append(p)

p = CollisionObject([700, 1400], [500, 20])
platforms.append(p)

p = CollisionObject([300, 1300], [20, 20])
platforms.append(p)

p = CollisionObject([400, 1050], [20, 20])
platforms.append(p)

p = CollisionObject([750, 900], [300, 20])
platforms.append(p)

p = CollisionObject([600, 1240], [100,1000])
platforms.append(p)





def update(dt, world):
    cam.update(world, dt, testObject.physicObject)
    testObject.update(dt,platforms)
    for platform in platforms:
        platform.update()

t = 0
def draw(world):
    global t
    t+=dt
    world.fill("black")
    startColor = pygame.math.Vector3(250,50,50)
    endColor = pygame.math.Vector3(50,50,250)
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
    #print(numDrawnPoints)
    for platform in platforms:
        platform.draw(world)
    playerPos = testObject.physicObject.rect.center
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,55 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,15 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))

    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,45 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(1)) + playerPos[0] ,25 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,90 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[75* math.sin((2*math.pi *t)/(3)) + playerPos[0] ,30 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,85 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(1)) + playerPos[0] ,25 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[75* math.sin((2*math.pi *t)/(2)) + playerPos[0] ,10 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
    pygame.draw.circle(world,color,[75* math.sin((2*math.pi *t)/(3)) + playerPos[0] ,70 * math.cos((2*math.pi *t)*3) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
isRunning = True
while isRunning:
    pygame.display.set_caption(str(testObject.physicObject.rect.center))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    update(dt, world)
    draw(world)
    screen.blit(cam.surface,[0,0])
    dt = min(clock.tick(fps)/1000,max_dt)
    pygame.display.flip()

pygame.quit()
sys.exit(1)