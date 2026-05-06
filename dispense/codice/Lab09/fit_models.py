"""
fit_models.py

Stima di modelli ARMA, ARCH e GARCH con massima likelihood gaussiana.

Questo file è volutamente didattico:

- non usa librerie specializzate per serie temporali;
- scrive esplicitamente residui, varianze condizionate e log-likelihood;
- usa scipy.optimize.minimize solo per massimizzare la likelihood.

Idea generale della massima likelihood:

    1. fissiamo un modello probabilistico;
    2. calcoliamo la probabilità dei dati per dati parametri;
    3. scegliamo i parametri che rendono i dati osservati più plausibili.

Poiché massimizzare L è equivalente a massimizzare log L,
lavoriamo con la log-likelihood. Numericamente, minimizziamo la
negative log-likelihood.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


# ============================================================
# Funzioni di utilità
# ============================================================

def as_1d_array(x):
    """
    Converte l'input in array NumPy monodimensionale.

    Serve a intercettare subito errori comuni:
    - dati mancanti;
    - valori infiniti;
    - array con dimensioni sbagliate.
    """
    x = np.asarray(x, dtype=float)

    if x.ndim != 1:
        raise ValueError("La serie deve essere monodimensionale.")

    if np.any(~np.isfinite(x)):
        raise ValueError("La serie contiene NaN o inf.")

    return x


def gaussian_negative_loglik(residuals, sigma2):
    """
    Negative log-likelihood gaussiana per residui indipendenti.

    Se e_t ~ N(0, sigma2), allora

        log p(e_t) = -1/2 log(2 pi sigma2) - e_t^2/(2 sigma2).

    Sommando su t e cambiando segno otteniamo la negative log-likelihood.
    """
    residuals = as_1d_array(residuals)

    if sigma2 <= 0:
        return np.inf

    n = len(residuals)

    return 0.5 * n * np.log(2.0 * np.pi * sigma2) + 0.5 * np.sum(residuals**2) / sigma2


# ============================================================
# ARMA(p,q)
# ============================================================


def compute_arma_residuals(x, constant, phi, theta):
    """
    Calcola previsione e residui di un modello ARMA(p,q).

    Modello:

        X_t = c
              + phi_1 X_{t-1} + ... + phi_p X_{t-p}
              + eps_t
              + theta_1 eps_{t-1} + ... + theta_q eps_{t-q}

    Riscrivendo:

        eps_t = X_t - previsione_t.

    Differenza didattica importante:

    - nei modelli AR i valori passati X_{t-1}, X_{t-2}, ... sono osservati;
    - nei modelli MA gli shock passati eps_{t-1}, eps_{t-2}, ... non sono osservati,
      quindi vanno ricostruiti ricorsivamente.
    """
    x = as_1d_array(x)
    phi = np.asarray(phi, dtype=float)
    theta = np.asarray(theta, dtype=float)

    p = len(phi)
    q = len(theta)
    n = len(x)

    # Per i primi max(p,q) tempi non abbiamo tutta la storia necessaria.
    start = max(p, q)

    residuals = np.zeros(n)
    fitted = np.zeros(n)

    for t in range(start, n):
        # Parte autoregressiva: dipende dai valori passati osservati.
        ar_part = 0.0
        for i in range(p):
            ar_part += phi[i] * x[t - i - 1]

        # Parte moving average: dipende dagli shock passati ricostruiti.
        ma_part = 0.0
        for j in range(q):
            ma_part += theta[j] * residuals[t - j - 1]

        # Previsione condizionata al passato.
        fitted[t] = constant + ar_part + ma_part

        # Residuo/innovazione stimata.
        residuals[t] = x[t] - fitted[t]

    # I primi valori sono convenzionali e non vanno interpretati.
    residuals[:start] = np.nan
    fitted[:start] = np.nan

    return residuals, fitted


def fit_arma_mle(x, p=1, q=0, include_constant=True):
    """
    Stima ARMA(p,q) con likelihood gaussiana condizionale.

    La funzione restituisce un dizionario con:
    - parametri stimati;
    - residui;
    - valori previsti;
    - log-likelihood;
    - AIC e BIC;
    - breve summary testuale.

    Nota:
    per mantenere il codice leggibile, imponiamo bounds semplici sui parametri
    AR e MA: ciascun coefficiente è vincolato in (-0.98, 0.98).
    Questo non è un controllo completo di stazionarietà/invertibilità per ordini
    superiori, ma è sufficiente per un laboratorio introduttivo.
    """
    x = as_1d_array(x)
    n = len(x)

    # --------------------------------------------------------
    # Preparazione del vettore dei parametri
    # --------------------------------------------------------
    # Parametri da stimare:
    #   constant, se richiesta
    #   phi_1, ..., phi_p
    #   theta_1, ..., theta_q
    #   log_sigma
    # Usiamo log_sigma invece di sigma per garantire sigma > 0.

    number_of_parameters = (1 if include_constant else 0) + p + q + 1

    initial_guess = np.zeros(number_of_parameters)

    index = 0

    if include_constant:
        initial_guess[index] = np.mean(x)
        index += 1

    for _ in range(p):
        initial_guess[index] = 0.1
        index += 1

    for _ in range(q):
        initial_guess[index] = 0.1
        index += 1

    initial_guess[index] = np.log(np.std(x, ddof=1))

    # Bounds semplici per evitare esplosioni numeriche.
    bounds = []

    if include_constant:
        bounds.append((None, None))

    for _ in range(p):
        bounds.append((-0.98, 0.98))

    for _ in range(q):
        bounds.append((-0.98, 0.98))

    bounds.append((np.log(1e-8), None))

    def unpack_parameters(params):
        """Trasforma il vettore piatto dei parametri in oggetti leggibili."""
        index = 0

        if include_constant:
            constant = params[index]
            index += 1
        else:
            constant = 0.0

        phi = params[index:index + p]
        index += p

        theta = params[index:index + q]
        index += q

        sigma = np.exp(params[index])

        return constant, phi, theta, sigma

    def objective(params):
        """
        Funzione da minimizzare: negative log-likelihood.
        """
        constant, phi, theta, sigma = unpack_parameters(params)

        residuals, _ = compute_arma_residuals(x, constant, phi, theta)
        residuals = residuals[np.isfinite(residuals)]

        return gaussian_negative_loglik(residuals, sigma2=sigma**2)

    # --------------------------------------------------------
    # Ottimizzazione numerica
    # --------------------------------------------------------

    result = minimize(
        objective,
        initial_guess,
        method="L-BFGS-B",
        bounds=bounds,
    )

    constant, phi, theta, sigma = unpack_parameters(result.x)
    residuals, fitted = compute_arma_residuals(x, constant, phi, theta)

    loglik = -result.fun
    aic = 2 * number_of_parameters - 2 * loglik
    bic = np.log(n) * number_of_parameters - 2 * loglik

    lines = []
    lines.append(f"ARMA({p},{q}) gaussiano")
    lines.append(f"convergenza: {result.success}")
    lines.append(f"log-likelihood: {loglik:.4f}")
    lines.append(f"AIC: {aic:.4f}")
    lines.append(f"BIC: {bic:.4f}")
    lines.append(f"constant = {constant:.6f}")

    for i, value in enumerate(phi, start=1):
        lines.append(f"phi_{i} = {value:.6f}")

    for j, value in enumerate(theta, start=1):
        lines.append(f"theta_{j} = {value:.6f}")

    lines.append(f"sigma = {sigma:.6f}")

    return {
        "success": result.success,
        "constant": constant,
        "phi": phi,
        "theta": theta,
        "sigma": sigma,
        "residuals": residuals,
        "fitted": fitted,
        "loglik": loglik,
        "aic": aic,
        "bic": bic,
        "summary": "\n".join(lines),
    }


# ============================================================
# ARCH(1)
# ============================================================


def fit_arch1_mle(x):
    """
    Stima ARCH(1) gaussiano.

    Modello:

        X_t = mu + eps_t
        eps_t = sigma_t z_t
        z_t ~ N(0,1)

        sigma_t^2 = omega + alpha eps_{t-1}^2

    Interpretazione:

    - mu descrive la media condizionata, qui assunta costante;
    - omega è il livello base della varianza;
    - alpha misura quanto uno shock grande al tempo t-1 aumenta la varianza al tempo t.

    Vincoli:

        omega > 0
        0 <= alpha < 1
    """
    x = as_1d_array(x)
    n = len(x)

    def unpack_parameters(params):
        """
        Parametrizzazione vincolata.

        Usiamo:
        - omega = exp(raw_omega), quindi omega > 0;
        - alpha = logistic(raw_alpha), quindi 0 < alpha < 1.
        """
        mu = params[0]
        omega = np.exp(params[1])
        alpha = 1.0 / (1.0 + np.exp(-params[2]))
        return mu, omega, alpha

    def compute_variance(eps, omega, alpha):
        """Calcola ricorsivamente sigma_t^2."""
        sigma2 = np.zeros(n)

        # Valore iniziale: varianza non condizionata dell'ARCH(1), se alpha < 1.
        sigma2[0] = omega / (1.0 - alpha)

        for t in range(1, n):
            sigma2[t] = omega + alpha * eps[t - 1] ** 2

        return sigma2

    def objective(params):
        """Negative log-likelihood ARCH(1)."""
        mu, omega, alpha = unpack_parameters(params)

        eps = x - mu
        sigma2 = compute_variance(eps, omega, alpha)

        if np.any(sigma2 <= 0) or np.any(~np.isfinite(sigma2)):
            return np.inf

        # Qui ogni eps_t ha varianza condizionata sigma_t^2,
        # quindi la likelihood gaussiana cambia a ogni t.
        nll = 0.5 * np.sum(
            np.log(2.0 * np.pi)
            + np.log(sigma2)
            + eps**2 / sigma2
        )

        return nll

    initial_guess = np.array([
        np.mean(x),
        np.log(0.2 * np.var(x, ddof=1) + 1e-8),
        0.0,
    ])

    result = minimize(objective, initial_guess, method="BFGS")

    mu, omega, alpha = unpack_parameters(result.x)
    eps = x - mu
    sigma2 = compute_variance(eps, omega, alpha)
    sigma = np.sqrt(sigma2)

    # Residui standardizzati: dovrebbero assomigliare a N(0,1)
    # se il modello ha catturato bene la varianza condizionata.
    standardized_residuals = eps / sigma

    number_of_parameters = 3
    loglik = -result.fun
    aic = 2 * number_of_parameters - 2 * loglik
    bic = np.log(n) * number_of_parameters - 2 * loglik

    lines = []
    lines.append("ARCH(1) gaussiano")
    lines.append(f"convergenza: {result.success}")
    lines.append(f"log-likelihood: {loglik:.4f}")
    lines.append(f"AIC: {aic:.4f}")
    lines.append(f"BIC: {bic:.4f}")
    lines.append(f"mu = {mu:.6f}")
    lines.append(f"omega = {omega:.6f}")
    lines.append(f"alpha = {alpha:.6f}")

    return {
        "success": result.success,
        "mu": mu,
        "omega": omega,
        "alpha": alpha,
        "sigma": sigma,
        "standardized_residuals": standardized_residuals,
        "loglik": loglik,
        "aic": aic,
        "bic": bic,
        "summary": "\n".join(lines),
    }


# ============================================================
# GARCH(1,1)
# ============================================================


def fit_garch11_mle(x):
    """
    Stima GARCH(1,1) gaussiano.

    Modello:

        X_t = mu + eps_t
        eps_t = sigma_t z_t
        z_t ~ N(0,1)

        sigma_t^2 = omega
                    + alpha eps_{t-1}^2
                    + beta sigma_{t-1}^2

    Interpretazione:

    - alpha misura la risposta della volatilità agli shock recenti;
    - beta misura la persistenza della volatilità passata;
    - alpha + beta misura la persistenza complessiva.

    Condizione usuale per varianza non condizionata finita:

        alpha + beta < 1.
    """
    x = as_1d_array(x)
    n = len(x)

    def unpack_parameters(params):
        """
        Parametrizzazione che impone:

            omega > 0
            alpha >= 0
            beta >= 0
            alpha + beta < 1

        Usiamo due variabili positive a_raw e b_raw e normalizziamo:

            alpha = a_raw / (1 + a_raw + b_raw)
            beta  = b_raw / (1 + a_raw + b_raw)
        """
        mu = params[0]
        omega = np.exp(params[1])

        a_raw = np.exp(params[2])
        b_raw = np.exp(params[3])

        denominator = 1.0 + a_raw + b_raw
        alpha = a_raw / denominator
        beta = b_raw / denominator

        return mu, omega, alpha, beta

    def compute_variance(eps, omega, alpha, beta):
        """Calcola ricorsivamente sigma_t^2."""
        sigma2 = np.zeros(n)

        # Varianza non condizionata, se alpha + beta < 1.
        sigma2[0] = omega / (1.0 - alpha - beta)

        for t in range(1, n):
            sigma2[t] = (
                omega
                + alpha * eps[t - 1] ** 2
                + beta * sigma2[t - 1]
            )

        return sigma2

    def objective(params):
        """Negative log-likelihood GARCH(1,1)."""
        mu, omega, alpha, beta = unpack_parameters(params)

        eps = x - mu
        sigma2 = compute_variance(eps, omega, alpha, beta)

        if np.any(sigma2 <= 0) or np.any(~np.isfinite(sigma2)):
            return np.inf

        nll = 0.5 * np.sum(
            np.log(2.0 * np.pi)
            + np.log(sigma2)
            + eps**2 / sigma2
        )

        return nll

    initial_guess = np.array([
        np.mean(x),
        np.log(0.05 * np.var(x, ddof=1) + 1e-8),
        np.log(0.10),
        np.log(0.80),
    ])

    result = minimize(objective, initial_guess, method="BFGS")

    mu, omega, alpha, beta = unpack_parameters(result.x)
    eps = x - mu
    sigma2 = compute_variance(eps, omega, alpha, beta)
    sigma = np.sqrt(sigma2)

    standardized_residuals = eps / sigma

    number_of_parameters = 4
    loglik = -result.fun
    aic = 2 * number_of_parameters - 2 * loglik
    bic = np.log(n) * number_of_parameters - 2 * loglik

    lines = []
    lines.append("GARCH(1,1) gaussiano")
    lines.append(f"convergenza: {result.success}")
    lines.append(f"log-likelihood: {loglik:.4f}")
    lines.append(f"AIC: {aic:.4f}")
    lines.append(f"BIC: {bic:.4f}")
    lines.append(f"mu = {mu:.6f}")
    lines.append(f"omega = {omega:.6f}")
    lines.append(f"alpha = {alpha:.6f}")
    lines.append(f"beta = {beta:.6f}")
    lines.append(f"alpha + beta = {alpha + beta:.6f}")

    return {
        "success": result.success,
        "mu": mu,
        "omega": omega,
        "alpha": alpha,
        "beta": beta,
        "persistence": alpha + beta,
        "sigma": sigma,
        "standardized_residuals": standardized_residuals,
        "loglik": loglik,
        "aic": aic,
        "bic": bic,
        "summary": "\n".join(lines),
    }
