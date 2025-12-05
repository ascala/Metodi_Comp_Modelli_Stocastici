import numpy as np
import matplotlib.pyplot as plt

# Definizione di alcune distribuzioni di progenie K con media m<1, m=1, m>1
# Subcritico: P(K=0)=0.6, P(K=1)=0.4  -> m = 0.4
p_sub = {0: 0.6, 1: 0.4}

# Critico: P(K=0)=0.5, P(K=2)=0.5    -> m = 1.0
p_crit = {0: 0.5, 2: 0.5}

# Supercritico: P(K=0)=0.2, P(K=2)=0.8 -> m = 1.6
p_super = {0: 0.2, 2: 0.8}

def G(s, pmf):
    """Funzione generatrice G(s) = E[s^K] per una data distribuzione pmf (dict k -> p)."""
    return sum(p * s**k for k, p in pmf.items())

# Griglia in [0,1]
s = np.linspace(0, 1, 400)

# Calcolo delle G(s) per i tre casi
G_sub   = np.array([G(x, p_sub)   for x in s])
G_crit  = np.array([G(x, p_crit)  for x in s])
G_super = np.array([G(x, p_super) for x in s])

m_sub   = sum(k * p for k, p in p_sub.items())
m_crit  = sum(k * p for k, p in p_crit.items())
m_super = sum(k * p for k, p in p_super.items())

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)

# Linea bisettrice y = s
bisettrice = s

# Subcritico
axes[0].plot(s, G_sub, label="G(s)")
axes[0].plot(s, bisettrice, linestyle="--", label="y = s")
axes[0].set_title(f"Subcritico (m = {m_sub:.1f})")
axes[0].set_xlabel("s")
axes[0].set_ylabel("G(s)")
axes[0].set_xlim(0, 1)
axes[0].set_ylim(0, 1)
axes[0].legend()

# Critico
axes[1].plot(s, G_crit, label="G(s)")
axes[1].plot(s, bisettrice, linestyle="--", label="y = s")
axes[1].set_title(f"Critico (m = {m_crit:.1f})")
axes[1].set_xlabel("s")
axes[1].set_xlim(0, 1)
axes[1].set_ylim(0, 1)

# Supercritico
axes[2].plot(s, G_super, label="G(s)")
axes[2].plot(s, bisettrice, linestyle="--", label="y = s")
axes[2].set_title(f"Supercritico (m = {m_super:.1f})")
axes[2].set_xlabel("s")
axes[2].set_xlim(0, 1)
axes[2].set_ylim(0, 1)

plt.tight_layout()
plt.show()
