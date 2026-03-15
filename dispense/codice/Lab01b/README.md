# README.md

## Laboratorio -- Richiami di metodi numerici (2 ore)

Questa cartella contiene tre script Python essenziali, pensati per mostrare:
- robustezza vs velocità nella ricerca di zeri (Newton vs bisezione);
- dipendenza dall’inizializzazione in ottimizzazione non convessa (single-start vs multi-start);
- vincoli "box" e soluzioni sul bordo (penalità vs proiezione).

### Requisiti
- Python 3.x
- numpy
- matplotlib

### Esecuzione
Da terminale:

- `python 01_zero_newton_vs_bisection.py`
- `python 02_minimi_two_basins_multistart.py`
- `python 03_box_constraint_penalty_vs_projection.py`

Ogni script stampa una diagnostica minima e mostra una figura.
