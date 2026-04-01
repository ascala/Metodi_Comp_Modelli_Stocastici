# Guida ai progetti -- per studenti e per docenti

## Perché organizzare i progetti in filoni tematici

Suddividere i progetti in aree, tematiche o filoni aiuta gli studenti a scegliere in modo più consapevole e permette ai docenti di riutilizzare gli stessi materiali in corsi diversi, con obiettivi differenti. Tuttavia, i filoni non devono essere intesi come categorie rigide: molti progetti appartengono naturalmente a più di un'area. Per questo motivo conviene usare una struttura a due livelli:

* un **filone principale**, che identifica il nucleo concettuale del progetto;
* alcuni **tag trasversali**, che descrivono strumenti, livello e tipo di lavoro richiesto.

I tag trasversali più utili sono:

* **struttura matematica principale**: DTMC, CTMC, SDE, Monte Carlo, ottimizzazione stocastica, modello su rete, mean-field, inferenza;
* **livello consigliato**: base, intermedio, avanzato;
* **profilo di lavoro**: teorico, computazionale, misto, applicativo;
* **output naturale**: simulazioni, analisi parametrica, confronto di modelli, risultati teorici, visualizzazioni.

---

# Guida per gli studenti

## 1. Come scegliere il progetto

La scelta del progetto non dovrebbe dipendere soltanto dal titolo o dal tema applicativo. Conviene guardare almeno quattro aspetti:

1. **il fenomeno studiato**;
2. **gli strumenti matematici e computazionali richiesti**;
3. **il tipo di lavoro prevalente**;
4. **il tipo di risultato finale atteso**.

Due progetti apparentemente lontani, ad esempio uno sulle epidemie e uno sul traffico, possono essere molto simili dal punto di vista del formalismo stocastico. Viceversa, due progetti sullo stesso tema possono richiedere competenze molto diverse.

## 2. Tre criteri pratici di scelta

### Interesse per il fenomeno

La prima domanda da porsi è: *quale linguaggio applicativo mi interessa di più?*

Alcuni progetti parlano il linguaggio della fisica statistica, altri delle reti, altri ancora dell'economia, dell'ecologia, dell'apprendimento o della scelta collettiva. L'interesse conta perché un buon progetto richiede non soltanto di programmare, ma anche di leggere, interpretare e discutere criticamente.

### Tipo di matematica che si preferisce

La seconda domanda è: *che tipo di lavoro matematico mi trovo meglio a fare?*

Si può preferire:

* simulare e visualizzare;
* derivare formule o soglie;
* lavorare con grafi e strutture spaziali;
* ragionare su processi di Markov e tempi di attesa;
* confrontare algoritmi e procedure di ottimizzazione.

### Tipo di elaborato che si vuole produrre

La terza domanda è: *che genere di progetto finale voglio realizzare?*

Alcuni progetti si prestano naturalmente a:

* un laboratorio computazionale ben strutturato;
* una piccola analisi teorica;
* un confronto tra scenari o parametri;
* uno studio critico di approssimazioni e limiti;
* una combinazione equilibrata di teoria e simulazione.

## 3. Domande utili prima di decidere

Prima di scegliere un progetto, conviene chiedersi:

* quanta programmazione richiede;
* se richiede conoscenze di probabilità, processi di Markov, grafi, equazioni differenziali o ottimizzazione;
* se la parte centrale è più analitica o più numerica;
* se il problema è ben delimitato o molto aperto;
* se l'obiettivo principale è capire un fenomeno oppure confrontare metodi e algoritmi.

## 4. Profili tipici di scelta

### Studente che vuole un ingresso graduale

Sono indicati progetti con struttura semplice, risultati leggibili e curva di ingresso relativamente dolce. Esempi tipici:

* voting;
* queueing;
* PageRank;
* network externalities;
* modello di March.

Questi progetti permettono in genere di ottenere risultati interessanti senza richiedere subito strumenti troppo avanzati.

### Studente orientato alla simulazione e alla visualizzazione

Sono particolarmente adatti:

* Deffuant;
* Vicsek o modelli di herding;
* jamming e traffico;
* percolazione;
* geografia ecologica;
* epidemie su reti.

In questi casi è naturale lavorare con diagrammi di fase, mappe di densità, misure aggregate e confronti parametrici.

### Studente interessato ai processi di Markov e alla dinamica a eventi

Sono consigliati:

* reaction networks con Gillespie;
* teoria delle code;
* Hawkes;
* contact process;
* TASEP/ASEP;
* epidemie su reti.

