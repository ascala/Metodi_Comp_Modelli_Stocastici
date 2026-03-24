---
title: "LAB03 Dallo stimatore Monte Carlo ai metodi MCMC"
author: "Antonio Scala"
date: "24 Marzo 2026"
---

# Obiettivi del laboratorio

In questo laboratorio useremo simulazioni numeriche per collegare in modo esplicito il Monte Carlo diretto visto nel laboratorio precedente con i metodi Markov Chain Monte Carlo introdotti nella lezione sulle catene di Markov e sull'algoritmo di Metropolis.

L'obiettivo non è solo implementare una catena corretta, ma capire:

1. come stimare la stessa quantità con tre strategie diverse;
2. perché il campionamento MCMC usa campioni correlati e non indipendenti;
3. che cosa significano, in pratica, burn-in, frequenza di accettazione e autocorrelazione;
4. quando una catena formalmente corretta può essere numericamente inefficiente;
5. perché, nel caso di un peso di Boltzmann, conviene usare direttamente $\Delta E$ nella regola di accettazione.

Confronteremo tre modi di stimare la stessa media:

1. integrazione numerica diretta su griglia;
2. Monte Carlo diretto con campioni indipendenti;
3. campionamento MCMC con algoritmo di Metropolis.

Nella parte finale discuteremo anche come misurare la correlazione temporale e come calcolarla in modo efficiente usando la FFT.

# Struttura del laboratorio

Il laboratorio è diviso in cinque parti:

- Parte 0 -- richiamo teorico e notazioni;
- Parte A -- la stessa media con tre metodi;
- Parte B -- Metropolis in forma di Boltzmann: rapporto vs $\Delta E$;
- Parte C -- burn-in, correlazione e autocorrelazione;
- Parte D -- effetto della scala di proposta;
- Microappendice -- correlazione via FFT.

# Parte 0 -- Richiamo teorico

## 0.1 Dal laboratorio precedente

Nel laboratorio sui metodi Monte Carlo abbiamo già visto che una quantità del tipo

$$
\langle O \rangle_p = \int O(x)\,p(x)\,dx
$$

può essere stimata come media campionaria se sappiamo generare campioni indipendenti da $p(x)$.

Nel caso di una media con peso di Boltzmann, si scrive

$$
\langle O \rangle =
\frac{\int O(x)e^{-\beta E(x)}\,dx}
{\int e^{-\beta E(x)}\,dx}.
$$

Nel laboratorio precedente questa quantità veniva stimata separando numeratore e denominatore.

## 0.2 Passaggio a MCMC

Se non sappiamo campionare direttamente da

$$
\pi(x)=\frac{1}{Z}e^{-\beta E(x)},
$$

possiamo costruire una catena di Markov che abbia $\pi$ come distribuzione stazionaria.

Se la catena è ergodica, allora per una osservabile $O$ vale il principio ergodico:

$$
\langle O \rangle_\pi
\approx
\frac{1}{N}\sum_{t=1}^N O(X_t),
\qquad X_t \sim \text{catena MCMC}.
$$

Questa stima usa però campioni successivi che, in generale, non sono indipendenti.

## 0.3 Correlazione temporale: idea di base

Se definiamo

$$
O_t = O(X_t),
$$

una quantità naturale da studiare è la funzione di correlazione temporale non centrata

$$
C(\tau)=\langle O_{t+\tau} O_t \rangle.
$$

Empiricamente, su una traiettoria finita di lunghezza $N$, la stimiamo come

$$
C(\tau)\approx
\frac{1}{N-\tau}\sum_{t=0}^{N-\tau-1} O_{t+\tau} O_t.
$$

Interpretazione:

- se $C(\tau)$ decade lentamente, la catena conserva memoria a lungo;
- se $C(\tau)$ decade rapidamente, i campioni diventano presto quasi indipendenti.

Se vogliamo una correlazione che, in un sistema ergodico, decada a zero per tempi lunghi, dobbiamo sottrarre il contributo delle medie:

