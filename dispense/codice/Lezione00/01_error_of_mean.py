import numpy as np
import matplotlib.pyplot as plt

seed = 1234
M = 20000
Nlist = [10, 20, 50, 100, 200, 500, 1000]

rng = np.random.default_rng(seed)

# X ~ Unif(0,1)
sigma = np.sqrt(1.0 / 12.0)

errs = []
for n in Nlist:
    X = rng.uniform(0.0, 1.0, size=(M, n))
    m = X.mean(axis=1)
    errs.append(m.std())

N = np.array(Nlist, dtype=float)
errs = np.array(errs)

# Fit pendenza su log-log
slope, intercept = np.linalg.lstsq(
    np.vstack([np.log(N), np.ones_like(N)]).T,
    np.log(errs),
    rcond=None
)[0]

plt.figure()
plt.loglog(N, errs, marker="o", linestyle="none", label=r"std(mean) estimated")

# Linea di riferimento ~ n^{-1/2}
ref = np.exp(intercept) * N**slope
plt.loglog(N, ref, label=f"fit: pendenza {slope:.3f}")

plt.title(r"Error of mean: std( $X̄_n$ ) $\sim$ $n^{-1/2}$")
plt.xlabel(r"n")
plt.ylabel(r"std( X̄_n )")
plt.legend()
plt.show()
