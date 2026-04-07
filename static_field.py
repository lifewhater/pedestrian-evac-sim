import numpy as np
from collections import deque

def static_field(GRID_COLS, GRID_ROWS, exit_cells, wall_cells):
    # Shape is (GRID_ROWS, GRID_COLS) so indexing is [row, col]
    static = np.full((GRID_ROWS, GRID_COLS), np.inf)
    queue = deque()

    for cell in exit_cells:
        static[cell] = 0
        queue.append(cell)

    while queue:
        row, col = queue.popleft()
        for dr, dc in [(-1,0), (1,0), (0,1), (0,-1)]:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                if (nr, nc) not in wall_cells and static[nr, nc] == np.inf:
                    static[nr, nc] = static[row, col] + 1
                    queue.append((nr, nc))

    return static