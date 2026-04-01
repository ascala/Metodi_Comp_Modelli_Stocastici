---
title: "Project: Contact process e processi di branching"
subtitle: "estinzione, sopravvivenza e soglia critica in dinamiche di contagio locale"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce il **contact process** come caso di studio per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare una dinamica stocastica locale di attivazione e spegnimento su reticolo o su grafo;

2. mostrare come la competizione tra propagazione e decadimento generi una soglia critica;

3. distinguere tra regime di estinzione e regime di sopravvivenza persistente;

4. collegare il modello ai processi di branching come approssimazione a bassa densità;

5. introdurre osservabili quantitative per misurare sopravvivenza, densità e tempi di estinzione;

6. discutere il ruolo della topologia nel sostenere oppure spegnere l'attività.

Dal punto di vista del corso, questo progetto è particolarmente importante perché introduce uno dei modelli più semplici e più istruttivi di **transizione verso uno stato assorbente**. A differenza di altri sistemi in cui il problema centrale è l'ordine o la corrente, qui la domanda fondamentale è più netta: il sistema riesce a mantenere attività nel lungo tempo, oppure cade inevitabilmente in uno stato morto da cui non può più uscire?

# 2. Motivazione: diffusione locale e stati assorbenti

Molti sistemi reali possono essere descritti come un insieme di siti o individui che possono trovarsi in uno stato attivo oppure inattivo.

Un sito attivo può:

* propagare la propria attività ai vicini;

* spegnersi spontaneamente.

Se la propagazione è troppo debole, l'attività si estingue. Se è abbastanza forte, può autosostenersi a livello collettivo.

Questo schema minimale ricorre in contesti molto diversi.

## 2.1 Epidemie locali

Un individuo infetto può contagiare i propri vicini di contatto, ma può anche guarire o essere rimosso. Se il contagio medio non è sufficiente a compensare la guarigione, l'epidemia locale si spegne.

## 2.2 Colonizzazione ecologica

Una specie può colonizzare siti vicini già occupati, ma le popolazioni locali possono anche estinguersi. Il problema centrale diventa allora: esiste una soglia di colonizzazione oltre la quale la specie riesce a persistere nel paesaggio?

## 2.3 Incendi e propagazione di attività

Un sito attivo può accendere siti vicini combustibili, ma il fuoco si spegne localmente dopo un certo tempo. Il sistema mostra una tensione tra propagazione spaziale e spegnimento.

## 2.4 Malware o diffusione di processi attivi su rete

Un nodo attivo può attivare nodi adiacenti, ma ogni nodo attivo può anche disattivarsi. Anche in questo caso esiste una soglia tra spegnimento veloce e attività persistente.

## 2.5 Significato metodologico

Il punto centrale è che il modello non richiede né una topologia complessa né una dinamica raffinata per mostrare un fenomeno collettivo molto ricco. Basta una regola locale elementare per produrre una vera soglia critica.

# 3. Definizione formale del modello

## 3.1 Spazio degli stati

Si consideri un grafo con $N$ nodi oppure un reticolo finito. Ogni sito $i$ ha una variabile di stato

$$
X_i(t) \in \{0,1\},
$$

dove:

* $X_i(t)=1$ indica che il sito è attivo, occupato o infetto;

* $X_i(t)=0$ indica che il sito è inattivo, vuoto o suscettibile.

Lo stato completo del sistema al tempo $t$ è quindi il vettore

$$
X(t) = (X_1(t),\dots,X_N(t)).
$$

## 3.2 Dinamica continua in tempo

La dinamica standard del contact process è una catena di Markov a tempo continuo con due tipi di transizioni elementari.

### Spegnimento o guarigione

Ogni sito attivo passa a 0 con tasso 1:

$$
1 \to 0 \quad \text{con tasso } 1.
$$

La scelta del tasso uguale a 1 non è restrittiva: serve solo a fissare la scala temporale.

### Attivazione o contagio

Ogni sito inattivo passa a 1 con tasso proporzionale al numero di vicini attivi:

$$
0 \to 1 \quad \text{con tasso } \lambda \times (\text{numero di vicini attivi}).
$$

