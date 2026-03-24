import numpy as np
import matplotlib.pyplot as plt

# Parametri
lam = 0.1
A0 = 100
t_max = 50
n_traj = 50

def gillespie_decay(A0, lam, t_max):
    t = 0.0
    A = A0
    times = [t]
    values = [A]

    while A > 0 and t < t_max:
        a0 = lam * A
        if a0 == 0:
            break
        dt = np.random.exponential(1 / a0)
        t += dt
        A -= 1
        times.append(t)
        values.append(A)

    return np.array(times), np.array(values)

# Griglia temporale per media
t_grid = np.linspace(0, t_max, 200)
mean_A = np.zeros_like(t_grid)

# Simulazioni
for _ in range(n_traj):
    t, A = gillespie_decay(A0, lam, t_max)
    A_interp = np.interp(t_grid, t, A, left=A0, right=0)
    mean_A += A_interp

mean_A /= n_traj

# Soluzione teorica
A_theory = A0 * np.exp(-lam * t_grid)

# Plot
plt.figure()
t, A = gillespie_decay(A0, lam, t_max)
plt.step(t, A, where='post', label='Traiettoria singola')

plt.plot(t_grid, mean_A, label='Media simulazioni')
plt.plot(t_grid, A_theory, linestyle='--', label='Soluzione teorica')

plt.xlabel('t')
plt.ylabel('A(t)')
plt.legend()
plt.title('Gillespie: A -> ∅')
plt.show()
