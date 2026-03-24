---
title: "04b: Autocorrelazione e tempi di decorrelazione"
author: "Antonio Scala"
date: ""
---

## 1. Perché serve

In molte applicazioni non osserviamo sequenze di dati indipendenti, ma serie temporali o traiettorie in cui il valore presente "ricorda" in parte il passato.

Esempi tipici:
- una traiettoria Monte Carlo o MCMC;
- una serie finanziaria;
- un segnale fisico misurato nel tempo;
- l'evoluzione di una popolazione o di un'epidemia simulata numericamente.

In tutti questi casi è utile quantificare **quanto due osservazioni separate da un ritardo temporale siano ancora dipendenti**.  
Lo strumento naturale per farlo è l'**autocorrelazione**.

## 2. Definizione continua

Sia $f(t)$ una grandezza dipendente dal tempo.  
La funzione di autocorrelazione si definisce come

$$
R_f(\tau) = \overline{f(t+\tau)\,f(t)},
$$

dove la barra indica una media temporale o, in un contesto probabilistico, una media d'ensemble.

Interpretazione:

- se $R_f(\tau)$ resta grande anche per $\tau$ grande, il sistema mantiene memoria del passato;
- se $R_f(\tau)$ decade rapidamente, la memoria si perde in fretta.

## 3. Funzione connessa

Spesso interessa eliminare il contributo dovuto alla media non nulla di $f$.  
Si introduce quindi la funzione di autocorrelazione **connessa**:

$$
C_f(\tau) = R_f(\tau) - \overline{f}^{\,2}.
$$

Equivalentemente,

$$
C_f(\tau) = \overline{\bigl(f(t+\tau)-\overline f\bigr)\bigl(f(t)-\overline f\bigr)}.
$$

Questa quantità misura la vera correlazione delle fluttuazioni attorno al valor medio.

## 4. Autocorrelazione normalizzata

Per confrontare segnali diversi è utile dividere per il valore a ritardo nullo:

$$
\hat C_f(\tau) = \frac{C_f(\tau)}{C_f(0)}.
$$

Allora:

$$
\hat C_f(0)=1.
$$

La funzione $\hat C_f(\tau)$ è adimensionale e descrive in modo pulito il decadimento della memoria.

## 5. Significato fisico e intuitivo

L'autocorrelazione risponde alla domanda:

> se conosco il valore di $f$ al tempo $t$, quanto questo mi aiuta a prevedere il valore a tempo $t+\tau$?

- se $\hat C_f(\tau)\approx 1$, i due valori sono ancora fortemente legati;
- se $\hat C_f(\tau)\approx 0$, il sistema ha praticamente dimenticato il passato;
- se $\hat C_f(\tau)<0$, i valori tendono a compensarsi o oscillare.

## 6. Tempo di decorrelazione

Se il decadimento è circa esponenziale, spesso si osserva una legge del tipo

$$
\hat C_f(\tau) \sim e^{-\tau/\tau_c},
$$

dove $\tau_c$ è il **tempo di decorrelazione**.

Interpretazione:
- per $\tau \ll \tau_c$, il sistema conserva memoria;
- per $\tau \gg \tau_c$, la memoria è sostanzialmente persa.

Questo tempo caratteristico è molto importante in simulazione numerica, perché indica dopo quanto tempo due campioni possono essere considerati quasi indipendenti.

## 7. Caso discreto

Se i dati sono campionati a tempi discreti,
$$
f_0, f_1, \dots, f_{N-1},
$$
l'autocorrelazione a ritardo $k$ si stima come

$$
R_f(k) \approx \frac{1}{N-k}\sum_{i=0}^{N-k-1} f_i f_{i+k}.
$$

La versione connessa è

$$
C_f(k) \approx \frac{1}{N-k}\sum_{i=0}^{N-k-1} (f_i-\bar f)(f_{i+k}-\bar f),
$$

dove

$$
\bar f = \frac{1}{N}\sum_{i=0}^{N-1} f_i.
$$

La versione normalizzata è quindi

$$
\hat C_f(k)=\frac{C_f(k)}{C_f(0)}.
$$

## 8. Attenzione pratica: rumore statistico

Per ritardi grandi, il numero di coppie disponibili diminuisce e la stima dell'autocorrelazione diventa rumorosa.

