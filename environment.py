import pygame
import numpy as np
from config import HEIGHT, WIDTH

def DefaulRoom(screen, center):
    exitWidth = 80
    # Grid implementation for 
    CELL_SIZE = 20
    cols = WIDTH // CELL_SIZE
    rows = HEIGHT // CELL_SIZE
    grid = np.zeros((rows, cols), dtype=int)

    # top left corner of the room
    x = center.x - WIDTH // 2
    y = center.y - HEIGHT // 2

    # start of the exit 
    exitX = center.x - exitWidth // 2

    # 3 regular walls
    pygame.draw.line(screen, "white", (x, y), (x, y + HEIGHT), 1) 
    pygame.draw.line(screen, "white", (x + WIDTH, y), (x + WIDTH, y + HEIGHT), 1) 
    pygame.draw.line(screen, "white", (x, y + HEIGHT), (x + WIDTH, y + HEIGHT), 1) 

    # wall with exit
    pygame.draw.line(screen, "white", (x, y), (exitX, y), 1)
    pygame.draw.line(screen, "white", (exitX + exitWidth, y), (x + WIDTH, y), 1)

    #EXIT
    pygame.draw.line(screen, "red", (exitX, y), (exitX + exitWidth, y), 1)

    for row in range(rows + 1):
        pygame.draw.line(screen, "gray", (x, y + row * CELL_SIZE), (x + WIDTH, y + row * CELL_SIZE), 1)

    return {
        "height": HEIGHT,
        "width": WIDTH,
        "x": x, "y": y,
        "exitX": exitX, "exitWidth": exitWidth
    }