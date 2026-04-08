import pygame
from config import RADIUS, CELL_SIZE, GRID_COLS, GRID_ROWS
import random

class Agents:
    def __init__(self, room, static_field, velocity = 2, mass = 80):
        self.velocity = velocity
        self.room = room
        self.mass = mass
        self.static_field = static_field
        self.reached_exit = False
        self.position = pygame.Vector2(
            random.randint(int(self.room["x"]) + RADIUS, int(self.room["x"] + self.room["width"]) - RADIUS),
            random.randint(int(self.room["y"]) + RADIUS, int(self.room["y"] + self.room["height"]) - RADIUS))

    # Private method
    def _get_cell(self):
        col = int((self.position.x - self.room["x"]) / CELL_SIZE)
        row = int((self.position.y - self.room["y"]) / CELL_SIZE)
        GRID_ROWS, GRID_COLS = self.static_field.shape
        col = max(0, min(col, GRID_COLS - 1))
        row = max(0, min(row, GRID_ROWS - 1))
        return row, col

    def draw(self, screen):
        pygame.draw.circle(screen, "thistle", self.position, RADIUS)
    
    def update(self, occupied):
        if self.reached_exit:
            return
        
        row, col = self._get_cell()
        GRID_ROWS, GRID_COLS = self.static_field.shape

        if self.static_field[row, col] == 0:
            self.reached_exit = True
            return
        
        # Gradient descent
        best_val = self.static_field[row, col]
        best_cell = None
        for dr, dc in [(-1,0), (1,0), (0,1), (0,-1)]:
            nc = dc + col
            nr = dr + row
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                if self.static_field[nr, nc] < best_val and (nr, nc) not in occupied:
                    best_val = self.static_field[nr, nc]
                    best_cell = (nr, nc)

        if best_cell is not None:
            target = pygame.Vector2(
                self.room["x"] + best_cell[1] * CELL_SIZE + CELL_SIZE / 2,
                self.room["y"] + best_cell[0] * CELL_SIZE + CELL_SIZE / 2,
            )
            direction = target - self.position
            if direction.length() > 0:
                direction = direction.normalize()
            self.position += direction * self.velocity