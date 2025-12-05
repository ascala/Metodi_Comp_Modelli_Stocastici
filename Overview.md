---
title: "Syllabus del corso: Modelli Stocastici e Metodi Computazionali"
date:
---

## Introduzione ai Modelli Stocastici

### Modelli stocastici e incertezza

I modelli stocastici sono strumenti fondamentali per rappresentare e analizzare sistemi in cui l'incertezza gioca un ruolo essenziale. A differenza dei modelli deterministici, che assegnano un'evoluzione certa e prevedibile a un sistema dato uno stato iniziale, i modelli stocastici incorporano elementi casuali e permettono di studiare le probabilità associate a differenti traiettorie o risultati.

Questa caratteristica li rende particolarmente adatti a descrivere fenomeni complessi e dinamici in cui l'informazione completa è inaccessibile o il rumore gioca un ruolo strutturale.

### Processi aleatori

Un processo aleatorio è una famiglia di variabili casuali indicizzate nel tempo (continuo o discreto), che descrive l'evoluzione di un sistema sotto l'effetto dell'incertezza. I processi aleatori sono utilizzati per modellare una varietà di fenomeni: l'andamento dei mercati finanziari, la diffusione di sostanze in un fluido, il comportamento di popolazioni biologiche, o le decisioni individuali in contesti incerti.

Alcuni esempi classici includono il moto browniano, il processo di Poisson e le catene di Markov.

### Processi di Markov

I processi di Markov rappresentano una classe particolarmente importante di processi aleatori, caratterizzati dalla *proprietà di Markov*: la probabilità della transizione verso stati futuri dipende solo dallo stato attuale e non dalla storia passata del processo.

Questa assunzione di *assenza di memoria* semplifica notevolmente l'analisi e la simulazione di modelli dinamici, permettendo di costruire modelli efficienti per una grande varietà di applicazioni. Le catene di Markov a tempo discreto, ad esempio, sono spesso utilizzate per modellare sequenze di eventi in biologia molecolare, sistemi computazionali o comportamento del consumatore.

### Esempi interdisciplinari

- **Diffusione**: il moto browniano descrive il comportamento casuale di particelle sospese in un fluido ed è alla base delle equazioni tipo Langevin. Questo tipo di modello si applica anche a contesti sociali, come la diffusione dell'informazione o di opinioni in una rete.
- **Crescita**: i modelli stocastici di crescita descrivono l'evoluzione nel tempo di popolazioni o sistemi fisici sotto vincoli di risorse, mutazioni o interazioni casuali. Un esempio classico è il processo di branching, usato anche in epidemiologia e fisica delle reazioni nucleari.
- **Epidemie**: i modelli stocastici tipo SIR (Susceptible–Infected–Recovered) con dinamiche aleatorie sono cruciali per simulare focolai infettivi e valutare strategie di contenimento in presenza di incertezza.
- **Scelte individuali**: in economia comportamentale e scienze cognitive, i modelli stocastici rappresentano il processo decisionale umano in presenza di informazione imperfetta, utilizzando modelli basati su catene di Markov o equazioni differenziali stocastiche.

---

## Metodi Monte Carlo e Simulazione Stocastica

### Introduzione ai metodi Monte Carlo

I metodi Monte Carlo costituiscono una classe fondamentale di tecniche computazionali per l'approssimazione di quantità complesse mediante l'uso della casualità. L'idea di base è semplice ma potente: anziché calcolare un valore in modo esatto (spesso impossibile), lo si stima generando molte realizzazioni casuali del fenomeno di interesse e computando una media. Questo approccio si applica all'integrazione numerica, alla stima di probabilità, all'ottimizzazione, e alla generazione di configurazioni secondo distribuzioni target.

### Generazione di numeri casuali e campionamento

Il primo passo nei metodi Monte Carlo è la generazione di **numeri pseudocasuali**, sequenze deterministiche ma con proprietà statistiche simili al caso reale. Da questi si ottengono variabili casuali secondo distribuzioni desiderate (uniforme, esponenziale, normale) tramite trasformazioni analitiche, inversione della funzione di ripartizione o tecniche di accettazione–rifiuto.

Il campionamento da distribuzioni arbitrarie è un problema centrale in statistica computazionale. Quando la funzione di densità non è normalizzata o è difficile da invertire, si ricorre a metodi indiretti, come accettazione–rifiuto o catene di Markov.

### Integrazione Monte Carlo

