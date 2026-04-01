import pygame
from config import SCALE
class Agents:
    SHAPE = [
        (-3, 0),
        (-2, 2),
        (2, 0),
        (-2, -2),
    ]

    def __init__(self, position, vector, velocity = 0, mass = 80):
        self.velocity = velocity
        self.mass = mass
        self.vector = vector
        self.position = position

    def draw(self, screen):
        arrow = [
            (self.position.x + x * SCALE, self.position.y + y * SCALE)
            for x, y in self.SHAPE
        ]
        pygame.draw.polygon(screen, "thistle", arrow)
    
    def update(self):
        self.position += self.vector * self.velocity