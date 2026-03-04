import numpy as np
import matplotlib.pyplot as plt

# Choose r and initial condition
r = 0.2            # try -0.2, 0.0, +0.2
N0 = 0.05          # initial condition
T = 8.0
dt = 0.05          # try 0.2, 0.1, 0.05, 0.02, 0.01

# Model: dN/dt = r N - N^2
def f(N, r):
    return r * N - N * N

# Explicit Euler
def euler(N0, r, dt, T):
    nsteps = int(T / dt)
    t = dt * np.arange(nsteps + 1, dtype=float)
    N = np.zeros(nsteps + 1, dtype=float)
    N[0] = N0
    for k in range(nsteps):
        N[k + 1] = N[k] + dt * f(N[k], r)
    return t, N

# Exact solution
def exact(t, N0, r):
    if abs(r) < 1e-14:
        return N0 / (1.0 + N0 * t)  # limit r->0
    return (r * N0) / (N0 + (r - N0) * np.exp(-r * t))

# Compute trajectories
t_eu, N_eu = euler(N0, r, dt, T)
t_ex = np.linspace(0.0, T, 800)
N_ex = exact(t_ex, N0, r)

# Plot
plt.figure(figsize=(7, 4))
plt.plot(t_eu, N_eu, linestyle="none", marker=".", markersize=3, label=fr"Euler (dt={dt:g})")
plt.plot(t_ex, N_ex, linewidth=1.0, linestyle="-", label="exact")
plt.title(rf"$\dot N = rN - N^2$  with  $r={r:g}$,  $N(0)={N0:g}$")
plt.xlabel("t")
plt.ylabel("N(t)")
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()