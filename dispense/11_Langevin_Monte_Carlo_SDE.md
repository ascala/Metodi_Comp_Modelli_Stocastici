---
title: "11: Langevin Monte Carlo e modelli generativi basati su SDE"
author: "Antonio Scala"
date: ""
---

# Langevin Monte Carlo e modelli generativi continui

Le dinamiche di Langevin introducono in modo naturale il **rumore termico** e permettono di collegare la dinamica molecolare deterministica con i metodi stocastici utilizzati in statistica computazionale, apprendimento automatico e modelli generativi.  
Le **SDE (Stochastic Differential Equations)** forniscono inoltre una base matematica unificata per descrivere sia processi fisici termalizzati sia dinamiche di campionamento e trasformazioni generative.

### Obiettivi didattici specifici

1. Comprendere la struttura generale delle equazioni di **Langevin** e il loro significato fisico.  
2. Collegare tali equazioni a schemi di **Monte Carlo** per il campionamento (Langevin MC, Hamiltonian MC, SG-LD).  
3. Introdurre le **SDE come modelli generativi** (VeVP, VP-SDE, modelli di diffusione).  
4. Analizzare schemi numerici per SDE: Euler--Maruyama, integrazione con drift e diffusione.  
5. Illustrare applicazioni interdisciplinari in fisica, machine learning e data science.

### Struttura della lezione

1. **Equazioni di Langevin** – interpretazione fisica e matematica.  
2. **Campionamento basato su SDE** – Langevin MC, SG-LD, HMC con dissipazione.  
3. **Modelli generativi basati su SDE** – forward diffusion, reverse-time SDE, score-based models.  
4. **Integrazione numerica delle SDE** – stabilità e convergenza.  
5. **Applicazioni interdisciplinari** – fisica, biologia, apprendimento automatico.

# 1. Equazioni di Langevin

La dinamica di Langevin modella un sistema soggetto a forze deterministiche e rumore termico.  
Per una particella di massa $m$ con posizione $\mathbf{x}$ e velocità $\mathbf{v}$:

$$
m \frac{d\mathbf{v}}{dt} = -\gamma \mathbf{v} - \nabla U(\mathbf{x}) + \sqrt{2\gamma k_B T}\,\boldsymbol{\eta}(t),
$$

con:
- $\gamma$ coefficiente di dissipazione,
- $U$ potenziale,
- $\boldsymbol{\eta}(t)$ rumore gaussiano bianco con varianza unitaria.

## 1.1 Forma sovra-smorzata

Nel limite di forti attriti:

$$
\frac{d\mathbf{x}}{dt} = -\nabla U(\mathbf{x}) + \sqrt{\frac{2}{\beta}}\,\boldsymbol{\eta}(t),
$$

dove $\beta = 1/k_B T$.  
Questa equazione costituisce la base per molti algoritmi di campionamento.

## 1.2 Legame con la distribuzione di equilibrio

La densità stazionaria della SDE è la misura di Boltzmann:

$$
\pi(\mathbf{x}) \propto e^{-\beta U(\mathbf{x})}.
$$

Questo collegamento consente di usare le dinamiche di Langevin come **metodo di campionamento**.

# 2. Campionamento tramite Langevin Monte Carlo

## 2.1 Euler--Maruyama e Unadjusted Langevin Algorithm (ULA)

Data la SDE:

$$
d\mathbf{x}_t = -\nabla U(\mathbf{x}_t)\,dt + \sqrt{2}\,d\mathbf{W}_t,
$$

lo schema di Euler--Maruyama produce:

$$
\mathbf{x}_{k+1} = \mathbf{x}_k - h \nabla U(\mathbf{x}_k) + \sqrt{2h}\,\boldsymbol{\xi}_k,
$$

con $\boldsymbol{\xi}_k \sim \mathcal{N}(0,I)$.

### Codice di esempio

