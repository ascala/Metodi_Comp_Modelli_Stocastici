---
title: "06a: Processi di salto e master equation"
author: "Antonio Scala"
date: ""
---

# Obiettivi della dispensa

In questa dispensa introduciamo il primo esempio sistematico di passaggio da una dinamica sulle traiettorie ad una dinamica sulla distribuzione di probabilità.

L'idea centrale è semplice ma fondamentale. Un sistema può evolvere in modo casuale passando da uno stato all'altro tramite transizioni discrete. Se osserviamo una singola realizzazione, vediamo una traiettoria irregolare fatta di salti. Se invece osserviamo un insieme di realizzazioni identiche, o immaginiamo di ripetere lo stesso esperimento molte volte, emerge una descrizione statistica più regolare: l'evoluzione della probabilità di trovare il sistema nei vari stati.

La domanda guida è quindi la seguente:

> come si passa da una legge microscopica sulle transizioni individuali ad una equazione chiusa per le probabilità di stato?

La risposta è la **master equation**, che vedremo nascere come semplice legge di bilancio tra flussi entranti e flussi uscenti.

Al termine della dispensa lo studente dovrebbe essere in grado di:

1. distinguere tra descrizione di una traiettoria e descrizione di una distribuzione di probabilità;
2. derivare la master equation a partire dai tassi di transizione;
3. interpretare la master equation come legge di conservazione della probabilità;
4. riscrivere la dinamica in forma matriciale;
5. comprendere il significato della soluzione formale come esponenziale di matrice;
6. discutere il rapporto tra evoluzione della pdf e simulazione di traiettorie;
7. collocare correttamente il metodo di Gillespie in questo quadro.

# 1. Traiettorie e probabilità di stato

Consideriamo un sistema il cui stato appartiene a un insieme discreto

$$
\mathcal{S} = \{1,2,3,\dots\}\;.
$$

Gli stati possono rappresentare configurazioni fisiche, numeri di individui in una popolazione, numeri di molecole in una reazione, classi epidemiologiche, occupazioni di nodi in una rete, oppure qualunque insieme discreto di configurazioni possibili.

Se osserviamo il sistema nel tempo, esso non si muove in modo continuo nello spazio degli stati, ma compie **salti** da uno stato ad un altro. Una singola realizzazione genera allora una traiettoria del tipo

$$
i_0 \to i_1 \to i_2 \to \cdots
$$

con tempi di salto casuali.

Questa è la descrizione più vicina al comportamento microscopico del sistema. Tuttavia, in moltissimi casi, ciò che interessa non è ricostruire una singola traiettoria, ma conoscere quantità statistiche come:

* la probabilità che il sistema si trovi nello stato $i$ al tempo $t$;
* la media di qualche osservabile;
* la probabilità di raggiungere certi stati;
* il rilassamento verso uno stato stazionario.

Per questo introduciamo la quantità

$$
p_i(t) = P(X_t = i),
$$

dove $X_t$ è la variabile aleatoria che descrive lo stato del sistema al tempo $t$.

Il vettore

$$
p(t) = \bigl(p_1(t), p_2(t), \dots\bigr)
$$

rappresenta la distribuzione di probabilità del sistema al tempo $t$.

Questa distribuzione soddisfa due proprietà immediate:

$$
p_i(t) \ge 0,
\qquad
\sum_i p_i(t) = 1.
$$

La seconda esprime la normalizzazione: il sistema deve trovarsi in qualche stato.

## 1.1 Due livelli di descrizione

È importante fermarsi un momento sulla differenza tra i due livelli di descrizione che d'ora in poi coesisteranno sempre.

### Livello 1: traiettorie

Una traiettoria è una successione casuale di stati visitati nel tempo. È l'oggetto naturale quando si simula il sistema evento per evento oppure quando si osserva una singola realizzazione sperimentale.

### Livello 2: distribuzione di probabilità

La distribuzione di probabilità assegna a ogni stato la probabilità di essere occupato al tempo $t$. È l'oggetto naturale quando si vogliono calcolare medie, probabilità, rilassamenti e distribuzioni stazionarie.

Questi due livelli non si contraddicono. Sono due modi diversi di descrivere la stessa dinamica.

