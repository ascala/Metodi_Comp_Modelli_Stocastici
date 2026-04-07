---
title: "S06 Equazione di Fokker--Planck e master equation"
author: "Antonio Scala"
date: "apr 2026"
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

## Obiettivi della lezione

**Idea centrale:** passare dalla descrizione di **singole traiettorie stocastiche** alla descrizione dell’evoluzione della **densità di probabilità**.

**Obiettivi:**

- distinguere descrizione per traiettorie e descrizione per densità
- introdurre la master equation come bilancio probabilistico
- ricavare la forma generale della Fokker--Planck
- interpretare drift, diffusione e corrente di probabilità
- discutere stati stazionari ed equilibrio
- analizzare esempi espliciti
- collegare simulazione di traiettorie e densità empirica

---

## Dove siamo nel corso

:::: {.columns}
::: {.column width="50%"}

### Finora

- dinamiche deterministiche
- Monte Carlo
- catene di Markov
- processi a eventi discreti
- SDE e formula di Itô

:::
::: {.column width="50%"}

### Oggi

- dalla traiettoria alla legge del processo
- master equation
- limite continuo
- equazione di Fokker--Planck
- stati stazionari e correnti

:::
::::

**Messaggio:** la dinamica stocastica può essere descritta a due livelli complementari.

---

## Due punti di vista sullo stesso sistema

:::: {.columns}
::: {.column width="50%"}

### Livello microscopico

Una SDE descrive una traiettoria casuale:

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t
$$

- ogni realizzazione è diversa
- il rumore agisce sulla singola traiettoria

:::
::: {.column width="50%"}

### Livello statistico

La Fokker--Planck descrive la densità:

$$
p(x,t)
$$

- evolve in modo deterministico
- riassume l’insieme delle realizzazioni

:::
::::

---

## Perché serve una descrizione per densità?

Se ripetiamo molte volte la stessa dinamica con la stessa condizione iniziale:

- le traiettorie non coincidono
- a tempo fissato otteniamo una distribuzione di posizioni
- la domanda naturale è: **come evolve questa distribuzione?**

La risposta è l’equazione di **Fokker--Planck**.

---

## Densità di probabilità

Se $A$ è una regione dello spazio degli stati:

$$
\mathbb{P}(X_t \in A) = \int_A p(x,t)\,dx
$$

**Interpretazione:**

- un picco di $p(x,t)$ indica molte traiettorie in quella zona
- una densità larga indica forte dispersione
- una densità stretta indica incertezza ridotta

---

## Stesso fenomeno, due descrizioni

:::: {.columns}
::: {.column width="50%"}

### Traiettorie

- oggetto casuale
- osservabile in una singola simulazione
- utile per first passage, sample paths, eventi rari

:::
::: {.column width="50%"}

### Densità

- oggetto deterministico
- utile per momenti, equilibrio, flussi, distribuzioni stazionarie

:::
::::

**Idea chiave:** la casualità sta nelle traiettorie, non nell’evoluzione della densità.

---

## Prima tappa: spazio degli stati discreto

Prima del caso continuo, ricordiamo il caso discreto.

Se gli stati possibili sono $n=0,1,2,\dots$, la quantità fondamentale è

$$
P(n,t)
$$

che rappresenta la probabilità di essere nello stato $n$ al tempo $t$.

---

## Tassi di transizione

Indichiamo con

