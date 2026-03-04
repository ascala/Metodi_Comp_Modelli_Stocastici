# 02_minimi_two_basins_multistart.py
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    # Two-basin objective (non-convex): two local minima near -1 and 2.
    return (x + 1.0)**2 * (x - 2.0)**2 + 0.10*x

def df(x):
    # Analytic derivative (kept explicit to avoid numerical differentiation issues).
    # d/dx [(x+1)^2 (x-2)^2] = 2(x+1)(x-2)^2 + 2(x-2)(x+1)^2
    return 2.0*(x+1.0)*(x-2.0)**2 + 2.0*(x-2.0)*(x+1.0)**2 + 0.10

def gradient_descent(x0, alpha=0.02, nmax=5000, gtol=1e-10):
    x = float(x0)
    xs = [x]
    for n in range(nmax):
        g = df(x)
        if abs(g) < gtol:
            return x, True, n+1, xs
        x = x - alpha*g
        xs.append(x)
        # Simple divergence guard (for teaching): if x explodes, stop.
        if abs(x) > 1e6:
            return x, False, n+1, xs
    return x, False, nmax, xs

# --- Single-start
x0_single = 0.0
x_single, ok_single, it_single, xs_single = gradient_descent(x0_single)

print("Single-start gradient descent:")
print("  x0 =", x0_single)
print("  ok =", ok_single)
print("  it =", it_single)
print("  x  =", x_single)
print("  f(x) =", f(x_single))

# --- Multi-start
starts = np.linspace(-4.0, 4.0, 9)  # few starts are enough to illustrate basins
results = []

for s in starts:
    x_end, ok, it, xs = gradient_descent(s)
    results.append((s, x_end, f(x_end), ok, it))

# pick best among convergent runs
best = None
for r in results:
    if r[3]:  # ok
        if best is None or r[2] < best[2]:
            best = r

print("\nMulti-start summary:")
for s, x_end, fx, ok, it in results:
    print("  start = % .2f  ->  x = % .6f   f = % .6e   ok = %s   it = %d" % (s, x_end, fx, str(ok), it))

if best is not None:
    print("\nBest (among converged):")
    print("  start =", best[0])
    print("  x     =", best[1])
    print("  f(x)  =", best[2])

# --- Plot objective and trajectories
grid = np.linspace(-4.5, 4.5, 800)
plt.figure()
plt.plot(grid, f(grid))
plt.scatter(xs_single[::50], [f(x) for x in xs_single[::50]], marker="o", label="Single-start (every 50)")
# show endpoints for multi-start
ends_x = [r[1] for r in results]
ends_y = [r[2] for r in results]
plt.scatter(ends_x, ends_y, marker="x", label="Multi-start endpoints")
plt.legend()
plt.title("Two basins: single-start vs multi-start")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()
