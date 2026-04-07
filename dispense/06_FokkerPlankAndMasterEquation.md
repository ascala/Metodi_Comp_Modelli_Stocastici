---
title: "06: Equazione di Fokker--Planck"
author: "Antonio Scala"
date: ""
---

L’equazione di Fokker--Planck fornisce la descrizione deterministica dell’evoluzione della distribuzione di probabilità associata a una dinamica stocastica continua.
Se una SDE descrive il comportamento di una singola traiettoria casuale, la Fokker--Planck descrive invece come evolve nel tempo la densità di probabilità di un intero insieme di realizzazioni.

In questo senso, essa costituisce il naturale complemento delle equazioni differenziali stocastiche introdotte nella lezione precedente: non sostituisce la dinamica stocastica, ma la riformula a livello statistico.

Dal punto di vista concettuale, questa lezione chiude un percorso iniziato con le dinamiche deterministiche, proseguito con Monte Carlo, catene di Markov, processi a salti e SDE: dalla dinamica di singole traiettorie si passa ora all’evoluzione della legge del processo.

## Obiettivi della lezione

Al termine della lezione lo studente dovrebbe essere in grado di:

1. spiegare la differenza tra descrizione per traiettorie e descrizione per densità;

2. scrivere l’equazione di Fokker--Planck associata a una SDE scalare di Itô;

3. interpretare i termini di drift e diffusione nella PDE;

4. riscrivere la Fokker--Planck come equazione di continuità con corrente di probabilità;

5. discutere il significato di stato stazionario e corrente stazionaria;

6. analizzare almeno un esempio esplicito;

7. collegare simulazione di traiettorie e stima empirica della densità;

8. riconoscere il ruolo della master equation come ponte tra processi di salto e limite diffusivo.

## Struttura

1. Dalle traiettorie casuali alle distribuzioni

2. Processi di salto e master equation

3. Forma generale dell’equazione di Fokker--Planck

4. Interpretazione dei termini: drift, diffusione e corrente

5. Stati stazionari ed equilibrio

6. Esempio 1: drift costante e diffusione costante

7. Esempio 2: processo di Ornstein--Uhlenbeck

8. Esempi opzionali: doppio pozzo, condizioni al bordo

9. Collegamento con la simulazione

10. Una possibile derivazione formale

11. Sintesi finale

# 1. Dalle traiettorie casuali alle distribuzioni

Nella lezione precedente abbiamo introdotto una SDE nella forma di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t\;.
$$

Questa equazione descrive una singola traiettoria casuale $X_t$.
A parità di condizione iniziale, realizzazioni diverse del moto browniano producono traiettorie diverse.

Nasce allora una domanda naturale:

> se non guardo una singola traiettoria, ma un intero insieme di realizzazioni, come evolve nel tempo la distribuzione di probabilità della variabile $X_t$?

La risposta è l’equazione di Fokker--Planck.

## 1.1 Idea di base

Supponiamo di ripetere molte volte la stessa dinamica stocastica a partire da condizioni iniziali identiche.
A ogni tempo $t$, le diverse realizzazioni non si troveranno nello stesso punto, ma formeranno una distribuzione nello spazio degli stati.

Indichiamo con

$$p(x,t)$$

la densità di probabilità di trovare il sistema vicino a $x$ al tempo $t$.

La Fokker--Planck descrive l’evoluzione deterministica di questa densità.

## 1.2 Messaggio concettuale

Una SDE e la corrispondente equazione di Fokker--Planck descrivono lo stesso fenomeno a due livelli diversi:

* la SDE descrive le traiettorie individuali;

* la Fokker--Planck descrive l’evoluzione della legge del processo.

La casualità resta nelle traiettorie; la legge evolve invece in modo deterministico.

## 1.3 Densità e probabilità locale

Se $A$ è un intervallo dello spazio degli stati, la probabilità di trovare il sistema in $A$ al tempo $t$ è

$$
\mathbb{P}(X_t \in A) = \int_A p(x,t),dx\,.
$$