> **Idea chiave**
> Una singola traiettoria mostra ciò che accade in una realizzazione. La pdf mostra ciò che accade statisticamente su un insieme di realizzazioni.

# 2. Transizioni elementari e tassi di salto

Per costruire l'equazione per le probabilità di stato dobbiamo specificare come avvengono le transizioni.

Supponiamo che, se il sistema si trova nello stato $i$, esso possa passare allo stato $j$ con un **tasso di transizione** (*transition rate*)

$$
w_{i \to j}.
$$

Il significato operativo di questa quantità è la seguente: in un intervallo di tempo molto piccolo $dt$, la probabilità che il sistema salti da $i$ a $j$ è, al primo ordine,

$$
P(\text{salto } i \to j \text{ in } [t,t+dt]) = w_{i \to j}\,dt + o(dt).
$$

Qui il simbolo $o(dt)$ indica termini di ordine superiore in $dt$, che trascureremo nel limite $dt \to 0$.

La struttura concettuale è dunque questa:

* gli stati sono discreti;
* il tempo è continuo;
* le transizioni avvengono in istanti casuali;
* i tassi controllano la frequenza media dei diversi salti.

## 2.1 Interpretazione dei tassi

Il tasso $w_{i \to j}$ non è una probabilità, ma una probabilità per unità di tempo. Per questo può essere maggiore di $1$, purché il prodotto $w_{i \to j}dt$ resti piccolo quando $dt$ è piccolo.

Dal punto di vista dimensionale $w_{i \to j}$ ha dimensione di un inverso di tempo.

Nei modelli applicativi i tassi possono dipendere:

* solo dagli stati coinvolti;
* da parametri esterni;
* dal numero di individui o particelle presenti;
* dalla configurazione globale del sistema.

In questa fase non ci serve specificare troppo. Ci basta sapere che i tassi esistono e definiscono la dinamica microscopica.

# 3. Derivazione della master equation

Vogliamo ora determinare come evolve nel tempo la probabilità $p_i(t)$ di essere nello stato $i$.

L'idea è semplicissima: in un piccolo intervallo $dt$, la probabilità di essere nello stato $i$ può cambiare per due ragioni opposte:

* il sistema può **entrare** in $i$ partendo da altri stati;
* il sistema può **uscire** da $i$ verso altri stati.

## 3.1 Termine di ingresso

Per arrivare in $i$ al tempo $t+dt$, il sistema può trovarsi al tempo $t$ in uno stato $j \neq i$ e compiere il salto $j \to i$ durante l'intervallo $dt$.

La probabilità di questo evento è, al primo ordine,

$$
p_j(t)\,w_{j \to i}\,dt\;.
$$

Sommando su tutti gli stati $j \neq i$, otteniamo il contributo totale di ingresso:

$$
\sum_{j \neq i} p_j(t) w_{j \to i} dt.
$$

## 3.2 Termine di uscita

Viceversa, se il sistema si trova in $i$ al tempo $t$, esso può lasciare questo stato saltando verso uno qualunque degli stati $j \neq i$.

La probabilità di un salto $i \to j$ in $dt$ è

$$
p_i(t) w_{i \to j} dt.
$$

Sommando su tutti i possibili stati di arrivo, il contributo totale di uscita è

$$
\sum_{j \neq i} p_i(t) w_{i \to j} dt.
$$

## 3.3 Bilancio completo

Mettiamo ora insieme i due contributi. La probabilità di essere in $i$ al tempo $t+dt$ è uguale alla probabilità di essere in $i$ al tempo $t$, più gli ingressi, meno le uscite:

$$
p_i(t+dt) = p_i(t) + \sum_{j \neq i} p_j(t) w_{j \to i} dt - \sum_{j \neq i} p_i(t) w_{i \to j} dt + o(dt).
$$

Sottraendo $p_i(t)$ da entrambi i membri, dividendo per $dt$ e passando al limite per $dt \to 0$, otteniamo:

$$
\frac{dp_i}{dt} = \sum_{j \neq i} \bigl[w_{j \to i} p_j - w_{i \to j} p_i\bigr].
$$