$$
C_{\mathrm{conn}}(\tau)
=
\langle O_{t+\tau} O_t \rangle
-
\langle O_{t+\tau}\rangle \langle O_t\rangle.
$$

In regime stazionario la media è invariante per traslazione temporale, quindi

$$
\langle O_{t+\tau}\rangle=\langle O_t\rangle=\langle O\rangle,
$$

e allora

$$
C_{\mathrm{conn}}(\tau)=
\langle O_{t+\tau} O_t \rangle - \langle O\rangle^2.
$$

Se poi vogliamo una funzione normalizzata tra 0 e 1, basta dividere per il valore a tempo zero:

$$
\widetilde C(\tau)=\frac{C(\tau)}{C(0)}
\qquad\text{oppure}\qquad
\widetilde C_{\mathrm{conn}}(\tau)=\frac{C_{\mathrm{conn}}(\tau)}{C_{\mathrm{conn}}(0)}.
$$

In questo modo si può leggere, ad esempio, un tempo caratteristico dal punto in cui la correlazione scende sotto $1/e$.

## 0.4 Snippet Python: correlazione non centrata

```python
import numpy as np

def corr_noncentrata(O, tau_max):
    O = np.asarray(O, dtype=float) # trasforma in un array per usare numpy
    N = len(O)
    C = np.empty(tau_max + 1) # le correlazioni andranno qui

    for tau in range(tau_max + 1):
        C[tau] = np.mean(O[:N - tau] * O[tau:])

    return C
```

## 0.5 Snippet Python: correlazione centrata e normalizzata

```python
import numpy as np

def corr_centrata_normalizzata(O, tau_max):
    O = np.asarray(O, dtype=float)
    m = np.mean(O)
    X = O - m
    N = len(X)
    C = np.empty(tau_max + 1)

    for tau in range(tau_max + 1):
        C[tau] = np.mean(X[:N - tau] * X[tau:])

    return C / C[0]
```

# Il problema di partenza

Useremo come distribuzione target un peso di Boltzmann del tipo

$$
\pi(x)=\frac{1}{Z}e^{-\beta E(x)},
$$

con energia

$$
E(x)=\frac{x^4}{4}-\frac{x^2}{2}.
$$

Questa scelta è utile perché:

1. si collega direttamente al laboratorio precedente;
2. consente integrazione numerica su griglia;
3. consente Monte Carlo diretto su un intervallo finito;
4. consente MCMC tramite Metropolis;
5. la forma della regola di accettazione può essere scritta direttamente in termini di $\Delta E$.

Come osservabile principale useremo

$$
O(x)=x^2.
$$

Vogliamo quindi stimare

$$
\langle O\rangle_\pi = \frac{\int O(x)e^{-\beta E(x)}\,dx}{\int e^{-\beta E(x)}\,dx}.
$$

Nel seguito si può prendere, ad esempio,

$$
\beta = 2.
$$

Per la parte numerica si lavora su un intervallo finito simmetrico $[-L,L]$, con $L$ abbastanza grande da rendere trascurabile il contributo delle code.

# Parte A -- La stessa media con tre metodi

## A1. Metodo (i): integrazione numerica diretta su griglia

Stimare numericamente

$$
A=\int_{-L}^{L} O(x)e^{-\beta E(x)},dx,
\qquad
Z=\int_{-L}^{L} e^{-\beta E(x)},dx,
$$

e poi costruire

$$
\langle O\rangle_\pi = \frac{A}{Z}.
$$

Usare una griglia uniforme e una regola numerica semplice, ad esempio trapezi o somma di Riemann.

### Compiti

1. Scegliere un valore di $L$ ragionevole e motivarlo.
2. Calcolare $\hat A_{\mathrm{grid}}$, $\hat Z_{\mathrm{grid}}$ e il rapporto.
3. Verificare quanto cambia il risultato raffinando la griglia.

