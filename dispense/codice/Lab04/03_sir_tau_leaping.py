import numpy as np
import matplotlib.pyplot as plt

# parameters
beta = 0.5
gamma = 0.2
N = 200

# initial condition
S, I, R = 199, 1, 0

# rng
rng = np.random.default_rng(123)

t = 0.0
T = 60.0
dt = 0.1

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

# plot
plt.plot(t_list, I_list, label="tau-leaping")

plt.xlabel("t")
plt.ylabel("infected")
plt.title("Tau-leaping SIR")
plt.legend()
plt.show()
