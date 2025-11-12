---
title: "Metodi Monte Carlo"
date: ""
---
# Metodi Monte Carlo

I metodi Monte Carlo costituiscono una delle tecniche fondamentali per la risoluzione numerica di problemi stocastici e deterministici di elevata complessità. Essi si basano sull’uso sistematico del campionamento casuale per stimare quantità di interesse, come integrali, medie o distribuzioni di probabilità, quando una soluzione analitica è impraticabile o impossibile.

L’approccio Monte Carlo trova applicazione in fisica statistica, finanza quantitativa, biologia, chimica computazionale e in generale in ogni ambito dove si debbano affrontare problemi ad alta dimensionalità o caratterizzati da incertezza intrinseca.

### Obiettivi didattici specifici

Al termine, lo studente dovrà essere in grado di:

- Comprendere i principi fondamentali dei metodi Monte Carlo.  
- Analizzare la generazione di numeri casuali e le loro proprietà.  
- Introdurre il campionamento da distribuzioni arbitrarie.  
- Applicare il metodo Monte Carlo all’integrazione numerica.  
- Discutere il ruolo dell’errore statistico e delle tecniche di riduzione della varianza.  
- Implementare semplici esempi numerici di stima Monte Carlo.
### Struttura della lezione

1. Principio di base e stima tramite media campionaria.
2. Generazione di numeri pseudocasuali: requisiti e qualità.
3. Campionamento da distribuzioni arbitrarie.
4. Integrazione Monte Carlo (1D e multidimensionale).
5. Errore statistico e tecniche di riduzione della varianza.

---

## Fondamenti teorici

Il metodo Monte Carlo nasce dall’idea di trasformare un problema di natura **continua** --- ad esempio il calcolo di un integrale o di una media --- in un problema **discreto** basato su un insieme finito di campioni casuali.  
In pratica, si sostituisce la media teorica con una **media empirica** calcolata su un campione sufficientemente ampio di punti generati in modo casuale.

Consideriamo un integrale definito su un intervallo $[a,b]$:

$$I = \int_a^b f(x)\,dx.$$

Calcolare $I$ in modo esatto può essere difficile o impossibile se $f(x)$ è complicata o se lo spazio di integrazione ha molte dimensioni.  
Per semplificare, si effettua un **cambio di variabile lineare** che porta l’integrale su un intervallo unitario:

$$I = (b-a) \int_0^1 f[a + (b-a)u]\,du,$$

dove $u$ è una variabile uniforme in $[0,1]$.  

A questo punto si generano $N$ numeri casuali indipendenti $u_i \in [0,1)$ e si approssima l’integrale con la **media aritmetica** dei valori della funzione nei punti campionati:

$$I \simeq (b-a)\frac{1}{N}\sum_{i=1}^N f[a + (b-a)u_i].$$

Questa è la forma più semplice di **integrazione Monte Carlo**.  
Essa si basa sul principio che la media dei campioni tende alla media vera quando il numero di campioni $N$ cresce, secondo la **legge dei grandi numeri**.

---

### Interpretazione statistica

La stima Monte Carlo può essere vista come una media statistica della variabile casuale $Y = f[a + (b-a)U]$, dove $U$ è distribuita uniformemente in $[0,1]$.  
La varianza della stima è proporzionale alla varianza di $Y$ e inversamente proporzionale al numero di campioni:

$$\sigma_I^2 = (b-a)^2\frac{\sigma_f^2}{N},$$

da cui l’incertezza (errore statistico) risulta:

$$\sigma_I = (b-a)\frac{\sigma_f}{\sqrt{N}},$$

dove $\sigma_f$ è la deviazione standard dei valori di $f$.  

In altre parole, **raddoppiare la precisione richiede circa quattro volte più campioni**.  
La convergenza è quindi lenta, ma possiede un vantaggio fondamentale: **non peggiora con la dimensione del problema**.  
Questo rende il metodo Monte Carlo particolarmente efficace in spazi di grande dimensionalità, dove i metodi deterministici (come Simpson o Gauss-Legendre) diventano rapidamente impraticabili.

---

### Commento concettuale

- L’approssimazione Monte Carlo non richiede una griglia regolare di punti: i campioni casuali esplorano lo spazio in modo uniforme in media.  
- L’errore stimato è di natura **statistica**, non sistematica: può essere ridotto ma non eliminato completamente.  
- La potenza del metodo deriva dalla sua **generalità**: la stessa idea si estende facilmente a integrali multidimensionali, equazioni integrali, simulazioni di sistemi fisici complessi e generazione di configurazioni aleatorie.


