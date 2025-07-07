import pygame,sys
from physicObject import PhysicObject
from collisionObject import CollisionObject

pygame.init()

WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode([WIDTH,HEIGHT])
clock = pygame.time.Clock()
fps = 60

dt = 0

testObject = PhysicObject((WIDTH/2, 32,), (64, 64))

platforms = [CollisionObject([WIDTH/2, Height-16], [WIDTH, 32])]

def update(dt):
    testObject.update(dt)

def draw(screen):
    screen.fill("black")
    testObject.draw(screen)


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