$$
W(n \mid n')
$$

il tasso di transizione dallo stato $n'$ allo stato $n$.

Allora la probabilità evolve secondo un bilancio di flussi tra stati.

---

## Forma generale della master equation

$$
\frac{d}{dt}P(n,t)
=
\sum_{n' \neq n}
\left[
W(n \mid n')P(n',t)
-
W(n' \mid n)P(n,t)
\right]
$$

Questa è la **master equation**.

---

## Interpretazione della master equation

:::: {.columns}
::: {.column width="50%"}

### Entrate

$$
\sum_{n'} W(n \mid n')P(n',t)
$$

flusso di probabilità che entra in $n$

:::
::: {.column width="50%"}

### Uscite

$$
\sum_{n'}W(n' \mid n)P(n,t)
$$

flusso di probabilità che esce da $n$

:::
::::

**Messaggio:** variazione della probabilità = entrate -- uscite.

---

## Legge di bilancio

La master equation è una legge di conservazione della probabilità nel caso discreto.

- probabilità guadagnata da uno stato
- probabilità persa verso altri stati
- struttura completamente analoga alle equazioni di continuità della fisica

---

## Collegamento con Gillespie

:::: {.columns}
::: {.column width="50%"}

### Gillespie

- genera traiettorie casuali
- un evento alla volta
- tempo continuo, stati discreti

:::
::: {.column width="50%"}

### Master equation

- non genera traiettorie
- descrive l’evoluzione di $P(n,t)$
- è la controparte deterministica del processo

:::
::::

---

## Esempio semplice: processo nascita--morte

Per esempio, se da $n$ posso passare a:

- $n+1$ con tasso $\lambda_n$
- $n-1$ con tasso $\mu_n$

allora

$$
\frac{d}{dt}P(n,t)
=
\lambda_{n-1}P(n-1,t)
+
\mu_{n+1}P(n+1,t)
-
(\lambda_n+\mu_n)P(n,t)
$$

---

## Cosa ci interessa oggi del caso discreto

Non tanto risolvere la master equation in generale, ma capire il suo ruolo concettuale:

- è l’analogo discreto della Fokker--Planck
- mostra il carattere di bilancio probabilistico
- suggerisce il passaggio dal discreto al continuo

---

## Dal discreto al continuo

Se:

- gli stati sono molto numerosi
- i salti elementari sono piccoli
- la variabile di stato può essere trattata come continua

allora la master equation può essere sviluppata in serie.

---

## Kramers--Moyal: idea generale

Dal bilancio discreto si passa formalmente a una espansione in potenze del salto.

Il risultato generale è la **serie di Kramers--Moyal**.

Troncando ai primi due ordini si ottiene una PDE con:

- termine di drift
- termine di diffusione

cioè la Fokker--Planck.

---

## Quadro concettuale complessivo

$$
\text{processo di salto}
\;\to\;
\text{master equation}
\;\to\;
\text{limite continuo}
\;\to\;
\text{Fokker--Planck}
$$

**Messaggio:** la Fokker--Planck non è un oggetto isolato, ma la controparte continua della dinamica markoviana.

---

## Torniamo alle SDE

Consideriamo la SDE scalare di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t
$$

Vogliamo descrivere l’evoluzione della densità associata al processo.

---

## Forma generale della Fokker--Planck

La densità $p(x,t)$ soddisfa formalmente

$$
\partial_t p(x,t) = -\partial_x\bigl(\,a(x,t)p(x,t)\,\bigr)
+ \frac{1}{2}\partial_x^2\bigl(\,b(x,t)^2 p(x,t)\,\bigr)
$$

Questa è l’equazione di **Fokker--Planck** in una dimensione.

---

## Struttura della formula

:::: {.columns}
::: {.column width="50%"}

### Trasporto

$$
-\partial_x(ap)
$$

- dovuto al drift
- sposta la massa di probabilità

:::
::: {.column width="50%"}

### Diffusione

$$
\frac{1}{2}\partial_x^2(b^2p)
$$

- dovuta al rumore
- tende ad allargare la distribuzione

:::
::::

---

## Il coefficiente di diffusione

Spesso si introduce

$$
D(x,t)=\frac{1}{2}b(x,t)^2
$$

e allora la Fokker--Planck diventa

$$
\partial_t p = -\partial_x(ap) + \partial_x^2(Dp)
$$

Questa forma rende evidente la parentela con l’equazione della diffusione classica.

---

## Da dove viene il fattore $1/2$?

Il fattore $1/2$ è legato al calcolo di Itô.

Ricordiamo infatti che formalmente

$$
(dW_t)^2 = dt
$$

e questo produce il termine diffusivo nella derivazione.

---

## Prima lettura fisica

Se $a(x,t)$ domina:

- la densità si sposta

Se $b(x,t)$ domina:

- la densità si allarga

Se entrambi sono presenti:

- la distribuzione viene trasportata e diffusa simultaneamente

---

## Fokker--Planck come equazione di continuità

La PDE può essere riscritta come

$$
\partial_t p(x,t) + \partial_x J(x,t)=0
$$

dove $J(x,t)$ è la **corrente di probabilità**.

---

## Corrente di probabilità

Nel caso unidimensionale

$$
J(x,t)
=
a(x,t)p(x,t)
-
\frac{1}{2}\partial_x\!\bigl(b(x,t)^2 p(x,t)\bigr)
$$

Questa grandezza misura il flusso locale di probabilità nello spazio degli stati.

---

## Significato della corrente

- se $J>0$, la probabilità fluisce verso destra
- se $J<0$, la probabilità fluisce verso sinistra
- se $\partial_x J > 0$, la densità locale diminuisce
- se $\partial_x J < 0$, la densità locale aumenta

---

## Conservazione della probabilità

Integrando su tutto lo spazio:

$$
\frac{d}{dt}\int p(x,t)\,dx = 0
$$

purché le condizioni al bordo siano appropriate.

**Messaggio:** la Fokker--Planck conserva la massa totale di probabilità.

---

## Ruolo delle condizioni al bordo

La PDE non è completa senza specificare cosa succede ai bordi del dominio.

Possibili casi:

- dominio infinito con decrescenza sufficiente
- bordi riflettenti
- bordi assorbenti
- dominio periodico

---

## Bordi riflettenti

Se non può uscire probabilità dal dominio, si impone

$$
J(0,t)=0,
\qquad
J(L,t)=0
$$

Interpretazione:

- le traiettorie restano confinate
- la probabilità totale nel dominio si conserva

---

## Bordi assorbenti

Se il sistema viene rimosso quando raggiunge il bordo, si impone tipicamente

$$
p(0,t)=0,
\qquad
p(L,t)=0
$$

oppure una formulazione equivalente in termini di flusso uscente.

**Interpretazione:** la massa di probabilità nel dominio decresce nel tempo.

---

## Stati stazionari

Uno stato stazionario è una densità $p_{\mathrm{st}}(x)$ tale che

$$
\partial_t p_{\mathrm{st}}(x)=0
$$

Allora

$$
\partial_x J_{\mathrm{st}}(x)=0
$$

quindi la corrente stazionaria è costante nello spazio.

---

## Equilibrio senza corrente

In molti problemi si cerca uno stato stazionario con

$$
J_{\mathrm{st}}(x)=0
$$

Allora la densità stazionaria soddisfa

$$
a(x)p_{\mathrm{st}}(x)
-
\frac{1}{2}\partial_x\!\bigl(b(x)^2p_{\mathrm{st}}(x)\bigr)=0
$$

---

## Caso di drift di gradiente

Se

$$
dX_t = -V'(X_t)\,dt + \sigma\,dW_t
$$

allora la Fokker--Planck è

$$
\partial_t p
=
\partial_x\!\bigl(V'(x)p\bigr)
+
\frac{\sigma^2}{2}\partial_x^2 p
$$

---

## Distribuzione stazionaria nel caso di gradiente

Imponendo corrente stazionaria nulla si ottiene formalmente

$$
p_{\mathrm{st}}(x)
\propto
\exp\!\left(
-\frac{2V(x)}{\sigma^2}
\right)
$$

---

## Lettura qualitativa della formula

- i minimi di $V(x)$ corrispondono a regioni più probabili
- i massimi di $V(x)$ corrispondono a barriere
- se $\sigma$ aumenta, la distribuzione si appiattisce
- se $\sigma$ diminuisce, la distribuzione si concentra vicino ai minimi

---

## Esempio 1: drift costante e diffusione costante

Consideriamo

$$
dX_t = \mu\,dt + \sigma\,dW_t
$$

La Fokker--Planck associata è

$$
\partial_t p
=
-\mu\,\partial_x p
+
\frac{\sigma^2}{2}\partial_x^2 p
$$

---

## Interpretazione dell’esempio 1

:::: {.columns}
::: {.column width="50%"}

### Drift costante

- sposta il centro della distribuzione
- velocità media pari a $\mu$

:::
::: {.column width="50%"}

### Rumore costante

- allarga la distribuzione
- varianza crescente nel tempo

:::
::::

---

## Soluzione fondamentale

Se

$$
p(x,0)=\delta(x-x_0)
$$

allora

$$
p(x,t)=
\frac{1}{\sqrt{2\pi\sigma^2 t}}
\exp\!\left[
-\frac{(x-x_0-\mu t)^2}{2\sigma^2 t}
\right]
$$

---

## Cosa ci insegna questo esempio

- la media si muove come $x_0+\mu t$
- la varianza cresce come $\sigma^2 t$
- drift e diffusione sono separati in modo molto trasparente

È il primo esempio ideale per confrontare teoria e simulazione.

---

## Esempio 2: Ornstein--Uhlenbeck

Consideriamo

$$
dX_t = -\lambda X_t\,dt + \sigma\,dW_t,
\qquad \lambda>0
$$

La Fokker--Planck associata è

$$
\partial_t p
=
\partial_x\!\bigl(\lambda x\,p\bigr)
+
\frac{\sigma^2}{2}\partial_x^2 p
$$

---

## Interpretazione dell’Ornstein--Uhlenbeck

- se $x>0$, il drift punta verso sinistra
- se $x<0$, il drift punta verso destra
- il rumore tende comunque a disperdere la probabilità

**Messaggio:** competizione tra confinamento e diffusione.

---

## Stato stazionario dell’OU

Imponendo corrente nulla:

$$
\lambda x\,p_{\mathrm{st}}(x)
+
\frac{\sigma^2}{2}\partial_x p_{\mathrm{st}}(x)=0
$$

si ottiene

$$
p_{\mathrm{st}}(x)
=
\sqrt{\frac{\lambda}{\pi\sigma^2}}
\exp\!\left(
-\frac{\lambda x^2}{\sigma^2}
\right)
$$

---

## Significato dello stato stazionario OU

- il drift lineare confina
- il rumore diffonde
- la gaussiana stazionaria è il compromesso tra i due effetti

Questo è uno dei modelli più importanti dell’intero corso.

---

## Esempio 3: doppio pozzo

Consideriamo

$$
dX_t = -U'(X_t)\,dt + \sigma\,dW_t
$$

con

$$
U(x)=\frac{x^4}{4}-\frac{x^2}{2}
$$

Allora

$$
p_{\mathrm{st}}(x)\propto \exp\!\left(-\frac{2U(x)}{\sigma^2}\right)
$$

---

## Cosa mostra il doppio pozzo

- due regioni favorite della densità
- una barriera tra i due minimi
- transizioni rare tra i pozzi
- fenomeni di metastabilità per rumore debole

---

## Lettura dinamica del doppio pozzo

Su tempi intermedi:

- la densità può restare concentrata quasi in un solo pozzo

Su tempi più lunghi:

- il rumore induce attraversamenti della barriera
- il sistema esplora entrambi i pozzi

---

## Collegamento con le simulazioni

La Fokker--Planck non sostituisce le simulazioni di traiettorie.

Piuttosto, le completa.

Strategia tipica:

1. simulare molte traiettorie con Euler--Maruyama
2. raccogliere i valori $X_t$ a tempo fissato
3. costruire un istogramma normalizzato
4. confrontarlo con la densità teorica

---

## Esperimento numerico concettuale

:::: {.columns}
::: {.column width="50%"}

### Microlivello

- molte traiettorie diverse
- forte variabilità individuale

:::
::: {.column width="50%"}

### Macrolivello

- istogramma regolare
- convergenza verso la densità prevista

:::
::::

**Messaggio:** il livello statistico emerge dalla media su molte realizzazioni.

---

## Accuratezza debole: perché c’entra qui?

Nel contesto delle SDE:

- l’accuratezza forte riguarda la singola traiettoria
- l’accuratezza debole riguarda osservabili e distribuzioni

La Fokker--Planck è il linguaggio naturale dell’accuratezza debole.

---

## Una derivazione formale: idea

Partiamo dalla SDE

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t
$$

Applichiamo la formula di Itô a una funzione test $f(X_t,t)$.

---

## Formula di Itô per la funzione test

$$
df(X_t,t)
=
\left(
\partial_t f
+
a\,\partial_x f
+
\frac{1}{2}b^2\partial_x^2 f
\right)dt
+
b\,\partial_x f\,dW_t
$$

Facendo il valore atteso, il termine con $dW_t$ scompare.

---

## Operatore generatore

Si introduce l’operatore

$$
Lf
=
a(x,t)\partial_x f
+
\frac{1}{2}b(x,t)^2 \partial_x^2 f
$$

così che formalmente

$$
\frac{d}{dt}\mathbb{E}[f(X_t,t)]
=
\mathbb{E}[Lf + \partial_t f]
$$

---

## Dal generatore alla PDE

Scrivendo il valore atteso in termini della densità,

$$
\mathbb{E}[f(X_t,t)] = \int f(x,t)p(x,t)\,dx
$$

e integrando per parti formalmente, si trasferiscono le derivate da $f$ a $p$.

Il risultato è

$$
\partial_t p = -\partial_x(ap)+\frac{1}{2}\partial_x^2(b^2p)
$$

---

## Morale della derivazione

- la struttura della PDE riflette la formula di Itô
- il drift produce una derivata prima
- il rumore produce una derivata seconda
- la Fokker--Planck è l’equazione aggiunta del generatore della dinamica

---

## Master equation e Fokker--Planck a confronto

:::: {.columns}
::: {.column width="50%"}

### Master equation

- spazio degli stati discreto
- somme sui possibili salti
- bilancio probabilistico su stati discreti

:::
::: {.column width="50%"}

### Fokker--Planck

- spazio degli stati continuo
- derivate spaziali
- bilancio probabilistico per densità

:::
::::

---

## Confronto tra i tre livelli del corso

| Livello | Oggetto | Evoluzione |
|---|---|---|
| Eventi discreti | traiettoria di salti | Gillespie |
| SDE | traiettoria continua casuale | Langevin / Itô |
| Densità | distribuzione di probabilità | Fokker--Planck |

---

## Esempio trasversale: cosa cambia davvero?

:::: {.columns}
::: {.column width="33%"}

### Gillespie

stato discreto  
tempo casuale tra eventi

:::
::: {.column width="33%"}

### SDE

stato continuo  
incrementi gaussiani piccoli

:::
::: {.column width="33%"}

### Fokker--Planck

nessuna traiettoria  
solo evoluzione della legge

:::
::::

---

## Quando conviene usare la Fokker--Planck?

- per studiare stati stazionari
- per analizzare correnti e bilanci
- per descrivere distribuzioni e momenti
- per capire il comportamento collettivo
- per collegare SDE e PDE

---

## Quando conviene pensare in termini di traiettorie?

- first passage
- crossing di soglie
- eventi rari
- simulazione numerica
- osservazione di singole realizzazioni

---

## Sintesi concettuale

La stessa dinamica stocastica può essere vista come:

- traiettorie casuali individuali
- legge deterministica della popolazione di traiettorie

Questa doppia lettura è uno dei punti centrali del corso.

---

## Take-home message

- la master equation è la forma naturale del bilancio probabilistico nel caso discreto
- la Fokker--Planck è la controparte continua della stessa idea
- drift e rumore della SDE diventano trasporto e diffusione nella PDE
- la corrente di probabilità è lo strumento giusto per leggere conservazione ed equilibrio
- gli stati stazionari collegano dinamica stocastica e paesaggi di potenziale
- simulare molte traiettorie permette di ricostruire empiricamente la densità

---

## Sviluppi possibili

- Fokker--Planck in più dimensioni
- equazione di Kramers
- tempi di primo passaggio
- metastabilità e transizioni rare
- metodi numerici per PDE stocastiche

---

## Backup -- Forma multidimensionale

Per

$$
d\mathbf{X}_t = \mathbf{a}(\mathbf{x},t)\,dt + B(\mathbf{x},t)\,d\mathbf{W}_t
$$

la Fokker--Planck diventa

$$
\partial_t p
=
-\sum_i \partial_{x_i}(a_i p)
+
\frac{1}{2}\sum_{i,j}\partial_{x_i}\partial_{x_j}\!\bigl((BB^{\top})_{ij}p\bigr)
$$

---

## Backup -- Diffusione pura

Se

$$
dX_t = \sigma\,dW_t
$$

allora

$$
\partial_t p = \frac{\sigma^2}{2}\partial_x^2 p
$$

che è la normale equazione del calore.

---

## Backup -- Drift deterministico puro

Se

$$
dX_t = a(X_t,t)\,dt
$$

senza rumore, allora formalmente

$$
\partial_t p = -\partial_x(ap)
$$

cioè una pura equazione di trasporto.

---

## Backup -- Domanda concettuale per gli studenti

Se una singola traiettoria resta casuale, perché la densità evolve in modo deterministico?

**Risposta attesa:** perché la densità descrive la legge del processo, non una realizzazione particolare.

---

## Backup -- Domanda computazionale

Per verificare numericamente una Fokker--Planck nota, cosa conviene fare?

- simulare molte traiettorie
- fissare un tempo $t$
- costruire un istogramma normalizzato
- confrontarlo con la soluzione teorica