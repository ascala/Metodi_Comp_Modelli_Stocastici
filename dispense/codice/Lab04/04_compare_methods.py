import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# parameters
beta = 0.5
gamma = 0.2
N = 200

S0, I0, R0 = 199, 1, 0

T = 60.0
t_grid = np.linspace(0, T, 300)

rng = np.random.default_rng(123)

# ---------------- ODE ----------------

def sir_rhs(t, y):
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

sol = solve_ivp(sir_rhs, [0, T], [S0, I0, R0], t_eval=t_grid)
I_ode = sol.y[1]

# ---------------- Gillespie ----------------

def simulate_gillespie():
    S, I, R = S0, I0, R0
    t = 0.0

    t_list = [t]
    I_list = [I]

    while t < T and I > 0:
        a1 = beta * S * I / N
        a2 = gamma * I
        a0 = a1 + a2

        tau = rng.exponential(1 / a0)

        if rng.random() < a1 / a0:
            S -= 1
            I += 1
        else:
            I -= 1
            R += 1

        t += tau

        t_list.append(t)
        I_list.append(I)

    return np.array(t_list), np.array(I_list)

# ---------------- Tau-leaping ----------------

def simulate_tau(dt):
    S, I, R = S0, I0, R0
    t = 0.0

    t_list = [t]
    I_list = [I]

    while t < T and I > 0:
        a1 = beta * S * I / N
        a2 = gamma * I

        k1 = rng.poisson(a1 * dt)
        k2 = rng.poisson(a2 * dt)

        S -= k1
        I += k1 - k2
        R += k2

        t += dt

        t_list.append(t)
        I_list.append(I)

    return np.array(t_list), np.array(I_list)

# ---------------- Ensemble ----------------

M = 50
I_gill = []
I_tau = []

for _ in range(M):
    t, I = simulate_gillespie()
    I_interp = np.interp(t_grid, t, I)
    I_gill.append(I_interp)

    t, I = simulate_tau(dt=0.1)
    I_interp = np.interp(t_grid, t, I)
    I_tau.append(I_interp)

I_gill = np.array(I_gill)
I_tau = np.array(I_tau)

mean_g = I_gill.mean(axis=0)
std_g = I_gill.std(axis=0)

mean_t = I_tau.mean(axis=0)
std_t = I_tau.std(axis=0)

# ---------------- Plot ----------------

plt.plot(t_grid, I_ode, label="ODE", linewidth=2)

plt.plot(t_grid, mean_g, label="Gillespie mean")
plt.fill_between(t_grid, mean_g - std_g, mean_g + std_g, alpha=0.3)

plt.plot(t_grid, mean_t, label="tau-leaping mean")
plt.fill_between(t_grid, mean_t - std_t, mean_t + std_t, alpha=0.3)

plt.xlabel("t")
plt.ylabel("infected")
plt.title("Comparison SIR")
plt.legend()
plt.show()