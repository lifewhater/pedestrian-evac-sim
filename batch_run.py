"""
Runs the evacuation simulation NUM_RUNS times (headless, no window)
and plots full evacuation time per run.

Change NUM_RUNS at the top to control how many runs to execute.
"""
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import random
import numpy as np
import pygame
import matplotlib.pyplot as plt

from src.environment import DefaultRoom
from src.agents import Agents
from src.static_field import static_field
from src.dynamic_field import deposit_dynamic_field, update_dynamic_field
from config import GRID_COLS, GRID_ROWS, CELL_SIZE, ALPHA, DELTA, KD, KS, NUM_AGENTS

# ── Configure here ────────────────────────────────────────────────────────────
NUM_RUNS = 10
# ─────────────────────────────────────────────────────────────────────────────

# Initialise pygame once (dummy driver → no window)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
room = DefaultRoom(screen, center)
static_f = static_field(GRID_COLS, GRID_ROWS, room["exit_cells"], room["wall_cells"])

# Pre-compute all valid spawn cells (same logic as app.py)
all_floor_cells = [
    (r, c)
    for r in range(GRID_ROWS // 2, GRID_ROWS)
    for c in range(GRID_COLS)
    if (r, c) not in room["exit_cells"] and (r, c) not in room["wall_cells"]
]


def run_once(seed: int) -> int:
    """Run one full simulation and return the step count when the room empties."""
    random.seed(seed)
    dynamic_f = np.zeros_like(static_f, dtype=float)

    cells = all_floor_cells[:]
    random.shuffle(cells)
    agents = [
        Agents(
            room, static_f, dynamic_f,
            position=(
                room["x"] + c * CELL_SIZE + CELL_SIZE / 2,
                room["y"] + r * CELL_SIZE + CELL_SIZE / 2,
            ),
        )
        for r, c in cells[:NUM_AGENTS]
    ]

    step = 0
    while True:
        agents = [a for a in agents if not a.reached_exit]
        if not agents:
            break

        occupied = {a._get_cell() for a in agents}
        intention: dict = {}
        for agent in agents:
            cell = agent.get_intention(occupied, room["wall_cells"])
            if cell is not None:
                intention.setdefault(cell, []).append(agent)

        moved_cells = []
        for cell, competing in intention.items():
            winner = random.choice(competing)
            moved_cells.append(winner._get_cell())
            winner.move_to(cell)

        for prev in moved_cells:
            deposit_dynamic_field(dynamic_f, prev)

        dynamic_f = update_dynamic_field(dynamic_f)
        for a in agents:
            a.dynamic_field = dynamic_f

        agents = [a for a in agents if not a.reached_exit]
        step += 1

    return step


# ── Batch run ─────────────────────────────────────────────────────────────────
evac_times = []
for i in range(NUM_RUNS):
    print(f"Run {i + 1}/{NUM_RUNS}...", end=" ", flush=True)
    t = run_once(seed=i)
    evac_times.append(t)
    print(f"{t} steps")

pygame.quit()

mean_t = np.mean(evac_times)
std_t = np.std(evac_times)
print(f"\nMean: {mean_t:.1f} steps   Std: {std_t:.1f} steps")

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
runs = list(range(1, NUM_RUNS + 1))

ax.plot(runs, evac_times, marker="o", color="steelblue", linewidth=2, label="Evacuation time")
ax.axhline(mean_t, color="tomato", linestyle="--", linewidth=1.5, label=f"Mean = {mean_t:.0f} steps")
ax.fill_between(runs, mean_t - std_t, mean_t + std_t, color="tomato", alpha=0.12, label=f"±1σ = {std_t:.1f}")

ax.set_xlabel("Run #")
ax.set_ylabel("Full Evacuation Time (steps)")
ax.set_title(
    f"Full Evacuation Time across {NUM_RUNS} Runs\n"
    f"α={ALPHA}   δ={DELTA}   KD={KD}   KS={KS}   N={NUM_AGENTS}"
)
ax.set_xticks(runs)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("evac_times.png", dpi=150)
print("Plot saved to evac_times.png")
plt.show()
