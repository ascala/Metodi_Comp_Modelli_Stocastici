---
title: "Project: Ising dinamico, Glauber e voter model"
subtitle: "ordine, consenso, rumore e dinamiche locali su reticoli e reti"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce una famiglia di modelli locali su reticoli e reti che, pur partendo da regole semplici e da variabili binarie, portano a fenomenologie collettive molto diverse.

Gli obiettivi sono sei:

1. formalizzare il **modello di Ising dinamico** con aggiornamento di Glauber come esempio di dinamica stocastica guidata da energia e rumore termico;

2. formalizzare il **voter model** come dinamica di imitazione locale senza funzione di energia;

3. confrontare ordine termodinamico e consenso per capire che non sono la stessa cosa;

4. introdurre osservabili quantitative come magnetizzazione, tempi di consenso, correlazioni e domini spaziali;

5. studiare il ruolo della temperatura, della topologia e della dimensione del sistema;

6. discutere in che modo modelli molto simili a livello microscopico possano avere interpretazioni fisiche o sociali molto diverse.

Dal punto di vista del corso, questo progetto è particolarmente importante perché mette fianco a fianco due grandi paradigmi.

Nel caso dell'Ising dinamico, la stocasticità è legata al rumore termico e alla probabilità di accettare configurazioni energeticamente sfavorevoli. Nel voter model, invece, la casualità entra nella scelta di chi copia chi, e la dinamica non è guidata da una funzione di energia. Questo confronto è estremamente istruttivo.

# 2. Motivazione generale

Una grande parte dei modelli di dinamica collettiva può essere ricondotta a una struttura molto semplice:

* ogni unità del sistema ha uno stato binario;

* ogni unità interagisce localmente con i vicini;

* l'aggiornamento è stocastico;

* l'esito macroscopico dipende dal bilancio tra allineamento e rumore.

Questa struttura compare in contesti diversi.

## 2.1 Magnetizzazione e fisica statistica

Nel linguaggio fisico, lo stato binario rappresenta uno spin che può essere orientato verso l'alto o verso il basso. L'interazione locale tende ad allineare spin vicini, mentre il rumore termico tende a disordinarli. Il problema centrale è capire quando emerge un ordine macroscopico spontaneo.

## 2.2 Opinioni binarie e consenso sociale

Nel linguaggio sociale, lo stato binario può rappresentare una scelta discreta, una convenzione, un'opinione o una posizione politica elementare. L'interazione locale tende allora a produrre imitazione, pressione sociale o influenza di prossimità.

## 2.3 Norme, convenzioni e imitazione

Il voter model è particolarmente naturale quando non esiste una forza sistematica verso un'opinione “migliore”, ma soltanto una dinamica di copia locale. In questo caso il problema centrale non è l'equilibrio termodinamico, ma la formazione di consenso o la persistenza di frontiere tra domini.

## 2.4 Messaggio metodologico

La lezione più importante è che non basta dire “gli agenti tendono ad allinearsi localmente”. Bisogna chiedersi:

* in base a quale regola si aggiornano?

* esiste una funzione di energia o no?

* il rumore è termico oppure puramente interazionale?

* il sistema converge a stati di equilibrio, a consenso, oppure resta intrappolato in metastabilità?

# 3. Struttura dello spazio degli stati

In entrambi i modelli considerati, a ogni sito o nodo $i$ viene associata una variabile binaria

$$\
\sigma\_i(t) \in {-1,+1}.\
$$

Lo stato completo del sistema al tempo $t$ è dunque il vettore

$$\
\sigma(t) = (\sigma\_1(t),\dots,\sigma\_N(t)).\
$$

Dal punto di vista formale, la differenza tra i due modelli non sta nello spazio degli stati, che è identico, ma nella regola di aggiornamento.

# 4. Modello 1: Ising dinamico con Glauber

## 4.1 Energia configurazionale

Nel modello di Ising si assume che la configurazione degli spin abbia una energia

$$\
H(\sigma) = -J \sum\_{\langle i,j \rangle} \sigma\_i \sigma\_j - h \sum\_i \sigma\_i,\
$$

dove:

