import pygame,sys
from player import Player
from collisionObject import CollisionObject

pygame.init()
WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode([WIDTH,HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = 0.2

testObject = Player([WIDTH/2,32],[42,64])

platforms = []
for i in range(3):
    p = CollisionObject([WIDTH/2 - WIDTH*i/4,HEIGHT -16 - i*32],[WIDTH - WIDTH*i/4,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + WIDTH*i/4,HEIGHT -200 - i*32],[WIDTH - WIDTH*i/4 - 150,32])
    platforms.append(p)


def update(dt):
    testObject.update(dt,platforms)
    for platform in platforms:
        platform.update()

def draw(screen):
    screen.fill("white")
    testObject.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    rect = pygame.Rect(0,0,25,200)
    rect.bottomright = platforms[0].rect.topright
    pygame.draw.rect(screen,"cyan",rect)


isRunning = True
while isRunning:
    pygame.display.set_caption(str(clock.get_fps()))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    update(dt)
    draw(screen)
    dt = min(clock.tick(fps)/1000, max_dt)
    pygame.display.flip()

pygame.quit()
sys.exit(1)