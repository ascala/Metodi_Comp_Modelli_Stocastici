import numpy as np
import matplotlib.pyplot as plt

seed = 1234
M = 20000
alpha = 1.5   # scegli in (1,2)
xmin = 1.0
Nlist = [10, 30, 100, 300, 1000, 3000]

rng = np.random.default_rng(seed)

Q = []
for n in Nlist:
    # Genera M somme S_n
    U = rng.uniform(0.0, 1.0, size=(M, n))
    Y = xmin * (1.0 - U) ** (-1.0 / alpha)       # inverting Pareto
    Sgn = rng.choice([-1, 1], size=(M, n))       # t have a symmetric Pareto distribution
    X = Sgn * Y
    S = X.sum(axis=1)
    Q.append(np.median(np.abs(S)))               # scala robusta

N = np.array(Nlist, dtype=float)
Q = np.array(Q)

# Fit: Q(n) ~ n^gamma, atteso gamma = 1/alpha
gamma, c = np.linalg.lstsq(
    np.vstack([np.log(N), np.ones_like(N)]).T,
    np.log(Q),
    rcond=None
)[0]

plt.figure()
plt.loglog(N, Q, marker="o", linestyle="none", label="median(|S_n|)")
plt.loglog(N, np.exp(c) * N**gamma, label=f"fit: gamma {gamma:.3f}, atteso {1/alpha:.3f}")

plt.title(r"heavy tails: scaling of the sum $S_n$ $\sim$ $n^{1/\alpha}$")
plt.xlabel(r"$n$")
plt.ylabel(r"median(|$S_n$|)")
plt.legend()
plt.show()
