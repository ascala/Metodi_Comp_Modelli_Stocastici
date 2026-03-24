---
title: "03 Metodi Markov Chain Monte Carlo (MCMC)"
author: "Antonio Scala"
date: ""
---

# Catene di Markov e metodi MCMC

Le catene di Markov costituiscono uno degli strumenti fondamentali della modellizzazione stocastica e della simulazione numerica. Esse descrivono sistemi che evolvono nel tempo secondo regole probabilistiche locali: il futuro dipende dallo stato presente, ma non dall’intera storia passata. Questa proprietà permette di costruire modelli dinamici molto generali, applicabili in fisica statistica, biologia, finanza quantitativa, teoria delle reti, inferenza bayesiana e apprendimento automatico.

Dal punto di vista computazionale, le catene di Markov diventano particolarmente importanti quando si vogliono campionare distribuzioni di probabilità complesse. Nei metodi Monte Carlo elementari, studiati nella lezione precedente, i campioni vengono generati in modo indipendente. In molti problemi reali, tuttavia, non è possibile generare direttamente campioni indipendenti dalla distribuzione desiderata. In questi casi si costruisce una catena di Markov la cui distribuzione stazionaria coincida con la distribuzione target: gli stati visitati dalla catena diventano allora campioni da utilizzare per stimare medie, integrali e osservabili.

L’algoritmo di Metropolis, e la sua generalizzazione Metropolis-Hastings, rappresentano il prototipo di questo approccio. Essi sono il nucleo dei metodi di Markov Chain Monte Carlo (MCMC): invece di campionare direttamente da $\pi(x)$, si progetta una dinamica artificiale che abbia $\pi(x)$ come distribuzione di equilibrio.

## Obiettivi didattici specifici

Al termine della lezione, lo studente dovrà essere in grado di:

- definire formalmente una catena di Markov a tempo discreto;
- interpretare il significato della matrice di transizione;
- distinguere tra irriducibilità, aperiodicità, ricorrenza, transienza ed ergodicità;
- comprendere il ruolo delle distribuzioni stazionarie;
- discutere il significato del bilancio dettagliato e della reversibilità;
- spiegare perché i metodi MCMC sono utili quando il campionamento diretto fallisce;
- derivare la regola di accettazione di Metropolis e di Metropolis-Hastings;
- confrontare Metropolis, Metropolis-Hastings e heat bath;
- riconoscere i principali problemi di efficienza nei metodi MCMC.

## Struttura della lezione

1. Processi stocastici discreti e definizione di catena di Markov.
2. Proprietà fondamentali delle catene di Markov.
3. Distribuzioni stazionarie, reversibilità e convergenza.
4. Metodi Monte Carlo basati su catene di Markov.
5. Algoritmo di Metropolis.
6. Algoritmo di Metropolis-Hastings.
7. Heat bath e Gibbs sampling.
8. Efficienza, autocorrelazione e limiti pratici.
9. Estensioni e collegamenti.
10. Esercizi.

---

# 1. Processi stocastici discreti e definizione di catena di Markov

Un processo stocastico è una successione di variabili aleatorie

$$
X_0, X_1, X_2, \dots
$$

che descrive l’evoluzione temporale di un sistema soggetto a casualità. Nel caso che ci interessa in questa lezione, il tempo è discreto e lo stato del sistema appartiene a un insieme finito o numerabile $\mathcal{S}$, detto spazio degli stati.

L’idea è semplice: a ogni istante il sistema si trova in uno stato, e al passo successivo può spostarsi in un altro stato con una certa probabilità. Se il sistema si trova nello stato $i$ al tempo $t$, la probabilità di trovarsi nello stato $j$ al tempo $t+1$ è data da

$$
P(X_{t+1}=j \mid X_t=i).
$$

Una catena di Markov è un processo stocastico in cui il futuro dipende solo dallo stato presente, e non dall’intera storia del sistema. Formalmente,

$$
P(X_{t+1}=j \mid X_t=i, X_{t-1}, \dots, X_0) =
P(X_{t+1}=j \mid X_t=i).
$$

Questa proprietà si chiama proprietà markoviana.

## 1.1 Interpretazione intuitiva

Dire che un processo è markoviano non significa che il sistema non abbia storia fisica. Significa piuttosto che, per prevedere statisticamente il prossimo passo, tutta l’informazione rilevante è già contenuta nello stato attuale. Lo stato presente funziona quindi come una descrizione sufficiente del passato.

In molti modelli questa ipotesi è naturale. Ad esempio:

- in un random walk su una rete, la posizione attuale del camminatore è sufficiente per determinare la prossima mossa;
- in un modello di popolazione semplice, il numero attuale di individui può bastare a determinare le probabilità di nascita o morte al passo successivo;
- in un algoritmo Monte Carlo, la configurazione attuale del sistema è sufficiente per proporre e accettare la prossima configurazione.

## 1.2 Matrice di transizione

Le probabilità di passaggio vengono raccolte in una matrice di transizione $P$, definita da

$$
P_{ij} = P(X_{t+1}=j \mid X_t=i).
$$

Gli elementi di $P$ soddisfano due proprietà fondamentali: $P_{ij} \ge 0$ e $\sum_j P_{ij} = 1$ per ogni $i$. Ogni riga rappresenta quindi una distribuzione di probabilità.

