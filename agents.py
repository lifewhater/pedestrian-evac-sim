import pygame
from config import SCALE
import random

class Agents:
    SHAPE = [
        (-3, 0),
        (-2, 2),
        (2, 0),
        (-2, -2),
    ]

    def __init__(self, position, room, velocity = 0.25, mass = 80):
        self.velocity = velocity
        self.room = room
        self.mass = mass
        self.vector = pygame.Vector2(random.randint(-10, 10), random.randint(-10,10))
        self.position = position

    def draw(self, screen):
        # arrow = [
        #     (self.position.x + x * SCALE, self.position.y + y * SCALE)
        #     for x, y in self.SHAPE
        # ]
        pygame.draw.circle(screen, "thistle", self.position, 5)
    
    def update(self):
        # exitCenter = pygame.Vector2(self.room["exitX"] + self.room["exitWidth"] / 2, self.room["y"])
        # self.vector = (self.position).normalize()
        self.position += self.vector * self.velocity
        # if self.position.y > pygame.Vector2(self.room["height"]):
        #     self.velocity *= -1
        # if self.position > pygame.Vector2(self.room["width"]):
        #     self.velocity.x *= -1