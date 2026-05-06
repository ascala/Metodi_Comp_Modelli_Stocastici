"""
main.py

File principale del laboratorio.

Questo file deve rimanere semplice: serve solo a scegliere una serie,
chiamare le funzioni di diagnostica, stimare alcuni modelli e salvare i risultati.

Gli studenti dovrebbero modificare soprattutto:

1. DATA_FILE
2. OUTPUT_DIR
3. USE_INCREMENTS (vedi Parte 1bis)
4. ARMA_P, ARMA_Q
5. quali modelli provare
6. il commento interpretativo finale nella relazione

Esecuzione dalla cartella principale del laboratorio:

    python main.py
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
    plot_block_stats,
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
DATA_FILE = "data/serie_10.csv"

# Cartella dove verranno salvati grafici e report.
OUTPUT_DIR = "output/serie_10_increments"


# ============================================================
# 2. Valori o incrementi? (Parte 1bis del laboratorio)
# ============================================================
# La diagnostica grezza viene SEMPRE eseguita sui valori originali:
# e' guardando raw_serie.png, raw_acf.png e raw_block_stats.png che
# si decide se la serie e' stazionaria o meno.
#
# Se i segnali indicano non stazionarieta' (varianza crescente, drift,
# ACF che decade lentamente), impostare USE_INCREMENTS = True e ri-eseguire:
#
# - viene prodotta una seconda passata di diagnostica con prefisso inc_;
# - i modelli ARMA/ARCH/GARCH vengono stimati sugli incrementi
#   Delta x_t = x_{t+1} - x_t.
#
# ATTENZIONE: differenziare una serie gia' stazionaria introduce un MA(1)
# spurio (autocorrelazione negativa al lag 1). Non usare USE_INCREMENTS=True
# come default "di sicurezza".

USE_INCREMENTS = True


# ============================================================
# 3. Scelta dei modelli da provare
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


def run_raw_diagnostics(t, x, output_dir, prefix="raw", what="serie"):
    """
    Diagnostica della serie osservata o degli incrementi.

    Questa diagnostica non dipende da nessun modello stimato. Viene fatta
    una sola volta sui valori originali (prefix='raw') e, se richiesto dalla
    Parte 1bis, una seconda volta sugli incrementi (prefix='inc').

    Parametri:

    - prefix: prefisso dei file PNG ('raw' o 'inc');
    - what: descrizione testuale per i titoli ('serie', 'incrementi').
    """

    plot_series(
        t,
        x,
        output_dir / f"{prefix}_serie.png",
        title=f"{what.capitalize()} osservata" if prefix == "raw" else what.capitalize(),
    )

    plot_histogram_with_gaussian(
        x,
        output_dir / f"{prefix}_istogramma.png",
        title=f"Istogramma {what} e gaussiana stimata",
    )

    plot_qq_gaussian(
        x,
        output_dir / f"{prefix}_qqplot.png",
        title=f"QQ-plot {what} contro gaussiana",
    )

    plot_acf(
        x,
        output_dir / f"{prefix}_acf.png",
        max_lag=40,
        title=f"ACF {what}",
    )

    plot_pacf(
        x,
        output_dir / f"{prefix}_pacf.png",
        max_lag=40,
        title=f"PACF {what}",
    )

    plot_acf(
        x**2,
        output_dir / f"{prefix}_acf_quadrati.png",
        max_lag=40,
        title=f"ACF dei quadrati {what}",
    )

    plot_block_stats(
        x,
        output_dir / f"{prefix}_block_stats.png",
        K=5,
        title=f"Statistiche per blocchi: {what}",
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
    # Diagnostica preliminare sui valori (sempre eseguita)
    # --------------------------------------------------------
    # Qui non stimiamo ancora nessun modello. Guardiamo solo la serie,
    # la distribuzione marginale, la memoria temporale nei valori,
    # la memoria nei quadrati e la stabilita' di media e varianza
    # tra blocchi consecutivi.
    #
    # I file prodotti hanno prefisso raw_, perche' si riferiscono ai dati grezzi.

    run_raw_diagnostics(t, x, output_dir, prefix="raw", what="serie")

    # --------------------------------------------------------
    # Decisione: valori o incrementi?
    # --------------------------------------------------------
    # Vedi Parte 1bis del laboratorio. Esamina raw_serie.png, raw_acf.png
    # e raw_block_stats.png. Se la varianza dei blocchi cresce
    # sistematicamente, oppure l'ACF resta alta su molti lag, la serie
    # non e' stazionaria: imposta USE_INCREMENTS = True e ri-esegui.

    if USE_INCREMENTS:
        print("\n==========================================")
        print("Differenziazione attivata (Parte 1bis)")
        print("==========================================")
        print("USE_INCREMENTS = True: l'analisi modello procede sugli incrementi.")

        dx = np.diff(x)
        t_dx = t[1:]

        print(f"numero incrementi:       {len(dx)}")
        print(f"media degli incrementi:  {np.mean(dx): .6f}")
        print(f"std degli incrementi:    {np.std(dx, ddof=1): .6f}")
        print("Se |media| e' confrontabile con std/sqrt(n) la serie originale")
        print("e' compatibile con un random walk puro;")
        print("se |media| e' nettamente piu' grande c'e' drift deterministico.")

        run_raw_diagnostics(t_dx, dx, output_dir, prefix="inc", what="incrementi")
        series_for_models = dx
    else:
        series_for_models = x

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
    if USE_INCREMENTS:
        print("(stimato sugli incrementi)")
    print("==========================================")

    arma = fit_arma_mle(series_for_models, p=ARMA_P, q=ARMA_Q, include_constant=True)
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
        if USE_INCREMENTS:
            print("(stimato sugli incrementi)")
        print("==========================================")

        arch = fit_arch1_mle(series_for_models)
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
    # Se alpha + beta e' vicino a 1, la volatilita' e' molto persistente.
    # Anche qui la diagnostica va fatta sui residui standardizzati.

    if TRY_GARCH:
        print("\n==========================================")
        print("Fit GARCH(1,1) gaussiano")
        if USE_INCREMENTS:
            print("(stimato sugli incrementi)")
        print("==========================================")

        garch = fit_garch11_mle(series_for_models)
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
    print("0. La serie e' stazionaria nei valori? (Parte 1bis)")
    print("   Hai dovuto passare agli incrementi?")
    print("1. La serie mostra autocorrelazione nei valori?")
    print("2. La serie mostra autocorrelazione nei quadrati?")
    print("3. Un modello ARMA sembra sufficiente?")
    print("4. Un modello ARCH/GARCH migliora la diagnostica?")
    print("5. Dopo la stima, i residui sembrano rumore bianco?")
    print("6. Che cosa resta non spiegato dal modello?")
    print(f"\nOutput salvato in: {output_dir}")
    print(f"USE_INCREMENTS = {USE_INCREMENTS}")


if __name__ == "__main__":
    main()
