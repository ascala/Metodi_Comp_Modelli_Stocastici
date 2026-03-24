import numpy as np
import matplotlib.pyplot as plt

# intervallo per m
m = np.linspace(-1.2, 1.2, 800)

# tre casi didattici
cases = [
    {"beta": 0.8, "J": 1.0, "h": 0.0, "title": r"$\beta J < 1,\ h=0$"},
    {"beta": 1.5, "J": 1.0, "h": 0.0, "title": r"$\beta J > 1,\ h=0$"},
    {"beta": 1.5, "J": 1.0, "h": 0.2, "title": r"$\beta J > 1,\ h\neq 0$"},
]

fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharex=True, sharey=True)

for ax, case in zip(axes, cases):
    beta = case["beta"]
    J = case["J"]
    h = case["h"]

    y_line = m
    y_tanh = np.tanh(beta * (J * m + h))

    ax.plot(m, y_line, label=r"$y=m$")
    ax.plot(m, y_tanh, label=r"$y=\tanh(\beta(Jm+h))$")
    ax.axhline(0.0, linewidth=0.8)
    ax.axvline(0.0, linewidth=0.8)

    ax.set_title(case["title"])
    ax.set_xlabel(r"$m$")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)

axes[0].set_ylabel(r"$y$")
axes[0].legend(loc="lower right")
fig.suptitle("Equazione di autoconsistenza: intersezioni tra retta e tangente iperbolica")
plt.tight_layout()
plt.show()
