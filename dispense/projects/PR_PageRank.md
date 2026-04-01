---
title: "Project: Random walk su grafi, assorbimento e PageRank"
subtitle: "catene di Markov su reti, hitting probabilities, stationary distribution e centralità dinamica"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce i **random walk su grafi** come caso di studio fondamentale per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare una passeggiata casuale su un grafo come **catena di Markov discreta** su spazio finito;
2. introdurre le nozioni di distribuzione stazionaria, hitting probability, first-passage time e stati assorbenti;
3. mostrare come la struttura topologica del grafo influenzi il comportamento dinamico del walker;
4. distinguere tra random walk su grafi non orientati e orientati;
5. introdurre PageRank come estensione di un random walk con teleportation;
6. discutere come una centralità dinamica differisca da misure puramente topologiche.

Dal punto di vista del corso, questo progetto è particolarmente importante perché fornisce una piattaforma estremamente chiara per studiare le **catene di Markov finite**. Molti altri modelli del corso usano idee simili in modo implicito, ma qui esse diventano l'oggetto diretto dell'analisi.

# 2. Motivazione generale

Una grande varietà di problemi può essere ricondotta a una dinamica di passeggiata casuale su una rete.

## 2.1 Navigazione sul web

Un utente che segue casualmente link ipertestuali da una pagina all'altra compie, in prima approssimazione, un random walk su un grafo orientato. PageRank nasce precisamente da questa intuizione.

## 2.2 Diffusione di informazione e ricerca casuale

Un'informazione, un agente o un messaggio che si muovono localmente su una rete possono essere descritti in termini di probabilità di transizione tra nodi adiacenti.

## 2.3 Reti di trasporto e mobilità

Se un agente sceglie casualmente quale strada percorrere a ogni incrocio, il suo movimento diventa un random walk su grafo. La probabilità di raggiungere certe zone e il tempo medio di arrivo dipendono allora in modo cruciale dalla struttura della rete.

## 2.4 Assorbimento, bersagli e stati di fallimento

In molti problemi interessa sapere:

* con quale probabilità un processo raggiunge un certo target;
* quanto tempo impiega in media a farlo;
* se viene assorbito in uno stato desiderato oppure in uno stato di perdita.

Questo rende i random walk con stati assorbenti un caso di studio estremamente utile.

## 2.5 Ranking e centralità dinamica

Un nodo può essere centrale non solo perché ha molti collegamenti, ma perché viene visitato spesso da una dinamica naturale di navigazione. Questa è precisamente l'idea dietro PageRank.

# 3. Struttura matematica del modello

## 3.1 Grafo e matrice di transizione

Consideriamo un grafo con $N$ nodi. Il random walk è definito da una matrice di transizione

$$
P=(p_{ij}),
$$

dove $p_{ij}$ è la probabilità che il walker passi dal nodo $i$ al nodo $j$ in un singolo passo.

Le righe di $P$ soddisfano

$$
p_{ij} \ge 0,
\qquad
\sum_{j=1}^N p_{ij}=1.
$$

Lo stato del sistema al tempo $t$ è il nodo occupato dal walker, oppure equivalentemente una distribuzione di probabilità sui nodi.

## 3.2 Caso semplice: grafo non orientato

Se il grafo è non orientato e il walker sceglie uniformemente tra i vicini del nodo corrente, allora

$$
p_{ij} = \frac{1}{k_i}
$$

se $j$ è vicino di $i$, dove $k_i$ è il grado del nodo $i$.

Questa scelta è la più naturale e costituisce il modello base del progetto.

## 3.3 Evoluzione della distribuzione

Se $\pi(t)$ è il vettore riga delle probabilità di occupazione al tempo $t$, allora

$$
\pi(t+1) = \pi(t)P.
$$

Questa equazione è la forma fondamentale della dinamica markoviana discreta.

# 4. Distribuzione stazionaria

## 4.1 Definizione

Una distribuzione stazionaria è un vettore $\pi$ tale che

