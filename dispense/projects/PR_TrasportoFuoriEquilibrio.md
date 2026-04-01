---
title: "Project: TASEP/ASEP e trasporto fuori equilibrio"
subtitle: "processi di esclusione, corrente stazionaria e transizioni indotte dai bordi"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce il **Totally Asymmetric Simple Exclusion Process** (TASEP), e opzionalmente la sua estensione **Asymmetric Simple Exclusion Process** (ASEP), come caso di studio per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare il trasporto stocastico su reticolo come processo di particelle interagenti;

2. mostrare come una semplice regola di esclusione locale generi fenomeni collettivi non banali;

3. introdurre il concetto di corrente stazionaria in un sistema fuori equilibrio;

4. distinguere tra condizioni periodiche e condizioni aperte ai bordi;

5. studiare l'effetto dei parametri di iniezione ed estrazione sulle fasi macroscopiche del sistema;

6. collegare il modello a fenomeni applicativi come traffico, trasporto intracellulare, code in pipeline e moto vincolato in spazi stretti.

Dal punto di vista del corso, questo progetto è particolarmente importante perché introduce uno dei più classici **interacting particle systems** della fisica statistica fuori equilibrio. Il modello è microscopicamente molto semplice, ma già sufficiente a produrre correnti, shock, colli di bottiglia e transizioni indotte dai bordi.

# 2. Motivazione: che cosa significa trasporto fuori equilibrio

Nei sistemi in equilibrio, i flussi macroscopici medi si annullano: non esiste una corrente netta persistente di materia, energia o informazione. Nei sistemi fuori equilibrio, invece, esistono spesso flussi stazionari mantenuti da:

* differenze di densità;

* differenze di potenziale;

* sorgenti e pozzi ai bordi;

* forzanti esterne direzionali.

Il TASEP è uno dei modelli più elementari in cui questa idea diventa completamente esplicita. Le particelle hanno una direzione preferenziale di moto, e l'interazione fondamentale non è attrattiva o repulsiva nel senso usuale, ma puramente **cinetica**: una particella può avanzare solo se il sito successivo è vuoto.

È proprio questa regola di esclusione a generare il fenomeno collettivo. Se le particelle fossero indipendenti, il problema sarebbe banale. Invece, il fatto che si ostacolino reciprocamente produce congestione, dipendenza spaziale e una relazione non lineare tra densità e corrente.

# 3. Campi di applicazione

Il modello è astratto, ma descrive in modo sorprendentemente efficace una famiglia molto ampia di situazioni.

## 3.1 Traffico veicolare su corsia singola

Se si pensa a un insieme di veicoli che avanzano su una corsia stretta senza possibilità di sorpasso, la regola di esclusione è naturale: un veicolo può avanzare solo se lo spazio davanti è libero. Il TASEP è molto più spartano del modello di Nagel--Schreckenberg, ma cattura già il cuore del problema: il flusso non cresce indefinitamente con la densità, perché a densità alte i veicoli si bloccano a vicenda.

## 3.2 Traduzione dell'mRNA e trasporto intracellulare

Uno degli usi più importanti del TASEP in biologia riguarda il moto di ribosomi lungo un filamento di mRNA. I ribosomi avanzano in una direzione prefissata, non possono sovrapporsi, e il tasso di ingresso/uscita ai bordi è spesso l'elemento chiave che controlla il throughput del sistema. Lo stesso formalismo compare anche nel trasporto di motori molecolari lungo microtubuli.

## 3.3 Pipeline e sistemi di produzione discreti

In molte pipeline computazionali o industriali, unità di lavoro avanzano lungo stazioni in serie con capacità limitata. Una stazione occupata blocca l'avanzamento della successiva unità. In questo senso il TASEP può essere letto come un modello minimale di flow-shop o pipeline con buffer unitari.

## 3.4 Pedoni o agenti in corridoi stretti

Quando il moto è fortemente canalizzato e il sorpasso è difficile o impossibile, l'esclusione diventa il vincolo dominante. Anche qui il modello non pretende di essere realistico in dettaglio, ma aiuta a capire come possa emergere il jamming da regole puramente locali.

## 3.5 Trasporto di pacchetti o job lungo strutture lineari

Se si immagina una catena di nodi che si passano job, pacchetti o task, con capacità finita per nodo, il TASEP fornisce una rappresentazione minimale della propagazione di congestione lungo la linea.

