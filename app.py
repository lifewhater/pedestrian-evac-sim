import pygame
from environment import DefaulRoom
from agents import Agents

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
agent = Agents(pygame.Vector2(center), pygame.Vector2(1, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0 ,0))
    
    DefaulRoom(screen, center) 
    # agent.update()
    agent.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()