---
title: "Simulazioni di eventi discreti (Gillespie e oltre)"
author: ""
date: ""
---

# Simulazioni di eventi discreti (Gillespie e oltre)

(Obiettivi della lezione: comprendere come simulare processi stocastici in cui gli eventi avvengono in tempi discreti e casuali, a partire dal metodo di Gillespie per reazioni chimiche e sue estensioni a modelli epidemiologici e di diffusione.)

---

### Obiettivi didattici specifici

1. Introdurre il concetto di **processo a eventi discreti** e la logica della simulazione diretta.  
2. Capire il significato di **tempo di attesa** e la sua distribuzione esponenziale.  
3. Presentare e implementare il **metodo di Gillespie** per reazioni stocastiche.  
4. Estendere il metodo a sistemi complessi (epidemie, reti, agent–based).  
5. Confrontare diversi approcci: simulazione esatta, tau-leaping, approssimazioni continue.

---

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Introduzione ai processi a eventi discreti** – cosa sono e dove si applicano.  
2. **Tempo di attesa e legge esponenziale** – probabilità che un evento avvenga dopo un certo tempo.  
3. **Algoritmo di Gillespie (Direct Method)** – simulazione passo per passo.  
4. **Estensioni e approssimazioni** – tau-leaping e metodi ibridi.  
5. **Applicazioni interdisciplinari** – reazioni chimiche, epidemie, dinamiche sociali.

---

### Conclusione introduttiva

Molti sistemi reali non evolvono in modo continuo, ma attraverso **eventi discreti**: un’infezione, una nascita, una reazione chimica. Il metodo di Gillespie fornisce una procedura esatta per generare simulazioni coerenti con le leggi di probabilità del processo sottostante. Questa lezione mostra come funziona e come adattarlo a contesti diversi.

---

## 1. Processi a eventi discreti

Un processo a eventi discreti è descritto da:
- un insieme di **stati** $S = \{s_1, s_2, \dots\}$,  
- un insieme di **transizioni** (eventi) con **tassi** $a_i(x)$ che dipendono dallo stato $x$,  
- una regola che specifica come lo stato cambia dopo ogni evento.

Esempi:
- una molecola che reagisce ($A + B \to C$),  
- una persona che si infetta ($S \to I$),  
- un cliente che entra in coda ($n \to n+1$).

L’evoluzione è **stocastica**: il tempo e il tipo del prossimo evento sono casuali.

---

## 2. Tempo di attesa e legge esponenziale

Se un evento accade con tasso costante $\lambda$, la probabilità che avvenga entro il tempo $t$ è
$$
P(T < t) = 1 - e^{-\lambda t}.
$$

La densità di probabilità del **tempo di attesa** è quindi
$$
p(t) = \lambda e^{-\lambda t},
$$
una **distribuzione esponenziale** con valore medio $1/\lambda$.

Nella simulazione, si può estrarre il tempo del prossimo evento come:
$$
\tau = -\frac{1}{\lambda}\ln U,
$$
dove $U$ è una variabile uniforme in $[0,1)$.

**Interpretazione:** il sistema “attende” un tempo casuale $\tau$ prima che qualcosa accada.

---

## 3. Algoritmo di Gillespie (Direct Method)

### 3.1 Idea generale

In un sistema con $M$ tipi di eventi, ciascuno con tasso $a_j(x)$, il **tasso totale** è
$$
a_0(x) = \sum_{j=1}^{M} a_j(x).
$$

A ogni passo:
1. si estrae il **tempo del prossimo evento**
   $$
   \tau = \frac{1}{a_0(x)} \ln\!\left(\frac{1}{U_1}\right),
   $$
2. si sceglie **quale evento avviene** con probabilità proporzionale al suo tasso:
   $$
   P(\text{evento } j) = \frac{a_j(x)}{a_0(x)}.
   $$
3. si **aggiorna lo stato** secondo la regola dell’evento selezionato,
4. si incrementa il tempo $t \to t + \tau$,
5. si ripete.

### 3.2 Implementazione base

```python
import numpy as np

def gillespie_step(state, rates, stoich):
    a = np.array([r(state) for r in rates])
    a0 = a.sum()
    if a0 == 0:
        return state, np.inf, None
    tau = np.random.exponential(1/a0)
    j = np.searchsorted(np.cumsum(a/a0), np.random.rand())
    new_state = state + stoich[j]
    return new_state, tau, j
````

### 3.3 Esempio: reazione $A \to \emptyset$

```python
def rate_A_to_null(state):
    return 0.1 * state[0]

rates = [rate_A_to_null]
stoich = [np.array([-1])]
state = np.array([100])
t = 0.0

trajectory = [(t, state[0])]
while state[0] > 0 and t < 100:
    state, dt, _ = gillespie_step(state, rates, stoich)
    t += dt
    trajectory.append((t, state[0]))
```

Risultato: il numero di $A$ decresce in modo casuale ma in media segue un decadimento esponenziale.

***

## 4. Estensioni e approssimazioni

### 4.1 Tau-leaping

Quando i tassi sono grandi, il metodo di Gillespie diventa lento: si può **saltare più eventi insieme** assumendo che i tassi restino quasi costanti in un intervallo $\Delta t$.

Numero di eventi del tipo $j$ in $\Delta t$:\
$$\
k\_j \sim \text{Poisson}(a\_j(x),\Delta t).\
$$

Aggiornamento:\
$$\
x \to x + \sum\_j k\_j,\nu\_j,\
$$\
dove $\nu\_j$ è il vettore di cambiamento per l’evento $j$.

Questo metodo è un ponte verso le **equazioni di Langevin chimiche**.

***

### 4.2 Metodi ibridi e approssimazioni continue

* **Approccio ibrido:** alcuni processi sono simulati in modo discreto, altri in modo continuo.

* **Diffusion approximation:** quando il numero di entità è grande, il processo può essere approssimato da un’equazione differenziale stocastica.

* **Applicazioni:** dinamiche di popolazioni, modelli di traffico, reti di comunicazione, epidemie su grafi.

***

## 5. Applicazioni interdisciplinari

### 5.1 Reazioni chimiche

Il metodo di Gillespie nasce per modellare sistemi chimici in cui le concentrazioni sono basse e il rumore è importante (es. regolazione genica).

### 5.2 Modelli epidemiologici

In un modello SIR discreto:

* $S \to I$ con tasso $\beta S I / N$,

* $I \to R$ con tasso $\gamma I$.

Lo stesso algoritmo si applica scegliendo i due tipi di eventi e aggiornando gli stati di conseguenza.

### 5.3 Sistemi sociali e agent–based

Ogni interazione tra agenti (adozione di un’idea, scambio, uscita da un gruppo) può essere trattata come un **evento discreto** con un proprio tasso.\
Il framework di Gillespie fornisce un linguaggio unificato per descrivere tali dinamiche.

---

## Riferimenti

* Gillespie, D. T. (1977). *Exact stochastic simulation of coupled chemical reactions*. J. Phys. Chem. 81(25): 2340–2361.

* Gibson, M. A., & Bruck, J. (2000). *Efficient exact stochastic simulation of chemical systems with many species and many channels*. J. Phys. Chem. A 104(9): 1876–1889.

* Higham, D. J. (2008). *Modeling and simulating chemical reactions*. SIAM Review, 50(2): 347–368.

* Allen, L. J. S. (2003). *An Introduction to Stochastic Processes with Applications to Biology*. Pearson.

* Wilkinson, D. J. (2006). *Stochastic Modelling for Systems Biology*. CRC Press.

---
