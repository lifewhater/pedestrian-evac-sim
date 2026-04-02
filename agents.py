import pygame
from config import RADIUS
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
        self.position = pygame.Vector2(random.randint(int(self.room["x"]) + RADIUS, int(self.room["x"] + self.room["width"]) - RADIUS),
                                        random.randint(int(self.room["y"]) + RADIUS, int(self.room["y"] + self.room["height"]) - RADIUS))

    def draw(self, screen):
        # arrow = [
        #     (self.position.x + x * SCALE, self.position.y + y * SCALE)
        #     for x, y in self.SHAPE
        # ]
        pygame.draw.circle(screen, "thistle", self.position, RADIUS)
    
    def update(self):
        self.position += self.vector * self.velocity
        exitCenter = pygame.Vector2(self.room["exitX"] + self.room["exitWidth"] / 2, self.room["y"])
        # self.vector = (self.position).normalize()
        top = self.room["y"] + RADIUS
        bottom = self.room["y"] + self.room["height"] - RADIUS
        left = self.room["x"] + RADIUS
        right = self.room["x"] + self.room["width"] - RADIUS

        if self.position.x < left:
            self.vector.x *= -1
        if self.position.x > right:
            self.vector.x *= -1
        if self.position.y < top:
            self.vector.y *= -1
        if self.position.y > bottom:
            self.vector.y *= -1 