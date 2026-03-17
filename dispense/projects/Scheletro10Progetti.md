# 10 possibili progetti per il corso di Metodi Computazionali per Modelli Stocastici

---

## Progetto 1 -- Confronto tra regole di voto su profili casuali

### Idea generale

Questo progetto introduce i sistemi di voto come caso di studio per un corso di metodi computazionali per modelli stocastici. L'obiettivo e' confrontare diverse regole di aggregazione delle preferenze individuali in presenza di profili generati casualmente.

Il punto centrale e' che regole di voto diverse possono produrre vincitori diversi a partire dallo stesso insieme di preferenze. Questo permette di studiare in modo computazionale temi classici come paradossi di maggioranza, robustezza delle procedure decisionali e sensibilita' alla struttura delle preferenze.

### Variabili di stato

Consideriamo una popolazione di $N$ elettori e un insieme di $m$ candidati.

Ogni elettore $i$ possiede una classifica completa dei candidati:
$$
\pi_i = (\pi_i(1),\dots,\pi_i(m)),
$$
dove $\pi_i(1)$ e' il candidato preferito e $\pi_i(m)$ il meno preferito.

L'intero stato del sistema e' il profilo delle preferenze:
$$
\Pi = (\pi_1,\dots,\pi_N).
$$

### Dinamica o componente stocastica

La parte stocastica del progetto non sta in una dinamica temporale, ma nella generazione casuale dei profili elettorali.

Si possono considerare almeno tre schemi:

1. profili completamente casuali;
2. preferenze spaziali, dove ogni elettore e ogni candidato occupano una posizione in uno spazio ideologico;
3. profili con blocchi o fazioni, per introdurre correlazioni tra elettori.

Per ogni profilo generato si applicano diverse regole di voto:
- plurality;
- majority runoff;
- Borda count;
- approval voting;
- criterio di Condorcet, quando applicabile.

### Osservabili da misurare

Le osservabili principali possono essere:

1. frequenza con cui regole diverse producono vincitori diversi;
2. probabilita' di ciclo di Condorcet;
3. robustezza del vincitore rispetto a piccole perturbazioni del profilo;
4. distanza tra vincitore e candidato mediano in modelli spaziali;
5. sensibilita' al numero di candidati.

### Schema del laboratorio

#### Laboratorio 1 -- Implementazione delle regole di voto

**Obiettivo**

Implementare diverse regole di voto e verificare che, sullo stesso profilo, possano produrre esiti diversi.

**Attivita'**

1. generare profili casuali;
2. implementare plurality, Borda e runoff;
3. confrontare i vincitori;
4. costruire esempi in cui i risultati divergono.

#### Laboratorio 2 -- Paradosso di Condorcet

**Obiettivo**

Studiare la frequenza dei cicli di maggioranza al variare di $N$ e $m$.

**Attivita'**

1. costruire la matrice dei confronti a due a due;
2. rilevare la presenza di cicli;
3. stimare la frequenza del fenomeno su molte simulazioni.

#### Laboratorio 3 -- Preferenze spaziali

**Obiettivo**

Confrontare le regole di voto quando gli elettori sono distribuiti in uno spazio delle preferenze.

**Attivita'**

1. assegnare posizioni casuali a elettori e candidati;
2. derivare le classifiche dalla distanza;
3. confrontare i vincitori e la loro stabilita'.

### Estensioni naturali

1. turnout casuale;
2. informazione incompleta degli elettori;
3. voto strategico;
4. sistemi a due turni con candidati che si riposizionano.

---

## Progetto 2 -- Opinion dynamics su rete con bounded confidence

### Idea generale

Questo progetto studia la formazione del consenso e della polarizzazione in una popolazione di agenti connessi da una rete sociale. Gli agenti aggiornano la propria opinione solo se la distanza rispetto ai vicini resta sotto una certa soglia di tolleranza.

Il progetto e' utile per introdurre il rapporto tra topologia della rete, interazione locale e configurazioni collettive finali.

### Variabili di stato

Consideriamo una rete con $N$ nodi e matrice di adiacenza $A$.

Ogni nodo $i$ possiede una opinione scalare:
$$
x_i(t) \in [0,1].
$$

Lo stato del sistema al tempo $t$ e' quindi il vettore:
$$
x(t) = (x_1(t),\dots,x_N(t)).
$$

### Dinamica stocastica

Una possibile versione e' il modello di Deffuant su rete.

