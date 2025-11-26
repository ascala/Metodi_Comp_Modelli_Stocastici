---
title: "Simulazioni di eventi discreti (Gillespie e oltre)"
author: ""
date: ""
---

# Simulazioni di eventi discreti (Gillespie e oltre)

Molti sistemi reali non evolvono in modo continuo, ma attraverso **eventi discreti**: un’infezione, una nascita, una reazione chimica. Il metodo di Gillespie fornisce una procedura esatta per generare simulazioni coerenti con le leggi di probabilità del processo sottostante. Questa lezione mostra come funziona e come adattarlo a contesti diversi in cui gli eventi avvengono in tempi discreti e casuali.

### Obiettivi didattici specifici

1. Introdurre il concetto di **processo a eventi discreti** e la logica della simulazione diretta.  
2. Capire il significato di **tempo di attesa** e la sua distribuzione esponenziale.  
3. Presentare e implementare il **metodo di Gillespie** per reazioni stocastiche.  
4. Estendere il metodo a sistemi complessi (epidemie, reti, agent–based).  
5. Confrontare diversi approcci: simulazione esatta, tau-leaping, approssimazioni continue.


### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Introduzione ai processi a eventi discreti** – cosa sono e dove si applicano.  
2. **Tempo di attesa e legge esponenziale** – probabilità che un evento avvenga dopo un certo tempo.  
3. **Algoritmo di Gillespie (Direct Method)** – simulazione passo per passo.  
4. **Estensioni e approssimazioni** – tau-leaping e metodi ibridi.  
5. **Applicazioni interdisciplinari** – reazioni chimiche, epidemie, dinamiche sociali.

---

## 1. Processi a eventi discreti

Un processo a eventi discreti è descritto da:
- un insieme di **stati** $S = \{s_1, s_2, \dots\}$,  
- un insieme di **transizioni** (eventi) con **tassi** $a_i(x)$ che dipendono dallo stato $x$,  
- una regola che specifica come lo stato cambia dopo ogni evento.

Esempi:
- una molecola che reagisce ($A + B \to C$),  
- una persona che si infetta ($S \to I$),  
- un cliente che entra in coda ($n \to n+1$).

L’evoluzione è **stocastica**: il tempo e il tipo del prossimo evento sono casuali.

---

## 2. Tempo di attesa e legge esponenziale

Quando si descrive un processo in cui gli eventi avvengono **in modo casuale ma con una frequenza media costante nel tempo**, si introduce il concetto di **tasso di evento** o **tasso di Poisson**, indicato con $\lambda$.  
Questo valore rappresenta, in media, **quante volte per unità di tempo** ci si aspetta che l’evento accada.  

Esempi intuitivi:
- il decadimento radioattivo di un atomo (ogni atomo ha la stessa probabilità per unità di tempo di decadere);
- l’arrivo di clienti in un negozio dove il flusso medio è costante;
- l’arrivo di messaggi o richieste in un sistema informatico con traffico stazionario.

In tutti questi casi non esiste una “memoria”: il fatto che un evento non sia ancora avvenuto **non cambia** la probabilità che accada nel prossimo istante.  
Questa proprietà è detta **assenza di memoria** o **memorylessness**.

---

### Da dove nasce la distribuzione esponenziale

Immaginiamo un processo con tasso costante $\lambda$.  
La probabilità che **nessun evento** sia ancora avvenuto fino al tempo $t$ è indicata con $S(t)$ (funzione di sopravvivenza).  
Nel piccolo intervallo di tempo $\Delta t$, la probabilità che **non accada nulla** è circa $(1 - \lambda \Delta t)$, e quindi:

$$
S(t + \Delta t) = S(t)\,(1 - \lambda \Delta t).
$$

Sviluppando al primo ordine ($S(t + \Delta t) \approx S(t) +\frac{dS}{dt} \Delta t$) e passando al limite per $\Delta t \to 0$, si ottiene l’equazione differenziale:

$$
\frac{dS}{dt} = -\lambda S(t),
$$

che descrive il decadimento esponenziale della probabilità di “non aver ancora visto un evento”.

La soluzione, imponendo $S(0)=1$, è

$$
S(t) = e^{-\lambda t}.
$$

Poiché $S(t)$ rappresenta la probabilità che l’evento **non** sia ancora avvenuto entro $t$, la probabilità che **sia avvenuto almeno una volta** è:

$$
P(T < t) = 1 - S(t) = 1 - e^{-\lambda t}.
$$

