#!/usr/bin/env python3
"""
Generazione dati sintetici per il laboratorio su serie temporali.

Crea serie anonime per esercizi su:
- rumore bianco gaussiano;
- AR(1) positivo;
- AR(1) negativo;
- MA(1);
- ARMA(1,1);
- ARCH(1);
- GARCH(1,1);
- GARCH asimmetrico tipo GJR-GARCH.

Lo script salva:
- data/serie_01.csv, ..., data/serie_08.csv
- data/soluzioni_generative.csv
- figures/serie_01.png, ..., figures/serie_08.png

Uso da terminale:

    python generate_lab08_arma_garch_data.py

oppure, scegliendo cartella di output e seed:

    python generate_lab08_arma_garch_data.py --outdir lab08_serie --seed 12345 --n 1200 --burnin 300
"""

from __future__ import annotations

import argparse
from pathlib import Path
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class SeriesMetadata:
    file: str
    label: str
    model: str
    parameters: str
    comment: str


def ensure_dirs(outdir: Path) -> tuple[Path, Path]:
    data_dir = outdir / "data"
    fig_dir = outdir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)
    return data_dir, fig_dir


def standardise(x: np.ndarray) -> np.ndarray:
    """Centra e riscalare una serie per rendere confrontabili i grafici."""
    x = np.asarray(x, dtype=float)
    return (x - np.mean(x)) / np.std(x, ddof=1)


def save_series(x: np.ndarray, data_dir: Path, fig_dir: Path, filename: str, title: str) -> None:
    df = pd.DataFrame({"t": np.arange(len(x), dtype=int), "x": x})
    df.to_csv(data_dir / filename, index=False)

    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(df["t"], df["x"], lw=1.0)
    ax.set_title(title)
    ax.set_xlabel("t")
    ax.set_ylabel("x")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(fig_dir / filename.replace(".csv", ".png"), dpi=160)
    plt.close(fig)


def simulate_white_noise(n_total: int, sigma: float, rng: np.random.Generator) -> np.ndarray:
    return sigma * rng.standard_normal(n_total)


def simulate_ar(n_total: int, phi: list[float], sigma: float, rng: np.random.Generator) -> np.ndarray:
    p = len(phi)
    x = np.zeros(n_total)
    eps = sigma * rng.standard_normal(n_total)
    for t in range(p, n_total):
        x[t] = sum(phi[i] * x[t - i - 1] for i in range(p)) + eps[t]
    return x


def simulate_ma(n_total: int, theta: list[float], sigma: float, rng: np.random.Generator) -> np.ndarray:
    q = len(theta)
    eps = sigma * rng.standard_normal(n_total + q)
    x = np.zeros(n_total)
    for t in range(n_total):
        x[t] = eps[t + q] + sum(theta[j] * eps[t + q - j - 1] for j in range(q))
    return x


def simulate_arma(
    n_total: int,
    phi: list[float],
    theta: list[float],
    sigma: float,
    rng: np.random.Generator,
) -> np.ndarray:
    p = len(phi)
    q = len(theta)
    m = max(p, q)
    x = np.zeros(n_total)
    eps = sigma * rng.standard_normal(n_total + q + 1)
    for t in range(m, n_total):
        ar_part = sum(phi[i] * x[t - i - 1] for i in range(p))
        ma_part = sum(theta[j] * eps[t + q - j - 1] for j in range(q))
        x[t] = ar_part + eps[t + q] + ma_part
    return x


