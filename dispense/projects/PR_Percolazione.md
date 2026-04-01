---
title: "Project: Percolazione su reticoli e reti"
subtitle: "connettività, cluster critici e robustezza di sistemi disordinati"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce la **percolazione** come caso di studio per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare la percolazione come modello di connettività casuale su reticoli e reti;

2. distinguere tra **site percolation** e **bond percolation**;

3. introdurre i concetti di cluster, giant component, spanning cluster e soglia critica;

4. mostrare come una geometria casuale possa produrre una transizione collettiva netta;

5. usare il modello per discutere frammentazione, robustezza e accessibilità in sistemi disordinati;

6. collegare la percolazione a problemi di epidemie, ecologia, materiali disordinati e reti infrastrutturali.

Dal punto di vista del corso, questo progetto è particolarmente importante perché introduce una delle soglie critiche più elementari e più profonde della teoria dei sistemi complessi. A differenza di molti altri modelli, qui non è necessario introdurre subito una dinamica temporale: basta una geometria casuale per far emergere una transizione macroscopica.

# 2. Motivazione generale

La domanda che dà origine al modello è semplicissima:

> se una struttura spaziale o reticolare è occupata solo parzialmente, esiste comunque un cammino connesso che attraversa il sistema?

Da questa domanda discendono problemi in molti ambiti diversi.

## 2.1 Materiali disordinati

In un materiale composito o poroso, alcune regioni conducono corrente o fluido, altre no. La percolazione descrive la soglia oltre la quale compare un cammino connesso macroscopico che rende possibile la conduzione o il passaggio del fluido.

## 2.2 Propagazione di incendi o epidemie

Un incendio può diffondersi solo attraverso siti combustibili adiacenti. Analogamente, una epidemia su un substrato spaziale discontinuo può propagarsi solo se esiste una connettività sufficiente tra regioni suscettibili.

## 2.3 Geografia ecologica e frammentazione dell'habitat

In un paesaggio frammentato, il problema fondamentale è capire se le regioni favorevoli formino ancora una struttura connessa abbastanza grande da permettere movimento, colonizzazione e persistenza.

## 2.4 Reti di comunicazione e infrastrutture

Se nodi o archi di una rete vengono rimossi casualmente, il sistema resta connesso? E se i guasti non sono casuali ma mirati ai nodi più importanti? La percolazione fornisce un linguaggio naturale per affrontare questi problemi.

## 2.5 Messaggio metodologico

Il grande pregio del modello è che mostra in modo molto chiaro una lezione generale: la struttura globale di un sistema può cambiare bruscamente quando un parametro locale di occupazione supera una soglia critica.

# 3. Definizione del modello

## 3.1 Site percolation

Nel caso di **site percolation**, ogni sito di un reticolo è occupato con probabilità $p$ e vuoto con probabilità $1-p$, indipendentemente dagli altri.

L'oggetto di interesse è il sottografo formato dai soli siti occupati e dai legami tra siti occupati vicini.

## 3.2 Bond percolation

Nel caso di **bond percolation**, tutti i siti sono presenti, ma ogni arco è mantenuto con probabilità $p$ e rimosso con probabilità $1-p$.

Qui il problema riguarda le componenti connesse del grafo risultante.

## 3.3 Reticoli e reti

Il modello può essere studiato su:

* reticoli regolari bidimensionali o tridimensionali;

* grafi casuali;

* reti reali;

* paesaggi rasterizzati;

* strutture orientate o non orientate.

Questa flessibilità è uno dei motivi del suo valore didattico.

# 4. Cluster e connettività

## 4.1 Cluster connessi

Un **cluster** è una componente connessa del sottografo occupato.

Nel caso di site percolation, un cluster è un insieme di siti occupati collegati da vicinanza. Nel caso di bond percolation, è un insieme di nodi collegati dagli archi sopravvissuti.

## 4.2 Cluster massimo e giant component

Per sistemi finiti si misura spesso la taglia del cluster massimo. Su grafi grandi o nel limite di sistemi grandi, si parla di **giant component** quando una componente contiene una frazione macroscopica dei nodi.

## 4.3 Spanning cluster

Su un dominio finito, per esempio un reticolo quadrato, si può anche chiedere se esista un cluster che connette due lati opposti del sistema. Questa è la nozione di **spanning cluster**.

# 5. La soglia critica

## 5.1 Idea generale

Per valori piccoli di $p$, i cluster restano piccoli e frammentati. Per valori grandi di $p$, compare con alta probabilità una struttura connessa macroscopica.