* $J>0$ favorisce l'allineamento tra siti vicini;

* $h$ è un campo esterno che favorisce una delle due orientazioni;

* la somma $\langle i,j \rangle$ è estesa alle coppie di siti vicini.

Se due spin vicini sono uguali, contribuiscono con energia più bassa. Se sono opposti, contribuiscono con energia più alta. Per questo il modello tende a formare domini omogenei.

## 4.2 Dinamica di Glauber

L'Ising dinamico non si limita a definire un'energia, ma introduce anche una regola stocastica di evoluzione verso configurazioni più probabili a temperatura finita.

Una scelta standard è l'aggiornamento di Glauber:

1. si sceglie un sito $i$;

2. si considera il flip\
   $$\
   \sigma\_i \to -\sigma\_i;\
   $$

3. si calcola la variazione di energia $\Delta H$;

4. il flip viene accettato con probabilità dipendente da $\Delta H$ e dalla temperatura $T$.

Una forma classica è

$$\
P(\text{flip}) = \frac{1}{1+e^{\Delta H/T}}.\
$$

In alternativa si può usare la regola di Metropolis:

$$\
P(\text{flip}) = \min{1,e^{-\Delta H/T}}.\
$$

## 4.3 Ruolo della temperatura

La temperatura $T$ controlla l'intensità del rumore.

* per $T$ piccola, il sistema tende fortemente a ridurre l'energia e quindi a ordinarsi;

* per $T$ grande, anche flip energeticamente sfavorevoli vengono accettati con frequenza significativa, e l'ordine viene distrutto.

Questo genera la classica transizione ordine--disordine dell'Ising.

## 4.4 Significato fisico

Nel contesto fisico, la dinamica di Glauber rappresenta il modo in cui un sistema di spin si rilassa verso l'equilibrio termico. È quindi una dinamica coerente con una distribuzione di Boltzmann nel lungo tempo.

# 5. Modello 2: voter model

## 5.1 Regola di aggiornamento

Nel voter model non esiste una funzione di energia. La dinamica è puramente imitativa.

A ogni passo:

1. si sceglie un nodo $i$;

2. si sceglie casualmente uno dei suoi vicini $j$;

3. il nodo $i$ copia lo stato di $j$:

$$\
\sigma\_i \leftarrow \sigma\_j.\
$$

Questa regola è estremamente semplice, ma produce già una dinamica ricca di coarsening, consenso e dipendenza dalla topologia.

## 5.2 Interpretazione

Nel voter model non c'è un “costo energetico” delle interfacce tra stati opposti. Le frontiere tra domini si muovono per fluttuazione casuale. In questo senso il modello descrive molto bene:

* imitazione sociale pura;

* diffusione di convenzioni;

* opinioni binarie senza preferenza intrinseca per uno dei due stati.

## 5.3 Differenza concettuale rispetto all'Ising

Questa distinzione è fondamentale:

* nell'Ising dinamico, il rumore compete con una forza di allineamento energetico;

* nel voter model, la dinamica è guidata solo dalla copia locale casuale.

Di conseguenza, anche se visivamente i due sistemi possono sembrare simili, le loro proprietà di lungo tempo non coincidono.

# 6. Ordine, consenso e coarsening

Questo progetto è molto adatto a chiarire una distinzione concettuale importante.

## 6.1 Ordine nell'Ising

Nel modello di Ising, il problema centrale è l'emergere di una magnetizzazione macroscopica non nulla al di sotto di una temperatura critica.

L'oggetto da studiare è dunque una vera misura d'ordine termodinamico.

## 6.2 Consenso nel voter model

Nel voter model, il problema centrale è invece il raggiungimento di uno stato di consenso, cioè una configurazione in cui tutti i nodi sono +1 oppure tutti sono -1.

Qui il consenso non nasce da minimizzazione di una funzione di energia, ma da una dinamica di assorbimento guidata dalle fluttuazioni locali.

## 6.3 Coarsening

In entrambi i modelli possono comparire domini spaziali sempre più grandi nel tempo. Tuttavia:

* nell'Ising a bassa temperatura, i domini crescono perché il sistema tende a ridurre le interfacce energeticamente costose;

