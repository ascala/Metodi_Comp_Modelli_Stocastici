"""
Nome file: drift_diffusion_sde.py

Scopo:
    Simulare la SDE continua di drift-diffusion con schema di Euler--Maruyama.
"""

from __future__ import annotations
import numpy as np

def simulate_drift_diffusion(x0: float, a: float, D: float, T: float, dt: float, M: int, rng: np.random.Generator | None = None):
    if rng is None:
        rng = np.random.default_rng()
    if D < 0:
        raise ValueError("D deve essere non negativo.")
    if dt <= 0:
        raise ValueError("dt deve essere positivo.")
    if T < 0:
        raise ValueError("T deve essere non negativo.")
    if M < 1:
        raise ValueError("M deve essere almeno 1.")
    n_steps = int(np.round(T / dt))
    times = np.linspace(0.0, n_steps * dt, n_steps + 1)
    X = np.empty((M, n_steps + 1), dtype=float)
    X[:, 0] = x0
    sigma = np.sqrt(2.0 * D * dt)
    for n in range(n_steps):
        eta = rng.normal(size=M)
        X[:, n + 1] = X[:, n] + a * dt + sigma * eta
    return times, X

if __name__ == "__main__":
    times, X = simulate_drift_diffusion(x0=0.0, a=1.0, D=1.0, T=1.0, dt=1e-3, M=1000)
    print("Media finale:", X[:, -1].mean())
    print("Varianza finale:", X[:, -1].var(ddof=1))