La densità $p(x,t)$ non va quindi interpretata come una traiettoria media, ma come una descrizione statistica dell’insieme delle realizzazioni.

In particolare:

* un picco di $p(x,t)$ indica che molte traiettorie si trovano in quella regione;

* una densità larga indica una forte dispersione delle realizzazioni;

* una densità concentrata indica invece che l’incertezza è piccola.

# 2. Processi di salto e master equation

Prima di introdurre la Fokker--Planck è utile esplicitare il ponte con i processi markoviani a tempo continuo già incontrati nella parte del corso dedicata a Gillespie e ai processi a eventi discreti.

Se lo spazio degli stati è discreto, la quantità fondamentale non è una traiettoria continua, ma la probabilità

$$P(n,t)$$

di trovare il sistema nello stato $n$ al tempo $t$.

## 2.1 Forma generale della master equation

Indichiamo con

$$
W(n \mid n')
$$

il tasso di transizione dallo stato $n'$ allo stato $n$.
La probabilità $P(n,t)$ evolve allora secondo

$$
\frac{d}{dt} P(n,t) =
\sum_{n' \neq n} \left[ W(n \mid n') P(n',t) - W(n' \mid n) P(n,t) \right]\,.
$$

Questa è la **master equation**.

## 2.2 Interpretazione come bilancio probabilistico

La struttura della formula è molto trasparente:

* il termine\
  $$ W(n \mid n') P(n',t) $$
  rappresenta il flusso di probabilità che entra nello stato $n$ partendo da $n'$;