## A2. Metodo (ii): Monte Carlo diretto con campioni indipendenti

Campionare punti uniformi

$$
X_i \sim \mathrm{Unif}([-L,L]),
$$

e stimare separatamente

$$
\hat A_{\mathrm{MC}} = \frac{2L}{N}\sum_{i=1}^N O(X_i)e^{-\beta E(X_i)},
$$

$$
\hat Z_{\mathrm{MC}} = \frac{2L}{N}\sum_{i=1}^N e^{-\beta E(X_i)},
$$

quindi

$$
\widehat{\langle O\rangle}_{\mathrm{MC}} = \frac{\hat A_{\mathrm{MC}}}{\hat Z_{\mathrm{MC}}}.
$$

### Compiti

1. Implementare lo stimatore Monte Carlo diretto.
2. Ripetere il calcolo per più valori di $N$.
3. Confrontare il risultato con l'integrazione numerica diretta.

## A3. Metodo (iii): Metropolis MCMC

Costruire una catena con target

$$
\pi(x)\propto e^{-\beta E(x)}
$$

usando una proposta random walk gaussiana

$$
x' = x + \eta,
\qquad
\eta\sim\mathcal N(0,\sigma^2).
$$

La stima dell'osservabile è

$$
\widehat{\langle O\rangle}_{\mathrm{MCMC}} = \frac{1}{N_{\mathrm{meas}}}
\sum_{t=t_{\mathrm{burn}}+1}^{N} O(X_t).
$$

### Compiti

1. Implementare uno scheletro di Metropolis.
2. Usare burn-in esplicito.
3. Stimare $\langle O\rangle_\pi$.
4. Confrontare il risultato con i metodi (i) e (ii).

## A4. Domande guida

1. I tre metodi convergono allo stesso valore?
2. Quale metodo è più semplice in una dimensione?
3. Quale metodo si generalizza meglio a dimensione più alta?
4. Quale metodo non richiede di conoscere $Z$?

## A5. Pseudocodice: tre approcci

```text
Metodo (i): griglia
- scegli griglia x_k su [-L,L]
- calcola A = somma O(x_k) exp(-beta E(x_k)) dx
- calcola Z = somma exp(-beta E(x_k)) dx
- restituisci A/Z

Metodo (ii): Monte Carlo diretto
- genera X_i uniformi in [-L,L]
- stima A e Z come medie campionarie
- restituisci A/Z

Metodo (iii): MCMC
- inizializza x_0
- esegui burn-in
- accumula O(X_t) lungo la traiettoria
- restituisci la media temporale
```

# Parte B -- Metropolis in forma di Boltzmann: rapporto vs $\Delta E$

## B1. Regola di accettazione

Per il target

$$
\pi(x)\propto e^{-\beta E(x)},
$$

la regola di Metropolis può essere scritta in due modi equivalenti.

### Forma 1: rapporto diretto

