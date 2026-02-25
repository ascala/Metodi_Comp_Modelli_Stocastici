# 03_saddle_node_bifurcation_and_tipping.py
import numpy as np
import matplotlib.pyplot as plt

# Parameters
r_min = -1.0
r_max = 0.6
Nr = 401

eps = 0.2
r_before = -eps
r_after = +eps

delta = 0.05
dt = 0.01
T = 4.0

# Model: dx/dt = r + x^2
def f(x, r):
    return r + x * x

def euler_trajectory(x0, r, dt, T):
    nsteps = int(T / dt)
    t = dt * np.arange(nsteps + 1, dtype=float)
    x = np.zeros(nsteps + 1, dtype=float)
    x[0] = x0
    for n in range(nsteps):
        x[n + 1] = x[n] + dt * f(x[n], r)
    return t, x

# --- Critical points map (analytic)
r_list = np.linspace(r_min, r_max, Nr)

r_st, x_st = [], []
r_un, x_un = [], []
r_mg, x_mg = [], []

for r in r_list:
    if r < 0.0:
        a = np.sqrt(-r)
        crit = [-a, +a]
        for xstar in crit:
            fp = 2.0 * xstar
            if fp < 0.0:
                r_st.append(r); x_st.append(xstar)
            elif fp > 0.0:
                r_un.append(r); x_un.append(xstar)
            else:
                r_mg.append(r); x_mg.append(xstar)
    elif r == 0.0:
        # marginal double root
        r_mg.append(r); x_mg.append(0.0)
    else:
        # no real equilibria
        pass

r_st = np.array(r_st); x_st = np.array(x_st)
r_un = np.array(r_un); x_un = np.array(x_un)
r_mg = np.array(r_mg); x_mg = np.array(x_mg)

# --- Trajectories before/after
a_before = np.sqrt(-r_before)
x_stable_before = -a_before
x_unstable_before = +a_before

IC_before = [
    x_stable_before + delta, x_stable_before - delta,
    x_unstable_before + delta, x_unstable_before - delta
]

# after: no equilibrium; start near where the stable branch was just before
IC_after = [x_stable_before + delta, x_stable_before - delta]

fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# Left panel: bifurcation diagram
ax[0].plot(r_st, x_st, marker="o", linestyle="none", label="stable")
ax[0].plot(r_un, x_un, marker="o", linestyle="none", markerfacecolor="none", label="unstable")
if len(r_mg) > 0:
    ax[0].plot(r_mg, x_mg, marker="x", linestyle="none", label="marginal")

ax[0].axvline(r_before, linestyle="--", linewidth=1.5, label=r"$r_{\mathrm{before}}$")
ax[0].axvline(r_after, linestyle="--", linewidth=1.5, label=r"$r_{\mathrm{after}}$")

ax[0].set_title(r"critical points: $f(x;r)=0$")
ax[0].set_xlabel(r"$r$")
ax[0].set_ylabel(r"$x^*(r)$")
ax[0].legend()

# Right panel: trajectories
first = True
for x0 in IC_before:
    t, x = euler_trajectory(x0, r_before, dt, T)
    lab = fr"before $r={r_before:g}$" if first else None
    ax[1].plot(t, x, linestyle="-", alpha=0.8, label=lab)
    first = False

first = True
for x0 in IC_after:
    t, x = euler_trajectory(x0, r_after, dt, T)
    lab = fr"after $r={r_after:g}$" if first else None
    ax[1].plot(t, x, linestyle="--", alpha=0.8, label=lab)
    first = False

ax[1].set_title(r"tipping: trajectories before/after (Euler)")
ax[1].set_xlabel(r"$t$")
ax[1].set_ylabel(r"$x(t)$")
ax[1].legend()

fig.suptitle(r"Saddle--node bifurcation: $\dot x = r + x^2$")
plt.tight_layout()
plt.show()