Questa è la **master equation**.

## 3.4 Significato della formula

Ogni termine della somma ha una lettura immediata:

* $w_{j \to i} p_j$ è il flusso di probabilità che entra in $i$ dallo stato $j$;
* $w_{i \to j} p_i$ è il flusso di probabilità che esce da $i$ verso lo stato $j$.

La master equation è dunque una legge di bilancio. Dice che la variazione temporale della probabilità in uno stato è data da

$$
\text{ingressi} - \text{uscite}.
$$

> **Idea chiave**
> La master equation non è un postulato misterioso: è semplicemente la forma differenziale di un bilancio probabilistico.

# 4. Un esempio elementare a due stati

Per fissare le idee, consideriamo il caso più semplice possibile: due stati, che chiameremo $1$ e $2$.

Supponiamo che i tassi di transizione siano:

$$
w_{1 \to 2} = \alpha,
\qquad
w_{2 \to 1} = \beta.
$$

Allora la master equation diventa

$$
\frac{dp_1}{dt} = \beta p_2 - \alpha p_1,
$$

$$
\frac{dp_2}{dt} = \alpha p_1 - \beta p_2.
$$

Poiché $p_1 + p_2 = 1$, basta in realtà una sola equazione. Sostituendo

$$
p_2 = 1 - p_1,
$$

si ottiene

$$
\frac{dp_1}{dt} = \beta(1-p_1) - \alpha p_1 = \beta - (\alpha+\beta)p_1.
$$

Questa è un'equazione lineare del primo ordine con soluzione

$$
p_1(t) = p_1^* + \bigl(p_1(0)-p_1^*\bigr)e^{-(\alpha+\beta)t},
$$

dove

$$
p_1^* = \frac{\beta}{\alpha+\beta}.
$$

Analogamente,

$$
p_2^* = \frac{\alpha}{\alpha+\beta}.
$$

Questa soluzione mostra già un punto importante: anche se le traiettorie individuali saltano in modo irregolare tra i due stati, la distribuzione di probabilità evolve in modo regolare e rilassa verso una distribuzione stazionaria.

# 5. Conservazione della probabilità

La master equation deve preservare la normalizzazione della distribuzione. Verifichiamolo esplicitamente.

Partiamo da

$$
\frac{dp_i}{dt} = \sum_{j \neq i} \bigl[w_{j \to i} p_j - w_{i \to j} p_i\bigr]
$$

e sommiamo su tutti gli stati $i$:

$$
\frac{d}{dt}\sum_i p_i = \sum_i \sum_{j \neq i} \bigl[w_{j \to i} p_j - w_{i \to j} p_i\bigr].
$$

Osserviamo ora che il doppio termine di somma contiene, per ogni coppia ordinata $(i,j)$ con $i \neq j$, un termine $+w_{j \to i} p_j$ e, nella riga $j$, un termine $-w_{j \to i} p_j$. Piu' precisamente, scambiando i nomi degli indici muti $i \leftrightarrow j$ nel termine di ingresso, si verifica che i due contributi si cancellano a coppie, e otteniamo

$$
\frac{d}{dt}\sum_i p_i(t) = 0.
$$

Dunque, se inizialmente

$$
\sum_i p_i(0)=1,
$$

allora per ogni tempo successivo vale ancora

$$
\sum_i p_i(t)=1.
$$

## 5.1 Lettura fisica

La probabilità totale si conserva perché la dinamica non crea né distrugge "massa probabilistica": la trasferisce da uno stato all'altro.

Questa idea è talmente importante che conviene formularla nel modo più chiaro possibile:

> **La master equation è una legge di continuità in uno spazio degli stati discreto.**

Nel caso continuo, che vedremo più avanti, la stessa idea riapparirà sotto forma di divergenza di una corrente. Qui, nel caso discreto, la corrente è sostituita da un bilancio tra stati distinti.

# 6. Forma matriciale e generatore

Per trattare la master equation in modo più compatto, introduciamo una notazione vettoriale.

Sia

$$
p(t) =
\begin{pmatrix}
p_1(t) \\
p_2(t) \\
\vdots \\
\end{pmatrix}
$$

