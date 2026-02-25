# 01_euler_vs_exact_exponential.py
import numpy as np
import matplotlib.pyplot as plt

# Parameters
x0 = 1.0
lam = -1.0
T = 5.0
dt_list = [1.0, 0.5, 0.2, 0.1, 0.05]

# Exact solution on a fine grid (reference curve)
t_ref = np.linspace(0.0, T, 1200)
x_ref = x0 * np.exp(lam * t_ref)

plt.figure()

plt.plot(t_ref, x_ref, linewidth=2.0, label="exact")

for dt in dt_list:
    nsteps = int(T / dt)
    t = dt * np.arange(nsteps + 1, dtype=float)
    x = np.zeros(nsteps + 1, dtype=float)
    x[0] = x0

    for n in range(nsteps):
        x[n + 1] = x[n] + dt * (lam * x[n])

    err_final = abs(x[-1] - x0 * np.exp(lam * T))
    print(r"dt =", dt, r"  |x(T)-x_exact(T)| =", err_final)

    plt.plot(t, x, label=f"Euler dt={dt:g}")

plt.suptitle(r"Euler method: comparison with exact solution")
plt.title(r"ODE: $\dot x = \lambda x$, exact: $x(t)=x_0 e^{\lambda t}$")
plt.xlabel(r"$t$")
plt.ylabel(r"$x(t)$")
plt.legend()
plt.show()
