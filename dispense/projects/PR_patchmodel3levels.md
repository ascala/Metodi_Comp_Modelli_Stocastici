---
title: "Project: Geografia Ecologica"
subtitle: "Dal movimento individuale ai modelli a patch: modelli stocastici su paesaggio eterogeneo"
author: ""
date: ""
---

# Idea generale

Il progetto è costruito come una sequenza di tre livelli descrittivi sullo **stesso paesaggio raster**:

1. **movimento di un singolo individuo** su una mappa eterogenea;

2. **movimento di molti individui interagenti**, per mostrare sia l'emergere di effetti collettivi sia l'aumento del costo computazionale;

3. **passaggio a un modello semplice a patch**, in cui i patch sono definiti a priori a partire dalla struttura della mappa, mentre la rete e i parametri dinamici sono inferiti dai modelli microscopici.

L'obiettivo didattico è mostrare:

* come si costruisce un modello stocastico spaziale;

* come si passa da una descrizione microscopica a una descrizione macroscopica;

* come il coarse graining possa essere realizzato in modo controllato;

* come una stessa struttura spaziale possa essere letta a diversi livelli.

# Paesaggio comune

Si considera una griglia bidimensionale di celle. Ogni cella rappresenta una porzione di territorio ed è caratterizzata da una classe ambientale.

Una scelta semplice è:

* `0` = barriera non attraversabile;

* `1` = habitat ostile;

* `2` = habitat neutro;

* `3` = habitat favorevole.

La mappa è **fissa** in tutti e tre i moduli. Ciò che cambia è la descrizione dinamica della popolazione sulla mappa.

# Definizione dei patch

In questa versione del progetto, i patch **non** vengono definiti come regioni emergenti di occupazione, ma come regioni della mappa identificate a priori sulla base delle proprietà ambientali delle celle.

La scelta più naturale è definire come patch le **componenti connesse delle celle favorevoli**. Per esempio:

* si selezionano tutte le celle con valore `3`;

* ogni componente connessa di queste celle viene interpretata come un patch di habitat.

In questo modo i patch hanno una definizione geometrica chiara e stabile nel tempo. Questo semplifica molto il problema e consente di distinguere nettamente tra:

* **struttura del paesaggio**, fissata dalla mappa;

* **dinamica della popolazione**, studiata nei moduli 1 e 2;

* **modello aggregato a patch**, costruito nel modulo 3.

# Modulo 1 -- Singolo individuo

## Obiettivo

Studiare il movimento stocastico di un individuo in un paesaggio eterogeneo e usare tale dinamica per inferire la connettività effettiva tra patch.

## Stato del sistema

Lo stato al tempo $t$ è dato dalla posizione dell'individuo sulla griglia, ed eventualmente da una variabile binaria vivo/morto.

## Dinamica

Ad ogni passo temporale, l'individuo:

1. sceglie una cella vicina accessibile;

2. si muove con probabilità che può dipendere dal tipo di cella di arrivo;

3. può morire con probabilità che dipende dalla cella occupata.

Si possono usare vicini di von Neumann oppure di Moore.

## Versione minima

* movimento uniforme tra celle accessibili;

* mortalità dipendente dal tipo di habitat;

* arresto della simulazione quando l'individuo muore oppure raggiunge un patch target.

## Osservabili

* probabilità di raggiungere un patch target;

* tempo medio di first passage;

* tempo medio di sopravvivenza;

* distanza media percorsa;

* mappa delle frequenze di visita.

## Ruolo del Modulo 1 nel coarse graining

Il Modulo 1 serve soprattutto a costruire una **rete di connettività effettiva tra patch**.

Se i patch sono etichettati come $P_1,\dots,P_M$, si possono lanciare molte simulazioni partendo da una cella del patch $P_j$ e registrare se il cammino raggiunge il patch $P_k$.

Questo consente di definire una matrice di pesi

$$
W_{j\to k},
$$

dove, per esempio,

$$
W_{j\to k}=\Pr(\text{raggiungere } P_k \mid \text{partenza da } P_j).
$$

In alternativa, si può usare il tempo medio di first passage $\tau_{ij}$ oppure una combinazione di probabilità di successo e tempo di attraversamento.

## Concetti stocastici coinvolti

* random walk su reticolo;

* catena di Markov a tempo discreto;

* hitting probabilities;

* first-passage times;

* assorbimento.

# Modulo 2 -- Molti individui interagenti

