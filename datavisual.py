import matplotlib.pyplot as plt
from src.static_field import static_field
from config import GRID_ROWS, GRID_COLS, CELL_SIZE, WIDTH

exit_width = 40
exitX = (WIDTH - exit_width) // 2
col_start = exitX // CELL_SIZE
col_end = (exitX + exit_width) // CELL_SIZE
exit_cells = set((0, col) for col in range(col_start, col_end + 1))
wall_cells = set() 

def field_heatmap(static_field, path="heatmap.png"):
    field = static_field(GRID_ROWS, GRID_COLS, exit_cells, wall_cells)
    # field_display = np.where(np.isinf(field), np.nan, field)
    plt.figure(figsize=(10, 6))
    plt.imshow(field, cmap="Purples_r", origin="upper")
    plt.title("Static Floor Field")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def agents_exit_plot(history, path="agents_v_time.png"):
    steps,remaining = zip(*history)
    total = remaining[0]
    exited = [total - r for r in remaining]
    plt.figure(figsize=(8, 5))
    plt.plot(steps, exited, color="steelblue", linewidth=2)
    plt.xlabel("Time Step")
    plt.ylabel("Agents Exited")
    plt.title("Agents Exited vs Time")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()