import numpy as np
import heapq, math

# Used Djikstra for floor field which accounts for diagonal movements
def static_field(row, col, exit_cells, wall_cells):
    static = np.full((row, col), np.inf)
    heap = []

    for cells in exit_cells:
        static[cells] = 0
        heapq.heappush(heap, (0, cells))

    while heap:
        cost, (r, c) = heapq.heappop(heap)
        if cost > static[r, c]:
            continue

        for dr, dc in [(-1, 1,), (1, 1), (-1, -1), (1, -1), (1, 0), (0, -1), (0, 1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            edge_cost = math.sqrt(2) if dr!= 0 and dc!= 0 else 1.0
            new_cost = edge_cost + cost
            if 0 <= nr < row and 0 <= nc < col:
                if (nr, nc) not in wall_cells and new_cost < static[nr, nc]:
                    static[nr, nc] = new_cost
                    heapq.heappush(heap, (new_cost, (nr, nc)))

    return static