* nel voter model, le interfacce si muovono per rumore e coalescenza, non per riduzione esplicita di una energia.

# 7. Osservabili da misurare

Per trasformare il progetto in un vero case study computazionale conviene introdurre alcune osservabili standard.

## 7.1 Magnetizzazione media

$$\
m(t)=\frac{1}{N}\sum\_{i=1}^N \sigma\_i(t).\
$$

Questa è la misura d'ordine più naturale per l'Ising, ma è utile anche nel voter model per seguire la deriva verso uno dei due stati assorbenti.

## 7.2 Valore assoluto della magnetizzazione

$$\
|m(t)|\
$$

è spesso più informativo, perché evita cancellazioni tra realizzazioni che convergono a stati di segno opposto.

## 7.3 Correlazione spaziale

Si può misurare una funzione di correlazione del tipo

$$\
C(r)=\langle \sigma\_i \sigma\_{i+r} \rangle,\
$$

oppure la probabilità che due siti a distanza $r$ abbiano lo stesso stato.

## 7.4 Numero di domini o interfacce

Su una linea o su un reticolo, si può contare il numero di coppie vicine con stato opposto. Questa quantità misura quanto il sistema sia frammentato.

## 7.5 Tempo di consenso

Nel voter model, e anche in Ising su sistemi finiti, si può misurare il tempo necessario a raggiungere una configurazione uniforme.

## 7.6 Suscettività empirica

Per l'Ising si può introdurre una misura delle fluttuazioni della magnetizzazione, utile per individuare il regime critico.

# 8. Domande scientifiche che il progetto permette di studiare

1. In che senso l'Ising presenta una transizione ordine--disordine?

2. Qual è il ruolo della temperatura nel mantenere oppure distruggere i domini ordinati?

3. Come varia il tempo di consenso nel voter model al cambiare della topologia?

4. In che modo il coarsening dei domini differisce tra Ising e voter?

5. Perché il voter model è più naturale per opinioni binarie e il modello di Ising per sistemi con rumore termico?

6. Quale relazione esiste tra questi modelli e quelli di dinamica dell'opinione, come Deffuant?

7. In che rapporto sta il voter con majority rule o con la replicator equation discreta?

# 9. Pseudocodice dei due modelli

## 9.1 Input

* numero di siti o nodi $N$

* struttura del reticolo o del grafo

* numero massimo di passi temporali $T$

* numero di realizzazioni indipendenti $R$

* temperatura $T\_{\mathrm{phys}}$ nel caso Ising

* eventuale campo esterno $h$

* configurazione iniziale degli spin

## 9.2 Pseudocodice: Ising con Glauber

```text
Inizializza il reticolo o il grafo
Assegna a ogni sito uno spin sigma_i in {-1,+1}

Per t = 0, ..., T-1:
    scegli un sito i a caso
    calcola la variazione di energia DeltaH associata al flip sigma_i -> -sigma_i
    calcola la probabilità di accettazione P_flip
    estrai u ~ U(0,1)
    se u < P_flip:
        poni sigma_i <- -sigma_i

    misura eventualmente:
        - magnetizzazione m(t)
        - numero di interfacce
        - correlazioni spaziali
```

## 9.3 Pseudocodice: voter model

```text
Inizializza il reticolo o il grafo
Assegna a ogni sito uno stato sigma_i in {-1,+1}

Per t = 0, ..., T-1:
    scegli un nodo i a caso
    scegli un vicino j di i a caso
    poni sigma_i <- sigma_j

    misura eventualmente:
        - magnetizzazione m(t)
        - numero di interfacce
        - tempo al consenso
        - configurazione spaziale
```

## 9.4 Osservazione implementativa

Anche qui conviene chiarire bene se si usi:

* aggiornamento asincrono, più naturale per entrambi i modelli;

* aggiornamento sincrono, che può modificare sensibilmente la dinamica.

# 10. Schema del laboratorio

## 10.1 Laboratorio 1 -- Ising: ordine e temperatura

### Obiettivo

Studiare come il comportamento del sistema cambi al variare della temperatura.

### Attività

