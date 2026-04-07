import pygame
from config import HEIGHT, WIDTH, CELL_SIZE, GRID_COLS, GRID_ROWS

def DefaulRoom(screen, center):
    exitWidth = 40

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

    for row in range(GRID_ROWS + 1):
        pygame.draw.line(screen, "gray", (x, y + row * CELL_SIZE), (x + WIDTH, y + row * CELL_SIZE), 1)
    for col in range(GRID_COLS + 1):
        pygame.draw.line(screen, "gray", (x + col * CELL_SIZE, y), (x + col * CELL_SIZE, y + HEIGHT), 1)

    # Exit cells are at row=0, columns that fall within the exit opening
    col_start = int((exitX - x) / CELL_SIZE)
    col_end = int((exitX + exitWidth - x) / CELL_SIZE)
    exit_cells = set((0, col) for col in range(col_start, col_end + 1))
    wall_cells = set()  # no internal walls yet

    return {
        "x": x, "y": y,
        "width": WIDTH, "height": HEIGHT,
        "exitX": exitX, "exitWidth": exitWidth,
        "exit_cells": exit_cells,
        "wall_cells": wall_cells,
    }