Se $\mu^{(t)}$ è il vettore riga che descrive la distribuzione del sistema al tempo $t$, allora l’evoluzione è data da

$$
\mu^{(t+1)} = \mu^{(t)} P.
$$

Iterando questa relazione,

$$
\mu^{(t)} = \mu^{(0)} P^t.
$$

Lo studio del comportamento a lungo termine della catena coincide quindi con lo studio delle potenze della matrice di transizione.

## 1.3 Esempio elementare: gioco vincita-perdita

Consideriamo un gioco in cui un giocatore può trovarsi in due stati:

- stato $0$: ha perso il turno precedente;
- stato $1$: ha vinto il turno precedente.

Supponiamo che la matrice di transizione sia

$$
P =
\begin{pmatrix}
0.6 & 0.4 \\
0.2 & 0.8
\end{pmatrix}.
$$

Questo significa che:

- se il giocatore ha perso, al turno successivo vince con probabilità $0.4$;
- se il giocatore ha vinto, al turno successivo perde con probabilità $0.2$.

Se inizialmente il giocatore parte certamente nello stato $0$, allora $\mu^{(0)} = (1,0)$; dopo un passo, $\mu^{(1)} = \mu^{(0)} P = (0.6,0.4)$; dopo due, $\mu^{(2)} = \mu^{(1)} P = \mu^{(0)} P^2$ ...

Il calcolo esplicito mostra che la distribuzione tende verso un equilibrio, che studieremo più avanti.

## 1.4 Un secondo esempio: random walk su tre stati

Consideriamo ora tre stati disposti linearmente, $\mathcal{S}=\{1,2,3\}$, con la seguente dinamica:

- dallo stato 1 si va sempre allo stato 2;
- dallo stato 3 si va sempre allo stato 2;
- dallo stato 2 si va a 1 o a 3 con probabilità uguale.

La matrice di transizione è

$$
P=
\begin{pmatrix}
0 & 1 & 0 \\
1/2 & 0 & 1/2 \\
0 & 1 & 0
\end{pmatrix}.
$$

Questa catena è utile per mostrare un punto importante: non basta poter visitare più stati, bisogna anche studiare la struttura temporale dei ritorni. In questo caso la catena oscilla tra il centro e i bordi, e dunque ha periodicità. Questo esempio mostrerà più avanti perché l’aperiodicità è una condizione importante per la convergenza.

# 2. Proprietà fondamentali delle catene di Markov

Per usare bene una catena di Markov non basta saper scrivere la matrice di transizione. Occorre capire quali proprietà qualitative determinano il comportamento a lungo termine della dinamica.

## 2.1 Matrice stocastica e rappresentazione come grafo

La matrice di transizione $P=(P_{ij})$ di una catena di Markov è una **matrice stocastica**: i suoi elementi sono non negativi e la somma degli elementi di ogni riga è uguale a 1,

$$
P_{ij} \ge 0, 
\qquad \sum_j P_{ij} = 1
\quad \text{per ogni } i.
$$

Questa condizione esprime il fatto che, fissato lo stato corrente $i$, le probabilità di transizione verso tutti gli stati possibili devono sommare a 1.

A ogni matrice di transizione si può associare un **grafo orientato**: i nodi rappresentano gli stati, e si disegna un arco $i \to j$ quando

$$
P_{ij} > 0.
$$

In questo linguaggio grafico molte proprietà della catena diventano immediatamente intuitive:

- l'esistenza di un cammino da $i$ a $j$ corrisponde alla possibilità di raggiungere $j$ partendo da $i$ in un numero finito di passi;
- l'irriducibilità corrisponde al fatto che il grafo sia fortemente connesso;
- la periodicità è legata alla struttura dei cicli del grafo;
- la presenza di un auto-arco $i \to i$ con $P_{ii}>0$ rende aperiodico lo stato $i$.

Nel caso particolare in cui tutti gli elementi della matrice siano strettamente positivi, cioè

$$
P_{ij} > 0
\qquad \text{per ogni } i,j,
$$

il grafo è completo orientato con auto-archi. In questo caso la catena è automaticamente irriducibile e aperiodica.

Dal punto di vista algebrico, ogni matrice stocastica possiede sempre almeno un autovalore uguale a 1. Inoltre, tutti gli autovalori $\lambda$ soddisfano

$$
|\lambda| \le 1.
$$

La distribuzione stazionaria $\pi$, quando esiste, soddisfa

$$
\pi = \pi P,
$$

e quindi è un autovettore sinistro associato all'autovalore 1.

Nel caso di una catena **finita**, **irriducibile** e **aperiodica**, l'autovalore 1 è semplice e tutti gli altri autovalori soddisfano

$$
|\lambda| < 1.
$$

Questa caratterizzazione spettrale è la controparte algebrica dell'ergodicità: le potenze $P^t$ sopprimono progressivamente i modi associati agli altri autovalori, e la distribuzione converge all'unica distribuzione stazionaria.

## 2.2 Comunicazione tra stati

Si dice che uno stato $j$ è **raggiungibile** da uno stato $i$ se esiste un intero $n \ge 1$ tale che

$$
(P^n)_{ij} > 0.
$$

In tal caso, partendo da $i$, esiste una probabilità positiva di trovarsi in $j$ dopo $n$ passi.