## Generazione di numeri pseudocasuali

L’efficacia dei metodi Monte Carlo dipende dalla qualità dei numeri casuali utilizzati.  
Un **generatore di numeri pseudocasuali** (PRNG) produce una sequenza deterministica che approssima una distribuzione uniforme in $[0,1)$.  
Un esempio classico è il **generatore congruenziale lineare**:

$$x_{n+1} = (a x_n + c) \bmod m,$$

con parametri $a$, $c$ e $m$ scelti per massimizzare il periodo e la qualità statistica.  
Le principali proprietà desiderate sono:

- **Uniformità**: i numeri devono coprire lo spazio in modo omogeneo;  
- **Indipendenza**: l’autocorrelazione tra valori successivi deve essere minima;  
- **Lungo periodo**: la sequenza non deve ripetersi in tempi brevi.

In applicazioni scientifiche si preferiscono generatori di tipo **Mersenne Twister**, **Xorshift** o **PCG**, che garantiscono uniformità e periodi molto lunghi.

---

### Tecniche di campionamento

Nella maggior parte delle applicazioni, non è sufficiente generare numeri uniformi in $[0,1)$: è necessario ottenere campioni che seguano una **distribuzione di probabilità assegnata** $p(x)$, la quale può rappresentare una grandezza fisica, un tempo di attesa, un’energia o qualsiasi altra variabile aleatoria.

In generale, se si dispone di un generatore uniforme $U \in [0,1)$, l’obiettivo è costruire una trasformazione $X = T(U)$ tale che i valori $X$ siano distribuiti secondo $p(x)$.  
Le tecniche più comuni per ottenere ciò sono: il **metodo dell’inversione**, il **metodo di accettazione–rifiuto**, e le **tecniche di campionamento per importanza**.  
In questa lezione ci limiteremo ai primi due, che costituiscono la base di tutti gli algoritmi Monte Carlo più avanzati.

---

#### Metodo dell’inversione

Il principio di questo metodo è concettualmente semplice: la probabilità che una variabile aleatoria $X$ sia minore o uguale a un certo valore $x$ è data dalla **funzione di distribuzione cumulativa** (CDF)