o, a seconda delle convenzioni, un vettore riga. La scelta della convenzione non è fondamentale, purché venga mantenuta con coerenza.

Definiamo ora una matrice $L$, detta **generatore** della dinamica, i cui elementi fuori diagonale sono i tassi di transizione:

$$
L_{ij} = w_{j \to i}, \qquad i \neq j,
$$

mentre gli elementi diagonali sono scelti in modo da garantire la conservazione della probabilità:

$$
L_{ii} = -\sum_{j \neq i} w_{i \to j}.
$$

Con questa convenzione, la master equation si scrive come

$$
\dot p(t) = L p(t).
$$

## 6.1 Struttura della matrice generatrice

La matrice $L$ è detta *generatore* dell'evoluzione ed ha proprietà importanti:

1. gli elementi fuori diagonale sono non negativi;
2. gli elementi diagonali sono non positivi;
3. la somma degli elementi di ogni colonna è nulla (nella convenzione adottata in §6, in cui $p$ è un vettore colonna e la master equation è $\dot p = Lp$).

Quest'ultima proprietà è precisamente la traduzione matriciale della conservazione della probabilità.

## 6.2 Perché si parla di generatore

La parola “generatore” non è casuale. La matrice $L$ genera l'evoluzione temporale della distribuzione nello stesso senso in cui, per una ODE lineare, la matrice dinamica genera il flusso.

Conoscere $L$ significa conoscere completamente la dinamica della pdf.

# 7. Soluzione formale come esponenziale di matrice

Una volta scritta la master equation nella forma

$$
\dot p(t) = L p(t),
$$

la soluzione formale è

$$
p(t) = e^{tL} p(0),
$$

dove

$$
e^{tL} = \sum_{n=0}^{\infty} \frac{(tL)^n}{n!}
$$

è l'esponenziale di matrice. La matrice $e^{tL}$ è detta il *propagatore* della dinamica.

Dal punto di vista simbolico, la situazione sembra molto semplice: abbiamo una equazione lineare e una soluzione scritta in forma chiusa. Tuttavia qui conviene fare un'osservazione importante.

## 7.1 Soluzione formale non significa soluzione facile

Scrivere la soluzione come $p(t)=e^{tL}p(0)$ è estremamente utile dal punto di vista teorico, perché mostra che la dinamica è completamente determinata dal generatore. Ma sul piano computazionale non significa necessariamente che il problema sia facile.

Le difficoltà principali sono almeno tre.

### 1. Dimensione dello spazio degli stati

In molti problemi applicativi il numero degli stati è molto grande. Anche quando lo spazio degli stati è finito, la matrice $L$ può avere dimensioni enormi.

### 2. Struttura spettrale

Il comportamento temporale dipende dallo spettro di $L$. Modi associati ad autovalori vicini a zero decadono lentamente; modi associati ad autovalori molto negativi decadono rapidamente. Questa separazione di scale può rendere il problema rigido dal punto di vista numerico.

### 3. Calcolo numerico dell'esponenziale

Calcolare l'esponenziale di una matrice grande o mal condizionata non è banale. A seconda del problema si usano diagonalizzazione, decomposizioni, metodi di Krylov, integratori impliciti o approcci basati sulla simulazione di traiettorie.

Non serve entrare qui nei dettagli tecnici. Basta capire il messaggio generale:

> **La linearità della master equation aiuta l'analisi, ma non elimina automaticamente le difficoltà numeriche.**

# 8. Generatore, osservabili e medie

Una volta nota la distribuzione $p_i(t)$, si possono calcolare le medie di qualunque osservabile $A(i)$ definita sugli stati come

$$
\langle A \rangle_t = \sum_i A(i) p_i(t).
$$

Questa formula chiarisce bene il ruolo della master equation: essa non serve solo a seguire le probabilità di stato, ma permette di seguire nel tempo tutte le quantità statistiche costruite a partire da esse.

Nel caso a due stati, ad esempio, se assegniamo all'osservabile valori diversi nei due stati, la sua media temporale rilassa verso il valore determinato dalla distribuzione stazionaria.

Il quadro concettuale è dunque il seguente:

