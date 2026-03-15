# 01_zero_newton_vs_bisection.py
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    # Example where Newton can enter a 2-cycle for a bad initial guess.
    # f(x) = x^3 - 2x + 2 has a real root in [-2, 0].
    return x**3 - 2.0*x + 2.0

def df(x):
    return 3.0*x**2 - 2.0

def newton(x0, nmax=30, atol=1e-12):
    x = float(x0)
    xs = [x]
    for n in range(nmax):
        fx = f(x)
        dfx = df(x)

        if abs(fx) < atol:
            return x, True, n+1, xs

        if abs(dfx) < 1e-14:
            # Derivative too small: likely huge step / numerical trouble.
            return x, False, n+1, xs

        x = x - fx/dfx
        xs.append(x)

    return x, False, nmax, xs

def bisection(a, b, nmax=80, atol=1e-12):
    fa = f(a)
    fb = f(b)
    if fa*fb > 0.0:
        raise ValueError("Invalid bracket: f(a) and f(b) must have opposite signs.")

    left = float(a)
    right = float(b)
    xs = []

    for n in range(nmax):
        m = 0.5*(left + right)
        fm = f(m)
        xs.append(m)

        if abs(fm) < atol or 0.5*(right-left) < atol:
            return m, True, n+1, xs

        if fa*fm < 0.0:
            right = m
            fb = fm
        else:
            left = m
            fa = fm

    return 0.5*(left + right), False, nmax, xs

# --- Run experiment
x0 = 0.0                 # Bad guess: Newton cycles 0 -> 1 -> 0 -> ...
a, b = -2.0, 0.0         # Valid bracket for bisection

xn, okn, itn, xs_newton = newton(x0)
xb, okb, itb, xs_bisect = bisection(a, b)

print("Newton:")
print("  x0 =", x0)
print("  ok =", okn)
print("  it =", itn)
print("  x  =", xn)
print("  f(x) =", f(xn))
print("  last iterates:", xs_newton[-6:])

print("\nBisection:")
print("  bracket =", (a, b))
print("  ok =", okb)
print("  it =", itb)
print("  x  =", xb)
print("  f(x) =", f(xb))

# --- Plot
grid = np.linspace(-2.2, 1.8, 600)
plt.figure()
plt.plot(grid, f(grid))
plt.axhline(0.0)
plt.scatter(xs_newton, [f(x) for x in xs_newton], marker="o", label="Newton iterates")
plt.scatter(xs_bisect[::5], [f(x) for x in xs_bisect[::5]], marker="x", label="Bisection (every 5)")
plt.legend()
plt.title("Root finding: Newton can fail without bracketing")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()
