import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

# Parametri
lam = 0.1
A0 = 50
t_max = 50
n_traj = 100
n_grid = 400
interval_ms = 120

rng = np.random.default_rng(12345)

def gillespie_decay(A0, lam, t_max, rng):
    t = 0.0
    A = A0
    times = [t]
    values = [A]

    while A > 0 and t < t_max:
        a0 = lam * A
        dt = rng.exponential(1.0 / a0)
        t += dt
        A -= 1
        times.append(t)
        values.append(A)

    if times[-1] < t_max:
        times.append(t_max)
        values.append(values[-1])

    return np.array(times), np.array(values)

# Precalcolo traiettorie
trajectories = [gillespie_decay(A0, lam, t_max, rng) for _ in range(n_traj)]

# Griglia comune per media e differenza
t_grid = np.linspace(0.0, t_max, n_grid)
A_mat = np.zeros((n_traj, n_grid))

for i, (t, A) in enumerate(trajectories):
    idx = np.searchsorted(t, t_grid, side="right") - 1
    idx[idx < 0] = 0
    A_mat[i] = A[idx]

A_theory = A0 * np.exp(-lam * t_grid)

# Figura con pannello alto + due pannelli bassi
fig = plt.figure(figsize=(12, 7))
gs = GridSpec(2, 2, height_ratios=[1, 3], figure=fig)

ax_top = fig.add_subplot(gs[0, :])
ax_left = fig.add_subplot(gs[1, 0])
ax_right = fig.add_subplot(gs[1, 1])

# Pannello alto: differenza teoria - media
ax_top.set_xlim(0, t_max)
ax_top.set_xlabel("t")
ax_top.set_ylabel("teoria - media")
ax_top.set_title("Scarto fra soluzione analitica e media empirica")
ax_top.axhline(0.0, linestyle="--", lw=1)
diff_line, = ax_top.plot([], [], lw=2)

# Pannello sinistro: traiettorie singole
ax_left.set_xlim(0, t_max)
ax_left.set_ylim(0, A0 + 2)
ax_left.set_xlabel("t")
ax_left.set_ylabel("A(t)")
ax_left.set_title("Traiettorie Gillespie")

traj_lines = []
for _ in range(n_traj):
    line, = ax_left.step([], [], where="post", lw=1)
    traj_lines.append(line)

# Pannello destro: media + soluzione analitica
ax_right.set_xlim(0, t_max)
ax_right.set_ylim(0, A0 + 2)
ax_right.set_xlabel("t")
ax_right.set_ylabel(r"$\langle A(t)\rangle$")
ax_right.set_title("Media empirica e soluzione analitica")
ax_right.plot(t_grid, A_theory, "--", lw=2, label="Soluzione analitica")
mean_line, = ax_right.plot([], [], lw=2, label="Media simulazioni")
ax_right.legend()

# Limiti verticali del pannello alto
max_diff = np.max(np.abs(A_mat.mean(axis=0) - A_theory))
#ax_top.set_ylim(-2 * max_diff, 2 * max_diff)
ax_top.set_ylim(-2 , 2)

def init():
    for line in traj_lines:
        line.set_data([], [])
    mean_line.set_data([], [])
    diff_line.set_data([], [])
    return traj_lines + [mean_line, diff_line]

def update(frame):
    # sinistra: aggiunge una traiettoria alla volta
    n_show = min(frame + 1, n_traj)

    for i, line in enumerate(traj_lines):
        if i < n_show:
            t, A = trajectories[i]
            line.set_data(t, A)
        else:
            line.set_data([], [])

    # destra: media delle traiettorie mostrate
    current_mean = A_mat[:n_show].mean(axis=0)
    mean_line.set_data(t_grid, current_mean)

    # sopra: differenza teoria - media
    diff_line.set_data(t_grid, A_theory - current_mean)

    return traj_lines + [mean_line, diff_line]

ani = FuncAnimation(
    fig,
    update,
    frames=n_traj,
    init_func=init,
    interval=interval_ms,
    blit=False,
    repeat=False
)

plt.tight_layout()
# ani.save("DemoChemReact.gif", writer="pillow", fps=8)
# ani.save("DemoChemReact.mp4", writer="ffmpeg", fps=8, dpi=150)
plt.show()