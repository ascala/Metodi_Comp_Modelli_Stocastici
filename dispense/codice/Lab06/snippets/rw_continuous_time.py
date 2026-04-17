"""
Nome file: rw_continuous_time.py

Scopo:
    Simulare una traiettoria del random walk continuo nel tempo su una griglia 1D.
"""

from __future__ import annotations
import numpy as np

def simulate_ctrw(i0: int, N: int, r: float, ell: float, T: float, rng: np.random.Generator | None = None):
    if rng is None:
        rng = np.random.default_rng()
    if not (0 <= i0 <= N):
        raise ValueError("i0 deve appartenere all'intervallo [0, N].")
    if T < 0:
        raise ValueError("T deve essere non negativo.")
    if r < 0 or ell < 0:
        raise ValueError("I tassi devono essere non negativi.")

    t = 0.0
    i = int(i0)
    times = [t]
    sites = [i]

    while t < T:
        rate_right = r if i < N else 0.0
        rate_left = ell if i > 0 else 0.0
        a0 = rate_right + rate_left
        if a0 <= 0:
            break
        tau = rng.exponential(scale=1.0 / a0)
        if t + tau > T:
            break
        t += tau
        if rng.random() < rate_right / a0:
            i += 1
        else:
            i -= 1
        times.append(t)
        sites.append(i)

    return np.asarray(times, dtype=float), np.asarray(sites, dtype=int)

if __name__ == "__main__":
    rng = np.random.default_rng(12345)
    times, sites = simulate_ctrw(i0=10, N=20, r=1.2, ell=0.8, T=5.0, rng=rng)
    print("Numero di salti:", len(times) - 1)
    print("Sito finale:", sites[-1])
