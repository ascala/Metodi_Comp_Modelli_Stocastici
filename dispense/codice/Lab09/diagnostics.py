"""
diagnostics.py

Funzioni per analizzare una serie temporale e i residui di un modello.

Contiene:

- lettura dei CSV;
- grafico della serie;
- istogramma con gaussiana stimata;
- ACF;
- PACF;
- QQ-plot;
- diagnostica dei residui.

Anche questo file è volutamente didattico: molte funzioni sono scritte in modo
esplicito, invece di usare librerie specializzate.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2


# ============================================================
# File e array
# ============================================================


def make_output_dir(path):
    """Crea una cartella se non esiste e restituisce un oggetto Path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_series_csv(filename):
    """
    Legge una serie temporale da CSV.

    Il file deve contenere due colonne:

        t, x

    Restituisce:

        t: array dei tempi
        x: array dei valori osservati
    """
    df = pd.read_csv(filename)

    if "t" not in df.columns or "x" not in df.columns:
        raise ValueError("Il file CSV deve contenere le colonne 't' e 'x'.")

    t = df["t"].to_numpy()
    x = df["x"].to_numpy(dtype=float)

    if np.any(~np.isfinite(x)):
        raise ValueError("La serie contiene NaN o inf.")

    return t, x


def remove_nan_and_inf(x):
    """
    Rimuove valori NaN e infiniti.

    Serve soprattutto per i residui ARMA, perché i primi valori possono essere NaN:
    per quei tempi non c'è abbastanza passato per calcolare la previsione.
    """
    x = np.asarray(x, dtype=float)
    return x[np.isfinite(x)]


# ============================================================
# Autocorrelazione
# ============================================================


def acf(x, max_lag=40):
    """
    Calcola l'autocorrelazione campionaria normalizzata.

    Definizione empirica:

        C(k) = sum_t (x_t - mean)(x_{t+k} - mean)

    Poi normalizziamo dividendo per C(0).

    L'ACF misura memoria lineare:
    se ACF(k) è grande, conoscere x_t aiuta a prevedere x_{t+k}.
    """
    x = remove_nan_and_inf(x)
    x = x - np.mean(x)

    n = len(x)
    denominator = np.sum(x**2)

    values = np.zeros(max_lag + 1)

    for k in range(max_lag + 1):
        numerator = np.sum(x[:n-k] * x[k:])
        values[k] = numerator / denominator

    return values


def pacf_ols(x, max_lag=40):
    """
    Stima semplice della PACF tramite regressioni lineari.

    La PACF al lag k misura il contributo di x_{t-k} nel prevedere x_t
    dopo aver già tenuto conto dei lag intermedi.

    Procedura:

    per ogni k, stimiamo la regressione

        x_t = b_1 x_{t-1} + ... + b_k x_{t-k} + errore_t

    e prendiamo b_k come PACF(k).
    """
    x = remove_nan_and_inf(x)
    x = x - np.mean(x)

    n = len(x)
    values = np.zeros(max_lag + 1)
    values[0] = 1.0

    for k in range(1, max_lag + 1):
        y = x[k:]

        # Matrice dei regressori laggati.
        # Colonna 1: x_{t-1}
        # Colonna 2: x_{t-2}
        # ...
        # Colonna k: x_{t-k}
        X = np.column_stack([
            x[k-j:n-j]
            for j in range(1, k + 1)
        ])

        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        values[k] = beta[-1]

    return values


def ljung_box_test(x, max_lag=20):
    """
    Test di Ljung-Box in forma semplice.

    Ipotesi nulla:
        autocorrelazioni fino al lag max_lag circa nulle.

    Se il p-value è piccolo, resta autocorrelazione significativa.

    Nota:
    questo è un test approssimato e didattico. Nel laboratorio ci interessa
    soprattutto come indicatore diagnostico.
    """
    x = remove_nan_and_inf(x)
    n = len(x)
    rho = acf(x, max_lag=max_lag)

    Q = 0.0

    for k in range(1, max_lag + 1):
        Q += rho[k] ** 2 / (n - k)

    Q *= n * (n + 2)

    p_value = 1.0 - chi2.cdf(Q, df=max_lag)

    return Q, p_value


# ============================================================
# Grafici base
# ============================================================


