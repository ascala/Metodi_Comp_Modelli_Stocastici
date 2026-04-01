---
title: "Project: Reti di reazioni e algoritmo di Gillespie"
subtitle: "catene di Markov a tempo continuo, chimica stocastica e simulazione esatta di eventi"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce le **reaction networks** stocastiche e l'algoritmo di **Gillespie** come caso di studio per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare una rete di reazioni come **catena di Markov a tempo continuo** su uno spazio discreto di stati;

2. distinguere chiaramente tra descrizione discreta stocastica, descrizione mean-field deterministica e, quando appropriato, limite diffusivo;

3. introdurre il concetto di **propensity** come tasso di occorrenza degli eventi elementari;

4. spiegare perché l'algoritmo di Gillespie fornisca una simulazione esatta della CTMC sottostante;

5. usare il formalismo per trattare esempi di nascita--morte, contagio, espressione genica e piccole reti biochimiche;

6. discutere quando una descrizione continua via ODE o SDE diventi insufficiente e quando invece rappresenti una buona approssimazione.

Dal punto di vista del corso, questo progetto è particolarmente importante perché introduce in modo molto esplicito un'intera classe di modelli che non coincide né con le equazioni differenziali ordinarie, né con le SDE, né con le simulazioni a passo fisso. Qui il sistema evolve per **salti discreti** e i tempi tra gli eventi sono essi stessi variabili aleatorie. È quindi uno dei luoghi migliori in cui insegnare davvero che cosa sia una dinamica event-driven su spazio discreto.

# 2. Motivazione generale

Molti sistemi reali non evolvono in modo continuo e regolare, ma attraverso eventi elementari che cambiano bruscamente lo stato del sistema.

Esempi tipici sono:

* una molecola che viene prodotta o degradata;

* un individuo che nasce o muore;

* un infetto che contagia un suscettibile;

* una proteina che si lega a un sito regolatorio;

* una preda che viene consumata da un predatore;

* una particella che subisce una trasformazione chimica discreta.

Quando le quantità in gioco sono grandi, questi sistemi possono spesso essere ben approssimati da equazioni differenziali continue. Ma quando i numeri sono piccoli, le fluttuazioni relative diventano importanti e la descrizione deterministica può essere fuorviante. In questi casi bisogna modellare esplicitamente:

* i salti discreti negli stati;

* i tempi casuali tra un evento e il successivo;

* la variabilità tra traiettorie diverse.

Questa è precisamente la situazione in cui entrano in gioco le reaction networks stocastiche.

# 3. Campi di applicazione

Il formalismo è nato in chimica stocastica, ma oggi è usato in contesti molto più ampi.

## 3.1 Reazioni chimiche elementari

Quando il numero di molecole non è molto grande, il numero di collisioni e trasformazioni elementari fluttua in modo significativo. In questo caso il modello deterministico a concentrazioni può perdere una parte importante della fenomenologia.

## 3.2 Dinamiche di nascita e morte

Un processo di nascita--morte è una delle reti di reazione più semplici possibili. Proprio per questo è un ottimo punto di ingresso per il formalismo generale.

## 3.3 Epidemiologia in popolazioni finite

Un contagio elementare come

$$
S+I \to 2I
$$

o la guarigione

$$
I \to S
$$

si scrivono naturalmente come reazioni. Quando la popolazione è piccola o il numero di infetti è basso, la descrizione stocastica è spesso più appropriata di una ODE media.

## 3.4 Espressione genica e biologia molecolare

Produzione e degradazione di mRNA e proteine, attivazione e disattivazione di geni, binding e unbinding di fattori regolatori sono tutti esempi tipici in cui la natura discreta delle molecole conta in modo essenziale.

## 3.5 Ecologia di piccole popolazioni

In sistemi con pochi individui, gli eventi di nascita, morte e interazione sono intrinsecamente discreti e il rischio di estinzione stocastica non è catturato da una descrizione puramente deterministica.

# 4. Reti di reazioni: formalismo generale

## 4.1 Stato del sistema

Consideriamo $n$ specie o tipi di entità. Lo stato del sistema al tempo $t$ è un vettore intero non negativo

$$
X(t) = (X_1(t),\dots,X_n(t)),
$$

dove $X_i(t)$ è il numero di individui o molecole della specie $i$.

