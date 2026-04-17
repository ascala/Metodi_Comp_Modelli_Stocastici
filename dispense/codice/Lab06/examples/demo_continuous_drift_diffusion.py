"""
Demo continua:
- simula la SDE di drift-diffusion;
- confronta istogramma finale e gaussiana teorica.
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

THIS_DIR = Path(__file__).resolve().parent
SNIPPETS_DIR = THIS_DIR.parent / "snippets"
sys.path.insert(0, str(SNIPPETS_DIR))

from drift_diffusion_sde import simulate_drift_diffusion
from gaussian_theory import gaussian_pdf, theoretical_mean, theoretical_variance

def main():
    rng = np.random.default_rng(2026)
    x0 = 0.0
    a = 1.0
    D = 1.0
    T = 2.0
    dt = 1e-3
    M = 5000

    times, X = simulate_drift_diffusion(x0=x0, a=a, D=D, T=T, dt=dt, M=M, rng=rng)
    x_final = X[:, -1]

    x_grid = np.linspace(x_final.min() - 1.0, x_final.max() + 1.0, 400)
    p_theory = gaussian_pdf(x_grid, t=times[-1], x0=x0, a=a, D=D)

    plt.figure(figsize=(6, 4))
    plt.hist(x_final, bins=50, density=True, alpha=0.7, label="simulazione")
    plt.plot(x_grid, p_theory, linewidth=2, label="teoria gaussiana")
    plt.xlabel("x")
    plt.ylabel("densità")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("Media empirica     :", x_final.mean())
    print("Media teorica      :", theoretical_mean(times[-1], x0, a))
    print("Varianza empirica  :", x_final.var(ddof=1))
    print("Varianza teorica   :", theoretical_variance(times[-1], D))

if __name__ == "__main__":
    main()
