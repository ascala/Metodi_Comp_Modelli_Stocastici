---
title: "02: Metodi Monte Carlo"
author: "Antonio Scala"
date: "11 Mar 2026"
---

I metodi Monte Carlo costituiscono una delle tecniche fondamentali per la risoluzione numerica di problemi stocastici e deterministici di elevata complessità. Essi si basano sull’uso sistematico del campionamento casuale per stimare quantità di interesse, come integrali, medie o distribuzioni di probabilità, quando una soluzione analitica è impraticabile o impossibile.

L’approccio Monte Carlo trova applicazione in fisica statistica, finanza quantitativa, biologia, chimica computazionale e in generale in ogni ambito dove si debbano affrontare problemi ad alta dimensionalità o caratterizzati da incertezza intrinseca.

## Obiettivi didattici specifici

Al termine, lo studente dovrà essere in grado di:

- comprendere i principi fondamentali dei metodi Monte Carlo;
- analizzare la generazione di numeri casuali e le loro proprietà;
- introdurre il campionamento da distribuzioni arbitrarie;
- applicare il metodo Monte Carlo all’integrazione numerica;
- discutere il ruolo dell’errore statistico e delle tecniche di riduzione della varianza;
- comprendere la differenza tra campionamento indipendente e campionamento con struttura di dipendenza assegnata.

## Struttura della lezione

1. Principio di base e stima tramite media campionaria.
2. Generazione di numeri pseudocasuali: requisiti e qualità.
3. Campionamento da distribuzioni arbitrarie.
4. Campionamento multivariato con covarianza assegnata.
5. Integrazione Monte Carlo in una e più dimensioni.
6. Errore statistico, errore sistematico e limiti del metodo.

---

# Fondamenti teorici

Il metodo Monte Carlo nasce dall’idea di trasformare un problema di natura **continua** -- ad esempio il calcolo di un integrale o di una media -- in un problema **discreto** basato su un insieme finito di campioni casuali.  
In pratica, si sostituisce la media teorica con una **media empirica** calcolata su un campione sufficientemente ampio di punti generati in modo casuale.

Consideriamo un integrale definito su un intervallo $[a,b]$:

$$
I = \int_a^b f(x)\,dx.
$$

Calcolare $I$ in modo esatto può essere difficile o impossibile se $f(x)$ è complicata o se lo spazio di integrazione ha molte dimensioni.  
Per semplificare, si effettua un **cambio di variabile lineare** che porta l’integrale su un intervallo unitario:

$$
I = (b-a) \int_0^1 f\!\big[a + (b-a)u\big]\,du,
$$

dove $u$ è una variabile uniforme in $[0,1]$.

A questo punto si generano $N$ numeri casuali indipendenti $u_i \in [0,1)$ e si approssima l’integrale con la **media aritmetica** dei valori della funzione nei punti campionati:

$$
I \simeq (b-a)\,\frac{1}{N}\sum_{i=1}^N f\!\big[a + (b-a)u_i\big].
$$

Questa è la forma più semplice di **integrazione Monte Carlo**. Essa si basa sul principio che la media dei campioni tende alla media vera quando il numero di campioni $N$ cresce, secondo la **legge dei grandi numeri**.

---

## Interpretazione statistica

La stima Monte Carlo può essere vista come una media statistica della variabile casuale $Y = f[a + (b-a)U]$, dove $U$ è distribuita uniformemente in $[0,1]$.  
La varianza della stima è proporzionale alla varianza di $Y$ e inversamente proporzionale al numero di campioni:

$$
\sigma_I^2 = (b-a)^2\,\frac{\sigma_f^2}{N},
$$

da cui l’incertezza (errore statistico) risulta:

$$
\sigma_I = (b-a)\,\frac{\sigma_f}{\sqrt{N}},
$$

dove $\sigma_f$ è la deviazione standard dei valori di $f$. In altre parole, **raddoppiare la precisione richiede circa quattro volte più campioni**. 

La convergenza è quindi lenta, ma il costo computazionale non peggiora con la dimensione del problema: questo aspetto sarà discusso in dettaglio nella sezione sull'integrazione multidimensionale.

---

## Commento concettuale

L’approssimazione Monte Carlo non richiede una griglia regolare di punti: i campioni casuali esplorano lo spazio in modo uniforme in media. L’errore stimato è di natura **statistica**, non sistematica: può essere ridotto ma non eliminato completamente. La potenza del metodo deriva dalla sua **generalità**: la stessa idea si estende facilmente a integrali multidimensionali, equazioni integrali, simulazioni di sistemi fisici complessi e generazione di configurazioni aleatorie.

Il metodo Monte Carlo non va inteso soltanto come una tecnica di integrazione numerica. Più in generale, esso fornisce una procedura per stimare il valore atteso di una grandezza aleatoria rispetto a una distribuzione di probabilità assegnata. Se $X$ è una variabile aleatoria con densità $p(x)$ e $A(X)$ è un’osservabile, allora

$$
\langle A \rangle = \int A(x)\,p(x)\,dx \simeq \frac{1}{N}\sum_{i=1}^N A(x_i),
$$

dove $x_1,\dots,x_N$ sono campioni indipendenti estratti secondo $p(x)$. In fisica statistica $A$ può rappresentare l’energia, la magnetizzazione o una funzione di correlazione; in finanza quantitativa, il payoff di un derivato. In entrambi i casi l’obiettivo computazionale è lo stesso: stimare una media rispetto a una distribuzione di probabilità.

Nel linguaggio della statistica computazionale, questa quantità è uno **stimatore** della grandezza cercata. Esso è **non distorto** -- il suo valore medio coincide con il valore esatto $\mathbb{E}[\hat{A}_N] = \langle A \rangle$ -- ed è **consistente**: $\hat{A}_N \to \langle A \rangle$ per $N \to \infty$. Il risultato di una simulazione non è quindi un numero “esatto”, ma una stima accompagnata da un’incertezza controllabile.

## Errore statistico ed errore sistematico

Come già osservato, l’errore statistico è intrinseco al metodo e quantificabile direttamente dai dati simulati. Accanto ad esso, possono tuttavia comparire **errori sistematici**, che non derivano dal numero finito di campioni ma da scelte scorrette nella costruzione della simulazione.