Sono progetti adatti a chi vuole capire bene la struttura probabilistica del modello: stati, transizioni, intensità, tempi di attesa, simulazione event-driven.

### Studente interessato a ottimizzazione e apprendimento

Sono indicati:

* bandit;
* simulated annealing;
* algoritmi genetici;
* reti neurali e SGD;
* foraging ottimale.

Questi progetti mettono al centro il rapporto tra esplorazione, sfruttamento, convergenza e costo computazionale.

### Studente con interesse teorico più marcato

Sono particolarmente adatti:

* replicator dynamics;
* dinamica delle imprese / Fokker--Planck;
* copule e affidabilità;
* percolazione;
* Ising dinamico / voter;
* contact process.

Qui è più naturale concentrarsi su soglie, stabilità, distribuzioni stazionarie, leggi limite o confronti tra modelli.

## 5. Criterio finale di scelta

In pratica, un buon progetto è quello che si trova nell'intersezione tra tre condizioni:

* **mi interessa davvero**;
* **posso iniziarlo con le competenze che possiedo ora**;
* **mi permette di imparare qualcosa di nuovo e rilevante**.

Se manca una di queste tre componenti, la scelta tende a funzionare meno bene.

## 6. Come leggere una scheda progetto

Quando si guarda una scheda, conviene identificare subito:

1. qual è l'oggetto stocastico principale;
2. quali osservabili si vogliono misurare;
3. che cosa si può simulare;
4. che cosa si può derivare o discutere teoricamente;
5. quali estensioni sono opzionali.

Le schede migliori sono quelle in cui i primi risultati si ottengono presto, ma esistono anche estensioni per chi vuole approfondire.

---

# Guida per i docenti

## 1. Come usare i progetti in corsi diversi

Gli stessi progetti possono essere usati in modi differenti a seconda del corso. Per farlo bene, conviene esplicitare per ogni insegnamento:

* quale parte del progetto è **centrale**;
* quale parte è **accessoria**;
* quale grado di rigore teorico è richiesto;
* che cosa si considera un buon elaborato finale.

Il valore dei progetti sta proprio nel fatto che possono essere riallineati a obiettivi didattici diversi senza essere riscritti da zero.

## 2. Uso in un corso introduttivo di modelli stocastici o laboratorio computazionale

### Obiettivo

Familiarizzare gli studenti con modellizzazione, simulazione, osservabili, interpretazione dei risultati e confronto tra scenari.

### Progetti particolarmente adatti

* voting;
* queueing;
* PageRank;
* Deffuant;
* percolazione;
* epidemie su reti;
* jamming;
* modello di March.

### Modalità d'uso consigliata

In questo tipo di corso conviene ridurre il formalismo al minimo indispensabile ed enfatizzare:

* implementazione corretta del modello;
* scelta delle osservabili;
* confronto tra parametri;
* qualità delle visualizzazioni;
* interpretazione dei risultati.

### Rischi da evitare

Non conviene sovraccaricare questi progetti con troppa teoria asintotica o con richieste analitiche che non siano funzionali agli obiettivi del corso.

## 3. Uso in un corso di processi di Markov o stochastic processes

### Obiettivo

Mettere in evidenza la struttura probabilistica dei modelli e collegare teoria e simulazione.

### Progetti particolarmente adatti

* queueing;
* reaction networks / Gillespie;
* Hawkes;
* PageRank;
* contact process;
* TASEP/ASEP;
* bandit;
* epidemie su reti.

### Modalità d'uso consigliata

Qui è naturale chiedere agli studenti di esplicitare:

* spazio degli stati;
* regole di transizione;
* intensità o probabilità di salto;
* osservabili principali;
* eventuali distribuzioni stazionarie o approssimazioni mean-field.

Questo è anche il contesto ideale per mostrare che problemi applicativi molto diversi condividono la stessa grammatica probabilistica.

## 4. Uso in un corso di fisica statistica o sistemi complessi

### Obiettivo

Studiare emergenza, transizioni di fase, ordine collettivo, metastabilità e dipendenza dalla scala.

### Progetti particolarmente adatti

* Ising dinamico / voter;
* percolazione;
* Vicsek;
* jamming;
* contact process;
* TASEP/ASEP;
* Deffuant.

### Modalità d'uso consigliata

In questo caso è utile chiedere:

* diagrammi di fase;
* analisi qualitativa del comportamento al variare dei parametri;
* effetti di taglia finita;
* tempi di rilassamento;
* confronto tra descrizione microscopica e fenomenologia macroscopica.

## 5. Uso in un corso di network science