## 4.2 Reazioni elementari

Supponiamo di avere $R$ reazioni elementari. Ogni reazione $r$ è caratterizzata da:

* un **vettore di variazione** o stoichiometria\
  $$
  \nu_r,
  $$
  che specifica come cambia lo stato quando la reazione avviene;

* una **propensity**
  $$
  a_r(X),
  $$
  che rappresenta il tasso con cui la reazione $r$ avviene quando il sistema si trova nello stato $X$.

Quando la reazione $r$ si verifica, lo stato viene aggiornato secondo

$$
X \to X + \nu_r.
$$

## 4.3 Significato della propensity

La propensity $a_r(X)$ ha una interpretazione probabilistica molto precisa:

$$
a_r(X),dt
$$

è, al primo ordine in $dt$, la probabilità che la reazione $r$ avvenga nell'intervallo di tempo $(t,t+dt]$ dato che il sistema è nello stato $X$ al tempo $t$.

Questo è il punto centrale dell'intero formalismo. Le reaction networks non sono soltanto “regole di aggiornamento”, ma veri processi stocastici a tempo continuo definiti da tassi locali di transizione.

# 5. Esempi fondamentali

## 5.1 Processo di nascita--morte

Il caso più semplice è un'unica specie $X$ con due reazioni:

$$
X \to X+1 \quad \text{con tasso } \lambda,\
$$
$$
X \to X-1 \quad \text{con tasso } \mu X.\
$$

Qui:

* la nascita avviene con tasso costante $\lambda$;

* la morte avviene con tasso proporzionale al numero attuale di individui.

Questo è un eccellente esempio base perché si può trattare sia analiticamente sia computazionalmente.

## 5.2 Modello SIS minimale come rete di reazioni

Un contagio SIS può essere scritto come:

$$
S+I \to 2I,\
$$
$$
I \to S.\
$$

La prima reazione rappresenta l'infezione di un suscettibile da parte di un infetto, la seconda la guarigione.

## 5.3 Espressione genica elementare

Una rete minima può includere:

* produzione di mRNA;

* degradazione di mRNA;

* produzione di proteina da mRNA;

* degradazione di proteina.

Questo caso è importante perché mostra come fluttuazioni stocastiche piccole a livello molecolare possano generare forte variabilità tra cellule.

## 5.4 Predatore--preda discreto

Si possono rappresentare in forma stocastica:

* nascita della preda;

* consumo della preda da parte del predatore;

* morte del predatore.

Questo fornisce un ponte naturale verso i modelli ecologici.

# 6. CTMC e master equation

## 6.1 Natura markoviana della dinamica

Una reaction network stocastica definisce una **catena di Markov a tempo continuo**. Lo stato futuro dipende soltanto dallo stato attuale e non dall'intera storia passata, ma i tempi di transizione sono casuali.

## 6.2 Tempo di attesa tra eventi

Se il sistema si trova nello stato $X$, il tasso totale di uscita è

$$
a_0(X) = \sum_{r=1}^R a_r(X).
$$

Il tempo fino al prossimo evento è distribuito come una variabile esponenziale:

$$
\tau \sim \mathrm{Exp}(a_0(X)).
$$

Questa proprietà è il cuore dell'algoritmo di Gillespie.

## 6.3 Master equation

Se indichiamo con $P(X,t)$ la probabilità di essere nello stato $X$ al tempo $t$, allora la sua evoluzione è governata da una **master equation**. In forma generale, il bilancio è dato da:

* probabilità che entra nello stato $X$ da stati vicini;

* probabilità che esce dallo stato $X$ a causa delle reazioni possibili.

Non è necessario sviluppare qui tutta la teoria generale, ma è importante che gli studenti capiscano che il processo microscopico possiede una descrizione probabilistica esatta a livello di distribuzione.

# 7. L'algoritmo di Gillespie

## 7.1 Idea di base

L'algoritmo di Gillespie, o **Stochastic Simulation Algorithm** (SSA), genera una traiettoria esatta del processo stocastico senza introdurre errori di discretizzazione temporale.

A stato dato $X$:

1. si calcolano tutte le propensities $a_r(X)$;

2. si somma
   $$
   a_0(X)=\sum_r a_r(X);
   $$

3. si estrae il tempo al prossimo evento
   $$
   \tau \sim \mathrm{Exp}(a_0);
   $$

