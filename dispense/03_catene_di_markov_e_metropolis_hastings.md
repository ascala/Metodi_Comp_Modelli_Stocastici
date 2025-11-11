---
title: "Catene di Markov e Metropolis"
author: ""
date: ""
---

# Catene di Markov e Metropolis

(Obiettivi della lezione: introdurre i concetti fondamentali delle catene di Markov come modelli di evoluzione probabilistica e presentare l’algoritmo di Metropolis come metodo generale per campionare distribuzioni arbitrarie in sistemi complessi, con esempi tratti da fisica, economia e scienze sociali.)

---

### Obiettivi didattici specifici

1. Comprendere la logica markoviana: il futuro dipende solo dallo stato presente.  
2. Analizzare la nozione di distribuzione stazionaria e il concetto di equilibrio.  
3. Intuire come l’algoritmo di Metropolis costruisce una catena coerente con una distribuzione target.  
4. Collegare il principio di bilancio dettagliato all’idea di equilibrio in fisica, apprendimento e decisione.  
5. Applicare concetti di Markov e Metropolis a esempi interdisciplinari (fisica statistica, mercati, reti sociali).

---

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Sistemi markoviani e proprietà di memoria corta** – definizione, esempi e significato.  
2. **Equilibrio e distribuzioni stazionarie** – cosa significa che una catena “si stabilizza”.  
3. **Algoritmo di Metropolis** – idea, logica e schema operativo.  
4. **Esperimento numerico** – simulazione di una distribuzione target.  
5. **Connessioni interdisciplinari** – interpretazioni e applicazioni.

---

### Conclusione introduttiva

Molti sistemi reali — fisici, biologici, economici, sociali — evolvono nel tempo seguendo regole probabilistiche.  
Le catene di Markov forniscono un quadro semplice ma generale per descrivere tali dinamiche.  
L’algoritmo di Metropolis sfrutta questa struttura per **campionare distribuzioni complesse**, generando sequenze di stati coerenti con la probabilità che ciascuno possieda nel sistema reale o nel modello teorico.

---

## 1. Sistemi markoviani e proprietà di memoria corta

### 1.1 Definizione intuitiva

Un sistema markoviano è un sistema in cui **il futuro dipende solo dal presente**, non dall’intera storia passata.  
In simboli:
$$
P(X_{t+1}=j \mid X_t=i, X_{t-1},\ldots,X_0) = P(X_{t+1}=j \mid X_t=i).
$$

È una proprietà sorprendentemente generale: la ritroviamo nei giochi di sorte, nei processi biologici, nelle scelte degli individui, nei modelli economici e nei flussi di informazione.

### 1.2 Esempio: gioco della moneta truccata

Un giocatore può trovarsi in due stati:
- **0:** ha perso il turno precedente;  
- **1:** ha vinto.

Le probabilità di transizione sono:
$$
P_{01}=0.4,\quad P_{00}=0.6,\quad P_{10}=0.2,\quad P_{11}=0.8.
$$

Questa matrice di transizione
$$
P=\begin{pmatrix}0.6 & 0.4 \\ 0.2 & 0.8\end{pmatrix}
$$
descrive l’intero processo.  
Dopo alcuni passi, la frequenza dei due stati tende a valori stabili indipendenti dalle condizioni iniziali — il sistema “dimentica il passato”.

---

## 2. Equilibrio e distribuzioni stazionarie

### 2.1 Concetto di equilibrio

Una **distribuzione stazionaria** $\pi$ è tale che
$$
\pi = \pi P,
$$
cioè la probabilità media di essere in ciascuno stato non cambia più nel tempo.  

Nel gioco della moneta truccata, risolvendo le equazioni:
$$
\pi_0 = 0.6\pi_0 + 0.2\pi_1, \quad \pi_0+\pi_1=1,
$$
si ottiene
$$
\pi = \left(\tfrac{1}{3}, \tfrac{2}{3}\right).
$$

Il giocatore trascorre circa un terzo del tempo perdendo e due terzi vincendo: questa è la condizione di equilibrio.

### 2.2 Reversibilità e bilancio dettagliato

In equilibrio, i flussi di probabilità da $i$ a $j$ e da $j$ a $i$ si compensano:
$$
\pi_i P_{ij} = \pi_j P_{ji}.
$$

