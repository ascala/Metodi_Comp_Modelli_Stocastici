"""
Nome file: build_generator_sparse.py

Scopo:
    Costruire il generatore tridiagonale della master equation in formato sparso.
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import diags

def build_generator_sparse(N: int, r: float, ell: float, reflecting: bool = True, fmt: str = "csr"):
    if N < 1:
        raise ValueError("N deve essere almeno 1.")
    if r < 0 or ell < 0:
        raise ValueError("I tassi devono essere non negativi.")
    size = N + 1
    upper = np.full(size - 1, ell, dtype=float)
    lower = np.full(size - 1, r, dtype=float)
    diag = np.full(size, -(r + ell), dtype=float)
    diag[0] = -r
    diag[-1] = -ell
    _ = reflecting
    return diags(
        diagonals=[lower, diag, upper],
        offsets=[-1, 0, 1],
        shape=(size, size),
        format=fmt,
        dtype=float,
    )

if __name__ == "__main__":
    L = build_generator_sparse(N=8, r=1.4, ell=0.6)
    print(L)
    print("nnz =", L.nnz)