Derivando rispetto a $t$ [¹], si ottiene la densità di probabilità del **tempo di attesa**:

$$
p(t) = \frac{d}{dt}P(T < t) = \lambda e^{-\lambda t},
$$

che è la **distribuzione esponenziale** con valore medio $E[T] = 1/\lambda$.

[¹] Ricordiamo che $p(t)dt$ indica la probabilità che un evento avvenga fra un tempo $t$ e $t+dt$.  
D'altro canto, se conosco la funzione di distribuzione cumulativa $P(T < t)$, posso scrivere tale probabilità come la differenza tra le probabilità cumulative ai due estremi dell’intervallo:

$$
p(t)\,dt = P(T < t + dt) - P(T < t).
$$

Passando al limite per $dt \to 0$, ottengo:

$$
p(t) = \frac{d}{dt}P(T < t),
$$

cioè la densità di probabilità è la **derivata** della probabilità cumulativa.  

---

### Interpretazione e simulazione

Il significato operativo di questa legge è che il sistema “attende” un tempo casuale $\tau$ prima che accada il prossimo evento, e che tempi lunghi sono possibili ma sempre meno probabili.

Per generare un tempo di attesa in una simulazione, si estrae un numero casuale $U$ uniforme in $[0,1)$ e si applica l’inversa della funzione cumulativa:

$$
\tau = -\frac{1}{\lambda}\ln U.
$$

Questo valore $\tau$ rappresenta il tempo che il sistema dovrà attendere prima che avvenga il prossimo evento.

Riassumendo:
- $\lambda$ = tasso medio di eventi per unità di tempo.  
- $1/\lambda$ = tempo medio di attesa.  
- La legge esponenziale nasce da un processo **senza memoria** in cui la probabilità di un evento per unità di tempo rimane costante.  
- È la base del **metodo di Gillespie**, che usa proprio questa estrazione per decidere il momento del prossimo evento.

---

## 3. Algoritmo di Gillespie (Direct Method)

### 3.1 Idea generale