4. si sceglie quale reazione avviene con probabilità proporzionale a\
   $$
   \frac{a_r(X)}{a_0(X)};
   $$

5. si aggiorna lo stato secondo il vettore stoichiometrico corrispondente.

## 7.2 Perché è esatto

Il metodo è esatto perché riproduce esattamente:

* la distribuzione del tempo al prossimo evento;

* la distribuzione condizionata del tipo di evento dato che un evento avviene.

In altre parole, non approssima la CTMC con piccoli passi temporali, ma campiona direttamente la sua dinamica reale.

## 7.3 Confronto con una simulazione a passo fisso

Una simulazione a passo fisso impone un reticolo temporale artificiale e può commettere errori se in un singolo intervallo avvengono:

* più eventi di quelli previsti;

* eventi in un ordine scorretto;

* salti con probabilità non ben approssimata.

Gillespie evita questo problema alla radice, perché il tempo stesso viene simulato come variabile casuale.

# 8. Mean-field, ODE e limite continuo

Uno dei punti didatticamente più importanti del progetto è il confronto tra diversi livelli descrittivi.

## 8.1 Descrizione microscopica discreta

Questa è la descrizione esatta quando lo stato è un vettore intero e gli eventi sono discreti. È il livello naturale di Gillespie.

## 8.2 Equazioni mean-field

Se i numeri sono grandi e le fluttuazioni relative piccole, le medie possono essere approssimate da equazioni differenziali ordinarie.

Per esempio, nel processo di nascita--morte:

$$
\frac{d}{dt}\mathbb{E}[X] \approx \lambda - \mu X.
$$

## 8.3 Limite diffusivo

In alcuni casi, con opportune riscalature, la dinamica discreta può essere approssimata da una SDE. Questo fornisce un ponte con i modelli continui già presenti nel corso.

## 8.4 Quando la descrizione continua fallisce

La descrizione deterministica diventa problematica quando:

* il numero di individui o molecole è piccolo;

* il sistema è vicino a uno stato assorbente;

* le fluttuazioni relative sono grandi;

* gli eventi rari dominano la fenomenologia.

# 9. Osservabili da misurare

Per trasformare il progetto in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 9.1 Traiettorie individuali

Le singole traiettorie mostrano in modo molto chiaro la natura a salti della dinamica.

## 9.2 Medie e varianze di ensemble

Ripetendo la simulazione su molte realizzazioni indipendenti si possono stimare:

* medie temporali;

* varianze;

* covarianze tra specie.

## 9.3 Distribuzioni stazionarie empiriche

Se il sistema ammette un regime stazionario, si può stimare empiricamente la distribuzione degli stati.

## 9.4 Tempi di estinzione o first-passage

Per sistemi con stati assorbenti o soglie di interesse, si possono misurare tempi di estinzione, tempi di raggiungimento e probabilità di hitting.

## 9.5 Confronto con le ODE mean-field

È molto utile confrontare:

* la media di ensemble delle traiettorie stocastiche;

* la soluzione delle equazioni deterministiche corrispondenti.

# 10. Domande scientifiche che il progetto permette di studiare

1. Quando la descrizione deterministica fallisce in modo qualitativo?

2. Quanto sono grandi le fluttuazioni finite-size?

3. In quali regimi la media di ensemble segue bene la dinamica mean-field?

4. Come cambia il comportamento al crescere della scala di popolazione?

5. Perché Gillespie è esatto rispetto alla CTMC sottostante?

6. In che senso tempi di estinzione o eventi rari non sono catturati bene da una ODE media?

7. Quali differenze emergono tra singole traiettorie e comportamento medio?

# 11. Pseudocodice del metodo

## 11.1 Input

* numero di specie $n$

* lista delle reazioni

* vettori stechiometrici $\nu_r$

* propensities $a_r(X)$

* stato iniziale $X(0)$

* tempo finale $T$

* numero di realizzazioni indipendenti $R$

## 11.2 Pseudocodice: algoritmo di Gillespie