È il cosiddetto **bilancio dettagliato**, equivalente all’assenza di correnti nette.  
In fisica rappresenta l’equilibrio microscopico; in economia o sociologia, una condizione di stabilità dinamica — gli scambi o le opinioni cambiano, ma il profilo medio resta costante.

---

## 3. Algoritmo di Metropolis

### 3.1 Idea generale

Spesso vogliamo campionare da una distribuzione $\pi(x)$ che non possiamo generare direttamente.  
L’idea dell’algoritmo di **Metropolis** è costruire una catena di Markov che abbia $\pi(x)$ come distribuzione di equilibrio.

A ogni passo:
1. Si propone una nuova configurazione $x'$ (da una distribuzione di proposta simmetrica $q(x'|x)$).  
2. Si accetta o rifiuta la mossa con probabilità:
$$
A(x\to x') = \min\left(1, \frac{\pi(x')}{\pi(x)}\right).
$$

Se $\pi(x')>\pi(x)$ la mossa è sempre accettata; se è peggiore, può comunque essere accettata con una probabilità che consente al sistema di “uscire dai minimi locali”.

### 3.2 Interpretazione intuitiva

- **Alta temperatura:** il sistema esplora liberamente (molte accettazioni).  
- **Bassa temperatura:** il sistema si concentra intorno alle regioni di alta probabilità.  
- **Equilibrio:** la frequenza degli stati generati riproduce $\pi(x)$.

L’algoritmo è semplice ma universale: funziona in fisica statistica, economia computazionale, ecologia o analisi di reti.

### 3.3 Schema operativo (pseudocodice)

```python
import numpy as np

def metropolis(E, x0, T, steps):
    x = x0
    samples = [x]
    for _ in range(steps):
        x_new = x + np.random.normal(0, 1)
        dE = E(x_new) - E(x)
        if np.random.rand() < np.exp(-dE/T):
            x = x_new
        samples.append(x)
    return np.array(samples)
````

---

## 4. Esperimento numerico

### 4.1 Obiettivo

Campionare una distribuzione gaussiana:
$$
\pi(x) \propto e^{-x^2/2}.
$$

Definiamo $E(x)=x^2/2$ come “energia” del sistema e applichiamo Metropolis con temperatura $T=1$.

### 4.2 Esempio in Python

```python
import numpy as np
import matplotlib.pyplot as plt

E = lambda x: 0.5*x**2
samples = metropolis(E, x0=0.0, T=1.0, steps=10000)
plt.hist(samples[2000:], bins=50, density=True)
plt.xlabel("x")
plt.ylabel("frequenza")
plt.title("Distribuzione campionata con Metropolis")
plt.show()
```

Il risultato mostra che l’istogramma dei campioni si sovrappone alla forma della distribuzione gaussiana: il sistema “simula” l’equilibrio statistico.

---

## 5. Connessioni interdisciplinari

### 5.1 Fisica

In fisica statistica, l’algoritmo simula il comportamento di un sistema termico:
ogni stato ha un’energia $E(x)$ e una probabilità proporzionale a $e^{-E(x)/T}$.
L’equilibrio di Boltzmann corrisponde alla distribuzione stazionaria della catena.

### 5.2 Economia

In economia computazionale, la catena rappresenta un mercato che esplora configurazioni di portafoglio:
le mosse accettate sono strategie più redditizie o variazioni casuali mantenute con probabilità proporzionale al “guadagno relativo”.

### 5.3 Scienze sociali e reti

Nel comportamento collettivo o nei modelli di opinione, l’algoritmo Metropolis descrive un gruppo di agenti che adattano le proprie scelte o idee:
mosse che aumentano la coerenza (o l’utilità) vengono adottate più facilmente, ma esiste sempre una componente casuale che favorisce la diversità e l’esplorazione.

---

## Riferimenti

* Metropolis, N., et al. (1953). *Equation of State Calculations by Fast Computing Machines*. J. Chem. Phys.
* Hastings, W. K. (1970). *Monte Carlo Sampling Methods Using Markov Chains and Their Applications*. Biometrika.
* Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
* Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
* Landau, D. P., & Binder, K. (2021). *A Guide to Monte Carlo Simulations in Statistical Physics*. Cambridge University Press.
* Gintis, H. (2017). *Individuality and Entanglement: The Moral and Material Bases of Social Life*. Princeton University Press.

---