Tra questi due regimi esiste una soglia critica

$$
p_c,
$$

che separa qualitativamente:

* un regime subcritico, senza connettività globale;

* un regime supercritico, con giant component o spanning cluster.

## 5.2 Significato

La soglia $p_c$ è uno degli esempi più puliti di transizione collettiva. Non nasce da una dinamica di equilibrio, né da una energia, ma dalla geometria casuale del supporto.

## 5.3 Sistemi finiti

Su sistemi finiti, la transizione non è perfettamente netta, ma si manifesta come una regione di crossover sempre più brusca al crescere della dimensione del sistema.

# 6. Reticoli regolari e grafi casuali

## 6.1 Reticoli regolari

Su reticoli regolari la soglia critica riflette il coordinamento geometrico del sistema. In due dimensioni, per esempio, site e bond percolation hanno soglie diverse, ma entrambe descrivono la nascita di un cluster connesso macroscopico.

## 6.2 Grafi casuali

Su grafi casuali, la fenomenologia si traduce spesso nella comparsa di un giant component. Questo collega la percolazione al problema classico della connettività in Erdős--Rényi.

## 6.3 Differenze concettuali

Su reticoli regolari la geometria spaziale conta in modo diretto. Su reti casuali o complesse, invece, la distribuzione dei gradi e la presenza di hub diventano cruciali.

# 7. Collegamenti con altri modelli

La percolazione è collegata a molti altri modelli del corso.

## 7.1 Epidemie

Una epidemia può diffondersi solo se esiste una connettività sufficiente tra regioni o individui suscettibili. In molte approssimazioni, la struttura dei cluster suscettibili è direttamente legata a una condizione di percolazione.

## 7.2 Geografia ecologica

La percolazione fornisce un linguaggio naturale per discutere quando un paesaggio frammentato smette di essere attraversabile a scala macroscopica.

## 7.3 Affidabilità e robustezza di rete

La rimozione casuale di componenti e la perdita di connettività sono problemi classici di percolazione su grafo.

## 7.4 Contact process

Entrambi i modelli coinvolgono soglie di connettività o attività, ma la percolazione è un modello statico, mentre il contact process introduce una dinamica temporale.

# 8. Osservabili da misurare

Per trasformare il progetto in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 8.1 Taglia del cluster massimo

Se $C_{\max}$ è il cluster più grande, si può misurare:

$$
S_{\max} = \frac{|C_{\max}|}{N},
$$

cioè la frazione di nodi contenuta nella componente massima.

## 8.2 Probabilità di spanning

Su un reticolo finito si può definire la probabilità che esista un cluster che connette due lati opposti del sistema.

## 8.3 Distribuzione delle taglie dei cluster

Se $n_s$ è il numero di cluster di taglia $s$, si può studiare la distribuzione delle dimensioni dei cluster, particolarmente interessante vicino alla soglia critica.

## 8.4 Frazione nel giant component

Su reti grandi si può misurare la frazione dei nodi appartenenti alla componente gigante.

## 8.5 Stima empirica della soglia critica

Si può stimare $p_c$ osservando dove la probabilità di spanning o la crescita del cluster massimo cambiano più rapidamente.

# 9. Domande scientifiche che il progetto permette di studiare

1. Esiste una soglia netta di connettività?

2. Come cresce il cluster massimo vicino a $p_c$?

3. Qual è la differenza tra reticoli regolari e reti casuali?

4. In che senso la percolazione è collegata a epidemie e propagazione?

5. Come usare la percolazione per studiare frammentazione di habitat o robustezza di reti?

6. Come cambia il comportamento se la rimozione dei nodi è casuale oppure mirata?

7. Quanto la soglia dipende dalla geometria e quanto dalla distribuzione dei gradi?

# 10. Pseudocodice del modello

## 10.1 Input

* dimensione del reticolo oppure grafo di partenza

* probabilità di occupazione o di sopravvivenza $p$

* numero di realizzazioni indipendenti $R$

* eventuale intervallo di valori di $p$

* regola di connettività (vicinato di von Neumann, Moore, archi del grafo, ecc.)

## 10.2 Pseudocodice: site percolation su reticolo

```text
Per ogni realizzazione:
    genera un reticolo
    per ogni sito:
        occupa il sito con probabilità p
        lascia vuoto con probabilità 1-p

    identifica tutti i cluster connessi di siti occupati
    misura:
        - taglia del cluster massimo
        - eventuale spanning tra lati opposti
        - distribuzione delle taglie dei cluster
```