Tra le cause più comuni vi sono:

- l’uso di un generatore pseudocasuale di qualità insufficiente;
- un campionamento non coerente con la distribuzione desiderata;
- l’uso di trasformazioni numericamente instabili;
- la presenza di correlazioni indesiderate tra campioni;
- una stima inadeguata della varianza o dell’incertezza.

Questa distinzione è essenziale. L’errore statistico si riduce aumentando $N$; l’errore sistematico, invece, **non scompare** semplicemente aumentando il numero di campioni. Una simulazione Monte Carlo affidabile richiede quindi sia un numero adeguato di campioni, sia una costruzione metodologicamente corretta dell’algoritmo.

## Origine storica del metodo Monte Carlo

Il metodo Monte Carlo fu sviluppato negli anni Quaranta durante il progetto Manhattan.

Stanislaw Ulam, riflettendo su problemi probabilistici legati al gioco del solitario, propose di stimare quantità difficili da calcolare analiticamente mediante simulazioni casuali.

John von Neumann contribuì successivamente allo sviluppo degli algoritmi necessari per implementare il metodo sui primi calcolatori elettronici.

Il nome "Monte Carlo" fu scelto come riferimento al celebre casinò del Principato di Monaco, per sottolineare il ruolo centrale del caso nel metodo.

# Generazione di numeri pseudocasuali

L’efficacia dei metodi Monte Carlo dipende dalla qualità dei numeri casuali utilizzati. Un **generatore di numeri pseudocasuali** (PRNG) produce una sequenza deterministica che approssima una distribuzione uniforme in $[0,1)$. Un esempio classico è il **generatore congruenziale lineare**:

$$
x_{n+1} = (a x_n + c) \bmod m,
$$

con parametri $a$, $c$ e $m$ scelti per massimizzare il periodo e la qualità statistica.  
Le principali proprietà desiderate sono:

- **Uniformità**: i numeri devono coprire lo spazio in modo omogeneo;
- **Indipendenza**: l’autocorrelazione tra valori successivi deve essere minima;
- **Lungo periodo**: la sequenza non deve ripetersi in tempi brevi.

In applicazioni scientifiche si preferiscono generatori di tipo **Mersenne Twister**, **Xorshift** o **PCG**, che garantiscono uniformità e periodi molto lunghi.

## Perché i numeri pseudocasuali sono accettabili

In un contesto computazionale, i numeri "casuali" non sono in genere prodotti da un processo fisico realmente aleatorio, ma da un algoritmo deterministico.  
Questo può sembrare paradossale: come può una sequenza deterministica essere usata per simulare il caso?

La risposta è che, per gli scopi del metodo Monte Carlo, non è necessario che i numeri siano ontologicamente casuali; è sufficiente che essi si comportino **come se** fossero indipendenti e uniformemente distribuiti, almeno rispetto alle osservabili che si vogliono stimare.

Un generatore pseudocasuale è quindi giudicato in base alla sua qualità statistica e non alla sua natura deterministica.  
Due aspetti sono essenziali:

- la sequenza deve riprodurre correttamente la distribuzione uniforme;
- le correlazioni residue tra campioni successivi devono essere trascurabili.

Il fatto che il generatore sia inizializzato da un valore iniziale detto **seed** ha anche un vantaggio pratico importante: la simulazione è riproducibile.  
Questo consente di verificare, confrontare e debuggare gli algoritmi numerici in modo controllato.

---

# Tecniche di campionamento

Nella maggior parte delle applicazioni, non è sufficiente generare numeri uniformi in $[0,1)$: è necessario ottenere campioni che seguano una **distribuzione di probabilità assegnata** $p(x)$, la quale può rappresentare una grandezza fisica, un tempo di attesa, un’energia o qualsiasi altra variabile aleatoria.

In generale, se si dispone di un generatore uniforme $U \in [0,1)$, l’obiettivo è costruire una trasformazione $X = T(U)$ tale che i valori $X$ siano distribuiti secondo $p(x)$.  
Le tecniche più comuni per ottenere ciò sono: il **metodo dell’inversione**, il **metodo di accettazione--rifiuto**, e le **tecniche di campionamento per importanza**.  
In questa lezione ci concentreremo maggiormente sui primi due, che costituiscono la base di tutti gli algoritmi Monte Carlo più avanzati.

---

## Metodo dell’inversione

Il principio di questo metodo è concettualmente semplice: la probabilità che una variabile aleatoria $X$ sia minore o uguale a un certo valore $x$ è data dalla **funzione di distribuzione cumulativa** (CDF)

