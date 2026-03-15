---
title: "Modelli di crescita e branching"
author: ""
date: ""
---

# Modelli di crescita e branching

La crescita è un fenomeno universale ma raramente regolare.  
I modelli deterministici forniscono una visione media, ma non descrivono la **variabilità** e l’**imprevedibilità** osservate nei sistemi reali.  
I modelli di crescita e branching introducono il caso come componente dinamica, permettendo di analizzare la probabilità di espansione o estinzione di popolazioni, idee o strutture sociali.
I principali modelli di crescita stocastica e di ramificazione permettono infatti di comprendere il ruolo della casualità nella dinamica di popolazioni o sistemi in espansione, e analizzare applicazioni interdisciplinari in biologia, epidemiologia, economia e reti.


### Obiettivi didattici specifici

1. Comprendere la differenza tra crescita deterministica e stocastica.  
2. Introdurre la logica dei **processi di branching** e il concetto di estinzione.  
3. Analizzare esempi numerici e simulazioni di crescita casuale.  
4. Introdurre varianti continue (Yule, logistica stocastica).  
5. Collegare i modelli di crescita a fenomeni reali in diversi ambiti disciplinari.


### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Crescita deterministica e stocastica** – differenze concettuali e modelli base.  
2. **Processo di branching (Galton–Watson)** – definizione, interpretazione, simulazione.  
3. **Distribuzioni e probabilità di estinzione** – comportamento medio e varianza.  
4. **Modelli di crescita continua e varianti** – Yule, logistica, processi moltiplicativi.  
5. **Applicazioni interdisciplinari** – biologia, epidemie, reti, economia.


---

## 1. Crescita deterministica e stocastica

### 1.1 Crescita deterministica

Il modello di crescita esponenziale classico:
$$\frac{dN}{dt} = rN$$
ha soluzione $N(t) = N_0 e^{rt}$, dove $r$ è il tasso di crescita.  
Tutti gli individui o agenti seguono la stessa legge, senza fluttuazioni.

### 1.2 Crescita stocastica

Nei sistemi reali, la crescita è soggetta a variazioni casuali:
$$\frac{dN}{dt} = rN + \sigma N \eta(t),$$
dove $\eta(t)$ è un rumore bianco gaussiano.  
Le fluttuazioni amplificano o riducono localmente la crescita, e i risultati cambiano a ogni simulazione.

---

## 2. Processo di branching (Galton–Watson)

### 2.1 Definizione

Ogni individuo produce un numero casuale di discendenti $K$, con distribuzione $P(K=k)$.  
Il numero totale alla generazione $t+1$ è:
$$N_{t+1} = \sum_{i=1}^{N_t} K_i.$$

### 2.2 Valore medio e soglia critica

Il numero medio di figli è $m = \mathbb{E}[K]$:
- Se $m < 1$: estinzione certa.  
- Se $m = 1$: crescita marginale, forte varianza.  
- Se $m > 1$: crescita potenzialmente illimitata.

### 2.3 Simulazione discreta

```python
import numpy as np

def branching_process(N0, p_offspring, steps):
    N = [N0]
    for t in range(steps):
        total = 0
        for i in range(N[-1]):
            total += np.random.choice(list(p_offspring.keys()), p=list(p_offspring.values()))
        N.append(total)
    return N

# distribuzione di figli: 0, 1, 2 con probabilità 0.3, 0.4, 0.3
p = {0:0.3, 1:0.4, 2:0.3}
trajectory = branching_process(1, p, 20)
print(trajectory)
````

Ogni realizzazione può portare a estinzione o crescita esplosiva, anche con gli stessi parametri.

---

## 3. Distribuzioni e probabilità di estinzione

### 3.1 Equazione di estinzione

Sia $q$ la probabilità che il processo si estingua. Essa soddisfa:
$$q = G(q),$$
dove $G(s) = \sum_k P(K=k)s^k$ è la funzione generatrice della distribuzione dei figli.

* Se $m \le 1$, l’unica soluzione è $q = 1$ (estinzione certa).
* Se $m > 1$, esiste una soluzione $q < 1$ (sopravvivenza possibile).

### 3.2 Comportamento delle distribuzioni

La distribuzione di $N_t$ è altamente asimmetrica:

* molti casi con $N_t=0$,
* pochi con crescita molto elevata.
  È un esempio di **distribuzione heavy-tailed**, tipica dei fenomeni auto-rinforzanti.

---

## 4. Modelli di crescita continua e varianti

### 4.1 Processo di Yule (crescita pura)

Ogni individuo genera nuovi individui con tasso $\lambda$:
$$\frac{dN}{dt} = \lambda N.$$
Il numero totale segue in media $N(t) = N_0 e^{\lambda t}$, ma con fluttuazioni lognormali.

### 4.2 Crescita logistica stocastica

Quando le risorse sono limitate:
$$\frac{dN}{dt} = rN(1 - N/K) + \sigma N \eta(t),$$
dove $K$ è la capacità portante.
Il termine rumoroso introduce oscillazioni intorno all’equilibrio.

### 4.3 Simulazione di crescita logistica stocastica

```python
import numpy as np
import matplotlib.pyplot as plt

def logistic_stochastic(N0, r, K, sigma, dt, steps):
    N = np.zeros(steps)
    N[0] = N0
    for t in range(steps-1):
        dN = r*N[t]*(1 - N[t]/K)*dt + sigma*N[t]*np.sqrt(dt)*np.random.randn()
        N[t+1] = max(N[t] + dN, 0)
    return N

N = logistic_stochastic(10, r=0.5, K=100, sigma=0.2, dt=0.01, steps=2000)
plt.plot(N)
plt.xlabel("tempo")
plt.ylabel("popolazione N(t)")
plt.show()
```

---

## 5. Applicazioni interdisciplinari

### 5.1 Biologia

Crescita cellulare, diffusione di specie, mutazioni genetiche: ogni individuo o gene può duplicarsi o estinguersi casualmente.

### 5.2 Epidemiologia

Ogni infetto genera un numero casuale di nuovi contagi $K$.
Il numero medio $R_0 = \mathbb{E}[K]$ stabilisce la soglia epidemica:

* $R_0 < 1$ → la malattia scompare,
* $R_0 > 1$ → epidemia potenzialmente esplosiva.

### 5.3 Economia e finanza

I processi di crescita moltiplicativa generano distribuzioni di reddito o dimensioni d’impresa **log-normali** e **power-law**, con molte unità piccole e poche molto grandi.

### 5.4 Reti e innovazione

La formazione di nuove connessioni in una rete segue spesso una dinamica di tipo branching: ogni nodo può generare nuovi collegamenti in modo probabilistico.

---

## Riferimenti

* Harris, T. E. (1963). *The Theory of Branching Processes*. Springer.
* Kimmel, M., & Axelrod, D. E. (2002). *Branching Processes in Biology*. Springer.
* Allen, L. J. S. (2003). *An Introduction to Stochastic Processes with Applications to Biology*. Pearson.
* Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
* Mitzenmacher, M. (2004). *A Brief History of Generative Models for Power Law and Lognormal Distributions*. Internet Mathematics, 1(2): 226–251.

---