# 4. Il modello TASEP

## 4.1 Struttura del reticolo

Consideriamo un reticolo unidimensionale di $L$ siti. Ogni sito può essere vuoto oppure occupato da una sola particella.

Introduciamo per ogni sito $i$ la variabile di occupazione

$$
\eta_i(t) \in {0,1},
$$

dove:

* $\eta_i(t)=1$ significa che il sito $i$ è occupato;

* $\eta_i(t)=0$ significa che il sito $i$ è vuoto.

Lo stato completo del sistema al tempo $t$ è quindi il vettore

$$
\eta(t) = (\eta_1(t),\dots,\eta_L(t)).
$$

## 4.2 Regola di esclusione

L'interazione fondamentale del modello è la seguente: due particelle non possono occupare lo stesso sito.

Questo implica che un salto da $i$ a $i+1$ è ammesso solo se:

$$
\eta_i = 1, \qquad \eta_{i+1}=0.\
$$

La dinamica dipende quindi non solo dalla posizione della particella, ma anche dallo stato locale del sito successivo.

## 4.3 Versione totalmente asimmetrica

Nel TASEP, il moto è completamente orientato. Le particelle possono saltare solo verso destra.

### Versione continua in tempo

Ogni particella nel sito $i$ tenta di saltare in $i+1$ con tasso 1, purché il sito di arrivo sia libero.

### Versione discreta in tempo

A ogni passo temporale si può:

* selezionare casualmente una particella oppure un sito;

* tentare l'avanzamento di una particella verso destra;

* eseguire il salto soltanto se il sito successivo è vuoto.

Dal punto di vista del corso, entrambe le versioni sono utili. La versione continua è concettualmente più naturale come catena di Markov a tempo continuo. La versione discreta è più facile da implementare e visualizzare in laboratorio.

# 5. La variante ASEP

Nel modello ASEP le particelle possono saltare sia verso destra sia verso sinistra, ma con tassi diversi.

Per esempio:

* salto verso destra con tasso $p$;

* salto verso sinistra con tasso $q$;

* con $p>q$ si ha una direzione preferenziale netta.

Il TASEP è il caso limite

$$
q=0.\
$$

L'ASEP è utile perché mostra come il trasporto diretto e la diffusione possano convivere nello stesso formalismo. Tuttavia, per una prima implementazione didattica, conviene quasi sempre partire dal TASEP.

# 6. Condizioni al contorno

Le condizioni al contorno cambiano profondamente il comportamento macroscopico del sistema.

## 6.1 Condizioni periodiche

Con condizioni periodiche, il sito $L$ è seguito dal sito $1$. Il sistema è topologicamente un anello.

Questa scelta è molto utile per studiare:

* il comportamento nel bulk;

* la relazione tra densità globale e corrente;

* la dinamica senza effetti di bordo.

In questo caso il numero totale di particelle è conservato.

## 6.2 Condizioni aperte

Con condizioni aperte si introducono due processi ai bordi:

* **iniezione** nel primo sito con tasso o probabilità $\alpha$, se il sito 1 è vuoto;

* **estrazione** dall'ultimo sito con tasso o probabilità $\beta$, se il sito $L$ è occupato.

Questa versione è molto più ricca, perché il sistema viene mantenuto fuori equilibrio dai bordi. Il flusso stazionario non dipende più soltanto dalla densità media iniziale, ma dal bilancio tra:

* immissione di particelle;

* trasporto nel bulk;

* rimozione all'uscita.

# 7. Corrente e relazione densità--flusso

Una delle quantità più importanti del progetto è la **corrente** di particelle.

In forma locale, la corrente media tra $i$ e $i+1$ può essere scritta come

$$
J_i = \langle \eta_i(1-\eta_{i+1}) \rangle.\
$$

Questa formula dice semplicemente che una particella contribuisce alla corrente se:

* il sito di partenza è occupato;

* il sito di arrivo è vuoto.

Nel caso periodico omogeneo, in regime stazionario, la corrente non dipende da $i$ e si può indicare con $J$.

In un'approssimazione mean-field elementare si scrive

$$
J \approx \rho(1-\rho),
$$

dove $\rho$ è la densità media.

Questa relazione è molto istruttiva, perché mostra subito che:

* a bassa densità ci sono poche particelle, quindi la corrente è piccola;

* ad alta densità ci sono pochi vuoti, quindi la corrente è ancora piccola;

