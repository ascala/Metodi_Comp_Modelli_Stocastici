---
title: "07: Modelli di crescita e branching"
author: "Antonio Scala"
date: ""
---

Nei modelli deterministici di crescita siamo abituati a descrivere l’evoluzione di una quantità macroscopica tramite una traiettoria ben definita. Se il tasso di crescita è positivo, la popolazione aumenta; se è negativo, diminuisce; se esiste una soglia, essa separa regimi qualitativamente differenti. Nei processi di branching il punto di vista cambia. Non studiamo più una sola traiettoria media, ma una famiglia di realizzazioni possibili generate da una legge microscopica di riproduzione. In questo contesto due sistemi preparati nello stesso modo possono avere esiti completamente diversi: uno può estinguersi rapidamente, un altro può crescere senza controllo.

Questa differenza non è un dettaglio secondario, ma il cuore stesso del problema. Nei processi di branching la domanda fondamentale non è soltanto come cresce la media, ma se il processo sopravvive oppure si estingue, e con quale probabilità. Vedremo che il numero medio di discendenti per individuo è un parametro importante, ma non basta a descrivere il comportamento reale del sistema. Conta la distribuzione completa del numero di discendenti, e compare naturalmente una nuova quantità di interesse: la probabilità di estinzione.

I processi di branching sono importanti in molti contesti: genealogie, popolazioni biologiche, diffusione iniziale di epidemie, propagazione di innovazioni, cascades su reti. In tutti questi casi il problema ha una struttura comune: un’unità elementare può generare un numero casuale di unità della generazione successiva, e il destino del processo dipende dall’interazione tra crescita media e fluttuazioni.

## Obiettivi didattici specifici

Al termine della lezione lo studente dovrebbe essere in grado di:

1. distinguere tra crescita media e sopravvivenza di un processo;

2. definire un processo di branching di Galton--Watson;

3. calcolare e interpretare il numero medio di discendenti per individuo;

4. riconoscere i regimi subcritico, critico e supercritico;

5. comprendere perché una media crescente non implica sopravvivenza certa;

6. introdurre la probabilità di estinzione come soluzione di un problema ai punti fissi;

7. usare la funzione generatrice per descrivere la distribuzione del numero di discendenti;

8. discutere qualitativamente i tempi di estinzione;

9. riconoscere alcune applicazioni tipiche del branching.

## 1. Dal modello di crescita alla domanda giusta

Consideriamo una popolazione in cui ciascun individuo può dare origine a nuovi individui. In un modello deterministico si tende a descrivere il numero totale di individui con una variabile continua $N(t)$ che soddisfa una legge del tipo

$$
\frac{dN}{dt} = rN.
$$

Se $r>0$, la soluzione cresce esponenzialmente; se $r<0$, decade. Questo linguaggio è utile quando vogliamo descrivere il comportamento medio di un sistema grande, ma trascura la variabilità intrinseca dei processi riproduttivi elementari.

Se invece partiamo da pochi individui, oppure se vogliamo capire la sorte di una singola linea di discendenza, il punto di vista deterministico diventa inadeguato. Supponiamo di partire da un solo individuo. Anche se, in media, ogni individuo produce più di un discendente, può comunque accadere che il primo non ne produca nessuno, oppure che le prime generazioni si spengano per fluttuazione. Al contrario, una singola realizzazione fortunata può crescere molto rapidamente.

La domanda naturale non è allora soltanto quanto vale il tasso medio di crescita, ma:

> il processo sopravvive oppure si estingue?

Questa è la domanda caratteristica dei processi di branching. La quantità da studiare non è solo il numero medio di individui, ma la distribuzione degli esiti possibili e, in particolare, la probabilità che il processo raggiunga lo stato estinto.

## 2. Il processo di Galton--Watson

Il modello classico per formalizzare queste idee è il processo di Galton--Watson. Il tempo è discreto e scandito in generazioni:

$$
t = 0,1,2,\dots
$$

Indichiamo con $N_t$ il numero di individui presenti alla generazione $t$. Ogni individuo produce un numero casuale di discendenti, indipendentemente dagli altri e con la stessa distribuzione di probabilità. Se chiamiamo $K$ il numero di figli di un individuo, la legge di riproduzione è descritta da

