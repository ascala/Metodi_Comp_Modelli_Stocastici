import numpy as np
import matplotlib.pyplot as plt

seed = 1234
M = 20000
Tlist = [10, 20, 50, 100, 200, 500, 1000]

rng = np.random.default_rng(seed)

msd = []
for T in Tlist:
    # Passi +/-1: matrice M x T
    steps = rng.choice([-1, 1], size=(M, T))
    X = steps.sum(axis=1)      # final position
    msd.append(np.mean(X**2))  # Mean Square Displacement <X_T^2>

T = np.array(Tlist, dtype=float)
msd = np.array(msd)

# Fit lineare su log-log: msd ~ T^beta atteso beta ~ 1
beta, a = np.linalg.lstsq(
    np.vstack([np.log(T), np.ones_like(T)]).T,
    np.log(msd),
    rcond=None
)[0]

plt.figure()
plt.loglog(T, msd, marker="o", linestyle="none", label="estimated MSD")
plt.loglog(T, np.exp(a) * T**beta, label=f"fit: exponent {beta:.3f}")

plt.title(r"Random walk: ⟨$X^2(T)$⟩ $\sim$ $T$  (ampiezza $\sim$ $T^{1/2}$)")
plt.xlabel(r"$T$")
plt.ylabel(r"⟨$X^2(T)$⟩")
plt.legend()
plt.show()
