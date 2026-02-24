---
title: "08: Dinamiche molecolari e sistemi a molti agenti"
author: ""
date: ""
---

La dinamica molecolare nasce per studiare l’evoluzione di sistemi fisici con molte particelle, ma i suoi principi si estendono naturalmente a ogni sistema formato da **unità interagenti**: atomi, cellule, individui, imprese o nodi di una rete.  
Ogni agente segue regole locali (forze, scelte, vincoli), ma dall’insieme emergono comportamenti collettivi complessi.

### Obiettivi didattici specifici

1. Comprendere i principi generali della **dinamica molecolare (MD)**.  
2. Collegare la MD ai modelli stocastici tramite la presenza di rumore e termalizzazione.  
3. Descrivere l’evoluzione di un sistema a **molti agenti interagenti**.  
4. Analizzare l’effetto delle interazioni locali (collisioni, attrazioni, repulsioni).  
5. Estendere il concetto di simulazione molecolare a contesti sociali o economici.

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Introduzione alla dinamica molecolare** – principi, equazioni del moto e interpretazione.  
2. **Interazioni e potenziali** – forze, energia e condizioni al contorno.  
3. **Aspetti computazionali** – integrazione numerica e conservazione dell’energia.  
4. **Dal micro al macro: sistemi a molti agenti** – analogie con modelli sociali e biologici.  
5. **Applicazioni interdisciplinari** – simulazioni fisiche, economiche, sociali.

## 1. Introduzione alla dinamica molecolare

La dinamica molecolare (MD) costituisce una tecnica computazionale sviluppata per studiare l’evoluzione temporale di sistemi composti da un numero elevato di unità elementari, tipicamente atomi o molecole. Nonostante la denominazione suggerisca un ambito esclusivamente chimico o fisico, l’approccio è oggi ampiamente utilizzato anche in biologia strutturale, scienza dei materiali, ingegneria, informatica, e in generale in tutti i contesti in cui sia rilevante modellare sistemi multi-agente governati da interazioni locali. La prospettiva interdisciplinare risiede nel fatto che MD non è altro che un metodo per integrare nel tempo un sistema di equazioni differenziali accoppiate: ciò che cambia tra campi diversi è la scelta delle variabili, dei potenziali e delle scale caratteristiche.

In un senso ampio, un modello di MD descrive l’evoluzione deterministica di un insieme di entità che interagiscono seguendo leggi di moto classiche. Esso fornisce quindi uno strumento per passare dal livello microscopico -- dove le dinamiche sono espresse in termini di forze e potenziali -- al livello mesoscopico o macroscopico, in cui emergono proprietà collettive quali viscosità, diffusione, stabilità delle strutture e fenomeni di auto-organizzazione. Tale collegamento è ottenuto tramite simulazioni numeriche che risolvono le equazioni del moto con passi temporali molto piccoli, mantenendo il controllo sistematico degli errori.

### 1.1 Equazioni del moto

In un sistema di $N$ particelle classiche, la dinamica è descritta dalle equazioni di Newton. Per ciascuna particella $i$, caratterizzata da massa $m_i$ e posizione $\mathbf{r}_i(t)$, vale la relazione
$$m_i \frac{d^{2}\mathbf{r}_i}{dt^{2}} = \mathbf{F}_i \, ,$$
dove $\mathbf{F}_i$ rappresenta la forza totale che agisce sulla particella. Questa forza è in generale la somma di contributi provenienti dalle interazioni con tutte le altre particelle del sistema, nonché da eventuali campi esterni. L’insieme delle equazioni forma un sistema accoppiato di dimensione $3N$, da integrare numericamente passo dopo passo.

Dal punto di vista interdisciplinare, è utile osservare che la struttura delle equazioni è formalmente analoga a quella che compare in modelli di altri domini: reti di agenti con interazioni deterministiche, modelli di folla, dinamiche di opinione con potenziali di attrazione e repulsione, oppure sistemi granulari. La specificità fisica risiede nella forma delle forze, ma lo schema algoritmico rimane invariato.

### 1.2 Conservazione e termalizzazione

Le forze interne del sistema sono usualmente derivate da un potenziale di interazione $U(\mathbf{r}_1,\dots,\mathbf{r}_N)$, così che
$$\mathbf{F}_i = -\nabla_i U \,.$$
Quando le interazioni sono conservative e non sono presenti sorgenti di rumore o accoppiamenti con un bagno termico, l’evoluzione nel tempo conserva l’energia meccanica totale del sistema,
$$E = K + U \,,$$
dove $K$ è l’energia cinetica complessiva e $U$ l’energia potenziale. Questa proprietà colloca la simulazione nel cosiddetto ensemble microcanonico (NVE) dove sono costanti il numero $N$ di particelle, il volume $V$ e lénergia totale $E$.

Tuttavia, nella maggior parte delle applicazioni pratiche è necessario rappresentare condizioni termiche specifiche, come temperatura costante o pressione controllata. Ciò richiede l’introduzione di termostati e barostati, ossia meccanismi algoritmici che modificano le equazioni del moto per mimare l’accoppiamento con un ambiente esterno. Questi strumenti permettono di riprodurre gli ensemble canonico (NVT - a *temperatura* fissata) e isobarico (NPT - a *pressione* fissata), rendendo MD utilizzabile per studiare fenomeni molto diversi: transizioni di fase, stabilità delle proteine, auto-assemblaggio di materiali, dinamiche collettive di agenti interagenti.

La capacità di collegare interazioni microscopiche e proprietà emergenti, indipendentemente dal dominio scientifico di riferimento, costituisce l’elemento centrale che rende MD uno strumento versatile per l’analisi di sistemi ad alta dimensionalità.