$$
P(K=k)=p_k, \qquad k=0,1,2,\dots,
$$

con

$$
\sum_{k=0}^{\infty} p_k = 1.
$$

Se alla generazione $t$ ci sono $N_t$ individui, e il numero di figli dell’individuo $i$ è $K_i$, allora il numero di individui della generazione successiva è

$$
N_{t+1} = \sum_{i=1}^{N_t} K_i.
$$

Questa formula definisce completamente il processo.

### 2.1 Ipotesi del modello

Le ipotesi sono semplici:

1. il tempo è discreto per generazioni;

2. gli individui sono indipendenti dal punto di vista riproduttivo;

3. tutti gli individui hanno la stessa distribuzione di offspring.

Il modello non include interazioni, competizione o memoria esplicita tra generazioni. Proprio per questo è un laboratorio teorico ideale: permette di isolare con chiarezza il ruolo della casualità riproduttiva.

### 2.2 Stato assorbente

Se a una certa generazione la popolazione diventa nulla, allora non esistono più individui in grado di produrre discendenti. Quindi

$$
N_t=0 \quad \Longrightarrow \quad N_{t+1}=0.
$$

Lo stato $0$ è dunque uno stato assorbente. Tutta la teoria dell’estinzione ruota attorno alla probabilità di raggiungere questo stato.

## 3. Primo momento e soglia media

Il primo parametro da introdurre è il numero medio di discendenti per individuo:

$$
m = \mathbb{E}[K] = \sum_{k=0}^{\infty} k p_k.
$$

Questo parametro controlla il comportamento della media della popolazione. Infatti, condizionando su $N_t$, abbiamo

$$
\mathbb{E}[N_{t+1} \mid N_t]
= \mathbb{E}\left[\sum_{i=1}^{N_t} K_i \middle| N_t\right]
= \sum_{i=1}^{N_t} \mathbb{E}[K_i]
= mN_t\;.
$$

Passando al valore atteso non condizionato,

$$
\mathbb{E}[N_{t+1}] = m \cdot \mathbb{E}[N_t]\;.
$$

Per ricorrenza,

$$
\mathbb{E}[N_t] = N_0 m^t\;.
$$

Questa formula suggerisce una classificazione in tre regimi:

* **subcritico** se $m<1$;

* **critico** se $m=1$;

* **supercritico** se $m>1$.

Se ci fermassimo qui, penseremmo che:

* per $m<1$ il processo decresce;

* per $m=1$ resta in equilibrio;

* per $m>1$ cresce.

Ma questa interpretazione, pur corretta per la media, è incompleta e talvolta fuorviante. La media descrive il comportamento d’ensemble, non quello di una singola realizzazione.

## 4. Perché la media non basta

Per capire il limite del primo momento, confrontiamo due distribuzioni diverse con la stessa media.

### Caso A

$$
P(K=1)=1\;.
$$

In questo caso ogni individuo produce esattamente un figlio. Se partiamo da un individuo, allora

$$
N_t=1 \qquad \text{per ogni } t.
$$

La media è $m=1$, ma il processo non si estingue mai e non presenta fluttuazioni.

### Caso B

$$
P(K=0)=\frac12, \qquad P(K=2)=\frac12\,.
$$

Anche qui la media vale

$$
m = 0\cdot \frac12 + 2\cdot \frac12 = 1\;.
$$

Tuttavia il comportamento è del tutto diverso. Una realizzazione può estinguersi subito, oppure continuare per qualche generazione, oppure crescere notevolmente. Il processo presenta forti fluttuazioni e l’estinzione è possibile.

I due casi hanno la stessa media, ma una dinamica qualitativamente differente. Questo mostra che il solo valore di $m$ non basta. Occorre studiare l’intera distribuzione del numero di discendenti.

Questa è una delle idee centrali della lezione:

> la crescita media e la sopravvivenza di una realizzazione sono concetti distinti.

## 5. La funzione generatrice della distribuzione di offspring

Per descrivere l’intera distribuzione di $K$ si introduce la funzione generatrice

$$
G(s) = \mathbb{E}[s^K] = \sum_{k=0}^{\infty} p_k s^k\;.
$$