## Obiettivo

Mostrare come la presenza di molti individui aumenti sia la ricchezza dinamica sia il costo computazionale, e usare questa dinamica per stimare quantità aggregate a livello di patch.

## Stato del sistema

Al tempo $t$, ogni cella contiene un numero di individui

$$
n_{ij}(t) \ge 0.
$$

## Dinamica consigliata

Per mantenere il modello semplice ma non banale, ogni individuo:

1. tenta un movimento verso una cella vicina accessibile;

2. sopravvive con probabilità dipendente dal tipo di habitat e, opzionalmente, dalla densità locale;

3. può riprodursi con probabilità maggiore nelle celle favorevoli;

4. il nuovo individuo, se generato, viene collocato nella stessa cella oppure in una cella vicina accessibile.

## Interazioni possibili

Per non appesantire troppo il progetto, conviene sceglierne una sola fra le seguenti:

* **esclusione locale**: ogni cella contiene al più $K$ individui;

* **mortalità densità-dipendente**: la probabilità di morte cresce con $n_{ij}(t)$;

* **riproduzione limitata dalla densità**: la natalità diminuisce in celle affollate.

## Perché serve il Modulo 2

Se il Modulo 1 serve soprattutto a studiare l'accessibilità e la connettività tra patch, il Modulo 2 serve a produrre una vera dinamica collettiva da cui inferire quantità aggregate più ecologiche:

* occupazione media dei patch;

* persistenza temporale;

* svuotamenti locali;

* ricolonizzazioni;

* ruolo delle interazioni e della densità.

## Variabili aggregate per patch

Una volta definiti i patch $P_k$, si può introdurre per ciascuno di essi la popolazione totale

$$
N_k(t)=\sum_{(i,j)\in P_k} n_{ij}(t).
$$

Questa quantità non è ancora il modello finale del Modulo 3, ma è la variabile intermedia naturale da cui estrarre i parametri efficaci.

## Osservabili

* numero totale di individui nel tempo;

* densità media per cella;

* popolazione media in ciascun patch;

* frazione di tempo in cui un patch è occupato;

* frequenza di svuotamento di un patch;

* costo computazionale al crescere del numero di individui.

# Modulo 3 -- Modello semplice a patch occupato/vuoto

## Obiettivo

Costruire un modello macroscopico semplice in cui ogni patch viene descritto solo come **occupato** oppure **vuoto**.

Questo modello va interpretato come un coarse graining del sistema spaziale dettagliato: non descrive più il moto dei singoli individui né l'occupazione cella per cella, ma soltanto lo stato aggregato dei patch.

## Variabile di stato

Per ciascun patch $P_k$ si introduce una variabile binaria

$$
X_k(t)\in \{0,1\},
$$

dove:

* $X_k(t)=1$ significa che il patch $k$ è occupato;

* $X_k(t)=0$ significa che il patch $k$ è vuoto.

La definizione naturale è:

$$
X_k(t)=\mathbf{1}_{\{N_k(t)>0\}},
$$

dove $N_k(t)$ è la popolazione totale del patch misurata nel Modulo 2.

## Dinamica del modello a patch

Il modello più semplice ha due ingredienti:

* **estinzione locale**;

* **colonizzazione da altri patch occupati**.

### Estinzione

Se $X_k(t)=1$, il patch $k$ diventa vuoto al passo successivo con probabilità $e_k$.

### Colonizzazione

Se $X_k(t)=0$, il patch $k$ può essere colonizzato dai patch occupati vicini.

Una forma semplice è:

$$
\Pr\big(X_k(t+1)=1 \mid X_k(t)=0\big) =
1-\prod_{j\neq k}\left(1-\lambda W_{j\to k}X_j(t)\right),
$$

dove:

* $W_{j\to k}$ è il peso della connessione dal patch $j$ al patch $k$;

* $\lambda$ è un parametro globale di colonizzazione.

Questa formula esprime l'idea che più patch occupati sono connessi a $k$, maggiore è la probabilità che $k$ venga colonizzato.

## Come si inferiscono i parametri

Qui sta il vero contenuto di coarse graining del progetto.

I parametri del modello a patch **non** vengono scelti arbitrariamente, ma devono essere stimati a partire dai moduli 1 e 2.

### Rete di patch da Modulo 1

Il Modulo 1 fornisce la matrice $W_{j\to k}$, che rappresenta la connettività effettiva tra patch, dedotta dalle probabilità di attraversamento del paesaggio da parte di un singolo individuo.

