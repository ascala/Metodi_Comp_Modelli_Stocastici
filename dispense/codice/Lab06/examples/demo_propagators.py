"""
Demo di confronto tra tre propagatori:
- Euler esplicito
- operator splitting
- full propagator
"""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

THIS_DIR = Path(__file__).resolve().parent
SNIPPETS_DIR = THIS_DIR.parent / "snippets"
sys.path.insert(0, str(SNIPPETS_DIR))

from build_generator_dense import build_generator_dense
from build_generator_sparse import build_generator_sparse
from split_generator import split_generator
from euler_propagator import propagate_euler
from splitting_propagator import propagate_splitting
from full_propagator import propagate_full

def main():
    N = 60
    r = 1.2
    ell = 0.8
    dt = 0.05
    n_steps = 40

    p0 = np.zeros(N + 1)
    p0[N // 2] = 1.0

    L_dense = build_generator_dense(N=N, r=r, ell=ell)
    L_sparse = build_generator_sparse(N=N, r=r, ell=ell)
    L_drift, L_diff = split_generator(N=N, r=r, ell=ell)

    out_full = propagate_full(L_sparse, p0, dt=dt, n_steps=n_steps)
    out_euler = propagate_euler(L_dense, p0, dt=dt, n_steps=n_steps)
    out_split = propagate_splitting(L_drift, L_diff, p0, dt=dt, n_steps=n_steps, strang=True)

    times = dt * np.arange(n_steps + 1)
    err_euler = np.sum(np.abs(out_euler - out_full), axis=1)
    err_split = np.sum(np.abs(out_split - out_full), axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    x = np.arange(N + 1)
    axes[0].plot(x, out_full[-1], label="full propagator")
    axes[0].plot(x, out_split[-1], linestyle="--", label="splitting")
    axes[0].plot(x, out_euler[-1], linestyle=":", label="Euler")
    axes[0].set_title("Distribuzione finale")
    axes[0].set_xlabel("sito")
    axes[0].set_ylabel("probabilità")
    axes[0].legend()

    axes[1].plot(times, err_euler, label="||Euler - full||_1")
    axes[1].plot(times, err_split, label="||splitting - full||_1")
    axes[1].set_title("Errore rispetto al propagatore completo")
    axes[1].set_xlabel("tempo")
    axes[1].set_ylabel("errore L1")
    axes[1].legend()
    fig.tight_layout()
    plt.show()

    print("Check dense vs sparse:", np.max(np.abs(L_dense - L_sparse.toarray())))
    print("Check split reconstruction:", np.max(np.abs((L_drift + L_diff).toarray() - L_sparse.toarray())))
    print("Normalizzazione finale full     :", out_full[-1].sum())
    print("Normalizzazione finale splitting :", out_split[-1].sum())
    print("Normalizzazione finale Euler    :", out_euler[-1].sum())
    print("Minimo componente finale Euler  :", out_euler[-1].min())

if __name__ == "__main__":
    main()