A ogni passo:
1. si sceglie casualmente un arco $(i,j)$;
2. se
   $$
   |x_i(t)-x_j(t)|<\varepsilon,
   $$
   allora i due agenti si avvicinano:
   $$
   x_i(t+1)=x_i(t)+\mu\bigl(x_j(t)-x_i(t)\bigr),
   $$
   $$
   x_j(t+1)=x_j(t)+\mu\bigl(x_i(t)-x_j(t)\bigr);
   $$
3. altrimenti non accade nulla.

Qui $\varepsilon$ e' la soglia di confidenza e $\mu$ il parametro di aggiustamento.

### Osservabili da misurare

1. numero finale di cluster di opinione;
2. tempo di convergenza;
3. varianza finale delle opinioni;
4. probabilita' di consenso globale;
5. dipendenza da $\varepsilon$ e dalla topologia della rete.

### Schema del laboratorio

#### Laboratorio 1 -- Implementazione del modello base

**Obiettivo**

Simulare il modello su rete casuale o su anello e osservare il ruolo della soglia di confidenza.

**Attivita'**

1. generare una rete semplice;
2. inizializzare opinioni uniformi in $[0,1]$;
3. simulare la dinamica;
4. visualizzare le traiettorie e i cluster finali.

#### Laboratorio 2 -- Effetto della topologia

**Obiettivo**

Confrontare anello, Erd\H{o}s--R\'enyi, small-world e rete con hub.

**Attivita'**

1. costruire reti con uguale numero di nodi;
2. fissare $\varepsilon$ e $\mu$;
3. confrontare consenso e polarizzazione.

#### Laboratorio 3 -- Rumore o agenti ostinati

**Obiettivo**

Studiare come il risultato cambi in presenza di agenti stubborn o di perturbazioni casuali.

**Attivita'**

1. fissare alcuni nodi con opinione bloccata;
2. aggiungere rumore debole;
3. osservare se il consenso viene impedito.

### Estensioni naturali

1. aggiornamento asincrono o sincrono;
2. opinioni vettoriali;
3. rete adattiva con rewiring;
4. influenza dei media.

---

## Progetto 3 -- Modello di Vicsek per branchi animali

### Idea generale

Questo progetto introduce un modello minimale di moto collettivo per descrivere branchi, stormi o sciami. Agenti auto-propellenti si muovono nel piano e tendono ad allineare la propria direzione con quella dei vicini, in presenza di rumore.

Il problema e' paradigmatico per lo studio di transizioni ordine--disordine in sistemi collettivi.

### Variabili di stato

Ogni particella $i$ ha:
- posizione $r_i(t) \in \mathbb{R}^2$;
- direzione di moto $\theta_i(t)$;
- velocita' di modulo costante $v_0$.

Lo stato del sistema e' dato da tutte le posizioni e direzioni.

### Dinamica stocastica

A ogni passo temporale:

1. la direzione si aggiorna verso la direzione media dei vicini entro raggio $R$:
   $$
   \theta_i(t+\Delta t)=\mathrm{Arg}\!\left(\sum_{j \in \mathcal{N}_i} e^{i\theta_j(t)}\right)+\eta \xi_i(t),
   $$
   dove $\xi_i(t)$ e' un rumore uniforme;
2. la posizione evolve come
   $$
   r_i(t+\Delta t)=r_i(t)+v_0(\cos\theta_i,\sin\theta_i)\Delta t.
   $$

### Osservabili da misurare

1. parametro d'ordine globale
   $$
   \Phi(t)=\frac{1}{N v_0}\left|\sum_{i=1}^N v_i(t)\right|;
   $$
2. dimensione dei cluster;
3. correlazione direzionale;
4. dipendenza da densita' e rumore;
5. tempi di formazione dell'ordine collettivo.

### Schema del laboratorio

#### Laboratorio 1 -- Simulazione del modello base

**Obiettivo**

Osservare la formazione spontanea del moto ordinato.

**Attivita'**

1. inizializzare posizioni e direzioni casuali;
2. simulare la dinamica per diversi valori di $\eta$;
3. visualizzare traiettorie e parametro d'ordine.

#### Laboratorio 2 -- Transizione ordine--disordine

**Obiettivo**

Studiare l'effetto del rumore.

**Attivita'**

1. fissare $N$, $v_0$ e la densita';
2. variare $\eta$;
3. costruire il grafico di $\Phi$ in funzione di $\eta$.

#### Laboratorio 3 -- Densita' e flocking

**Obiettivo**

Studiare il ruolo della densita' nel favorire allineamento e clustering.