Il parametro fondamentale del modello è quindi

$$
\lambda > 0,\
$$

che misura la forza della propagazione rispetto allo spegnimento.

## 3.3 Interpretazione del parametro $\lambda$

* se $\lambda$ è piccolo, ogni sito attivo tende a spegnersi prima di generare nuova attività;

* se $\lambda$ è grande, i siti attivi riescono a propagare l'attività prima di decadere.

Il comportamento collettivo cambia qualitativamente al variare di $\lambda$.

# 4. Stato assorbente e transizione critica

## 4.1 Stato assorbente

La configurazione completamente vuota,

$$
X_i = 0 \qquad \forall i,
$$

è uno **stato assorbente**. Una volta raggiunta, il sistema non può più uscirne, perché non esiste nessun sito attivo che possa riattivare gli altri.

Questa proprietà distingue il contact process da modelli come Ising o Deffuant, dove in generale il sistema continua ad evolvere anche nel lungo tempo.

## 4.2 Regime subcritico e supercritico

Per valori piccoli di $\lambda$, il sistema cade rapidamente nello stato assorbente.

Per valori sufficientemente grandi di $\lambda$, l'attività può sostenersi per tempi molto lunghi e, nel limite di sistemi molto grandi, persistere in modo macroscopico.

Tra questi due regimi esiste una soglia critica

$$
\lambda_c,\
$$

che dipende dalla topologia del sistema.

## 4.3 Il significato della soglia

La soglia critica separa due fasi qualitativamente diverse:

* **fase inattiva**: l'attività si spegne;

* **fase attiva**: la densità media di siti attivi resta positiva nel lungo tempo, almeno nel limite termodinamico.

Dal punto di vista didattico, questa è una delle situazioni più semplici in cui compare una vera transizione di fase non di equilibrio.

# 5. Collegamento con i processi di branching

Uno dei punti più belli del progetto è il legame con i **branching processes**.

## 5.1 Approssimazione a bassa densità

Se il sistema è molto poco attivo e i siti attivi sono lontani tra loro, le collisioni e le sovrapposizioni diventano rare. In questa fase iniziale, ogni sito attivo si comporta quasi come un individuo che:

* muore con un certo tasso;

* genera discendenti nei siti vicini con un altro tasso.

In questo senso il contact process, vicino all'origine, assomiglia a un branching process.

## 5.2 Perché l'approssimazione non è esatta

Quando la densità cresce, l'approssimazione si rompe per due ragioni:

* due propagazioni diverse possono tentare di attivare lo stesso sito;

* l'occupazione massima di un sito è 1, quindi non esiste crescita indipendente illimitata come in una ramificazione pura.

Questo punto è metodologicamente molto importante: il branching process descrive bene il regime diluito, ma non la dinamica collettiva piena.

## 5.3 Messaggio didattico

Il modello è quindi un eccellente esempio di come:

* una descrizione lineare o di ramificazione sia utile in prima approssimazione;

* ma la saturazione e la geometria locale generino una fenomenologia più ricca.

# 6. Ruolo della topologia

Il contact process è molto sensibile alla struttura del grafo o del reticolo su cui evolve.

## 6.1 Reticoli regolari

Su un reticolo regolare, la soglia critica riflette il fatto che ogni sito ha un numero limitato di vicini e che la propagazione locale deve vincere la tendenza al decadimento.

## 6.2 Alberi o grafi più ramificati

Su strutture più ramificate, la propagazione può essere facilitata, perché l'attività ha più direzioni in cui espandersi.

## 6.3 Reti casuali o eterogenee

Su reti con forte eterogeneità di grado, alcuni nodi possono agire come hub locali e sostenere l'attività più efficacemente.

Questo rende il modello molto utile anche come ponte verso i modelli epidemici su rete.

# 7. Osservabili da misurare

Per trasformare il modello in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 7.1 Densità media di siti attivi

$$
\rho(t)=\frac{1}{N}\sum_{i=1}^N X_i(t).
$$

Questa quantità misura quanta attività è presente nel sistema al tempo $t$.

## 7.2 Probabilità di sopravvivenza