* la corrente massima si ottiene a densità intermedia.

Questa struttura non lineare è uno dei messaggi più importanti del modello.

# 8. Fenomenologia con bordi aperti

La versione a bordi aperti è famosa perché mostra come condizioni ai bordi possano controllare l'intera fase macroscopica del sistema.

In termini qualitativi, si osservano tipicamente tre regimi:

## 8.1 Fase a bassa densità

Se l'iniezione è il fattore limitante, il sistema resta globalmente scarico. La corrente è controllata soprattutto da $\alpha$.

## 8.2 Fase ad alta densità

Se l'estrazione è il collo di bottiglia, le particelle si accumulano e il sistema resta carico. La corrente è controllata soprattutto da $\beta$.

## 8.3 Fase di massima corrente

Se né iniezione né estrazione sono troppo limitanti, il bulk del sistema si autoregola verso la configurazione che massimizza la corrente. Questa è forse la caratteristica più sorprendente del modello.

Dal punto di vista didattico, questo mostra in modo molto chiaro che un sistema fuori equilibrio può essere controllato dai bordi in modo non banale.

# 9. Osservabili da misurare

Per trasformare il modello in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 9.1 Densità media

$$
\rho(t)=\frac{1}{L}\sum_{i=1}^L \eta_i(t).
$$

Nel caso periodico, può essere costante se il numero di particelle è conservato. Nel caso aperto, evolve fino a un regime stazionario.

## 9.2 Corrente media

Una misura pratica della corrente consiste nel contare quanti salti vengono eseguiti per unità di tempo e normalizzare opportunamente.

## 9.3 Profilo spaziale di densità

Con bordi aperti si può misurare

$$
\rho_i = \langle \eta_i \rangle,
$$

cioè la probabilità media che il sito $i$ sia occupato. Questo permette di osservare gradienti, accumuli e zone di shock.

## 9.4 Fluttuazioni della corrente

Si può misurare la variabilità temporale del flusso per capire quanto il sistema sia regolare oppure intermittente.

## 9.5 Tempo di rilassamento

Quanto tempo impiega il sistema a raggiungere il regime stazionario a partire da una configurazione iniziale assegnata?

# 10. Domande scientifiche che il modello permette di studiare

1. Come dipende la corrente dalla densità nel caso periodico?

2. Quale densità massimizza il flusso?

3. Come cambiano densità e corrente al variare di $\alpha$ e $\beta$?

4. In che senso i bordi controllano il bulk?

5. Qual è la differenza tra un collo di bottiglia interno e un collo di bottiglia imposto ai bordi?

6. Quanto è buona l'approssimazione mean-field $J\approx\rho(1-\rho)$?

7. Come si collega il TASEP a modelli più realistici di traffico o trasporto biologico?

# 11. Pseudocodice del modello

Di seguito una versione semplice del TASEP a tempo discreto, prima con condizioni periodiche e poi con bordi aperti.

## 11.1 Input

* numero di siti $L$

* numero iniziale di particelle $N$ oppure densità iniziale $\rho_0$

* numero di passi temporali $T$

* parametri di bordo $\alpha$ e $\beta$ nella versione aperta

* numero di realizzazioni indipendenti $R$

## 11.2 Pseudocodice: caso periodico

```text
Inizializza un reticolo di L siti
Inserisci N particelle in siti scelti senza sovrapposizione

Per t = 0, ..., T-1:
    scegli un sito i oppure una particella in modo casuale
    se il sito i è occupato:
        definisci j = i+1 modulo L
        se il sito j è vuoto:
            sposta la particella da i a j
            incrementa il conteggio dei salti

    misura eventualmente:
        - densità media
        - corrente cumulata
        - configurazione istantanea
```

## 11.3 Pseudocodice: caso aperto

```text
Inizializza un reticolo di L siti

Per t = 0, ..., T-1:
    se il sito 1 è vuoto:
        con probabilità alpha inserisci una particella nel sito 1

    scegli un sito interno i oppure scandisci i siti in ordine casuale
    se il sito i è occupato e il sito i+1 è vuoto:
        sposta la particella da i a i+1
        incrementa il conteggio dei salti

    se il sito L è occupato:
        con probabilità beta rimuovi la particella dal sito L

    misura eventualmente:
        - densità totale
        - profilo spaziale medio
        - corrente
```

## 11.4 Osservazione implementativa