**Attivita'**

1. variare la dimensione del dominio;
2. mantenere fisso $N$;
3. confrontare i regimi osservati.

### Estensioni naturali

1. interazioni metriche o topologiche;
2. ostacoli nello spazio;
3. predatori o repulsione locale;
4. velocita' variabile.

---

## Progetto 4 -- Affidabilita' di reti infrastrutturali

### Idea generale

Il progetto studia la robustezza di una rete infrastrutturale soggetta a guasti casuali. I nodi possono rappresentare stazioni, sottostazioni, router o snodi logistici, mentre gli archi rappresentano collegamenti fisici o funzionali.

L'obiettivo e' capire come la struttura della rete influisca sulla sua vulnerabilita'.

### Variabili di stato

Consideriamo una rete con $N$ nodi e matrice di adiacenza $A$.

Ogni nodo o arco puo' essere:
- funzionante;
- guasto.

Lo stato del sistema puo' essere rappresentato da un vettore binario:
$$
s_i(t) \in \{0,1\},
$$
oppure da stati sugli archi.

### Dinamica stocastica

Una versione elementare prevede:

1. ogni componente funzionante fallisce con probabilita' $p_f$;
2. ogni componente guasto viene riparato con probabilita' $p_r$;
3. opzionalmente, il guasto di un nodo puo' aumentare il carico sui vicini, rendendo piu' probabili guasti secondari.

### Osservabili da misurare

1. dimensione della componente connessa principale;
2. probabilita' di disconnessione tra sorgente e destinazione;
3. numero medio di componenti guaste;
4. tempo medio al collasso;
5. resilienza dopo riparazione.

### Schema del laboratorio

#### Laboratorio 1 -- Guasti indipendenti

**Obiettivo**

Studiare la robustezza della rete sotto rimozione casuale di nodi o archi.

**Attivita'**

1. generare diverse topologie;
2. rimuovere una frazione casuale di componenti;
3. misurare connettivita' residua.

#### Laboratorio 2 -- Guasti mirati

**Obiettivo**

Confrontare attacchi casuali e attacchi ai nodi ad alto grado.

**Attivita'**

1. ordinare i nodi per centralita';
2. rimuoverli progressivamente;
3. confrontare il danno strutturale.

#### Laboratorio 3 -- Riparazione e resilienza

**Obiettivo**

Studiare come strategie diverse di ripristino influenzino il recupero del sistema.

**Attivita'**

1. introdurre riparazione casuale;
2. introdurre riparazione prioritaria;
3. confrontare i tempi di recupero.

### Estensioni naturali

1. reti pesate;
2. flussi e capacità limitate;
3. failure cascades;
4. reti multilivello interdipendenti.

---

## Progetto 5 -- Sistemi di coda M/M/1 e M/M/c con simulazione a eventi discreti

### Idea generale

Questo progetto introduce i processi di coda come caso di studio classico della probabilita' applicata. Clienti arrivano in modo casuale, richiedono servizio e possono attendere in coda se tutti i server sono occupati.

Il progetto e' particolarmente utile per collegare processi di Poisson, tempi esponenziali e simulazione ad eventi discreti.

### Variabili di stato

Nel caso M/M/1, lo stato al tempo $t$ e' il numero di clienti nel sistema:
$$
X(t) \in \{0,1,2,\dots\}.
$$

Nel caso M/M/c, lo stato resta il numero totale di clienti, ma il numero di server e' $c$.

### Dinamica stocastica

Gli arrivi seguono un processo di Poisson di intensita' $\lambda$.

I tempi di servizio sono esponenziali con parametro $\mu$.

Nel caso M/M/1:
- se il sistema non e' vuoto, il tasso di uscita e' $\mu$;
- se il sistema e' vuoto, non ci sono uscite.

Nel caso M/M/c:
- se ci sono $n$ clienti nel sistema, il tasso totale di completamento e'
  $$
  \min(n,c)\mu.
  $$

### Osservabili da misurare

1. lunghezza media della coda;
2. tempo medio nel sistema;
3. tempo medio di attesa;
4. utilizzazione del server o dei server;
5. probabilita' di congestione.

### Schema del laboratorio

#### Laboratorio 1 -- Simulazione di una M/M/1

**Obiettivo**

Implementare una simulazione ad eventi discreti e stimare le osservabili principali.

**Attivita'**

1. generare tempi di arrivo e servizio;
2. aggiornare il sistema evento per evento;
3. registrare attese e tempi di permanenza;
4. confrontare i risultati con le formule teoriche.