$$
\pi = \pi P.
$$

Se il processo è irriducibile e aperiodico su uno spazio finito, questa distribuzione esiste, è unica, e il sistema vi converge da qualunque condizione iniziale.

## 4.2 Caso non orientato

Per un random walk semplice su grafo non orientato, la distribuzione stazionaria è proporzionale al grado:

$$
\pi_i = \frac{k_i}{\sum_j k_j}.
$$

Questo è un risultato molto importante: i nodi di grado alto vengono visitati più spesso, ma la centralità dinamica è qui legata in modo diretto alla struttura topologica locale.

## 4.3 Significato

La distribuzione stazionaria misura il tempo relativo trascorso dal walker in ciascun nodo nel lungo tempo. È quindi una misura naturale di “importanza dinamica” dei nodi.

# 5. Tempi di ritorno, hitting e first-passage

## 5.1 Tempo medio di ritorno

Se il processo è stazionario, il tempo medio di ritorno al nodo $i$ è collegato alla distribuzione stazionaria dalla relazione

$$
\mathbb{E}[T_{i\to i}^{\mathrm{return}}] = \frac{1}{\pi_i}.
$$

Questa formula è molto istruttiva perché lega una proprietà dinamica del cammino a una proprietà statica del processo.

## 5.2 Hitting probability

Data una coppia di insiemi bersaglio, si può chiedere qual è la probabilità di raggiungere un insieme prima dell'altro. Questo problema compare naturalmente in contesti di scelta, fallimento o assorbimento competitivo.

## 5.3 First-passage time

Dato un nodo target $j$, il **first-passage time** da $i$ a $j$ è il numero di passi necessari per raggiungere $j$ per la prima volta partendo da $i$.

Questa quantità è una delle più importanti dell'intero progetto, perché misura l'accessibilità dinamica e non solo topologica.

# 6. Stati assorbenti

## 6.1 Definizione

Uno stato assorbente è un nodo $a$ tale che

$$
p_{aa}=1.
$$

Una volta raggiunto, il walker vi resta per sempre.

## 6.2 Decomposizione della matrice

Se si separano i nodi transienti da quelli assorbenti, la matrice di transizione può essere scritta in forma a blocchi. Questo consente di studiare:

* probabilità di assorbimento in ciascun target;
* tempi medi di assorbimento;
* dipendenza dai nodi iniziali.

## 6.3 Significato applicativo

Gli stati assorbenti possono rappresentare:

* raggiungimento di un obiettivo;
* fallimento del processo;
* uscita da un sistema;
* cattura, morte o arresto.

Per questo i random walk assorbenti hanno un valore applicativo molto ampio.

# 7. Grafi orientati e problemi di ergodicità

Su grafi orientati la situazione si complica. Possono comparire:

* nodi irraggiungibili da certi altri;
* classi chiuse;
* stati ricorrenti non comunicanti;
* periodicità.

In questi casi la distribuzione stazionaria può:

* non essere unica;
* dipendere dalla componente iniziale;
* non essere raggiunta in modo semplice da ogni condizione iniziale.

Questo è precisamente il motivo per cui PageRank introduce il meccanismo di teleportation.

# 8. PageRank

## 8.1 Idea di base

PageRank nasce dall'idea di un navigatore casuale che, con alta probabilità, segue un link uscente dalla pagina corrente, ma con una piccola probabilità “si annoia” e salta a una pagina scelta indipendentemente dalla struttura locale.

## 8.2 Matrice di transizione con teleportation

Se $P$ è la matrice di transizione del random walk sul grafo, si costruisce una matrice modificata

$$
P' = \gamma P + (1-\gamma) \mathbf{1}v^T,
$$

dove:

* $\gamma \in (0,1)$ è il **damping factor**;
* $v$ è una distribuzione di teleportation, spesso uniforme;
* $\mathbf{1}v^T$ rappresenta il salto casuale globale.

## 8.3 Ruolo del damping factor

Il parametro $\gamma$ controlla il compromesso tra:

* esplorazione locale della rete;
* salti globali indipendenti dai link.

Valori tipici sono vicini a 1, ma non uguali a 1, proprio per garantire una dinamica ben definita e robusta.

## 8.4 Perché PageRank è importante

PageRank non misura soltanto quanti link puntano a un nodo, ma quanto un nodo venga visitato da una dinamica di navigazione lunga e iterata. Per questo è una centralità genuinamente dinamica.

# 9. Interpretazione lineare e computazionale

Dal punto di vista matematico, sia i random walk sia PageRank collegano in modo molto naturale:

* matrici di transizione;
* autovettori sinistri associati all'autovalore 1;
* iterazione numerica;
* stabilità e convergenza.

Questo rende il progetto ideale per far vedere agli studenti il legame tra:

* probabilità;
* algebra lineare;
* simulazione Monte Carlo;
* algoritmi di ranking.

# 10. Osservabili da misurare

Per trasformare il progetto in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 10.1 Distribuzione stazionaria

La distribuzione stazionaria $\pi$ è la quantità di base.

## 10.2 Tempo medio di ritorno

Misura quanto rapidamente il walker torna in un nodo tipico.

## 10.3 Hitting times e first-passage times

Permettono di quantificare l'accessibilità dinamica tra nodi o tra sottoinsiemi di nodi.

## 10.4 Probabilità di assorbimento

Nel caso con target multipli assorbenti, questa quantità è fondamentale per capire quale esito sia più probabile a seconda della posizione iniziale.

## 10.5 Ranking dinamico

Nel caso PageRank, il vettore stazionario della matrice modificata fornisce un ordinamento dei nodi in termini di centralità dinamica.

# 11. Domande scientifiche che il progetto permette di studiare

1. Come la topologia influenza la distribuzione stazionaria?
2. Quali nodi vengono visitati più spesso nel lungo tempo?
3. Come si calcolano e si interpretano i tempi medi di first passage?
4. Quali nodi sono più facilmente raggiungibili e quali più periferici dal punto di vista dinamico?
5. In che senso gli stati assorbenti cambiano radicalmente la natura del problema?
6. Perché PageRank è una centralità dinamica e non puramente topologica?
7. Qual è il ruolo del teleportation nel rendere il processo ergodico e numericamente stabile?

# 12. Pseudocodice del modello

## 12.1 Input

* grafo o matrice di adiacenza
* matrice di transizione $P$
* distribuzione iniziale del walker oppure nodo iniziale
* numero massimo di passi $T$
* eventuali nodi assorbenti
* damping factor $\gamma$ e vettore $v$ per PageRank
* numero di realizzazioni indipendenti $R$

## 12.2 Pseudocodice: random walk semplice

```text
Inizializza il grafo e costruisci la matrice di transizione P
Scegli il nodo iniziale i0
Poni i <- i0

Per t = 0, ..., T-1:
    scegli il nodo successivo j secondo la distribuzione P[i,:]
    poni i <- j
    registra eventualmente:
        - nodo visitato
        - numero di visite per nodo
        - tempo del primo arrivo in nodi bersaglio
```

## 12.3 Pseudocodice: random walk con assorbimento

```text
Inizializza il grafo e la matrice di transizione P
Rendi assorbenti alcuni nodi target
Scegli il nodo iniziale i0
Poni i <- i0
Poni t <- 0

Finché i non è assorbente e t < T:
    scegli j secondo P[i,:]
    poni i <- j
    incrementa t

Registra:
    - nodo di assorbimento
    - tempo di assorbimento
```

## 12.4 Pseudocodice: PageRank via iterazione

```text
Costruisci la matrice P del grafo orientato
Costruisci P' = gamma P + (1-gamma) 1 v^T
Inizializza una distribuzione pi^(0)

Per n = 0, 1, 2, ... finché non c'è convergenza:
    pi^(n+1) = pi^(n) P'

Restituisci il vettore limite pi
```

# 13. Schema del laboratorio

