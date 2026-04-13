SCALE = 4
HEIGHT = 600
WIDTH = 800
CELL_SIZE = 20
RADIUS = CELL_SIZE // 3
GRID_COLS = WIDTH // CELL_SIZE
GRID_ROWS = HEIGHT // CELL_SIZE

# Kirchner urgency factor — controls how strongly agents prefer the shortest path.
# High KD (e.g. 20): agents funnel aggressively toward exit → strong bottleneck.
# Low KD (e.g. 1-2): agents spread out more randomly → weaker bottleneck.
KD = 20
KS = 25

# Defined in the paper
# Diffusion probability
ALPHA = 0.1
# Decay probabilty
DELTA = 0.1

NUM_AGENTS = 400