* il termine
  $$ W(n' \mid n) P(n,t)$$
  rappresenta invece il flusso che esce dallo stato $n$ verso $n'$.

La master equation è quindi una legge di bilancio: variazione della probabilità in uno stato = entrate meno uscite.

## 2.3 Collegamento con Gillespie

Il metodo di Gillespie genera traiettorie individuali di un processo di salto continuo nel tempo.
La master equation descrive invece l’evoluzione deterministica della distribuzione di probabilità dello stesso processo.

Questa relazione è del tutto analoga a quella che, nel caso diffusivo, lega una SDE alla corrispondente equazione di Fokker--Planck:

* Gillespie / processo di salto = traiettorie casuali;

* master equation = evoluzione deterministica delle probabilità sugli stati discreti.

## 2.4 Dal discreto al continuo

Se gli stati diventano molto numerosi, la variabile di stato può essere trattata come quasi continua, e i salti come piccoli incrementi.
In questo regime la master equation può essere sviluppata in serie nei piccoli salti.

Formalmente, da questa espansione si ottiene la **serie di Kramers--Moyal**.
Troncando ai primi due ordini si arriva precisamente all’equazione di Fokker--Planck.

Il quadro concettuale è dunque il seguente:

$$
\text{processo di salto} \to \text{master equation} \to
\text{limite continuo} \to
\text{Fokker--Planck}\;.
$$

## 2.5 Perché questo passaggio è importante

La Fokker--Planck non va quindi vista come un oggetto separato dalla teoria dei processi markoviani, ma come la sua controparte continua nel regime in cui:

* la variabile di stato è trattata come continua;

* i salti elementari sono piccoli;

* gli effetti principali sono descritti da drift e diffusione.

# 3. Forma generale dell’equazione di Fokker--Planck

Consideriamo la SDE scalare di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t\;.
$$

La densità $p(x,t)$ associata al processo soddisfa formalmente l’equazione

$$
\partial_t p(x,t) =
- \partial_x\bigl(a(x,t)\,p(x,t)\bigr)
+ \frac{1}{2},\partial_x^2\bigl(b(x,t)^2\,p(x,t)\bigr).\
$$

Questa è l’equazione di Fokker--Planck nel caso unidimensionale.

## 3.1 Struttura della formula

L’equazione contiene due contributi:

1. un termine di trasporto
   $$ -\partial_x(ap), $$
   dovuto al drift;

2. un termine di diffusione
   $$
   \frac{1}{2}\partial_x^2(b^2 p)\;,
   $$
   dovuto alle fluttuazioni casuali.

La struttura riflette esattamente quella della SDE:

* il drift sposta la massa di probabilità;

* il rumore tende ad allargarla.

## 3.2 Commento sul fattore $1/2$

Il fattore $1/2$ davanti al termine diffusivo è caratteristico del formalismo di Itô e deriva dal fatto che

$$
(dW_t)^2 = dt
$$

nel calcolo stocastico.

## 3.3 Notazione alternativa

Spesso si introduce il coefficiente di diffusione

$$
D(x,t) = \frac{1}{2} b(x,t)^2.
$$

In questa notazione la Fokker--Planck si scrive

$$
\partial_t p = -\partial_x(ap) + \partial_x^2(Dp).
$$

Questa forma mette in evidenza la parentela con l’equazione della diffusione classica.

# 4. Interpretazione: drift, diffusione e corrente di probabilità

L’equazione di Fokker--Planck può essere riscritta come una legge di continuità:

$$
\partial_t p(x,t) + \partial_x J(x,t) = 0,
$$

dove

$$
J(x,t) = a(x,t)\,p(x,t) - \frac{1}{2}\partial_x \bigl(\,b(x,t)^2 p(x,t)\,\bigr)
$$

è la **corrente di probabilità**.

## 4.1 Significato fisico

Questa forma è molto istruttiva.

* Se $J>0$, la probabilità fluisce localmente verso destra.

* Se $J<0$, la probabilità fluisce localmente verso sinistra.

* Se $\partial_x J$ è positivo, in quel punto la densità diminuisce nel tempo.

* Se $\partial_x J$ è negativo, la densità aumenta.

La Fokker--Planck è quindi una vera equazione di conservazione della probabilità totale.

## 4.2 Normalizzazione

Integrando su tutto lo spazio e assumendo condizioni al bordo appropriate, si ottiene

$$
\frac{d}{dt}\int p(x,t)\,dx = 0.
$$

La probabilità totale resta dunque uguale a 1.

## 4.3 Drift contro diffusione

Dal punto di vista intuitivo, i due termini della corrente giocano ruoli diversi.

Il contributo

$$
a(x,t)\,p(x,t)
$$

trasporta la probabilità seguendo la tendenza media della dinamica.

Il contributo

$$
-\frac{1}{2}\partial_x\bigl(\,b(x,t)^2 p(x,t)\,\bigr)
$$

tende invece a redistribuire la massa di probabilità in modo diffusivo.
Quando $b$ è costante, questo termine si riduce a un normale flusso diffusivo proporzionale al gradiente di densità.

# 5. Stati stazionari ed equilibrio

Uno stato stazionario è una densità $p_{\mathrm{st}}(x)$ tale che

$$
\partial_t\,p_{\mathrm{st}}(x) = 0.
$$

In questo caso la Fokker--Planck diventa

$$
\partial_x\,J_{\mathrm{st}}(x) = 0,
$$

cioè la corrente stazionaria è costante nello spazio.

## 5.1 Caso di equilibrio senza corrente

In molti problemi su dominio illimitato o con condizioni riflettenti si impone

$$
J_{\mathrm{st}}(x)=0.
$$

Allora la stazionarietà si ottiene risolvendo

$$
a(x)\,p_{\mathrm{st}}(x) -
\frac{1}{2}\partial_x \bigl(\, b(x)^2 p_{\mathrm{st}}(x)\,\bigr) = 0\;.
$$

Questo è spesso il modo più semplice per trovare la distribuzione stazionaria.

## 5.2 Caso di drift di gradiente e rumore costante

Se

$$
dX_t = -V'(X_t)\,dt + \sigma\,dW_t\;,
$$

allora la Fokker--Planck è

$$
\partial_t p = \partial_x\bigl(\,V'(x)\,p\,\bigr)
+ \frac{\,\sigma^2}{\!2}\partial_x^2 p\;.
$$

Imponendo corrente stazionaria nulla si trova formalmente

$$
p_{\mathrm{st}}(x) \propto \exp\!\left(-\frac{2V(x)}{\sigma^2}\right)\;. 
$$

Questa formula è molto importante, perché collega:

* paesaggio di potenziale;

* rumore;

* distribuzione di equilibrio.

## 5.3 Lettura qualitativa della formula stazionaria

La distribuzione stazionaria è maggiore dove il potenziale è più basso e minore dove il potenziale è più alto.
In altre parole:

* i minimi di $V(x)$ corrispondono a regioni di alta probabilità;

* i massimi di $V(x)$ corrispondono a barriere probabilistiche;

* aumentando $\sigma$, la distribuzione si appiattisce;

* diminuendo $\sigma$, la densità si concentra sempre più vicino ai minimi del potenziale.

Questa è la controparte probabilistica dell’immagine del paesaggio introdotta nella parte deterministica del corso.

# 6. Esempio 1 -- Drift costante e diffusione costante

Consideriamo la SDE

$$
dX_t = \mu\,dt + \sigma\,dW_t\;.
$$

La Fokker--Planck associata è

$$
\partial_t p = -\mu\,\partial_x p + \frac{\,\sigma^2}{\!2}\,\partial_x^2 p\;.
$$

## 6.1 Interpretazione

* il termine con $\mu$ trasporta "rigidamente" (trasla) la distribuzione;

* il termine diffusivo la allarga nel tempo.

Se all’inizio tutta la probabilità è concentrata in un punto, la soluzione diventa una gaussiana con:

* media che si sposta come $\mu t$;

* varianza che cresce linearmente come $\sigma^2 t$.

## 6.2 Caso con dato iniziale puntuale

Se la condizione iniziale è

$$
p(x,0)=\delta(x-x_0),
$$

allora la soluzione è

$$
p(x,t)=
\frac{1}{\sqrt{2\pi \sigma^2 t}}
\exp\!\left[
-\frac{(x-x_0-\mu t)^2}{2\sigma^2 t}
\right]\;.
$$

Questa formula mostra in modo trasparente i due effetti fondamentali:

* il centro della distribuzione si muove con velocità $\mu$;

* la larghezza cresce come $\sqrt{t}$.

## 6.3 Messaggio didattico

Questo è il primo esempio ideale perché separa in modo netto i due effetti:

* drift = traslazione della media;

* diffusione = dispersione crescente.

È utile anche per confrontare immediatamente una simulazione Euler--Maruyama con l’istogramma empirico delle traiettorie.

# 7. Esempio 2 -- Processo di Ornstein--Uhlenbeck

Consideriamo ora

$$
dX_t = -\lambda X_t\,dt + \sigma\,dW_t,
\qquad \lambda > 0\;.
$$

La Fokker--Planck associata è

$$
\partial_t p(x,t) = \partial_x\!\bigl(\,\lambda x\,p(x,t)\,\bigr)
+ \frac{\sigma^2}{2}\partial_x^2 p(x,t)\;.
$$

## 7.1 Interpretazione

Qui il drift non è costante, ma riporta il sistema verso l’origine:

* per $x>0$, il drift punta verso sinistra;

* per $x<0$, il drift punta verso destra.

Il rumore continua invece a disperdere la probabilità.

## 7.2 Stato stazionario

Imponendo corrente stazionaria nulla,

$$
\lambda x\,p_{\mathrm{st}}(x) + \frac{\sigma^2}{2}\partial_x p_{\mathrm{st}}(x) = 0\;.
$$

Si ottiene

$$
p_{\mathrm{st}}(x) \propto 
\exp\!\left(-\frac{\lambda x^2}{\sigma^2}\right)\;,
$$

cioè una distribuzione gaussiana centrata.

Dopo normalizzazione,

$$
p_{\mathrm{st}}(x) =
\sqrt{\frac{\lambda}{\pi \sigma^2}}
\exp\!\left(-\frac{\lambda x^2}{\sigma^2}\right)\;.
$$

## 7.3 Bilancio tra confinamento e rumore

Questo esempio mostra bene la competizione tra due effetti opposti:

* il drift lineare tende a riportare le traiettorie verso l’origine;

* il rumore tende ad allargare la distribuzione.

Lo stato stazionario rappresenta il compromesso tra questi due meccanismi.

## 7.4 Messaggio didattico

Questo esempio è particolarmente adatto perché:

* la SDE è già nota dalla lezione precedente;

* il drift di richiamo è intuitivo;

* la distribuzione stazionaria è esplicita;

* mostra bene la competizione tra confinamento e diffusione.

# 8. Esempi opzionali

## 8.1 Esempio opzionale A -- Doppio pozzo e metastabilità

Consideriamo

$$
dX_t = -U'(X_t)\,dt + \sigma\,dW_t\;,
$$

con potenziale

$$
U(x) = \frac{x^4}{4} - \frac{x^2}{2}\;.
$$

La Fokker--Planck associata è

$$
\partial_t p = \partial_x\!\bigl(\,U'(x)\,p\,\bigr)
+ \frac{\sigma^2}{2}\partial_x^2 p\;.
$$

La distribuzione stazionaria formale è

$$
p_{\mathrm{st}}(x) \propto \exp\!\left(-\frac{2U(x)}{\sigma^2}\right)\;.
$$

### Interpretazione

Il potenziale ha due minimi separati da una barriera:

* la densità tende ad accumularsi nei due pozzi;

* il rumore permette transizioni rare da un pozzo all’altro;

* per rumore debole si osserva metastabilità.

Questo esempio è eccellente per collegare Fokker--Planck alle idee già introdotte sui paesaggi di potenziale, bacini e tipping.

### Lettura fisica

Se il sistema parte in prossimità di uno dei due minimi, per tempi intermedi la densità può restare concentrata quasi tutta in un solo pozzo.
Solo su tempi più lunghi il rumore induce attraversamenti della barriera e porta gradualmente verso la distribuzione stazionaria simmetrica.

Questa separazione di scale temporali è il segno distintivo della metastabilità.

## 8.2 Esempio opzionale B -- Domini finiti e condizioni al bordo

In un intervallo finito $x \in [0,L]$, la Fokker--Planck richiede anche condizioni al bordo.

### Pareti riflettenti

Se ai bordi non può uscire probabilità, si impone corrente nulla:

$$
J(0,t)=0\;, \quad J(L,t)=0\;.
$$

Questo significa che la massa di probabilità resta confinata nel dominio.

### Pareti assorbenti

Se invece il sistema viene rimosso quando raggiunge il bordo, si impone tipicamente

$$
p(0,t)=0\;, \quad p(L,t)=0
$$

oppure una formulazione equivalente in termini di flusso uscente.

### Messaggio didattico

Questo esempio è utile per mostrare che la Fokker--Planck non dipende solo dall’equazione, ma anche dalla geometria del problema e dal tipo di interazione con i bordi.

### Significato probabilistico dei bordi

* con bordi riflettenti, le traiettorie non possono lasciare il dominio, e la probabilità totale resta confinata;

* con bordi assorbenti, una parte della massa di probabilità viene progressivamente persa, perché le traiettorie che raggiungono il bordo vengono eliminate dal sistema osservato.

Questo linguaggio è molto utile quando si studiano tempi di primo passaggio, escape e processi di assorbimento.

# 9. Collegamento con la simulazione

La Fokker--Planck non sostituisce la simulazione delle traiettorie: la completa.

In pratica si possono confrontare due approcci:

1. simulare molte traiettorie con Euler--Maruyama;

2. costruire l’istogramma empirico a un tempo fissato;

3. confrontarlo con la densità $p(x,t)$ prevista dalla Fokker--Planck.

Questo confronto è molto utile dal punto di vista computazionale perché mostra che:

* le traiettorie singole restano casuali;

* la densità collettiva evolve in modo regolare e deterministico.

## 9.1 Strategia pratica in laboratorio

Una buona procedura computazionale è la seguente:

1. fissare una condizione iniziale $X_0=x_0$;

2. generare molte realizzazioni indipendenti della SDE;

3. raccogliere i valori $X_t$ a un tempo finale fissato;

4. costruire un istogramma normalizzato;

5. confrontarlo con la soluzione teorica della Fokker--Planck, quando disponibile.

Questo rende molto concreto il rapporto tra livello microscopico e livello statistico.

## 9.2 Collegamento con l’accuratezza debole

Dal punto di vista numerico, la Fokker--Planck è anche il contesto naturale in cui interpretare l’accuratezza debole degli schemi per SDE.
Se ci interessa riprodurre bene la distribuzione o le medie di osservabili, il problema non è più la fedeltà di una singola traiettoria, ma la correttezza statistica dell’insieme delle realizzazioni.

# 10. Una possibile derivazione formale

In una prima esposizione non è necessario entrare nei dettagli tecnici della derivazione.
È però utile sapere da dove proviene, almeno a livello formale, la struttura della Fokker--Planck.

L’idea è applicare la formula di Itô a una funzione test regolare $f(X_t,t)$ e poi passare al valore atteso.
Nel caso scalare,

$$\
dX_t = a(X_t,t),dt + b(X_t,t),dW_t,\
$$

la formula di Itô dà

$$
df(X_t,t) = \left( \partial_t f
+ a\,\partial_x f
+\frac{1}{2}b^2\partial_x^2 f \right)dt
+ b\,\partial_x f\,dW_t\;.
$$

Prendendo il valore atteso, il termine in $dW_t$ ha media nulla e resta

$$
\frac{d}{dt}\mathbb{E}[f(X_t,t)] =
\mathbb{E}\left[
\partial_t f + a\,\partial_x f + \frac{1}{2}b^2\partial_x^2 f
\right]\;.
$$

Scrivendo ora il valore atteso in termini della densità $p(x,t)$ e integrando per parti in modo formale, si trasferiscono le derivate da $f$ a $p$, ottenendo infine

$$
\partial_t p = -\partial_x(ap) + \frac{1}{2}\partial_x^2(b^2p)\;.
$$

Questa derivazione non è completamente rigorosa nei dettagli, ma è molto utile per capire perché la struttura della PDE rifletta esattamente quella del calcolo di Itô.

# 11. Sintesi finale

L’equazione di Fokker--Planck descrive l’evoluzione deterministica della densità associata a una dinamica stocastica continua.

Per una SDE di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t
$$

la densità soddisfa

$$
\partial_t p = -\partial_x(ap)
+ \frac{1}{2}\partial_x^2(b^2 p)\;.
$$

I due termini corrispondono a:

* trasporto dovuto al drift;

* diffusione dovuta al rumore.

Scritta come

$$
\partial_t p + \partial_x J = 0\;,
$$

la Fokker--Planck appare come una legge di conservazione della probabilità, con una corrente $J$ che codifica il flusso probabilistico.

Dal punto di vista concettuale, questa lezione completa la descrizione introdotta con le SDE:

* la SDE descrive le singole traiettorie;

* la Fokker--Planck descrive la loro distribuzione.

Questa è la base naturale per sviluppi successivi: stati stazionari, tempi di rilassamento, transizioni rare, equazioni di Kramers, metodi numerici per PDE stocastiche e collegamenti con processi a salti.

## Take home messages

1. La casualità sta nelle traiettorie, non nell’evoluzione della densità.

2. La master equation è il ponte naturale tra processi di salto e limite diffusivo.

3. Drift e rumore della SDE diventano trasporto e diffusione nella Fokker--Planck.

4. La corrente di probabilità è lo strumento giusto per leggere conservazione, equilibrio e bordi.

5. Gli stati stazionari collegano in modo diretto dinamica stocastica e paesaggi di potenziale.

6. Simulare molte traiettorie e osservare la densità empirica è il ponte computazionale tra SDE e Fokker--Planck.