Se si ripete la simulazione molte volte a partire da una stessa condizione iniziale, si può definire

$$
P_{\mathrm{surv}}(t)=\Pr(\text{il sistema non si è ancora estinto al tempo } t).
$$

## 7.3 Tempo medio di estinzione

Su sistemi finiti, il tempo fino al raggiungimento dello stato assorbente è sempre finito. Una osservabile molto utile è il tempo medio di estinzione.

## 7.4 Densità quasi-stazionaria

Per simulazioni che non si sono ancora estinte, si può misurare la densità media condizionata alla sopravvivenza. Questa quantità è particolarmente utile vicino alla soglia critica.

## 7.5 Cluster spaziali di attività

Su reticoli, si possono analizzare:

* dimensioni dei cluster attivi;

* estensione spaziale media;

* forma delle regioni attive nel tempo.

# 8. Domande scientifiche che il modello permette di studiare

1. Esiste una soglia critica $\lambda_c$?

2. Come cambia il tempo medio di estinzione al crescere della dimensione del sistema?

3. Quanto è accurata l'approssimazione branching nelle prime fasi della diffusione?

4. In che modo la topologia del grafo modifica la soglia di sopravvivenza?

5. Qual è la differenza tra densità media non condizionata e densità condizionata alla sopravvivenza?

6. Qual è la relazione tra contact process e modello SIS?

7. Come cambia la dinamica se si introduce disordine spaziale nei tassi?

# 9. Mean-field elementare

Per avere un primo confronto teorico, si può introdurre una chiusura media molto semplice.

Se $\rho(t)$ è la frazione media di siti attivi e ogni nodo ha grado medio $k$, allora una forma grezza del bilancio è

$$
\dot\rho = -\rho + \lambda k , \rho(1-\rho).\
$$

Il primo termine rappresenta il decadimento spontaneo, il secondo la propagazione verso siti vuoti.

Questa equazione suggerisce l'esistenza di una soglia mean-field

$$
\lambda_c^{\mathrm{MF}} = \frac{1}{k}.\
$$

Naturalmente questa non coincide in generale con la soglia vera del sistema spaziale, ma fornisce un benchmark molto utile.

# 10. Pseudocodice del modello

Per un corso computazionale conviene presentare due possibili implementazioni:

* una versione a tempo discreto semplificata, più facile da programmare;

* una versione event-driven più fedele alla dinamica continua.

## 10.1 Input

* numero di nodi o siti $N$

* struttura del reticolo o del grafo

* parametro di propagazione $\lambda$

* tempo massimo di simulazione $T$

* numero di realizzazioni indipendenti $R$

* condizione iniziale, per esempio un solo sito attivo oppure una frazione iniziale $\rho_0$

## 10.2 Pseudocodice: versione semplificata a tempo discreto

```text
Inizializza il grafo o il reticolo
Inizializza la configurazione X_i(0)

Per t = 0, ..., T-1:
    crea una copia temporanea della configurazione corrente

    Per ogni sito i:
        se X_i(t) = 1:
            con probabilità p_off spegni il sito nella nuova configurazione

        se X_i(t) = 0:
            conta il numero n_i di vicini attivi
            con probabilità proporzionale a lambda * n_i attiva il sito nella nuova configurazione

    sostituisci la configurazione corrente con quella nuova
    misura:
        - densità rho(t)
        - sopravvivenza
        - eventuali cluster spaziali
```

Questa versione è didatticamente utile, anche se non coincide esattamente con la dinamica continua standard.

## 10.3 Pseudocodice: versione event-driven più fedele

```text
Inizializza il grafo o il reticolo
Inizializza la configurazione X_i(0)
Poni t = 0

Finché t < T e il sistema non è estinto:
    calcola il numero totale di eventi di spegnimento possibili
    calcola il numero totale di eventi di attivazione possibili
    costruisci il tasso totale r_tot

    estrai un tempo di attesa tau ~ Exp(r_tot)
    poni t <- t + tau

    scegli il tipo di evento in proporzione ai rispettivi tassi:
        - spegnimento di un sito attivo
        - attivazione di un sito vuoto da parte di un vicino attivo

    aggiorna la configurazione
    registra eventuali osservabili
```