#### Laboratorio 2 -- Effetto del carico

**Obiettivo**

Studiare il ruolo del rapporto
$$
\rho=\frac{\lambda}{\mu}.
$$

**Attivita'**

1. fissare $\mu$;
2. variare $\lambda$;
3. misurare crescita della coda al tendere di $\rho$ a $1$.

#### Laboratorio 3 -- Confronto M/M/1 e M/M/c

**Obiettivo**

Valutare l'effetto di piu' server.

**Attivita'**

1. fissare il tasso totale di servizio;
2. confrontare diversi valori di $c$;
3. osservare tempi di attesa e congestione.

### Estensioni naturali

1. distribuzioni di servizio non esponenziali;
2. code con capacità finita;
3. priorità tra clienti;
4. rete di code.

---

## Progetto 6 -- Multi-armed bandits e apprendimento sequenziale

### Idea generale

Questo progetto studia il problema della scelta sequenziale in condizioni di incertezza. Un agente deve scegliere, a ogni istante, uno tra piu' bracci, ciascuno con ricompensa casuale ignota.

Il problema esprime in modo molto pulito il trade-off tra exploration ed exploitation.

### Variabili di stato

Supponiamo di avere $K$ bracci.

Per ciascun braccio $a$:
- numero di volte in cui e' stato scelto, $N_a(t)$;
- ricompensa media empirica, $\hat \mu_a(t)$.

Lo stato dell'algoritmo e' l'insieme di queste statistiche.

### Dinamica stocastica

A ogni tempo $t$:

1. l'algoritmo sceglie un braccio $A_t$ secondo una regola decisionale;
2. osserva una ricompensa casuale
   $$
   R_t \sim \nu_{A_t};
   $$
3. aggiorna le statistiche del braccio selezionato.

Si possono confrontare almeno tre strategie:
- epsilon-greedy;
- UCB;
- Thompson sampling.

### Osservabili da misurare

1. regret cumulato;
2. numero di selezioni del braccio ottimo;
3. velocita' di apprendimento;
4. sensibilita' ai parametri dell'algoritmo;
5. confronto tra scenari facili e difficili.

### Schema del laboratorio

#### Laboratorio 1 -- Epsilon-greedy

**Obiettivo**

Implementare la strategia epsilon-greedy e studiare il ruolo del parametro $\varepsilon$.

**Attivita'**

1. definire ricompense Bernoulli o gaussiane;
2. simulare molte traiettorie;
3. misurare il regret medio.

#### Laboratorio 2 -- UCB

**Obiettivo**

Confrontare una politica guidata dall'incertezza con epsilon-greedy.

**Attivita'**

1. implementare UCB;
2. confrontare il regret;
3. osservare la rapidita' di identificazione del braccio migliore.

#### Laboratorio 3 -- Thompson sampling

**Obiettivo**

Studiare una strategia bayesiana elementare.

**Attivita'**

1. usare ricompense Bernoulli;
2. aggiornare posteriori beta;
3. confrontare le prestazioni con gli altri metodi.

### Estensioni naturali

1. bandits non stazionari;
2. contextual bandits;
3. costi di switching;
4. vincoli di rischio.

---

## Progetto 7 -- Reti di reazione chimica con algoritmo di Gillespie

### Idea generale

Questo progetto introduce una descrizione stocastica di reazioni chimiche in sistemi con numeri di molecole finiti. Quando le popolazioni sono piccole, il comportamento discreto e casuale degli eventi di reazione diventa importante e le equazioni deterministiche di concentrazione non sono piu' sufficienti.

### Variabili di stato

Consideriamo $d$ specie chimiche con conteggi molecolari:
$$
X(t)=(X_1(t),\dots,X_d(t)).
$$

Ogni reazione $r$ e' caratterizzata da:
- uno stato iniziale;
- uno stato finale;
- una propensity $a_r(X)$.

### Dinamica stocastica

L'algoritmo di Gillespie procede cosi':

1. dato lo stato corrente $X$, si calcolano tutte le propensity;
2. si estrae il tempo del prossimo evento da una legge esponenziale;
3. si sceglie quale reazione avviene con probabilita' proporzionale alla propria propensity;
4. si aggiorna lo stato.

### Osservabili da misurare

1. traiettorie temporali dei conteggi molecolari;
2. distribuzioni stazionarie;
3. tempi di primo passaggio;
4. media e varianza delle specie;
5. differenze rispetto alla descrizione deterministica.

