import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Figure generator for slides on generalized inverse / quantile
# Safe for plain Python + matplotlib on Linux
# Output files:
#   slide_pmf.png
#   slide_cdf.png
#   slide_quantile_selection.png
#   slide_quantile_mapping.png
#   slide_quantile_compare.png
# ============================================================

# Example discrete distribution
x = np.array([1, 2, 3, 4], dtype=float)
p = np.array([0.2, 0.3, 0.1, 0.4], dtype=float)
F = np.cumsum(p)

# ------------------------------------------------------------
# helper: consistent save
# ------------------------------------------------------------
def savefig(name):
    plt.tight_layout()
    plt.savefig(name, dpi=220, bbox_inches="tight")
    plt.close()

# ------------------------------------------------------------
# 1. PMF
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.bar(x, p, width=0.1)
plt.xlabel("x")
plt.ylabel("P(X = x)")
plt.title("Discrete distribution (PMF)")
savefig("slide_pmf.png")

# ------------------------------------------------------------
# 2. CDF
# ------------------------------------------------------------
# for a clean step plot, prepend a point at x[0]-1 with value 0
x_step = np.concatenate(([x[0] - 1], x, [x[-1] + 1]))
F_step = np.concatenate(([0.0], F, [F[-1]]))

plt.figure(figsize=(6, 6))
plt.step(x_step, F_step, where="post")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.title("Cumulative distribution function (CDF)")
plt.xlim(-0.02, 4.32)
plt.ylim(-0.02, 1.02)
savefig("slide_cdf.png")

# ------------------------------------------------------------
# 3. Quantile selection with a chosen u
# ------------------------------------------------------------
u = 0.55
idx = np.where(F >= u)[0][0]
xq = x[idx]

plt.figure(figsize=(6, 4))
plt.step(x_step, F_step, where="post")
plt.axhline(u, linestyle="--")
plt.axvline(xq, linestyle="--")
plt.xlabel("x")
plt.ylabel("F(x)")
plt.title(r"Quantile selection: $F^{-1}(u)$")
plt.ylim(-0.02, 1.02)
savefig("slide_quantile_selection.png")

# ------------------------------------------------------------
# 4. Mapping U -> X = F^{-1}(U)
# ------------------------------------------------------------
u_vals = np.linspace(0, 1, 2000)
x_map = np.zeros_like(u_vals)

cum = np.concatenate(([0.0], F))
for i in range(len(x)):
    mask = (u_vals >= cum[i]) & (u_vals < cum[i + 1])
    x_map[mask] = x[i]

# include u = 1 exactly
x_map[u_vals == 1.0] = x[-1]

plt.figure(figsize=(6, 4))
plt.plot(u_vals, x_map)
plt.xlabel("u ~ Uniform(0,1)")
plt.ylabel(r"$X = F^{-1}(u)$")
plt.title("Mapping from uniform variable to discrete X")
savefig("slide_quantile_mapping.png")

# ------------------------------------------------------------
# 5. Continuous vs discrete quantile
# ------------------------------------------------------------
u_cont = np.linspace(0, 1, 2000)

# continuous example: Uniform(0,1), so quantile is x=u
x_cont = u_cont.copy()

x_disc = np.zeros_like(u_cont)
for i in range(len(x)):
    mask = (u_cont >= cum[i]) & (u_cont < cum[i + 1])
    x_disc[mask] = x[i]
x_disc[u_cont == 1.0] = x[-1]

plt.figure(figsize=(6, 4))
plt.plot(u_cont, x_cont, label="continuous quantile")
plt.plot(u_cont, x_disc, label="discrete quantile")
plt.xlabel("u")
plt.ylabel(r"$F^{-1}(u)$")
plt.title("Continuous vs discrete quantile function")
plt.legend()
savefig("slide_quantile_compare.png")

print("Generated files:")
print("  slide_pmf.png")
print("  slide_cdf.png")
print("  slide_quantile_selection.png")
print("  slide_quantile_mapping.png")
print("  slide_quantile_compare.png")