"""
High level purpose, it represents a single agent in the simulation. It uses stochastic decision making 
process based on a "Potential Field". It tells the agent which direction leads to exit but also considers obstacles and walls 
and social pressure from the other agents.
"""

import pygame
import math
import random
from config import RADIUS, CELL_SIZE, KD


class Agents:
    def __init__(self, room, static_field, position, velocity = 1, mass = 100):
        self.velocity = velocity
        self.room = room
        self.mass = mass
        self.static_field = static_field
        self.reached_exit = False
        self.position = pygame.Vector2(position)

    # Private method for getting the row and col 
    def _get_cell(self):
        col = int((self.position.x - self.room["x"]) / CELL_SIZE)
        row = int((self.position.y - self.room["y"]) / CELL_SIZE)
        GRID_ROWS, GRID_COLS = self.static_field.shape
        col = max(0, min(col, GRID_COLS - 1))
        row = max(0, min(row, GRID_ROWS - 1))
        return row, col

    # Draws the agent
    def draw(self, screen):
        pygame.draw.circle(screen, "thistle", self.position, RADIUS)
    
    #
    def get_intention(self, occupied, wall_cells):
        if self.reached_exit:
            return
        
        row, col = self._get_cell()
        GRID_ROWS, GRID_COLS = self.static_field.shape

        if self.static_field[row, col] == 0:
            self.reached_exit = True
            return None
        
        # Stochastic transition: only consider unoccupied neighbors closer to exit
        neighbors = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                val = self.static_field[nr, nc]
                if val < self.static_field[row, col] and (nr, nc) not in occupied:
                    
                    # Using Kirchner's method for determining conflicts and who occupies what cell
                    #  s_ij static field
                    # n_ij is 0 if occupied and 1 if not
                    # d_ij is 1 if not wall and 0 if wall
                    static_ij = self.static_field[nr, nc] - self.static_field[row, col]


                    dynamic_ij = 0
                    occupied_ij = 1 if (nr, nc) in occupied else 0
                    wall_ij = 0 if (nr, nc) in wall_cells else 1

                    # NEED TO INCORPORATE DYNAMIC FIELD FOR CORRECT IMPLEMENTATION
                    p_ij = math.exp(KD * static_ij) * (1 - occupied_ij) * wall_ij
                    if p_ij > 0:
                        neighbors.append(((nr, nc), p_ij))

        if not neighbors:
            return None
        total = sum(w for _, w in neighbors)
        roll = random.uniform(0, total)
        cumulative = 0
        best_cell = neighbors[-1][0]  # fallback
        for cell, w in neighbors:
            cumulative += w
            if roll <= cumulative:
                best_cell = cell
                break
        return best_cell
    
    def move_to(self, cell):
        target = pygame.Vector2(
            self.room["x"] + cell[1] * CELL_SIZE + CELL_SIZE / 2,
            self.room["y"] + cell[0] * CELL_SIZE + CELL_SIZE / 2,)
        direction = target - self.position
        if direction.length() > 0:
            direction = direction.normalize()
        self.position += direction * self.velocity