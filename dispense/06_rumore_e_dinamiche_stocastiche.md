---
title: "Rumore e dinamiche stocastiche"
author: ""
date: ""
---

# Rumore e dinamiche stocastiche

(Obiettivi della lezione: comprendere il significato del rumore nei modelli dinamici, distinguere tra fluttuazioni deterministiche e casuali, e introdurre le equazioni di Langevin come modello generale di evoluzione sotto incertezza.)

---

### Obiettivi didattici specifici

1. Capire che cosa si intende per **rumore** in un sistema dinamico e da dove nasce.  
2. Distinguere fra **rumore additivo** e **rumore moltiplicativo**.  
3. Introdurre la forma concettuale dell’**equazione di Langevin**.  
4. Interpretare le traiettorie stocastiche come famiglie di possibili evoluzioni.  
5. Collegare le dinamiche stocastiche a fenomeni reali (fisici, biologici, sociali).

---

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Rumore e fluttuazioni nei modelli reali** – da errore sperimentale a fattore dinamico.  
2. **Concetto di equazione stocastica** – l’idea di evoluzione casuale nel tempo.  
3. **Equazione di Langevin** – modello base del moto browniano.  
4. **Simulazioni numeriche di traiettorie** – metodo di Euler–Maruyama (intuitivo).  
5. **Esempi interdisciplinari** – diffusione, apprendimento, mercati, reti sociali.

---

### Conclusione introduttiva

Il rumore non è soltanto un disturbo: in molti sistemi è parte integrante della dinamica.  
Nei modelli stocastici, l’incertezza è rappresentata esplicitamente, e il comportamento medio emerge da molte realizzazioni del processo. La teoria di Langevin fornisce un linguaggio unificato per descrivere questi fenomeni, dal moto delle particelle al comportamento collettivo di popolazioni e agenti.

---

## 1. Rumore e fluttuazioni nei modelli reali

Nella realtà, quasi nessun processo è perfettamente prevedibile:  
- nelle **reazioni chimiche**, il numero di collisioni varia casualmente;  
- nei **mercati finanziari**, le decisioni individuali producono fluttuazioni aggregate;  
- nelle **epidemie**, contatti e tempi di infezione non sono regolari;  
- nei **sistemi sociali**, la risposta degli individui a stimoli comuni è variabile.

Il **rumore** rappresenta l’effetto di cause non modellate, ma statisticamente caratterizzabili.

Si parla di:
- **rumore additivo** quando si somma una perturbazione indipendente dallo stato,  
- **rumore moltiplicativo** quando l’intensità del rumore dipende dal valore della variabile stessa.

---

## 2. Concetto di equazione stocastica

Un sistema dinamico deterministico è descritto da
$$\frac{dx}{dt} = f(x,t),$$
mentre un sistema stocastico include un termine casuale:
$$\frac{dx}{dt} = f(x,t) + g(x,t)\,\eta(t),$$
dove $\eta(t)$ è un “rumore bianco” ideale: una variabile casuale con media nulla e varianza unitaria per ogni intervallo infinitesimo.

**Interpretazione:** il termine $f(x,t)$ rappresenta la tendenza media del sistema, mentre $g(x,t)\eta(t)$ introduce fluttuazioni imprevedibili.

---

## 3. Equazione di Langevin

L’equazione di Langevin nasce in fisica per descrivere il **moto browniano** di una particella:
$$m\frac{dv}{dt} = -\gamma v + \sqrt{2\gamma k_B T}\,\eta(t).$$

Il termine $-\gamma v$ rappresenta l’attrito, mentre $\sqrt{2\gamma k_B T}\,\eta(t)$ è la forza casuale dovuta alle collisioni molecolari.  
In forma semplificata:
$$\frac{dx}{dt} = f(x) + \sigma\,\eta(t).$$

Questa struttura è universale: può descrivere l’evoluzione di qualunque variabile soggetta a un equilibrio fra tendenza e fluttuazione.

---

## 4. Simulazioni numeriche di traiettorie

La versione discreta (schema di Euler–Maruyama) approssima l’evoluzione per passi di ampiezza $\Delta t$:
$$x_{n+1} = x_n + f(x_n)\,\Delta t + \sigma\sqrt{\Delta t}\,\xi_n,$$
dove $\xi_n$ è una variabile gaussiana standard ($\mathcal{N}(0,1)$).

**Esempio in Python:**

```python
import numpy as np
import matplotlib.pyplot as plt

def langevin(f, sigma, x0, dt, N):
    x = np.zeros(N)
    x[0] = x0
    for n in range(N-1):
        x[n+1] = x[n] + f(x[n])*dt + sigma*np.sqrt(dt)*np.random.randn()
    return x

# esempio: moto browniano con drift negativo
f = lambda x: -0.5*x
x = langevin(f, sigma=0.3, x0=1.0, dt=0.01, N=1000)
plt.plot(x)
plt.xlabel("passo temporale")
plt.ylabel("x")
plt.show()
````

Ogni simulazione produce una traiettoria diversa, ma l’andamento medio è prevedibile.

---

## 5. Esempi interdisciplinari

### 5.1 Fisica

Il moto browniano o la diffusione di calore sono descritti da equazioni stocastiche: la temperatura o la posizione media si evolvono in modo regolare, ma con fluttuazioni microscopiche.

### 5.2 Biologia

L’espressione genica è un processo rumoroso: la quantità di una proteina varia nel tempo anche in condizioni identiche. Le equazioni di Langevin descrivono le fluttuazioni intorno all’equilibrio.

### 5.3 Economia

Nei mercati finanziari, la variazione del prezzo $S_t$ è spesso modellata come
$$dS_t = \mu S_t,dt + \sigma S_t,dW_t,$$
dove $W_t$ è un processo di Wiener. Questo è il modello di **moto geometrico browniano**.

### 5.4 Scienze sociali e reti

Le decisioni individuali possono essere viste come processi rumorosi:
un agente cambia opinione con probabilità che fluttua nel tempo, oppure l’informazione si diffonde come particelle casuali su un grafo.

---

## Riferimenti

* Langevin, P. (1908). *Sur la théorie du mouvement brownien*. C. R. Acad. Sci. 146: 530–533.
* Gardiner, C. (2004). *Handbook of Stochastic Methods*. Springer.
* Risken, H. (1989). *The Fokker–Planck Equation*. Springer.
* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review, 43(3): 525–546.
* Gillespie, D. T. (2000). *The chemical Langevin equation*. J. Chem. Phys. 113(1): 297–306.

---



