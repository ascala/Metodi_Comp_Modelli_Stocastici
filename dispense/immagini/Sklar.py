import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon

np.random.seed(0)

# ------------------------------------------------------------
# 1. generiamo una dipendenza gaussiana
# ------------------------------------------------------------

N = 2000
rho = 0.7

Sigma = np.array([[1, rho],
                  [rho, 1]])

L = np.linalg.cholesky(Sigma)

Z = np.random.randn(2, N)
Xg = (L @ Z).T

# ------------------------------------------------------------
# 2. trasformiamo in uniformi (copula gaussiana)
# ------------------------------------------------------------

U = norm.cdf(Xg)

# ------------------------------------------------------------
# 3. cambiamo marginali
# ------------------------------------------------------------

X1 = expon.ppf(U[:,0])
X2 = norm.ppf(U[:,1])

# ------------------------------------------------------------
# plot
# ------------------------------------------------------------

fig, ax = plt.subplots(1,3, figsize=(12,4))

# dati gaussiani
ax[0].scatter(Xg[:,0], Xg[:,1], s=5, alpha=0.5)
ax[0].set_title("Gaussiana correlata")

# copula
ax[1].scatter(U[:,0], U[:,1], s=5, alpha=0.5)
ax[1].set_title("Copula (U1,U2)")

# nuove marginali
ax[2].scatter(X1, X2, s=5, alpha=0.5)
ax[2].set_title("Marginali arbitrarie")

for a in ax:
    a.set_aspect("equal")

plt.tight_layout()
plt.savefig("copula_transformation.png", dpi=220)
plt.show()