import numpy as np
import matplotlib.pyplot as plt

# dominio
s = np.linspace(0, 1, 500)

# Caso 1: subcritico
# P(K=0)=0.7, P(K=1)=0.3
def G_sub(x):
    return 0.7 + 0.3*x

m_sub = 0.3

# Caso 2: supercritico
# P(K=0)=0.3, P(K=2)=0.8  --> attenzione: somma=1.1 sarebbe sbagliata
# Usiamo invece P(K=0)=0.2, P(K=2)=0.8
# Allora G(s)=0.2+0.8 s^2 e m=1.6
def G_sup(x):
    return 0.2 + 0.8*x**2

m_sup = 1.6

# punto fisso q<1 nel caso supercritico:
# q = 0.2 + 0.8 q^2  ->  0.8 q^2 - q + 0.2 = 0
# le soluzioni sono q=1 e q=0.25
q_sup = 0.25

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# ---- pannello sinistro ----
ax = axes[0]
ax.plot(s, G_sub(s), label=r"$G(s)$")
ax.plot(s, s, "--", label=r"$y=s$")
ax.scatter([1], [1], zorder=5)
ax.text(1.0, 1.0, "  (1,1)", va="bottom")
ax.set_title(r"Subcritico: $m=G'(1)=0.3 \leq 1$")
ax.set_xlabel(r"$s$")
ax.set_ylabel(r"$y$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3)
ax.legend()

# ---- pannello destro ----
ax = axes[1]
ax.plot(s, G_sup(s), label=r"$G(s)$")
ax.plot(s, s, "--", label=r"$y=s$")
ax.scatter([q_sup, 1], [q_sup, 1], zorder=5)
ax.text(q_sup, q_sup, r"  $q$", va="bottom")
ax.text(1.0, 1.0, "  (1,1)", va="bottom")
ax.set_title(r"Supercritico: $m=G'(1)=1.6 > 1$")
ax.set_xlabel(r"$s$")
ax.set_ylabel(r"$y$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.savefig("branching_fixed_points.png", dpi=200, bbox_inches="tight")
plt.show()
