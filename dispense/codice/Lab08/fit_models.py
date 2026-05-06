"""
Funzioni di stima per LAB08.

Le funzioni principali sono utilizzate da main.py.
Alcune parti possono essere modificate dagli studenti.
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize

from likelihoods import (
    loglik_exponential_rate,
    loglik_ou_euler_gamma,
    loglik_ou_exact_gamma,
)


def mle_exponential_rate_closed(s):
    """
    MLE in forma chiusa per tempi esponenziali.
    """
    s = np.asarray(s, dtype=float)
    return len(s) / np.sum(s)


def mle_exponential_rate_numeric(s, bounds=(0.01, 10.0)):
    """
    MLE numerica del tasso esponenziale.
    """
    res = minimize_scalar(
        lambda lam: -loglik_exponential_rate(lam, s),
        bounds=bounds,
        method="bounded"
    )
    return res.x, res


def two_state_sufficient_statistics(jumps_df, T, x0=1):
    """
    Calcola N12, N21, T1, T2 da una traiettoria a due stati.

    jumps_df deve contenere colonne:
        time, from_state, to_state
    """
    N12 = 0
    N21 = 0
    T1 = 0.0
    T2 = 0.0

    t_prev = 0.0
    x = int(x0)

    for _, row in jumps_df.iterrows():
        t_jump = float(row["time"])
        from_state = int(row["from_state"])
        to_state = int(row["to_state"])

        duration = t_jump - t_prev

        if x == 1:
            T1 += duration
        elif x == 2:
            T2 += duration
        else:
            raise ValueError("Lo stato deve essere 1 oppure 2.")

        if from_state == 1 and to_state == 2:
            N12 += 1
        elif from_state == 2 and to_state == 1:
            N21 += 1

        x = to_state
        t_prev = t_jump

    # ultimo intervallo senza salto fino a T
    duration = T - t_prev
    if x == 1:
        T1 += duration
    elif x == 2:
        T2 += duration

    return N12, N21, T1, T2


def estimate_two_state_rates(N12, N21, T1, T2):
    """
    MLE dei tassi alpha e beta.
    """
    if T1 <= 0 or T2 <= 0:
        raise ValueError("Tempi di esposizione nulli: stima non definita.")

    alpha_hat = N12 / T1
    beta_hat = N21 / T2
    return alpha_hat, beta_hat


def estimate_ou_gamma_regression(x, dt, mu):
    """
    Stima di gamma per OU dalla regressione sugli incrementi.
    """
    x = np.asarray(x, dtype=float)
    dx = x[1:] - x[:-1]
    y = x[:-1] - mu

    denom = dt * np.sum(y**2)

    if denom <= 0:
        raise ValueError("Denominatore nullo nella stima di gamma.")

    return -np.sum(y*dx) / denom


def estimate_ou_gamma_euler(x, dt, mu, sigma, bounds=(0.01, 5.0)):
    """
    Stima numerica di gamma con likelihood Euler--Maruyama.
    """
    res = minimize_scalar(
        lambda g: -loglik_ou_euler_gamma(g, x, dt, mu, sigma),
        bounds=bounds,
        method="bounded"
    )
    return res.x, res


def estimate_ou_gamma_exact(x, dt, mu, sigma, bounds=(0.01, 5.0)):
    """
    Stima numerica di gamma con propagatore esatto OU.
    """
    res = minimize_scalar(
        lambda g: -loglik_ou_exact_gamma(g, x, dt, mu, sigma),
        bounds=bounds,
        method="bounded"
    )
    return res.x, res


# ---------------------------------------------------------------------
# Parte D: SIR simulation-based
# ---------------------------------------------------------------------

def simulate_sir_gillespie(beta, gamma, N, I0, R0, T_max, seed=None):
    """
    Simula un modello SIR stocastico con algoritmo di Gillespie.
    """
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
    """
    Restituisce statistiche riassuntive:
    final_size_R, peak_I, time_peak.
    """
    I = traj["I"]
    R = traj["R"]
    t = traj["t"]

    final_size = R[-1]
    peak_I = np.max(I)
    time_peak = t[np.argmax(I)]

    return np.array([final_size, peak_I, time_peak], dtype=float)


def smm_objective_sir(params, obs_stats, N, I0, R0, T_max,
                      n_sim=20, scale=None, seed=1234):
    """
    Funzione obiettivo per metodo dei momenti simulati.
    """
    beta, gamma = params

    if beta <= 0 or gamma <= 0:
        return 1e12

    obs_stats = np.asarray(obs_stats, dtype=float)

    if scale is None:
        scale = np.maximum(np.abs(obs_stats), 1.0)

    rng = np.random.default_rng(seed)
    stats = []

    for _ in range(n_sim):
        sim_seed = int(rng.integers(0, 2**32 - 1))
        traj = simulate_sir_gillespie(
            beta, gamma, N, I0, R0, T_max, seed=sim_seed
        )
        stats.append(sir_summary_stats(traj))

    mean_stats = np.mean(stats, axis=0)
    diff = (mean_stats - obs_stats) / scale

    return float(np.sum(diff**2))


def estimate_sir_smm(obs_stats, N, I0, R0, T_max,
                     x0=(0.35, 0.15), n_sim=20):
    """
    Stima beta, gamma con Nelder--Mead.
    """
    scale = np.maximum(np.abs(obs_stats), 1.0)

    res = minimize(
        smm_objective_sir,
        x0=np.array(x0, dtype=float),
        args=(obs_stats, N, I0, R0, T_max, n_sim, scale),
        method="Nelder-Mead",
        options={"maxiter": 80, "xatol": 0.02, "fatol": 0.02}
    )

    return res.x, res