* il livello microscopico è definito dai tassi di salto;
* questi tassi definiscono il generatore $L$;
* il generatore determina l'evoluzione $e^{Lt}$ della pdf;
* la pdf determina le medie delle osservabili.

Questa catena logica è uno dei fili conduttori dell'intero corso.

# 9. Evolvere la pdf o simulare traiettorie?

A questo punto emerge naturalmente una domanda pratica e concettuale.

Se voglio studiare il processo, che cosa conviene fare?

* risolvere la master equation per la pdf;
* oppure simulare direttamente molte traiettorie individuali?

La risposta dipende dal problema, ma è importante capire che i due approcci non descrivono due dinamiche diverse. Sono due modi diversi di trattare la stessa dinamica.

## 9.1 Evoluzione della pdf

Risolvere la master equation significa seguire direttamente le probabilità di stato. Questo è naturale se:

* lo spazio degli stati non è troppo grande;
* interessano distribuzioni e medie globali;
* si vuole una descrizione completa della probabilità al tempo $t$.

## 9.2 Simulazione di traiettorie

Simulare traiettorie significa invece produrre realizzazioni individuali del processo. Questo è naturale se:

* lo spazio degli stati è molto grande;
* si vogliono stimare quantità statistiche via medie empiriche;
* interessa il comportamento di singole realizzazioni;
* si vuole evitare il costo di evolvere direttamente una pdf ad alta dimensione.

## 9.3 Le due descrizioni sono compatibili

Se si simulano molte traiettorie indipendenti e si costruisce, a un tempo fissato $t$, la frequenza empirica con cui ciascuno stato è occupato, questa frequenza converge alla distribuzione di probabilità $p_i(t)$.

In questo senso, la master equation descrive l'evoluzione statistica dell'insieme delle traiettorie, mentre la simulazione produce campioni di quelle traiettorie.

> **Idea chiave**
> Evoluzione della pdf e simulazione di traiettorie non sono approcci concorrenti, ma due rappresentazioni complementari dello stesso processo.

# 10. Dove si colloca il metodo di Gillespie

Il metodo di Gillespie è uno degli algoritmi fondamentali per simulare processi di salto in tempo continuo.

È importante però collocarlo con precisione nel quadro che abbiamo costruito.

## 10.1 Che cosa fa Gillespie

Dato uno stato corrente e dati i tassi delle possibili transizioni, l'algoritmo estrae:

1. il tempo di attesa fino al prossimo evento;
2. quale evento avviene tra quelli possibili.

Ripetendo questa procedura, esso genera una traiettoria completa del processo.

## 10.2 Che rapporto ha con la master equation

Il punto fondamentale è questo: Gillespie **non descrive una dinamica diversa** dalla master equation.

* la master equation evolve la pdf;
* Gillespie genera realizzazioni individuali del processo;
* le due descrizioni corrispondono allo stesso modello stocastico sottostante.

Se ripetiamo molte simulazioni di Gillespie e calcoliamo le frequenze empiriche degli stati, otteniamo una stima della stessa distribuzione governata dalla master equation.

## 10.3 Il ruolo del tempo

Qui emerge una distinzione concettuale molto importante. Nel contesto dei processi di salto in tempo continuo, il tempo generato da Gillespie ha **significato fisico**: rappresenta davvero l'istante in cui avvengono gli eventi nel modello.

Questo è diverso da molti algoritmi di campionamento basati su catene di Markov, dove la successione dei passi serve a costruire campioni da una distribuzione target e il “tempo” della catena non va interpretato, in generale, come tempo fisico del sistema.

Questa distinzione è essenziale per evitare confusioni:

* nei processi dinamici reali, il tempo fa parte del modello;
* nei metodi di campionamento artificiale, il tempo della catena è spesso solo un indice algoritmico.

> **Idea chiave**
> Gillespie è un simulatore esatto di traiettorie per un processo di salto in tempo continuo, non una teoria alternativa alla master equation.

# 11. Stato stazionario nel caso discreto

Anche se la discussione completa degli stati stazionari verrà ripresa più avanti in altri contesti, vale già la pena introdurre qui la nozione di base.

Una distribuzione $p^*$ si dice **stazionaria** se non cambia nel tempo. Dunque deve soddisfare

