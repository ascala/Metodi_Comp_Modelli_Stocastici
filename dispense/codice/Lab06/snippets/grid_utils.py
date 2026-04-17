"""
Nome file: grid_utils.py

Scopo:
    Gestire la conversione tra indici di sito e coordinate fisiche su griglia uniforme.
"""

from __future__ import annotations
import numpy as np


def spatial_grid(N: int, dx: float) -> np.ndarray:
    if N < 0:
        raise ValueError("N deve essere non negativo.")
    if dx <= 0:
        raise ValueError("dx deve essere positivo.")
    return dx * np.arange(N + 1, dtype=float)


def site_to_x(sites, dx: float):
    if dx <= 0:
        raise ValueError("dx deve essere positivo.")
    return dx * np.asarray(sites, dtype=float)


def x0_from_i0(i0: int, dx: float) -> float:
    return float(site_to_x(i0, dx))


if __name__ == "__main__":
    print(spatial_grid(5, 0.25))
    print(site_to_x([0, 2, 4], 0.25))
    print(x0_from_i0(3, 0.25))
