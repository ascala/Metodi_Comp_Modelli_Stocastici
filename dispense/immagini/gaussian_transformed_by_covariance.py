import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Figura a due pannelli:
#  - sinistra: gaussiana standard isotropa
#  - destra  : gaussiana correlata con covarianza assegnata
# ============================================================

np.random.seed(42)

# ------------------------------------------------------------
# Parametri
# ------------------------------------------------------------
N = 1500
mu = np.array([0.0, 0.0])

# angolo di rotazione
theta = np.pi / 4.0   # 45 gradi

# autovalori desiderati (assi principali dell'ellisse)
lam1 = 4.0
lam2 = 0.5

# matrice di rotazione
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)]
])

# matrice diagonale degli autovalori
Lambda = np.diag([lam1, lam2])

# covarianza ruotata
Sigma = R @ Lambda @ R.T

# fattorizzazione di Cholesky
L = np.linalg.cholesky(Sigma)

# ------------------------------------------------------------
# Campioni
# ------------------------------------------------------------
Z = np.random.randn(2, N)              # gaussiana standard
X = (L @ Z).T + mu                     # gaussiana correlata

# ------------------------------------------------------------
# Griglia per contorni
# ------------------------------------------------------------
grid = np.linspace(-5, 5, 400)
Xg, Yg = np.meshgrid(grid, grid)

# densità gaussiana standard
std_exp = -0.5 * (Xg**2 + Yg**2)
std_pdf = np.exp(std_exp)

# densità gaussiana correlata
pos = np.stack([Xg, Yg], axis=-1)
Sigma_inv = np.linalg.inv(Sigma)
quad = np.einsum("...i,ij,...j->...", pos, Sigma_inv, pos)
corr_pdf = np.exp(-0.5 * quad)

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# ----- pannello sinistro -----
axes[0].scatter(Z[0, :], Z[1, :], s=6, alpha=0.5)
axes[0].contour(Xg, Yg, std_pdf, levels=4)
axes[0].set_title("Gaussiana standard isotropa")
axes[0].set_xlabel(r"$x_1$")
axes[0].set_ylabel(r"$x_2$")
axes[0].set_aspect("equal")
axes[0].set_xlim(-5, 5)
axes[0].set_ylim(-5, 5)

# ----- pannello destro -----
axes[1].scatter(X[:, 0], X[:, 1], s=6, alpha=0.5)
axes[1].contour(Xg, Yg, corr_pdf, levels=4)
axes[1].set_title("Gaussiana correlata")
axes[1].set_xlabel(r"$x_1$")
axes[1].set_ylabel(r"$x_2$")
axes[1].set_aspect("equal")
axes[1].set_xlim(-5, 5)
axes[1].set_ylim(-5, 5)

plt.tight_layout()
plt.savefig("gaussian_2d_covariance.png", dpi=220, bbox_inches="tight")
plt.show()