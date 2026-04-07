import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def field_heatmap(static_field, path="heatmap.png"):
    plt.figure(figsize=(8, 6))
    plt.imshow(static_field, cmap="coolwarm", interpolation="nearest", origin="upper")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"Heatmap saved to {path}")

def agents_exit_plot(history, path="agents_vs_time.png"):
    """history: list of (time_step, agents_remaining) tuples"""
    steps, remaining = zip(*history)
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
    print(f"Exit plot saved to {path}")