$$F(x) = P(X \le x) = \int_{-\infty}^{x} p(x')\,dx'.$$

Poiché $F(x)$ cresce monotonamente da $0$ a $1$, essa è **invertibile** se $p(x)$ è continua e non nulla sull’intervallo di interesse.  
Di conseguenza, se si estrae un numero casuale $U$ distribuito uniformemente in $[0,1)$, si può definire

$$X = F^{-1}(U),$$

ottenendo un valore $X$ che segue esattamente la distribuzione $p(x)$.  

Questo procedimento consente di convertire un generatore uniforme in un generatore di qualunque distribuzione, purché la CDF sia invertibile in forma chiusa o numerica.

---

#### Esempio: distribuzione esponenziale

Si consideri la distribuzione esponenziale

$$p(x) = \lambda e^{-\lambda x}, \quad x \ge 0,$$

che descrive ad esempio i tempi di attesa tra eventi indipendenti (come decadimenti radioattivi o arrivi di particelle in un rivelatore).  
La funzione cumulativa è

$$F(x) = 1 - e^{-\lambda x}.$$

Ponendo $U = F(x)$ e risolvendo rispetto a $x$, si ottiene:

$$x = F^{-1}(U) = -\frac{1}{\lambda}\ln(1 - U).$$

Poiché $U$ è uniforme in $[0,1)$, anche $1-U$ lo è, quindi si può semplicemente scrivere

$$x = -\frac{1}{\lambda}\ln U.$$

Questo fornisce un metodo pratico e diretto per generare numeri casuali esponenzialmente distribuiti.  

In linguaggio Python:

```python
import numpy as np

U = np.random.rand(100000)
X = -np.log(U) / 2.0  # esempio con λ = 2.0
```
L’istogramma dei valori di `X` segue perfettamente la distribuzione esponenziale desiderata.

---

#### Vantaggi e limiti

* **Vantaggi**: semplice, esatto, non produce rigetti di campioni; adatto a tutte le distribuzioni con $F^{-1}$ calcolabile analiticamente o numericamente.

* **Limiti**: non sempre la funzione inversa è disponibile in forma chiusa (es. distribuzioni di Maxwell o di Planck); la valutazione numerica di $F^{-1}$ può essere costosa in termini computazionali.

---

### Metodo di accettazione–rifiuto

Quando la distribuzione $p(x)$ è complicata e non invertibile, si ricorre al metodo di **accettazione–rifiuto** (o *accept–reject method*), ideato da von Neumann.\
L’idea è confrontare $p(x)$ con una **distribuzione di riferimento** $g(x)$, dalla quale sia facile generare campioni, e che la maggiori ovunque:

p(x)≤cg(x),per ogni x,

dove $c>1$ è una costante di normalizzazione detta **fattore di sovracampionamento**.

L’algoritmo procede come segue:

1. Genera un valore $x$ secondo la distribuzione $g(x)$.

2. Genera un numero uniforme $u \in [0,1)$.

3. Se $u < \frac{p(x)}{c,g(x)}$, **accetta** $x$; altrimenti **rigetta** e ripeti il processo.

I valori accettati seguono la distribuzione desiderata $p(x)$.

---

#### Esempio: distribuzione triangolare

Supponiamo di voler campionare una distribuzione triangolare definita su $[0,1]$:

p(x)=2x,0≤x≤1.

È semplice campionare da $g(x)=1$ (uniforme in $[0,1]$) e notare che $p(x)\le 2g(x)$, quindi $c=2$.\
L’algoritmo diventa:

1. Estrai $x$ uniforme in $[0,1]$.

2. Estrai $u$ uniforme in $[0,1]$.

3. Accetta $x$ se $u < x$, altrimenti rigetta.

Il valore medio di accettazione è $1/c = 1/2$, quindi circa metà dei campioni sarà scartata.\
Nonostante lo spreco, questo metodo è estremamente versatile e applicabile a qualunque forma di $p(x)$.

---

#### Efficienza del metodo

L’efficienza complessiva è data da $1/c$, cioè dal rapporto tra l’area sotto $p(x)$ e quella sotto $c g(x)$.\
Scegliere una funzione di riferimento $g(x)$ che segua da vicino la forma di $p(x)$ riduce gli scarti e migliora la produttività del metodo.\
In situazioni reali, una buona scelta di $g(x)$ può aumentare di ordini di grandezza la velocità di simulazione.

---

#### Esempio pratico in Python


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

### Confronto tra i due metodi

| Metodo                | Principio                        | Vantaggi                                      | Limiti                                                 |
|------------------------|----------------------------------|-----------------------------------------------|---------------------------------------------------------|
| **Inversione**         | Usa $X = F^{-1}(U)$              | Semplice, esatto, senza rigetti               | Richiede l’inversa analitica o numerica di $F(x)$       |
| **Accettazione–rifiuto** | Usa una distribuzione ausiliaria $g(x)$ | Applicabile a distribuzioni complesse         | Inefficiente se il fattore di scala $c$ è grande        |

Entrambi i metodi costituiscono le fondamenta di tecniche più avanzate, come **Metropolis–Hastings** e **Gibbs sampling**, che saranno trattate nella prossima lezione.

---

### Osservazioni conclusive

- I metodi di campionamento permettono di trasformare un generatore uniforme in un generatore di distribuzioni arbitrarie.  
- Il metodo dell’inversione è ideale per distribuzioni semplici e monotone, mentre l’accettazione–rifiuto è più flessibile e adatto a distribuzioni complesse o multimodali.  
- L’efficienza del metodo di accettazione–rifiuto dipende fortemente dalla scelta della funzione ausiliaria $g(x)$ e del fattore $c$.  
- Nelle simulazioni Monte Carlo, il campionamento rappresenta la fase cruciale in cui la teoria probabilistica si traduce in **algoritmo numerico operativo**, costituendo il ponte tra formalismo matematico e implementazione computazionale.

---

## Integrazione Monte Carlo

L’integrazione Monte Carlo rappresenta una delle applicazioni più dirette e significative del metodo.  
Essa consente di stimare integrali di funzioni complesse o multidimensionali attraverso un campionamento casuale, sostituendo il calcolo analitico con una media statistica.

---

### Estensione multidimensionale

Sia $\Omega \subset \mathbb{R}^d$ un dominio $d$–dimensionale di volume finito $V(\Omega)$.  
L’obiettivo è stimare un integrale del tipo:

$$I = \int_{\Omega} f(\mathbf{x})\, d\mathbf{x}.$$

Introducendo la variabile aleatoria $\mathbf{X}$ uniformemente distribuita in $\Omega$, possiamo riscrivere:

$$I = V(\Omega)\, \mathbb{E}[f(\mathbf{X})].$$

Questo significa che l’integrale è proporzionale al valore medio di $f$ calcolato su punti distribuiti uniformemente nel dominio.  
La stima Monte Carlo corrispondente è:

$$I \simeq \frac{V(\Omega)}{N}\sum_{i=1}^{N} f(\mathbf{x}_i),$$

dove $\mathbf{x}_i$ sono campioni casuali indipendenti uniformi in $\Omega$.

Questo approccio si estende naturalmente a qualunque dimensione: il numero di campioni $N$ necessario per ottenere una precisione fissata **non dipende dalla dimensione $d$**, in contrasto con i metodi deterministici, che richiedono un numero di punti proporzionale a $n^d$.  
Questo è il motivo per cui il metodo Monte Carlo è la tecnica elettiva per l’integrazione in spazi ad alta dimensionalità, ad esempio in fisica statistica (calcolo di medie d’ensemble), in finanza (pricing di derivati multidimensionali) e in meccanica statistica (stima dell’energia media di un sistema).

---

### Interpretazione geometrica

L’idea di fondo può essere vista in termini di probabilità geometrica: stimare un integrale equivale a stimare la **frazione di punti che “cadono” in una regione pesata** dalla funzione $f$.  

Nel caso di una funzione $f(\mathbf{x}) \ge 0$, si può interpretare l’integrale come il volume sotto la superficie $z = f(\mathbf{x})$.  
Campionando punti uniformi $(\mathbf{x}_i, z_i)$ in un parallelepipedo di base $\Omega$ e altezza $f_{\text{max}}$, la proporzione di punti con $z_i < f(\mathbf{x}_i)$ fornisce una stima diretta dell’integrale relativo a $f$.

#### Esempio: stima di $\pi$

Un esempio classico è la stima di $\pi$ con un metodo geometrico.  
Si consideri un quadrato unitario $[0,1]^2$ che contiene un quarto di cerchio di raggio 1.  
L’area del quarto di cerchio è $\pi/4$, mentre l’area del quadrato è 1.  

Generando $N$ punti uniformi $(x_i, y_i)$ nel quadrato, si calcola la frazione di punti che soddisfano $x_i^2 + y_i^2 \le 1$.  
Denotando con $N_{\text{cerchio}}$ il numero di punti interni al quarto di cerchio, si ha:

$$\frac{N_{\text{cerchio}}}{N_{\text{totale}}} \simeq \frac{\pi}{4},
\qquad
\pi \simeq 4 \frac{N_{\text{cerchio}}}{N_{\text{totale}}}.$$

Questo esempio mostra come un concetto geometrico (rapporto di aree) e una procedura probabilistica (conteggio di eventi) coincidano perfettamente nel quadro Monte Carlo.

---

### Analisi dell’errore

Il valore stimato dell’integrale può essere visto come una media di variabili casuali indipendenti:

$$\bar{f}_N = \frac{1}{N}\sum_{i=1}^{N} f(\mathbf{x}_i).$$

Dalla teoria della probabilità segue che la media empirica è una variabile aleatoria con media $\langle f \rangle$ e varianza:

$$\mathrm{Var}(\bar{f}_N) = \frac{\mathrm{Var}(f)}{N}.$$

L’incertezza associata alla stima dell’integrale è quindi:

$$\sigma_I = V(\Omega) \frac{\sigma_f}{\sqrt{N}},$$

dove $\sigma_f$ è la deviazione standard dei valori di $f$ campionati.

#### Cause di fluttuazione
- **Campionamento finito:** un numero limitato di campioni introduce rumore statistico.  
- **Distribuzione non uniforme:** se $f$ ha regioni a grande variabilità, i campioni casuali possono non esplorarle in modo equilibrato.  
- **Correlazione:** se i punti non sono indipendenti (ad esempio, in simulazioni Markoviane), la varianza effettiva cresce.

In tutti i casi, l’errore si riduce lentamente ma in modo prevedibile con $1/\sqrt{N}$, permettendo di stimare direttamente la precisione dai dati stessi.

---

### Tecniche di riduzione della varianza

Poiché la convergenza è lenta, una parte fondamentale dell’efficienza del metodo Monte Carlo consiste nel ridurre la varianza **senza aumentare $N$**.  
Le principali strategie sono:

#### Campionamento stratificato
Il dominio $\Omega$ viene suddiviso in sottoinsiemi (strati) di uguale misura, e si genera un punto casuale in ciascuno di essi.  
In questo modo si evita che i punti si concentrino casualmente in una sola zona, migliorando l’uniformità del campionamento.

#### Importance sampling
Si sceglie una distribuzione di probabilità $q(\mathbf{x})$ che approssimi la forma di $|f(\mathbf{x})|$, e si campiona secondo $q$ invece che uniformemente.  
L’integrale diventa:

$$I = \int_{\Omega} \frac{f(\mathbf{x})}{q(\mathbf{x})} q(\mathbf{x})\,d\mathbf{x}
   \simeq \frac{1}{N}\sum_{i=1}^{N} \frac{f(\mathbf{x}_i)}{q(\mathbf{x}_i)}.$$

In questo modo i campioni sono concentrati nelle regioni più rilevanti, riducendo la fluttuazione statistica.

#### Antithetic variates
Si usano coppie di campioni correlati in modo controllato.  
Per esempio, se si genera $u \in [0,1)$, si può considerare anche $1-u$ come campione complementare.  
Le due valutazioni di $f$ tendono ad avere errori opposti, la cui media è più stabile.

---

### Applicazione pratica

Come esempio semplice, si può stimare l’integrale

$$I = \int_0^1 e^{-x^2}\,dx$$

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
La precisione cresce come $\sqrt{N}$, e il confronto con metodi deterministici (es. Simpson) mostra che, per funzioni in bassa dimensione, il metodo Monte Carlo è meno efficiente ma molto più generale.

---

## Collegamento con i metodi successivi

L’integrazione Monte Carlo è in realtà un caso particolare del **calcolo di medie d’ensemble** su una distribuzione di probabilità.  
Molti problemi fisici o statistici --- come la stima di osservabili in un sistema termico o di valori attesi in una catena di Markov --- si riducono allo stesso principio generale:

$$\langle A \rangle = \int A(x)\, p(x)\,dx \simeq \frac{1}{N}\sum_{i=1}^{N} A(x_i),$$

dove $x_i$ sono campioni estratti secondo la distribuzione $p(x)$.

Le lezioni successive mostreranno come generare tali campioni quando $p(x)$ non è nota in forma analitica, ma è definita in modo implicito --- ad esempio tramite un potenziale, un’energia di sistema o una probabilità di transizione.  
Questo condurrà naturalmente ai **metodi di campionamento Markoviano** (come Metropolis–Hastings), ai **processi di simulazione di eventi discreti** e ai **metodi di dinamica molecolare stocastica**, che estendono il principio Monte Carlo a dinamiche dipendenti dal tempo e distribuzioni non uniformi.

## Riferimenti

* Kalos, M. H., Whitlock, P. A. *Monte Carlo Methods*. Wiley.

* Binder, K., Heermann, D. *Monte Carlo Simulation in Statistical Physics*. Springer.

* Fishman, G. S. *Monte Carlo: Concepts, Algorithms, and Applications*. Springer.

* Kroese, D. P., Brereton, T., Taimre, T., Botev, Z. I. (2014). *Why the Monte Carlo method is so important today*. *Wiley Interdisciplinary Reviews: Computational Statistics*.

* Metropolis, N., Ulam, S. (1949). *The Monte Carlo Method*. *Journal of the American Statistical Association*.

---

\newpage

## Appendice: Dimostrazione del metodo dell’inversione

L’idea fondamentale del metodo dell’inversione è che, se $U$ è una variabile uniforme in $[0,1)$ e si definisce $X = F^{-1}(U)$, allora $X$ è distribuita secondo la distribuzione di probabilità avente funzione cumulativa $F(x) = P(X \le x)$.  
Questo risultato, apparentemente semplice, può essere dimostrato in modo rigoroso utilizzando la definizione di funzione di distribuzione e la formula della derivata dell’inversa.

---

### Dimostrazione tramite la funzione di ripartizione

Sia $F(x)$ una funzione di distribuzione cumulativa (CDF) strettamente crescente e continua, dunque invertibile.  
Per ogni $x$ reale, consideriamo:

$$P(X \le x) = P(F^{-1}(U) \le x).$$

Poiché $F$ è crescente, l’inequazione $F^{-1}(U) \le x$ equivale a $U \le F(x)$.  
Dato che $U$ è uniforme in $[0,1)$, vale:

$$P(U \le F(x)) = F(x).$$

Pertanto, la distribuzione cumulativa della variabile $X = F^{-1}(U)$ coincide con $F(x)$:  
$$P(X \le x) = F(x).$$

Questo mostra che $X$ ha proprio la distribuzione desiderata.

---

### Dimostrazione differenziale: uso della derivata dell’inversa

Supponiamo ora che $F$ sia una funzione derivabile e strettamente crescente, con densità $p(x) = F'(x) > 0$.  
Definiamo nuovamente $X = F^{-1}(U)$, dove $U$ è uniforme in $[0,1)$.  
Poiché $U = F(X)$, derivando entrambi i membri otteniamo:

$$\frac{dU}{dX} = F'(X) = p(X).$$

Applicando la regola della derivata dell’inversa, si ha:

$$\frac{dX}{dU} = \frac{1}{F'(X)} = \frac{1}{p(X)}.$$

Ora, per una trasformazione monotona $U \mapsto X$, la densità si trasforma come:

$$f_X(x) = f_U(u) \left|\frac{dU}{dX}\right| = f_U(F(x)) \, p(x).$$

Poiché $f_U(u) = 1$ per $u \in [0,1)$, segue immediatamente che:

$$f_X(x) = p(x).$$

Quindi la variabile $X = F^{-1}(U)$ possiede esattamente la densità desiderata.

---

### Caso generale: l’inversa generalizzata (quantile function)

Quando $F$ non è strettamente crescente o presenta tratti piatti (come nelle distribuzioni discrete o miste), l’inversa classica non esiste in senso stretto.  
Si definisce allora la **funzione quantile** o **inversa generalizzata**:

$$F^{-1}(u) = \inf \{x \in \mathbb{R} : F(x) \ge u\}, \quad u \in (0,1).$$

Se $U \sim \mathrm{Unif}(0,1)$ e $X = F^{-1}(U)$, si verifica comunque che:

$$P(X \le x) = P(F^{-1}(U) \le x) = P(U \le F(x)) = F(x).$$

Dunque, anche nel caso discreto o misto, la definizione mantiene la proprietà fondamentale.

---

### Condizioni di validità e considerazioni pratiche

- **Monotonia:** $F$ deve essere non decrescente (condizione intrinseca per ogni CDF).  
  La stretta crescita e la derivabilità sono richieste solo per usare la formula della derivata dell’inversa.

- **Supporto:** la relazione $P(X \le x) = F(x)$ è valida per $x$ appartenenti al dominio di definizione di $F$.  
  Fuori dal supporto, vale $P(X \le x) = 0$ per $x < \inf \mathrm{supp}(F)$ e $1$ per $x > \sup \mathrm{supp}(F)$.

- **Implementazione numerica:** quando $F^{-1}$ non è nota in forma chiusa, si può calcolare per via numerica (tabulazione, interpolazione monotona, metodi di bisezione o Newton).  
  Per evitare instabilità numeriche, si evita di usare direttamente $U$ troppo vicino a $0$ o $1$ (si può usare $U \in [\varepsilon, 1-\varepsilon]$ con $\varepsilon$ piccolo).

---

### Esempio di verifica: distribuzione esponenziale

Consideriamo $p(x) = \lambda e^{-\lambda x}$ per $x \ge 0$.  
La funzione cumulativa è:

$$F(x) = 1 - e^{-\lambda x}.$$

Il metodo dell’inversione dà:

$$X = F^{-1}(U) = -\frac{1}{\lambda} \ln(1 - U).$$

Poiché $U$ è uniforme in $[0,1)$, anche $1-U$ lo è, e dunque:

$$P(X \le x) = P\left(-\frac{1}{\lambda}\ln(1-U) \le x\right)
= P(U \le 1 - e^{-\lambda x}) = 1 - e^{-\lambda x} = F(x).$$

Infine, derivando $F(x)$ si ottiene $F'(x) = \lambda e^{-\lambda x} = p(x)$, confermando che la variabile generata con $X = -\frac{1}{\lambda} \ln(1-U)$ segue la distribuzione esponenziale attesa.

---

### Sintesi concettuale

- Il metodo dell’inversione funziona perché applicare $F^{-1}$ a una variabile uniforme trasforma l’uniforme in una variabile con distribuzione $F$.  
- La dimostrazione si basa sulla relazione $P(U \le F(x)) = F(x)$ e sulla formula della derivata dell’inversa.  
- È un metodo esatto e generale, purché si possa valutare o approssimare $F^{-1}$.  
- In molti casi pratici, le funzioni di quantile tabulate o le librerie numeriche implementano questa trasformazione in modo efficiente.