L’idea alla base del metodo di Gillespie è sorprendentemente semplice: se conosciamo **quanto spesso** ciascun tipo di evento può verificarsi, possiamo simulare l’evoluzione del sistema un evento alla volta, rispettando le leggi di probabilità del processo.  
In altre parole, invece di avanzare il tempo in piccoli passi fissi (come nelle simulazioni <u>deterministiche</u> basate sull'integrazione di equazioni differenziali), il tempo “salta” direttamente da un evento al successivo.

Immaginiamo un sistema che può produrre $M$ tipi diversi di eventi: ad esempio, in un modello chimico potrebbero essere $M$ reazioni, in un’epidemia $M$ tipi di transizione (infetto → guarito, suscettibile → infetto, ecc.).  
Per ogni evento $j$ conosciamo il suo **tasso di accadimento** $a_j(x)$, che dipende dallo stato corrente $x$ del sistema.

Il tasso totale con cui può avvenire *qualunque* evento è:

$$
a_0(x) = \sum_{j=1}^{M} a_j(x).
$$

Questo valore rappresenta, intuitivamente, la **velocità complessiva** con cui il sistema “si muove” da uno stato al successivo.

---

### 3.2 Il passo di simulazione

A ogni iterazione della simulazione si compiono due scelte casuali fondamentali:

1. **Quando** avverrà il prossimo evento.  
   Poiché gli eventi complessivi seguono un processo di Poisson con tasso $a_0(x)$, il tempo di attesa $\tau$ è distribuito esponenzialmente.  
   Da ciò deriva la formula per estrarre il tempo del prossimo evento:

   $$
   \tau = \frac{1}{a_0(x)} \ln\!\left(\frac{1}{U_1}\right),
   $$

   dove $U_1$ è una variabile uniforme in $[0,1)$.

   In pratica, si genera un numero casuale $U_1$ e si ottiene $\tau$: un tempo breve se il sistema è molto “attivo” (grande $a_0$), o più lungo se il sistema è “quasi fermo”.

2. **Quale evento** avverrà.  
   Ogni evento $j$ compete con gli altri in proporzione al proprio tasso $a_j(x)$.  
   La probabilità che venga scelto proprio l’evento $j$ è:

   $$
   P(\text{evento } j) = \frac{a_j(x)}{a_0(x)}.
   $$

   In questo modo, eventi più probabili (con $a_j$ maggiore) hanno più possibilità di verificarsi.

---

### 3.3 Aggiornamento e ciclo

Dopo aver determinato quale evento accade:
- si **aggiorna lo stato del sistema** secondo la sua regola di transizione (ad esempio, una molecola viene consumata o un individuo cambia stato);
- si **aggiorna il tempo**: $t \to t + \tau$;
- e infine si ripete l’intero procedimento per il nuovo stato $x(t)$.

L’algoritmo genera così una sequenza di stati e tempi $(x_0, t_0), (x_1, t_1), \ldots$ che rappresentano un possibile percorso del sistema nel tempo.


Il metodo di Gillespie è una **simulazione esatta** del processo stocastico sottostante: non usa approssimazioni di tempo, ma riproduce direttamente la sequenza casuale di eventi che il modello teorico predice.  
Per questo è spesso definito un “microscopio” del caso: permette di vedere, passo dopo passo, come il comportamento complessivo di un sistema emerge dalla somma di eventi elementari e casuali.


### 3.2 Implementazione base

Per tradurre l’algoritmo di Gillespie in codice, serve prima una rappresentazione generale di come gli eventi modificano il sistema.  
In particolare, dobbiamo specificare **due elementi fondamentali**:

1. i **tassi di evento** $a_k(x)$, che descrivono quanto frequentemente può avvenire ciascun tipo di evento quando il sistema è nello stato $x$;
2. la **matrice stechiometrica** `stoich`, che descrive come lo stato cambia quando quell’evento si verifica.

Se il sistema ha $d$ variabili di stato (per esempio, le popolazioni di $d$ specie chimiche o i *compartimenti* in un modello epidemiologico) e $M$ tipi di evento, la matrice stechiometrica ha dimensione $(M, d)$.  
Ogni riga $j$ corrisponde all’evento $j$ e contiene la variazione da applicare quando quell’evento accade.

Ad esempio, per un modello epidemico con tre stati (SIR), dove

1. $S$ è il numero di individui **s**uscettibili all’infezione;  
2. $I$ è il numero di individui **i**nfettati ed **i**nfettivi;  
3. $R$ è il numero di individui che sono immuni essendosi **r**ipresi dall’infezione;

uno stato è una tripla (in questo caso un vettore riga) $[S, I, R]$  che rappresenta il numero di individui nei tre stati.  
In questo modello si consideriano due tipi di evento:

1. *infezione*: $[S, I, R] \to [S - 1, I + 1, R]$ con tasso $a_1(x) = \beta S I / N$;  
2. *guarigione*: $[S, I, R] \to [S, I - 1, R + 1]$ con tasso $a_2(x) = \gamma I$.

I tassi $a_k(x)$ vengono calcolati dinamicamente a ogni passo, in base allo stato corrente, e determinano la probabilità che un certo tipo di evento sia scelto.

La matrice stechiometrica è quindi

$$
\text{stoich} =
\begin{bmatrix}
-1 & +1 & 0 \\
0 & -1 & +1
\end{bmatrix}.
$$

dove ho associato gli indici di riga 1, 2 agli eventi *infezione* e *guarigione*.

Quando l’evento $j$ avviene, il nuovo stato si ottiene semplicemente come

$$
\text{new\_state} = \text{state} + \text{stoich}[j],
$$

cioè si somma la variazione corrispondente alla riga $j$.

Con questa notazione, l’implementazione base del metodo di Gillespie risulta estremamente compatta:

```python
import numpy as np

def gillespie_step(state, rates, stoich):
    """
    Esegue un singolo passo dell'algoritmo di Gillespie.

    state : array (d,)             stato corrente del sistema
    rates : lista di funzioni      ciascuna restituisce a_j(x)
    stoich : array (M,d)           matrice stechiometrica; riga j = variazione di stato dell'evento j

    Restituisce:
        new_state : nuovo stato dopo l'evento
        tau       : tempo di attesa
        j         : indice dell'evento scelto (0..M-1)
    """
    a = np.array([r(state) for r in rates])   # propensioni a_j(x)
    a0 = a.sum()                              # tasso totale
    if a0 == 0:
        return state, np.inf, None            # per rate 0 lo stato non cambia
    tau = np.random.exponential(1/a0)         # tempo di attesa
    j = np.searchsorted(np.cumsum(a/a0), np.random.rand())  # evento selezionato
    new_state = state + stoich[j]             # aggiorna lo stato
    return new_state, tau, j
```

### 3.3 Esempio: reazione $A \to \emptyset$

Consideriamo il caso più semplice possibile: una sola specie $A$ che decade spontaneamente con tasso costante $\lambda = 0.1$.  
Ogni molecola di $A$ può scomparire indipendentemente dalle altre, e il sistema evolve per eventi discreti di tipo
$$
A \longrightarrow \emptyset.
$$
In questo caso:
- lo stato è semplicemente $x = [A]$, il numero di molecole presenti;
- il tasso di evento è $a(x) = \lambda A$;
- la variazione di stato è $\Delta x = [-1]$.

L’implementazione in Python risulta quindi:

```python
def rate_A_to_null(state):
    return 0.1 * state[0]     # tasso: lambda * A

rates = [rate_A_to_null]      # lista di funzioni di tasso
stoich = np.array([[-1]])     # matrice (1 evento x 1 variabile)
state = np.array([100])       # stato iniziale: 100 molecole

t = 0.0

trajectory = [(t, state[0])]
while state[0] > 0 and t < 100:
    state, dt, _ = gillespie_step(state, rates, stoich)
    t += dt
    trajectory.append((t, state[0]))
```

**Risultato:** il numero di molecole $A$ diminuisce nel tempo in modo irregolare, con tempi di decadimento casuali.  
Ogni traiettoria simulata mostra un andamento _a gradini_, ma la media su molte repliche segue un decadimento esponenziale con legge  
$$  
\langle A(t) \rangle = A_0 e^{-\lambda t}.  
$$

Questo esempio illustra chiaramente come l’algoritmo di Gillespie ricostruisca la dinamica microscopica degli eventi discreti, restituendo traiettorie individuali coerenti con il comportamento statistico previsto analiticamente.

***

## 4. Estensioni e approssimazioni

### 4.1 Tau-leaping

Quando i tassi di evento sono molto alti, il metodo di Gillespie può diventare inefficiente: il sistema compie moltissimi eventi simili in tempi molto brevi.  
In questi casi, invece di simulare ogni evento singolarmente, si può **saltare in avanti di un intervallo temporale finito** $\Delta t$, assumendo che i tassi $a_j(x)$ restino quasi costanti in quell’intervallo.

In tale intervallo, il **numero di eventi** del tipo $j$ segue una distribuzione di Poisson:

$$
k_j \sim \text{Poisson}(a_j(x)\,\Delta t).
$$

Lo stato viene poi aggiornato sommando i contributi di tutti gli eventi che si sono verificati nel salto temporale:

$$
x \;\to\; x + \sum_j k_j\,\nu_j,
$$

dove $\nu_j$ è il vettore di variazione (la riga $j$ della matrice stechiometrica).  

Tuttavia, questa approssimazione è valida solo se gli eventi sono **commutativi**, cioè se l’ordine in cui avvengono non cambia il risultato finale.[^non_commut] 
Ciò accade nei processi puramente quantitativi, dove ciascun evento aggiunge o rimuove oggetti in modo indipendente (come nelle reazioni chimiche o nei modelli di nascita–morte).  
Se invece gli eventi interagiscono o modificano la struttura del sistema, il tau-leaping può introdurre errori e richiede varianti più controllate.

In queste condizioni, il **tau-leaping** permette di ridurre drasticamente il numero di iterazioni mantenendo una buona accuratezza, ed è un ponte naturale verso le **equazioni di Langevin chimiche**, dove le fluttuazioni vengono trattate come rumore continuo.

[^non_commut]: L’assunzione di commutatività è valida quando gli eventi **cambiano solo il numero di oggetti** (molecole, individui, pacchetti, ecc.), senza introdurre vincoli o stati qualitativi, e le variazioni sono **additive** e indipendenti dal percorso.  
Esempi tipici sono le reazioni chimiche del tipo $A \to B$ o $A + B \to C$, i modelli di nascita–morte o epidemici in cui $(S,I,R)$ rappresentano numeri di individui, e i sistemi di code o traffico dove le quantità cambiano in modo lineare.  
In questi casi, l’ordine degli eventi in $\Delta t$ non influisce sullo stato finale.  
Viceversa, la commutatività non vale quando gli eventi **modificano la struttura del sistema**, introducono **vincoli logici** (ad esempio: se $A$ é accaduto, $B$ non puó accadere) o **interazioni** tali che l’esito di un evento alteri la probabilità di un altro nello stesso intervallo: in tali situazioni il tau–leaping può introdurre errori sistematici (ad esempio il problema delle *negative populations*).

### 4.2 Metodi ibridi e approssimazioni continue

Quando nel sistema coesistono processi lenti e veloci, o variabili discrete e continue, si ricorre a **approcci ibridi**:
- alcune reazioni o transizioni sono simulate in modo discreto (come nel metodo di Gillespie);
- altre sono approssimate con equazioni differenziali o stocastiche continue.

Il metodo di Gillespie fornisce infatti la **descrizione microscopica esatta** del processo di salto, da cui si possono derivare, mediante espansioni di Kramers–Moyal, le forme continue che conducono all’equazione di **Fokker–Planck** o alla corrispondente **equazione di Langevin**.  
Quando il numero di entità è grande e le fluttuazioni relative diventano piccole, il processo può essere rappresentato da una **approssimazione diffusive** del tipo

$$
dx = f(x)\,dt + G(x)\,dW_t,
$$

dove $f(x)$ rappresenta la dinamica media deterministica e $G(x)\,dW_t$ introduce le fluttuazioni casuali residue.

Queste approssimazioni, derivate direttamente dal formalismo stocastico di Gillespie, sono oggi ampiamente utilizzate in contesti molto diversi:
- dinamiche di popolazioni biologiche,  
- modelli di traffico e flussi in rete,  
- sistemi di comunicazione o di coda,  
- e modelli epidemici su reti complesse.

Esse permettono di passare senza soluzione di continuità dal livello microscopico (eventi discreti) a quello mesoscopico o macroscopico (dinamiche medie e rumore continuo), mantenendo il legame formale con la teoria stocastica di partenza. 
In questo regime non si esegue più una simulazione evento–per–evento come nel metodo di Gillespie, ma si integrano direttamente le corrispondenti equazioni stocastiche — un approccio che sarà approfondito nel capitolo *Rumore e dinamiche stocastiche*.

---
## 5. Applicazioni interdisciplinari

### 5.1 Reazioni chimiche

Il metodo di Gillespie nasce per modellare sistemi chimici in cui le concentrazioni sono basse e il rumore è importante (es. regolazione genica).

### 5.2 Modelli epidemiologici

In un modello SIR discreto:

* $S \to I$ con tasso $\beta S I / N$,

* $I \to R$ con tasso $\gamma I$.

Lo stesso algoritmo si applica scegliendo i due tipi di eventi e aggiornando gli stati di conseguenza.

### 5.3 Sistemi sociali e agent–based

Ogni interazione tra agenti (adozione di un’idea, scambio, uscita da un gruppo) può essere trattata come un **evento discreto** con un proprio tasso.\
Il framework di Gillespie fornisce un linguaggio unificato per descrivere tali dinamiche.


## 5. Applicazioni interdisciplinari

L’approccio a eventi discreti non è confinato alla chimica o alla fisica statistica: è un linguaggio generale per descrivere **sistemi complessi** in cui i cambiamenti avvengono attraverso transizioni elementari, ciascuna con una certa probabilità per unità di tempo.  
In questi contesti, l’algoritmo di Gillespie o le sue varianti forniscono un quadro unificato per simulare e analizzare l’evoluzione temporale dei sistemi.

---

### 5.1 Reazioni chimiche

Il metodo di Gillespie nasce originariamente per modellare sistemi chimici in cui le **concentrazioni sono basse** e le fluttuazioni diventano rilevanti.  
In un ambiente cellulare, ad esempio, può esserci un numero ridotto di molecole regolatrici, e il comportamento medio descritto da equazioni differenziali non è più sufficiente.

Esempi tipici:

1. **Reazione di decadimento**  
   $A \to \emptyset$ con tasso $\lambda A$:  
   è il caso classico già simulato nella sezione precedente.

2. **Reazione bimolecolare**  
   $A + B \to C$ con tasso $a(x) = kAB$:  
   gli eventi corrispondono agli urti fra molecole di tipo $A$ e $B$, e ogni evento riduce di una unitá $A$ e $B$, aumentando di una unitá $C$.

3.3. **Regolazione genica**

Un gene può trovarsi in due stati: **acceso** ($G_{\text{on}}$) o **spento** ($G_{\text{off}}$).  
Solo quando è acceso produce una proteina $P$.  
Il sistema può essere rappresentato dalle seguenti reazioni:

$$
\begin{aligned}
G_{\text{off}} &\xrightarrow{k_{\text{on}}} G_{\text{on}}, \\
G_{\text{on}} &\xrightarrow{k_{\text{off}}} G_{\text{off}}, \\
G_{\text{on}} &\xrightarrow{k_{\text{prod}}} G_{\text{on}} + P, \\
P &\xrightarrow{k_{\text{deg}}} \emptyset.
\end{aligned}
$$

Le prime due descrivono l’alternanza **stocastica** dello stato del gene (accensione e spegnimento), mentre le ultime due governano la produzione e il decadimento della proteina.
Quando le frequenze di accensione e spegnimento sono confrontabili con i tempi di produzione e degradazione, il numero di proteine mostra forti **fluttuazioni**:   la cellula produce impulsi di proteine durante i periodi “on”, separati da fasi “off” di silenzio.  
Queste dinamiche a **burst** di espressione genica sono osservate sperimentalmente e rappresentano un esempio emblematico del ruolo del rumore intrinseco nei sistemi biologici discreti.


---

### 5.2 Modelli epidemiologici

Il formalismo di Gillespie si adatta in modo naturale anche ai modelli di epidemie, dove le transizioni tra compartimenti avvengono in tempi casuali, come nel modello **SIR discreto** cha abbiamo giá incontrato allínizio del capitolo:

- *infezione*: $S \to I$ con tasso $a_1(x) = \beta S I / N$;  
- *guarigione*: $I \to R$ con tasso $a_2(x) = \gamma I$.

Il metodo riproduce le fluttuazioni casuali nel numero di infetti e permette di stimare, ad esempio, la distribuzione dei tempi di picco o la probabilità di estinzione precoce dell’epidemia.

Varianti più complesse includono:
- **modelli a metapopolazioni** o su **reti di contatto**, dove ciascun nodo rappresenta una città o una comunità e gli eventi descrivono infezioni o spostamenti;  
- **modelli multi–ceppo**, con eventi di mutazione o competizione fra varianti.

---

### 5.3 Sistemi sociali e agent–based

In ambito sociale o economico, le interazioni tra individui o agenti possono essere descritte anch’esse come **eventi discreti**: adozione di un’idea, scambio di informazioni, uscita o ingresso in un gruppo, scelta di un prodotto, o cambiamento di opinione.

Ogni evento ha un proprio tasso che dipende dallo stato del sistema — per esempio, dal numero di vicini che condividono una certa opinione o dal livello di esposizione a un messaggio.  
Il formalismo di Gillespie permette quindi di:

- simulare dinamiche di **diffusione dell’informazione** (analoghe alla diffusione di un’infezione);
- studiare la **polarizzazione** e la formazione di comunità;
- modellare **mercati digitali** o sistemi di reputazione, dove gli eventi rappresentano scambi, raccomandazioni o aggiornamenti di punteggio.

Ad esempio, in un semplice modello di adozione di innovazione, consideriamo due tipi di individui:

- $S$: non ancora adottanti;
- $I$: adottanti (hanno già accettato o diffuso l’innovazione).

Un individuo non adottante può adottare con tasso proporzionale al numero $n_I$ di vicini adottanti:

- *adozione*: $S \to I$ con tasso $a_1(x) = \beta S n_I / N$.

La logica è formalmente identica al modello epidemiologico, ma il significato del parametro $\beta$ cambia: non misura la probabilità di contagio biologico, bensì l’influenza sociale o la pressione imitativa nel processo di diffusione.


---

### 5.4 Altri contesti

Il paradigma a eventi discreti trova applicazione anche in:
- **ecologia** (nascita, morte, competizione tra specie);  
- **finanza** (transazioni e ordini come eventi puntuali in un book di mercato);  
- **traffico e reti di comunicazione** (arrivi, partenze, congestione);  
- **neuroscienze** (potenziali d’azione di neuroni modellati come eventi di soglia).

In tutti questi casi, ciò che conta è la possibilità di rappresentare la dinamica attraverso **transizioni stocastiche elementari**, mantenendo il legame tra livello microscopico (gli eventi) e fenomenologia macroscopica (le distribuzioni e le medie osservabili).

---

## Riferimenti

* Gillespie, D. T. (1977). *Exact stochastic simulation of coupled chemical reactions*. J. Phys. Chem. 81(25): 2340–2361.

* Gibson, M. A., & Bruck, J. (2000). *Efficient exact stochastic simulation of chemical systems with many species and many channels*. J. Phys. Chem. A 104(9): 1876–1889.

* Higham, D. J. (2008). *Modeling and simulating chemical reactions*. SIAM Review, 50(2): 347–368.

* Allen, L. J. S. (2003). *An Introduction to Stochastic Processes with Applications to Biology*. Pearson.

* Wilkinson, D. J. (2006). *Stochastic Modelling for Systems Biology*. CRC Press.

---