### Obiettivo

Far vedere come la topologia della rete influenzi propagazione, robustezza, centralità e dinamiche collettive.

### Progetti particolarmente adatti

* epidemie su reti;
* PageRank;
* percolazione;
* Deffuant su rete;
* contact process;
* geografia ecologica interpretata come rete di patch;
* network externalities.

### Modalità d'uso consigliata

Conviene variare sistematicamente la topologia e confrontare, per esempio:

* reticoli;
* Erdős--Rényi;
* scale-free;
* small-world.

In questo modo gli studenti imparano a distinguere effetti dovuti alla topologia da effetti dovuti alla dinamica locale.

## 6. Uso in un corso di economia, scienze sociali computazionali o decisione collettiva

### Obiettivo

Mostrare come strumenti stocastici e dinamici possano modellare coordinamento, apprendimento, competizione, adozione e comportamento collettivo.

### Progetti particolarmente adatti

* voting;
* network externalities;
* economic competition;
* replicator dynamics;
* modello di March;
* bandit;
* Deffuant;
* firm dynamics.

### Modalità d'uso consigliata

Qui conviene enfatizzare:

* interpretazione economica o sociale dei parametri;
* eterogeneità degli agenti;
* lock-in e dipendenza dal percorso;
* equilibrio multiplo;
* implicazioni istituzionali o organizzative.

## 7. Uso in un corso di ottimizzazione stocastica, machine learning o algoritmi adattivi

### Obiettivo

Confrontare famiglie diverse di strategie di ricerca e apprendimento sotto incertezza.

### Progetti particolarmente adatti

* bandit;
* simulated annealing;
* algoritmi genetici;
* reti neurali / SGD;
* foraging.

### Modalità d'uso consigliata

In questi corsi è utile chiedere:

* benchmark coerenti;
* protocolli di confronto;
* misure di performance;
* costo computazionale;
* qualità empirica della convergenza.

Un filo comune molto produttivo è il trade-off tra esplorazione e sfruttamento.

## 8. Uso in un corso interdisciplinare su biologia, ecologia o sistemi adattivi

### Obiettivo

Collegare dinamiche individuali, popolazioni, interazioni e ambiente.

### Progetti particolarmente adatti

* reaction networks;
* epidemie su reti;
* foraging;
* geografia ecologica;
* Vicsek;
* contact process;
* copule e affidabilità, in chiave di robustezza e rischio sistemico.

### Modalità d'uso consigliata

In questi casi è particolarmente utile lavorare sui diversi livelli di descrizione:

* microsimulazione;
* dinamica mesoscopica;
* approssimazione mean-field;
* interpretazione biologica o ecologica delle osservabili.

---

# Filoni tematici consigliati

## A. Processi su reti, reticoli e sistemi spaziali

Progetti in cui la struttura di interazione conta esplicitamente.

Esempi:

* epidemie su reti;
* PageRank / random walk su grafi;
* percolazione;
* contact process e branching su grafi o reticoli;
* Ising dinamico / voter;
* geografia ecologica;
* TASEP/ASEP e trasporto fuori equilibrio.

## B. Dinamiche collettive e transizioni emergenti

Progetti in cui il punto centrale è l'emergere di ordine, consenso, polarizzazione, congestione o sopravvivenza.

Esempi:

* Ising dinamico / voter;
* Deffuant;
* Vicsek / herding;
* jamming e traffico;
* contact process;
* percolazione;
* TASEP/ASEP.

## C. Processi a eventi discreti e Markov in tempo continuo

Progetti centrati su eventi, intensità, salti, attese e CTMC.

Esempi:

* reaction networks / Gillespie;
* teoria delle code;
* Hawkes;
* contact process;
* epidemie su reti;
* TASEP/ASEP.

## D. Ottimizzazione stocastica, apprendimento e decisione

Progetti in cui si decide, si apprende o si ottimizza sotto incertezza.

Esempi:

* bandit;
* simulated annealing;
* algoritmi genetici;
* reti neurali e SGD;
* modello di March;
* foraging ottimale.

## E. Dinamiche socio-economiche e strategiche

Progetti in cui il linguaggio principale è quello dell'interazione sociale, dell'adozione, della competizione o della scelta collettiva.

Esempi:

* voting;
* Deffuant;
* network externalities;
* economic competition;
* replicator dynamics;
* modello di March;
* firm dynamics.

## F. Affidabilità, rischio e robustezza sistemica

Progetti centrati su dipendenza statistica, tempi di vita, fragilità o collasso.

Esempi:

* copule e affidabilità;
* percolazione;
* epidemie su reti;
* queueing in regime di overload;
* geografia ecologica in chiave di connettività e frammentazione.

---

# Classificazione a matrice

La classificazione piú utile non è una tassonomia rigida, ma una **matrice** in cui ogni progetto viene descritto simultaneamente lungo piú dimensioni. In questo modo uno stesso progetto può appartenere a un filone principale, ma anche essere confrontato con altri progetti per livello, strumenti richiesti e tipo di elaborato.

## Assi della matrice

Per ciascun progetto conviene indicare almeno le seguenti colonne:

| Progetto          | Filone principale        | Struttura matematica                                         | Livello                      | Profilo di lavoro                              | Output naturale                                              |
| ----------------- | ------------------------ | ------------------------------------------------------------ | ---------------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| Nome del progetto | una delle aree tematiche | DTMC, CTMC, SDE, Monte Carlo, rete, mean-field, ottimizzazione, inferenza | base / intermedio / avanzato | teorico / computazionale / misto / applicativo | simulazioni / analisi parametrica / confronto modelli / risultati teorici / visualizzazioni |

## Matrice completa dei progetti

\begin{landscape}
\footnotesize
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.15}

\begin{xltabular}{\linewidth}{
>{\RaggedRight\arraybackslash}p{2.8cm}
>{\RaggedRight\arraybackslash}p{3.4cm}
>{\RaggedRight\arraybackslash}X
>{\RaggedRight\arraybackslash}p{1.9cm}
>{\RaggedRight\arraybackslash}p{2.8cm}
>{\RaggedRight\arraybackslash}X
}
\caption{Classificazione a matrice dei progetti} \\
\toprule
Progetto & Filone principale & Struttura matematica & Livello & Profilo di lavoro & Output naturale \\
\midrule
\endfirsthead

\toprule
Progetto & Filone principale & Struttura matematica & Livello & Profilo di lavoro & Output naturale \\
\midrule
\endhead

\midrule
\multicolumn{6}{r}{\emph{Continua nella pagina seguente}} \\
\endfoot

\bottomrule
\endlastfoot

Bandit
& Ottimizzazione stocastica, apprendimento e decisione
& decisione stocastica sequenziale
& intermedio
& computazionale / applicativo
& regret, confronto tra strategie, trade-off esplorazione--sfruttamento \\

Chemical Reaction Networks
& Processi a eventi discreti e Markov in tempo continuo
& CTMC, simulazione event-driven, mean-field
& intermedio
& misto
& traiettorie, fluttuazioni, confronto con dinamica deterministica \\

Contact Process and Branching
& Dinamiche collettive e transizioni emergenti
& CTMC su reticolo o grafo, branching
& intermedio--avanzato
& teorico / computazionale
& soglia critica, sopravvivenza, assorbimento \\

Copule e Affidabilità
& Affidabilità, rischio e robustezza sistemica
& dipendenza statistica, affidabilità
& avanzato
& teorico / applicativo
& dipendenza in coda, failure system, robustezza \\

Deffuant
& Dinamiche collettive e transizioni emergenti
& dinamica agente-based
& base--intermedio
& computazionale
& consenso, polarizzazione, frammentazione \\

Economic Competition
& Dinamiche socio-economiche e strategiche
& modello dinamico stocastico / agente-based
& intermedio
& applicativo / misto
& quote di mercato, diffusione competitiva, scenari \\

Firm Dynamics
& Dinamiche socio-economiche e strategiche
& SDE / Fokker--Planck / mean-field
& avanzato
& teorico / misto
& distribuzioni, scaling, evoluzione temporale \\

Foraging
& Ottimizzazione stocastica, apprendimento e decisione
& random walk, decisione stocastica
& intermedio
& computazionale / misto
& efficienza di ricerca, trade-off esplorazione, tempi di scoperta \\

Genetic Algorithm
& Ottimizzazione stocastica, apprendimento e decisione
& euristiche stocastiche
& intermedio
& computazionale
& performance comparata, convergenza empirica, qualità della soluzione \\

Hawkes
& Processi a eventi discreti e Markov in tempo continuo
& point process autoeccitato
& intermedio--avanzato
& teorico / computazionale
& clustering temporale, intensità, simulazione o stima \\

Herding
& Dinamiche collettive e transizioni emergenti
& dinamica agente-based / interacting particles
& intermedio
& computazionale / applicativo
& comportamento collettivo, cascades, transizioni di regime \\