Per evitare artefatti, conviene chiarire molto bene agli studenti quale schema di aggiornamento si stia usando:

* sequenziale casuale;

* scansione ordinata;

* aggiornamento parallelo.

Queste scelte non sono equivalenti e possono modificare il comportamento osservato.

# 12. Schema del laboratorio

## 12.1 Laboratorio 1 -- Corrente e densità con condizioni periodiche

### Obiettivo

Studiare la relazione tra densità globale e corrente in un sistema chiuso.

### Attività

1. fissare $L$;

2. scegliere diversi valori della densità iniziale $\rho$;

3. simulare il TASEP con condizioni periodiche;

4. stimare la corrente media per ciascun valore di $\rho$;

5. rappresentare il diagramma empirico $J(\rho)$.

### Domande guida

* La curva è simmetrica attorno a $\rho=1/2$?

* Dove si osserva il massimo della corrente?

* Quanto bene la simulazione segue il risultato mean-field?

## 12.2 Laboratorio 2 -- Sistema aperto e fasi indotte dai bordi

### Obiettivo

Studiare l'effetto di $\alpha$ e $\beta$ su densità e corrente stazionaria.

### Attività

1. fissare $L$;

2. scegliere una griglia di valori $(\alpha,\beta)$;

3. simulare il sistema aperto fino al regime stazionario;

4. misurare corrente media e profilo spaziale di densità;

5. confrontare configurazioni iniettate lentamente, estratte lentamente e in regime di alta corrente.

### Domande guida

* Quando il sistema è scarico e quando è congestionato?

* In quali casi il collo di bottiglia è all'ingresso oppure all'uscita?

* Il bulk sembra riflettere soprattutto $\alpha$, soprattutto $\beta$, oppure nessuno dei due?

## 12.3 Laboratorio 3 -- Difetti locali e colli di bottiglia

### Obiettivo

Studiare l'effetto di un sito lento o di una regione difettosa sul flusso globale.

### Attività

1. introdurre un sito o un arco con probabilità di salto ridotta;

2. ripetere le simulazioni del caso periodico o aperto;

3. confrontare la corrente con quella del sistema omogeneo;

4. osservare eventuali accumuli a monte del difetto.

### Domande guida

* Quanto un singolo difetto modifica la corrente globale?

* Si forma una coda stabile a monte del difetto?

* Il difetto si comporta come un collo di bottiglia macroscopico?

# 13. Estensioni possibili

Una volta implementato il TASEP base, si possono considerare diverse estensioni.

## 13.1 ASEP

Introdurre una piccola probabilità di salto all'indietro, per vedere come il trasporto direzionale si deforma in presenza di diffusione controcorrente.

## 13.2 Particelle estese

In alcune applicazioni biologiche, una particella occupa più di un sito. Questo rende il problema molto più realistico, ma anche più complesso.

## 13.3 Velocità eterogenee o disordine spaziale

Si possono introdurre siti lenti, regioni lente o particelle con tassi di salto diversi.

## 13.4 Confronto con modelli di traffico più ricchi

È istruttivo confrontare il TASEP con Nagel--Schreckenberg per capire quali fenomeni dipendano già dalla sola esclusione e quali richiedano una dinamica di velocità esplicita.

# 14. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce un modello canonico e molto pulito di **particelle interagenti**.

Secondo, mette al centro una nozione molto importante ma spesso poco presente nei corsi introduttivi: il **fuori equilibrio stazionario**.

Terzo, permette di passare facilmente da simulazioni semplici a domande più profonde su correnti, shock, profili stazionari e controllo ai bordi.

Quarto, crea un ponte naturale con altri progetti del corso:

* con **jamming**, perché entrambi trattano congestione e flusso;

* con **queueing**, perché il collo di bottiglia e la saturazione giocano un ruolo centrale;

* con **geografia ecologica**, perché anche lì il paesaggio controlla il trasporto e la connettività;

* con **processi di Markov su grafi**, perché il moto resta un processo stocastico su uno spazio discreto.

## Osservazione finale

Il TASEP è uno di quei modelli in cui si vede molto chiaramente una lezione generale dei sistemi complessi: una dinamica microscopica quasi banale può produrre una fenomenologia macroscopica ricca, strutturata e fortemente non lineare. Proprio per questo è uno dei migliori laboratori concettuali per introdurre il trasporto fuori equilibrio.
