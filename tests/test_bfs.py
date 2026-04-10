import numpy as np 
from collections import deque

row, col = 3, 3
exit_cells = [(0, 1)]
wall_cells = []

def static_field(row, col, exit_cells, wall_cells):
    static = np.full((row, col), np.inf)
    queue = deque()

    for cells in exit_cells:
        static[cells] = 0
        queue.append(cells)

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = dr + r, dc + c
            if 0 <= nr < row and 0 <= nc < col:
                if (nr, nc) not in wall_cells and static[nr, nc] == np.inf:
                    static[nr, nc] = static [r, c] + 1
                    queue.append((nr, nc))

    return static

grid = static_field(row, col, exit_cells, wall_cells)

print(grid)


