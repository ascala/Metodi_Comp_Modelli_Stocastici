# Lab08 -- Analisi di serie stocastiche: ARMA, ARCH e GARCH

Questa cartella contiene dati sintetici e codice Python per il laboratorio sulle serie temporali stocastiche.

## Struttura

```text
Lab08/
├── data/
│   ├── serie_01.csv
│   ├── ...
│   ├── serie_08.csv
│   └── soluzioni_generative.csv
├── diagnostics.py
├── figures/
│   ├── serie_01.png
│   ├── ...
│   └── serie_08.png
├── fit_models.py
├── main.py
├── requirements.txt
└── output/                 # generata quando si esegue main.py
```

## Installazione

Dalla cartella `Lab08/`:

```bash
pip install -r requirements.txt
```

## Esecuzione

Dalla cartella `Lab08/`:

```bash
python main.py
```

Per cambiare serie, aprire `main.py` e modificare:

```python
DATA_FILE = "data/serie_01.csv"
OUTPUT_DIR = "output/serie_01"
```

Per esempio, per analizzare `serie_04.csv`:

```python
DATA_FILE = "data/serie_04.csv"
OUTPUT_DIR = "output/serie_04"
```

## File dati

Ogni serie ha due colonne:

```text
t,x
```

- `t` è l'indice temporale;
- `x` è il valore osservato.

Il file `data/soluzioni_generative.csv` contiene il modello generatore e i parametri delle serie. È una chiave docente e non dovrebbe essere usato dagli studenti durante l'analisi.

## Output

Lo script crea una cartella `output/serie_XX/` con:

- diagnostica della serie osservata: serie, istogramma, QQ-plot, ACF, PACF, ACF dei quadrati;
- diagnostica dei residui ARMA;
- diagnostica dei residui standardizzati ARCH;
- diagnostica dei residui standardizzati GARCH.

## Nota

Il laboratorio non usa librerie specializzate come `statsmodels` o `arch`, perché l'obiettivo è vedere esplicitamente come si costruiscono residui, varianze condizionate e log-likelihood.
