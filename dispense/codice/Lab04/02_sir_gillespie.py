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

t_list = [t]
S_list = [S]
I_list = [I]
R_list = [R]

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
    S_list.append(S)
    I_list.append(I)
    R_list.append(R)

# plot
plt.step(t_list, I_list, where="post", label="I(t)")

plt.xlabel("t")
plt.ylabel("infected")
plt.title("Gillespie SIR (single trajectory)")
plt.legend()
plt.show()
