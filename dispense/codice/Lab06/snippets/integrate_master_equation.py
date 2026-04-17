"""
Nome file: integrate_master_equation.py

Scopo:
    Integrare numericamente la master equation a partire dal generatore e dal dato iniziale.
"""

from __future__ import annotations
import numpy as np
from scipy.integrate import solve_ivp

def integrate_master_equation(L, p0, t_span, t_eval=None, method: str = "RK45", rtol: float = 1e-8, atol: float = 1e-10):
    p0 = np.asarray(p0, dtype=float)
    def rhs(t, p):
        return L @ p
    sol = solve_ivp(rhs, t_span=t_span, y0=p0, t_eval=t_eval, method=method, rtol=rtol, atol=atol)
    return sol.t, sol.y

if __name__ == "__main__":
    from build_generator_dense import build_generator_dense
    N = 20
    L = build_generator_dense(N=N, r=1.2, ell=0.8)
    p0 = np.zeros(N + 1)
    p0[N // 2] = 1.0
    t, y = integrate_master_equation(L, p0, t_span=(0.0, 3.0), t_eval=np.linspace(0.0, 3.0, 6))
    print("Shape soluzione:", y.shape)
    print("Normalizzazione finale:", y[:, -1].sum())