### Estinzione da Modulo 2

Il Modulo 2 fornisce una stima empirica di $e_k$. Una stima semplice è:

$$e_k \approx \frac{|\{t : N_k(t)>0,\; N_k(t+1)=0\}|}{|\{t : N_k(t)>0\}|}$$

In altre parole, si conta quante volte un patch occupato si svuota al passo successivo, e si normalizza per il numero totale di volte in cui esso era occupato.

### Colonizzazione da Modulo 2

Il parametro globale $\lambda$ può essere scelto o calibrato in modo che il modello a patch riproduca, almeno grossolanamente, alcuni osservabili del Modulo 2, per esempio:

* numero medio di patch occupati;

* tempo medio di persistenza globale;

* frequenza di ricolonizzazione.

## Significato del coarse graining

Questa costruzione è un vero coarse graining, ma in una forma semplice e controllata:

* i patch sono definiti **spazialmente** a partire dalla mappa;

* la rete tra patch è inferita **dinamicamente** dal Modulo 1;

* i parametri minimi di occupazione/estinzione sono calibrati **statisticamente** dal Modulo 2.

Quindi il Modulo 3 non è un modello indipendente, ma una descrizione efficace del sistema dettagliato.

# Domande scientifiche possibili

## Modulo 1

* Quanto conta una barriera lineare nel ridurre la probabilità di raggiungere un altro patch?

* Come cambia la matrice di connettività al variare dell'ostilità della matrice ambientale?

* Quale ruolo ha un corridoio stretto tra due regioni favorevoli?

## Modulo 2

* Come cresce il costo computazionale al crescere del numero di individui?

* Quali patch risultano più persistenti?

* Quale relazione c'è tra area del patch e popolazione media?

* Come cambia la persistenza locale al variare delle interazioni?

## Modulo 3

* Il modello a patch riproduce il numero medio di patch occupati osservato nel Modulo 2?

* Quali patch hanno maggiore probabilità di estinzione?

* Quali collegamenti della rete sono più importanti per la persistenza globale?

* Quanto il comportamento macroscopico dipende dalla matrice $W_{j\to k}$ inferita dal Modulo 1?

# Struttura consigliata dell'assegnazione

## Parte obbligatoria

* implementare il Modulo 1;

* definire i patch dalla mappa;

* stimare una matrice di connettività tra patch;

* discutere l'effetto di alcune caratteristiche del paesaggio.

## Parte intermedia

* implementare il Modulo 2 con interazione semplice;

* costruire le quantità aggregate $N_k(t)$;

* misurare persistenza, svuotamenti e costo computazionale.

## Parte avanzata

* costruire il Modulo 3 occupato/vuoto;

* stimare i parametri minimi da Modulo 1 e Modulo 2;

* confrontare il comportamento del modello a patch con quello del modello multi-individuo.

# Vantaggi didattici della struttura

Questa architettura consente di mostrare in modo molto chiaro:

1. il ruolo della simulazione Monte Carlo in modelli spaziali;

2. la differenza tra descrizione individuale, descrizione many-body e descrizione aggregata;

3. il fatto che il costo computazionale diventa esso stesso un tema scientifico;

4. come i modelli aggregati nascano da una procedura di coarse graining controllata;

5. come una stessa mappa possa supportare diversi livelli di modellizzazione.

# Osservazione finale

In questa formulazione, i patch non sono entità mobili né strutture emergenti dalla sola occupazione istantanea, ma regioni dell'habitat definite a partire dalla mappa. Ciò che viene inferito dai modelli microscopici non è l'identità dei patch, ma la loro **connettività effettiva** e i loro **parametri dinamici efficaci**. Questa scelta rende il progetto più semplice, più robusto e più adatto a un contesto didattico.

# Mini-sezione operativa: pseudocodice dei tre moduli

Questa sezione non sostituisce la descrizione concettuale precedente, ma serve a rendere più esplicito come i tre livelli possano essere implementati in pratica.

## Modulo 1 -- Singolo individuo

L'idea è simulare molte traiettorie indipendenti e usarle per stimare accessibilità e connettività tra patch.

