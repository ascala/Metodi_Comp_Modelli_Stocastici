import numpy as np
import matplotlib.pyplot as plt

# Parameters
seed = 1234
M = 20000
Nlist = [1, 2, 100]

rng = np.random.default_rng(seed)

# Choice: X ~ Unif(0,1)
mu = 0.5
sigma = np.sqrt(1.0 / 12.0)

plt.figure()

for n in Nlist:
    # Generate an array M x n of i.i.d. 
    X = rng.uniform(0.0, 1.0, size=(M, n))
    S = X.sum(axis=1) # sum over columns
    Z = (S - n * mu) / (sigma * np.sqrt(n))
    plt.hist(Z, bins=80, density=True, alpha=0.35, label=f"n={n}")

# Standard Gaussian as reference
xx = np.linspace(-4, 4, 600)
phi = (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * xx**2)
plt.plot(xx, phi, linewidth=2.0, label="N(0,1)")

plt.suptitle(r"Central Limit Theorem")
plt.title(r"$pdf$ of standardised sum $\to N(0,1)$")
plt.legend()
plt.show()