Un'applicazione tipica è l'integrazione numerica di una funzione $f(x)$ su un dominio $D$:

$$\int_D f(x)\,dx \approx \frac{1}{N} \sum_{i=1}^N f(x_i)$$

dove i punti $x_i$ sono scelti casualmente secondo una distribuzione nota. Il metodo è vantaggioso in alta dimensione, dove le tecniche deterministiche diventano inefficienti.

### Accettazione–rifiuto e Metropolis–Hastings

Il metodo di accettazione–rifiuto genera campioni da una distribuzione difficile usando una funzione di proposta più semplice, accettando con probabilità basata sul rapporto tra funzione target e proposta.

L'algoritmo di **Metropolis–Hastings** generalizza questo approccio e costituisce il cuore delle tecniche *Markov Chain Monte Carlo* (MCMC). Esso costruisce una catena che ha come distribuzione stazionaria quella desiderata, consentendo il campionamento anche in distribuzioni complesse.

### Catene di Markov e applicazioni MCMC

Le catene di Markov vengono usate nei metodi Monte Carlo per costruire sequenze di stati che esplorano efficacemente lo spazio delle configurazioni.  
Le tecniche MCMC trovano applicazioni in stima bayesiana, simulazioni di sistemi fisici complessi (es. modelli di spin), e inferenza statistica.

### Esempi interdisciplinari

- **Fisica statistica**: simulazioni di reticoli di spin (Ising, Potts) e sistemi termodinamici con MCMC.  
- **Chimica computazionale**: campionamento dello spazio conformazionale di molecole e calcolo di energie libere.  
- **Biologia**: inferenza di reti genetiche e simulazioni di dinamiche evolutive.  
- **Finanza**: pricing di opzioni e calibrazione di modelli stocastici.  
- **Ingegneria**: analisi di affidabilità strutturale e propagazione di incertezza.  
- **Scienze sociali**: diffusione di opinioni e informazione su reti.

---

## Equazioni tipo Langevin e dinamiche stocastiche

### Equazioni di Langevin

Le equazioni di Langevin descrivono l'evoluzione di sistemi fisici, biologici o sociali soggetti a fluttuazioni casuali:

$$\frac{dx}{dt} = -\frac{dU}{dx} + \sqrt{2D}\,\eta(t)$$

dove $U(x)$ è il potenziale, $D$ la costante di diffusione e $\eta(t)$ rumore bianco con $\langle \eta(t)\eta(t')\rangle=\delta(t-t')$.

### Integrazione numerica: schema di Euler–Maruyama

Lo schema di Euler–Maruyama, per passi $\Delta t$, è:

$$x_{n+1} = x_n + f(x_n)\Delta t + \sigma(x_n)\sqrt{\Delta t}\,Z_n$$

dove $Z_n\sim\mathcal{N}(0,1)$.  
È analogo al metodo di Eulero deterministico, ma con un termine casuale.

### Stabilità numerica

Per il caso lineare

$$dx = -\lambda x\,dt + \sigma\,dW_t$$

la soluzione ha varianza finita solo se $\lambda>0$.  
Euler–Maruyama è stabile se $\lambda\Delta t < 2$.

### Espansioni gaussiane vicino agli stati stazionari

Linearizzando vicino a $x^*$:

$$dx \approx -A(x-x^*)\,dt + \sqrt{2D}\,dW_t$$

con $A=\frac{df}{dx}|_{x^*}$, la varianza stazionaria è $\mathrm{Var}(x)=D/A$.

### Esempi interdisciplinari

- **Fisica**: moto browniano e fluttuazioni fuori equilibrio.  
- **Chimica**: tassi di reazione termicamente attivati.  
- **Biologia**: movimento cellulare, rumore nell’espressione genica.  
- **Economia e finanza**: modelli stocastici dei tassi o dei prezzi.  
- **Ingegneria**: vibrazioni stocastiche e controllo robusto.

---

## Simulazione di eventi discreti e algoritmo di Gillespie

### Modelli a eventi discreti

Molti sistemi reali evolvono attraverso eventi casuali discreti (reazioni chimiche, infezioni, interazioni sociali).  
In questi casi, si usa una rappresentazione esplicita degli eventi.

### Algoritmo di Gillespie

Procedura esatta per simulare la dinamica temporale di un sistema con tassi $a_j$ associati a ciascun evento:

1. Calcola $a_0=\sum_j a_j$.  
2. Genera $r_1,r_2\sim\mathcal{U}(0,1)$.  
3. Determina $\Delta t = (1/a_0)\ln(1/r_1)$.  
4. Scegli l’evento $j$ tale che $\sum_{k<j}a_k < r_2 a_0 \le \sum_{k\le j}a_k$.  
5. Aggiorna lo stato e ripeti.

### Applicazioni

- **Reazioni chimiche**: reti biochimiche a basse concentrazioni.  
- **Ecologia**: dinamiche preda–predatore in popolazioni piccole.  
- **Epidemie**: modelli SIR discreti per la fase iniziale di un focolaio.

### Vantaggi e limiti

- **Vantaggi**: esatto, generalizzabile.  
- **Limiti**: costoso per eventi frequenti; esistono versioni accelerate ($\tau$-leaping) o ibride.

---

## Processi di branching e modelli di crescita

### Dinamiche di crescita stocastica

La crescita di popolazioni, epidemie o strutture può essere descritta da modelli in cui ogni entità genera un numero casuale di discendenti.

### Processi di branching

Modello classico:

$$Z_{t+1} = \sum_{i=1}^{Z_t} X_i$$

con $X_i$ i.i.d. e $\mu=\mathbb{E}[X_i]$:
- $\mu<1$: estinzione certa;
- $\mu=1$: processo critico;
- $\mu>1$: probabilità positiva di crescita illimitata.

### Soglie critiche e comportamento asintotico

Vicino a $\mu=1$ si osservano leggi di potenza in durate e dimensioni.  
Fenomeni analoghi compaiono in propagazione di idee, attivazione neuronale, percolazione.

### Modelli di crescita su reti

L'estensione dei processi di crescita a **reti complesse** permette di modellare fenomeni reali in cui le interazioni non sono uniformi.  
In questi modelli, ogni nodo rappresenta un'entità (ad esempio individuo, cellula, o sito), mentre gli archi definiscono le possibili interazioni o influenze.

La struttura della rete influenza profondamente la soglia critica e la probabilità di crescita o estinzione:

- nei **reticoli regolari**, la soglia critica dipende dalla dimensionalità;  
- nelle **reti scale-free**, la soglia può scomparire se la distribuzione dei gradi ha varianza infinita;  
- nelle **reti small-world**, la connessione a lungo raggio accelera la diffusione e modifica la probabilità di sopravvivenza.


**Principali ambiti di applicazione:**

- **epidemiologia matematica**: diffusione di epidemie su reti di contatto o mobilità, studio della soglia epidemica e delle strategie di contenimento;  
- **ecologia e biologia delle popolazioni**: espansione di specie in habitat frammentati, metapopolazioni e processi di colonizzazione; 
- **Economia e finanza**: propagazione di shock o crisi attraverso reti di interdipendenze produttive o finanziarie, effetti moltiplicativi e *contagion models*;  
- **marketing e scienze sociali**: diffusione di innovazioni, prodotti o idee in reti di consumo e comunicazione (marketing virale, adozione sociale);  
- **demografia e dinamiche urbane**: modelli di crescita e migrazione su reti territoriali;  
- **infrastrutture e sistemi**: cascata di guasti, congestioni o vulnerabilità sistemiche.

---

## Dinamiche molecolari e Boltzmann machine

### Dinamiche molecolari (MD)

Le simulazioni di **dinamica molecolare** descrivono l’evoluzione nel tempo di un sistema di particelle interagenti soggette alle leggi della meccanica classica:

$$m \frac{d^2\mathbf{x}_i}{dt^2} = -\nabla_{\mathbf{x}_i}U(\mathbf{x}_1,\ldots,\mathbf{x}_N).$$

Esse permettono di ricavare grandezze termodinamiche, distribuzioni spaziali e proprietà di trasporto a partire dalle traiettorie delle particelle.

### Sistemi di hard e soft spheres

- **Hard spheres**: particelle che interagiscono solo al contatto, mediante collisioni elastiche istantanee.  
- **Soft spheres**: interazioni regolate da potenziali continui, ad esempio il potenziale di Lennard–Jones:

  $$U(r)=4\epsilon[(\sigma/r)^{12}-(\sigma/r)^6].$$

La scelta del potenziale dipende dal livello di dettaglio richiesto e dal tipo di sistema studiato.

### Aspetti computazionali

