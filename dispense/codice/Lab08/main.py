"""
LAB08 -- Stima dei parametri, likelihood e simulazione.

Eseguire da terminale dentro la cartella Lab08:

    python main.py

Il codice produce stampe a video e figure nella cartella output/.
"""

from pathlib import Path
import numpy as np
import pandas as pd

from fit_models import (
    mle_exponential_rate_closed,
    mle_exponential_rate_numeric,
    two_state_sufficient_statistics,
    estimate_two_state_rates,
    estimate_ou_gamma_regression,
    estimate_ou_gamma_euler,
    estimate_ou_gamma_exact,
    estimate_sir_smm,
    simulate_sir_gillespie,
    sir_summary_stats,
)
from diagnostics import (
    ensure_dir,
    plot_poisson_loglik,
    plot_ou_trajectory,
    plot_sir_objective_grid,
    plot_sir_stats_hist,
)


DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")


def run_part_a():
    print("\n=== Parte A: Poisson / esponenziale ===")
    df = pd.read_csv(DATA_DIR / "poisson_interarrivals.csv")
    s = df["s"].to_numpy()

    lam_closed = mle_exponential_rate_closed(s)
    lam_numeric, _ = mle_exponential_rate_numeric(s)

    print(f"lambda MLE chiusa   = {lam_closed:.6f}")
    print(f"lambda MLE numerica = {lam_numeric:.6f}")

    plot_poisson_loglik(s, lam_closed, OUTPUT_DIR / "poisson_loglik.png")
    print("Figura salvata: output/poisson_loglik.png")


def run_part_b():
    print("\n=== Parte B: processo di salto a due stati ===")
    jumps = pd.read_csv(DATA_DIR / "jump_process.csv")
    meta = pd.read_csv(DATA_DIR / "jump_process_metadata.csv")

    T = float(meta["T"].iloc[0])
    x0 = int(meta["x0"].iloc[0])

    N12, N21, T1, T2 = two_state_sufficient_statistics(jumps, T, x0)
    alpha_hat, beta_hat = estimate_two_state_rates(N12, N21, T1, T2)

    print(f"N12 = {N12}, N21 = {N21}")
    print(f"T1  = {T1:.6f}, T2  = {T2:.6f}")
    print(f"alpha_hat = {alpha_hat:.6f}")
    print(f"beta_hat  = {beta_hat:.6f}")

    pi1_hat = T1 / T
    pi2_hat = T2 / T
    print(f"frazione empirica stato 1 = {pi1_hat:.4f}")
    print(f"frazione empirica stato 2 = {pi2_hat:.4f}")


def run_part_c():
    print("\n=== Parte C: Ornstein--Uhlenbeck ===")
    df = pd.read_csv(DATA_DIR / "ou_process.csv")
    meta = pd.read_csv(DATA_DIR / "ou_metadata.csv")

    t = df["t"].to_numpy()
    x = df["x"].to_numpy()

    dt = float(meta["dt"].iloc[0])
    mu = float(meta["mu_assumed"].iloc[0])
    sigma = float(meta["sigma_assumed"].iloc[0])

    gamma_reg = estimate_ou_gamma_regression(x, dt, mu)
    gamma_euler, _ = estimate_ou_gamma_euler(x, dt, mu, sigma)
    gamma_exact, _ = estimate_ou_gamma_exact(x, dt, mu, sigma)

    print(f"gamma regressione = {gamma_reg:.6f}")
    print(f"gamma Euler       = {gamma_euler:.6f}")
    print(f"gamma esatto      = {gamma_exact:.6f}")

    plot_ou_trajectory(t, x, OUTPUT_DIR / "ou_trajectory.png")
    print("Figura salvata: output/ou_trajectory.png")

    # Sottocampionamento
    stride = 10
    x_sparse = x[::stride]
    dt_sparse = dt * stride

    gamma_euler_sparse, _ = estimate_ou_gamma_euler(x_sparse, dt_sparse, mu, sigma)
    gamma_exact_sparse, _ = estimate_ou_gamma_exact(x_sparse, dt_sparse, mu, sigma)

    print("\nSottocampionamento ogni 10 punti:")
    print(f"gamma Euler sparse  = {gamma_euler_sparse:.6f}")
    print(f"gamma esatto sparse = {gamma_exact_sparse:.6f}")


def run_part_d():
    print("\n=== Parte D: SIR simulation-based ===")
    stats_df = pd.read_csv(DATA_DIR / "sir_observed_stats.csv")
    meta = pd.read_csv(DATA_DIR / "sir_metadata.csv")

    obs_stats = stats_df["value"].to_numpy(dtype=float)

    N = int(meta["N"].iloc[0])
    I0 = int(meta["I0"].iloc[0])
    R0 = int(meta["R0"].iloc[0])
    T_max = float(meta["T_max"].iloc[0])

    print("Statistiche osservate:")
    print(stats_df)

    params_hat, res = estimate_sir_smm(
        obs_stats, N, I0, R0, T_max, x0=(0.35, 0.15), n_sim=20
    )

    beta_hat, gamma_hat = params_hat

    print(f"beta_hat  = {beta_hat:.6f}")
    print(f"gamma_hat = {gamma_hat:.6f}")
    print(f"obiettivo = {res.fun:.6f}")

    beta_grid = np.linspace(0.20, 0.70, 11)
    gamma_grid = np.linspace(0.08, 0.35, 11)

    plot_sir_objective_grid(
        obs_stats, N, I0, R0, T_max,
        beta_grid, gamma_grid,
        OUTPUT_DIR / "sir_smm_landscape.png",
        n_sim=10
    )
    print("Figura salvata: output/sir_smm_landscape.png")

    # Diagnostica simulando dal modello stimato
    rng = np.random.default_rng(999)
    all_stats = []
    for _ in range(200):
        seed = int(rng.integers(0, 2**32 - 1))
        traj = simulate_sir_gillespie(beta_hat, gamma_hat, N, I0, R0, T_max, seed=seed)
        all_stats.append(sir_summary_stats(traj))

    all_stats = np.asarray(all_stats)
    plot_sir_stats_hist(all_stats, obs_stats, OUTPUT_DIR)
    print("Figure diagnostiche SIR salvate in output/.")


def main():
    ensure_dir(OUTPUT_DIR)

    run_part_a()
    run_part_b()
    run_part_c()
    run_part_d()


if __name__ == "__main__":
    main()
