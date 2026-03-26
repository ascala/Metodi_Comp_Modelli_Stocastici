import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# parameters
beta = 0.5
gamma = 0.2
N = 200

# initial condition
S0, I0, R0 = 199, 1, 0

# rhs
def sir_rhs(t, y):
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

# time grid
t0, T = 0.0, 60.0
t_eval = np.linspace(t0, T, 400)

# solve
sol = solve_ivp(sir_rhs, [t0, T], [S0, I0, R0], t_eval=t_eval)

# plot
plt.plot(sol.t, sol.y[0], label="S")
plt.plot(sol.t, sol.y[1], label="I")
plt.plot(sol.t, sol.y[2], label="R")

plt.legend()
plt.xlabel("t")
plt.ylabel("population")
plt.title("SIR ODE")
plt.show()
