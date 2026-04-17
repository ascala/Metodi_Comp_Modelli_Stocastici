# Supporto tecnico rivisto per LAB06

Questa cartella contiene file Python di supporto per il laboratorio su:

- random walk continuo nel tempo su griglia 1D;
- master equation;
- passaggio da dinamica discreta a drift e diffusione;
- drift-diffusion continua e Fokker--Planck elementare;
- formulazione sparsa del generatore;
- confronto tra diversi propagatori numerici.

Questi file **non sostituiscono** il testo del laboratorio.
Servono come supporto tecnico per evitare di perdere tempo su dettagli implementativi non essenziali.

## Novità di questa revisione

Questa versione è allineata alla versione aggiornata di LAB06 in cui:

- il passo spaziale `dx` entra esplicitamente nel raccordo discreto--continuo;
- si distinguono chiaramente:
  - `i0` = indice del sito iniziale discreto;
  - `x0` = posizione fisica iniziale;
- i parametri continui efficaci vengono letti dal modello discreto:
  - `v = (r - ell) * dx`
  - `D = 0.5 * (r + ell) * dx**2`
- il confronto tra dinamica discreta e Fokker--Planck continua è illustrato anche nei demo.

## Librerie richieste

I file usano principalmente:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.sparse import diags, csr_matrix
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import expm
```

## Installazione minima

```bash
pip install numpy matplotlib scipy
```

## Struttura dei file

### Blocco base

- `rw_continuous_time.py` -- simulazione di una traiettoria del random walk continuo nel tempo
- `sample_positions_at_times.py` -- estrazione della posizione a tempi fissati da molte traiettorie
- `histogram_positions.py` -- costruzione di istogrammi della posizione
- `grid_utils.py` -- conversione sito \leftrightarrow coordinata fisica
- `build_generator_dense.py` -- costruzione del generatore tridiagonale in forma densa
- `integrate_master_equation.py` -- integrazione numerica della master equation
- `drift_diffusion_sde.py` -- simulazione della SDE continua di drift-diffusion
- `gaussian_theory.py` -- densità teorica gaussiana, media e varianza teoriche, parametri efficaci

### Blocco aggiuntivo

- `build_generator_sparse.py` -- costruzione del generatore in formato sparso
- `split_generator.py` -- decomposizione del generatore in parte di drift e parte diffusiva
- `euler_propagator.py` -- evoluzione numerica con Euler esplicito
- `splitting_propagator.py` -- evoluzione con operator splitting
- `full_propagator.py` -- evoluzione tramite propagatore completo

## Demo inclusi

Nella cartella `examples/` sono presenti tre script completi:

- `demo_discrete_pipeline.py` -- simula traiettorie discrete, campiona le posizioni a tempi fissati, costruisce istogrammi, integra la master equation e sovrappone la gaussiana continua efficace;
- `demo_propagators.py` -- confronta Euler, operator splitting e full propagator sullo stesso dato iniziale;
- `demo_continuous_drift_diffusion.py` -- simula la SDE continua e confronta l'istogramma con la gaussiana teorica.

## Ordine consigliato d'uso

1. `rw_continuous_time.py`
2. `sample_positions_at_times.py`
3. `histogram_positions.py`
4. `grid_utils.py`
5. `build_generator_dense.py`
6. `integrate_master_equation.py`
7. `drift_diffusion_sde.py`
8. `gaussian_theory.py`
9. `build_generator_sparse.py`
10. `split_generator.py`
11. `euler_propagator.py`
12. `splitting_propagator.py`
13. `full_propagator.py`

## Convenzioni usate

- `build_...` per funzioni che costruiscono operatori o matrici;
- `simulate_...` per funzioni che simulano traiettorie;
- `integrate_...` per funzioni che evolvono sistemi differenziali;
- `..._theory` per formule teoriche;
- `..._propagator` per metodi di evoluzione basati sul generatore.

## Verifiche utili nel laboratorio

Quando confrontate risultati teorici e simulazioni:

- una singola traiettoria non va confrontata direttamente con una pdf;
- gli istogrammi vanno costruiti su un numero sufficientemente grande di realizzazioni;
- nella master equation conviene sempre controllare:
  - normalizzazione;
  - non negatività;
  - sensibilità rispetto al passo temporale;
- nel raccordo discreto--continuo conviene controllare:
  - coerenza tra asse dei siti e asse fisico;
  - coerenza tra `i0` e `x0 = i0 * dx`;
  - uso corretto di `v` e `D`.