Se due stati sono reciprocamente raggiungibili, si dice che **comunicano**. La relazione di comunicazione suddivide lo spazio degli stati in classi di equivalenza, dette classi comunicanti.

Nel linguaggio dei grafi, due stati comunicano se esistono cammini orientati sia da $i$ a $j$ sia da $j$ a $i$.

## 2.3 Irriducibilità

Una catena si dice **irriducibile** se tutti gli stati comunicano tra loro. In una catena irriducibile non esistono regioni dello spazio degli stati isolate dal resto.

Dal punto di vista grafico, ciò significa che il grafo associato è fortemente connesso: da ogni nodo si può raggiungere ogni altro nodo attraverso un cammino orientato.

Per i metodi MCMC questa proprietà è essenziale. Se la catena non è irriducibile, essa non può esplorare tutto lo spazio su cui la distribuzione target è definita, e il campionamento risulta scorretto o parziale.

Nel caso del gioco a due stati, la catena è irriducibile se entrambe le probabilità di cambio stato sono positive.

## 2.4 Periodicità e aperiodicità

Uno stato $i$ ha **periodo** $d$ se i ritorni possibili in $i$ avvengono solo a tempi multipli di $d$, e $d$ è il massimo intero con questa proprietà. Formalmente,

$$
d(i) = \gcd \{ n \ge 1 : (P^n)_{ii} > 0 \}.
$$

Se $d(i)=1$, lo stato è **aperiodico**.

In una catena irriducibile tutti gli stati hanno lo stesso periodo, quindi si può parlare del periodo della catena nel suo complesso.

Dal punto di vista intuitivo, una catena periodica è costretta a muoversi secondo un ritmo rigido: certi stati possono essere visitati solo a tempi appartenenti a determinate classi modulari. Questo ostacola una convergenza regolare della distribuzione nel tempo.

Un criterio semplice ma molto utile è il seguente: se una catena irriducibile contiene almeno uno stato con

$$
P_{ii} > 0,
$$

allora l'intera catena è aperiodica. Infatti la possibilità di restare nello stesso stato spezza la rigidità dei cicli.

L'esempio del random walk su tre stati mostrato sopra ha periodo 2. Se il sistema parte dal centro, torna al centro solo dopo un numero pari di passi. Questa periodicità impedisce una convergenza regolare della distribuzione nel tempo, anche se una distribuzione stazionaria può comunque esistere.

## 2.5 Ricorrenza e transienza

Uno stato è **ricorrente** se, una volta lasciato, il sistema vi ritorna quasi certamente. È invece **transiente** se esiste una probabilità positiva di non ritornarvi mai.

La distinzione tra ricorrenza e transienza è particolarmente importante quando lo spazio degli stati è infinito. In quel caso alcune regioni possono essere visitate solo un numero finito di volte, mentre altre possono attrarre la dinamica in modo persistente.

Nel caso di catene finite e irriducibili, tutti gli stati sono ricorrenti positivi. Questo semplifica molto la teoria e garantisce l'esistenza di almeno una distribuzione stazionaria.

## 2.6 Ergodicità

Una catena finita, irriducibile e aperiodica è **ergodica**. In tal caso esiste un'unica distribuzione stazionaria $\pi$ e vale

$$
\mu^{(t)} \to \pi
\qquad \text{per } t \to \infty,
$$

qualunque sia la distribuzione iniziale $\mu^{(0)}$.

L'ergodicità garantisce quindi che il sistema dimentichi la condizione iniziale e che la statistica a lungo termine sia ben definita.

Dal punto di vista spettrale, l'ergodicità corrisponde al fatto che l'autovalore 1 domina il comportamento asintotico, mentre tutti gli altri contributi decadono con il numero di passi.

## 2.7 Perché queste proprietà contano in simulazione

Nel contesto Monte Carlo, vogliamo che la catena:

- possa visitare tutte le configurazioni rilevanti;
- non resti intrappolata in cicli rigidi;
- converga a un'unica distribuzione di equilibrio.

Queste richieste corrispondono precisamente a irriducibilità, aperiodicità ed ergodicità.

Per questo motivo, quando si progetta un algoritmo MCMC, tali proprietà sono importanti quanto la correttezza formale del criterio di accettazione. Un algoritmo può infatti soddisfare il detailed balance rispetto a una certa distribuzione target, ma risultare inutile in pratica se la catena non esplora efficacemente lo spazio degli stati o se converge in modo troppo lento.

La rappresentazione tramite grafo e il punto di vista spettrale sono due strumenti complementari per analizzare questi aspetti: il grafo rende visibile la struttura delle transizioni, mentre gli autovalori della matrice di transizione descrivono la velocità con cui la catena perde memoria della condizione iniziale.

# 3. Distribuzioni stazionarie, reversibilità e convergenza

## 3.1 Distribuzione stazionaria

Una distribuzione di probabilità $\pi$ si dice stazionaria per la catena se soddisfa

$$
\pi = \pi P.
$$

Equivalentemente,

$$
\pi_j = \sum_i \pi_i P_{ij}.
$$

Se il sistema parte distribuito secondo $\pi$, allora resta distribuito secondo $\pi$ a ogni passo successivo. La distribuzione stazionaria descrive quindi l’*equilibrio statistico della catena*.