## 1. Introduzione alla dinamica molecolare

La **dinamica molecolare (MD)** è un metodo numerico per risolvere le equazioni del moto di un sistema di $N$ particelle.

### 1.1 Equazioni del moto

Per ciascuna particella $i$ di massa $m_i$ e posizione $\mathbf{r}_i$:
$$m_i \frac{d^2\mathbf{r}_i}{dt^2} = \mathbf{F}_i,$$
dove $\mathbf{F}_i$ è la forza risultante dovuta alle interazioni con le altre particelle.

### 1.2 Conservazione e termalizzazione

Le forze derivano in genere da un **potenziale di interazione** $U(\mathbf{r}_1, \dots, \mathbf{r}_N)$:
$$\mathbf{F}_i = -\nabla_i U.$$
L’energia totale $E = K + U$ (cinematica + potenziale) si conserva in assenza di rumore o termostati.

## 2. Interazioni e potenziali

### 2.1 Potenziale di Lennard–Jones

Un modello classico per le interazioni tra particelle neutre:
$$U(r) = 4\epsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right].$$
Il termine $r^{-12}$ rappresenta la repulsione a corta distanza, il termine $r^{-6}$ l’attrazione di van der Waals.

### 2.2 Potenziali semplici e modelli granulari

In simulazioni didattiche o sociali, si possono usare potenziali semplificati:

- **potenziale duro (hard spheres):** urto elastico, nessuna interazione a distanza,  
- **potenziale armonico:** interazione tipo molla,  
- **potenziale sociale:** repulsione a breve raggio, attrazione a lungo raggio (es. modelli di coesione).

## 3. Aspetti computazionali

### 3.1 Integrazione numerica

Le equazioni del moto sono integrate per passi discreti $\Delta t$:
$$\mathbf{r}_i(t+\Delta t) = \mathbf{r}_i(t) + \mathbf{v}_i(t)\Delta t + \frac{1}{2m_i}\mathbf{F}_i(t)\Delta t^2.$$

Il metodo **Verlet** (o Velocity Verlet) è spesso usato per la sua stabilità e conservazione dell’energia.

```python
import numpy as np

def verlet_step(r, v, F, m, dt, force_func):
    r_new = r + v*dt + 0.5*F/m*dt**2
    F_new = force_func(r_new)
    v_new = v + 0.5*(F + F_new)/m*dt
    return r_new, v_new, F_new
```

### 3.2 Condizioni al contorno

In un sistema finito si usano:

* **muri rigidi** (rimbalzo elastico),
* **condizioni periodiche** (il sistema si “ripete” su se stesso),
* **dissipazione o termostati** per simulare scambi di energia con l’ambiente.

## 4. Dal micro al macro: sistemi a molti agenti

Le regole di interazione non devono essere fisiche: possono rappresentare decisioni, preferenze, o strategie.
Un sistema a molti agenti può essere descritto da:
$$\frac{d\mathbf{x}_i}{dt} = \mathbf{f}_i(\mathbf{x}_1, \dots, \mathbf{x}_N) + \boldsymbol{\eta}_i(t),$$
dove $\mathbf{f}_i$ sintetizza la risposta dell’agente alle condizioni locali e $\boldsymbol{\eta}_i(t)$ rappresenta rumore o imprevedibilità.

### 4.1 Dinamiche di consenso

Esempio: ogni agente adatta la propria opinione alla media dei vicini:
$$x_i(t+\Delta t) = x_i(t) + \alpha\sum_{j\in\mathcal{N}_i}(x_j(t) - x_i(t)) + \xi_i(t),$$
dove $\mathcal{N}_i$ è il vicinato di $i$ e $\xi_i$ è un termine casuale.

### 4.2 Simulazione semplice

```python
import numpy as np
import matplotlib.pyplot as plt

N = 100
x = np.random.rand(N)
alpha = 0.1
for t in range(200):
    noise = 0.02*np.random.randn(N)
    x += alpha*(np.mean(x) - x) + noise

plt.hist(x, bins=15)
plt.xlabel("opinione finale")
plt.ylabel("frequenza")
plt.show()
```

Il sistema tende al consenso, con fluttuazioni residue dovute al rumore.

## 5. Applicazioni interdisciplinari

- **Fisica e chimica:** Simulazione di gas, liquidi e solidi; dinamiche di transizione di fase; collisioni e termalizzazione.
- **Biologia:** Movimento collettivo (flocking, swarming), dinamiche cellulari, auto-organizzazione di colonie.
- **Scienze sociali:** Modelli di interazione agent–based: diffusione di opinioni, aggregazione, polarizzazione, formazione di gruppi.
- **Economia e reti:** Simulazioni di mercati e di reti di scambio, con agenti che reagiscono a incentivi o interazioni locali, analoghe a forze in un sistema fisico.

## Riferimenti

* Allen, M. P., & Tildesley, D. J. (1987). *Computer Simulation of Liquids*. Oxford University Press.
* Frenkel, D., & Smit, B. (2002). *Understanding Molecular Simulation*. Academic Press.
* Helbing, D. (2012). *Social Self-Organization: Agent-Based Simulations and Experiments to Study Emergent Social Behavior*. Springer.
* Castellano, C., Fortuito, S., & Loreto, V. (2009). *Statistical physics of social dynamics*. Rev. Mod. Phys. 81: 591–646.
* Bonabeau, E. (2002). *Agent-based modeling: Methods and techniques for simulating human systems*. PNAS, 99(3): 7280–7287.

