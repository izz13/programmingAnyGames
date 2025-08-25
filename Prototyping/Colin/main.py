import pygame,sys
from player import Player
from collisionObject import CollisionObject
from camera import Camera


pygame.init()
WIDTH, HEIGHT = 5000, 1200
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640


screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = 0.2

world = pygame.Surface([WIDTH, HEIGHT])
cam = Camera([SCREEN_WIDTH, SCREEN_HEIGHT])

testObject = Player([WIDTH/2,32],[42,64])

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


def update(dt, world):
    cam.update(world, dt, testObject.physicObject)
    testObject.update(dt,platforms)
    for platform in platforms:
        platform.update()

def draw(world):
    world.fill("black")
    testObject.draw(world)
    for platform in platforms:
        platform.draw(world)

        

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