L’efficienza delle simulazioni MD richiede:
- integrazione temporale stabile ed efficiente (schemi Verlet, leapfrog, velocity–Verlet);  
- aggiornamento rapido delle **liste di vicinato**;  
- **condizioni al contorno periodiche** per minimizzare gli effetti di bordo;  
- bilanciamento tra realismo fisico e costo computazionale.

### Boltzmann machine

Una **Boltzmann machine** è un modello probabilistico ispirato alla fisica statistica, basato su unità binarie $s_i\in\{0,1\}$ con interazioni simmetriche:

$$P(\mathbf{s})=\frac{1}{Z}\exp\!\left(\sum_{i<j}w_{ij}s_is_j+\sum_i b_i s_i\right).$$

Questi modelli apprendono distribuzioni complesse dai dati e sono allenati tramite algoritmi **MCMC** (Metropolis o Gibbs sampling).  
Le versioni *restricted* o *deep* (RBM, DBM) costituiscono la base di molte architetture di apprendimento profondo.

### Applicazioni interdisciplinari

- **Fisica della materia condensata**: studio di transizioni di fase, dinamiche di cristallizzazione e proprietà strutturali di liquidi e solidi.  
- **Chimica computazionale**: simulazione del moto molecolare, calcolo di energie libere e cinetiche di reazione.  
- **Biologia strutturale**: dinamica di proteine, acidi nucleici e complessi molecolari, progettazione di farmaci.  
- **Scienza dei materiali**: progettazione e analisi di nanostrutture, polimeri e superfici funzionalizzate.  
- **Ingegneria chimica e fisica tecnica**: modellazione del trasporto di massa e calore in fluidi complessi.  
- **Machine learning e AI**: apprendimento non supervisionato, generazione di pattern e rappresentazioni latenti mediante Boltzmann machine e reti neurali stocastiche.  
- **Neuroscienze computazionali**: modellazione di reti neuronali stocastiche e propagazione dell’attività sinaptica.  
- **Finanza quantitativa**: simulazioni di mercati e dinamiche di prezzo ispirate a modelli di energia libera e transizioni di fase.  
- **Scienze sociali e reti**: modellazione di interazioni binarie (scelte, cooperazione, opinioni) come configurazioni di spin in reti sociali complesse.

## Simulated Annealing e ottimizzazione stocastica

### Ottimizzazione e paesaggi energetici complessi

Molti problemi di ottimizzazione presentano *paesaggi energetici* con numerosi minimi locali; servono strategie globali.

### Principio del simulated annealing

Ispirato al raffreddamento termico: accetta transizioni verso stati a energia maggiore con probabilità

$$P_{\text{acc}} =
\begin{cases}
1 & \text{se } \Delta E \le 0,\\
\exp(-\Delta E/T) & \text{se } \Delta E > 0
\end{cases}$$

dove $\Delta E=E(x')-E(x)$.

### Algoritmo di base

1. Inizializza $x$ e temperatura $T$.  
2. Genera proposta $x'$.  
3. Calcola $\Delta E$.  
4. Accetta $x'$ con $P_{\text{acc}}$.  
5. Riduci $T$ (es. $T_k=T_0/\log(1+k)$).  
6. Ripeti fino a convergenza.

### Convergenza e vantaggi

Con schedule adeguato, converge al minimo globale con probabilità 1.  
Vantaggi: esplorazione globale, semplicità, robustezza al rumore.

### Esempi interdisciplinari

- **Fisica**: spin-glass e stati a bassa energia.  
- **Chimica computazionale**: struttura molecolare minima, docking.  
- **Biologia computazionale**: struttura proteica e filogenesi.  
- **Ingegneria**: reti ottimizzate e sistemi complessi.  
- **Finanza**: costruzione di portafogli ottimali.  
- **Reti**: ottimizzazione della resilienza.  
- **Machine learning**: ricerca di iperparametri o architetture.

---

## Riferimenti essenziali

- Gardiner, C. W. *Handbook of Stochastic Methods*. Springer.  
- Van Kampen, N. G. *Stochastic Processes in Physics and Chemistry*. Elsevier.  
- Gillespie, D. T. (1977). *Exact stochastic simulation of coupled chemical reactions*. *J. Phys. Chem.*  
- Kalos, M. H., Whitlock, P. A. *Monte Carlo Methods*. Wiley.  
- Binder, K., Heermann, D. *Monte Carlo Simulation in Statistical Physics*. Springer.  
- Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. *SIAM Review.*  
- Metropolis, N., Ulam, S. (1949). *The Monte Carlo Method*. *JASA.*