## 13.1 Laboratorio 1 -- Random walk su grafo non orientato

### Obiettivo

Studiare distribuzione stazionaria e tempi di ritorno su grafi semplici.

### Attività

1. costruire grafi elementari, per esempio:

   * linea finita;
   * ciclo;
   * stella;
   * grafo casuale piccolo;
2. simulare il random walk semplice;
3. stimare empiricamente la distribuzione stazionaria;
4. confrontarla con la previsione teorica proporzionale al grado.

### Domande guida

* I nodi ad alto grado vengono visitati più spesso?
* Quanto rapidamente il walk converge alla distribuzione stazionaria?
* I tempi medi di ritorno sono coerenti con $1/\pi_i$?

## 13.2 Laboratorio 2 -- Hitting e assorbimento

### Obiettivo

Studiare first-passage times e probabilità di assorbimento.

### Attività

1. scegliere un grafo con uno o più nodi bersaglio;
2. rendere alcuni nodi assorbenti;
3. simulare molte traiettorie da diversi nodi iniziali;
4. misurare:

   * probabilità di assorbimento in ciascun target;
   * tempo medio di assorbimento.

### Domande guida

* Alcuni nodi iniziali favoriscono sistematicamente un target rispetto a un altro?
* I tempi di assorbimento riflettono bene la struttura del grafo?
* La distanza topologica coincide con l'accessibilità dinamica?

## 13.3 Laboratorio 3 -- PageRank

### Obiettivo

Capire come il teleportation modifichi la centralità dei nodi in un grafo orientato.

### Attività

1. costruire o importare un piccolo grafo orientato;
2. calcolare il ranking dei nodi senza teleportation, se possibile;
3. introdurre il damping factor;
4. calcolare il PageRank per diversi valori di $\gamma$;
5. confrontare il ranking con misure topologiche semplici, come grado entrante o uscente.

### Domande guida

* Il ranking coincide con il semplice numero di link entranti?
* Quali nodi guadagnano importanza grazie alla struttura globale della rete?
* Quanto il risultato dipende dal valore di $\gamma$?

# 14. Estensioni possibili

Una volta implementato il modello base, si possono considerare diverse estensioni.

## 14.1 Random walk con bias

Il walker può preferire certi nodi o certe direzioni, introducendo una dinamica non uniforme.

## 14.2 Reti orientate e dangling nodes

Si può studiare in modo più dettagliato il problema dei nodi senza uscite e il modo in cui PageRank lo gestisce.

## 14.3 Comunità e colli di bottiglia

È interessante osservare come comunità fortemente connesse rallentino il mixing e influenzino hitting e distribuzione stazionaria.

## 14.4 Collegamenti con altri progetti del corso

Si possono costruire ponti diretti con:

* epidemie su reti;
* opinion dynamics su grafi;
* geografia ecologica e connettività;
* processi di assorbimento e first-passage in altri modelli spaziali.

# 15. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce in forma molto chiara il formalismo delle **catene di Markov finite**, che è una base concettuale importante per molti altri modelli.

Secondo, mostra come proprietà della rete e proprietà dinamiche del processo siano profondamente intrecciate.

Terzo, collega in modo naturale probabilità discreta, algebra lineare, simulazione Monte Carlo e algoritmi reali di ranking.

Quarto, crea ponti con una vasta parte del resto del corso:

* con **epidemie su reti**, perché anche lì la topologia controlla la diffusione;
* con **geografia ecologica**, perché hitting e connettività sono centrali;
* con **PageRank** come applicazione algoritmica moderna;
* con **processi markoviani** più generali, perché qui compaiono in una forma estremamente trasparente.

## Osservazione finale

Questo progetto è uno dei migliori punti di ingresso per far capire agli studenti che una rete non è solo una struttura statica di nodi e archi. È anche uno spazio dinamico su cui si definiscono processi di movimento, accesso, assorbimento e centralità. Proprio questa unione tra struttura e dinamica rende i random walk su grafi un caso di studio fondamentale.
