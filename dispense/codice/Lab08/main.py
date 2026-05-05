"""
main.py

File principale del laboratorio.

Questo file deve rimanere semplice: serve solo a scegliere una serie,
chiamare le funzioni di diagnostica, stimare alcuni modelli e salvare i risultati.

Gli studenti dovrebbero modificare soprattutto:

1. DATA_FILE
2. OUTPUT_DIR
3. ARMA_P, ARMA_Q
4. quali modelli provare
5. il commento interpretativo finale nella relazione

Esecuzione dalla cartella principale del laboratorio:

    python src/main.py
"""

import numpy as np

from diagnostics import (
    read_series_csv,
    make_output_dir,
    plot_series,
    plot_histogram_with_gaussian,
    plot_acf,
    plot_pacf,
    plot_qq_gaussian,
    residual_diagnostics,
)

from fit_models import (
    fit_arma_mle,
    fit_arch1_mle,
    fit_garch11_mle,
)


# ============================================================
# 1. Scelta del file da analizzare
# ============================================================

# Cambiare questo nome per analizzare un'altra serie.
DATA_FILE = "data/serie_08.csv"

# Cartella dove verranno salvati grafici e report.
OUTPUT_DIR = "output/serie_08"


# ============================================================
# 2. Scelta dei modelli da provare
# ============================================================

# Modello ARMA(p,q) da stimare.
# Esempi:
#   AR(1)       -> p=1, q=0
#   MA(1)       -> p=0, q=1
#   ARMA(1,1)   -> p=1, q=1
ARMA_P = 1
ARMA_Q = 0

# Provare anche modelli per varianza condizionata?
TRY_ARCH = True
TRY_GARCH = True


def run_raw_diagnostics(t, x, output_dir):
    """
    Diagnostica della serie osservata.

    Questa diagnostica va fatta una sola volta per ogni serie, prima di stimare
    qualunque modello. I modelli cambiano i residui, non la serie osservata.
    """

    plot_series(
        t,
        x,
        output_dir / "raw_serie.png",
        title="Serie osservata",
    )

    plot_histogram_with_gaussian(
        x,
        output_dir / "raw_istogramma.png",
        title="Istogramma della serie e gaussiana stimata",
    )

    plot_qq_gaussian(
        x,
        output_dir / "raw_qqplot.png",
        title="QQ-plot della serie contro gaussiana",
    )

    plot_acf(
        x,
        output_dir / "raw_acf.png",
        max_lag=40,
        title="ACF della serie",
    )

    plot_pacf(
        x,
        output_dir / "raw_pacf.png",
        max_lag=40,
        title="PACF della serie",
    )

    plot_acf(
        x**2,
        output_dir / "raw_acf_quadrati.png",
        max_lag=40,
        title="ACF dei quadrati della serie",
    )


def main():
    # --------------------------------------------------------
    # Creazione cartella di output
    # --------------------------------------------------------

    output_dir = make_output_dir(OUTPUT_DIR)

    # --------------------------------------------------------
    # Lettura della serie
    # --------------------------------------------------------

    t, x = read_series_csv(DATA_FILE)

    print("\n==========================================")
    print("Analisi della serie")
    print("==========================================")
    print(f"file: {DATA_FILE}")
    print(f"numero osservazioni: {len(x)}")
    print(f"media campionaria:    {np.mean(x): .4f}")
    print(f"varianza campionaria: {np.var(x, ddof=1): .4f}")

    # --------------------------------------------------------
    # Diagnostica preliminare della serie osservata
    # --------------------------------------------------------
    # Qui non stimiamo ancora nessun modello.
    # Guardiamo solo la serie, la distribuzione marginale,
    # la memoria temporale nei valori e la memoria nei quadrati.
    #
    # I file prodotti hanno prefisso raw_, perché si riferiscono ai dati grezzi.

    run_raw_diagnostics(t, x, output_dir)

    # --------------------------------------------------------
    # Fit ARMA gaussiano
    # --------------------------------------------------------
    # Un modello ARMA cerca di spiegare la dipendenza nella media:
    #
    #   X_t = c + termini AR + innovazione + termini MA.
    #
    # Dopo il fit, i residui dovrebbero assomigliare a rumore bianco.

    print("\n==========================================")
    print(f"Fit ARMA({ARMA_P},{ARMA_Q}) gaussiano")
    print("==========================================")

    arma = fit_arma_mle(x, p=ARMA_P, q=ARMA_Q, include_constant=True)
    print(arma["summary"])

    # Per ARMA i residui sono residui della previsione della media.
    residual_diagnostics(
        arma["residuals"],
        output_dir=output_dir,
        prefix="arma",
        title_prefix=f"ARMA({ARMA_P},{ARMA_Q}), residui",
    )

    # --------------------------------------------------------
    # Fit ARCH(1)
    # --------------------------------------------------------
    # Un modello ARCH cerca di spiegare memoria nella varianza.
    # Qui la media viene modellata solo con una costante.
    #
    # Dopo il fit, la diagnostica va fatta sui residui standardizzati:
    #
    #   z_t = eps_t / sigma_t.

    if TRY_ARCH:
        print("\n==========================================")
        print("Fit ARCH(1) gaussiano")
        print("==========================================")

        arch = fit_arch1_mle(x)
        print(arch["summary"])

        residual_diagnostics(
            arch["standardized_residuals"],
            output_dir=output_dir,
            prefix="arch_standardized",
            title_prefix="ARCH(1), residui standardizzati",
        )

    # --------------------------------------------------------
    # Fit GARCH(1,1)
    # --------------------------------------------------------
    # Un modello GARCH introduce persistenza nella varianza:
    #
    #   sigma_t^2 = omega + alpha eps_{t-1}^2 + beta sigma_{t-1}^2.
    #
    # Se alpha + beta è vicino a 1, la volatilità è molto persistente.
    # Anche qui la diagnostica va fatta sui residui standardizzati.

    if TRY_GARCH:
        print("\n==========================================")
        print("Fit GARCH(1,1) gaussiano")
        print("==========================================")

        garch = fit_garch11_mle(x)
        print(garch["summary"])

        residual_diagnostics(
            garch["standardized_residuals"],
            output_dir=output_dir,
            prefix="garch_standardized",
            title_prefix="GARCH(1,1), residui standardizzati",
        )

    # --------------------------------------------------------
    # Domande per la relazione
    # --------------------------------------------------------

    print("\n==========================================")
    print("Domande per la relazione")
    print("==========================================")
    print("1. La serie mostra autocorrelazione nei valori?")
    print("2. La serie mostra autocorrelazione nei quadrati?")
    print("3. Un modello ARMA sembra sufficiente?")
    print("4. Un modello ARCH/GARCH migliora la diagnostica?")
    print("5. Dopo la stima, i residui sembrano rumore bianco?")
    print("6. Che cosa resta non spiegato dal modello?")
    print(f"\nOutput salvato in: {output_dir}")


if __name__ == "__main__":
    main()
