import pygame, random
import numpy as np
from environment import DefaulRoom
from agents import Agents
from static_field import static_field
from config import GRID_COLS, GRID_ROWS
from heatmap import agents_exit_plot

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
room = DefaulRoom(screen, center)
field = static_field(GRID_COLS, GRID_ROWS, room["exit_cells"], room["wall_cells"])

random.seed(42)
occupied = set()
agents = [Agents(room, field, occupied) for _ in range(200)]

font = pygame.font.SysFont(None, 36)
history = []
step = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    DefaulRoom(screen, center)

    agents = [a for a in agents if not a.reached_exit]
    history.append((step, 0 + len(agents)))
    step += 1

    for agent in agents:
        agent.update(occupied)
        agent.draw(screen)

    text = font.render(f"Remaining: {len(agents)}", True, "white")
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
if history:
    agents_exit_plot(history)