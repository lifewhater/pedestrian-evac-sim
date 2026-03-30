import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
SCALE = 5

mathPoints = [
    (-3, 0),
    (-2, 2),
    (2, 0),
    (-2, -2),
]

arrow = [
    (center.x + x * SCALE, center.y + y * SCALE)
    for x, y in mathPoints
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0 ,0))

    pygame.draw.polygon(screen, "thistle", arrow)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()