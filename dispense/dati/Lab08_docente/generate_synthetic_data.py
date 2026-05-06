"""
generate_synthetic_data.py

Script docente per generare i dati sintetici del LAB08.

Questo file NON va distribuito agli studenti se si vuole che i parametri veri
rimangano nascosti.

Esecuzione:

    python generate_synthetic_data.py

Produce la cartella data/ con:

- poisson_interarrivals.csv
- jump_process.csv
- jump_process_metadata.csv
- ou_process.csv
- ou_metadata.csv
- sir_observed_stats.csv
- sir_metadata.csv
- soluzioni_parametri.csv
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd


OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------
# Parte A -- Tempi di interarrivo di un processo di Poisson
# ---------------------------------------------------------------------

def generate_poisson_interarrivals(
    lambda_true=2.5,
    n=300,
    seed=20260506,
    output_dir=OUTPUT_DIR,
):
    rng = np.random.default_rng(seed)
    inter_arrivals = rng.exponential(scale=1/lambda_true, size=n)

    pd.DataFrame({"s": inter_arrivals}).to_csv(
        output_dir / "poisson_interarrivals.csv",
        index=False
    )

    return {
        "dataset": "poisson_interarrivals",
        "lambda_true": lambda_true,
        "n": n,
        "seed": seed,
    }


# ---------------------------------------------------------------------
# Parte B -- Processo di salto a due stati
# ---------------------------------------------------------------------

def simulate_two_state(alpha, beta, T, x0=1, seed=123):
    rng = np.random.default_rng(seed)

    t = 0.0
    x = x0
    jumps = []

    while t < T:
        if x == 1:
            rate = alpha
            new_x = 2
        elif x == 2:
            rate = beta
            new_x = 1
        else:
            raise ValueError("Lo stato iniziale deve essere 1 oppure 2.")

        tau = rng.exponential(scale=1/rate)

        if t + tau > T:
            break

        t = t + tau
        jumps.append((t, x, new_x))
        x = new_x

    return jumps


def generate_jump_process(
    alpha_true=1.2,
    beta_true=0.7,
    T=100.0,
    x0=1,
    seed=202,
    output_dir=OUTPUT_DIR,
):
    jumps = simulate_two_state(alpha_true, beta_true, T, x0=x0, seed=seed)

    pd.DataFrame(jumps, columns=["time", "from_state", "to_state"]).to_csv(
        output_dir / "jump_process.csv",
        index=False
    )

    pd.DataFrame({"T": [T], "x0": [x0]}).to_csv(
        output_dir / "jump_process_metadata.csv",
        index=False
    )

    return {
        "dataset": "jump_process",
        "alpha_true": alpha_true,
        "beta_true": beta_true,
        "T": T,
        "x0": x0,
        "seed": seed,
    }


# ---------------------------------------------------------------------
# Parte C -- Ornstein--Uhlenbeck
# ---------------------------------------------------------------------

def simulate_ou(gamma, mu, sigma, x0, dt, T, seed=123):
    rng = np.random.default_rng(seed)

    n_steps = int(round(T/dt))
    x = np.empty(n_steps + 1)
    x[0] = x0

    for k in range(n_steps):
        dW = rng.normal(0.0, math.sqrt(dt))
        x[k+1] = x[k] - gamma*(x[k]-mu)*dt + sigma*dW

    t = np.linspace(0.0, T, n_steps + 1)
    return t, x


def generate_ou_process(
    gamma_true=1.5,
    mu_true=2.0,
    sigma_true=0.8,
    x0=2.0,
    dt=0.01,
    T=50.0,
    seed=303,
    output_dir=OUTPUT_DIR,
):
    t, x = simulate_ou(
        gamma_true,
        mu_true,
        sigma_true,
        x0=x0,
        dt=dt,
        T=T,
        seed=seed,
    )

    pd.DataFrame({"t": t, "x": x}).to_csv(
        output_dir / "ou_process.csv",
        index=False
    )

    # Questi valori sono forniti agli studenti perché nel lab stimano solo gamma.
    pd.DataFrame({
        "dt": [dt],
        "mu_assumed": [mu_true],
        "sigma_assumed": [sigma_true],
    }).to_csv(
        output_dir / "ou_metadata.csv",
        index=False
    )

    return {
        "dataset": "ou_process",
        "gamma_true": gamma_true,
        "mu_true": mu_true,
        "sigma_true": sigma_true,
        "x0": x0,
        "dt": dt,
        "T": T,
        "seed": seed,
    }


# ---------------------------------------------------------------------
# Parte D -- SIR osservato parzialmente
# ---------------------------------------------------------------------

def simulate_sir_gillespie(beta, gamma, N, I0, R0, T_max, seed=None):
    rng = np.random.default_rng(seed)

    S = int(N - I0 - R0)
    I = int(I0)
    R = int(R0)
    t = 0.0

    times = [t]
    S_values = [S]
    I_values = [I]
    R_values = [R]

    while t < T_max and I > 0:
        a_inf = beta * S * I / N
        a_rec = gamma * I
        a0 = a_inf + a_rec

        if a0 <= 0:
            break

        tau = rng.exponential(scale=1/a0)

        if t + tau > T_max:
            break

        t = t + tau

        if rng.random() < a_inf / a0:
            S -= 1
            I += 1
        else:
            I -= 1
            R += 1

        times.append(t)
        S_values.append(S)
        I_values.append(I)
        R_values.append(R)

    return {
        "t": np.array(times),
        "S": np.array(S_values),
        "I": np.array(I_values),
        "R": np.array(R_values),
    }


def sir_summary_stats(traj):
    I = traj["I"]
    R = traj["R"]
    t = traj["t"]

    final_size = R[-1]
    peak_I = np.max(I)
    time_peak = t[np.argmax(I)]

    return np.array([final_size, peak_I, time_peak], dtype=float)


def generate_sir_observed_stats(
    beta_true=0.45,
    gamma_true=0.18,
    N=500,
    I0=5,
    R0=0,
    T_max=80.0,
    seed=404,
    output_dir=OUTPUT_DIR,
):
    obs_traj = simulate_sir_gillespie(
        beta_true,
        gamma_true,
        N,
        I0,
        R0,
        T_max,
        seed=seed,
    )

    obs_stats = sir_summary_stats(obs_traj)

    pd.DataFrame({
        "statistic": ["final_size_R", "peak_I", "time_peak"],
        "value": obs_stats,
    }).to_csv(
        output_dir / "sir_observed_stats.csv",
        index=False
    )

    pd.DataFrame({
        "N": [N],
        "I0": [I0],
        "R0": [R0],
        "T_max": [T_max],
    }).to_csv(
        output_dir / "sir_metadata.csv",
        index=False
    )

    # Utile al docente: traiettoria completa che ha generato le statistiche.
    pd.DataFrame({
        "t": obs_traj["t"],
        "S": obs_traj["S"],
        "I": obs_traj["I"],
        "R": obs_traj["R"],
    }).to_csv(
        output_dir / "sir_hidden_full_trajectory_teacher_only.csv",
        index=False
    )

    return {
        "dataset": "sir_observed_stats",
        "beta_true": beta_true,
        "gamma_true": gamma_true,
        "N": N,
        "I0": I0,
        "R0": R0,
        "T_max": T_max,
        "seed": seed,
        "final_size_R": obs_stats[0],
        "peak_I": obs_stats[1],
        "time_peak": obs_stats[2],
    }


# ---------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------

def main():
    records = []

    records.append(generate_poisson_interarrivals())
    records.append(generate_jump_process())
    records.append(generate_ou_process())
    records.append(generate_sir_observed_stats())

    # Tabella lunga, più leggibile per il docente.
    rows = []
    for rec in records:
        dataset = rec.pop("dataset")
        for key, value in rec.items():
            rows.append({
                "dataset": dataset,
                "quantity": key,
                "value": value,
            })

    pd.DataFrame(rows).to_csv(
        OUTPUT_DIR / "soluzioni_parametri.csv",
        index=False
    )

    print("Dati generati in:", OUTPUT_DIR.resolve())
    print("File soluzioni:", (OUTPUT_DIR / "soluzioni_parametri.csv").resolve())


if __name__ == "__main__":
    main()