Ising and Voter
& Dinamiche collettive e transizioni emergenti
& spin system, DTMC / CTMC
& intermedio
& teorico / computazionale
& magnetizzazione, consenso, tempi caratteristici \\

Jamming
& Dinamiche collettive e transizioni emergenti
& automa cellulare o dinamica discreta
& base--intermedio
& computazionale / applicativo
& flusso, congestione, diagrammi fondamentali \\

March Model
& Dinamiche socio-economiche e strategiche
& dinamica discreta, apprendimento organizzativo
& base--intermedio
& applicativo / misto
& adattamento, esplorazione, rendimento \\

Network Epidemics
& Processi su reti, reticoli e sistemi spaziali
& CTMC o simulazione discreta su rete
& intermedio
& misto
& soglie epidemiche, prevalenza, confronto tra topologie \\

Network Externalities
& Dinamiche socio-economiche e strategiche
& dinamica discreta / agente-based
& base--intermedio
& applicativo / misto
& lock-in, diffusione, dipendenza dal percorso \\

Neural Networks
& Ottimizzazione stocastica, apprendimento e decisione
& ottimizzazione stocastica, SGD
& intermedio--avanzato
& computazionale
& curve di apprendimento, generalizzazione, confronto di architetture \\

PageRank
& Processi su reti, reticoli e sistemi spaziali
& DTMC su grafo
& base--intermedio
& computazionale / applicativo
& ranking, centralità, confronto topologico \\

Percolazione
& Dinamiche collettive e transizioni emergenti
& modello su reticolo o grafo, Monte Carlo
& intermedio
& teorico / computazionale
& cluster, soglie, transizioni \\

Queueing
& Processi a eventi discreti e Markov in tempo continuo
& CTMC
& base--intermedio
& teorico / computazionale
& tempi di attesa, utilizzo, regimi stazionari \\

Replicator Dynamics
& Dinamiche socio-economiche e strategiche
& ODE / mean-field
& intermedio--avanzato
& teorico / misto
& stabilità, equilibri, selezione dinamica \\

Simulated Annealing
& Ottimizzazione stocastica, apprendimento e decisione
& Monte Carlo, ottimizzazione
& intermedio
& computazionale
& qualità delle soluzioni, confronto tra schedule \\

Trasporto Fuori Equilibrio
& Dinamiche collettive e transizioni emergenti
& CTMC, trasporto fuori equilibrio
& avanzato
& teorico / computazionale
& correnti, profili di densità, transizioni di bordo \\

Voting
& Dinamiche socio-economiche e strategiche
& DTMC, agente-based
& base
& computazionale / misto
& consenso, tempi di assorbimento, dipendenza dalle regole \\

Patch Model 3 Levels
& Processi su reti, reticoli e sistemi spaziali
& modello spaziale multiscala / occupato-vuoto
& intermedio
& computazionale / misto
& persistenza, coarse graining, confronto tra livelli \\

\end{xltabular}
\end{landscape}

## Come usare concretamente la matrice

### Per gli studenti

La matrice permette di filtrare i progetti secondo tre domande molto semplici:

* voglio un progetto **piú teorico** o **piú computazionale**?
* cerco un progetto **base**, **intermedio** o **avanzato**?
* mi interessa di piú una dinamica su **reti**, un problema di **Markov**, un tema di **ottimizzazione**, oppure una dinamica **socio-economica**?

### Per i docenti

La matrice permette di selezionare i progetti in base al tipo di corso. Per esempio:

* in un corso introduttivo si possono preferire progetti di livello base o intermedio con output fortemente simulativo;
* in un corso di processi stocastici si possono scegliere progetti con struttura DTMC, CTMC o point process;
* in un corso di sistemi complessi si possono privilegiare progetti con transizioni emergenti e fenomeni collettivi;
* in un corso di metodi computazionali si possono scegliere progetti con forte componente algoritmica o di benchmarking numerico.

## Schema minimo da mettere in ogni scheda progetto

Per rendere davvero operativa la classificazione a matrice, ogni scheda progetto dovrebbe riportare in apertura una riga sintetica del tipo:

| Filone | Struttura | Livello | Profilo | Output |
| ------ | --------- | ------- | ------- | ------ |
| ...    | ...       | ...     | ...     | ...    |

In questo modo lo studente può orientarsi in pochi secondi, mentre il docente può confrontare rapidamente progetti diversi.

---

# Raccomandazione finale

La classificazione a matrice è il compromesso migliore tra chiarezza e flessibilità. I filoni servono a dare una mappa concettuale generale; la matrice serve invece a scegliere, confrontare e riusare i progetti in contesti didattici diversi.