Infatti, per ritardo $k$ usiamo solo $N-k$ coppie:
- per $k$ piccolo, molte coppie;
- per $k$ grande, poche coppie.

Quindi la parte finale della curva di autocorrelazione va interpretata con cautela: spesso il rumore numerico domina il segnale.

## 9. Numero effettivo di campioni

Se i dati sono correlati, $N$ osservazioni non equivalgono a $N$ campioni indipendenti.

Si introduce allora un numero effettivo di campioni,
$$
N_{\mathrm{eff}} < N,
$$
che dipende dal tempo di autocorrelazione.

In termini qualitativi:
- forte autocorrelazione $\Rightarrow$ pochi campioni davvero indipendenti;
- debole autocorrelazione $\Rightarrow$ $N_{\mathrm{eff}}$ vicino a $N$.

Questo è cruciale nei metodi Monte Carlo e MCMC, dove l'errore statistico dipende dal numero di campioni effettivamente indipendenti, non solo dal numero totale di iterazioni.

## 10. Autocorrelazione e simulazioni Monte Carlo

Nei metodi MCMC, i campioni successivi sono generati da una dinamica che dipende dallo stato corrente.  
Di conseguenza, campioni vicini lungo la traiettoria sono inevitabilmente correlati.

L'autocorrelazione serve quindi a:

- misurare quanto rapidamente la catena esplora lo spazio degli stati;
- stimare quanti campioni indipendenti stiamo realmente ottenendo;
- valutare l'efficienza dell'algoritmo.

Una catena con autocorrelazione lenta è formalmente corretta, ma può essere molto inefficiente.

## 11. Costo computazionale

Il calcolo diretto di $C_f(k)$ per molti ritardi richiede, in modo ingenuo, un costo dell'ordine di

$$
O(N^2).
$$

Per serie lunghe, conviene usare il teorema di Wiener--Khinchin e la trasformata di Fourier veloce (FFT), ottenendo un costo tipico

$$
O(N\log N).
$$

Questo è particolarmente utile nell'analisi di lunghe simulazioni numeriche o di segnali sperimentali.

## 12. Messaggio finale

L'autocorrelazione è uno strumento fondamentale per capire la **memoria temporale** di un sistema.

Permette di:

- distinguere campioni indipendenti da campioni correlati;
- stimare tempi caratteristici di rilassamento;
- valutare l'efficienza di una simulazione;
- interpretare meglio serie temporali e traiettorie stocastiche.

Per questo compare naturalmente in fisica statistica, analisi dei dati, metodi Monte Carlo, finanza, neuroscienze e studio dei sistemi complessi.

---

## Appendice -- Perché la FFT accelera il calcolo dell'autocorrelazione

Nel caso discreto, la funzione di autocorrelazione di una sequenza $\{f_i\}$ può essere scritta come una somma di prodotti tra la sequenza centrata e una sua copia traslata:

$$
C(k) \approx \sum_i (f_i-\bar f)(f_{i+k}-\bar f).
$$

Questa struttura è molto vicina a una convoluzione (più precisamente, a una correlazione discreta).  
Il fatto importante è che, nel dominio di Fourier, convoluzioni e correlazioni diventano prodotti.

Se indichiamo con $\hat f$ la trasformata discreta di Fourier della sequenza centrata $f_i-\bar f$, allora l'autocorrelazione si può ottenere, a meno di normalizzazioni e dettagli tecnici, come trasformata inversa di

$$
|\hat f|^2 = \hat f\,\hat f^{\,*},
$$

dove $\hat f^{\,*}$ indica il complesso coniugato.

In forma compatta:

$$
C = \mathcal{F}^{-1}\!\left( |\mathcal{F}(f-\bar f)|^2 \right).
$$

Quindi il procedimento pratico è:

1. sottraggo la media ai dati;
2. calcolo la FFT della sequenza centrata;
3. moltiplico per il complesso coniugato;
4. applico la trasformata inversa.

Questo evita il calcolo diretto di tutte le somme per tutti i ritardi e riduce il costo computazionale da circa

$$
O(N^2)
$$

a circa

$$
O(N\log N).
$$

### Messaggio essenziale

Non è necessario ricordare tutti i dettagli tecnici: basta sapere che l'autocorrelazione ha struttura di correlazione/convoluzione, e che per questo la FFT è il metodo naturale per calcolarla rapidamente.
