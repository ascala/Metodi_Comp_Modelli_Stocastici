import numpy as np
import matplotlib.pyplot as plt


def landscape(X, Y):
    """
    Paesaggio multimodale artificiale:
        C(x,y) = a(x^2+y^2) - sum_k A_k exp(-((x-xk)^2+(y-yk)^2)/(2 sk^2))

    Il termine quadratico confina il paesaggio.
    Le gaussiane negative creano valli locali.
    """
    a = 0.08

    wells = [
        # (A_k, x_k, y_k, s_k)
        (3.2, -2.4, -1.8, 0.75),
        (4.4,  1.7,  1.4, 0.65),  # valle più profonda: minimo globale circa
        (2.8, -1.2,  2.0, 0.55),
        (2.4,  2.5, -1.6, 0.85),
        (1.8,  0.0, -0.2, 1.10),
    ]

    C = a * (X**2 + Y**2)

    for A, x0, y0, s in wells:
        C -= A * np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * s**2))

    return C


def grad_landscape(x, y, eps=1e-4):
    """
    Gradiente numerico centrale di C(x,y).
    Utile per mantenere il codice semplice e modificabile.
    """
    cx1 = landscape(x + eps, y)
    cx0 = landscape(x - eps, y)
    cy1 = landscape(x, y + eps)
    cy0 = landscape(x, y - eps)

    dCdx = (cx1 - cx0) / (2 * eps)
    dCdy = (cy1 - cy0) / (2 * eps)

    return np.array([dCdx, dCdy])


def greedy_descent(x0, y0, eta=0.06, n_steps=350, tol=1e-5):
    """
    Discesa greedy / hill climbing in versione continua:
    segue la direzione -grad C.

    Serve come analogia visuale di una ricerca locale:
    scende verso la valle più vicina e può fermarsi in un minimo locale.
    """
    path = [(x0, y0)]
    x, y = x0, y0

    for _ in range(n_steps):
        g = grad_landscape(x, y)
        norm_g = np.linalg.norm(g)

        if norm_g < tol:
            break

        x_new = x - eta * g[0]
        y_new = y - eta * g[1]

        # evita che la traiettoria esca troppo dal dominio visualizzato
        if not (-4 <= x_new <= 4 and -4 <= y_new <= 4):
            break

        x, y = x_new, y_new
        path.append((x, y))

    return np.array(path)


# -----------------------------
# Griglia per il paesaggio
# -----------------------------
xmin, xmax = -4, 4
ymin, ymax = -4, 4
n_grid = 350

x = np.linspace(xmin, xmax, n_grid)
y = np.linspace(ymin, ymax, n_grid)
X, Y = np.meshgrid(x, y)
C = landscape(X, Y)

# Punto di minimo globale numerico sulla griglia
idx_min = np.unravel_index(np.argmin(C), C.shape)
x_min = X[idx_min]
y_min = Y[idx_min]

# Condizioni iniziali per traiettorie greedy
initial_points = [
    (-3.5, -3.2),
    (-3.2,  2.8),
    ( 3.2,  3.0),
    ( 3.5, -3.0),
    ( 0.0,  3.5),
    ( 0.5, -3.5),
]

paths = [greedy_descent(x0, y0) for x0, y0 in initial_points]

# -----------------------------
# Figura
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)

# Pannello A: paesaggio
ax = axes[0]
levels = 35
cf = ax.contourf(X, Y, C, levels=levels)
cs = ax.contour(X, Y, C, levels=levels, linewidths=0.4)

ax.plot(x_min, y_min, marker="*", markersize=14, label="minimo globale su griglia")
ax.set_title("Paesaggio multimodale")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_aspect("equal")
ax.legend(loc="upper right")

cbar = fig.colorbar(cf, ax=ax)
cbar.set_label("$C(x,y)$")

# Pannello B: traiettorie greedy
ax = axes[1]
cf2 = ax.contourf(X, Y, C, levels=levels)
ax.contour(X, Y, C, levels=levels, linewidths=0.4)

for path in paths:
    ax.plot(path[:, 0], path[:, 1], linewidth=2)
    ax.plot(path[0, 0], path[0, 1], marker="o", markersize=5)
    ax.plot(path[-1, 0], path[-1, 1], marker="x", markersize=7)

ax.plot(x_min, y_min, marker="*", markersize=14, label="minimo globale su griglia")
ax.set_title("Traiettorie greedy da condizioni iniziali diverse")
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_aspect("equal")
ax.legend(loc="upper right")

cbar2 = fig.colorbar(cf2, ax=ax)
cbar2.set_label("$C(x,y)$")

plt.savefig("fig10_multimodal_landscape.png", dpi=300, bbox_inches="tight")
plt.show()