Questa funzione contiene tutta l’informazione sulla legge di riproduzione. In particolare:

$$
G(1)=1\;,
$$

$$
G(0)=p_0\;,
$$

e, derivando,

$$
G'(1)=\sum_{k=0}^{\infty} k p_k = m\;.
$$

Quindi il numero medio di discendenti è la derivata della generatrice nel punto $1$.

La funzione generatrice è utile perché permette di trattare in modo compatto somme di variabili indipendenti. Questo è esattamente ciò che accade nel processo di branching, poiché la popolazione della generazione successiva è somma dei figli prodotti dagli individui della generazione corrente.

Se definiamo la funzione generatrice di $N_t$ come

$$
F_t(s)=\mathbb{E}[s^{N_t}]\;,
$$

allora si ottiene la relazione

$$
F_{t+1}(s)=F_t(G(s))\;.
$$

Deriviamo questa relazione esplicitamente. Per definizione,

$$
F_{t+1}(s) = \mathbb{E}[s^{N_{t+1}}]\;.
$$

Condizioniamo su $N_t = n$: se alla generazione $t$ ci sono $n$ individui, ognuno produce indipendentemente un numero di figli con funzione generatrice $G(s)$, e $N_{t+1}$ è la somma di $n$ variabili indipendenti con quella stessa distribuzione. La funzione generatrice di una somma di $n$ variabili indipendenti e identicamente distribuite è la $n$-esima potenza della funzione generatrice del singolo termine, quindi

$$
\mathbb{E}[s^{N_{t+1}} \mid N_t = n] = [G(s)]^n\;.
$$

Rimuovendo il condizionamento,

$$
F_{t+1}(s)
= \mathbb{E}\!\left[[G(s)]^{N_t}\right]
= F_t(G(s))\;.
$$

Nel caso iniziale più semplice, con un solo progenitore,

$$
N_0=1\;,
$$

si ha

$$
F_0(s)=s\;,
$$

e quindi

$$
F_t(s)=G^{\circ t}(s)\;,
$$

dove $G^{\circ t}$ indica l’iterata $t$-esima di $G$.

Questa struttura iterativa sarà fondamentale per lo studio dell’estinzione.

## 6. Probabilità di estinzione

Definiamo la probabilità di estinzione finale partendo da un solo individuo:

$$
q = P(\,\exists t : N_t=0 \mid N_0=1)\;.
$$

Vogliamo trovare un’equazione che determini $q$.

Supponiamo che il primo individuo produca esattamente $k$ figli. Perché l’intero processo si estingua, devono estinguersi tutte e $k$ le linee di discendenza generate da questi figli. Se la probabilità di estinzione di una singola linea è $q$, allora, per indipendenza, la probabilità di estinzione totale condizionata a $K=k$ è

$$
q^k\;.
$$

Mediando rispetto alla distribuzione di $K$, otteniamo

$$
q = \sum_{k=0}^{\infty} p_k q^k\;.
$$

Ma il membro di destra è proprio $G(q)$. Dunque la probabilità di estinzione soddisfa l’equazione ai punti fissi

$$
q = G(q)\;.
$$

Questa è l’equazione fondamentale del branching elementare.

### 6.1 Interpretazione geometrica

L’equazione $q=G(q)$ si può leggere come intersezione tra la curva $y=G(s)$ e la retta $y=s$ nel segmento $[0,1]$.

Poiché $G(1)=1$, il punto $s=1$ è sempre una soluzione. La domanda è se esista anche un’altra soluzione in $[0,1)$.

Per rispondere occorre osservare che $G(s)$ è convessa su $[0,1]$. Infatti

$$
G''(s) = \sum_{k=2}^{\infty} k(k-1)\,p_k\,s^{k-2} \ge 0\;,
$$

poiché tutti i coefficienti $p_k$ sono non negativi. Inoltre $G(0)=p_0\ge 0$.
La curva è quindi convessa, parte da $p_0$ nell’origine e arriva a $1$ nel punto $s=1$.
Se la pendenza in $s=1$ vale $m = G'(1) \le 1$, la curva arriva a $1$ da sotto (o tangenzialmente), e non interseca la retta $y=s$ in nessun punto di $[0,1)$. Se invece $m>1$, la curva arriva a $1$ con pendenza maggiore di $1$, e la convessità garantisce che esiste esattamente un’altra intersezione con la retta in $[0,1)$.

