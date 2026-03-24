# LAB03 -- Dallo stimatore Monte Carlo ai metodi MCMC

Questa cartella contiene gli script di partenza per il laboratorio su **Monte Carlo diretto**, **Metropolis** e **MCMC**.

L'idea del laboratorio è confrontare diversi modi di stimare la stessa quantità

$$
\langle O\rangle_\pi
=
\frac{\int O(x)e^{-\beta E(x)}\,dx}{\int e^{-\beta E(x)}\,dx},
$$

e capire, in pratica, il ruolo di:

- campioni indipendenti vs campioni correlati;
- burn-in;
- correlazione temporale;
- scala della proposta;
- differenza tra correttezza teorica ed efficienza numerica.

## Struttura dei file

### `01_grid_vs_direct_mc.py`

Confronta due metodi già visti nel laboratorio precedente:

1. **integrazione numerica su griglia**;
2. **Monte Carlo diretto** con campioni indipendenti uniformi.

Obiettivo: verificare che entrambi stimino lo stesso valore di

$$
\langle O\rangle_\pi.
$$

Questo file è **quasi completo** e serve come riferimento di partenza.


### `02_metropolis_boltzmann.py`

Implementa l'algoritmo di **Metropolis** per un peso di Boltzmann

$$
\pi(x)\propto e^{-\beta E(x)}.
$$

Contiene due versioni equivalenti della probabilità di accettazione:

1. in termini del **rapporto tra pesi**;
2. in termini della **differenza di energia** $\Delta E$.

Obiettivo: verificare che le due versioni producano la stessa statistica e confrontarne il costo computazionale.

Anche questo file è **quasi completo**.


### `03_correlation_and_burnin.py`

Introduce la diagnostica della catena:

- **burn-in**;
- **media cumulativa**;
- **correlazione temporale**;
- versione **centrata e normalizzata** della correlazione.

Questo file è **da completare** in alcune parti.  
Le funzioni lasciate incomplete hanno però un fallback interno, in modo che il codice possa essere eseguito e testato anche prima del completamento.

In particolare, si possono completare:

- `cumulative_mean(...)`
- `corr_noncentrata(...)`
- `corr_centrata_normalizzata(...)`

Per rendere il file realmente "da laboratorio", si possono disattivare le reference implementation mettendo a `False` i flag interni.

### `04_proposal_scale_and_diagnostics.py`

Confronta diverse scelte della scala di proposta $\sigma$ nel random-walk Metropolis.

Per ciascun valore di $\sigma$, il file permette di studiare:

- frequenza di accettazione;
- trace plot;
- istogrammi;
- correlazione temporale.

Anche questo file è **da completare** in alcune funzioni, ma è già eseguibile grazie a implementazioni provvisorie.

Le parti tipicamente lasciate agli studenti sono:

- `acceptance_rate(...)`
- `corr_noncentrata(...)`

### `05_gibbs_bonus.py`

File bonus sul **Gibbs sampling** per una gaussiana 2D correlata.

La distribuzione target è

$$
\pi(x_1,x_2)\propto
\exp\!\left[
-\frac{x_1^2-2\rho x_1x_2+x_2^2}{2(1-\rho^2)}
\right].
$$

Le condizionate sono note esplicitamente, quindi un passo Gibbs consiste in:

$$
x_1^{(t+1)} \sim \pi(x_1\mid x_2^{(t)}),
\qquad
x_2^{(t+1)} \sim \pi(x_2\mid x_1^{(t+1)}).
$$

Il file è eseguibile così com'è, ma la funzione

- `gibbs_step(...)`

può essere lasciata da completare agli studenti.

Questo script è pensato come **bonus** o come confronto concettuale con Metropolis.---

## Ordine consigliato di lavoro

Si suggerisce di lavorare nell'ordine seguente:

1. `01_grid_vs_direct_mc.py`
2. `02_metropolis_boltzmann.py`
3. `03_correlation_and_burnin.py`
4. `04_proposal_scale_and_diagnostics.py`
5. `05_gibbs_bonus.py` (opzionale)

Questo ordine segue la logica del laboratorio:

- prima il confronto tra metodi di stima della stessa media;
- poi la costruzione della catena MCMC;
- poi la diagnostica della traiettoria;
- infine il confronto con Gibbs.

## Obiettivi didattici associati ai file

| File | Tema principale |
|---|---|
| `01_grid_vs_direct_mc.py` | integrazione su griglia vs Monte Carlo diretto |
| `02_metropolis_boltzmann.py` | algoritmo di Metropolis e forma con $\Delta E$ |
| `03_correlation_and_burnin.py` | burn-in e correlazione temporale |
| `04_proposal_scale_and_diagnostics.py` | efficienza della proposta |
| `05_gibbs_bonus.py` | Gibbs sampling |

## Cosa verificare durante il laboratorio

Per ogni script, non limitarsi a far "girare il codice". Occorre sempre chiedersi:

1. **che quantità sto stimando?**
2. **quale distribuzione sto campionando?**
3. **i campioni sono indipendenti oppure correlati?**
4. **la catena sembra in equilibrio?**
5. **la stima è corretta ma inefficiente, oppure anche numericamente buona?**

## Nota sulle funzioni incomplete

Nei file `03` e `04` alcune funzioni sono volutamente lasciate come esercizio.  
Per evitare che il codice smetta di funzionare durante lo sviluppo, sono state inserite implementazioni temporanee o flag del tipo:

```python
USE_REFERENCE_...
````

Questi flag permettono di:

* testare il file immediatamente;

* sostituire gradualmente le parti provvisorie con l'implementazione scritta dagli studenti.

## Possibili estensioni

Una volta completato il laboratorio base, si possono esplorare alcune estensioni:

* confronto tra diversi valori di $\beta$;

* distribuzioni bimodali con trapping metastabile;

* confronto quantitativo tra correlazione diretta e correlazione via FFT;

* confronto tra Metropolis e Gibbs sulla stessa distribuzione target.

## Dipendenze

Gli script usano soltanto librerie standard del calcolo scientifico in Python:

* `numpy`

* `matplotlib`

* `time` oppure `timeit` per i benchmark

## Suggerimento finale

Il punto centrale del laboratorio non è solo verificare che i metodi diano lo stesso valore medio, ma capire **quanto costi ottenerlo** in termini di:

* lunghezza della traiettoria;

* burn-in;

* correlazione tra campioni;

* scelta della proposta.

In altre parole: una catena MCMC può essere **corretta** e tuttavia **poco efficiente**.