$$
\frac{dp_i^*}{dt} = 0
$$

per ogni stato $i$, cioè

$$
\sum_{j \neq i} \bigl[w_{j \to i} p_j^* - w_{i \to j} p_i^*\bigr] = 0.
$$

In forma matriciale,

$$
L p^* = 0.
$$

Ciò significa che una distribuzione stazionaria è un vettore nel *nucleo* del generatore (i.e. autovettore con autovalore nullo), compatibile con la normalizzazione.

## 11.1 Significato

Uno stato stazionario non implica che le traiettorie individuali si fermino. Le traiettorie possono continuare a saltare indefinitamente. Significa solo che, a livello statistico, la distribuzione delle probabilità non cambia più.

Questo punto è concettualmente molto importante e ricomparirà in modo ancora più ricco quando discuteremo la Fokker--Planck e le correnti di probabilità.

# 12. Lettura unificante

Siamo ora in grado di riassumere la struttura concettuale della dispensa in una forma molto compatta.

## Livello microscopico

Il sistema evolve tramite salti casuali tra stati discreti, governati dai tassi $w_{i \to j}$.

## Livello intermedio

I tassi definiscono un generatore lineare $L$.

## Livello statistico

Il generatore induce una equazione chiusa sulla pdf:

$$
\dot p = Lp.
$$

Questa è la master equation.

## Livello delle osservabili

Conoscendo $p(t)$ possiamo calcolare medie, probabilità e quantità aggregate.

Questa struttura a quattro livelli è il vero contenuto teorico della dispensa. Il caso discreto è il primo laboratorio concettuale in cui si vede chiaramente come una dinamica sulle traiettorie induca una dinamica sulla distribuzione.

# 13. Sintesi finale

Riassumiamo i punti principali.

1. Un processo di salto in tempo continuo è descritto microscopicamente da transizioni casuali tra stati discreti.
2. La quantità fondamentale a livello statistico è la probabilità di stato $p_i(t)$.
3. La sua evoluzione si ottiene con un bilancio tra flussi entranti e flussi uscenti.
4. Il risultato è la master equation:

$$
\frac{dp_i}{dt} = \sum_{j \neq i} \bigl[w_{j \to i} p_j - w_{i \to j} p_i\bigr].
$$

5. La master equation conserva la probabilità totale.
6. In forma compatta essa si scrive come

$$
\dot p = Lp,
$$

dove $L$ è il generatore.

7. La soluzione formale è data da un esponenziale di matrice,

$$
p(t)=e^{tL}p(0),
$$

ma questa forma non elimina le possibili difficoltà numeriche.
8. Simulare traiettorie ed evolvere la pdf sono due modi diversi di descrivere la stessa dinamica.
9. Il metodo di Gillespie genera traiettorie esatte del processo e va collocato precisamente a questo livello.

Se i tassi di transizione dipendono dal tempo, il generatore diventa $L(t)$ e la soluzione formale non si scrive piu' come semplice esponenziale. In quel caso serve il concetto di esponenziale cronologicamente ordinato, che trattiamo in appendice.

# 14. Ponte verso il caso continuo

Nella presente dispensa lo spazio degli stati è discreto e la probabilità viene redistribuita tra stati distinti tramite salti. Nella dispensa successiva considereremo invece sistemi in cui lo stato varia in uno spazio continuo.

Lì ritroveremo la stessa idea di fondo, ma in una forma diversa:

* per una ODE, la pdf viene trasportata dal flusso deterministico;
* per una SDE, oltre al trasporto compare anche la diffusione;
* l'equazione risultante sarà una equazione di continuità o, nel caso stocastico, una Fokker--Planck.

In altri termini:

$$
\text{stati discreti} \longrightarrow \text{master equation},
$$

$$
\text{stati continui} \longrightarrow \text{equazione di continuità / Fokker--Planck}.
$$

Questo passaggio mostrerà che master equation, equazione di continuità e Fokker--Planck non sono oggetti scollegati, ma tre versioni della stessa idea generale: una dinamica sulle traiettorie induce una dinamica lineare sulla distribuzione di probabilità.