"""
Nome file: build_generator_dense.py

Scopo:
    Costruire il generatore tridiagonale della master equation in forma densa.
"""

from __future__ import annotations
import numpy as np

def build_generator_dense(N: int, r: float, ell: float, reflecting: bool = True) -> np.ndarray:
    if N < 1:
        raise ValueError("N deve essere almeno 1.")
    if r < 0 or ell < 0:
        raise ValueError("I tassi devono essere non negativi.")
    size = N + 1
    L = np.zeros((size, size), dtype=float)
    for j in range(size):
        rate_right = r if j < N else 0.0
        rate_left = ell if j > 0 else 0.0
        if reflecting:
            pass
        else:
            if j == 0:
                rate_left = 0.0
                rate_right = r
            if j == N:
                rate_right = 0.0
                rate_left = ell
        if j < N:
            L[j + 1, j] += rate_right
        if j > 0:
            L[j - 1, j] += rate_left
        L[j, j] -= (rate_right + rate_left)
    return L

if __name__ == "__main__":
    L = build_generator_dense(N=5, r=1.2, ell=0.8)
    print(L)
    print("Somme di colonna:", L.sum(axis=0))