$$
F(x) = P(X \le x) = \int_{-\infty}^{x} p(x')\,dx'.
$$

Poiché $F(x)$ cresce monotonamente da $0$ a $1$, essa è **invertibile** se $p(x)$ è continua e non nulla sull’intervallo di interesse.  
Di conseguenza, se si estrae un numero casuale $U$ distribuito uniformemente in $[0,1)$, si può definire

$$
X = F^{-1}(U),
$$

ottenendo un valore $X$ che segue esattamente la distribuzione $p(x)$.

Questo procedimento consente di convertire un generatore uniforme in un generatore di qualunque distribuzione, purché la CDF sia invertibile in forma chiusa o numerica.

## Limiti operativi del metodo dell’inversione

Il metodo dell’inversione è concettualmente elegante e, quando applicabile, fornisce un campionamento esatto.  
Tuttavia, il suo uso pratico presenta limiti importanti.

Il primo limite è di natura analitica: la funzione cumulativa inversa $F^{-1}$ non è sempre disponibile in forma chiusa. Molte distribuzioni di interesse applicativo possiedono una densità semplice ma una cumulativa non invertibile esplicitamente.

Il secondo limite è di natura numerica: anche quando $F^{-1}$ esiste, la sua valutazione può risultare costosa o delicata, specialmente nelle code della distribuzione, dove piccole variazioni di $U$ possono produrre variazioni molto grandi di $X$.

Infine, nel caso multidimensionale, il metodo dell’inversione diventa rapidamente meno naturale, perché richiede di costruire trasformazioni congiunte compatibili con l’intera distribuzione target.

Per queste ragioni, l’inversione rappresenta un metodo fondamentale dal punto di vista teorico, ma spesso non è la soluzione più conveniente nelle applicazioni realistiche. In molti casi si preferiscono metodi più flessibili, come l’accettazione--rifiuto o procedure iterative di campionamento.

---

## Esempio: distribuzione esponenziale

Si consideri la distribuzione esponenziale

$$
p(x) = \lambda e^{-\lambda x}, \quad x \ge 0,
$$

che descrive ad esempio i tempi di attesa tra eventi indipendenti (come decadimenti radioattivi o arrivi di particelle in un rivelatore).  
La funzione cumulativa è

$$
F(x) = 1 - e^{-\lambda x}.
$$

Ponendo $U = F(x)$ e risolvendo rispetto a $x$, si ottiene:

$$
x = F^{-1}(U) = -\frac{1}{\lambda}\ln(1 - U).
$$

Poiché $U$ è uniforme in $[0,1)$, anche $1-U$ lo è, quindi si può semplicemente scrivere

$$
x = -\frac{1}{\lambda}\ln U.
$$

Questo fornisce un metodo pratico e diretto per generare numeri casuali esponenzialmente distribuiti.

In linguaggio Python:

```python
import numpy as np

U = np.random.rand(100000)
X = -np.log(U) / 2.0  # esempio con $\lambda = 2.0$
```

L’istogramma dei valori di `X` segue perfettamente la distribuzione esponenziale desiderata.

---

## Metodo di accettazione--rifiuto

Quando la distribuzione $p(x)$ è complicata e non invertibile, si ricorre al metodo di **accettazione--rifiuto** (o *accept--reject method*), ideato da von Neumann. L’idea è confrontare $p(x)$ con una **distribuzione di riferimento** $g(x)$, dalla quale sia facile generare campioni, e che la maggiori ovunque:

$$
p(x) \le c\, g(x), \quad \text{per ogni } x,
$$

dove $c>1$ è una costante di normalizzazione detta **fattore di sovracampionamento**.

L’algoritmo procede come segue:

1. Genera un valore $x$ secondo la distribuzione $g(x)$.
2. Genera un numero uniforme $u \in [0,1)$.
3. Se $u < \dfrac{p(x)}{c\, g(x)}$, **accetta** $x$; altrimenti **rigetta** e ripeti il processo.

I valori accettati seguono la distribuzione desiderata $p(x)$.

## Perché il metodo di accettazione--rifiuto funziona: interpretazione geometrica

Il metodo di accettazione--rifiuto può essere interpretato geometricamente come un campionamento uniforme nell’area sottesa alla funzione $c,g(x)$.

Si genera dapprima un valore $x$ secondo la distribuzione ausiliaria $g(x)$, quindi una quota verticale casuale uniforme tra $0$ e $c,g(x)$.
In termini geometrici, si sta estraendo un punto casuale nel dominio compreso sotto la curva dell’inviluppo $c,g(x)$.

Il punto viene accettato soltanto se cade sotto la curva della distribuzione target $p(x)$.
I punti accettati risultano così uniformemente distribuiti nell’area sottesa a $p(x)$, e la distribuzione marginale delle loro ascisse coincide con la densità desiderata.

Questa interpretazione rende intuitivo anche il ruolo del parametro $c$.
Se l’inviluppo $c,g(x)$ è molto più alto di $p(x)$ in gran parte del dominio, una frazione significativa dei punti cadrà nella regione compresa tra le due curve e verrà rigettata.
Se invece $c,g(x)$ approssima bene $p(x)$, il tasso di accettazione sarà più elevato e il metodo più efficiente.

L’efficienza media del procedimento è infatti pari a $1/c$, e dipende quindi direttamente da quanto bene la distribuzione ausiliaria riesce a seguire il profilo della distribuzione target.

---

## Esempio: distribuzione triangolare

Supponiamo di voler campionare una distribuzione triangolare definita su $[0,1]$:

$$
p(x) = 2x, \qquad 0 \le x \le 1.
$$

È semplice campionare da $g(x)=1$ (uniforme in $[0,1]$) e notare che $p(x)\le 2,g(x)$, quindi $c=2$.
L’algoritmo diventa:

1. Estrai $x$ uniforme in $[0,1]$.
2. Estrai $u$ uniforme in $[0,1]$.
3. Accetta $x$ se $u < x$, altrimenti rigetta.

Il valore medio di accettazione è $1/c = 1/2$, quindi circa metà dei campioni sarà scartata.
Nonostante lo spreco, questo metodo è estremamente versatile e applicabile a qualunque forma di $p(x)$.

---

## Efficienza del metodo

L’efficienza complessiva è data da $1/c$, cioè dal rapporto tra l’area sotto $p(x)$ e quella sotto $c, g(x)$.
Scegliere una funzione di riferimento $g(x)$ che segua da vicino la forma di $p(x)$ riduce gli scarti e migliora la produttività del metodo.
In situazioni reali, una buona scelta di $g(x)$ può aumentare di ordini di grandezza la velocità di simulazione.

---

## Esempio pratico in Python

```python
import numpy as np

def p(x): return 2*x  # distribuzione target
def g(x): return 1.0  # distribuzione uniforme

N = 100000
accepted = []
while len(accepted) < N:
    x = np.random.rand()
    u = np.random.rand()
    if u < p(x)/(2*g(x)):  # c = 2
        accepted.append(x)
```

Il vettore `accepted` conterrà campioni distribuiti secondo $p(x) = 2x$.
Il confronto tra l’istogramma empirico e la curva teorica mostra un accordo eccellente.

---

## Il problema delle regioni rare

In molti problemi pratici l’integrale è dominato da una piccola regione dello spazio delle variabili.

Se il campionamento è uniforme, la probabilità di esplorare queste regioni può essere molto bassa.
Di conseguenza, la stima Monte Carlo può avere una varianza molto grande.

Questo fenomeno è particolarmente rilevante quando:

* la funzione $f(x)$ è molto concentrata;
* l’integrale è dominato da code della distribuzione;
* lo spazio delle variabili ha dimensione elevata.

Una strategia naturale consiste nel modificare la distribuzione di campionamento in modo da concentrare i punti nelle regioni più rilevanti.
Questo principio è alla base delle tecniche di **importance sampling**.

---

## Campionamento per importanza

Una delle idee più potenti del metodo Monte Carlo consiste nel modificare la distribuzione con cui si generano i campioni, in modo da concentrare l’esplorazione nelle regioni più rilevanti dello spazio delle variabili.

Supponiamo di voler calcolare un integrale della forma

$$
I = \int f(x)\,dx.
$$

Se si introduce una densità di probabilità $q(x)$ tale che $q(x) > 0$ ovunque $f(x)$ contribuisca in modo significativo, si può riscrivere l’integrale come

$$
I = \int \frac{f(x)}{q(x)} q(x)\,dx.
$$

Questo significa che $I$ può essere interpretato come un valore atteso rispetto alla distribuzione $q(x)$:

$$
I = \mathbb{E}_q\!\left[\frac{f(X)}{q(X)}\right].
$$

Generando quindi campioni $x_1,\dots,x_N$ secondo $q(x)$, si ottiene la stima Monte Carlo

$$
I \simeq \frac{1}{N}\sum_{i=1}^N \frac{f(x_i)}{q(x_i)}.
$$

L’idea fondamentale è che la distribuzione ausiliaria $q(x)$ può essere scelta in modo da campionare più frequentemente le regioni in cui $|f(x)|$ è grande.  
In questo modo si ottiene una stima più efficiente rispetto al campionamento uniforme, soprattutto quando l’integrale è dominato da contributi localizzati o da regioni rare.

## Interpretazione concettuale

Nel campionamento uniforme tutti i punti dello spazio vengono trattati allo stesso modo. Nel campionamento per importanza, invece, si decide deliberatamente di visitare più spesso le regioni che contribuiscono maggiormente al valore dell’integrale.

Poiché questo altera la frequenza di campionamento, è necessario introdurre un **peso correttivo** dato dal rapporto $f(x)/q(x)$. Il metodo resta quindi esatto, ma redistribuisce lo sforzo computazionale in modo più intelligente.

## Scelta della distribuzione ausiliaria

In linea ideale, la scelta ottimale di $q(x)$ sarebbe proporzionale a $|f(x)|$, perché in questo caso la varianza della stima si riduce drasticamente. Nella pratica, però, non è sempre possibile campionare direttamente da una distribuzione così costruita.

Per questo motivo si scelgono spesso distribuzioni ausiliarie che:

- siano facili da campionare;
- approssimino la forma generale di $|f(x)|$;
- non siano troppo piccole nelle regioni importanti.

Una scelta inadeguata di $q(x)$ può rendere il metodo inefficiente o addirittura instabile, se i pesi $f(x)/q(x)$ diventano troppo grandi.

## Esempio semplice

Si consideri l’integrale

$$
I = \int_0^1 e^{-10x}\,dx.
$$

Poiché la funzione è concentrata vicino a $x=0$, un campionamento uniforme spreca molti punti nella regione dove il contributo è trascurabile.

Una scelta più efficiente consiste nel campionare secondo una distribuzione esponenziale troncata o, più semplicemente, secondo una densità più concentrata vicino a zero. I campioni ottenuti vengono poi pesati con il fattore correttivo appropriato.

Questo esempio mostra che il vantaggio del campionamento per importanza non consiste nel modificare il valore dell’integrale, ma nel ridurre la fluttuazione statistica della stima.

## Ruolo nel metodo Monte Carlo

Il campionamento per importanza occupa una posizione centrale nella teoria e nella pratica dei metodi Monte Carlo. Da un lato, esso è una tecnica di campionamento non uniforme; dall’altro, rappresenta una delle strategie più efficaci per la riduzione della varianza.

Per questa ragione, l’importance sampling può essere visto come il primo esempio di una filosofia più generale: migliorare una simulazione non aumentando soltanto il numero di campioni, ma progettando meglio il modo in cui i campioni vengono generati.

---

# Campionamento multivariato e variabili correlate

Nelle applicazioni più semplici del metodo Monte Carlo, le variabili generate sono indipendenti. In molti problemi realistici, tuttavia, le grandezze di interesse presentano dipendenze reciproche e devono quindi essere campionate con una struttura di correlazione assegnata.

Questo problema compare naturalmente in numerosi contesti:

* in fisica, quando diverse componenti di rumore non sono indipendenti;
* in finanza, quando i rendimenti di più attivi mostrano covarianze non nulle;
* in statistica multivariata, quando si vogliono simulare dati coerenti con una matrice di covarianza stimata empiricamente.

Il caso più importante e più trattabile è quello della distribuzione gaussiana multivariata. Andiamo prima peró a fare un rapido recap delle misure di correlazione

## Covarianza, correlazione e misure di dipendenza

Prima di affrontare il campionamento di variabili correlate è utile richiamare
le principali misure di dipendenza tra variabili aleatorie.

### Covarianza

Data due variabili $X$ e $Y$ con medie $\mu_X$ e $\mu_Y$, la covarianza è

$$
\mathrm{Cov}(X,Y) = \mathbf{E}[(X - \mu_X)(Y - \mu_Y)].
$$

Un valore positivo indica che le due variabili tendono a crescere insieme;
un valore negativo che una cresce quando l'altra decresce; un valore nullo
che non esiste dipendenza lineare. La covarianza dipende però dalle unità
di misura delle variabili, il che la rende difficile da interpretare in
termini assoluti.

### Correlazione di Pearson

Si ottiene normalizzando la covarianza con le deviazioni standard:

$$
\rho(X,Y) = \frac{\mathrm{Cov}(X,Y)}{\sigma_X \sigma_Y} \in [-1,1].
$$

Il coefficiente $\rho$ è adimensionale e misura l'intensità della dipendenza
**lineare**: $\rho = \pm 1$ corrisponde a una relazione lineare perfetta,
$\rho = 0$ indica assenza di dipendenza lineare. Quest'ultimo caso non implica
però indipendenza: due variabili possono essere fortemente dipendenti in modo
non lineare e avere comunque $\rho = 0$.

### Correlazione di Kendall

Per catturare forme di dipendenza non lineari si ricorre a misure basate
sui ranghi. La **correlazione di Kendall** $\tau_K$ confronta la concordanza
delle coppie di osservazioni: dati due campioni $(x_i, y_i)$ e $(x_j, y_j)$,
la coppia è detta concordante se $x_i > x_j$ e $y_i > y_j$ oppure
$x_i < x_j$ e $y_i < y_j$, discordante altrimenti. Si definisce

$$
\tau_K = \frac{\text{coppie concordanti} - \text{coppie discordanti}}{\text{coppie totali}}.
$$

Il vantaggio principale di $\tau_K$ rispetto a $\rho$ è che è invariante per
trasformazioni monotone: se $U = F(X)$ con $F$ strettamente crescente, allora
$\tau_K(U,V) = \tau_K(X,Y)$. Questa proprietà lo rende la misura naturale
nel contesto delle copule, dove le marginali vengono trasformate in variabili
uniformi tramite le rispettive CDF.

## Distribuzione normale multivariata

Un vettore aleatorio $\mathbf{X} \in \mathbb{R}^d$ si dice gaussianamente distribuito con media $\boldsymbol{\mu}$ e matrice di covarianza $\Sigma$ se la sua densità è

$$
p(\mathbf{x}) =
\frac{1}{(2\pi)^{d/2} (\det \Sigma)^{1/2}}
\exp\!\left[
-\frac{1}{2}
(\mathbf{x}-\boldsymbol{\mu})^T
\Sigma^{-1}
(\mathbf{x}-\boldsymbol{\mu})
\right].
$$

La matrice $\Sigma$ deve essere simmetrica e semidefinita positiva. Gli elementi diagonali rappresentano le varianze delle componenti, mentre quelli fuori diagonale descrivono le covarianze:

$$
\Sigma_{ij} = \mathrm{Cov}(X_i, X_j).
$$

## Generazione di campioni gaussiani correlati

Supponiamo di disporre di un vettore $\mathbf{Z}$ di variabili gaussiane standard indipendenti:

$$
\mathbf{Z} \sim \mathcal{N}(\mathbf{0}, I).
$$

Se esiste una matrice $L$ tale che

$$
\Sigma = L L^T,
$$

allora il vettore

$$
\mathbf{X} = \boldsymbol{\mu} + L\mathbf{Z}
$$

ha media $\boldsymbol{\mu}$ e covarianza $\Sigma$.

Infatti,

$$
\mathbb{E}[\mathbf{X}] = \boldsymbol{\mu},
$$

e

$$
\mathrm{Cov}(\mathbf{X}) =
\mathbb{E}\!\left[
(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^T
\right] =
L\,\mathbb{E}[\mathbf{Z}\mathbf{Z}^T]\,L^T =
L I L^T =
\Sigma.
$$

Il problema del campionamento gaussiano correlato si riduce quindi alla costruzione di una fattorizzazione appropriata della matrice di covarianza.

## Fattorizzazione di Cholesky

Se $\Sigma$ è definita positiva, il metodo numericamente più efficiente è la **fattorizzazione di Cholesky**:

$$
\Sigma = L L^T,
$$

dove $L$ è triangolare inferiore. Questa scelta è molto comune nelle simulazioni Monte Carlo perché è stabile, veloce e semplice da implementare.

Tuttavia, la decomposizione di Cholesky richiede che la matrice sia strettamente definita positiva. In presenza di autovalori nulli o di piccole violazioni numeriche della positività, il metodo può fallire.

## Decomposizione spettrale

Un’alternativa più generale consiste nella diagonalizzazione della matrice di covarianza:

$$
\Sigma = Q \Lambda Q^T,
$$

dove $Q$ è ortogonale e $\Lambda$ è diagonale con autovalori non negativi.
Si può allora porre

$$
L = Q \Lambda^{1/2},
$$

e generare nuovamente

$$
\mathbf{X} = \boldsymbol{\mu} + L\mathbf{Z}.
$$

Questa rappresentazione è utile anche geometricamente: la trasformazione lineare $L$ ruota e dilata il vettore gaussiano isotropo, deformando la sfera unitaria in un ellissoide di covarianza $\Sigma$.

## Problemi numerici delicati

Nelle applicazioni reali, la matrice di covarianza stimata dai dati può essere mal condizionata, quasi singolare o perfino numericamente non definita positiva a causa degli errori di arrotondamento.

I principali problemi sono:

* autovalori molto piccoli, che rendono instabile l’inversione;
* perdita di definita positività per rumore numerico;
* matrici singolari, che impediscono l’uso diretto di $\Sigma^{-1}$ o della Cholesky.

In questi casi si adottano varie strategie.

## Regolarizzazione diagonale

Una tecnica semplice consiste nel sostituire $\Sigma$ con

$$
\Sigma_{\varepsilon} = \Sigma + \varepsilon I,
$$

dove $\varepsilon > 0$ è piccolo.
Questo sposta gli autovalori lontano da zero e rende la matrice meglio condizionata.

## Troncamento spettrale

Se alcuni autovalori sono numericamente negativi ma di modulo molto piccolo, essi possono essere posti uguali a zero oppure sostituiti con una soglia minima positiva. Si ottiene così una matrice proiettata sul cono delle matrici semidefinite positive.

## Pseudoinversa

Quando $\Sigma$ è singolare o quasi singolare, la sua inversa ordinaria non esiste o non è affidabile. Si utilizza allora la **pseudoinversa di Moore--Penrose**, costruita ignorando le direzioni a varianza nulla.

Se $\Sigma$ ha rango $r < d$, si scrive la decomposizione ridotta

$$ \Sigma = Q_r \Lambda_r Q_r^T, $$

dove $Q_r \in \mathbb{R}^{d \times r}$ contiene solo gli $r$ autovettori significativi e $\Lambda_r$ i corrispondenti autovalori positivi. La pseudoinversa è allora

$$ \Sigma^{+} = Q_r \Lambda_r^{-1} Q_r^T. $$

Per il campionamento, si genera $\mathbf{Z}_r \in \mathbb{R}^r$ gaussiano standard e si pone

$$ \mathbf{X} = \boldsymbol{\mu} + Q_r \Lambda_r^{1/2} \mathbf{Z}_r. $$

La matrice $Q_r \Lambda_r^{1/2}$ **proietta** il campionamento sul sottospazio di dimensione $r$ su cui la distribuzione è effettivamente concentrata: le direzioni a varianza nulla non vengono mai esplorate, coerentemente con la struttura degenere di $\Sigma$.

## Commento metodologico

Dal punto di vista Monte Carlo, la difficoltà principale non è tanto generare gaussiane standard indipendenti, quanto trasformarle in campioni con la struttura di dipendenza desiderata in modo stabile e numericamente robusto.

Questo esempio mostra bene una caratteristica generale dei metodi Monte Carlo: il problema teorico del campionamento è spesso inseparabile dai problemi numerici legati alla rappresentazione e manipolazione delle matrici.

## Oltre la dipendenza gaussiana: copule

La matrice di covarianza descrive completamente la dipendenza tra variabili solo nel caso gaussiano. Per distribuzioni non gaussiane, due vettori aleatori possono avere la stessa matrice di covarianza ma strutture di dipendenza molto diverse: ad esempio, possono concordare quasi sempre oppure concordare nelle situazioni normali ma divergere fortemente nelle code. La covarianza non distingue questi casi.

### Il teorema di Sklar

Il risultato fondamentale è il seguente: data una distribuzione congiunta $F(x_1, \dots, x_d)$ con marginali $F_1(x_1), \dots, F_d(x_d)$, esiste una funzione $C : [0,1]^d \to [0,1]$, detta **copula**, tale che

$$ F(x_1, \dots, x_d) = C!\left(F_1(x_1), \dots, F_d(x_d)\right). $$

La copula $C$ contiene tutta e sola la struttura di dipendenza, separata dal comportamento marginale.

### Costruzione intuitiva

L'idea è semplice: se $X_i$ ha CDF $F_i$, allora $U_i = F_i(X_i)$ è uniforme in $[0,1]$ -- questo è il metodo dell'inversione applicato al contrario. Le variabili $U_1, \dots, U_d$ sono tutte uniformi, ma non sono indipendenti: la loro distribuzione congiunta è esattamente la copula $C$. Essa cattura come le variabili si muovono insieme, indipendentemente dalla forma delle singole marginali.

Per **simulare** da una distribuzione con marginali $F_1, \dots, F_d$ e copula $C$:

1. generare $(u_1, \dots, u_d)$ dalla copula $C$;
2. applicare le inverse: $x_i = F_i^{-1}(u_i)$.

### Esempi di copule

Le copule più usate in pratica sono:

* **copula gaussiana**: la dipendenza è quella di una gaussiana multivariata, ma le marginali possono essere arbitrarie;
* **copula di Student**: simile alla gaussiana ma con code più pesanti, cattura la concordanza in situazioni estreme;
* **copule archimedee** (Clayton, Gumbel, Frank): famiglie parametriche con diverse asimmetrie nella dipendenza, utili quando la coda inferiore e quella superiore si comportano diversamente.

### Perché importa nel campionamento Monte Carlo

Le copule permettono di costruire distribuzioni multivariate con marginali assegnate e dipendenza non gaussiana, il che è essenziale ogni volta che la struttura di correlazione reale del problema non è ben descritta da una gaussiana multivariata. Applicazioni tipiche sono la modellazione del rischio di portafoglio in finanza, dove i titoli tendono a crollare insieme più spesso di quanto una gaussiana preveda, e la statistica multivariata applicata a dati con distribuzioni asimmetriche o a code pesanti.

---

# Integrazione Monte Carlo

L’integrazione Monte Carlo rappresenta una delle applicazioni più dirette e significative del metodo. Essa consente di stimare integrali di funzioni complesse o multidimensionali attraverso un campionamento casuale, sostituendo il calcolo analitico con una media statistica.

## Estensione multidimensionale

Sia $\Omega \subset \mathbb{R}^d$ un dominio $d$--dimensionale di volume finito $V(\Omega)$.
L’obiettivo è stimare un integrale del tipo:

$$
I = \int_{\Omega} f(\mathbf{x}), d\mathbf{x}.
$$

Introducendo la variabile aleatoria $\mathbf{X}$ uniformemente distribuita in $\Omega$, possiamo riscrivere:

$$
I = V(\Omega), \mathbb{E}[f(\mathbf{X})].
$$

Questo significa che l’integrale è proporzionale al valore medio di $f$ calcolato su punti distribuiti uniformemente nel dominio.
La stima Monte Carlo corrispondente è:

$$
I \simeq \frac{V(\Omega)}{N}\sum_{i=1}^{N} f(\mathbf{x}_i),
$$

dove $\mathbf{x}_i$ sono campioni casuali indipendenti uniformi in $\Omega$.

Questo approccio si estende naturalmente a qualunque dimensione: il numero di campioni $N$ necessario per ottenere una precisione fissata **non dipende dalla dimensione $d$**, in contrasto con i metodi deterministici, che richiedono un numero di punti proporzionale a $n^d$.
Questo è il motivo per cui il metodo Monte Carlo è la tecnica elettiva per l’integrazione in spazi ad alta dimensionalità, ad esempio in fisica statistica, in finanza e in meccanica statistica.

## Il vantaggio in alta dimensione

La vera forza del metodo Monte Carlo emerge quando il problema dipende da molte variabili.

Nei metodi deterministici basati su griglie, se in una dimensione si usano $n$ punti, in $d$ dimensioni il numero totale di valutazioni cresce come

$$
n^d.
$$

Questa crescita esponenziale rende rapidamente impraticabile l’integrazione numerica in spazi di grande dimensionalità.

Nel metodo Monte Carlo, invece, l’errore statistico dipende essenzialmente dal numero complessivo di campioni:

$$
\sigma \sim \frac{1}{\sqrt{N}},
$$

e non peggiora direttamente con la dimensione dello spazio.
Questo non significa che i problemi ad alta dimensione diventino "facili", ma significa che la complessità del metodo non esplode nel modo catastrofico tipico delle griglie deterministiche.

Per questa ragione il metodo Monte Carlo è particolarmente adatto alla fisica statistica, alla chimica computazionale, alla finanza quantitativa e, più in generale, a tutti i problemi con molti gradi di libertà.

## Interpretazione geometrica

L’idea di fondo può essere vista in termini di probabilità geometrica: stimare un integrale equivale a stimare la **frazione di punti che cadono in una regione pesata** dalla funzione $f$.

Nel caso di una funzione $f(\mathbf{x}) \ge 0$, si può interpretare l’integrale come il volume sotto la superficie $z = f(\mathbf{x})$. Campionando punti uniformi $(\mathbf{x}*i, z_i)$ in un parallelepipedo di base $\Omega$ e altezza $f*{\max}$, la proporzione di punti con $z_i < f(\mathbf{x}_i)$ fornisce una stima diretta dell’integrale relativo a $f$.

## Esempio: stima di $\pi$

Un esempio classico è la stima di $\pi$ con un metodo geometrico.
Si consideri un quadrato unitario $[0,1]^2$ che contiene un quarto di cerchio di raggio 1.
L’area del quarto di cerchio è $\pi/4$, mentre l’area del quadrato è 1.

Generando $N$ punti uniformi $(x_i, y_i)$ nel quadrato, si calcola la frazione di punti che soddisfano $x_i^2 + y_i^2 \le 1$.
Denotando con $N_{\text{cerchio}}$ il numero di punti interni al quarto di cerchio, si ha:

$$
\frac{N_{\text{cerchio}}}{N_{\text{totale}}} \simeq \frac{\pi}{4},
\qquad
\pi \simeq 4 \frac{N_{\text{cerchio}}}{N_{\text{totale}}}.
$$

## Analisi dell’errore

Nel caso multidimensionale, l’incertezza sulla stima dell’integrale è:

$$
\sigma_I = V(\Omega)\,\frac{\sigma_f}{\sqrt{N}},
$$

dove $\sigma_f$ è la deviazione standard dei valori di $f$ campionati. Le cause principali di fluttuazione sono il campionamento finito, la presenza di regioni ad alta variabilità di $f$ mal esplorate da campioni uniformi, e l’uso di generatori o trasformazioni di qualità insufficiente. In tutti i casi, la precisione può essere stimata direttamente dai dati simulati.

## Efficienza statistica e numero effettivo di campioni

Non tutti i campioni contribuiscono allo stesso modo all’informazione statistica. Se esistono correlazioni tra campioni successivi, il numero effettivo di osservazioni indipendenti è inferiore al totale: si introduce il **numero effettivo di campioni**

$$
N_{\text{eff}} \approx \frac{N}{\tau},
$$

dove $\tau$ è una lunghezza di correlazione caratteristica della sequenza. Questo concetto diventa fondamentale nei metodi di **Markov Chain Monte Carlo**, dove i campioni non sono indipendenti: la sola dimensione del campione non basta a misurare l’effettiva qualità statistica della stima.

## Tecniche di riduzione della varianza

Poiché la convergenza è lenta, una parte fondamentale dell’efficienza del metodo Monte Carlo consiste nel ridurre la varianza **senza aumentare $N$**.
Le principali strategie sono:

## Campionamento stratificato

Il dominio $\Omega$ viene suddiviso in sottoinsiemi (strati) di uguale misura, e si genera un punto casuale in ciascuno di essi.
In questo modo si evita che i punti si concentrino casualmente in una sola zona, migliorando l’uniformità del campionamento.

## Importance sampling

Il campionamento per importanza, già trattato nella sezione dedicata, è anche la principale strategia di riduzione della varianza: concentrando i campioni nelle regioni che contribuiscono maggiormente all’integrale, riduce le fluttuazioni statistiche della stima.

## Antithetic variates

Si usano coppie di campioni correlati in modo controllato.
Per esempio, se si genera $u \in [0,1)$, si può considerare anche $1-u$ come campione complementare.
Le due valutazioni di $f$ tendono ad avere errori opposti, la cui media è più stabile.

## Applicazione pratica

Come esempio semplice, si può stimare l’integrale

$$
I = \int_0^1 e^{-x^2},dx
$$

usando campioni uniformi.

```python
import numpy as np

def f(x):
    return np.exp(-x**2)

N = 100000
x = np.random.rand(N)
I = np.mean(f(x))
sigma = np.std(f(x)) / np.sqrt(N)

print(f"Stima Monte Carlo: {I:.6f} ± {sigma:.6f}")
```

Confrontando con il valore numerico reale $I_{\text{vero}} \simeq 0.746824$, si osserva che la stima converge correttamente entro l’errore previsto.
La precisione cresce come $1/\sqrt{N}$, e il confronto con metodi deterministici (es. Simpson) mostra che, per funzioni in bassa dimensione, il metodo Monte Carlo è meno efficiente ma molto più generale.

---

# Collegamento con i metodi successivi e limiti della presente trattazione

In questa lezione sono stati considerati metodi Monte Carlo basati su campioni indipendenti, generati direttamente oppure ottenuti tramite trasformazioni di variabili uniformi, sia in dimensione scalare sia nel caso multivariato con covarianza assegnata.

L’integrazione Monte Carlo è un caso particolare del **calcolo di medie d’ensemble** su una distribuzione di probabilità: molti problemi fisici o statistici -- dalla stima di osservabili in sistemi termici al valore atteso di payoff finanziari -- si riducono allo stesso principio già discusso.

Le lezioni successive mostreranno come generare campioni quando $p(x)$ non è nota in forma analitica, ma è definita in modo implicito -- ad esempio tramite un potenziale o una probabilità di transizione. In quel caso il campionamento assume un carattere dinamico e richiede il linguaggio delle **catene di Markov**. Questo condurrà naturalmente ai **metodi di campionamento Markoviano** (come Metropolis--Hastings), ai **processi di simulazione di eventi discreti** e ai **metodi di dinamica molecolare stocastica**, che estendono il principio Monte Carlo a dinamiche dipendenti dal tempo e distribuzioni non uniformi.

# Riferimenti

* Kalos, M. H., Whitlock, P. A. *Monte Carlo Methods*. Wiley.
* Binder, K., Heermann, D. *Monte Carlo Simulation in Statistical Physics*. Springer.
* Fishman, G. S. *Monte Carlo: Concepts, Algorithms, and Applications*. Springer.
* Kroese, D. P., Brereton, T., Taimre, T., Botev, Z. I. (2014). *Why the Monte Carlo method is so important today*. *Wiley Interdisciplinary Reviews: Computational Statistics*.
* Metropolis, N., Ulam, S. (1949). *The Monte Carlo Method*. *Journal of the American Statistical Association*.

---

\newpage

# Appendice: Dimostrazione del metodo dell’inversione

L’idea fondamentale del metodo dell’inversione è che, se $U$ è una variabile uniforme in $[0,1)$ e si definisce $X = F^{-1}(U)$, allora $X$ è distribuita secondo la distribuzione di probabilità avente funzione cumulativa $F(x) = P(X \le x)$.
Questo risultato, apparentemente semplice, può essere dimostrato in modo rigoroso utilizzando la definizione di funzione di distribuzione e la formula della derivata dell’inversa.

## Dimostrazione tramite la funzione di ripartizione

Sia $F(x)$ una funzione di distribuzione cumulativa (CDF) strettamente crescente e continua, dunque invertibile.
Per ogni $x$ reale, consideriamo:

$$
P(X \le x) = P(F^{-1}(U) \le x).
$$

Poiché $F$ è crescente, l’inequazione $F^{-1}(U) \le x$ equivale a $U \le F(x)$.
Dato che $U$ è uniforme in $[0,1)$, vale:

$$
P(U \le F(x)) = F(x).
$$

Pertanto, la distribuzione cumulativa della variabile $X = F^{-1}(U)$ coincide con $F(x)$:

$$
P(X \le x) = F(x).
$$

Questo mostra che $X$ ha proprio la distribuzione desiderata.

## Dimostrazione differenziale: uso della derivata dell’inversa

Supponiamo ora che $F$ sia una funzione derivabile e strettamente crescente, con densità $p(x) = F'(x) > 0$.
Definiamo nuovamente $X = F^{-1}(U)$, dove $U$ è uniforme in $[0,1)$.
Poiché $U = F(X)$, derivando entrambi i membri otteniamo:

$$
\frac{dU}{dX} = F'(X) = p(X).
$$

Applicando la regola della derivata dell’inversa, si ha:

$$
\frac{dX}{dU} = \frac{1}{F'(X)} = \frac{1}{p(X)}.
$$

Ora, per una trasformazione monotona $U \mapsto X$, la densità si trasforma come:

$$
f_X(x) = f_U(u) \left|\frac{dU}{dX}\right| = f_U(F(x)) , p(x).
$$

Poiché $f_U(u) = 1$ per $u \in [0,1)$, segue immediatamente che:

$$
f_X(x) = p(x).
$$

Quindi la variabile $X = F^{-1}(U)$ possiede esattamente la densità desiderata.

## Caso generale: l’inversa generalizzata (quantile function)

Quando $F$ non è strettamente crescente o presenta tratti piatti (come nelle distribuzioni discrete o miste), l’inversa classica non esiste in senso stretto.
Si definisce allora la **funzione quantile** o **inversa generalizzata**:

$$
F^{-1}(u) = \inf {x \in \mathbb{R} : F(x) \ge u}, \quad u \in (0,1).
$$

Se $U \sim \mathrm{Unif}(0,1)$ e $X = F^{-1}(U)$, si verifica comunque che:

$$
P(X \le x) = P(F^{-1}(U) \le x) = P(U \le F(x)) = F(x).
$$

Dunque, anche nel caso discreto o misto, la definizione mantiene la proprietà fondamentale.

## Condizioni di validità e considerazioni pratiche

* **Monotonia:** $F$ deve essere non decrescente (condizione intrinseca per ogni CDF).
  La stretta crescita e la derivabilità sono richieste solo per usare la formula della derivata dell’inversa.
* **Supporto:** la relazione $P(X \le x) = F(x)$ è valida per $x$ appartenenti al dominio di definizione di $F$.
  Fuori dal supporto, vale $P(X \le x) = 0$ per $x < \inf \mathrm{supp}(F)$ e $1$ per $x > \sup \mathrm{supp}(F)$.
* **Implementazione numerica:** quando $F^{-1}$ non è nota in forma chiusa, si può calcolare per via numerica (tabulazione, interpolazione monotona, metodi di bisezione o Newton).
  Per evitare instabilità numeriche, si evita di usare direttamente $U$ troppo vicino a $0$ o $1$ (si può usare $U \in [\varepsilon, 1-\varepsilon]$ con $\varepsilon$ piccolo).

## Esempio di verifica: distribuzione esponenziale

Consideriamo $p(x) = \lambda e^{-\lambda x}$ per $x \ge 0$.
La funzione cumulativa è:

$$
F(x) = 1 - e^{-\lambda x}.
$$

Il metodo dell’inversione dà:

$$
X = F^{-1}(U) = -\frac{1}{\lambda} \ln(1 - U).
$$

Poiché $U$ è uniforme in $[0,1)$, anche $1-U$ lo è, e dunque:

$$
P(X \le x) = P\left(-\frac{1}{\lambda}\ln(1-U) \le x\right)
= P(U \le 1 - e^{-\lambda x}) = 1 - e^{-\lambda x} = F(x).
$$

Infine, derivando $F(x)$ si ottiene $F'(x) = \lambda e^{-\lambda x} = p(x)$, confermando che la variabile generata con $X = -\frac{1}{\lambda} \ln(1-U)$ segue la distribuzione esponenziale attesa.

## Sintesi concettuale

* Il metodo dell’inversione funziona perché applicare $F^{-1}$ a una variabile uniforme trasforma l’uniforme in una variabile con distribuzione $F$.
* La dimostrazione si basa sulla relazione $P(U \le F(x)) = F(x)$ e sulla formula della derivata dell’inversa.
* È un metodo esatto e generale, purché si possa valutare o approssimare $F^{-1}$.
* In molti casi pratici, le funzioni di quantile tabulate o le librerie numeriche implementano questa trasformazione in modo efficiente.

