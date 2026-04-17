"""
Nome file: gaussian_theory.py

Scopo:
    Fornire la soluzione teorica gaussiana per la drift-diffusion continua
    e i parametri efficaci letti dal modello discreto.
"""

from __future__ import annotations
import numpy as np


def theoretical_mean(t, x0: float, a: float):
    t = np.asarray(t, dtype=float)
    return x0 + a * t


def theoretical_variance(t, D: float):
    t = np.asarray(t, dtype=float)
    return 2.0 * D * t


def gaussian_pdf(x, t: float, x0: float, a: float, D: float):
    x = np.asarray(x, dtype=float)
    if t <= 0:
        raise ValueError("Per la pdf gaussiana serve t > 0.")
    if D <= 0:
        raise ValueError("Per la pdf gaussiana serve D > 0.")
    mean = theoretical_mean(t, x0, a)
    var = theoretical_variance(t, D)
    return np.exp(-(x - mean) ** 2 / (2.0 * var)) / np.sqrt(2.0 * np.pi * var)


def effective_drift(r: float, ell: float, dx: float) -> float:
    if dx <= 0:
        raise ValueError("dx deve essere positivo.")
    return (r - ell) * dx


def effective_diffusion(r: float, ell: float, dx: float) -> float:
    if dx <= 0:
        raise ValueError("dx deve essere positivo.")
    return 0.5 * (r + ell) * dx**2


def effective_parameters(r: float, ell: float, dx: float):
    return effective_drift(r, ell, dx), effective_diffusion(r, ell, dx)


if __name__ == "__main__":
    x = np.linspace(-5, 5, 200)
    v, D = effective_parameters(r=1.4, ell=0.8, dx=0.5)
    p = gaussian_pdf(x, t=1.0, x0=0.0, a=v, D=D)
    print("v =", v, "D =", D)
    print("Integrale approssimato:", np.trapz(p, x))
