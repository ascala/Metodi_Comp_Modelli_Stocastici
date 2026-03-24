# 02_metropolis_boltzmann.py
# Metropolis per un peso di Boltzmann:
#   pi(x) \propto exp(-beta E(x))
#
# Confronto tra due forme equivalenti dell'accettazione:
#   (i) rapporto dei pesi
#   (ii) uso diretto di Delta E
#
# Il codice è quasi completo.

import numpy as np
import matplotlib.pyplot as plt
import time


# ----------------------------
# Parametri
# ----------------------------
beta = 2.0
sigma = 0.8
x0 = 0.0
n_burn = 5000
n_steps = 50000
seed = 12345


# ----------------------------
# Problema
# ----------------------------
def energy(x):
    return 0.25 * x**4 - 0.5 * x**2


def observable(x):
    return x**2


def weight_unnormalized(x, beta):
    return np.exp(-beta * energy(x))


# ----------------------------
# Un passo Metropolis: forma 1
# ----------------------------
def metropolis_step_ratio(x, sigma, beta, rng):
    x_new = x + rng.normal(0.0, sigma)

    r = weight_unnormalized(x_new, beta) / weight_unnormalized(x, beta)
    alpha = min(1.0, r)

    u = rng.uniform()

    if u < alpha:
        return x_new, True
    else:
        return x, False


# ----------------------------
# Un passo Metropolis: forma 2
# ----------------------------
def metropolis_step_deltaE(x, sigma, beta, rng):
    x_new = x + rng.normal(0.0, sigma)

    dE = energy(x_new) - energy(x)
    alpha = min(1.0, np.exp(-beta * dE))

    u = rng.uniform()

    if u < alpha:
        return x_new, True
    else:
        return x, False


# ----------------------------
# Simulazione completa
# ----------------------------
def run_chain(step_function, x0, sigma, beta, n_burn, n_steps, rng):
    x = x0

    # burn-in
    for _ in range(n_burn):
        x, _ = step_function(x, sigma, beta, rng)

    samples = np.empty(n_steps)
    accepted = 0

    for i in range(n_steps):
        x, acc = step_function(x, sigma, beta, rng)
        samples[i] = x
        if acc:
            accepted += 1

    acceptance_rate = accepted / n_steps
    estimate = np.mean(observable(samples))

    return samples, estimate, acceptance_rate


# ----------------------------
# Benchmark
# ----------------------------
rng1 = np.random.default_rng(seed)
t0 = time.perf_counter()
samples_ratio, est_ratio, acc_ratio = run_chain(
    metropolis_step_ratio, x0, sigma, beta, n_burn, n_steps, rng1
)
t1 = time.perf_counter()

rng2 = np.random.default_rng(seed)
t2 = time.perf_counter()
samples_dE, est_dE, acc_dE = run_chain(
    metropolis_step_deltaE, x0, sigma, beta, n_burn, n_steps, rng2
)
t3 = time.perf_counter()

print("Forma con rapporto")
print("  stima <x^2>        =", est_ratio)
print("  acceptance rate    =", acc_ratio)
print("  tempo totale       =", t1 - t0)

print()
print("Forma con Delta E")
print("  stima <x^2>        =", est_dE)
print("  acceptance rate    =", acc_dE)
print("  tempo totale       =", t3 - t2)

# Trace plot
plt.figure(figsize=(8, 4))
plt.plot(samples_dE[:2000])
plt.xlabel("t")
plt.ylabel("x_t")
plt.title("Trace plot Metropolis (forma con Delta E)")
plt.show()

# Istogramma
plt.figure(figsize=(8, 4))
plt.hist(samples_dE, bins=80, density=True)
plt.xlabel("x")
plt.ylabel("densità")
plt.title("Istogramma dei campioni MCMC")
plt.show()