## 10.3 Pseudocodice: bond percolation su grafo

```text
Per ogni realizzazione:
    parti da un grafo dato
    per ogni arco:
        mantieni l'arco con probabilità p
        rimuovilo con probabilità 1-p

    calcola le componenti connesse del grafo risultante
    misura:
        - taglia della componente massima
        - frazione di nodi nel giant component
        - numero di componenti
```

## 10.4 Osservazione implementativa

Dal punto di vista computazionale, identificare i cluster richiede un algoritmo di visita del grafo, per esempio:

* depth-first search;

* breadth-first search;

* union-find.

Questa parte del progetto è utile anche per consolidare strumenti algoritmici fondamentali.

# 11. Schema del laboratorio

## 11.1 Laboratorio 1 -- Site percolation su reticolo quadrato

### Obiettivo

Visualizzare la transizione da cluster piccoli e frammentati a cluster macroscopici connessi.

### Attività

1. scegliere una griglia di valori di $p$;

2. generare molte realizzazioni su un reticolo quadrato;

3. identificare i cluster occupati;

4. misurare:

   * taglia del cluster massimo;

   * probabilità di spanning;

   * distribuzione delle taglie dei cluster.

### Domande guida

* A quale valore di $p$ compare una connettività macroscopica?

* La crescita del cluster massimo è graduale oppure brusca?

* Come cambia il comportamento al crescere della dimensione del sistema?

## 11.2 Laboratorio 2 -- Bond percolation su grafo casuale

### Obiettivo

Studiare la nascita di una componente gigante in una rete casuale.

### Attività

1. partire da un grafo casuale o da una rete data;

2. rimuovere archi con probabilità $1-p$;

3. calcolare le componenti connesse residue;

4. osservare come varia la frazione nel giant component.

### Domande guida

* Esiste una soglia ben visibile per la nascita della componente gigante?

* In che senso questo fenomeno somiglia alla percolazione su reticolo?

* Quanto la distribuzione dei gradi influenza la robustezza della rete?

## 11.3 Laboratorio 3 -- Robustezza: attacco casuale vs attacco mirato

### Obiettivo

Confrontare due modi diversi di degradare una rete.

### Attività

1. scegliere un grafo con eterogeneità di grado;

2. rimuovere nodi:

   * casualmente;

   * in ordine di grado decrescente;

3. misurare la dimensione della componente massima dopo ogni rimozione.

### Domande guida

* Una rete eterogenea è robusta ai guasti casuali?

* È fragile rispetto ad attacchi mirati ai nodi più connessi?

* Come si collega questo alla nozione di percolazione su rete?

# 12. Estensioni possibili

Una volta implementato il modello base, si possono considerare diverse estensioni.

## 12.1 Percolazione su reti reali

Si può applicare il modello a una rete geografica, di trasporto o di comunicazione reale.

## 12.2 Frammentazione ecologica

Un paesaggio raster può essere reinterpretato come problema di percolazione di habitat favorevole.

## 12.3 Collegamento con Erdős--Rényi

Si può mettere in relazione la percolazione con la comparsa del giant component nei grafi casuali classici.

## 12.4 Soglie direzionali e percolazione anisotropa

In sistemi orientati o con pesi diversi lungo direzioni diverse, la soglia di attraversamento può cambiare sensibilmente.

# 13. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce una soglia critica in una forma molto semplice e visivamente immediata.

Secondo, mostra che una grande parte della fenomenologia dei sistemi complessi nasce già dalla struttura geometrica e topologica, anche in assenza di una dinamica temporale sofisticata.

Terzo, consolida strumenti computazionali molto utili, come identificazione di componenti connesse, simulazione Monte Carlo e analisi statistica di transizioni su sistemi finiti.

Quarto, crea ponti naturali con molti altri progetti del corso:

* con **epidemie** e **contact process**, per il tema della soglia;

* con **geografia ecologica**, per il tema della connettività del paesaggio;

* con **affidabilità e reti**, per il tema della robustezza strutturale;

* con **Ising e cluster**, per il ruolo delle strutture connesse nello spazio.

## Osservazione finale

La percolazione è uno dei migliori modelli per mostrare che una soglia collettiva può emergere anche senza una dinamica temporale complessa. Basta una geometria casuale, un parametro di occupazione e una nozione di connettività. Proprio questa semplicità la rende un caso di studio straordinariamente potente.