## 3.2 Esempio esplicito

Riprendiamo il gioco a due stati, con

$$
P =
\begin{pmatrix}
0.6 & 0.4 \\
0.2 & 0.8
\end{pmatrix}.
$$

Cerchiamo $\pi=(\pi_0,\pi_1)$ tale che $\pi = \pi P$. Le equazioni sono $\pi_0 = 0.6\,\pi_0 + 0.2\,\pi_1$ e $\pi_1 = 0.4\,\pi_0 + 0.8\,\pi_1$, insieme al vincolo di normalizzazione $\pi_0 + \pi_1 = 1$. Dalla prima si ricava $0.4\,\pi_0 = 0.2\,\pi_1$, cioè $\pi_1 = 2\pi_0$. Sostituendo nella normalizzazione si ottiene $3\pi_0=1$, quindi

$$
\pi_0 = \frac{1}{3}, \qquad \pi_1 = \frac{2}{3}.
$$

Questa è la distribuzione di equilibrio della catena. Potete vericare  numericamente che

$$
\lim_{t\to\infty} P^t =
\begin{pmatrix}
1/3 & 2/3 \\
1/3 & 2/3
\end{pmatrix}\,;
$$
in generale, $P^t$ tenderà sempre (se è finita, irriducibile e aperiodica) ad una matrice le cui righe sono esattamente $\pi$.

## 3.3 Bilancio globale

La relazione

$$
\pi_j = \sum_i \pi_i P_{ij}
$$

esprime il fatto che, in equilibrio, la probabilità totale che entra nello stato $j$ coincide con la probabilità che ne esce. Si parla di bilancio globale.

Questa è la condizione minima necessaria per la stazionarietà.

## 3.4 Bilancio dettagliato

Una condizione più forte è il bilancio dettagliato:

$$
\pi_i P_{ij} = \pi_j P_{ji}
\qquad \text{per ogni } i,j.
$$

Questa condizione implica la stazionarietà, ma non è equivalente a essa in generale.

Il significato è il seguente: in equilibrio, il flusso medio di probabilità che va da $i$ a $j$ è uguale al flusso medio da $j$ a $i$.

È importante sottolineare che il bilancio dettagliato non implica che $i$ e $j$ siano equiprobabili. Le probabilità $\pi_i$ e $\pi_j$ possono essere molto diverse; ciò che si bilancia sono i flussi, non le occupazioni dei singoli stati.

## 3.5 Reversibilità

Se una catena soddisfa il bilancio dettagliato rispetto a $\pi$, si dice reversibile rispetto a $\pi$.

La reversibilità è molto utile in fisica statistica e nei metodi Monte Carlo perché fornisce un criterio semplice per costruire dinamiche corrette. Gli algoritmi di Metropolis e Metropolis-Hastings sono progettati precisamente in modo da soddisfare questa proprietà.

## 3.6 Significato e interpretazioni

Il concetto di reversibilità ha significato concreto in ambiti molto diversi.

In fisica statistica, la distribuzione di equilibrio canonica ha la forma $\pi(x) \propto e^{-\beta E(x)}$, dove $E(x)$ è l'energia della configurazione e $\beta=1/T$. Una dinamica reversibile rispetto a $\pi$ realizza un equilibrio microscopico: il sistema continua a muoversi nello spazio delle configurazioni, ma non c'è corrente netta di probabilità tra coppie di stati. Le configurazioni a energia più bassa restano comunque più probabili di quelle a energia più alta.

In statistica bayesiana, la distribuzione target è la distribuzione a posteriori $\pi(\theta \mid y) \propto L(y \mid \theta)\,p(\theta)$, dove $L$ è la verosimiglianza e $p(\theta)$ il prior. La costante di normalizzazione — l'evidenza marginale — è spesso intrattabile, ma i metodi MCMC richiedono solo rapporti tra densità, nei quali essa si cancella. Una dinamica reversibile rispetto a $\pi(\theta \mid y)$ permette quindi di campionare la distribuzione a posteriori senza mai calcolarla esplicitamente.

## 3.7 Convergenza all’equilibrio

Se la catena è ergodica, allora la distribuzione al tempo $t$ converge a $\pi$. Questo significa che, per $t$ grande, la statistica degli stati visitati lungo la traiettoria si avvicina alla statistica imposta dalla distribuzione stazionaria.

Questo è il principio matematico alla base dei metodi MCMC.

# 4. Metodi Monte Carlo basati su catene di Markov

## 4.1 Motivazione

Supponiamo di voler calcolare una media rispetto a una distribuzione target $\pi(x)$:

$$
\langle A \rangle_\pi = \sum_x A(x)\pi(x)
$$

oppure, nel caso continuo,

$$
\langle A \rangle_\pi = \int A(x)\pi(x)\,dx.
$$

Se non sappiamo generare campioni indipendenti da $\pi$, possiamo costruire una catena di Markov che abbia $\pi$ come distribuzione stazionaria.

## 4.2 Distribuzioni note solo a meno di una costante

Molto spesso la distribuzione target è nota solo nella forma

$$
\pi(x) = \frac{1}{Z} \tilde{\pi}(x),
$$

dove $\tilde{\pi}(x)$ è calcolabile, mentre $Z$ non lo è.

