import pygame
import math
from config import RADIUS, CELL_SIZE, GRID_COLS, GRID_ROWS
import random

class Agents:
    def __init__(self, room, static_field,occupied, velocity = 3, mass = 100):
        self.velocity = velocity
        self.room = room
        self.mass = mass
        self.static_field = static_field
        self.reached_exit = False

        GRID_ROWS, GRID_COLS = static_field.shape
        while True:
            row = random.randint(1, GRID_ROWS - 2)
            col = random.randint(0, GRID_COLS - 1)
            if (row, col) not in occupied:
                self.cell = (row, col)
                occupied.add((row, col))
                break

    # Private method
    def _get_cell(self):
        col = int((self.position.x - self.room["x"]) / CELL_SIZE)
        row = int((self.position.y - self.room["y"]) / CELL_SIZE)
        GRID_ROWS, GRID_COLS = self.static_field.shape
        col = max(0, min(col, GRID_COLS - 1))
        row = max(0, min(row, GRID_ROWS - 1))
        return row, col

    def draw(self, screen):
        row, col = self.cell
        px = self.room["x"] + col * CELL_SIZE + CELL_SIZE // 2
        py = self.room["y"] + row * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, "thistle", (px, py), RADIUS)
    def update(self, occupied):
        if self.reached_exit:
            return

        row, col = self.cell
        GRID_ROWS, GRID_COLS = self.static_field.shape

        if self.static_field[row, col] == 0:
            self.reached_exit = True
            occupied.discard((row, col))
            return

        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                val = self.static_field[nr, nc]
                if val < self.static_field[row, col] and (nr, nc) not in occupied:
                    neighbors.append(((nr, nc), math.exp(-val)))

        if neighbors:
            total = sum(w for _, w in neighbors)
            roll = random.uniform(0, total)
            cumulative = 0
            best_cell = neighbors[-1][0]
            for cell, w in neighbors:
                cumulative += w
                if roll <= cumulative:
                    best_cell = cell
                    break

            occupied.discard((row, col))
            occupied.add(best_cell)
            self.cell = best_cell