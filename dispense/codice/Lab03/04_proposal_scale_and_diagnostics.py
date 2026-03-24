# 04_proposal_scale_and_diagnostics.py
# Confronto tra diverse scale di proposta:
#   - acceptance rate
#   - trace plot
#   - istogramma
#   - correlazione
#
# Anche questo file è volutamente incompleto.
# Le funzioni TODO hanno un fallback, così il codice gira.
#
# Per assegnarlo davvero:
#   - mettere USE_REFERENCE_CORR = False
#   - mettere USE_REFERENCE_ACCEPTANCE = False
# e completare le funzioni.

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Parametri
# ----------------------------
beta = 2.0
x0 = 0.0
n_burn = 5000
n_steps = 30000
tau_max = 100
seed = 12345

sigmas = [0.1, 0.8, 2.5]

USE_REFERENCE_CORR = True
USE_REFERENCE_ACCEPTANCE = True


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
        return x_new, True
    else:
        return x, False


def run_chain_with_diagnostics(x0, sigma, beta, n_burn, n_steps, rng):
    x = x0

    # burn-in
    for _ in range(n_burn):
        x, _ = metropolis_step(x, sigma, beta, rng)

    samples = np.empty(n_steps)
    accepted_flags = np.zeros(n_steps, dtype=int)

    for i in range(n_steps):
        x, acc = metropolis_step(x, sigma, beta, rng)
        samples[i] = x
        accepted_flags[i] = int(acc)

    return samples, accepted_flags


# ----------------------------
# TODO 1: acceptance rate
# ----------------------------
def acceptance_rate(accepted_flags):
    if USE_REFERENCE_ACCEPTANCE:
        return np.mean(accepted_flags)

    # TODO:
    # restituire la frazione di mosse accettate
    #
    # placeholder eseguibile
    return 0.0


# ----------------------------
# TODO 2: correlazione non centrata
# ----------------------------
def corr_noncentrata(values, tau_max):
    if USE_REFERENCE_CORR:
        values = np.asarray(values, dtype=float)
        N = len(values)
        C = np.empty(tau_max + 1)

        for tau in range(tau_max + 1):
            C[tau] = np.mean(values[:N - tau] * values[tau:])

        return C

    # TODO:
    # implementare la correlazione non centrata
    #
    # placeholder eseguibile
    return np.ones(tau_max + 1)


# ----------------------------
# Main
# ----------------------------
rng = np.random.default_rng(seed)

all_samples = []
all_acceptance = []
all_corr = []

for sigma in sigmas:
    samples, accepted_flags = run_chain_with_diagnostics(
        x0, sigma, beta, n_burn, n_steps, rng
    )

    acc = acceptance_rate(accepted_flags)
    corr = corr_noncentrata(observable(samples), tau_max)

    all_samples.append(samples)
    all_acceptance.append(acc)
    all_corr.append(corr)

    print("sigma =", sigma)
    print("  acceptance rate =", acc)
    print("  stima <x^2>     =", np.mean(observable(samples)))
    print()

# Trace plot
plt.figure(figsize=(8, 4))
for i, sigma in enumerate(sigmas):
    plt.plot(all_samples[i][:2000], label=f"sigma = {sigma}")
plt.xlabel("t")
plt.ylabel("x_t")
plt.title("Trace plot per diverse scale di proposta")
plt.legend()
plt.show()

# Istogrammi
plt.figure(figsize=(8, 4))
for i, sigma in enumerate(sigmas):
    plt.hist(all_samples[i], bins=80, density=True, histtype="step", label=f"sigma = {sigma}")
plt.xlabel("x")
plt.ylabel("densità")
plt.title("Istogrammi per diverse scale di proposta")
plt.legend()
plt.show()

# Correlazioni
plt.figure(figsize=(8, 4))
for i, sigma in enumerate(sigmas):
    plt.plot(all_corr[i], label=f"sigma = {sigma}")
plt.xlabel(r"$\tau$")
plt.ylabel(r"$C(\tau)$")
plt.title("Correlazione non centrata di $x_t^2$")
plt.legend()
plt.show()

# Grafico acceptance rate
plt.figure(figsize=(6, 4))
plt.plot(sigmas, all_acceptance, "o-")
plt.xlabel(r"$\sigma$")
plt.ylabel("acceptance rate")
plt.title("Acceptance rate vs scala di proposta")
plt.show()