1. fissare una topologia, per esempio un reticolo quadrato;

2. scegliere diversi valori di temperatura;

3. simulare il modello di Ising con Glauber;

4. misurare magnetizzazione media, valore assoluto della magnetizzazione e numero di interfacce;

5. confrontare il regime ordinato con quello disordinato.

### Domande guida

* A basse temperature il sistema tende a uno stato ordinato?

* Le fluttuazioni crescono in una regione intermedia di temperatura?

* Come cambia il tempo di rilassamento vicino alla transizione?

## 10.2 Laboratorio 2 -- Voter: consenso e topologia

### Obiettivo

Studiare il tempo di consenso e il coarsening nel voter model.

### Attività

1. simulare il voter model su linea, reticolo o piccola rete casuale;

2. partire da una configurazione iniziale casuale;

3. misurare il tempo di consenso su molte realizzazioni;

4. osservare la dinamica dei domini nel tempo.

### Domande guida

* Quanto cresce il tempo di consenso con la taglia del sistema?

* La topologia accelera o rallenta il consenso?

* I domini si fondono gradualmente oppure il processo è dominato da grandi fluttuazioni?

## 10.3 Laboratorio 3 -- Confronto diretto tra Ising e voter

### Obiettivo

Mettere in evidenza che regole microscopicamente simili possono produrre dinamiche di natura diversa.

### Attività

1. scegliere la stessa topologia e condizioni iniziali per i due modelli;

2. simulare Ising e voter separatamente;

3. confrontare:

   * magnetizzazione;

   * tempi di consenso;

   * numero di domini;

   * configurazioni spaziali.

### Domande guida

* In quale senso il voter raggiunge consenso senza temperatura?

* In quale senso l'Ising produce ordine per riduzione energetica?

* I due modelli hanno la stessa nozione di stato stazionario?

# 11. Estensioni possibili

Una volta implementati i modelli base, si possono considerare diverse estensioni.

## 11.1 Campo esterno e disordine

Nel caso Ising si possono introdurre campi locali disordinati oppure campi globali deboli, per studiare la robustezza dell'ordine.

## 11.2 Reti complesse

Sia Ising sia voter possono essere simulati su reti non regolari, permettendo di studiare l'effetto dell'eterogeneità topologica.

## 11.3 Majority rule

Si può aggiungere una terza dinamica, in cui ogni nodo adotta la maggioranza del proprio vicinato. Questo rende il confronto ancora più istruttivo.

## 11.4 Legami con i modelli di opinione continui

Il voter model può essere confrontato con Deffuant per mostrare la differenza tra:

* stati discreti e opinioni continue;

* copia pura e compromesso parziale.

# 12. Perché questo è un buon case study per il corso

Questa dispensa è molto adatta a un corso di metodi computazionali per almeno quattro ragioni.

Primo, introduce un classico assoluto della fisica statistica, il modello di Ising, ma in una forma dinamica computazionalmente accessibile.

Secondo, mette a confronto diretto due nozioni diverse di dinamica locale:

* aggiornamento termico guidato da energia;

* imitazione stocastica senza energia.

Terzo, permette di insegnare concetti centrali come:

* misura d'ordine;

* consenso;

* domini spaziali;

* metastabilità;

* tempi di rilassamento.

Quarto, crea ponti molto naturali con altri progetti del corso:

* con **Deffuant**, perché entrambi trattano dinamiche di opinione;

* con **replicator dynamics**, perché tutti studiano la diffusione di stati nella popolazione;

* con **percolazione**, perché la struttura dei cluster e delle interfacce diventa importante;

* con **trasporto fuori equilibrio** e altri modelli spaziali, perché il coarsening su reticolo è un tema comune.

## Osservazione finale

Questo progetto è uno dei luoghi migliori in cui mostrare che una somiglianza superficiale tra regole microscopiche non implica equivalenza macroscopica. Ising e voter sono vicini nello spazio delle idee, ma insegnano lezioni diverse: l'uno sull'ordine termico e la competizione con il rumore, l'altro sul consenso e sulla dinamica di imitazione locale. Proprio questo confronto li rende un caso di studio particolarmente formativo.
