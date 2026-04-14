import numpy as np
from config import ALPHA, DELTA

def deposit_dynamic_field(dynamic_field, cell, amount=1.0):
    row, col = cell
    if 0 <= row < dynamic_field.shape[0] and 0 <= col < dynamic_field.shape[1]:
        dynamic_field[row, col] += amount


def update_dynamic_field(dynamic_field, alpha=ALPHA, delta=DELTA):
    decayed = dynamic_field * (1 - delta)
    padded = np.pad(decayed, 1, mode="constant")

    updated = decayed * (1 - alpha)
    share = alpha / 4.0
    updated += share * (
        padded[:-2, 1:-1]
        + padded[2:, 1:-1]
        + padded[1:-1, :-2]
        + padded[1:-1, 2:]
    )

    return updated