# 03_correlation_and_burnin.py
# Burn-in, media cumulativa e correlazione temporale.
#
# Questo file è volutamente da completare.
# Il codice però gira già, perché le funzioni TODO
# usano temporaneamente una reference implementation.
#
# Per lasciare davvero il lavoro agli studenti:
#   - mettere USE_REFERENCE_CUMULATIVE = False
#   - mettere USE_REFERENCE_CORRELATION = False
# e completare le funzioni TODO.

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Parametri
# ----------------------------
beta = 2.0
sigma = 0.8
n_steps = 30000
tau_max = 200
seed = 12345

initial_conditions = [-3.0, 0.0, 3.0]

USE_REFERENCE_CUMULATIVE = True
USE_REFERENCE_CORRELATION = True


# ----------------------------
# Problema
# ----------------------------
def energy(x):
    return 0.25 * x**4 - 0.5 * x**2


def observable(x):
    return x**2


def metropolis_step(x, sigma, beta, rng):
    x_new = x + rng.normal(0.0, sigma)
    dE = energy(x_new) - energy(x)
    alpha = min(1.0, np.exp(-beta * dE))

    if rng.uniform() < alpha:
        return x_new
    else:
        return x


def run_chain(x0, sigma, beta, n_steps, rng):
    x = x0
    samples = np.empty(n_steps)

    for i in range(n_steps):
        x = metropolis_step(x, sigma, beta, rng)
        samples[i] = x

    return samples


# ----------------------------
# TODO 1: media cumulativa
# ----------------------------
def cumulative_mean(values):
    if USE_REFERENCE_CUMULATIVE:
        csum = np.cumsum(values)
        n = np.arange(1, len(values) + 1)
        return csum / n

    # TODO:
    # implementare la media cumulativa senza usare la reference.
    # deve restituire un array m tale che
    # m[n-1] = (values[0] + ... + values[n-1]) / n

    # placeholder eseguibile
    return np.zeros_like(values, dtype=float)


# ----------------------------
# TODO 2: correlazione non centrata
# C(tau) = < O_{t+tau} O_t >
# ----------------------------
def corr_noncentrata(values, tau_max):
    if USE_REFERENCE_CORRELATION:
        values = np.asarray(values, dtype=float)
        N = len(values)
        C = np.empty(tau_max + 1)

        for tau in range(tau_max + 1):
            C[tau] = np.mean(values[:N - tau] * values[tau:])

        return C

    # TODO:
    # implementare la formula
    # C[tau] = mean(values[:N-tau] * values[tau:])
    #
    # placeholder eseguibile
    return np.ones(tau_max + 1)


# ----------------------------
# TODO 3: correlazione centrata e normalizzata
# ----------------------------
def corr_centrata_normalizzata(values, tau_max):
    values = np.asarray(values, dtype=float)
    m = np.mean(values)
    centered = values - m

    C = corr_noncentrata(centered, tau_max)

    # TODO:
    # normalizzare in modo che C[0] = 1
    #
    # placeholder eseguibile
    if C[0] != 0.0:
        return C / C[0]
    else:
        return C


# ----------------------------
# Esperimenti
# ----------------------------
rng = np.random.default_rng(seed)

all_samples = []
all_obs = []

for x0 in initial_conditions:
    samples = run_chain(x0, sigma, beta, n_steps, rng)
    obs = observable(samples)

    all_samples.append(samples)
    all_obs.append(obs)

# Trace plot di x_t
plt.figure(figsize=(8, 4))
for i, samples in enumerate(all_samples):
    plt.plot(samples[:3000], label=f"x0 = {initial_conditions[i]}")
plt.xlabel("t")
plt.ylabel("x_t")
plt.title("Trace plot da condizioni iniziali diverse")
plt.legend()
plt.show()

# Media cumulativa di O_t = x_t^2
plt.figure(figsize=(8, 4))
for i, obs in enumerate(all_obs):
    plt.plot(cumulative_mean(obs), label=f"x0 = {initial_conditions[i]}")
plt.xlabel("n")
plt.ylabel("media cumulativa di $x_t^2$")
plt.title("Burn-in e stabilizzazione della media cumulativa")
plt.legend()
plt.show()

# Correlazione sulla catena partita da x0 = 0
obs0 = all_obs[1]
C_raw = corr_noncentrata(obs0, tau_max)
C_norm = corr_centrata_normalizzata(obs0, tau_max)

plt.figure(figsize=(8, 4))
plt.plot(C_raw)
plt.xlabel(r"$\tau$")
plt.ylabel(r"$C(\tau)$")
plt.title("Correlazione non centrata")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(C_norm)
plt.xlabel(r"$\tau$")
plt.ylabel(r"$\widetilde C(\tau)$")
plt.title("Correlazione centrata e normalizzata")
plt.show()
