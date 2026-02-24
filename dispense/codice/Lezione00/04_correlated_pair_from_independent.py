import numpy as np
import matplotlib.pyplot as plt

seed = 1234
M = 50000
rho = 0.8  # target correlation in (-1,1)

rng = np.random.default_rng(seed)

Z1 = rng.normal(0.0, 1.0, size=M)
Z2 = rng.normal(0.0, 1.0, size=M)

X = Z1
Y = rho * Z1 + np.sqrt(1.0 - rho**2) * Z2

# Estimated correlation
corr_hat = np.corrcoef(X, Y)[0, 1]
print(r"target $\rho$ =", rho)
print(r"estimated $\rho$ =", corr_hat)

plt.figure()
plt.scatter(X, Y, s=3, alpha=0.2)
plt.title(fr"Correlation: $\rho$ ≈ {corr_hat:.3f}")
plt.xlabel("X")
plt.ylabel("Y")
plt.axis("equal")
plt.show()
