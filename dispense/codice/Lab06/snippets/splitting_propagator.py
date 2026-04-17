"""
Nome file: splitting_propagator.py

Scopo:
    Evolvere la distribuzione con operator splitting tra drift e diffusione.
"""

from __future__ import annotations
import numpy as np
from scipy.sparse.linalg import expm_multiply

def propagate_splitting(L_drift, L_diff, p0, dt: float, n_steps: int, strang: bool = False, store_all: bool = True):
    if dt <= 0:
        raise ValueError("dt deve essere positivo.")
    if n_steps < 1:
        raise ValueError("n_steps deve essere almeno 1.")
    p = np.asarray(p0, dtype=float).copy()
    if store_all:
        out = np.empty((n_steps + 1, len(p)), dtype=float)
        out[0] = p
    for n in range(n_steps):
        if strang:
            p = expm_multiply(0.5 * dt * L_drift, p)
            p = expm_multiply(dt * L_diff, p)
            p = expm_multiply(0.5 * dt * L_drift, p)
        else:
            p = expm_multiply(dt * L_drift, p)
            p = expm_multiply(dt * L_diff, p)
        if store_all:
            out[n + 1] = p
    return out if store_all else p

if __name__ == "__main__":
    from split_generator import split_generator
    N = 30
    Ld, Lf = split_generator(N, r=1.2, ell=0.8)
    p0 = np.zeros(N + 1)
    p0[N // 2] = 1.0
    out = propagate_splitting(Ld, Lf, p0, dt=0.1, n_steps=5, strang=True)
    print("Normalizzazione finale:", out[-1].sum())