Il comportamento è dunque controllato dalla pendenza nel punto $1$:

$$
G'(1)=m\;.
$$

Questo porta al risultato qualitativo fondamentale:

* se $m\le 1$, allora l’estinzione è certa e
  $$
  q=1\;;
  $$

* se $m>1$, allora esiste una soluzione con
  $$
  0<q<1\;,
  $$
  che rappresenta la probabilità di estinzione.

Quindi nel regime supercritico l’estinzione non è impossibile: è soltanto non certa.

## 7. I tre regimi: subcritico, critico, supercritico

Possiamo ora reinterpretare i tre regimi in modo corretto, andando oltre la sola media.

### 7.1 Regime subcritico: $m<1$

Quando il numero medio di discendenti è inferiore a $1$, la popolazione tende a contrarsi. In questo caso:

* la media decresce;

* l’estinzione è certa;

* i tempi tipici di sopravvivenza restano limitati.

Dal punto di vista intuitivo, ogni generazione è troppo piccola, in media, per compensare le perdite della precedente.

### 7.2 Regime critico: $m=1$

Questo è il caso più sottile. La media resta costante:

$$
\mathbb{E}[N_t]=N_0\;.
$$

Ma ciò non significa affatto che la popolazione resti stabilmente vicina al valore iniziale. In realtà:

* l’estinzione è ancora certa;

* la varianza cresce;

* le fluttuazioni dominano il comportamento del processo.

Il caso critico non è quindi un equilibrio stabile nel senso deterministico. È un regime in cui molte realizzazioni si estinguono, mentre poche diventano molto grandi, e la media resta costante soltanto come compensazione statistica.

### 7.3 Regime supercritico: $m>1$

Nel regime supercritico la media cresce esponenzialmente, ma questo non implica sopravvivenza certa. Una parte delle realizzazioni si estingue comunque nelle prime generazioni; un’altra parte sopravvive e può crescere rapidamente. In questo caso:

* la sopravvivenza ha probabilità positiva;

* l’estinzione resta possibile;

* la media è fortemente influenzata dalle realizzazioni che crescono molto.

## 8. Tempi di estinzione

Oltre alla probabilità di estinzione, è naturale introdurre il **tempo di estinzione**

$$
T_{\mathrm{ext}} = \inf\{t \ge 0 : N_t = 0\}.
$$

Questa variabile aleatoria risponde a una domanda diversa: non se il processo si estingue, ma in quanto tempo lo fa.

Dal punto di vista qualitativo:

* nel regime subcritico l’estinzione è certa e avviene tipicamente in tempi relativamente brevi;

* nel regime critico l’estinzione è ancora certa, ma i tempi possono essere molto lunghi e molto dispersi;

* nel regime supercritico una parte delle realizzazioni si estingue, mentre un’altra sopravvive indefinitamente.

Questo chiarisce che probabilità di estinzione e tempo di estinzione sono osservabili distinte. Un processo può estinguersi quasi certamente, ma solo dopo tempi molto variabili.

### 8.1 Un caso esattamente calcolabile

Esiste un esempio molto semplice in cui la distribuzione del tempo di estinzione si calcola esplicitamente. Supponiamo che ogni individuo possa avere al più un figlio:

$$
P(K=0)=1-p\;, \qquad P(K=1)=p\;,
$$

con $0\le p<1$.

In questo caso, partendo da un solo individuo, il processo può soltanto:

* continuare con un solo individuo alla generazione successiva, con probabilità $p$;

* estinguersi, con probabilità $1-p$.

Quindi il tempo di estinzione ha distribuzione geometrica:

$$
P(T_{\mathrm{ext}}=t)=p^{t-1}(1-p), \qquad t=1,2,3,\dots
$$

Il suo valore medio è

$$
\mathbb{E}[T_{\mathrm{ext}}]=\frac{1}{1-p}\;.
$$