def plot_series(t, x, filename, title="Serie temporale"):
    """Grafico della serie nel tempo."""
    fig, ax = plt.subplots(figsize=(9, 3.2))

    ax.plot(t, x, linewidth=1.0)
    ax.set_title(title)
    ax.set_xlabel("t")
    ax.set_ylabel("x")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def plot_histogram_with_gaussian(x, filename, title="Istogramma", bins=40):
    """
    Istogramma empirico con gaussiana avente stessa media e varianza.

    Serve a controllare in modo visuale:
    - simmetria;
    - code pesanti;
    - presenza di outlier;
    - deviazioni dalla gaussianità.
    """
    x = remove_nan_and_inf(x)

    mu = np.mean(x)
    sigma = np.std(x, ddof=1)

    grid = np.linspace(np.min(x), np.max(x), 400)
    gaussian_density = norm.pdf(grid, loc=mu, scale=sigma)

    fig, ax = plt.subplots(figsize=(6.5, 4.0))

    ax.hist(x, bins=bins, density=True, alpha=0.65, label="dati")
    ax.plot(grid, gaussian_density, linewidth=2.0, label="gaussiana stimata")

    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("densità")
    ax.legend()
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def plot_acf(x, filename, max_lag=40, title="ACF"):
    """Grafico dell'autocorrelazione."""
    x = remove_nan_and_inf(x)
    values = acf(x, max_lag=max_lag)
    lags = np.arange(max_lag + 1)

    # Banda indicativa per rumore bianco.
    # Circa 95%: +/- 1.96/sqrt(n).
    n = len(x)
    band = 1.96 / np.sqrt(n)

    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    ax.axhline(0.0, linewidth=1.0)
    ax.axhline(band, linestyle="--", linewidth=1.0)
    ax.axhline(-band, linestyle="--", linewidth=1.0)

    ax.vlines(lags, 0.0, values, linewidth=1.5)
    ax.scatter(lags, values, s=18)

    ax.set_title(title)
    ax.set_xlabel("lag")
    ax.set_ylabel("ACF")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def plot_pacf(x, filename, max_lag=40, title="PACF"):
    """Grafico della partial autocorrelation function."""
    x = remove_nan_and_inf(x)
    values = pacf_ols(x, max_lag=max_lag)
    lags = np.arange(max_lag + 1)

    n = len(x)
    band = 1.96 / np.sqrt(n)

    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    ax.axhline(0.0, linewidth=1.0)
    ax.axhline(band, linestyle="--", linewidth=1.0)
    ax.axhline(-band, linestyle="--", linewidth=1.0)

    ax.vlines(lags, 0.0, values, linewidth=1.5)
    ax.scatter(lags, values, s=18)

    ax.set_title(title)
    ax.set_xlabel("lag")
    ax.set_ylabel("PACF")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


def plot_qq_gaussian(x, filename, title="QQ-plot gaussiano"):
    """
    QQ-plot contro una gaussiana.

    Procedura:
    1. standardizziamo i dati;
    2. ordiniamo i valori osservati;
    3. calcoliamo i quantili teorici gaussiani;
    4. confrontiamo punti empirici e retta y=x.

    Lettura:
    - punti vicini alla retta: compatibilità qualitativa con gaussianità;
    - deviazioni nelle code: code più pesanti o più leggere;
    - curvatura sistematica: asimmetria o distribuzione non gaussiana.
    """
    x = remove_nan_and_inf(x)

    z = (x - np.mean(x)) / np.std(x, ddof=1)
    z_sorted = np.sort(z)

    n = len(z_sorted)
    probabilities = (np.arange(1, n + 1) - 0.5) / n
    theoretical_quantiles = norm.ppf(probabilities)

    fig, ax = plt.subplots(figsize=(5.0, 5.0))

    ax.scatter(theoretical_quantiles, z_sorted, s=12, alpha=0.75)

    lower = min(np.min(theoretical_quantiles), np.min(z_sorted))
    upper = max(np.max(theoretical_quantiles), np.max(z_sorted))
    ax.plot([lower, upper], [lower, upper], linewidth=1.5)

    ax.set_title(title)
    ax.set_xlabel("quantili gaussiani teorici")
    ax.set_ylabel("quantili empirici standardizzati")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)


# ============================================================
# Momenti empirici
# ============================================================


def sample_skewness(x):
    """Skewness empirica. Per una gaussiana simmetrica vale circa 0."""
    x = remove_nan_and_inf(x)
    z = (x - np.mean(x)) / np.std(x, ddof=1)
    return np.mean(z**3)


def sample_kurtosis(x):
    """
    Kurtosis empirica non-excess.

    Per una gaussiana vale circa 3.
    Valori molto maggiori di 3 indicano code pesanti o outlier.
    """
    x = remove_nan_and_inf(x)
    z = (x - np.mean(x)) / np.std(x, ddof=1)
    return np.mean(z**4)


# ============================================================
# Diagnostica dei residui
# ============================================================