```python
import numpy as np

def ula_step(x, gradU, h):
    noise = np.sqrt(2*h) * np.random.randn(*x.shape)
    return x - h * gradU(x) + noise
````

## 2.2 Langevin Monte Carlo corretto (MALA)

Si applica un passo di Metropolis--Hastings per correggere il bias della discretizzazione.
La proposta:

$$
q(\mathbf{x}'|\mathbf{x}) = \mathcal{N}(\mathbf{x} - h\nabla U(\mathbf{x}), 2hI)
$$

viene accettata con probabilità:

$$
\alpha = \min\left(1, \frac{\pi(\mathbf{x}') q(\mathbf{x}|\mathbf{x}')}{\pi(\mathbf{x}) q(\mathbf{x}'|\mathbf{x})} \right).
$$

## 2.3 Stochastic Gradient Langevin Dynamics (SGLD)

Quando $U = \sum_{i=1}^N U_i$ è somma su un dataset, si usa una stima stocastica del gradiente:

$$
\mathbf{x}_{k+1} = \mathbf{x}_k - h_k \widehat{\nabla U}(\mathbf{x}_k) + \sqrt{2h_k},\boldsymbol{\xi}_k,
$$

con $h_k$ gradualmente decrescente.

# 3. SDE per modelli generativi

I **modelli di diffusione** e gli **score-based generative models** descrivono una trasformazione graduale di un dato in rumore (forward SDE) e la corrispondente dinamica inversa (reverse-time SDE).

## 3.1 Forward SDE

Forma generale:

$$
d\mathbf{x}_t = f(\mathbf{x}_t, t),dt + g(t),d\mathbf{W}_t,
$$

con soluzioni che portano progressivamente a una distribuzione gaussiana.

Esempio di **Variance Exploding (VE) SDE**:

$$
d\mathbf{x}_t = g(t) d\mathbf{W}_t.
$$

## 3.2 Reverse-time SDE

Data la forward SDE, la reverse SDE è:

$$
d\mathbf{x}_t = \big[f(\mathbf{x}*t,t) - g(t)^2 \nabla*{\mathbf{x}} \log p_t(\mathbf{x}_t)\big] dt + g(t) d\mathbf{W}_t,
$$

dove $\nabla_{\mathbf{x}} \log p_t$ è lo **score**, appreso da una rete neurale.

## 3.3 Processo generativo

1. Si parte da $\mathbf{x}_T \sim \mathcal{N}(0, I)$.
2. Si integra la reverse SDE verso $t=0$.
3. Si ottiene una nuova istanza sintetica $\mathbf{x}_0$.

# 4. Integrazione numerica delle SDE

## 4.1 Schema di Euler--Maruyama

Per una SDE $dx_t = a(x_t,t)dt + b(x_t,t)dW_t$:

$$
x_{k+1} = x_k + a(x_k,t_k) h + b(x_k,t_k) \sqrt{h} \xi_k.
$$

## 4.2 Stabilità e passi adattivi

* Passi troppo grandi introducono bias.
* Passi troppo piccoli rallentano la simulazione.
* Nelle SDE dei modelli generativi si usano spesso **schedulazioni temporali** per $g(t)$ e per il passo numerico.

### Esempio numerico semplice

```python
def euler_maruyama(x0, drift, diffusion, h, steps):
    x = x0
    traj = [x0]
    for k in range(steps):
        xi = np.random.randn(*x.shape)
        x = x + drift(x) * h + diffusion(x) * np.sqrt(h) * xi
        traj.append(x)
    return np.array(traj)
```

# 5. Applicazioni interdisciplinari

## 5.1 Fisica computazionale

* Sistemi dissipativi e termalizzati.
* Modelli granulari e colloidali.
* Diffusione e trasporto.

## 5.2 Machine Learning

* Campionamento bayesiano.
* Addestramento con SG-LD.
* Modelli generativi di ultima generazione (score-based, diffusion models).

## 5.3 Biologia

* Movimento cellulare con chemotassi rumorosa.
* Modelli di dinamica di popolazione con fluttuazioni ambientali.
* Evoluzione stocastica di sistemi complessi.

## 5.4 Scienze sociali ed economia

* Dinamiche di volatilità nei mercati finanziari: SDE tipo Ornstein--Uhlenbeck.
* Scelte con rumore: modelli logit dinamici.
* Diffusione stocastica di informazioni e innovazioni.

# Riferimenti

* Roberts, G., & Tweedie, R. (1996). *Exponential convergence of Langevin diffusions and their discretisations*.
* Welling, M., & Teh, Y. W. (2011). *Bayesian learning via stochastic gradient Langevin dynamics*.
* Song, Y., & Ermon, S. (2020). *Score-based generative modelling through stochastic differential equations*.
* Pavliotis, G. (2014). *Stochastic Processes and Applications*. Springer.
* Risken, H. (1989). *The Fokker--Planck Equation*. Springer.

