"""
Nome file: full_propagator.py

Scopo:
    Evolvere la distribuzione tramite il propagatore completo del generatore.
"""

from __future__ import annotations
import numpy as np
from scipy.linalg import expm
from scipy.sparse import issparse
from scipy.sparse.linalg import expm_multiply

def propagate_full(L, p0, dt: float, n_steps: int, store_all: bool = True):
    if dt <= 0:
        raise ValueError("dt deve essere positivo.")
    if n_steps < 1:
        raise ValueError("n_steps deve essere almeno 1.")
    p = np.asarray(p0, dtype=float).copy()
    if store_all:
        out = np.empty((n_steps + 1, len(p)), dtype=float)
        out[0] = p
    if issparse(L):
        for n in range(n_steps):
            p = expm_multiply(dt * L, p)
            if store_all:
                out[n + 1] = p
    else:
        P = expm(dt * np.asarray(L, dtype=float))
        for n in range(n_steps):
            p = P @ p
            if store_all:
                out[n + 1] = p
    return out if store_all else p

if __name__ == "__main__":
    from build_generator_dense import build_generator_dense
    N = 20
    L = build_generator_dense(N, r=1.1, ell=0.9)
    p0 = np.zeros(N + 1)
    p0[N // 2] = 1.0
    out = propagate_full(L, p0, dt=0.1, n_steps=3)
    print("Normalizzazione finale:", out[-1].sum())
