"""
Nome file: split_generator.py

Scopo:
    Decomporre il generatore discreto in parte di drift e parte diffusiva.
"""

from __future__ import annotations
import numpy as np
from scipy.sparse import diags

def split_generator(N: int, r: float, ell: float, fmt: str = "csr"):
    if N < 1:
        raise ValueError("N deve essere almeno 1.")
    size = N + 1
    a = 0.5 * (ell - r)
    b = 0.5 * (ell + r)
    upper_drift = np.full(size - 1, a, dtype=float)
    lower_drift = np.full(size - 1, -a, dtype=float)
    diag_drift = np.zeros(size, dtype=float)
    upper_diff = np.full(size - 1, b, dtype=float)
    lower_diff = np.full(size - 1, b, dtype=float)
    diag_diff = np.full(size, -2.0 * b, dtype=float)
    diag_diff[0] = -r
    diag_diff[-1] = -ell
    upper_diff[0] = ell
    lower_diff[-1] = r
    upper_drift[0] = 0.0
    lower_drift[-1] = 0.0
    L_drift = diags([lower_drift, diag_drift, upper_drift], offsets=[-1, 0, 1], shape=(size, size), format=fmt)
    L_diff = diags([lower_diff, diag_diff, upper_diff], offsets=[-1, 0, 1], shape=(size, size), format=fmt)
    return L_drift, L_diff

if __name__ == "__main__":
    Ld, Lf = split_generator(N=10, r=1.4, ell=0.8)
    print("nnz drift:", Ld.nnz)
    print("nnz diff :", Lf.nnz)