```text
Inizializza lo stato X = X(0)
Poni t = 0

Finché t < T:
    calcola tutte le propensities a_r(X)
    calcola a0 = somma_r a_r(X)

    se a0 = 0:
        termina la simulazione

    estrai u1, u2 ~ U(0,1)
    calcola tau = -(1/a0) * log(u1)
    poni t <- t + tau

    scegli la reazione r tale che
        somma_{k <= r-1} a_k < u2 * a0 <= somma_{k <= r} a_k

    aggiorna lo stato:
        X <- X + nu_r

    registra eventualmente:
        - stato X
        - tempo t
        - osservabili derivate
```

## 11.3 Osservazione implementativa

Il punto importante è che il tempo non viene aggiornato in modo uniforme, ma tramite salti casuali di ampiezza variabile. Questa è la caratteristica che rende il metodo qualitativamente diverso da un integratore a passo fisso.

# 12. Schema del laboratorio

## 12.1 Laboratorio 1 -- Birth--death process

### Obiettivo

Capire la logica del formalismo su un esempio minimale.

### Attività

1. implementare il processo di nascita--morte con Gillespie;

2. simulare molte traiettorie indipendenti;

3. confrontare media e varianza con le previsioni teoriche;

4. osservare la differenza tra singole traiettorie e andamento medio.

### Domande guida

* Le traiettorie individuali sono molto fluttuanti?

* La media di ensemble segue la soluzione mean-field?

* Come cambia la variabilità relativa al crescere della popolazione media?

## 12.2 Laboratorio 2 -- SIS minimale come reaction network

### Obiettivo

Usare Gillespie su un piccolo modello epidemico discreto.

### Attività

1. implementare le reazioni $S+I \to 2I$ e $I \to S$;

2. simulare molte realizzazioni per diversi parametri;

3. misurare numero medio di infetti e tempi di estinzione;

4. confrontare con la corrispondente descrizione deterministica.

### Domande guida

* Le estinzioni stocastiche compaiono anche dove la ODE predice uno stato endemico?

* Quanto conta la dimensione totale della popolazione?

* Le fluttuazioni diventano piccole solo per popolazioni grandi?

## 12.3 Laboratorio 3 -- Gene expression o piccola rete biochimica

### Obiettivo

Mostrare che la discrezione molecolare può produrre grande variabilità tra traiettorie.

### Attività

1. implementare una piccola rete di produzione e degradazione di mRNA e proteine;

2. simulare molte cellule indipendenti;

3. misurare medie, varianze e distribuzioni stazionarie;

4. discutere il significato biologico delle fluttuazioni.

### Domande guida

* Due traiettorie con stessi parametri possono apparire molto diverse?

* La distribuzione stazionaria è larga o stretta?

* La descrizione deterministica perde la variabilità essenziale del sistema?

# 13. Estensioni possibili

Una volta implementato Gillespie nella sua forma base, si possono considerare diverse estensioni.

## 13.1 Tau-leaping

Per accelerare le simulazioni, si può usare una approssimazione in cui si fanno avanzare più eventi insieme in piccoli intervalli temporali.

## 13.2 Reazioni reversibili e detailed balance

Si possono introdurre reti semplici reversibili per discutere il rapporto tra dinamica stocastica, stati stazionari e equilibrio.

## 13.3 Collegamento con SDE

È istruttivo confrontare le traiettorie ottenute con Gillespie con una approssimazione diffusive-limit integrata tramite Euler--Maruyama.

## 13.4 Event-driven oltre la chimica

Si può discutere il collegamento con:

* queueing;

* Hawkes;

* contact process;

* modelli epidemici finiti.

## 13.5 La master equation e la sua verifica numerica

### Significato generale della master equation

Se indichiamo con $P(X,t)$ la probabilità che il sistema si trovi nello stato discreto $X$ al tempo $t$, allora la sua evoluzione è governata da una **master equation**, cioè da una equazione di bilancio delle probabilità.

L'idea è semplice: la probabilità nello stato $X$ può cambiare per due ragioni.

- probabilità che entra in $X$ da altri stati compatibili con una singola reazione;
- probabilità che esce da $X$ perché, partendo da $X$, avviene una delle reazioni possibili.

Per ogni reazione $r$, se il salto associato è $\nu_r$, allora uno stato $X-\nu_r$ può entrare in $X$ attraverso la reazione $r$, mentre da $X$ si può uscire verso $X+\nu_r$ con la stessa reazione.

### Forma generale

La forma standard è

