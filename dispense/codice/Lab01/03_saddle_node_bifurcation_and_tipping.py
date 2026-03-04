import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters
r = 0.2
x0 = -0.45
T = 8.0
dt = 0.05
xmax = 50.0   # stop when |x| exceeds this (both exact and Euler)

# Model
def f(x, r):
    return r + x*x

# Euler with stop
def euler_trajectory(x0, r, dt, T, xmax):
    nsteps = int(T / dt)
    t = dt * np.arange(nsteps + 1, dtype=float)
    x = np.zeros(nsteps + 1, dtype=float)
    x[0] = x0
    stop = nsteps
    for n in range(nsteps):
        x[n + 1] = x[n] + dt * f(x[n], r)
        if (not np.isfinite(x[n + 1])) or (abs(x[n + 1]) > xmax):
            stop = n + 1
            break
    return t[:stop + 1], x[:stop + 1]

# Exact solution
def exact_solution(t, x0, r):
    if abs(r) < 1e-14:
        return x0 / (1.0 - x0 * t)  # dx/dt = x^2
    if r > 0.0:
        a = np.sqrt(r)
        return a * np.tan(a * t + np.arctan(x0 / a))
    a = np.sqrt(-r)
    y0 = (x0 - a) / (x0 + a)
    y = y0 * np.exp(2.0 * a * t)
    return a * (1.0 + y) / (1.0 - y)

# Optional: exact blow-up time for r>0 (to show tipping clearly)
def blowup_time(x0, r):
    if r <= 0.0:
        return None
    a = np.sqrt(r)
    return (0.5*np.pi - np.arctan(x0 / a)) / a

# Compute Euler
t_eu, x_eu = euler_trajectory(x0, r, dt, T, xmax)

# Compute exact on a fine grid up to the same stop time, then stop when it exceeds xmax
t_stop = min(T, t_eu[-1])
t_ex_full = np.linspace(0.0, t_stop, 4000)
x_ex_full = exact_solution(t_ex_full, x0, r)

mask = np.isfinite(x_ex_full) & (np.abs(x_ex_full) <= xmax)
if np.any(~mask):
    last = np.argmax(~mask)  # first index where it fails
    t_ex = t_ex_full[:last]
    x_ex = x_ex_full[:last]
else:
    t_ex, x_ex = t_ex_full, x_ex_full

# Plot
plt.figure(figsize=(7.2, 4.2))
plt.plot(t_ex, x_ex, linewidth=2.0, linestyle="--", label="exact")
plt.plot(t_eu, x_eu, linestyle="none", marker="o", markersize=3.0,
         label=f"Euler (dt={dt:g})")

tb = blowup_time(x0, r)
if tb is not None and tb <= T:
    plt.axvline(tb, linestyle=":", linewidth=1.5, label=f"blow-up time ~ {tb:.3f}")

plt.title(rf"$\dot x = r + x^2$   with   $r={r:g}$,  $x(0)={x0:g}$")
plt.xlabel("t")
plt.ylabel("x(t)")
plt.ylim(-1.0, xmax)  # keep scale readable for the lab
plt.grid(True, alpha=0.25)
plt.legend()
plt.tight_layout()
plt.show()