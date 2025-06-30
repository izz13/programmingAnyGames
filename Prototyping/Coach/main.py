import pygame,sys

pygame.init()

WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode([WIDTH,HEIGHT])
clock = pygame.time.Clock()
fps = 60

dt = 0

def update(dt):
    pass

def draw(screen):
    screen.fill("black")


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