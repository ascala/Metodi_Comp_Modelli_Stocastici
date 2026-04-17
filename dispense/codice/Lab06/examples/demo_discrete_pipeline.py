"""
Demo completa del flusso discreto:
- simula molte traiettorie del random walk continuo nel tempo;
- campiona le posizioni a tempi fissati;
- costruisce istogrammi;
- integra la master equation;
- converte i siti in coordinate fisiche;
- legge v e D dal modello discreto;
- sovrappone la gaussiana continua efficace.
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

THIS_DIR = Path(__file__).resolve().parent
SNIPPETS_DIR = THIS_DIR.parent / "snippets"
sys.path.insert(0, str(SNIPPETS_DIR))

from rw_continuous_time import simulate_ctrw
from sample_positions_at_times import sample_positions_at_times
from build_generator_dense import build_generator_dense
from integrate_master_equation import integrate_master_equation
from grid_utils import spatial_grid, site_to_x, x0_from_i0
from gaussian_theory import effective_parameters, gaussian_pdf

def main():
    rng = np.random.default_rng(12345)
    N = 80
    dx = 0.5
    i0 = N // 2
    x0 = x0_from_i0(i0, dx)
    r = 1.4
    ell = 0.8
    T = 4.0
    M = 3000
    query_times = np.array([1.0, 2.0, 4.0])

    trajectories = [simulate_ctrw(i0=i0, N=N, r=r, ell=ell, T=T, rng=rng) for _ in range(M)]
    sampled_sites = sample_positions_at_times(trajectories, query_times)
    sampled_x = site_to_x(sampled_sites, dx)

    L = build_generator_dense(N=N, r=r, ell=ell, reflecting=True)
    p0 = np.zeros(N + 1)
    p0[i0] = 1.0
    t, y = integrate_master_equation(L, p0, t_span=(0.0, T), t_eval=query_times)

    x = spatial_grid(N, dx)
    v, D = effective_parameters(r, ell, dx)

    fig, axes = plt.subplots(1, len(query_times), figsize=(4 * len(query_times), 3), squeeze=False)
    axes = axes[0]
    bin_edges = np.arange(x[0] - 0.5 * dx, x[-1] + 1.5 * dx, dx)

    for j, ax in enumerate(axes):
        ax.hist(sampled_x[:, j], bins=bin_edges, density=True, alpha=0.6, label="istogramma traiettorie")
        ax.plot(x, y[:, j] / dx, marker="o", linestyle="none", label="master equation")
        p_cont = gaussian_pdf(x, t=query_times[j], x0=x0, a=v, D=D)
        ax.plot(x, p_cont, linewidth=2, label="gaussiana efficace")
        ax.set_title(f"t = {query_times[j]:.2f}")
        ax.set_xlabel("x")
        ax.set_ylabel("densità")
        ax.legend()

    fig.tight_layout()
    plt.show()

    print("Parametri efficaci dal modello discreto:")
    print("v =", v)
    print("D =", D)

if __name__ == "__main__":
    main()