$$
A(x\to x')=
\min\left(1,\frac{e^{-\beta E(x')}}{e^{-\beta E(x)}}\right).
$$

### Forma 2: differenza di energia

Definendo

$$
\Delta E = E(x')-E(x),
$$

si ottiene

$$
A(x\to x')=
\min\left(1,e^{-\beta\Delta E}\right).
$$

Le due formule sono matematicamente equivalenti.

## B2. Compiti

1. Implementare entrambe le versioni.
2. Verificare che producano la stessa statistica finale.
3. Misurare il tempo di esecuzione delle due implementazioni usando `time.perf_counter()` oppure `timeit`.
4. Discutere quale forma è più conveniente dal punto di vista computazionale.

## B3. Snippet Python: misura del tempo

```python
import time

t0 = time.perf_counter()
# esegui qui molte iterazioni del metodo
t1 = time.perf_counter()

print("tempo totale =", t1 - t0)
```

## B4. Domande guida

1. Le due forme dell'accettazione danno gli stessi risultati?
2. La forma con $\Delta E$ è più naturale fisicamente?
3. La forma con $\Delta E$ è più efficiente o più stabile numericamente?

---

# Parte C -- Burn-in, correlazione e medie cumulative

## C1. Burn-in

Una catena MCMC non parte, in generale, dalla distribuzione di equilibrio. I primi passi dipendono dalla condizione iniziale e devono spesso essere scartati.

### Esperimento

Lanciare tre catene con condizioni iniziali diverse, ad esempio

$$
x_0=-3,\qquad x_0=0,\qquad x_0=3.
$$

Per ciascuna catena:

1. tracciare il trace plot di $x_t$;
2. tracciare il trace plot di $O_t=x_t^2$;
3. tracciare la media cumulativa

$$
M_n=\frac{1}{n}\sum_{t=1}^n O_t.
$$

### Domande guida

1. Le tre catene convergono alla stessa statistica?
2. Dopo quanti passi la media cumulativa sembra stabilizzarsi?
3. Quanto cambia la stima se si scartano i primi $n_{\mathrm{burn}}$ passi?

## C2. Correlazione temporale

Usare l'osservabile

$$
O_t = X_t^2
$$

oppure

$$
O_t = X_t.
$$

Calcolare la correlazione non centrata

$$
C(\tau)=\langle O_{t+\tau} O_t\rangle
$$

tramite la formula empirica

$$
C(\tau)\approx
\frac{1}{N-\tau}\sum_{t=0}^{N-\tau-1} O_{t+\tau} O_t.
$$

Poi, se si vuole una correlazione che tenda a zero in un sistema ergodico, passare alla forma centrata

$$
C_{\mathrm{conn}}(\tau)=
\langle O_{t+\tau} O_t\rangle - \langle O\rangle^2.
$$

Infine, se si vuole una funzione normalizzata tra 0 e 1, dividere per il valore a tempo zero.

### Compiti

1. Calcolare $C(\tau)$ per $\tau=0,1,\dots,\tau_{\max}$.
2. Calcolare anche la versione centrata e normalizzata.
3. Confrontare il decadimento della correlazione per diverse scelte della scala di proposta.

### Domande guida

1. La correlazione decade rapidamente o lentamente?
2. Quanto dipende dalla scala di proposta?
3. Una catena con alta accettazione ha necessariamente correlazione più bassa?

# Parte D -- Effetto della scala di proposta

## D1. Idea

Nel random walk Metropolis la proposta è

$$
x' = x + \eta,
\qquad
\eta\sim\mathcal N(0,\sigma^2).
$$

La scelta di $\sigma$ controlla il compromesso tra:

* frequenza di accettazione;
* esplorazione dello spazio degli stati;
* correlazione tra campioni successivi.

## D2. Esperimento

Confrontare almeno tre valori di $\sigma$, ad esempio

$$
\sigma=0.1,\qquad \sigma=0.8,\qquad \sigma=2.5.
$$

Per ciascun valore:

1. generare una traiettoria;
2. misurare la frequenza di accettazione;
3. plottare il trace plot;
4. calcolare $C(\tau)$;
5. stimare $\langle O\rangle_\pi$.

## D3. Cosa aspettarsi

* proposta troppo piccola:

  * accettazione alta;
  * movimento lento;
  * correlazione forte;
* proposta intermedia:

  * buon compromesso;
  * correlazione più breve;
* proposta troppo grande:

  * molte proposte rifiutate;
  * catena quasi bloccata;
  * accettazione bassa.

## D4. Domande guida

1. Quale valore di $\sigma$ produce la stima più affidabile a parità di tempo computazionale?
2. Il miglior valore di $\sigma$ è quello con accettazione più alta?
3. Come cambia il decadimento di $C(\tau)$ passando da una proposta troppo piccola a una troppo grande?

# Parte E -- Bonus opzionale: Gibbs sampling

Questa parte è opzionale e serve come confronto concettuale con Metropolis.

Considerare una gaussiana bidimensionale correlata

$$
\pi(x_1,x_2)\propto
\exp!\left[
-\frac{x_1^2-2\rho x_1x_2+x_2^2}{2(1-\rho^2)}
\right].
$$

Le condizionate sono gaussiane:

$$
x_1\mid x_2 \sim \mathcal N(\rho x_2,1-\rho^2),
\qquad
x_2\mid x_1 \sim \mathcal N(\rho x_1,1-\rho^2).
$$

Un passo di Gibbs consiste in:

$$
x_1^{(t+1)} \sim \pi(x_1\mid x_2^{(t)}),
\qquad
x_2^{(t+1)} \sim \pi(x_2\mid x_1^{(t+1)}).
$$

## Domande guida

1. Perché Gibbs non ha rifiuti?
2. Che cosa richiede in più rispetto a Metropolis?
3. In quale senso è più strutturato ma meno generale?

---

# Materiale di partenza

Per il laboratorio si suggerisce di partire da tre script:

* `01_grid_vs_direct_mc.py`
* `02_metropolis_boltzmann.py`
* `03_correlation_and_diagnostics.py`

eventualmente con un quarto file opzionale:

* `04_gibbs_bonus.py`

# Consegna

Ogni gruppo deve produrre:

1. il confronto tra i tre metodi di stima della stessa media;
2. una verifica che la forma con rapporto e la forma con $\Delta E$ danno la stessa statistica;
3. una misura dei tempi di esecuzione delle due implementazioni;
4. un trace plot che mostri il burn-in;
5. almeno un grafico di correlazione $C(\tau)$;
6. un confronto tra almeno tre scale di proposta;
7. un breve commento finale sui punti seguenti:

   * differenza tra Monte Carlo diretto e MCMC;
   * ruolo del burn-in;
   * significato della correlazione temporale;
   * correttezza teorica vs efficienza pratica.

# Checklist finale

1. Stima di $\langle O\rangle_\pi$ con:

   * griglia,
   * Monte Carlo diretto,
   * MCMC.
2. Confronto tra forma con rapporto e forma con $\Delta E$.
3. Diagnostica di burn-in e media cumulativa.
4. Calcolo della correlazione non centrata.
5. Versione centrata/normalizzata della correlazione.
6. Confronto tra diverse scale di proposta.

---

# Microappendice -- Calcolo veloce della correlazione con FFT

La correlazione discreta può essere vista come una convoluzione.

Per una sequenza $O_t$, la quantità

$$
C(\tau)\sim \sum_t O_{t+\tau}O_t
$$

ha struttura di convoluzione tra la sequenza e la sequenza ribaltata.

Poiché la trasformata di Fourier trasforma una convoluzione in un prodotto, il calcolo della correlazione può essere accelerato usando la FFT:

$$
\mathcal F[f*g] = \mathcal F[f];\mathcal F[g].
$$

Nel caso centrato, se definiamo

$$
X_t = O_t - \langle O\rangle,
$$

allora schematicamente

$$
C_{\mathrm{conn}}(\tau) = \mathcal F^{-1}!\left(\mathcal F[X];\mathcal F[X]^*\right),
$$

dove $^*$ indica il complesso coniugato.

Questo riduce il costo computazionale da circa $N^2$ a circa $N\log N$.

## Snippet Python con FFT

```python
import numpy as np

def corr_fft_centrata(O):
    O = np.asarray(O, dtype=float)
    X = O - np.mean(O)
    N = len(X)

    nfft = 2 * N
    F = np.fft.rfft(X, n=nfft)
    S = F * np.conjugate(F)
    C = np.fft.irfft(S, n=nfft)[:N]

    C /= np.arange(N, 0, -1)
    return C
```

## Versione normalizzata

```python
def corr_fft_centrata_normalizzata(O):
    C = corr_fft_centrata(O)
    return C / C[0]
```

## Domanda finale

Quando conviene usare la FFT invece del calcolo diretto della correlazione?

