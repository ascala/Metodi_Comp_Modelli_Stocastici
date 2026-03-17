
import numpy as np
import matplotlib.pyplot as plt

DOMAIN_X = (-4, 4)
DOMAIN_Y = (-4, 4)

MU = np.array([0.0, 0.0])
SIGMA_X = 1.5
SIGMA_Y = 0.7
ROTATION_DEG = 25.0

N_STEPS = 160
STEP_SMALL = 0.12
STEP_GOOD = 0.55
STEP_LARGE = 2.5
START = np.array([-2.0, -2.0])
SEED = 3

def rotation_matrix(theta_deg):
    th = np.deg2rad(theta_deg)
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s],[s, c]])

def covariance(sigx, sigy, theta):
    R = rotation_matrix(theta)
    D = np.diag([sigx**2, sigy**2])
    return R @ D @ R.T

def gaussian_pdf(points, mu, Sigma):
    invS = np.linalg.inv(Sigma)
    d = points - mu
    expo = -0.5 * np.einsum("...i,ij,...j->...", d, invS, d)
    return np.exp(expo)

def metropolis_accepted_rejected(step_size, start, mu, Sigma, n_steps, rng):
    x = start.copy()
    fx = gaussian_pdf(x[None, :], mu, Sigma)[0]

    accepted = [x.copy()]
    rejected = []
    n_accept = 0

    for _ in range(n_steps):
        proposal = x + rng.normal(scale=step_size, size=2)
        fp = gaussian_pdf(proposal[None, :], mu, Sigma)[0]
        alpha = min(1.0, fp / fx)

        if rng.uniform() < alpha:
            x = proposal
            fx = fp
            accepted.append(x.copy())
            n_accept += 1
        else:
            rejected.append(proposal.copy())

    accepted = np.array(accepted)
    rejected = np.array(rejected) if rejected else np.empty((0, 2))
    acc_rate = n_accept / n_steps
    return accepted, rejected, acc_rate

def main():
    rng = np.random.default_rng(SEED)
    Sigma = covariance(SIGMA_X, SIGMA_Y, ROTATION_DEG)

    x = np.linspace(*DOMAIN_X, 350)
    y = np.linspace(*DOMAIN_Y, 350)
    X, Y = np.meshgrid(x, y)
    pts = np.stack([X, Y], axis=-1)
    Z = gaussian_pdf(pts, MU, Sigma)

    cases = [
        ("Proposta troppo piccola", STEP_SMALL),\
        ("Scala quasi ottimale", STEP_GOOD),
        ("Proposta troppo grande", STEP_LARGE),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(12, 8), sharex=True, sharey=True)

    for ax, (title, step) in zip(axes, cases):
        accepted, rejected, acc_rate = metropolis_accepted_rejected(
            step, START, MU, Sigma, N_STEPS, rng
        )

        ax.contour(X, Y, Z, levels=8, linewidths=1.0)
        ax.plot(accepted[:, 0], accepted[:, 1], linewidth=1.8)
        ax.scatter(accepted[:, 0], accepted[:, 1], s=14, zorder=3)

        if len(rejected) > 0:
            ax.scatter(
                rejected[:, 0], rejected[:, 1],
                marker='*', s=38, c='red', alpha=0.85, zorder=4
            )

        ax.scatter([START[0]], [START[1]], marker='x', s=70, linewidths=2, zorder=5)
        #ax.set_title(title)
        ax.text(
            0.03, 0.97, f"acc = {acc_rate:.2f}",
            transform=ax.transAxes, ha='left', va='top', fontsize=11,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.8", alpha=0.9)
        )
        ax.set_xlim(*DOMAIN_X)
        ax.set_ylim(*DOMAIN_Y)
        ax.set_aspect("auto")
#        ax.set_aspect("equal")
#        ax.set_aspect(0.5)
        ax.set_xlabel(r"$x_1$")

    axes[0].set_ylabel(r"$x_2$")
    #fig.suptitle("Effetto della scala della proposta: traiettoria accettata e mosse rifiutate", fontsize=14)
    fig.savefig("acceptance_rate_accepted_vs_rejected.png", dpi=240, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