Questo esempio è utile perché mostra immediatamente che, anche in un caso semplice, il tempo medio di estinzione cresce quando il sistema si avvicina alla soglia critica $p\to 1^-$. In altre parole, estinguersi quasi certamente non significa estinguersi rapidamente.

## 9. Esempi analitici di probabilità di estinzione

### 9.1 Caso binario: zero o due figli

Consideriamo la distribuzione

$$
P(K=0)=1-p, \qquad P(K=2)=p\;.
$$

La funzione generatrice è

$$
G(s)=1-p+ps^2\;.
$$

L’equazione per la probabilità di estinzione è

$$
q = 1-p + pq^2.
$$

che ha sempre $q=1$ come soluzione, e un'altra

$$
q = \frac{1-p}{p}.
$$

La seconda soluzione è maggiore di uno per $p<1/2$ per cui non può rappresentare una probabilità. Notare che la media vale

$$
m = 2p\;.
$$

Quindi:

* se $p\le \frac12$, allora $m\le 1$ e la soluzione fisica è $q=1$;

* se $p>\frac12$, allora $m>1$ e compare una soluzione con $q<1$.

Questo esempio mostra in modo molto chiaro come la soglia su $m$ si traduca in comparsa di una probabilità di sopravvivenza positiva.

### 9.2 Caso a tre valori: zero, uno o due figli

Consideriamo ora

$$
P(K=0)=p_0, \qquad P(K=1)=p_1, \qquad P(K=2)=p_2\;,
$$

con

$$
p_0+p_1+p_2=1\;.
$$

La funzione generatrice è

$$
G(s)=p_0+p_1 s+p_2 s^2\;,
$$

la media è

$$
m = p_1 + 2p_2\;,
$$

e la probabilità di estinzione soddisfa

$$
q = p_0 + p_1 q + p_2 q^2\;.
$$

Il punto importante non è tanto la formula esplicita della soluzione, quanto il fatto che distribuzioni diverse con stessa media possono produrre probabilità di estinzione diverse. Ancora una volta, la media da sola non basta.

## 10. Applicazioni

### 10.1 Genealogie

Questo è il contesto storico originale. Una linea familiare può essere vista come un processo di branching in cui ciascun individuo produce un numero casuale di discendenti. La domanda centrale non è la crescita media della popolazione totale, ma se la linea sopravvive oppure no.

### 10.2 Epidemie nella fase iniziale

All’inizio di un’epidemia, quando il numero di suscettibili è ancora grande, ogni infetto può essere visto come origine di una linea di trasmissione quasi indipendente. Anche se il numero medio di casi secondari è maggiore di $1$, un focolaio iniziale può spegnersi per caso. Il branching è quindi una buona approssimazione della fase iniziale della diffusione.

### 10.3 Cascades su reti

In una rete, un nodo attivo può attivare un numero casuale di vicini. Almeno nella fase iniziale della propagazione, e in assenza di forti effetti di saturazione, il processo può essere approssimato da un branching. Questo vale per diffusione di informazione, guasti a cascata, contagio comportamentale.

### 10.4 Diffusione di innovazioni

Un adottante di una nuova tecnologia o di un nuovo comportamento può indurre un numero casuale di nuovi adottanti. Anche qui il successo della diffusione non dipende soltanto dalla crescita media, ma dalla dispersione delle prime traiettorie.

## 11. Messaggio finale

I processi di branching mostrano in modo particolarmente chiaro una differenza che ricorrerà spesso nello studio dei modelli stocastici: la differenza tra comportamento medio e comportamento realizzato. In un sistema deterministico, fissata la condizione iniziale, il futuro è unico. In un processo di branching, invece, la stessa legge microscopica può produrre estinzione rapida oppure crescita indefinita.

Per questa ragione il numero medio di discendenti non basta. Occorre studiare la distribuzione completa della riproduzione, introdurre la funzione generatrice e usare la probabilità di estinzione come nuova quantità fondamentale. Il risultato è una nozione di soglia profondamente probabilistica: sotto soglia l’estinzione è certa, sopra soglia la sopravvivenza diventa possibile ma non garantita.

Questo rende il branching uno dei primi esempi in cui la probabilità non entra come semplice perturbazione di una traiettoria media, ma come struttura essenziale del problema.