### Schema del laboratorio

#### Laboratorio 1 -- Birth--death process

**Obiettivo**

Implementare il caso piu' semplice e confrontare media empirica e teoria.

**Attivita'**

1. definire una nascita e una morte;
2. simulare molte traiettorie;
3. costruire istogrammi.

#### Laboratorio 2 -- Dimerizzazione o conversione

**Obiettivo**

Studiare una rete di reazione con interazioni non lineari.

**Attivita'**

1. introdurre una reazione bimolecolare;
2. confrontare simulazioni e rate equations;
3. osservare il ruolo delle fluttuazioni.

#### Laboratorio 3 -- Autocatalisi o bistabilita'

**Obiettivo**

Studiare sistemi con switching stocastico tra stati metastabili.

**Attivita'**

1. implementare una rete con feedback;
2. stimare i tempi di switching;
3. confrontare diverse dimensioni del sistema.

### Estensioni naturali

1. reaction--diffusion su reticolo;
2. tau-leaping;
3. rumore estrinseco sui parametri;
4. coupling con modelli biologici.

---

## Progetto 8 -- Modelli di scambio di ricchezza

### Idea generale

Questo progetto studia come semplici interazioni casuali tra agenti possano generare distribuzioni aggregate di ricchezza non banali. Il problema e' interessante perche' collega dinamiche microscopiche semplici a misure macroscopiche di disuguaglianza.

### Variabili di stato

Consideriamo $N$ agenti con ricchezze
$$
w_i(t)\ge 0.
$$

Lo stato del sistema e' il vettore
$$
w(t)=(w_1(t),\dots,w_N(t)).
$$

In molte versioni la ricchezza totale e' conservata:
$$
\sum_{i=1}^N w_i(t)=W.
$$

### Dinamica stocastica

A ogni passo si seleziona casualmente una coppia $(i,j)$ e si applica una regola di scambio.

Una versione semplice senza saving e':
$$
w_i'=\varepsilon (w_i+w_j), \qquad
w_j'=(1-\varepsilon)(w_i+w_j),
$$
dove $\varepsilon$ e' casuale uniforme in $[0,1]$.

Una versione con saving propensity $\lambda$ e':
$$
w_i'=\lambda w_i+\varepsilon(1-\lambda)(w_i+w_j),
$$
$$
w_j'=\lambda w_j+(1-\varepsilon)(1-\lambda)(w_i+w_j).
$$

### Osservabili da misurare

1. distribuzione della ricchezza;
2. coefficiente di Gini;
3. curva di Lorenz;
4. quota di ricchezza detenuta dal top $x\%$;
5. tempi di rilassamento verso lo stato stazionario.

### Schema del laboratorio

#### Laboratorio 1 -- Modello base conservativo

**Obiettivo**

Implementare la regola di scambio elementare e osservare la distribuzione stazionaria.

**Attivita'**

1. inizializzare tutti gli agenti con la stessa ricchezza;
2. simulare molti scambi;
3. costruire l'istogramma finale.

#### Laboratorio 2 -- Saving propensity

**Obiettivo**

Studiare come il risparmio modifichi la distribuzione e la disuguaglianza.

**Attivita'**

1. introdurre $\lambda$;
2. variare $\lambda$;
3. misurare il Gini finale.

#### Laboratorio 3 -- Eterogeneita' individuale

**Obiettivo**

Studiare l'effetto di saving propensity diversa tra agenti.

**Attivita'**

1. assegnare $\lambda_i$ casuali;
2. simulare la dinamica;
3. confrontare le code della distribuzione.

### Estensioni naturali

1. tassazione e redistribuzione;
2. reddito da lavoro o rendimento del capitale;
3. interazioni su rete;
4. mobilita' sociale e matrici di transizione.

---

## Progetto 9 -- Assembly stocastico del microbioma

### Idea generale

Questo progetto introduce un modello stocastico di comunità microbica in cui specie diverse competono per stabilirsi, sopravvivere e colonizzare un ambiente. L'obiettivo e' studiare come rumore demografico, immigrazione e competizione influenzino composizione e stabilita' della comunità.

### Variabili di stato

Consideriamo $S$ specie e indichiamo con
$$
n_i(t)
$$
l'abbondanza della specie $i$ al tempo $t$.

Lo stato del sistema e' il vettore
$$
n(t)=(n_1(t),\dots,n_S(t)).
$$

### Dinamica stocastica

Una versione elementare puo' includere per ogni specie:

