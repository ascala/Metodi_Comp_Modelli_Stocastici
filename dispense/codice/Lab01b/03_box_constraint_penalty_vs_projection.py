# 03_box_constraint_penalty_vs_projection.py
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    # Unconstrained minimiser at x=3
    return (x - 3.0)**2

def df(x):
    return 2.0*(x - 3.0)

def penalty_objective(x, a, b, mu):
    # Penalise violation of box [a,b]
    v = 0.0
    if x < a:
        v = a - x
    elif x > b:
        v = x - b
    return f(x) + mu*(v**2)

def d_penalty(x, a, b, mu):
    # Subgradient-like derivative: smooth inside, linear penalty outside.
    g = df(x)
    if x < a:
        g += -2.0*mu*(a - x)   # derivative of mu*(a-x)^2
    elif x > b:
        g +=  2.0*mu*(x - b)   # derivative of mu*(x-b)^2
    return g

def clip(x, a, b):
    return min(max(x, a), b)

def gd_penalty(x0, a, b, mu, alpha=0.05, nmax=2000, gtol=1e-12):
    x = float(x0)
    xs = [x]
    for n in range(nmax):
        g = d_penalty(x, a, b, mu)
        if abs(g) < gtol:
            return x, True, n+1, xs
        x = x - alpha*g
        xs.append(x)
        if abs(x) > 1e6:
            return x, False, n+1, xs
    return x, False, nmax, xs

def projected_gd(x0, a, b, alpha=0.1, nmax=2000, gtol=1e-12):
    x = clip(float(x0), a, b)
    xs = [x]
    for n in range(nmax):
        g = df(x)
        # Note: at the constrained optimum on the boundary, g need not be zero.
        x_new = clip(x - alpha*g, a, b)
        xs.append(x_new)
        if abs(x_new - x) < gtol:
            return x_new, True, n+1, xs
        x = x_new
    return x, False, nmax, xs

# --- Problem setup
a, b = 0.0, 2.0   # box constraint, true constrained optimum is x*=2
x0 = 1.5

# --- Run penalty and projection
mu = 50.0
x_pen, ok_pen, it_pen, xs_pen = gd_penalty(x0, a, b, mu)
x_proj, ok_proj, it_proj, xs_proj = projected_gd(x0, a, b)

print("Box-constrained minimisation:")
print("  box =", (a, b))
print("  unconstrained optimum = 3.0  (outside the box)")
print("  constrained optimum   = 2.0  (on the boundary)")

print("\nPenalty method:")
print("  mu =", mu)
print("  ok =", ok_pen)
print("  it =", it_pen)
print("  x  =", x_pen)
print("  f(x) =", f(x_pen))
print("  penalised objective =", penalty_objective(x_pen, a, b, mu))

print("\nProjected gradient:")
print("  ok =", ok_proj)
print("  it =", it_proj)
print("  x  =", x_proj)
print("  f(x) =", f(x_proj))

# --- Plot objective and iterates
grid = np.linspace(-0.5, 3.5, 800)
plt.figure()
plt.plot(grid, [f(x) for x in grid])
plt.axvline(a)
plt.axvline(b)
plt.scatter(xs_pen[::20], [f(x) for x in xs_pen[::20]], marker="o", label="Penalty iterates (every 20)")
plt.scatter(xs_proj[::5], [f(x) for x in xs_proj[::5]], marker="x", label="Projected iterates (every 5)")
plt.legend()
plt.title("Box constraint: penalty vs projection")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()

