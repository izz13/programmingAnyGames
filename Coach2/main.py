import pygame,sys
from player import Player
from collisionObject import CollisionObject

pygame.init()
WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode([WIDTH,HEIGHT],vsync=1)
clock = pygame.time.Clock()
fps = 60

dt = 0

testObject = Player([WIDTH/2,32],[64,64])

platforms = [CollisionObject([WIDTH/2,HEIGHT -16],[WIDTH,32])]

def update(dt):
    testObject.update(dt,platforms)
    for platform in platforms:
        platform.update()

def draw(screen):
    screen.fill("black")
    testObject.draw(screen)
    for platform in platforms:
        platform.draw(screen)


isRunning = True
while isRunning:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False
    update(dt)
    draw(screen)
    dt = clock.tick(fps)/1000
    pygame.display.flip()

pygame.quit()
sys.exit(1)