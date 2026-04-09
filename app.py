import pygame, random
from src.environment import DefaultRoom
# from src.gradient_descent_method import Agents
from src.agents import Agents
from src.static_field import static_field
from config import GRID_COLS, GRID_ROWS, CELL_SIZE

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Build the room and compute the BFS-based static floor field
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
room = DefaultRoom(screen, center)
field = static_field(GRID_COLS, GRID_ROWS, room["exit_cells"], room["wall_cells"])

# Spawn agents at unique cell centers so no two agents share a cell at start
random.seed(90)
all_cells = [
    (r, c) for r in range(GRID_ROWS) for c in range(GRID_COLS)
    if (r, c) not in room["exit_cells"] and (r, c) not in room["wall_cells"]
]
random.shuffle(all_cells)
agents = [
    Agents(room, field, position=(
        room["x"] + c * CELL_SIZE + CELL_SIZE / 2,
        room["y"] + r * CELL_SIZE + CELL_SIZE / 2,
    ))
    for r, c in all_cells[:400]
]
font = pygame.font.SysFont(None, 36)

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen and redraw room
    screen.fill((0, 0, 0))
    DefaultRoom(screen, center)

    # Remove agents that have reached the exit
    agents = [a for a in agents if not a.reached_exit]

    # Build set of currently occupied cells for conflict resolution
    occupied = {agent._get_cell() for agent in agents}

    # Gather each agent's intended next cell (Kirchner stochastic model)
    intention = {}
    for agent in agents:
        cell = agent.get_intention(occupied, room["wall_cells"])
        if cell is not None:
            intention.setdefault(cell, []).append(agent)

    # Resolve conflicts: if multiple agents want the same cell, pick one at random
    for cell, competing in intention.items():
        winner = random.choice(competing)
        winner.move_to(cell)

    # Draw all remaining agents
    for agent in agents:
        agent.draw(screen)

    text = font.render(f"Remaining: {len(agents)}", True, "white")
    screen.blit(text, (10, 10))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

