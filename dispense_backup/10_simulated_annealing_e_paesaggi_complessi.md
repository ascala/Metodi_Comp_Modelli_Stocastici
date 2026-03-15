---
title: "Simulated Annealing e Paesaggi Complessi"
author: ""
date: ""
---

# Simulated Annealing e Paesaggi Complessi

(Obiettivi della lezione: introdurre l’algoritmo di *simulated annealing* come metodo stocastico di ottimizzazione ispirato alla fisica statistica, comprendere il concetto di paesaggio di energia o costo, e discutere le implicazioni per problemi complessi, apprendimento e adattamento.)

---

### Obiettivi didattici specifici

1. Introdurre il concetto di **paesaggio energetico o di costo**.  
2. Comprendere la logica del **simulated annealing (SA)** e la sua ispirazione fisica.  
3. Analizzare il ruolo della **temperatura** e del **raffreddamento** nel controllo dell’esplorazione.  
4. Implementare e interpretare esempi di ottimizzazione stocastica.  
5. Collegare SA a sistemi complessi, reti, e apprendimento.

---

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Paesaggi di energia e problemi di ottimizzazione** – analogie tra fisica e informatica.  
2. **Principio del simulated annealing** – esplorazione stocastica controllata.  
3. **Algoritmo e parametri** – temperatura, schedule, criteri di accettazione.  
4. **Esempi numerici e interpretazioni** – funzioni multimodali, combinatoriali.  
5. **Applicazioni interdisciplinari** – fisica, machine learning, reti e società.

---

### Conclusione introduttiva

Molti sistemi naturali e computazionali devono trovare configurazioni “ottimali” tra un numero enorme di possibilità.  
Il *simulated annealing* traduce il processo fisico di **raffreddamento lento** di un materiale in un algoritmo di esplorazione globale del paesaggio di energia o costo, capace di evitare minimi locali e di avvicinarsi a configurazioni ottimali.

---

## 1. Paesaggi di energia e problemi di ottimizzazione

### 1.1 Paesaggio di energia

Ogni sistema o problema può essere rappresentato da una funzione di energia o costo $E(x)$ che associa a ogni configurazione $x$ un valore:
- basso → stato desiderabile o ottimale,  
- alto → stato sfavorevole.

La sfida è **trovare il minimo globale** di $E(x)$ in presenza di molti minimi locali.

### 1.2 Analogia fisica

Nel raffreddamento di un solido, le particelle si organizzano in configurazioni sempre più stabili man mano che la temperatura scende.  
Un raffreddamento troppo rapido porta a **vetri amorfi** (minimi locali); uno lento conduce a **cristalli perfetti** (minimo globale).

---

## 2. Principio del simulated annealing

L’algoritmo riproduce la dinamica di un sistema termico che esplora configurazioni secondo la distribuzione di Boltzmann:
$$
P(x) \propto e^{-E(x)/T}.
$$

A ogni passo:
1. Si propone una nuova configurazione $x'$.  
2. Si calcola la variazione di energia $\Delta E = E(x') - E(x)$.  
3. Si accetta la mossa con probabilità
$$
p_{\text{acc}} = \min(1, e^{-\Delta E/T}).
$$

La temperatura $T$ controlla il grado di esplorazione:
- alta $T$ → accettazione di molte mosse, anche peggiorative;  
- bassa $T$ → esplorazione fine intorno ai minimi.

---

## 3. Algoritmo e parametri

### 3.1 Schema generale

```python
import numpy as np

def simulated_annealing(E, x0, T0, alpha, steps):
    x = x0
    E_curr = E(x)
    T = T0
    history = [E_curr]
    for _ in range(steps):
        x_new = x + np.random.normal(0, 1)
        E_new = E(x_new)
        if np.random.rand() < np.exp(-(E_new - E_curr)/T):
            x, E_curr = x_new, E_new
        history.append(E_curr)
        T *= alpha  # raffreddamento geometrico
    return x, history
````

### 3.2 Parametri principali

* **$T_0$**: temperatura iniziale (esplorazione ampia).
* **$\alpha$**: coefficiente di raffreddamento (tipicamente $0.95$–$0.99$).
* **Numero di passi**: determina il tempo di esplorazione.
* **Schedule**: può essere lineare, geometrico o adattivo.

---

## 4. Esempi numerici e interpretazioni

### 4.1 Funzione multimodale

Esempio con una funzione con più minimi locali:
$$
E(x) = x^4 - 3x^3 + 2.
$$

```python
def E(x): return x**4 - 3*x**3 + 2
x_best, history = simulated_annealing(E, x0=0.0, T0=5.0, alpha=0.98, steps=500)
```

Durante il raffreddamento, il sistema accetta mosse verso stati peggiori all’inizio (per esplorare), ma alla fine converge verso il minimo globale.

### 4.2 Paesaggi combinatoriali

Il SA si applica anche a problemi discreti, come:

* **Traveling Salesman Problem (TSP)**,
* **colorazione di grafi**,
* **ottimizzazione di layout**,
* **allocazione di risorse**.

Le “mosse” corrispondono a piccole permutazioni, e l’energia è il costo totale della soluzione.

---

## 5. Applicazioni interdisciplinari

### 5.1 Fisica statistica

Il SA è un’estensione algoritmica del processo di termalizzazione: trova minimi globali del potenziale di energia in sistemi con molti gradi di libertà.

### 5.2 Machine learning

Può essere usato per inizializzare reti neurali o per ottimizzare funzioni di perdita non convexe.
In modelli energetici (Boltzmann Machines, Hopfield Networks), il raffreddamento corrisponde al processo di apprendimento.

### 5.3 Biologia

Descrizione di folding proteico: la proteina “esplora” configurazioni energetiche e si stabilizza nella conformazione più stabile.

### 5.4 Economia e reti sociali

Interpretazione come **processo di decisione collettiva**: gli agenti esplorano strategie o opinioni e gradualmente convergono verso stati più stabili o coerenti.

---

## Riferimenti

* Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). *Optimization by Simulated Annealing*. Science, 220(4598): 671–680.
* Aarts, E., & Korst, J. (1989). *Simulated Annealing and Boltzmann Machines*. Wiley.
* Neal, R. M. (1993). *Probabilistic inference using Markov chain Monte Carlo methods*. Technical Report CRG-TR-93-1.
* Binder, K., & Heermann, D. W. (2010). *Monte Carlo Simulation in Statistical Physics*. Springer.
* Mezard, M., Parisi, G., & Virasoro, M. (1987). *Spin Glass Theory and Beyond*. World Scientific.

---
