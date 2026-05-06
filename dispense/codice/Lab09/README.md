# Dati sintetici per laboratorio ARMA/GARCH

Questa cartella contiene serie temporali sintetiche generate da modelli noti.

## File prodotti

- `data/serie_01.csv` ... `data/serie_10.csv`: serie anonime da assegnare agli studenti.
- `data/soluzioni_generative.csv`: modello generatore e parametri, da tenere per il docente.
- `figures/serie_01.png` ... `figures/serie_10.png`: grafici rapidi di controllo.

Ogni serie contiene due colonne: `t` e `x`.

## Note

Le serie da 01 a 08 sono stazionarie e vengono standardizzate per default,
in modo che scala e varianza empirica non rivelino troppo facilmente il modello.

Le serie 09 e 10 sono non stazionarie (random walk e random walk con drift)
e NON vengono standardizzate, anche se il flag globale --standardize e' attivo:
una standardizzazione globale di una serie non stazionaria nasconderebbe
proprio il segnale (varianza crescente, drift) che la diagnostica
valori-vs-incrementi della Parte 1bis deve identificare.

Per disattivare la standardizzazione anche sulle serie stazionarie usare `--no-standardize`.