Questa seconda versione è più naturale se si vuole insistere sul fatto che il contact process è una CTMC su spazio discreto.

# 11. Schema del laboratorio

## 11.1 Laboratorio 1 -- Estinzione e sopravvivenza

### Obiettivo

Osservare la differenza qualitativa tra regime subcritico e supercritico.

### Attività

1. fissare la topologia del sistema, per esempio un reticolo quadrato oppure una linea;

2. scegliere diversi valori di $\lambda$;

3. inizializzare con un piccolo numero di siti attivi;

4. simulare molte realizzazioni indipendenti;

5. misurare probabilità di sopravvivenza e densità media nel tempo.

### Domande guida

* Per quali valori di $\lambda$ il sistema si spegne quasi sempre rapidamente?

* Per quali valori la sopravvivenza diventa apprezzabile?

* La transizione appare netta oppure graduale nei sistemi finiti?

## 11.2 Laboratorio 2 -- Effetto della dimensione del sistema

### Obiettivo

Studiare come il tempo di estinzione dipenda dalla taglia del sistema.

### Attività

1. fissare un valore di $\lambda$ vicino alla soglia;

2. simulare il processo su sistemi di dimensione crescente;

3. misurare il tempo medio di estinzione;

4. confrontare il comportamento subcritico, quasi critico e supercritico.

### Domande guida

* Il tempo medio di estinzione cresce con la taglia del sistema?

* Quanto cambia il comportamento vicino alla soglia?

* È plausibile parlare di persistenza macroscopica per sistemi molto grandi?

## 11.3 Laboratorio 3 -- Confronto con branching e mean-field

### Obiettivo

Capire in quali regimi le approssimazioni semplici funzionano e in quali falliscono.

### Attività

1. confrontare la fase iniziale della crescita con un branching process efficace;

2. confrontare la densità media con la previsione mean-field;

3. discutere il ruolo delle collisioni e della geometria.

### Domande guida

* Il branching descrive bene l'inizio della dinamica?

* Dove cominciano a comparire deviazioni significative?

* Il mean-field sovrastima oppure sottostima la sopravvivenza?

# 12. Estensioni possibili

Una volta implementato il modello base, si possono considerare diverse estensioni.

## 12.1 Disordine spaziale

Si possono introdurre tassi di attivazione diversi da sito a sito, per rappresentare eterogeneità ambientale o topologica.

## 12.2 Immunizzazione o siti inattivabili

Alcuni siti possono essere resi permanentemente inattivi oppure più difficili da attivare, introducendo una forma di barriera strutturale.

## 12.3 Reti diverse

È istruttivo confrontare il comportamento del modello su:

* linea;

* reticolo bidimensionale;

* albero regolare;

* rete casuale.

## 12.4 Collegamento con modelli epidemici più ricchi

Il contact process può essere confrontato con SIS o SIR su rete per capire quali aspetti siano già presenti nel modello minimo e quali richiedano stati aggiuntivi.

# 13. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce in forma molto semplice una **transizione verso uno stato assorbente**, che è una delle grandi classi di fenomeni nei sistemi stocastici fuori equilibrio.

Secondo, collega in modo naturale:

* topologia;

* propagazione locale;

* estinzione;

* persistenza.

Terzo, permette un confronto molto istruttivo tra:

* simulazione microscopica;

* branching process;

* chiusura mean-field.

Quarto, crea ponti diretti con altri progetti del corso:

* con **epidemie su reti**, perché il meccanismo di contagio locale è affine;

* con **geografia ecologica**, perché la colonizzazione locale e l'estinzione sono temi centrali;

* con **percolazione**, perché in entrambi i casi compare una soglia di connettività/attività;

* con **Gillespie**, perché il modello può essere simulato come CTMC event-driven.

## Osservazione finale

Il contact process è uno dei migliori esempi di come un modello microscopico quasi minimale possa già contenere una domanda scientifica profonda: quando un'attività locale riesce a diventare collettivamente sostenibile? Proprio questa chiarezza concettuale lo rende un case study eccellente per un corso di modelli stocastici.
