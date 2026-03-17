
import numpy as np
import matplotlib.pyplot as plt

# =========================
# Parametri modificabili
# =========================
X_MIN, X_MAX = -5.0, 5.0
N_BINS = 28

# distribuzione target gaussiana
MU_TARGET = 1.2
SIGMA_TARGET = 0.9

# sequenza dei tempi mostrati
TIMES = [0, 1, 5, 20, "∞"]

# parametri delle distribuzioni "transienti"
MU_T0, SIGMA_T0 = -2.8, 0.45
MU_T1, SIGMA_T1 = -1.8, 0.60
MU_T5, SIGMA_T5 = -0.2, 0.95
MU_T20, SIGMA_T20 = 0.9, 0.95

N_SAMPLES = 5000
SEED = 12

# =========================
# Funzioni
# =========================
def normal_pdf(x, mu, sigma):
    return (1.0 / (np.sqrt(2*np.pi) * sigma)) * np.exp(-0.5 * ((x - mu)/sigma)**2)

def sample_hist(rng, mu, sigma, n_samples, x_min, x_max, n_bins):
    x = rng.normal(mu, sigma, size=n_samples)
    x = x[(x >= x_min) & (x <= x_max)]
    bins = np.linspace(x_min, x_max, n_bins + 1)
    hist, edges = np.histogram(x, bins=bins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    width = edges[1] - edges[0]
    return centers, hist, width

def main():
    rng = np.random.default_rng(SEED)

    transient_params = {
        0: (MU_T0, SIGMA_T0),
        1: (MU_T1, SIGMA_T1),
        5: (MU_T5, SIGMA_T5),
        20: (MU_T20, SIGMA_T20),
        "∞": (MU_TARGET, SIGMA_TARGET),
    }

    xgrid = np.linspace(X_MIN, X_MAX, 600)
    target_pdf = normal_pdf(xgrid, MU_TARGET, SIGMA_TARGET)

    fig, axes = plt.subplots(len(TIMES), 1, figsize=(7.0, 11.5), sharex=True, constrained_layout=True)

    for ax, t in zip(axes, TIMES):
        mu, sigma = transient_params[t]
        centers, hist, width = sample_hist(rng, mu, sigma, N_SAMPLES, X_MIN, X_MAX, N_BINS)

        ax.bar(centers, hist, width=0.92*width, alpha=0.75, edgecolor="black", linewidth=0.6)
        ax.plot(xgrid, target_pdf, linewidth=2.0)

        if t == "∞":
            title = r"$\mu^{(\infty)} = \pi$"
        else:
            title = rf"$\mu^{{({t})}}$"

        ax.text(0.03, 0.88, title, transform=ax.transAxes, fontsize=14, ha="left", va="top")
        ax.set_ylabel("densità")
        ax.set_ylim(0, max(target_pdf)*1.35)
        ax.grid(False)

    axes[-1].set_xlabel(r"$x$")
    fig.suptitle("Evoluzione della distribuzione verso la distribuzione stazionaria", fontsize=15)
    fig.savefig("distribution_evolution_vertical.png", dpi=240, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    main()