In fisica statistica, $Z$ è la funzione di partizione. In statistica e in machine learning, lo stesso oggetto viene spesso chiamato costante di normalizzazione. Nei problemi bayesiani può coincidere con l’evidenza marginale.

Gli algoritmi MCMC sono utili proprio perché richiedono spesso solo rapporti tra densità non normalizzate, nei quali $Z$ si cancella.

## 4.3 Stima tramite medie temporali

Se $\{X_t\}$ è una catena ergodica con distribuzione stazionaria $\pi$, allora per un’osservabile $A$ vale il principio ergodico:

$$
\frac{1}{N}\sum_{t=1}^N A(X_t) \to \langle A \rangle_\pi
\qquad \text{per } N \to \infty.
$$

Le medie temporali lungo una singola traiettoria diventano quindi stime delle medie teoriche rispetto a $\pi$.

## 4.4 Burn-in

Poiché la catena parte da una configurazione arbitraria, i primi passi risentono della condizione iniziale. Questa fase viene chiamata burn-in o termalizzazione. In pratica, una parte iniziale della traiettoria viene scartata prima di iniziare la misura delle osservabili.

## 4.5 Campioni correlati

A differenza del Monte Carlo con campioni indipendenti, nei metodi MCMC i campioni successivi sono correlati. Questa correlazione riduce l’efficienza statistica: il numero effettivo di campioni indipendenti è minore del numero totale di passi simulati.

Di conseguenza, oltre alla correttezza teorica della distribuzione stazionaria, conta anche la velocità con cui la catena esplora lo spazio degli stati.

# 5. Algoritmo di Metropolis

## 5.1 Struttura generale

Supponiamo di voler campionare una distribuzione target $\pi(x)$ su uno spazio degli stati discreto o continuo. L’algoritmo di Metropolis si basa su due ingredienti:

- una proposta di nuova configurazione $x'$ a partire da quella corrente $x$;
- una regola di accettazione o rifiuto.

Nel caso classico, la proposta è simmetrica:

$$
q(x' \mid x) = q(x \mid x').
$$

## 5.2 Regola di accettazione

Una volta proposta $x'$, si accetta la mossa con probabilità

$$
A(x \to x') =
\min\left(1,\frac{\pi(x')}{\pi(x)}\right).
$$

Se la mossa è accettata, si pone $X_{t+1}=x'$; se è rifiutata, si resta nello stato corrente: $X_{t+1}=x$.

## 5.3 Interpretazione della regola

La logica della regola è molto chiara:

- se $x'$ è più probabile di $x$, allora la mossa viene sempre accettata;
- se $x'$ è meno probabile di $x$, allora può essere accettata con una probabilità positiva.

Questo permette al sistema di muoversi verso configurazioni favorevoli, ma anche di uscire da minimi locali e di esplorare lo spazio in modo non puramente deterministico.

## 5.4 Caso di Boltzmann

Se la distribuzione target è della forma $\pi(x) \propto e^{-\beta E(x)}$, allora $\pi(x')/\pi(x) = e^{-\beta (E(x')-E(x))}$ e la probabilità di accettazione diventa

$$
A(x \to x') = \min\left(1,\,e^{-\beta (E(x')-E(x))}\right).
$$

Configurazioni a energia più bassa sono sempre accettate, mentre configurazioni a energia più alta sono accettate con probabilità esponenzialmente decrescente.

## 5.5 Dimostrazione del detailed balance

Per $x \ne x'$, il kernel di transizione della catena è $P(x \to x') = q(x' \mid x) A(x \to x')$. Moltiplicando per $\pi(x)$,

$$
\pi(x) P(x \to x') =
\pi(x) q(x' \mid x) \min\left(1,\frac{\pi(x')}{\pi(x)}\right).
$$

Poiché la proposta è simmetrica, $q(x' \mid x)=q(x \mid x')$, si può riscrivere

