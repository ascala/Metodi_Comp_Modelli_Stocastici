"""
Nome file: sample_positions_at_times.py

Scopo:
    Estrarre la posizione del processo a tempi fissati da molte traiettorie discrete.
"""

from __future__ import annotations
import numpy as np

def sample_single_trajectory(times: np.ndarray, sites: np.ndarray, query_times: np.ndarray) -> np.ndarray:
    times = np.asarray(times, dtype=float)
    sites = np.asarray(sites, dtype=int)
    query_times = np.asarray(query_times, dtype=float)
    idx = np.searchsorted(times, query_times, side="right") - 1
    idx = np.clip(idx, 0, len(sites) - 1)
    return sites[idx]

def sample_positions_at_times(trajectories, query_times):
    query_times = np.asarray(query_times, dtype=float)
    sampled = [sample_single_trajectory(times, sites, query_times) for times, sites in trajectories]
    return np.asarray(sampled, dtype=int)

if __name__ == "__main__":
    traj = [
        (np.array([0.0, 0.4, 0.9, 1.3]), np.array([5, 6, 5, 4])),
        (np.array([0.0, 0.2, 0.7]), np.array([5, 4, 3])),
    ]
    qt = np.array([0.1, 0.5, 1.0])
    print(sample_positions_at_times(traj, qt))
