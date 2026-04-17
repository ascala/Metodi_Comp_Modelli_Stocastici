"""
Nome file: euler_propagator.py

Scopo:
    Evolvere la distribuzione con il metodo di Euler esplicito.
"""

from __future__ import annotations
import numpy as np

def propagate_euler(L, p0, dt: float, n_steps: int, store_all: bool = True):
    if dt <= 0:
        raise ValueError("dt deve essere positivo.")
    if n_steps < 1:
        raise ValueError("n_steps deve essere almeno 1.")
    p = np.asarray(p0, dtype=float).copy()
    if store_all:
        out = np.empty((n_steps + 1, len(p)), dtype=float)
        out[0] = p
    for n in range(n_steps):
        p = p + dt * (L @ p)
        if store_all:
            out[n + 1] = p
    return out if store_all else p

if __name__ == "__main__":
    from build_generator_dense import build_generator_dense
    N = 20
    L = build_generator_dense(N, r=1.2, ell=0.8)
    p0 = np.zeros(N + 1)
    p0[N // 2] = 1.0
    out = propagate_euler(L, p0, dt=1e-2, n_steps=10)
    print("Normalizzazione finale:", out[-1].sum())