$$
\pi(x) P(x \to x') = q(x' \mid x)\min(\pi(x),\pi(x')).
$$

Questa espressione è simmetrica nello scambio $x \leftrightarrow x'$, quindi

$$
\pi(x) P(x \to x') = \pi(x') P(x' \to x).
$$

Il detailed balance è verificato, e dunque $\pi$ è stazionaria.

## 5.6 Esempio numerico semplice

Supponiamo di voler campionare tre stati con pesi non normalizzati

$$
\tilde{\pi}(1)=1, \qquad \tilde{\pi}(2)=3, \qquad \tilde{\pi}(3)=2.
$$

Usiamo una proposta simmetrica che da ogni stato propone uniformemente uno dei due rimanenti.

Se il sistema si trova in $1$ e propone $2$, il rapporto è

$$
\frac{\tilde{\pi}(2)}{\tilde{\pi}(1)} = 3,
$$

quindi la mossa è sempre accettata.

Se si trova in $2$ e propone $1$, il rapporto è

$$
\frac{\tilde{\pi}(1)}{\tilde{\pi}(2)} = \frac{1}{3},
$$

quindi la mossa viene accettata con probabilità $1/3$.

Si vede già da questo piccolo esempio che il sistema tende a trascorrere più tempo negli stati di peso maggiore.

## 5.7 Pseudocodice essenziale

```python
def metropolis_step(x):
    x_new = propose_symmetric(x)
    r = pi_tilde(x_new) / pi_tilde(x)
    alpha = min(1.0, r)
    if uniform_0_1() < alpha:
        return x_new
    else:
        return x
```

# 6. Algoritmo di Metropolis-Hastings

## 6.1 Perché serve una generalizzazione

In molti casi una proposta simmetrica non è naturale o non è efficiente. Si può voler proporre mosse direzionali, oppure usare una proposta che dipende in modo asimmetrico dallo stato corrente. In questi casi l’algoritmo di Metropolis non è più sufficiente.

Metropolis-Hastings corregge l’asimmetria della proposta introducendo un fattore aggiuntivo nel criterio di accettazione.

## 6.2 Regola generale

Se la proposta è $q(x' \mid x)$, la probabilità di accettazione è

$$
A(x \to x') =
\min\left(
1,
\frac{\pi(x') q(x \mid x')}{\pi(x) q(x' \mid x)}
\right).
$$

Se si lavora con densità non normalizzate,

$$
A(x \to x') =
\min\left(
1,
\frac{\tilde{\pi}(x') q(x \mid x')}{\tilde{\pi}(x) q(x' \mid x)}
\right).
$$

## 6.3 Derivazione del criterio

Vogliamo imporre il detailed balance:

$$
\pi(x) P(x \to x') = \pi(x') P(x' \to x).
$$

Per $x \ne x'$, si ha $P(x \to x') = q(x' \mid x) A(x \to x')$. Quindi vogliamo che

$$
\pi(x) q(x' \mid x) A(x \to x') = \pi(x') q(x \mid x') A(x' \to x).
$$

La scelta

$$
A(x \to x') =
\min\left(
1,
\frac{\pi(x') q(x \mid x')}{\pi(x) q(x' \mid x)}
\right)
$$

soddisfa esattamente questa condizione.

## 6.4 Verifica del detailed balance

Infatti,

$$
\pi(x) P(x \to x') = \pi(x) q(x' \mid x)
\min\left( 1,\frac{\pi(x') q(x \mid x')}{\pi(x) q(x' \mid x)} \right).
$$

Questa quantità si può riscrivere come

$$
\min\left( \pi(x) q(x' \mid x), \pi(x') q(x \mid x') \right),
$$

che è simmetrica in $x$ e $x'$. Segue dunque che

$$
\pi(x) P(x \to x') = \pi(x') P(x' \to x).
$$

## 6.5 Metropolis come caso particolare

Se la proposta è simmetrica, cioè $q(x' \mid x)=q(x \mid x')$, il rapporto delle proposte si semplifica e si recupera il criterio di Metropolis:

$$
A(x \to x')=
\min\left(1,\frac{\pi(x')}{\pi(x)}\right).
$$

## 6.6 Un esempio di proposta asimmetrica

Supponiamo di avere uno spazio discreto ordinato, e di costruire una proposta che favorisca il passo verso destra piuttosto che verso sinistra. Ad esempio,

$$
q(i+1 \mid i)=0.7, \qquad q(i-1 \mid i)=0.3.
$$

Senza correzione, questa proposta introdurrebbe un drift artificiale nella dinamica. Il fattore di Hastings compensa esattamente questo sbilanciamento, in modo che la distribuzione stazionaria finale rimanga quella desiderata.

## 6.7 Pseudocodice essenziale

```python
def metropolis_hastings_step(x):
    x_new = propose(x)
    r = pi_tilde(x_new) * q(x, x_new, reverse=True) / (pi_tilde(x) * q(x, x_new, reverse=False))
    alpha = min(1.0, r)
    if uniform_0_1() < alpha:
        return x_new
    else:
        return x
```

# 7. Heat bath e Gibbs sampling

## 7.1 Idea generale

Metropolis e Metropolis-Hastings funzionano proponendo una mossa e decidendo poi se accettarla o rifiutarla. In alcuni casi, però, si può fare qualcosa di più efficiente: aggiornare direttamente una parte del sistema campionandola dalla sua distribuzione condizionata esatta.

Questo approccio prende il nome di heat bath, e la sua forma più generale è nota come Gibbs sampling.

## 7.2 Aggiornamento condizionato

Supponiamo che la configurazione sia composta da molte variabili,

$$
x = (x_1, x_2, \dots, x_n).
$$

Scegliamo una componente, ad esempio $x_i$, e la aggiorniamo campionando da

$$
\pi(x_i \mid x_1,\dots,x_{i-1},x_{i+1},\dots,x_n).
$$

In questo modo il nuovo valore di $x_i$ è già distribuito correttamente rispetto alla legge condizionata, e non serve alcun rifiuto.

## 7.3 Perché l’accettazione è uguale a 1

Il punto chiave è che la proposta coincide con la distribuzione condizionata target. Di conseguenza, il bilancio dettagliato risulta automaticamente verificato, e ogni aggiornamento è accettato con probabilità 1.

## 7.4 Esempio qualitativo: spin Ising

In un modello di Ising, ogni spin $s_i$ può assumere valori $\pm 1$. Se si fissano gli spin vicini, la probabilità condizionata di $s_i$ dipende dal campo locale. L’aggiornamento heat bath consiste nel scegliere direttamente il nuovo valore di $s_i$ con la corretta probabilità condizionata.

Questo evita il rifiuto tipico del metodo di Metropolis.

## 7.5 Gibbs sampling

Il Gibbs sampling consiste nell’aggiornare ripetutamente, una alla volta, tutte le componenti di una configurazione campionando dalle loro distribuzioni condizionate complete.

È molto usato in statistica bayesiana, in modelli gerarchici, in grafi probabilistici e in fisica statistica.

## 7.6 Confronto con Metropolis

Metropolis ha il vantaggio della generalità: basta conoscere la distribuzione target a meno di costante e saper calcolare rapporti di probabilità.

Heat bath e Gibbs richiedono invece di conoscere e saper campionare esplicitamente le distribuzioni condizionate.

In sintesi:

* Metropolis è più generale;
* heat bath non ha rifiuti;
* Gibbs può essere molto efficiente se le condizionate sono semplici;
* Metropolis è spesso più facile da implementare in problemi complessi.

# 8. Efficienza, autocorrelazione e limiti pratici

La correttezza asintotica dell'algoritmo non basta. Una catena può essere
formalmente giusta ma esplorare lo spazio degli stati in modo molto lento.

## 8.1 Tasso di accettazione

Nel random walk Metropolis, se i passi proposti sono troppo piccoli, quasi
tutte le mosse vengono accettate ma la catena si muove lentamente nello
spazio degli stati. Se i passi sono troppo grandi, la maggior parte delle
proposte viene rifiutata e la catena rimane ferma.

L'efficienza dipende dal compromesso tra ampiezza delle mosse e tasso di
accettazione. In spazi continui, un tasso di accettazione intorno al 20–40%
è spesso un buon punto di partenza.

## 8.2 Autocorrelazione

Se definiamo un'osservabile lungo la traiettoria come

$$
A_t = A(X_t),
$$

la funzione di autocorrelazione è

$$
C(\tau) = \langle A_t A_{t+\tau} \rangle - \langle A \rangle^2.
$$

Un decadimento lento di $C(\tau)$ indica che la catena conserva memoria per
tempi lunghi e che i campioni sono fortemente correlati.

## 8.3 Tempo di autocorrelazione

Il tempo di autocorrelazione integrato

$$
\tau_{\mathrm{int}} = \frac{1}{2} \sum_{\tau=-\infty}^{+\infty}
\frac{C(\tau)}{C(0)}
$$

misura quanti passi sono necessari per ottenere l'equivalente di un nuovo
campione quasi indipendente. Il numero effettivo di campioni indipendenti
ottenibili da una traiettoria di $N$ passi è

$$
N_{\mathrm{eff}} = \frac{N}{\tau_{\mathrm{int}}} \ll N.
$$

Maggiore è $\tau_{\mathrm{int}}$, minore è l'efficienza statistica della
simulazione.

## 8.4 Termalizzazione insufficiente

Se si inizia a misurare troppo presto, prima che la catena abbia raggiunto
l'equilibrio, si introducono errori sistematici. Questo problema è
particolarmente grave quando la condizione iniziale è molto lontana dalla
regione tipica della distribuzione target.

## 8.5 Metastabilità e multimodalità

Quando la distribuzione target ha più modi separati da barriere elevate, la
catena può restare intrappolata a lungo in una sola regione dello spazio. In
questi casi i tempi di mixing possono diventare enormi, e la stima numerica
può risultare gravemente distorta pur in presenza di un algoritmo
formalmente corretto.

## 8.6 Diagnostica empirica

Nella pratica si controllano spesso:

* andamento temporale delle osservabili;
* stabilità delle medie cumulative;
* confronto tra catene inizializzate in punti diversi;
* autocorrelazioni empiriche;
* frequenza di accettazione.

Questi strumenti non sostituiscono la teoria, ma sono essenziali per
valutare l'affidabilità di una simulazione concreta.

# 9. Estensioni e collegamenti

## 9.1 Metropolis adattivo

Nei metodi adattivi, la proposta viene modificata durante la simulazione per adattarsi alla geometria empirica della distribuzione target. Questo può migliorare molto l’efficienza, ma richiede attenzione per non compromettere la convergenza asintotica.

## 9.2 Hamiltonian Monte Carlo

Nei problemi continui ad alta dimensionalità, il random walk diventa molto inefficiente. Hamiltonian Monte Carlo introduce variabili ausiliarie di momento e una dinamica quasi deterministica che consente di proporre mosse lunghe con alta probabilità di accettazione.

## 9.3 Simulated annealing

Se invece di campionare una distribuzione si vuole cercare un minimo globale, si può usare una dinamica di tipo Metropolis con temperatura progressivamente decrescente. Questo porta al metodo del simulated annealing, che verrà discusso più avanti nel corso.

## 9.4 Collegamento con modelli di spin e machine learning

Le dinamiche di Metropolis e heat bath sono centrali nella simulazione di modelli di spin, nelle Boltzmann machines e in molti modelli probabilistici usati in machine learning. Esse costituiscono quindi un ponte naturale tra fisica statistica, inferenza e computazione.

# 10. Esercizi

## 10.1 Esercizi di base

1. Considerare la catena a due stati con matrice

$$
P=
\begin{pmatrix}
1-p & p \\
q & 1-q
\end{pmatrix}.
$$

Determinare la distribuzione stazionaria in funzione di $p$ e $q$.

2. Verificare per quali valori di $p$ e $q$ la catena del punto precedente è irriducibile e aperiodica.

3. Per la catena su tre stati con matrice

$$
P=
\begin{pmatrix}
0 & 1 & 0 \\
1/2 & 0 & 1/2 \\
0 & 1 & 0
\end{pmatrix},
$$

mostrare che la catena è periodica.

## 10.2 Esercizi su Metropolis

4. Si consideri una distribuzione discreta con pesi non normalizzati

$$
\tilde{\pi}(1)=1,\qquad \tilde{\pi}(2)=4,\qquad \tilde{\pi}(3)=2.
$$

Costruire un algoritmo di Metropolis con proposta simmetrica uniforme tra stati distinti e calcolare le probabilità di accettazione per tutte le possibili mosse.

5. Dimostrare esplicitamente il detailed balance per l’algoritmo di Metropolis nel caso discreto.

## 10.3 Esercizi su Metropolis-Hastings

6. Considerare una proposta asimmetrica su stati interi, con probabilità di muoversi a destra uguale a $0.7$ e a sinistra uguale a $0.3$. Scrivere il rapporto di Hastings per una distribuzione target assegnata $\pi(i)$.

7. Mostrare che l’algoritmo di Metropolis si ottiene come caso particolare di Metropolis-Hastings quando la proposta è simmetrica.

## 10.4 Esercizi concettuali

8. Spiegare perché il bilancio dettagliato è sufficiente ma non necessario per la stazionarietà.

9. Discutere perché una catena con alta probabilità di accettazione non è necessariamente efficiente.

10. Confrontare vantaggi e svantaggi di Metropolis e heat bath in un modello di Ising.

# Conclusioni

Le catene di Markov forniscono un quadro matematico estremamente potente per descrivere sistemi stocastici e per costruire algoritmi di campionamento. La nozione di distribuzione stazionaria chiarisce cosa significhi equilibrio probabilistico; l’ergodicità spiega quando tale equilibrio venga effettivamente raggiunto; il bilancio dettagliato fornisce un principio costruttivo semplice per progettare dinamiche corrette.

L’algoritmo di Metropolis rappresenta la prima realizzazione concreta di questa idea. Metropolis-Hastings ne estende la portata a proposte asimmetriche, mentre heat bath e Gibbs mostrano che, in presenza di informazioni condizionate più ricche, si possono costruire aggiornamenti ancora più efficienti.

Dal punto di vista pratico, tuttavia, la correttezza teorica non basta: burn-in, autocorrelazione, metastabilità e scelta della proposta determinano la qualità reale di una simulazione. Per questo i metodi MCMC sono al tempo stesso uno strumento teorico e una tecnica computazionale raffinata.

# Riferimenti

* Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H., Teller, E. (1953). Equation of State Calculations by Fast Computing Machines.
* Hastings, W. K. (1970). Monte Carlo Sampling Methods Using Markov Chains and Their Applications.
* Norris, J. R. (1997). Markov Chains.
* Robert, C. P., Casella, G. (2004). Monte Carlo Statistical Methods.
* Landau, D. P., Binder, K. (2021). A Guide to Monte Carlo Simulations in Statistical Physics.
* Newman, M. E. J. (2010). Networks: An Introduction.

---

# Appendice A. Dimostrazione che il detailed balance implica la stazionarietà

Supponiamo che data una distribuzione $\pi$, abbia costruito una matrice stocastica $P$ per cui valga il *bilancio dettagliato*:

$$
\pi_i P_{ij} = \pi_j P_{ji}
\qquad \text{per ogni } i,j.
$$

Sommando su $j$

$$
\pi_i \sum_j  P_{ij} = \sum_j \pi_j P_{ji}.
$$

Il membro sinistro vale $\pi_i$ perché $\sum_j P_{ij}=1$ ($P$ è una matrice stocastica), quindi

$$
\pi_i = \sum_j \pi_j P_{ji} = \left( \pi \, P \right)_i
$$

ovvero $\pi=\pi P$; quindi imporre il bilancio dettagliato su $P$ rispetto a $\pi$ implica che $\pi$ è proprio la distribuzione di equilibrio di $P$.

# Appendice B. Pseudocodice di Metropolis

```python
def metropolis(x0, n_steps):
    x = x0
    samples = []
    for _ in range(n_steps):
        x_new = propose_symmetric(x)
        r = pi_tilde(x_new) / pi_tilde(x)
        alpha = min(1.0, r)
        if uniform_0_1() < alpha:
            x = x_new
        samples.append(x)
    return samples
```

# Appendice C. Pseudocodice di Metropolis-Hastings

```python
def metropolis_hastings(x0, n_steps):
    x = x0
    samples = []
    for _ in range(n_steps):
        x_new = propose(x)
        r = (pi_tilde(x_new) * q_reverse(x, x_new)) / (pi_tilde(x) * q_forward(x, x_new))
        alpha = min(1.0, r)
        if uniform_0_1() < alpha:
            x = x_new
        samples.append(x)
    return samples
```

# Appendice D. Schema di Gibbs sampling

```python
for t in range(T):
    x1 = sample_from_conditional_x1(x2, x3, ..., xn)
    x2 = sample_from_conditional_x2(x1, x3, ..., xn)
    ...
    xn = sample_from_conditional_xn(x1, ..., x_{n-1})
```
