import pygame,sys
from player import Player
from collisionObject import CollisionObject
from camera import Camera
from random import randint
from enemy import Enemy
import math


pygame.init()
WIDTH, HEIGHT = 2000, 1200
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = 0.2

world = pygame.Surface([WIDTH, HEIGHT])
cam = Camera([SCREEN_WIDTH, SCREEN_HEIGHT])

testObject = Player([WIDTH/2,32],[42,64])
enemies = []
for enemy in range(1):
    e = Enemy([WIDTH/2 - 48, 32], [42,64], "base")
    enemies.append(e)

platforms = []
for i in range(3):
    p = CollisionObject([WIDTH/2 - WIDTH*i/4,HEIGHT -16 - i*32],[WIDTH - WIDTH*i/4,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + WIDTH*i/4,HEIGHT -200 - i*32],[WIDTH - WIDTH*i/4 - 150,32])
    platforms.append(p)
p = CollisionObject([WIDTH,HEIGHT/2],[1, HEIGHT])
platforms.append(p)
p = CollisionObject([0, HEIGHT/2],[1, HEIGHT])
platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + i*200,HEIGHT/2 + 200 - i*150],[100,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + 100 - i*200,HEIGHT/2 -200 - i*150],[100,32])
    platforms.append(p)
slideTestWall = CollisionObject([200,HEIGHT/2],[100,HEIGHT*4/5 - 264])
platforms.append(p)
platforms.append(slideTestWall)

def update(dt, world):
    cam.update(world, dt, testObject.physicObject)
    testObject.update(dt,platforms)
    for enemy in enemies:
        enemy.update(dt, platforms)
    for platform in platforms:
        platform.update()

t = 0
#startColor = pygame.math.Vector3(randint(0,255),randint(0,255),randint(0,255))
#endColor = pygame.math.Vector3(255 - startColor.x,255 - startColor.y,255 - startColor.z)
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
    for enemy in enemies:
        enemy.draw(world)
    print(numDrawnPoints)
    for platform in platforms:
        platform.draw(world)
    playerPos = testObject.physicObject.rect.center
    pygame.draw.circle(world,color,[-75* math.sin((2*math.pi *t)/(1)) + playerPos[0] ,55 * math.cos((2*math.pi *t)/(10)) + playerPos[1]],3 + 7 * abs(math.sin((2*math.pi *t)/(2))))
        

isRunning = True
while isRunning:
    pygame.display.set_caption(str(clock.get_fps()))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    update(dt, world)
    draw(world)
    screen.blit(cam.surface, [0, 0])
    dt = min(clock.tick(fps)/1000, max_dt)
    pygame.display.flip()

pygame.quit()
sys.exit(1)