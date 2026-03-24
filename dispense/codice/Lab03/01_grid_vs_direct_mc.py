# 01_grid_vs_direct_mc.py
# Confronto tra:
#   (i) integrazione numerica su griglia
#   (ii) Monte Carlo diretto
#
# Stimiamo
#   <O> = [\int O(x) exp(-beta E(x)) dx] / [\int exp(-beta E(x)) dx]
#
# Esempio:
#   E(x) = x^4/4 - x^2/2
#   O(x) = x^2

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Parametri
# ----------------------------
beta = 2.0
L = 3.0
n_grid = 4001
n_mc = 200000
seed = 12345


# ----------------------------
# Problema
# ----------------------------
def energy(x):
    return 0.25 * x**4 - 0.5 * x**2


def observable(x):
    return x**2


def boltzmann_weight(x, beta):
    return np.exp(-beta * energy(x))


# ----------------------------
# Metodo 1: integrazione su griglia
# ----------------------------
def estimate_grid(beta, L, n_grid):
    x = np.linspace(-L, L, n_grid)
    dx = x[1] - x[0]

    w = boltzmann_weight(x, beta)
    num = np.sum(observable(x) * w) * dx
    den = np.sum(w) * dx

    return num / den, x, w


# ----------------------------
# Metodo 2: Monte Carlo diretto
# ----------------------------
def estimate_direct_mc(beta, L, n_mc, rng):
    x = rng.uniform(-L, L, size=n_mc)

    w = boltzmann_weight(x, beta)

    # integrali su [-L, L]
    num = 2.0 * L * np.mean(observable(x) * w)
    den = 2.0 * L * np.mean(w)

    return num / den, x


# ----------------------------
# Main
# ----------------------------
rng = np.random.default_rng(seed)

est_grid, x_grid, w_grid = estimate_grid(beta, L, n_grid)
est_mc, x_mc = estimate_direct_mc(beta, L, n_mc, rng)

print("Stima su griglia        =", est_grid)
print("Stima Monte Carlo       =", est_mc)
print("Differenza assoluta     =", abs(est_grid - est_mc))

# Grafico del peso non normalizzato
plt.figure(figsize=(7, 4))
plt.plot(x_grid, w_grid)
plt.xlabel("x")
plt.ylabel(r"$e^{-\beta E(x)}$")
plt.title("Peso di Boltzmann non normalizzato")
plt.show()

# Istogramma dei campioni uniformi del MC diretto
plt.figure(figsize=(7, 4))
plt.hist(x_mc, bins=60, density=True)
plt.xlabel("x")
plt.ylabel("densità")
plt.title("Campioni uniformi usati nel Monte Carlo diretto")
plt.show()
