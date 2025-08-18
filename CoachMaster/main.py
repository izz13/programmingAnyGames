import pygame,sys
from player import Player
from collisionObject import CollisionObject
import animator

pygame.init()
WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode([WIDTH,HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0
max_dt = .2
windowMoving = False

testObject = Player([WIDTH/2,32],[42,64])

platforms = []
for i in range(3):
    p = CollisionObject([WIDTH/2 - WIDTH*i/4,HEIGHT -16 - i*32],[WIDTH - WIDTH*i/4,32])
    platforms.append(p)
for i in range(3):
    p = CollisionObject([WIDTH/2 + WIDTH*i/4,HEIGHT -200 - i*32],[WIDTH - WIDTH*i/4 - 150,32])
    platforms.append(p)
# for i in range(32):
#     width = WIDTH/16
#     p = CollisionObject([width/2 + i*width/2, HEIGHT - 32],[width,64])
#     platforms.append(p)

# for i in range(32):
#     width = WIDTH/32
#     p = CollisionObject([width/2 + i*width/2, HEIGHT - 200],[width,64])
#     platforms.append(p)

# for i in range(32):
#     height = HEIGHT/16
#     p = CollisionObject([WIDTH -32,height/2 + i*height/2],[64,height])
#     platforms.append(p)


def update(dt):
    testObject.update(dt,platforms,events)
    for platform in platforms:
        platform.update()

def draw(screen):
    screen.fill("white")
    testObject.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    rect = pygame.Rect(0,0,25,200)
    rect.bottomright = platforms[0].rect.topright
    rect.y -= 248
    pygame.draw.rect(screen,"cyan",rect)


isRunning = True
while isRunning:
    pygame.display.set_caption(str(windowMoving))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.WINDOWMOVED:
            windowMoving = True
        else:
            windowMoving = False
            
    if pygame.display.get_active() and not windowMoving:
        update(dt)
        draw(screen)
    dt = min(clock.tick(fps)/1000,max_dt)
    pygame.display.flip()

pygame.quit()
sys.exit(1)