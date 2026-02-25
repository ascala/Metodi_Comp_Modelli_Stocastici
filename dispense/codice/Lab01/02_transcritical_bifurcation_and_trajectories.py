# 02_transcritical_bifurcation_and_trajectories.py
import numpy as np
import matplotlib.pyplot as plt

# Parameters
r_min = -1.0
r_max = 1.0
Nr = 401

eps = 0.2
r_before = -eps
r_after = +eps

delta = 0.05
dt = 0.01
T = 8.0

# Model: dN/dt = r N - N^2
def f(N, r):
    return r * N - N * N

def fprime_at(Nstar, r):
    return r - 2.0 * Nstar

def euler_trajectory(x0, r, dt, T):
    nsteps = int(T / dt)
    t = dt * np.arange(nsteps + 1, dtype=float)
    x = np.zeros(nsteps + 1, dtype=float)
    x[0] = x0
    for n in range(nsteps):
        x[n + 1] = x[n] + dt * f(x[n], r)
    return t, x

# --- Critical points map (analytic): N* = 0, N* = r
r_list = np.linspace(r_min, r_max, Nr)

r_st, N_st = [], []
r_un, N_un = [], []
r_mg, N_mg = [], []

for r in r_list:
    crit = [0.0, r]
    for Nstar in crit:
        fp = fprime_at(Nstar, r)
        if fp < 0.0:
            r_st.append(r); N_st.append(Nstar)
        elif fp > 0.0:
            r_un.append(r); N_un.append(Nstar)
        else:
            r_mg.append(r); N_mg.append(Nstar)

r_st = np.array(r_st); N_st = np.array(N_st)
r_un = np.array(r_un); N_un = np.array(N_un)
r_mg = np.array(r_mg); N_mg = np.array(N_mg)

# --- Trajectories near critical points, before/after
IC_before = [0.0 + delta, 0.0 - delta, r_before + delta, r_before - delta]
IC_after = [0.0 + delta, 0.0 - delta, r_after + delta, r_after - delta]

fig, ax = plt.subplots(1, 2, figsize=(12, 4))

# Left panel: bifurcation diagram (critical points vs r)
ax[0].plot(r_st, N_st, marker="o", linestyle="none", label="stable")
ax[0].plot(r_un, N_un, marker="o", linestyle="none", markerfacecolor="none", label="unstable")
if len(r_mg) > 0:
    ax[0].plot(r_mg, N_mg, marker="x", linestyle="none", label="marginal")

ax[0].axvline(r_before, linestyle="--", linewidth=1.5, label=r"$r_{\mathrm{before}}$")
ax[0].axvline(r_after, linestyle="--", linewidth=1.5, label=r"$r_{\mathrm{after}}$")

ax[0].set_title(r"critical points: $f(N;r)=0$")
ax[0].set_xlabel(r"$r$")
ax[0].set_ylabel(r"$N^*(r)$")
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

ax[1].set_title(r"trajectories near equilibria (Euler)")
ax[1].set_xlabel(r"$t$")
ax[1].set_ylabel(r"$N(t)$")
ax[1].legend()

fig.suptitle(r"Transcritical bifurcation: $\dot N = rN - N^2$")
plt.tight_layout()
plt.show()