1. nascita con tasso $b_i n_i$;
2. morte con tasso $d_i n_i$;
3. immigrazione con tasso $m_i$;
4. competizione che aumenta il tasso di morte al crescere delle altre specie.

Ad esempio:
$$
d_i^{\mathrm{eff}}(t)=d_i+\sum_{j=1}^S \alpha_{ij} n_j(t).
$$

La simulazione puo' essere realizzata con Gillespie o con aggiornamenti discreti.

### Osservabili da misurare

1. ricchezza specifica, cioe' numero di specie presenti;
2. abbondanze relative;
3. diversita' di Shannon;
4. probabilita' di dominanza di una specie;
5. dipendenza dalle condizioni iniziali.

### Schema del laboratorio

#### Laboratorio 1 -- Colonizzazione e estinzione

**Obiettivo**

Studiare l'effetto combinato di immigrazione e rumore demografico.

**Attivita'**

1. scegliere pochi taxa;
2. fissare tassi di nascita, morte e immigrazione;
3. simulare molte traiettorie;
4. confrontare la composizione finale.

#### Laboratorio 2 -- Competizione interspecifica

**Obiettivo**

Studiare come la matrice $\alpha_{ij}$ modifichi la struttura della comunità.

**Attivita'**

1. introdurre competizione simmetrica o asimmetrica;
2. variare l'intensita' della competizione;
3. osservare ricchezza e dominanza.

#### Laboratorio 3 -- Priority effects

**Obiettivo**

Studiare la dipendenza dall'ordine di arrivo delle specie.

**Attivita'**

1. usare le stesse specie in ordini di colonizzazione diversi;
2. confrontare le comunità finali;
3. discutere la dipendenza dalla storia.

### Estensioni naturali

1. interazioni mutualistiche;
2. specie rare e invasione;
3. comunità su patch multiple;
4. antibiotici come shock esterno.

---

## Progetto 10 -- Traffico veicolare con cellular automata

### Idea generale

Questo progetto studia il traffico stradale con modelli a celle discrete. Ogni veicolo occupa una posizione su una griglia unidimensionale e aggiorna velocita' e posizione secondo regole locali con una componente casuale.

Il caso di studio mostra come semplici interazioni locali possano generare congestione, onde di stop-and-go e transizioni di fase tra traffico libero e traffico congestionato.

### Variabili di stato

Consideriamo una strada discretizzata in celle.

Per ogni veicolo $i$:
- posizione $x_i(t)$;
- velocita' discreta
  $$
  v_i(t)\in\{0,1,\dots,v_{\max}\}.
  $$

### Dinamica stocastica

Nel modello di Nagel--Schreckenberg, a ogni passo si applicano:

1. **accelerazione**
   $$
   v_i \leftarrow \min(v_i+1,v_{\max});
   $$
2. **adattamento alla distanza**
   se il gap davanti e' $g_i$, allora
   $$
   v_i \leftarrow \min(v_i,g_i);
   $$
3. **rallentamento casuale**
   con probabilita' $p$,
   $$
   v_i \leftarrow \max(v_i-1,0);
   $$
4. **avanzamento**
   $$
   x_i \leftarrow x_i+v_i.
   $$

### Osservabili da misurare

1. flusso medio di traffico;
2. velocita' media;
3. diagramma fondamentale flusso--densita';
4. distribuzione delle dimensioni degli ingorghi;
5. tempi di percorrenza.

### Schema del laboratorio

#### Laboratorio 1 -- Implementazione del modello base

**Obiettivo**

Simulare il traffico su una strada circolare e osservare la formazione di ingorghi.

**Attivita'**

1. fissare densita' e $v_{\max}$;
2. inizializzare i veicoli;
3. simulare la dinamica;
4. rappresentare il diagramma spazio--tempo.

#### Laboratorio 2 -- Effetto del rumore

**Obiettivo**

Studiare il ruolo del parametro di rallentamento casuale $p$.

**Attivita'**

1. variare $p$;
2. misurare velocita' media e flusso;
3. osservare quando emergono onde di congestione.

#### Laboratorio 3 -- Diagramma fondamentale

**Obiettivo**

Costruire la relazione tra densita' e flusso.

**Attivita'**

1. variare la densita' di veicoli;
2. simulare il sistema per tempi lunghi;
3. stimare il flusso medio in ogni regime.

### Estensioni naturali

1. corsie multiple;
2. semafori o incroci;
3. veicoli eterogenei;
4. ingresso e uscita da rampe.

---