$$
\frac{d}{dt}P(X,t) =
\sum_{r=1}^R \left[a_r(X-\nu_r)P(X-\nu_r,t) - a_r(X)P(X,t)\right],
$$

dove:

- il primo termine rappresenta i contributi entranti nello stato $X$;
- il secondo termine rappresenta i contributi uscenti dallo stato $X$.

Questa è la forma fondamentale della dinamica probabilistica esatta del sistema.

### Esempio: birth--death process

Nel caso di una sola specie $X \in \{0,1,2,\dots\}$ con:

$$
X \to X+1 \quad \text{con tasso } \lambda,
$$

$$
X \to X-1 \quad \text{con tasso } \mu X,
$$

la probabilità $P_n(t)=\Pr[X(t)=n]$ soddisfa

$$
\frac{d}{dt}P_n(t) =
\lambda P_{n-1}(t) + \mu(n+1)P_{n+1}(t) - (\lambda + \mu n)P_n(t),
$$

per $n \ge 1$, mentre per $n=0$ si ha

$$
\frac{d}{dt}P_0(t) = \mu P_1(t) - \lambda P_0(t).
$$

Questo esempio è molto istruttivo perché mostra in modo completamente esplicito il significato dei termini entranti e uscenti.

### Perché la master equation è importante

Dal punto di vista del corso, la master equation è importante per almeno tre ragioni.

Primo, rende esplicito che il modello non è solo una procedura di simulazione, ma una dinamica probabilistica ben definita.

Secondo, chiarisce la differenza tra:

- equazione per la distribuzione di probabilità;
- equazione per la media;
- traiettoria stocastica individuale.

Terzo, permette di spiegare in modo rigoroso in che senso Gillespie sia un simulatore esatto della CTMC: esso non approssima la master equation, ma genera traiettorie la cui distribuzione è esattamente quella descritta da essa.

### Verifica numerica della master equation

Per un modello semplice come il birth--death process, una procedura ragionevole di verifica è la seguente.

1. Si fissano alcuni tempi di osservazione $t_1, t_2, \dots$.
2. Si eseguono molte simulazioni indipendenti con Gillespie.
3. Per ogni tempo $t_k$, si costruisce la distribuzione empirica degli stati.
4. In parallelo, si integra numericamente la master equation su uno spazio degli stati troncato.
5. Si confrontano le due distribuzioni, per esempio tramite:
   - norma $L^1$;
   - errore quadratico;
   - confronto grafico punto per punto.

Questa attività è molto preziosa, perché mostra agli studenti che il simulatore stocastico non è una scatola nera indipendente dalla teoria, ma uno strumento che realizza concretamente la stessa dinamica descritta dalla master equation.

### Domande guida sulla verifica

- Le distribuzioni empiriche convergono alla soluzione della master equation all'aumentare del numero di realizzazioni?
- L'errore è uniforme oppure cresce nelle code della distribuzione?
- È più facile verificare la master equation a livello di media o di distribuzione completa?
- In quali modelli la soluzione esplicita è disponibile, e in quali bisogna usare un'integrazione numerica della master equation?

# 14. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce in modo molto chiaro la nozione di **CTMC su spazio discreto**, che è fondamentale ma spesso poco interiorizzata dagli studenti.

Secondo, insegna una metodologia computazionale molto importante, l'algoritmo di Gillespie, che è uno standard in molti ambiti applicativi.

Terzo, permette di confrontare in modo estremamente concreto tre livelli di descrizione:

* dinamica discreta stocastica;

* dinamica media deterministica;

* eventuale limite diffusive.

Quarto, crea ponti naturali con molti altri progetti del corso:

* con **contact process** ed **epidemie su reti**, perché il contagio può essere scritto come rete di reazioni;

* con **Hawkes**, perché entrambi sono processi a eventi ma con strutture diverse;

* con **queueing**, perché condividono una logica event-driven;

* con le **SDE**, perché offre un contrasto molto pulito tra salti discreti e rumore continuo.

## Osservazione finale

Questo progetto è uno dei migliori strumenti didattici per mostrare che il modo in cui si simula un sistema non è un dettaglio tecnico secondario, ma riflette la natura matematica del modello. Se gli eventi sono discreti e i tempi tra eventi sono casuali, la simulazione naturale non è a passo fisso: è proprio questo che Gillespie rende trasparente.

