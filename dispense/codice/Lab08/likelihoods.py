"""
Funzioni di log-likelihood per LAB08.

Alcune funzioni sono già complete, altre sono lasciate volutamente da completare.
"""

import numpy as np


def loglik_exponential_rate(lam, s):
    """
    Log-likelihood di tempi di attesa esponenziali con tasso lam.

    Parametri
    ---------
    lam : float
        Tasso del processo.
    s : array-like
        Tempi di interarrivo osservati.

    Ritorna
    -------
    float
        Log-likelihood.
    """
    s = np.asarray(s, dtype=float)

    if lam <= 0:
        return -np.inf

    n = len(s)

    # DA COMPLETARE:
    # ell(lam) = n log(lam) - lam sum_i s_i
    return n * np.log(lam) - lam * np.sum(s)


def loglik_two_state(alpha, beta, N12, N21, T1, T2):
    """
    Log-likelihood del processo di salto a due stati.

    ell(alpha,beta) =
        N12 log alpha + N21 log beta - alpha T1 - beta T2
    """
    if alpha <= 0 or beta <= 0:
        return -np.inf

    # DA COMPLETARE se si vuole rifare a mano:
    return N12*np.log(alpha) + N21*np.log(beta) - alpha*T1 - beta*T2


def loglik_ou_euler_gamma(gamma, x, dt, mu, sigma):
    """
    Log-likelihood approssimata Euler--Maruyama per OU,
    stimando gamma e assumendo mu e sigma noti.
    """
    if gamma <= 0 or sigma <= 0 or dt <= 0:
        return -np.inf

    x = np.asarray(x, dtype=float)

    xk = x[:-1]
    xnext = x[1:]

    mean = xk - gamma*(xk - mu)*dt
    var = sigma**2 * dt
    resid = xnext - mean

    return -0.5*np.sum(np.log(2*np.pi*var) + resid**2/var)


def loglik_ou_exact_gamma(gamma, x, dt, mu, sigma):
    """
    Log-likelihood esatta per OU,
    stimando gamma e assumendo mu e sigma noti.

    X_{k+1}|X_k=x_k ~ N(
        mu + (x_k-mu) exp(-gamma dt),
        sigma^2/(2 gamma) (1-exp(-2 gamma dt))
    )
    """
    if gamma <= 0 or sigma <= 0 or dt <= 0:
        return -np.inf

    x = np.asarray(x, dtype=float)

    xk = x[:-1]
    xnext = x[1:]

    a = np.exp(-gamma*dt)
    mean = mu + (xk - mu)*a
    var = sigma**2/(2*gamma) * (1 - np.exp(-2*gamma*dt))

    if var <= 0:
        return -np.inf

    resid = xnext - mean

    return -0.5*np.sum(np.log(2*np.pi*var) + resid**2/var)
