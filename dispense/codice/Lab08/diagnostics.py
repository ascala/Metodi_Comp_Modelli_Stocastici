"""
Grafici diagnostici per LAB08.
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from likelihoods import loglik_exponential_rate
from fit_models import smm_objective_sir


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def plot_poisson_loglik(s, lambda_hat, output_path, lam_min=0.2, lam_max=6.0):
    grid = np.linspace(lam_min, lam_max, 400)
    values = np.array([loglik_exponential_rate(lam, s) for lam in grid])

    plt.figure()
    plt.plot(grid, values)
    plt.axvline(lambda_hat, linestyle=":", label="MLE")
    plt.xlabel(r"$\lambda$")
    plt.ylabel(r"$\ell(\lambda)$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_ou_trajectory(t, x, output_path):
    plt.figure()
    plt.plot(t, x, lw=1)
    plt.xlabel("t")
    plt.ylabel("x(t)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def plot_sir_objective_grid(obs_stats, N, I0, R0, T_max,
                            beta_grid, gamma_grid, output_path,
                            n_sim=10):
    scale = np.maximum(np.abs(obs_stats), 1.0)
    Z = np.zeros((len(gamma_grid), len(beta_grid)))

    for i, gam in enumerate(gamma_grid):
        for j, bet in enumerate(beta_grid):
            Z[i, j] = smm_objective_sir(
                [bet, gam],
                obs_stats,
                N,
                I0,
                R0,
                T_max,
                n_sim=n_sim,
                scale=scale,
                seed=1000 + 100*i + j,
            )

    plt.figure()
    plt.imshow(
        Z,
        origin="lower",
        extent=[beta_grid[0], beta_grid[-1], gamma_grid[0], gamma_grid[-1]],
        aspect="auto"
    )
    plt.colorbar(label="obiettivo SMM")
    plt.xlabel(r"$\beta$")
    plt.ylabel(r"$\gamma$")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return Z


def plot_sir_stats_hist(stats, obs_stats, output_dir):
    labels = ["R_finale", "picco_I", "tempo_picco"]

    ensure_dir(output_dir)

    for k, label in enumerate(labels):
        plt.figure()
        plt.hist(stats[:, k], bins=25, alpha=0.75)
        plt.axvline(obs_stats[k], linestyle="--", label="osservato")
        plt.xlabel(label)
        plt.ylabel("frequenza")
        plt.legend()
        plt.tight_layout()
        plt.savefig(Path(output_dir) / f"sir_check_{label}.png", dpi=150)
        plt.close()
