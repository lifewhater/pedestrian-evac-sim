# NEED TO IMPLEMENT BFS FIRST FOR THE WHOLE ROOM
# - It will initialize the space for all the agents
import numpy as np
from collections import deque

def static_field(GRID_ROWS, GRID_COLS, exit_cells, wall_cells):
    static = np.full((GRID_ROWS, GRID_COLS), np.inf)
    queue = deque()

    for cell in exit_cells:
        static[cell] = 0
        queue.append(cell)
    
    while queue:
        row, col = queue.popleft()
        for dc, dr in [(-1, 0), (1,0), (0, 1), (0, -1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
                if (nr, nc) not in wall_cells and static[nr, nc] == np.inf:
                    static[nr, nc] = static[row, col] + 1
                    queue.append((nr, nc))
    
    return static