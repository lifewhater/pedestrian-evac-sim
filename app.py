import pygame, random, os, cv2
import numpy as np
from src.environment import DefaultRoom
#from src.gradient_descent_method import Agents
# from tests.test_bfs import static_field
from src.agents import Agents
from src.static_field import static_field
from src.dynamic_field import deposit_dynamic_field, update_dynamic_field
from config import GRID_COLS, GRID_ROWS, CELL_SIZE, ALPHA, DELTA, KD, KS, NUM_AGENTS
import matplotlib.pyplot as plt

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Build the room and compute the BFS-based static floor field
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
room = DefaultRoom(screen, center)
field = static_field(GRID_COLS, GRID_ROWS, room["exit_cells"], room["wall_cells"])
dynamic_field = np.zeros_like(field, dtype=float)

# Spawn agents at unique cell centers so no two agents share a cell at start
random.seed()
all_cells = [
    (r, c) for r in range(GRID_ROWS // 2, GRID_ROWS) for c in range(GRID_COLS)
    if (r, c) not in room["exit_cells"] and (r, c) not in room["wall_cells"]
]
random.shuffle(all_cells)
agents = [
    Agents(room, field, dynamic_field, position=(
        room["x"] + c * CELL_SIZE + CELL_SIZE / 2,
        room["y"] + r * CELL_SIZE + CELL_SIZE / 2,
    ))
    for r, c in all_cells[:NUM_AGENTS]
]
font = pygame.font.SysFont(None, 36)
history = []
step = 0
flow_data = []  # This should be populated with actual flow rate data during the simulation
os.makedirs("frames", exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("evacuation.mp4", fourcc, 30, (screen.get_width(), screen.get_height()))

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
    moved_cells = []
    for cell, competing in intention.items():
        winner = random.choice(competing)
        previous_cell = winner._get_cell()
        winner.move_to(cell)
        moved_cells.append((previous_cell, cell))

    for previous_cell, _ in moved_cells:
        deposit_dynamic_field(dynamic_field, previous_cell)

    dynamic_field = update_dynamic_field(dynamic_field)
    for agent in agents:
        agent.dynamic_field = dynamic_field

    agents = [a for a in agents if not a.reached_exit]
    history.append((step, 0 + len(agents)))
    step += 1
    # Draw all remaining agents
    for agent in agents:
        agent.draw(screen)

    text = font.render(f"Remaining: {len(agents)}", True, "white")
    screen.blit(text, (10, 10))

    param_lines = [
        f"ALPHA = {ALPHA}",
        f"DELTA = {DELTA}",
        f"KD    = {KD}",
        f"KS    = {KS}",
        f"N     = {NUM_AGENTS}",
    ]
    small_font = pygame.font.SysFont("monospace", 20)
    for i, line in enumerate(param_lines):
        label = small_font.render(line, True, (200, 200, 200))
        screen.blit(label, (10, 50 + i * 24))
    pygame.display.flip()

    clock.tick(0)

pygame.quit()

out.release()
print("Saved evacuation.mp4")