```text
Input:
- mappa raster
- lista dei patch P_1, ..., P_M
- posizione iniziale in un patch P_i
- numero di simulazioni R
- regole di movimento e mortalità

Per ogni patch iniziale P_i:
    Per ogni simulazione r = 1, ..., R:
        inizializza l'individuo in una cella di P_i
        vivo = vero
        t = 0

        Ripeti finché vivo e non ha raggiunto un altro patch:
            scegli una cella vicina accessibile
            muovi l'individuo
            aggiorna t
            con probabilità dipendente dall'habitat, l'individuo muore
            se entra in un patch P_j con j != i:
                registra il raggiungimento di P_j
                registra il tempo di first passage
                termina la traiettoria

Da queste simulazioni stima:
- probabilità di raggiungere P_j partendo da P_i
- tempo medio di first passage tra patch
- matrice di connettività W_ij
```

## Modulo 2 -- Molti individui interagenti

L'idea è simulare una popolazione distribuita sulla stessa mappa e misurare quantità aggregate a livello di cella e di patch.

```text
Input:
- mappa raster
- lista dei patch P_1, ..., P_M
- configurazione iniziale degli individui
- numero di passi temporali T
- regole di movimento
- regole di nascita/morte
- eventuale interazione locale

Inizializza n_ij(0) per tutte le celle

Per t = 0, ..., T-1:
    Per ogni individuo:
        scegli una mossa consentita
        aggiorna la posizione
        applica la sopravvivenza in base all'habitat
        applica eventuale regola di riproduzione
        applica eventuale interazione locale

    Per ogni patch P_k:
        calcola N_k(t) = somma degli individui nelle celle del patch
        registra se il patch è occupato oppure no

Alla fine della simulazione stima:
- popolazione media per patch
- frazione di tempo in cui ciascun patch è occupato
- frequenza di svuotamento dei patch
- costo computazionale al variare del numero di individui
```

## Modulo 3 -- Modello a patch occupato/vuoto

L'idea è sostituire la dinamica dettagliata con un processo stocastico binario sui patch.

```text
Input:
- lista dei patch P_1, ..., P_M
- matrice di connettività W_ij dal Modulo 1
- probabilità di estinzione e_k dal Modulo 2
- parametro globale di colonizzazione lambda
- configurazione iniziale X_k(0) in {0,1}
- numero di passi temporali T

Per t = 0, ..., T-1:
    Per ogni patch k:
        se X_k(t) = 1:
            con probabilità e_k poni X_k(t+1) = 0
            altrimenti poni X_k(t+1) = 1

        se X_k(t) = 0:
            calcola la probabilità di colonizzazione
            p_k = 1 - prodotto sui j != k di (1 - lambda W_jk X_j(t))
            con probabilità p_k poni X_k(t+1) = 1
            altrimenti poni X_k(t+1) = 0

Alla fine confronta con il Modulo 2:
- numero medio di patch occupati
- persistenza globale
- frequenza di ricolonizzazione
```

## Collegamento operativo fra i tre moduli

Il flusso logico dell'intero progetto può essere riassunto così:

```text
mappa raster
-> definizione geometrica dei patch
-> Modulo 1: stima della rete W_ij
-> Modulo 2: stima di N_k(t), occupazione e svuotamenti
-> Modulo 3: dinamica binaria sui patch
-> confronto tra modello dettagliato e modello aggregato
```

Questo schema rende esplicito che il modello a patch finale non viene introdotto indipendentemente, ma costruito a partire dalle informazioni ottenute nei moduli precedenti.

# Parti avanzate facoltative

Estensioni indipendenti del progetto, da sviluppare dopo aver completato i tre moduli principali.

## A -- Tempo interno effettivo (estensione del Modulo 1)

### Motivazione

Nel Modulo 1, il tempo di first passage tra patch è misurato come numero di passi. Questa scelta ignora il fatto che il costo biologico di attraversare una cella dipende dal suo tipo: un individuo che percorre habitat ostile accumula rischio, stress energetico o mortalità differenziale.

Questa estensione introduce un *tempo interno effettivo* in cui ogni passo contribuisce con un peso che dipende dal tipo di cella attraversata.

### Definizione

Sia $c(s)$ il costo per passo associato alla cella di tipo $s$. Per una traiettoria di $T$ passi che attraversa le celle $s_0, s_1, \dots, s_{T-1}$, il tempo interno effettivo è

$$\tau_{\mathrm{eff}} = \sum_{t=0}^{T-1} c(s_t).$$

Una scelta naturale, coerente con la mappa del progetto, è per esempio $c(1) = 3$, $c(2) = 1$, $c(3) = 0.5$, ma i valori sono liberamente modificabili.