def simulate_arch(
    n_total: int,
    omega: float,
    alpha: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if omega <= 0:
        raise ValueError("omega deve essere positivo")
    if not (0 <= alpha < 1):
        raise ValueError("Per ARCH(1) stazionario serve 0 <= alpha < 1")

    x = np.zeros(n_total)
    sigma2 = np.zeros(n_total)
    z = rng.standard_normal(n_total)
    sigma2[0] = omega / (1.0 - alpha)
    x[0] = np.sqrt(sigma2[0]) * z[0]

    for t in range(1, n_total):
        sigma2[t] = omega + alpha * x[t - 1] ** 2
        x[t] = np.sqrt(sigma2[t]) * z[t]
    return x


def simulate_garch(
    n_total: int,
    omega: float,
    alpha: float,
    beta: float,
    rng: np.random.Generator,
) -> np.ndarray:
    if omega <= 0:
        raise ValueError("omega deve essere positivo")
    if alpha < 0 or beta < 0 or alpha + beta >= 1:
        raise ValueError("Per GARCH(1,1) stazionario serve alpha >= 0, beta >= 0, alpha + beta < 1")

    x = np.zeros(n_total)
    sigma2 = np.zeros(n_total)
    z = rng.standard_normal(n_total)
    sigma2[0] = omega / (1.0 - alpha - beta)
    x[0] = np.sqrt(sigma2[0]) * z[0]

    for t in range(1, n_total):
        sigma2[t] = omega + alpha * x[t - 1] ** 2 + beta * sigma2[t - 1]
        x[t] = np.sqrt(sigma2[t]) * z[t]
    return x


def simulate_gjr_garch(
    n_total: int,
    omega: float,
    alpha: float,
    gamma: float,
    beta: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    GJR-GARCH schematico:

        x_t = sigma_t z_t
        sigma_t^2 = omega + alpha x_{t-1}^2
                    + gamma x_{t-1}^2 1_{x_{t-1}<0}
                    + beta sigma_{t-1}^2

    Per innovazioni gaussiane simmetriche, una condizione sufficiente di stazionarietà
    debole è alpha + beta + gamma/2 < 1.
    """
    if omega <= 0:
        raise ValueError("omega deve essere positivo")
    if alpha < 0 or gamma < 0 or beta < 0 or alpha + beta + 0.5 * gamma >= 1:
        raise ValueError("Per questa parametrizzazione serve alpha + beta + gamma/2 < 1")

    x = np.zeros(n_total)
    sigma2 = np.zeros(n_total)
    z = rng.standard_normal(n_total)
    sigma2[0] = omega / (1.0 - alpha - beta - 0.5 * gamma)
    x[0] = np.sqrt(sigma2[0]) * z[0]

    for t in range(1, n_total):
        indicator = 1.0 if x[t - 1] < 0 else 0.0
        sigma2[t] = (
            omega
            + alpha * x[t - 1] ** 2
            + gamma * x[t - 1] ** 2 * indicator
            + beta * sigma2[t - 1]
        )
        x[t] = np.sqrt(sigma2[t]) * z[t]
    return x


def generate_all(outdir: Path, seed: int, n: int, burnin: int, standardize: bool) -> None:
    rng = np.random.default_rng(seed)
    data_dir, fig_dir = ensure_dirs(outdir)
    n_total = n + burnin

    series: list[tuple[str, np.ndarray, SeriesMetadata]] = []

    x = simulate_white_noise(n_total, sigma=1.0, rng=rng)[burnin:]
    series.append((
        "serie_01.csv",
        x,
        SeriesMetadata(
            file="serie_01.csv",
            label="Serie 01",
            model="Rumore bianco gaussiano",
            parameters="sigma=1.0",
            comment="Controllo nullo: nessuna memoria nella media o nella varianza.",
        ),
    ))

    x = simulate_ar(n_total, phi=[0.75], sigma=1.0, rng=rng)[burnin:]
    series.append((
        "serie_02.csv",
        x,
        SeriesMetadata(
            file="serie_02.csv",
            label="Serie 02",
            model="AR(1)",
            parameters="phi=0.75, sigma=1.0",
            comment="Persistenza positiva; ACF attesa con decadimento positivo.",
        ),
    ))

    x = simulate_ar(n_total, phi=[-0.65], sigma=1.0, rng=rng)[burnin:]
    series.append((
        "serie_03.csv",
        x,
        SeriesMetadata(
            file="serie_03.csv",
            label="Serie 03",
            model="AR(1)",
            parameters="phi=-0.65, sigma=1.0",
            comment="Persistenza negativa; ACF attesa con alternanza di segno.",
        ),
    ))

    x = simulate_ma(n_total, theta=[0.70], sigma=1.0, rng=rng)[burnin:]
    series.append((
        "serie_04.csv",
        x,
        SeriesMetadata(
            file="serie_04.csv",
            label="Serie 04",
            model="MA(1)",
            parameters="theta=0.70, sigma=1.0",
            comment="Memoria breve negli shock; ACF teoricamente troncata dopo lag 1.",
        ),
    ))

    x = simulate_arma(n_total, phi=[0.60], theta=[-0.45], sigma=1.0, rng=rng)[burnin:]
    series.append((
        "serie_05.csv",
        x,
        SeriesMetadata(
            file="serie_05.csv",
            label="Serie 05",
            model="ARMA(1,1)",
            parameters="phi=0.60, theta=-0.45, sigma=1.0",
            comment="Memoria mista: persistenza dello stato e degli shock.",
        ),
    ))

    x = simulate_arch(n_total, omega=0.20, alpha=0.70, rng=rng)[burnin:]
    series.append((
        "serie_06.csv",
        x,
        SeriesMetadata(
            file="serie_06.csv",
            label="Serie 06",
            model="ARCH(1)",
            parameters="omega=0.20, alpha=0.70",
            comment="Media non prevedibile, ma varianza condizionata dipendente dallo shock passato.",
        ),
    ))

    x = simulate_garch(n_total, omega=0.05, alpha=0.10, beta=0.86, rng=rng)[burnin:]
    series.append((
        "serie_07.csv",
        x,
        SeriesMetadata(
            file="serie_07.csv",
            label="Serie 07",
            model="GARCH(1,1)",
            parameters="omega=0.05, alpha=0.10, beta=0.86",
            comment="Volatilità persistente; alpha+beta=0.96.",
        ),
    ))

    x = simulate_gjr_garch(n_total, omega=0.05, alpha=0.06, gamma=0.16, beta=0.84, rng=rng)[burnin:]
    series.append((
        "serie_08.csv",
        x,
        SeriesMetadata(
            file="serie_08.csv",
            label="Serie 08",
            model="GJR-GARCH(1,1) asimmetrico",
            parameters="omega=0.05, alpha=0.06, gamma=0.16, beta=0.84",
            comment="Volatilità asimmetrica: shock negativi aumentano maggiormente la varianza futura.",
        ),
    ))

    metadata: list[SeriesMetadata] = []
    for filename, x, meta in series:
        x_out = standardise(x) if standardize else x
        save_series(x_out, data_dir, fig_dir, filename, title=meta.label)
        metadata.append(meta)

    pd.DataFrame([asdict(m) for m in metadata]).to_csv(
        data_dir / "soluzioni_generative.csv",
        index=False,
    )

    readme = outdir / "README_lab08_dati.md"
    readme.write_text(
        "# Dati sintetici per laboratorio ARMA/GARCH\n\n"
        "Questa cartella contiene serie temporali sintetiche generate da modelli noti.\n\n"
        "## File prodotti\n\n"
        "- `data/serie_01.csv` ... `data/serie_08.csv`: serie anonime da assegnare agli studenti.\n"
        "- `data/soluzioni_generative.csv`: modello generatore e parametri, da tenere per il docente.\n"
        "- `figures/serie_01.png` ... `figures/serie_08.png`: grafici rapidi di controllo.\n\n"
        "Ogni serie contiene due colonne: `t` e `x`.\n\n"
        "## Nota\n\n"
        "Le serie sono standardizzate per default, in modo che scala e varianza empirica non rivelino troppo facilmente il modello.\n"
        "Per disattivare la standardizzazione usare `--no-standardize`.\n",
        encoding="utf-8",
    )

    print(f"Creati dati in: {data_dir}")
    print(f"Create figure in: {fig_dir}")
    print(f"Soluzioni docente: {data_dir / 'soluzioni_generative.csv'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera serie sintetiche ARMA/ARCH/GARCH per laboratorio.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("lab08_serie_temporali"),
        help="Directory di output. Default: lab08_serie_temporali",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=20260504,
        help="Seed del generatore casuale. Default: 20260504",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1200,
        help="Lunghezza finale di ciascuna serie. Default: 1200",
    )
    parser.add_argument(
        "--burnin",
        type=int,
        default=300,
        help="Osservazioni iniziali scartate. Default: 300",
    )
    parser.add_argument(
        "--no-standardize",
        action="store_true",
        help="Non standardizza le serie in uscita.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_all(
        outdir=args.outdir,
        seed=args.seed,
        n=args.n,
        burnin=args.burnin,
        standardize=not args.no_standardize,
    )


if __name__ == "__main__":
    main()