def residual_diagnostics(residuals, output_dir, prefix="resid", title_prefix="Residui"):
    """
    Produce diagnostica completa dei residui.

    Salva:
    - serie dei residui;
    - istogramma;
    - QQ-plot;
    - ACF dei residui;
    - ACF dei residui quadrati;
    - report testuale.

    Interpretazione:

    1. Residui autocorrelati:
       il modello non ha catturato tutta la memoria nella media.

    2. Quadrati dei residui autocorrelati:
       il modello non ha catturato tutta la memoria nella varianza.

    3. QQ-plot non lineare:
       l'ipotesi gaussiana è discutibile.

    4. Media dei residui lontana da zero:
       la previsione condizionata è mal centrata.
    """
    output_dir = make_output_dir(output_dir)
    r = remove_nan_and_inf(residuals)
    t = np.arange(len(r))

    plot_series(
        t,
        r,
        output_dir / f"{prefix}_residui.png",
        title=f"{title_prefix}: residui nel tempo",
    )

    plot_histogram_with_gaussian(
        r,
        output_dir / f"{prefix}_istogramma.png",
        title=f"{title_prefix}: istogramma",
    )

    plot_qq_gaussian(
        r,
        output_dir / f"{prefix}_qqplot.png",
        title=f"{title_prefix}: QQ-plot gaussiano",
    )

    plot_acf(
        r,
        output_dir / f"{prefix}_acf_residui.png",
        max_lag=40,
        title=f"{title_prefix}: ACF residui",
    )

    plot_acf(
        r**2,
        output_dir / f"{prefix}_acf_residui_quadrati.png",
        max_lag=40,
        title=f"{title_prefix}: ACF residui quadrati",
    )

    q_res, p_res = ljung_box_test(r, max_lag=20)
    q_sq, p_sq = ljung_box_test(r**2, max_lag=20)

    report_lines = []
    report_lines.append(title_prefix)
    report_lines.append("=" * len(title_prefix))
    report_lines.append("")
    report_lines.append(f"numero residui validi: {len(r)}")
    report_lines.append(f"media:                {np.mean(r): .6f}")
    report_lines.append(f"varianza:             {np.var(r, ddof=1): .6f}")
    report_lines.append(f"skewness:             {sample_skewness(r): .6f}")
    report_lines.append(f"kurtosis:             {sample_kurtosis(r): .6f}")
    report_lines.append("")
    report_lines.append("Ljung-Box sui residui")
    report_lines.append(f"Q = {q_res:.4f}")
    report_lines.append(f"p-value = {p_res:.4f}")
    report_lines.append("")
    report_lines.append("Ljung-Box sui residui quadrati")
    report_lines.append(f"Q = {q_sq:.4f}")
    report_lines.append(f"p-value = {p_sq:.4f}")
    report_lines.append("")
    report_lines.append("Lettura qualitativa")
    report_lines.append("- p-value piccolo sui residui: resta memoria lineare.")
    report_lines.append("- p-value piccolo sui residui quadrati: resta memoria nella varianza.")
    report_lines.append("- kurtosis molto maggiore di 3: code pesanti o outlier.")
    report_lines.append("- QQ-plot curvo nelle code: ipotesi gaussiana discutibile.")

    text = "\n".join(report_lines)

    report_file = output_dir / f"{prefix}_report.txt"
    report_file.write_text(text, encoding="utf-8")

    print("\n" + text)
    
"""
diagnostics_addons.py

Funzioni aggiuntive da incollare in fondo a `diagnostics.py`.

Servono per la diagnostica della Parte 1bis del laboratorio:
decidere se lavorare sulla serie originale o sui suoi incrementi.

Le due funzioni sono:

- block_stats(x, K): media e varianza su K blocchi consecutivi;
- plot_block_stats(x, filename, K, title): grafico delle stesse, fianco a fianco.

Una varianza che cresce sistematicamente tra blocchi consecutivi e' un
sintomo forte di non stazionarieta'. Una serie stazionaria mostra invece
fluttuazioni delle varianze attorno a un valore costante.
"""

import numpy as np
import matplotlib.pyplot as plt


def block_stats(x, K=5):
    """
    Media e varianza campionaria su K blocchi consecutivi.

    Per una serie stazionaria, le varianze dei blocchi devono fluttuare
    attorno a un livello costante. Per un random walk, la varianza dei
    blocchi successivi cresce sistematicamente con il tempo.

    Restituisce (means, variances), entrambi array di lunghezza K.
    """
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]

    blocks = np.array_split(x, K)
    means = np.array([np.mean(b) for b in blocks])
    variances = np.array([np.var(b, ddof=1) for b in blocks])
    return means, variances


def plot_block_stats(x, filename, K=5, title="Statistiche per blocchi"):
    """
    Grafico affiancato di media e varianza per blocchi.

    Lettura:

    - barre approssimativamente uguali, oscillazioni casuali: serie stazionaria;
    - varianze che crescono sistematicamente con l'indice di blocco: random walk
      o piu' in generale processo non stazionario nei valori;
    - medie che derivano sistematicamente: trend o drift presente.

    Le linee tratteggiate orizzontali indicano la media globale dei valori
    riportati (media-delle-medie e media-delle-varianze).
    """
    means, variances = block_stats(x, K=K)
    block_indices = np.arange(1, K + 1)

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.6))

    axes[0].bar(block_indices, means, alpha=0.7, edgecolor="black")
    axes[0].axhline(np.mean(means), linestyle="--", linewidth=1.0)
    axes[0].set_title("Media per blocco")
    axes[0].set_xlabel("blocco")
    axes[0].set_ylabel("media campionaria")
    axes[0].grid(alpha=0.25)

    axes[1].bar(block_indices, variances, alpha=0.7, edgecolor="black")
    axes[1].axhline(np.mean(variances), linestyle="--", linewidth=1.0)
    axes[1].set_title("Varianza per blocco")
    axes[1].set_xlabel("blocco")
    axes[1].set_ylabel("varianza campionaria")
    axes[1].grid(alpha=0.25)

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(filename, dpi=160)
    plt.close(fig)
