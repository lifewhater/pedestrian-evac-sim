import pygame
from environment import DefaulRoom
# from gradient_descent_method import Agents
from agents import Agents
from static_field import static_field
from config import GRID_COLS, GRID_ROWS

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
room = DefaulRoom(screen, center)
field = static_field(GRID_COLS, GRID_ROWS, room["exit_cells"], room["wall_cells"])
agents = [Agents(room, field) for _ in range(100)]

# Main pygame loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Draws the room 
    screen.fill((0, 0 ,0))
    DefaulRoom(screen, center)

    # for agents to move 
    agents = [a for a in agents if not a.reached_exit]
    occupied = {agent._get_cell() for agent in agents}
    for agent in agents:
        agent.update(occupied)
        agent.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()