### Implementazione

L'unica modifica al codice del Modulo 1 è aggiungere un accumulatore alla traiettoria:

```text
tau_eff = 0
Per ogni passo t nella traiettoria:
    tau_eff += c(tipo_cella(posizione_t))
Registra tau_eff alla fine della traiettoria
```

### Conseguenze sulla rete di patch

La matrice $W_{ij}$ del Modulo 1 puo essere estesa. Invece di pesare la connessione tra $P_i$ e $P_j$ con la sola probabilità di raggiungimento, si usa il tempo interno medio condizionato al successo:

$$
W^{\mathrm{eff}}_{ij} = \frac{\Pr(\text{raggiungere } P_j \mid P_i)}{\langle \tau_{\mathrm{eff}} \mid \text{raggiungere } P_j,\, P_i \rangle}.
$$

Questo separa nettamente due concetti: l'*accessibilità* (probabilità di successo) ed il *costo di connessione* (quanto e costoso, in media, attraversare il paesaggio con successo). Due patch possono essere ugualmente accessibili ma molto diversi per costo.

### Osservabili aggiuntivi

* distribuzione di $\tau_{\mathrm{eff}}$ per coppie di patch;
* correlazione tra costo effettivo e probabilità di sopravvivenza durante il transito;
* confronto tra $W_{ij}$ (probabilità) e $W^{\mathrm{eff}}_{ij}$ (costo normalizzato) nel Modulo 3.

## B -- Algoritmo di Gillespie e confronto con il tempo interno effettivo

### Motivazione

Il Modulo 3 usa un aggiornamento sincrono a passi discreti: tutti i patch vengono aggiornati simultaneamente con lo stesso passo temporale. Questa convenzione è comoda ma arbitraria. L'algoritmo di Gillespie permette di simulare lo stesso sistema come un processo a tempo continuo, in cui ogni evento (estinzione o colonizzazione) avviene al momento giusto secondo la sua propria scala temporale.

### Formulazione a tempo continuo

Si associa a ogni patch $k$ un tasso di estinzione $\mu_k$ e un tasso di colonizzazione

$$\lambda_k(t) = \lambda \sum_{j \neq k} W_{jk}\, X_j(t).$$

Il tasso totale di tutti gli eventi possibili al tempo $t$ e

$$R(t) = \sum_{k:\, X_k=1} \mu_k \;+\; \sum_{k:\, X_k=0} \lambda_k(t).$$

### Pseudocodice Gillespie

```text
t = 0
Inizializza X_k(0) per ogni patch k

Ripeti:
    calcola tutti i tassi individuali
    calcola R = somma di tutti i tassi
    estrai il tempo al prossimo evento: Delta_t ~ Exp(R)
    t = t + Delta_t
    scegli l'evento proporzionalmente al suo tasso
    aggiorna X_k

Termina quando t > T_max
```

N.B. L'aggiornamento usa sempre i valori correnti di $X_k(t)$ prima dell'evento, esattamente come nel tempo discreto. La differenza e che $\Delta t$ non e fisso ma estratto da una distribuzione esponenziale.

### Raccordo delle scale temporali

Per confrontare la simulazione di Gillespie con quella a passi discreti del Modulo 3 è necessario raccordare le scale temporali. Il raccordo naturale e

$$\mu_k = -\ln(1 - e_k), \qquad \lambda = -\ln(1 - \lambda_{\mathrm{discreto}}),$$

che converte probabilità per passo in tassi per unita di tempo.

### Collegamento con il tempo interno effettivo

L'algoritmo di Gillespie e il tempo interno effettivo dell'estensione A sono concettualmente legati: entrambi introducono una misura di tempo che non e il semplice conteggio dei passi. Il confronto naturale e verificare se il tempo interno effettivo medio di attraversamento tra $P_i$ e $P_j$, moltiplicato per $\mu_k$, predice correttamente la distribuzione dei tempi interevent nella simulazione di Gillespie.

### Osservabili aggiuntivi

* distribuzione dei tempi tra eventi di estinzione e colonizzazione;
* confronto tra il numero medio di patch occupati nel tempo discreto e in Gillespie, a parita di parametri raccordati;
* verifica che la distribuzione stazionaria sia la stessa nei due approcci;
* correlazione tra $\tau_{\mathrm{eff}}$ (estensione A) e $1/\lambda_k$ (tempo medio di attesa Gillespie per la colonizzazione di $k$).