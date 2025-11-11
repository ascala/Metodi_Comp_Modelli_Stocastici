---
title: "Boltzmann Machine e Sampling"
author: ""
date: ""
---

# Boltzmann Machine e Sampling

(Obiettivi della lezione: comprendere come la distribuzione di Boltzmann descriva sistemi complessi con molte variabili interagenti, introdurre la logica delle *Boltzmann Machines* come modelli probabilistici apprendibili, e illustrare i metodi di campionamento Monte Carlo utilizzati per stimare quantità termodinamiche e statistiche in reti di neuroni.)

---

### Obiettivi didattici specifici

1. Introdurre la **distribuzione di Boltzmann** come modello probabilistico fondamentale.  
2. Comprendere la struttura e il funzionamento di una **Boltzmann Machine (BM)**.  
3. Intuire il legame fra energia, probabilità e apprendimento.  
4. Esaminare il ruolo del **campionamento Monte Carlo** (Metropolis, Gibbs).  
5. Collegare i concetti fisici di equilibrio e temperatura all’ottimizzazione e al learning.

---

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Dalla fisica statistica ai modelli probabilistici** – energia e distribuzioni.  
2. **La distribuzione di Boltzmann** – interpretazione termodinamica e statistica.  
3. **La Boltzmann Machine** – architettura, funzione di energia e apprendimento.  
4. **Sampling e algoritmi di simulazione** – Metropolis, Gibbs sampling.  
5. **Applicazioni e connessioni interdisciplinari** – reti neurali, inferenza, ottimizzazione.

---

### Conclusione introduttiva

La teoria di Boltzmann lega energia e probabilità: gli stati di un sistema hanno maggiore o minore probabilità a seconda della loro energia.  
Questo principio, alla base della fisica statistica, è stato reinterpretato nel machine learning come un modello di apprendimento distribuito, dove le connessioni fra unità determinano la probabilità di configurazioni osservate.

---

## 1. Dalla fisica statistica ai modelli probabilistici

Un sistema con molte variabili interagenti può trovarsi in diversi stati $x$.  
A ciascuno stato si associa un’energia $E(x)$, che misura la sua “compatibilità” interna.

L’idea chiave è che gli stati a bassa energia siano più probabili:
$$P(x) \propto e^{-E(x)/T},$$
dove $T$ rappresenta la temperatura (grado di rumore o incertezza del sistema).

Nei modelli computazionali, $E(x)$ è una funzione che rappresenta le interazioni tra le variabili e i vincoli del sistema.

---

## 2. La distribuzione di Boltzmann

### 2.1 Forma generale

La probabilità di uno stato $x$ in equilibrio termico:
$$P(x) = \frac{1}{Z} e^{-E(x)/T},$$
dove
$$Z = \sum_x e^{-E(x)/T}$$
è la **funzione di partizione**, necessaria per normalizzare la distribuzione.

### 2.2 Interpretazione

- Stati a **bassa energia** → alta probabilità.  
- Stati ad **alta energia** → bassa probabilità.  
- La temperatura controlla il grado di esplorazione:  
  - $T$ grande → esplorazione ampia (stati anche improbabili).  
  - $T$ piccola → sistema “bloccato” vicino ai minimi di energia.

Questa distribuzione è il ponte fra **fisica** e **intelligenza artificiale**: la probabilità di uno stato riflette quanto esso è coerente con i vincoli appresi.

---

## 3. La Boltzmann Machine

### 3.1 Architettura

Una **Boltzmann Machine (BM)** è una rete di unità binarie $\{s_i\}$ collegate da pesi simmetrici $w_{ij}$:
$$E(s) = -\frac{1}{2}\sum_{i,j} w_{ij} s_i s_j - \sum_i b_i s_i.$$
Gli stati $s_i \in \{0,1\}$ rappresentano neuroni o variabili binarie.

### 3.2 Dinamica stocastica

Ogni unità si aggiorna con probabilità:
$$P(s_i = 1 | s_{-i}) = \frac{1}{1 + e^{-\Delta E_i/T}},$$
dove $\Delta E_i$ è la variazione di energia se $s_i$ passa da 0 a 1.

Questa regola è analoga al **campionamento di Gibbs**, e garantisce che, nel tempo, il sistema esplori la distribuzione di Boltzmann associata all’energia $E(s)$.

### 3.3 Apprendimento

L’obiettivo dell’apprendimento è modificare $w_{ij}$ e $b_i$ per ridurre la differenza tra la distribuzione appresa $P(s)$ e quella osservata nei dati.

Il gradiente dell’errore implica due termini:
$$\Delta w_{ij} \propto \langle s_i s_j \rangle_{\text{data}} - \langle s_i s_j \rangle_{\text{model}},$$
cioè la differenza fra correlazioni osservate e correlate generate dal modello.

---

## 4. Sampling e algoritmi di simulazione

Poiché $Z$ è in genere inaccessibile (richiede somma su troppi stati), si usano metodi di campionamento Monte Carlo.

### 4.1 Metropolis–Hastings

A ogni passo:
1. si propone una modifica dello stato (es. invertire un bit);  
2. si accetta con probabilità
$$p_{\text{acc}} = \min\left(1, e^{-\Delta E/T}\right);$$
3. si ripete per ottenere una sequenza di stati distribuiti secondo $P(x)$.

### 4.2 Gibbs sampling

Aggiornamento coordinato di singole variabili in base alle loro probabilità condizionate.  
È particolarmente efficiente per Boltzmann Machines, dove le unità sono indipendenti a parità delle altre.

### 4.3 Simulazione semplice

```python
import numpy as np

def metropolis_step(s, E, T):
    i = np.random.randint(len(s))
    s_new = s.copy()
    s_new[i] = 1 - s[i]
    dE = E(s_new) - E(s)
    if np.random.rand() < np.exp(-dE/T):
        return s_new
    else:
        return s

def energy(s):
    w = np.array([[0,1,1],[1,0,1],[1,1,0]])
    b = np.zeros(3)
    return -0.5*np.dot(s, w.dot(s)) - np.dot(b,s)

s = np.random.randint(0,2,3)
for _ in range(1000):
    s = metropolis_step(s, energy, T=1.0)
````

---

## 5. Applicazioni e connessioni interdisciplinari

### 5.1 Fisica statistica

Le Boltzmann Machines sono formalmente equivalenti a reti di spin di Ising, con il campionamento che simula l’equilibrio termico.

### 5.2 Machine learning

Le BM e le **Restricted Boltzmann Machines (RBM)** costituiscono la base di molte architetture di *deep learning* (es. autoencoder probabilistici, Deep Belief Networks).

### 5.3 Neuroscienze

Il modello energetico descrive reti neurali che si auto-organizzano per minimizzare l’energia, analogamente al cervello che riduce l’errore predittivo.

### 5.4 Economia e scienze sociali

L’equilibrio di Boltzmann può interpretarsi come una distribuzione di preferenze o scelte in un sistema collettivo con vincoli globali (es. mercati, reti di interazione).

---

## Riferimenti

* Ackley, D. H., Hinton, G. E., & Sejnowski, T. J. (1985). *A learning algorithm for Boltzmann Machines*. Cognitive Science, 9(1): 147–169.
* Hinton, G. E. (2002). *Training products of experts by minimizing contrastive divergence*. Neural Computation, 14(8): 1771–1800.
* Neal, R. M. (1993). *Probabilistic inference using Markov chain Monte Carlo methods*. Technical Report CRG-TR-93-1.
* Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
* Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.

---
