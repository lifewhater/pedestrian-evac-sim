import pygame

def DefaulRoom(screen, center):
    room = pygame.draw.rect(screen, "white", (center.x - 100, center.y - 100, 200, 200), width=1)