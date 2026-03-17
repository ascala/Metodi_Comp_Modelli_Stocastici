
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Parametri modificabili
# =========================
SIGMA_X = 1.8
SIGMA_Y = 0.6
ROTATION_DEG = 35.0
MU_X = 0.0
MU_Y = 0.0

DOMAIN_X = (-5.0, 5.0)
DOMAIN_Y = (-5.0, 5.0)

N_DIRECT = 220          # punti "Monte Carlo standard" uniformi sul dominio
N_MCMC = 180            # lunghezza traiettoria MCMC
MCMC_STEP = 0.45        # ampiezza proposta random-walk
MCMC_START = (-3.5, -2.8)
SEED = 7

# =========================
# Costruzione gaussiana 2D ruotata
# =========================
def rotation_matrix(theta_deg):
    th = np.deg2rad(theta_deg)
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s], [s,  c]])

def covariance_matrix(sigmax, sigmay, theta_deg):
    R = rotation_matrix(theta_deg)
    D = np.diag([sigmax**2, sigmay**2])
    return R @ D @ R.T

def gaussian_unnormalized(points, mu, Sigma):
    invS = np.linalg.inv(Sigma)
    d = points - mu
    expo = -0.5 * np.einsum("...i,ij,...j->...", d, invS, d)
    return np.exp(expo)

def mcmc_random_walk(n_steps, start, mu, Sigma, step, rng):
    x = np.array(start, dtype=float)
    traj = [x.copy()]
    fx = gaussian_unnormalized(x[None, :], mu, Sigma)[0]
    for _ in range(n_steps - 1):
        proposal = x + rng.normal(scale=step, size=2)
        fp = gaussian_unnormalized(proposal[None, :], mu, Sigma)[0]
        alpha = min(1.0, fp / fx)
        if rng.uniform() < alpha:
            x = proposal
            fx = fp
        traj.append(x.copy())
    return np.array(traj)

def main():
    rng = np.random.default_rng(SEED)

    mu = np.array([MU_X, MU_Y], dtype=float)
    Sigma = covariance_matrix(SIGMA_X, SIGMA_Y, ROTATION_DEG)

    # Griglia per curve di livello
    x = np.linspace(*DOMAIN_X, 300)
    y = np.linspace(*DOMAIN_Y, 300)
    X, Y = np.meshgrid(x, y)
    pts = np.stack([X, Y], axis=-1)
    Z = gaussian_unnormalized(pts, mu, Sigma)

    # Punti uniformi nel dominio
    direct_x = rng.uniform(DOMAIN_X[0], DOMAIN_X[1], size=N_DIRECT)
    direct_y = rng.uniform(DOMAIN_Y[0], DOMAIN_Y[1], size=N_DIRECT)

    # Traiettoria MCMC
    traj = mcmc_random_walk(N_MCMC, MCMC_START, mu, Sigma, MCMC_STEP, rng)

    fig, axes = plt.subplots(2, 1, figsize=(10, 10), constrained_layout=True)

    # Pannello alto: punti uniformi su dominio
    ax = axes[0]
    ax.contour(X, Y, Z, levels=8, linewidths=1.2)
    ax.scatter(direct_x, direct_y, s=14, alpha=0.9)
    ax.set_title("Punti uniformi sul dominio")
    ax.set_xlim(*DOMAIN_X)
    ax.set_ylim(*DOMAIN_Y)
    #ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")

    # Pannello basso: traiettoria MCMC
    ax = axes[1]
    ax.contour(X, Y, Z, levels=8, linewidths=1.2)
    ax.plot(traj[:, 0], traj[:, 1], linewidth=1.1, alpha=0.95)
    ax.scatter(traj[:, 0], traj[:, 1], s=8, alpha=0.8)
    ax.scatter([traj[0, 0]], [traj[0, 1]], s=60, marker="x", linewidths=2, label="start")
    ax.set_title("Traiettoria MCMC concentrata vicino al picco")
    ax.set_xlim(*DOMAIN_X)
    ax.set_ylim(*DOMAIN_Y)
    #ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper right", frameon=True)

    fig.suptitle("Campionamento uniforme vs MCMC su una gaussiana 2D ruotata", fontsize=14)
    fig.savefig("direct_vs_mcmc_contours.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
