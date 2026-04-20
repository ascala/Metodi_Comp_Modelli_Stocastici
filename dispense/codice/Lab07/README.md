# LAB07 -- Branching, estinzione e funzione generatrice

Questa cartella contiene gli scheletri Python per il laboratorio LAB07.
Completate i file nell'ordine indicato, verificando ogni modulo prima di
passare al successivo.

## Struttura dei file

- `gw_core.py` -- campionamento dell'offspring e simulazione di una singola traiettoria
- `gw_simulation.py` -- simulazioni multiple e stime empiriche
- `gw_generating_function.py` -- funzione generatrice, iterazione del punto fisso, calcolo di $G^t(0)$
- `gw_plots.py` -- grafici essenziali

## Dipendenze tra i moduli

```
gw_core  <--  gw_simulation  <--  gw_plots
gw_generating_function       <--  gw_plots
```

`gw_plots` riceve array gia' calcolati: non importa direttamente da
`gw_simulation` o `gw_generating_function`, ma li usa chiamandoli
nello script principale.

## Come rinominare i file

I file distribuiti hanno il suffisso `_todo`. Quando completate un modulo,
rinominatelo togliendo il suffisso, ad esempio:

```
gw_core_todo.py  -->  gw_core.py
```

Aggiornate di conseguenza le righe `import` nei file che dipendono da esso.

## Ordine di lavoro consigliato

1. Completate e testate `gw_core.py`.
2. Completate `gw_simulation.py` (importa da `gw_core`).
3. Completate `gw_generating_function.py` (indipendente dagli altri).
4. Usate `gw_plots.py` per produrre i grafici richiesti nelle Parti A, B, C.
5. La Parte D (estensione facoltativa) non ha uno scheletro dedicato:
   potete aggiungere le funzioni in `gw_generating_function.py`.

## Verifica rapida

Dopo aver completato `gw_core.py`, controllate che:

```python
from gw_core import campiona_offspring, simula_traiettoria
import numpy as np

# deve restituire solo 0 e 2
print(np.unique(campiona_offspring(0.5, size=1000)))

# deve essere un array di lunghezza 21 con N[0] = 1
traj = simula_traiettoria(N0=1, T=20, p=0.7)
print(len(traj), traj[0])
```

Dopo aver completato `gw_generating_function.py`:

```python
from gw_generating_function import G, q_teorico, iterazione_punto_fisso

# deve valere 1.0
print(G(1.0, p=0.7))

# deve valere (1-0.7)/0.7 ~ 0.4286
print(q_teorico(0.7))

# deve convergere allo stesso valore
q, storia = iterazione_punto_fisso(p=0.7)
print(q)
```
