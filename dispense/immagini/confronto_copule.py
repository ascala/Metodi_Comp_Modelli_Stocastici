import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t as student_t
from scipy.stats import kendalltau

rng = np.random.default_rng(42)
N = 5000

# --- copula gaussiana ---
rho = 0.7
cov = [[1, rho], [rho, 1]]
Z = rng.multivariate_normal([0, 0], cov, N)
u_gauss = norm.cdf(Z)

# --- copula di Student (nu=3) ---
nu = 3
Z2 = rng.multivariate_normal([0, 0], cov, N)
chi2 = rng.chisquare(nu, N) / nu
T = Z2 / np.sqrt(chi2[:, None])
u_student = student_t.cdf(T, df=nu)

# --- copula di Clayton (theta=2) ---
theta_c = 2.0
u1 = rng.uniform(0, 1, N)
v  = rng.uniform(0, 1, N)
u2_clayton = (u1**(-theta_c) * (v**(-theta_c/(theta_c+1)) - 1) + 1)**(-1/theta_c)
u_clayton = np.column_stack([u1, u2_clayton])

# --- copula di Gumbel (theta=2) ---
# via metodo Marshall-Olkin / algoritmo standard
theta_g = 2.0
# campionamento tramite variabile latente stabile
from scipy.stats import levy_stable
S = levy_stable.rvs(1/theta_g, 1, size=N,
                    random_state=rng.integers(1e9))
E1 = rng.exponential(1, N)
E2 = rng.exponential(1, N)
u_gumbel = np.column_stack([
    np.exp(-(E1/S)**(1/theta_g)),
    np.exp(-(E2/S)**(1/theta_g))
])

# --- figura ---
datasets = [
    (u_gauss,   "Gaussiana"),
    (u_student, "Student $t$ ($\\nu=3$)"),
    (u_clayton, "Clayton ($\\theta=2$)"),
    (u_gumbel,  "Gumbel ($\\theta=2$)"),
]

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

for ax, (u, title) in zip(axes.flat, datasets):
    ax.scatter(u[:, 0], u[:, 1], s=2, alpha=0.3, color="steelblue")
    ax.set_title(title, fontsize=12)
    ax.set_xlabel("$U_1$", fontsize=11)
    ax.set_ylabel("$U_2$", fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
#    ax.set_aspect("equal")
    tau, _ = kendalltau(u[:, 0], u[:, 1])
    ax.text(0.05, 0.92, f"$\\tau_K = {tau:.2f}$",
            transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7))

#fig.suptitle("Stessa dipendenza, copule diverse",
#             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("copule_confronto.png",
            dpi=150, bbox_inches="tight")
plt.show()
print("Salvato in copule_confronto.png")