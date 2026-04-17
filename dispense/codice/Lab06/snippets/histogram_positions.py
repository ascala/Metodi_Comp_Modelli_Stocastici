"""
Nome file: histogram_positions.py

Scopo:
    Costruire e visualizzare istogrammi delle posizioni a tempi fissati.
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_position_histograms(sampled_positions: np.ndarray, query_times, bins=None, density: bool = True):
    sampled_positions = np.asarray(sampled_positions)
    query_times = np.asarray(query_times, dtype=float)
    K = sampled_positions.shape[1]
    fig, axes = plt.subplots(1, K, figsize=(4 * K, 3), squeeze=False)
    axes = axes[0]
    for j, ax in enumerate(axes):
        ax.hist(sampled_positions[:, j], bins=bins, density=density)
        ax.set_title(f"t = {query_times[j]:.2f}")
        ax.set_xlabel("posizione")
        ax.set_ylabel("densità" if density else "conteggio")
    fig.tight_layout()
    return fig, axes

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    sampled = rng.integers(low=0, high=10, size=(1000, 3))
    plot_position_histograms(sampled, query_times=[1.0, 2.0, 3.0], bins=np.arange(-0.5, 10.5, 1))
    plt.show()
