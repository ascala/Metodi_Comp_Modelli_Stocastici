# 05_gibbs_bonus.py
# Gibbs sampling per una gaussiana 2D correlata
#
# Target:
#   pi(x1, x2) \propto exp(-(x1^2 - 2 rho x1 x2 + x2^2) / [2(1-rho^2)])
#
# Condizionate:
#   x1 | x2 ~ N(rho x2, 1-rho^2)
#   x2 | x1 ~ N(rho x1, 1-rho^2)
#
# Il file è eseguibile così com'è.
# Se vuoi lasciarlo agli studenti da completare:
#   - metti USE_REFERENCE_GIBBS_STEP = False
#   - fai completare la funzione gibbs_step()

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------
# Parametri
# ----------------------------
rho = 0.9
x1_0 = -2.5
x2_0 = 2.0
n_burn = 2000
n_steps = 20000
seed = 12345

USE_REFERENCE_GIBBS_STEP = True


# ----------------------------
# Osservabili / target
# ----------------------------
def target_unnormalized(x1, x2, rho):
    q = (x1**2 - 2.0 * rho * x1 * x2 + x2**2) / (2.0 * (1.0 - rho**2))
    return np.exp(-q)


def observable_1(x1, x2):
    return x1


def observable_2(x1, x2):
    return x2


def observable_12(x1, x2):
    return x1 * x2


# ----------------------------
# TODO: un passo Gibbs
# ----------------------------
def gibbs_step(x1, x2, rho, rng):
    if USE_REFERENCE_GIBBS_STEP:
        sigma = np.sqrt(1.0 - rho**2)

        # x1^(t+1) ~ pi(x1 | x2^(t))
        x1_new = rng.normal(loc=rho * x2, scale=sigma)

        # x2^(t+1) ~ pi(x2 | x1^(t+1))
        x2_new = rng.normal(loc=rho * x1_new, scale=sigma)

        return x1_new, x2_new

    # TODO:
    # completare usando le due condizionate gaussiane
    #
    # placeholder eseguibile
    return x1, x2


# ----------------------------
# Simulazione
# ----------------------------
def run_gibbs_chain(x1_0, x2_0, rho, n_burn, n_steps, rng):
    x1 = x1_0
    x2 = x2_0

    for _ in range(n_burn):
        x1, x2 = gibbs_step(x1, x2, rho, rng)

    samples = np.empty((n_steps, 2), dtype=float)

    for t in range(n_steps):
        x1, x2 = gibbs_step(x1, x2, rho, rng)
        samples[t, 0] = x1
        samples[t, 1] = x2

    return samples


# ----------------------------
# Main
# ----------------------------
rng = np.random.default_rng(seed)

samples = run_gibbs_chain(x1_0, x2_0, rho, n_burn, n_steps, rng)

x1 = samples[:, 0]
x2 = samples[:, 1]

print("Media empirica di x1      =", np.mean(x1))
print("Media empirica di x2      =", np.mean(x2))
print("Media empirica di x1*x2   =", np.mean(x1 * x2))
print("Varianza empirica di x1   =", np.var(x1))
print("Varianza empirica di x2   =", np.var(x2))
print("Correlazione empirica     =", np.corrcoef(x1, x2)[0, 1])

# Trace plot di x1 e x2
plt.figure(figsize=(8, 4))
plt.plot(x1[:2000], label="x1")
plt.plot(x2[:2000], label="x2")
plt.xlabel("t")
plt.ylabel("valore")
plt.title("Trace plot Gibbs (primi 2000 passi)")
plt.legend()
plt.show()

# Traiettoria nel piano
plt.figure(figsize=(6, 6))
plt.plot(x1[:800], x2[:800], lw=1.0)
plt.scatter([x1[0]], [x2[0]], marker="x", s=80, label="inizio")
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Traiettoria Gibbs nel piano (primi 800 passi)")
plt.legend()
plt.axis("equal")
plt.show()

# Scatter finale
plt.figure(figsize=(6, 6))
plt.scatter(x1, x2, s=4, alpha=0.3)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Campioni Gibbs: gaussiana 2D correlata")
plt.axis("equal")
plt.show()

# Istogrammi marginali
plt.figure(figsize=(8, 4))
plt.hist(x1, bins=80, density=True, histtype="step", label="x1")
plt.hist(x2, bins=80, density=True, histtype="step", label="x2")
plt.xlabel("valore")
plt.ylabel("densità")
plt.title("Marginali empiriche")
plt.legend()
plt.show()
