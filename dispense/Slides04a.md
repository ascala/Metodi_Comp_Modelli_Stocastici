---
title: "S04a Entropia, logaritmi e massima entropia"
author: "Antonio Scala"
date: ""
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

## Perché compare il logaritmo?

### Osservazione

Molte quantità hanno forma:

$$
\log p \qquad \text{oppure} \qquad e^{-x}
$$

### Domanda

Perché non lavorare direttamente con $p$?

---

## Prodotti → somme

### Probabilità indipendenti

$$
P = \prod_{i=1}^n p_i
$$

### Con il logaritmo

$$
\log P = \sum_{i=1}^n \log p_i
$$

### Messaggio

Il logaritmo rende **additive** quantità moltiplicative

---

## Sorpresa matematica

### Idea

Eventi rari sono più "sorprendenti"

### Definizione

$$
I = \log\frac{1}{p} = -\log p
$$

### Proprietà

- $p$ piccolo → sorpresa grande  
- eventi indipendenti → sorpresa additiva  

---

## Entropia

### Sorpresa media

$$
H = -\sum_i p_i \log p_i
$$

### Interpretazione

- misura l'incertezza  
- massima per distribuzione uniforme  
- minima per evento certo  

---

## Likelihood e log-likelihood

### Likelihood (parametri  $\theta$, osservazioni $x_i$ [indipendenti]{.underline})

$$
L(\theta) = \prod_i p(x_i \mid \theta)
$$

### Log-likelihood

$$
\ell(\theta) = \sum_i \log p(x_i \mid \theta)
$$

### Perché usarla?

- somme invece di prodotti  
- più stabile numericamente  
- più facile da ottimizzare  

---

## Massima entropia

### Idea (Jaynes)

Scegliere la distribuzione "più ignorante", ovvero che massimizzi l'entropia $\mathcal{H}(x)$ compatibilmente con i vincoli $g_i(x)=0$

### Tecnica: moltiplicatori di Lagrange

1. Costruisco la Lagrangiana $\mathcal{L}=\mathcal{H}-\sum_i \lambda_i g_i$
2. Trovo i punti stazionari imponendo $\frac{\partial \mathcal{L}}{\partial x_j}=0 \,,\, \frac{\partial \mathcal{L}}{\partial \lambda_i}=0$
3. Le equazioni ottenute rispetto alle $\lambda_i$ restituiscono proprio i vincoli $g_i(x)=0$

Risolvendo il sistema si ottiene la distribuzione che massimizza l'entropia compatibilmente con l'informazione disponibile

### Risultato tipico

$$
p_i \propto e^{-\beta x_i}
$$

---

## Determinazione di $\beta$

### Vincolo

$$
\sum_i x_i p_i = m
$$

### Equazione

$$
\sum_i x_i \frac{e^{-\beta x_i}}{Z(\beta)} = m
$$

### Idea

Si sceglie $\beta$ per ottenere il valore medio desiderato

---

## Take-home message

- il logaritmo rende additive quantità probabilistiche  
- misura la **sorpresa**  
- porta naturalmente all’entropia  
- semplifica la statistica (log-likelihood)  
- genera distribuzioni esponenziali (MaxEnt)