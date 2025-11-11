---
title: "Equazioni tipo Langevin ed Euler–Maruyama"
author: ""
date: ""
---

# Equazioni tipo Langevin ed Euler–Maruyama

(Obiettivi della lezione: comprendere la dinamica stocastica continua e la discretizzazione numerica di processi rumorosi, con applicazioni a sistemi fisici e modelli simulativi.)

---

## Introduzione

Le equazioni di tipo Langevin rappresentano un ponte tra la descrizione deterministica e quella stocastica di sistemi dinamici. Esse modellano l’evoluzione temporale di grandezze fisiche o astratte soggette a forze regolari e a rumore casuale.  
La parte finale della lezione sarà dedicata al metodo di discretizzazione di Euler–Maruyama, strumento essenziale per la simulazione numerica di equazioni differenziali stocastiche (SDE).

### Obiettivi didattici specifici

1. Comprendere il significato fisico e matematico dell’equazione di Langevin.
2. Analizzare la relazione tra Langevin e l’equazione di Fokker–Planck.
3. Introdurre la formulazione generale di un’equazione differenziale stocastica (SDE).
4. Derivare il metodo di Euler–Maruyama per l’integrazione numerica di SDE.
5. Confrontare l’approssimazione stocastica con quella deterministica classica.
6. Applicare il metodo a semplici casi di moto browniano e pozzetti potenziali.

### Struttura della lezione

La lezione è articolata in 5 parti principali:

1. **Motivazioni fisiche e modellistiche**  
   Dal moto browniano alle equazioni di Langevin: forze deterministiche e rumore.

2. **Forma generale dell’equazione di Langevin**  
   Scrittura in forma differenziale e interpretazione dei termini.

3. **Equazioni differenziali stocastiche (SDE)**  
   Formalismo di Itô e Stratonovich, interpretazione e connessione con la Fokker–Planck.

4. **Discretizzazione numerica: metodo di Euler–Maruyama**  
   Derivazione e implementazione algoritmica.

5. **Esempi e simulazioni**  
   Moto browniano libero e particella in un potenziale armonico.

### Conclusione introduttiva

Lo studio dell’equazione di Langevin e delle sue discretizzazioni fornisce le basi per comprendere i modelli di dinamica stocastica utilizzati in fisica, chimica, finanza e biologia, nonché le tecniche computazionali necessarie per la loro analisi numerica.

---

## 1. Motivazioni fisiche e modellistiche

Il punto di partenza è la descrizione del **moto browniano**, fenomeno osservato per la prima volta da Robert Brown (1827) come movimento irregolare di piccole particelle sospese in un fluido.  
A livello microscopico, tale comportamento è dovuto agli **urti casuali** tra la particella e le molecole del fluido, che trasferiscono quantità di moto in modo disordinato.

Einstein (1905) e Smoluchowski (1906) mostrarono come questo moto potesse essere descritto in termini probabilistici, collegando la **diffusione macroscopica** osservata alla **fluttuazione microscopica** delle forze esercitate dalle molecole.  
Questa idea fu poi formalizzata da Paul Langevin (1908) in un’equazione dinamica che combina una forza deterministica e una forza casuale, introducendo così un ponte tra la meccanica classica e la descrizione statistica dei sistemi.

Consideriamo una particella di massa $m$ e velocità $v(t)$.  
L’equazione di Langevin nella forma più semplice è:

$$
m \frac{dv}{dt} = -\gamma v + \sqrt{2D\gamma^2}\,\eta(t)
$$

Il significato fisico dei termini è il seguente:

- **$-\gamma v$** è la **forza di attrito viscoso**, proporzionale e opposta alla velocità; rappresenta la perdita di energia dovuta all’interazione con il fluido.  
- **$\sqrt{2D\gamma^2}\,\eta(t)$** è la **forza stocastica**: un termine casuale che descrive l’effetto combinato di molti urti microscopici indipendenti.  
  Il fattore $\sqrt{2D\gamma^2}$ regola l’intensità del rumore, e $D$ è il **coefficiente di diffusione**.

Il processo $\eta(t)$ rappresenta **rumore bianco gaussiano**, caratterizzato da media nulla e correlazione delta:

$$
\langle \eta(t) \rangle = 0, \qquad 
\langle \eta(t)\eta(t') \rangle = \delta(t - t').
$$

Queste proprietà implicano che i valori del rumore in tempi diversi sono indipendenti, e che l’ampiezza delle fluttuazioni è costante nel tempo.

---

### Dal moto della velocità al moto della posizione

Integrando nel tempo la velocità, si ottiene la posizione $x(t)$ della particella:

$$
\frac{dx}{dt} = v(t).
$$

Combinando le due equazioni, si ottiene un sistema accoppiato di equazioni differenziali stocastiche che descrive sia la **dissipazione** (dovuta all’attrito) sia la **fluttuazione** (dovuta al rumore).  
Questo dualismo è alla base del cosiddetto **principio di fluttuazione–dissipazione**, che stabilisce un legame profondo tra la quantità di rumore nel sistema e la sua tendenza a rilassarsi verso l’equilibrio termico.

---

### Interpretazione intuitiva

- Se $\gamma$ è grande, l’attrito domina: la particella si muove lentamente e il suo moto è fortemente smorzato.  
- Se $D$ è grande, le fluttuazioni sono intense e la traiettoria della particella appare molto irregolare.  
- Nel limite in cui l’inerzia è trascurabile ($m \to 0$), si ottiene il cosiddetto **moto browniano sovra-smorzato**, descritto da un’equazione di Langevin solo per la posizione.

Queste idee costituiscono il punto di partenza per lo studio delle **equazioni differenziali stocastiche** e per i metodi di integrazione numerica come quello di **Euler–Maruyama**, che verranno introdotti nelle sezioni successive.


## 2. Forma generale dell’equazione di Langevin

L’equazione di Langevin può essere generalizzata a sistemi multidimensionali e a forme più astratte.  
In un sistema di coordinate $\mathbf{x}(t) = (x_1(t), \dots, x_n(t))$, la dinamica stocastica è descritta da:

$$
\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x},t) + \mathbf{G}(\mathbf{x},t)\,\boldsymbol{\eta}(t),
$$

dove:

- $\mathbf{f}(\mathbf{x},t)$ è il **campo di forze deterministiche**, cioè il termine regolare che descrive la dinamica media o sistematica del sistema;  
- $\mathbf{G}(\mathbf{x},t)$ è una **matrice di accoppiamento** che modula l’intensità e la direzione del rumore in ciascuna componente;  
- $\boldsymbol{\eta}(t) = (\eta_1(t), \dots, \eta_m(t))$ è un **vettore di processi di rumore bianco**, ciascuno con le proprietà: $$\langle \eta_i(t) \rangle = 0, \qquad  \langle \eta_i(t)\eta_j(t') \rangle = \delta_{ij}\,\delta(t - t')\;.$$

### Rumore additivo e rumore moltiplicativo

A seconda della dipendenza del termine di rumore da $\mathbf{x}$, si distinguono due casi:

1. **Rumore additivo**  
   $\mathbf{G}$ è costante: l’intensità del rumore non dipende dallo stato del sistema.  
   L’equazione assume la forma: $$\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x},t) + \mathbf{G}\,\boldsymbol{\eta}(t)\;,$$e le fluttuazioni agiscono in modo uniforme su tutto il dominio.  
   È il caso tipico del moto browniano libero o del moto in un potenziale armonico.

2. **Rumore moltiplicativo**  
  $\mathbf{G}$ dipende da $\mathbf{x}$ o da $t$: l’intensità del rumore varia nello spazio o nel tempo.  
   Si tratta di un caso più complesso, in cui il rumore interagisce con la dinamica del sistema e può generare fenomeni come **rumore indotto**, **trasporto stocastico** o **transizioni rumorose**.  
   In questo caso diventa fondamentale specificare l’interpretazione dell’integrale stocastico (Itô o Stratonovich, vedi sezione successiva).

---

### Significato fisico dei termini

L’equazione di Langevin rappresenta il bilancio tra due meccanismi fondamentali:

- **Determinismo locale**: la forza $\mathbf{f}(\mathbf{x},t)$ guida la traiettoria verso l’equilibrio o la direzione imposta da un potenziale.  
  Ad esempio, nel caso di una particella in un campo di forza $\mathbf{F}(\mathbf{x}) = -\nabla U(\mathbf{x})$, si ha: $$\mathbf{f}(\mathbf{x}) = \frac{\mathbf{F}(\mathbf{x})}{\gamma} = -\frac{1}{\gamma}\nabla U(\mathbf{x})\;,$$dove $\gamma$ è il coefficiente di attrito.

- **Fluttuazioni casuali**: la parte $\mathbf{G}(\mathbf{x},t)\boldsymbol{\eta}(t)$ descrive gli urti microscopici o le perturbazioni ambientali che introducono incertezza nella traiettoria.  
  Queste fluttuazioni sono responsabili della **diffusione** nello spazio delle configurazioni.

La combinazione di questi due effetti genera un **cammino stocastico** che, nel lungo tempo, dà origine a una distribuzione di probabilità $P(\mathbf{x},t)$ delle configurazioni del sistema.

---

### Quantità statistiche associate

Per descrivere in modo sintetico l’evoluzione del sistema si considerano alcune grandezze medie fondamentali:

- **Valore atteso (media):** $$\langle \mathbf{x}(t) \rangle = \int \mathbf{x}\, P(\mathbf{x},t)\, d\mathbf{x}\;.$$
- **Varianza o covarianza:** $$\langle (\mathbf{x}(t) - \langle \mathbf{x}(t) \rangle)(\mathbf{x}(t) - \langle \mathbf{x}(t) \rangle)^{T} \rangle\;,$$che misura l’ampiezza delle fluttuazioni.
  
- **Distribuzione di probabilità $P(\mathbf{x},t)$**: evolve nel tempo secondo una equazione detta di *Fokker–Planck* (vedi appendice), che deriva direttamente dalla forma di Langevin.

---

## 3. Equazioni differenziali stocastiche (SDE)

Le **equazioni differenziali stocastiche** (SDE, *Stochastic Differential Equations*) rappresentano la formalizzazione matematica dell’equazione di Langevin.  
Esse permettono di descrivere quantitativamente sistemi dinamici soggetti a **rumore aleatorio continuo nel tempo**.

L’idea di fondo è estendere le equazioni differenziali ordinarie (ODE) per includere, oltre al termine deterministico, un contributo dovuto al rumore, modellato tramite il **moto browniano** o processi affini.

---

### 3.1 Dal deterministico allo stocastico

Consideriamo una ODE per una variabile $x(t)$:

$$
\frac{dx}{dt} = a(x,t),
$$

dove $a(x,t)$ è il campo di velocità o drift deterministico.  
La soluzione, in forma integrale, è:

$$
x(t+\Delta t) = x(t) + \int_t^{t+\Delta t} a(x(s),s)\,ds.
$$

Per introdurre l’effetto di fluttuazioni casuali, Langevin propose di aggiungere un termine di rumore $\xi(t)$:

$$
\frac{dx}{dt} = a(x,t) + b(x,t)\,\xi(t),
$$

dove $\xi(t)$ è un processo casuale con media nulla e correlazione delta $\langle \xi(t)\xi(t') \rangle = \delta(t-t')$.  
Poiché $\xi(t)$ è formalmente “troppo irregolare” per essere trattato come una funzione classica, si introduce il **moto browniano** $W_t$ come sua *primitiva stocastica*: come vedremo $\xi(t)$ si comporta come la derivata di $W_t$.

---

### 3.2 Il moto browniano come integratore stocastico

Il **moto browniano standard** (o processo di Wiener) $W_t$ è un processo stocastico continuo che svolge, nel calcolo stocastico, un ruolo analogo a quello dell’integrale nel calcolo classico.

Esso è definito dalle proprietà fondamentali:

1. $W_0 = 0$;
2. Gli incrementi $W_{t+\Delta t} - W_t$ sono **indipendenti** e **gaussiani** con media nulla;
3. La varianza cresce linearmente nel tempo: $$\langle (W_{t+\Delta t} - W_t)^2 \rangle = \Delta t\,;$$
4. Le traiettorie sono continue ma **non derivabili quasi mai**.

---

Poiché le fluttuazioni $\xi(t)$ introdotte da Langevin sono “troppo irregolari” per essere trattate come una funzione classica, si definisce $W_t$ come la **primitiva stocastica** di $\xi(t)$, cioè un processo tale che:

$$
dW_t = \xi(t)\,dt
\quad \text{oppure in forma integrale:} \quad
W_t = \int_0^t \xi(s)\,ds.
$$

Questa relazione va intesa **in senso simbolico**:  
$W_t$ gioca il ruolo di una “somma cumulativa” degli impulsi casuali $\xi(t)$,  
mentre $\xi(t)$ è la **derivata formale** del moto browniano, ossia un *rumore bianco* che non esiste come funzione ordinaria ma solo come oggetto distribuzionale.

---

### Interpretazione intuitiva

- In un intervallo infinitesimo $dt$, l’incremento $dW_t$ è una variabile casuale gaussiana con media nulla e varianza $dt$: $$dW_t \sim \mathcal{N}(0,dt)\,.$$  
  Si può pensare a $W_t$ come alla traiettoria casuale di una particella che subisce urti infinitesimali, mentre $\xi(t)$ rappresenta la successione istantanea e irregolare di tali urti.

- Formalmente, se $\xi(t)$ fosse una funzione “ben comportata”, varrebbe $\frac{dW_t}{dt} = \xi(t)$, ma in realtà $\xi(t)$ non è definita punto per punto: solo i suoi **integrali nel tempo** hanno significato matematico.  
  Per questo motivo si lavora direttamente con $dW_t$, cioè con gli **incrementi** del moto browniano, anziché con il rumore bianco $\xi(t)$ stesso.

---

### Collegamento operativo

Ogni integrale stocastico del tipo

$$
\int_0^t b(x_s,s)\,dW_s
$$

va quindi interpretato come una **somma di contributi casuali infinitesimi**, analogamente a un integrale di Riemann, ma dove gli incrementi $dW_s$ sono variabili gaussiane indipendenti.  
Il calcolo differenziale classico non si applica direttamente, e occorrono regole nuove — quelle del **calcolo di Itô** — per trattare prodotti e derivate di questi incrementi.

---

In sintesi:
- $\xi(t)$ è il **rumore bianco** (un oggetto distribuzionale non regolare),
- $W_t$ è la **primitiva stocastica** (il suo integrale cumulativo),
- $dW_t$ rappresenta un incremento aleatorio di ampiezza $\sqrt{dt}$,
- e le **SDE** utilizzano proprio $dW_t$ per modellizzare in modo rigoroso l’effetto del rumore continuo.


### 3.3 Forma differenziale di una SDE

Utilizzando $dW_t$ come elemento di integrazione stocastica, una SDE in **notazione di Itô** si scrive:

$$
dx_t = a(x_t,t)\,dt + b(x_t,t)\,dW_t,
$$

dove:

- $a(x_t,t)$ è il **termine di drift** (deterministico),
- $b(x_t,t)$ è il **coefficiente di diffusione** (ampiezza del rumore),
- $dW_t$ rappresenta un incremento casuale del moto browniano.

Nel caso multidimensionale, la SDE diventa:

$$
d\mathbf{x}_t = \mathbf{a}(\mathbf{x}_t,t)\,dt + \mathbf{B}(\mathbf{x}_t,t)\,d\mathbf{W}_t,
$$

con $\mathbf{B}$ matrice $n\times m$ e $\mathbf{W}_t$ vettore di $m$ moti browniani indipendenti.

---

### 3.4 Interpretazioni: Itô e Stratonovich

L’integrale stocastico $\int b(x_t,t)\,dW_t$ **non è un integrale ordinario**, poiché $W_t$ non è differenziabile.  
Esistono quindi diverse **convenzioni di interpretazione**, che differiscono per il punto dell’intervallo $(t, t+\Delta t)$ in cui si valuta la funzione $b(x_t,t)$.

| Interpretazione | Punto di valutazione | Caratteristiche principali |
|:-----------------|:--------------------|:----------------------------|
| **Itô** | Valutazione all’inizio: $b(x_t,t)$ | Formulazione matematica rigorosa; non valida la regola classica della catena, ma esiste il lemma di Itô |
| **Stratonovich** | Valutazione nel punto medio: $b(x_{t+\Delta t/2},t+\Delta t/2)$ | Preserva la regola della catena; preferita in fisica per sistemi derivati da limiti di processi a rumore colorato |

Le due formulazioni sono equivalenti ma **non identiche**.  
Si possono trasformare l’una nell’altra tramite la relazione:

$$
a_{\text{Strat}}(x,t) = a_{\text{Itô}}(x,t) - \frac{1}{2}b(x,t)\frac{\partial b(x,t)}{\partial x}.
$$

Questo termine correttivo è detto **“drift di Itô”** e tiene conto del contributo medio dovuto alla curvatura della funzione $b(x,t)$ nel dominio di rumore.

---

### 3.5 Significato fisico e geometrico

- In **Itô**, gli incrementi $\Delta W_t$ sono considerati “futuri” rispetto al valore di $x(t)$: il rumore è *anticipato*, e il processo è **non anticipativo** (nessuna informazione futura).  
  È la scelta naturale per modelli economici o simulazioni numeriche.

- In **Stratonovich**, l’incremento è valutato a metà intervallo, quindi tiene conto parzialmente della retroazione del rumore sul sistema.  
  Questa interpretazione è coerente con i limiti di processi fisici con **rumore colorato a tempo di correlazione finito**.

Visivamente, si può pensare che:
- in Itô, $b(x_t,t)$ sia “congelato” all’inizio dell’intervallo;
- in Stratonovich, $b$ si aggiorni continuamente, generando un effetto medio aggiuntivo.

---

### 3.6 Esempio: moto browniano con deriva

Consideriamo la SDE:

$$
dx_t = \mu\,dt + \sigma\,dW_t,
$$

dove $\mu$ è la velocità media (drift costante) e $\sigma$ l’intensità del rumore.  
Integrando, si ottiene:

$$
x_t = x_0 + \mu t + \sigma W_t.
$$

Le proprietà del moto browniano implicano:

$$
\langle x_t \rangle = x_0 + \mu t, \qquad 
\mathrm{Var}[x_t] = \sigma^2 t.
$$

Pertanto, la media cresce linearmente, mentre la varianza cresce nel tempo: il sistema non si stabilizza, ma **diffonde**.

La distribuzione associata è gaussiana:

$$
P(x,t) = \frac{1}{\sqrt{2\pi\sigma^2 t}}
\exp\!\left[-\frac{(x - x_0 - \mu t)^2}{2\sigma^2 t}\right].
$$

Questo semplice esempio illustra come una SDE definisca, in modo naturale, un processo aleatorio continuo con proprietà statistiche calcolabili.

---

### 3.8 Sintesi concettuale

| **Elemento** | **Significato** | **Formula tipica** |
|:--------------|:----------------|:-------------------|
| Drift deterministico | Effetto sistematico o “forza media” | $a(x_t,t)\,dt$ |
| Diffusione stocastica | Rumore casuale proporzionale a $\sqrt{dt}$ | $b(x_t,t)\,dW_t$ |
| Moto browniano | Processo gaussiano con varianza lineare nel tempo | $\langle W_t^2 \rangle = t$ |
| Itô vs Stratonovich | Scelta del punto di valutazione del rumore | Differiscono per un termine $-\frac{1}{2}b\partial_x b$ |
| Legame con FP | Evoluzione della distribuzione $P(x,t)$ | $\partial_t P = -\partial_x(aP) + \frac{1}{2}\partial_x^2(b^2P)$ |

---

Questa formalizzazione fornisce il linguaggio matematico per trattare sistemi stocastici continui.  
Nelle sezioni successive si introdurranno le **tecniche di discretizzazione numerica**, in particolare il metodo di **Euler–Maruyama**, che consente di simulare al calcolatore le soluzioni approssimate delle SDE.



## 4. Discretizzazione numerica: metodo di Euler–Maruyama

Il metodo di Euler–Maruyama è la generalizzazione stocastica dell’integrazione di Eulero per SDE:

$$
x_{n+1} = x_n + a(x_n,t_n)\,\Delta t + b(x_n,t_n)\,\Delta W_n,
$$

dove $\Delta W_n$ è un incremento del moto browniano simulato come $\sqrt{\Delta t}\,\mathcal{N}(0,1)$.

### Schema algoritmico

1. Fissare il passo $\Delta t$ e il numero di iterazioni $N$.
2. Inizializzare $x_0$.
3. Per ogni $n=0,\dots,N-1$:
   - generare $\xi_n \sim \mathcal{N}(0,1)$,
   - calcolare $\Delta W_n = \sqrt{\Delta t}\,\xi_n$,
   - aggiornare $x_{n+1} = x_n + a(x_n,t_n)\Delta t + b(x_n,t_n)\Delta W_n$.

---

#### Esempio: moto browniano libero

```python
import numpy as np
import matplotlib.pyplot as plt

T = 10.0
dt = 0.01
N = int(T/dt)
x = np.zeros(N)
for n in range(N-1):
    xi = np.random.normal(0, 1)
    x[n+1] = x[n] + np.sqrt(2*dt) * xi

t = np.linspace(0, T, N)
plt.plot(t, x)
plt.xlabel("t")
plt.ylabel("x(t)")
plt.title("Traiettoria di moto browniano (Euler–Maruyama)")
plt.show()
````

---

## 5. Il ruolo interdisciplinare delle equazioni di Langevin

L’equazione di Langevin rappresenta uno dei modelli concettualmente più fertili della scienza moderna.  
Nata nel contesto della fisica statistica, essa è oggi riconosciuta come un **principio unificante** per la descrizione di dinamiche complesse in cui coesistono ordine e fluttuazione, struttura e caso, determinismo e incertezza.

Dal punto di vista formale, la sua generalità risiede nella decomposizione: $$\frac{dx}{dt} = a(x,t) + b(x,t),\eta(t)\;,$$dove $a(x,t)$ esprime la **tendenza sistematica** (drift) e $b(x,t)\eta(t)$ la **perturbazione casuale**.  
Tale struttura elementare si presta a modellizzare un’ampia gamma di fenomeni, anche lontani dalla fisica, purché caratterizzati da una competizione fra regolarità e rumore.

---

### 5.1 Economia e finanza

Nel mondo economico e finanziario, le equazioni di Langevin descrivono la fluttuazione continua dei prezzi, dei tassi o delle quantità aggregate.

- **Moto browniano geometrico (GBM)**  
  Modello classico per l’evoluzione di un prezzo $S_t$: $$dS_t = \mu S_t\,dt + \sigma S_t\,dW_t\;.$$
  Il termine $\mu S_t$ rappresenta la crescita media attesa (trend), mentre $\sigma S_t\,dW_t$ modella le variazioni casuali di mercato.  
  Il logaritmo del prezzo segue una distribuzione gaussiana, e il processo dà luogo alla famosa formula di Black–Scholes per la valutazione delle opzioni.

- **Dinamiche di volatilità stocastica**  
  Nei modelli di Heston o Ornstein–Uhlenbeck per la volatilità $\nu_t$: $$d\nu_t = \kappa(\theta - \nu_t)\,dt + \xi\sqrt{\nu_t}\,dW_t\;,$$
  la forza di richiamo $\kappa(\theta - \nu_t)$ stabilizza il processo attorno a un valore medio $\theta$, mentre il rumore amplifica le fluttuazioni.  
  È un tipico esempio di *Langevin con forza di richiamo*.

---

### 5.2 Sociologia, psicologia e scienze cognitive

In ambito sociale e cognitivo, il formalismo di Langevin viene impiegato per modellizzare decisioni, opinioni e processi di apprendimento soggetti a incertezza.

- **Modelli di opinione con rumore sociale**  
  Si consideri la dinamica di un’opinione media $x(t)$ influenzata da conformismo e rumore: $$\frac{dx}{dt} = -\lambda (x - x_0) + \sqrt{2D}\,\eta(t)\;,$$dove $x_0$ è il valore di consenso e $\lambda$ la forza di conformismo.  
  Le fluttuazioni rappresentano rumore informativo, esposizione casuale a contenuti o interazioni impreviste.  
  In equilibrio si ottiene una distribuzione di opinioni centrata su $x_0$ con varianza proporzionale a $D/\lambda$.

- **Dinamiche cognitive o decisionali rumorose**  
  Processi come il *decision making under uncertainty* o la *drift-diffusion theory* nei tempi di risposta psicologici sono descritti da: $$dx_t = \mu\,dt + \sigma\,dW_t\;,$$
  dove $\mu$ misura la tendenza verso una scelta e $\sigma$ l’intensità delle fluttuazioni interne (rumore neurale o indecisione).  
  Le traiettorie rappresentano l’accumulo di evidenza fino a una soglia di decisione.

---

### 5.3 Ecologia e biologia dei sistemi

In ecologia e biologia quantitativa, le equazioni di Langevin modellizzano la variabilità ambientale, le fluttuazioni demografiche e le interazioni fra popolazioni.

- **Dinamiche di popolazione stocastiche (Verhulst–Langevin)**  
  Versione rumorosa dell’equazione logistica: $$\frac{dN}{dt} = rN\!\left(1-\frac{N}{K}\right) + \sqrt{2D\,N^2}\,\eta(t)\;,$$dove $r$ è il tasso di crescita e $K$ la capacità portante.  
  Il termine rumoroso cattura le fluttuazioni ecologiche o ambientali che influenzano la riproduzione e la mortalità.  
  La diffusione moltiplicativa $D\,N^2$ riflette il fatto che la variabilità aumenta con la scala della popolazione.


  In realtá, a seconda dell’origine della variabilità, il termine stocastico può scalare in modo diverso con la popolazione: nel **rumore ambientale**, che agisce collettivamente su tutti gli individui, l’ampiezza cresce proporzionalmente a $N$; nel **rumore demografico**, dovuto a eventi indipendenti di nascita e morte, cresce invece come $\sqrt{N}$, poiché le fluttuazioni si sommano in modo incoerente.


- **Modelli biochimici e genetici**  
  In biofisica molecolare, la concentrazione di specie chimiche o proteiche evolve come: $$\frac{dx}{dt} = v_+(x) - v_-(x) + \sqrt{\frac{v_+(x)+v_-(x)}{\Omega}}\,\eta(t)\;,$$
  dove $\Omega$ rappresenta il volume o la scala del sistema.  
  La fluttuazione è inversamente proporzionale alla dimensione: nei piccoli sistemi cellulari domina il rumore, nei grandi si recupera il comportamento medio deterministico.

---

### 5.4 Scienze dell’informazione e dinamiche di rete

Nel campo delle reti sociali, della comunicazione o dell’analisi dei dati, la formalizzazione tipo Langevin viene impiegata per studiare la diffusione dell’informazione, la polarizzazione e l’adattamento algoritmico.

- **Diffusione di informazione rumorosa su reti**  
  Per un nodo $i$ con stato $x_i(t)$, si può scrivere: $$\frac{dx_i}{dt} = -\sum_j L_{ij}\,x_j + \sqrt{2D_i}\,\eta_i(t)\;,$$dove $L_{ij}$ è la matrice laplaciana della rete e $D_i$ l’intensità del rumore.  
  Il termine deterministico tende all’omogeneizzazione (consenso), mentre il rumore mantiene diversità e disordine.  
  In regime stazionario si osservano distribuzioni di opinioni stabili ma non uniformi, analoghe a configurazioni termiche in equilibrio.

- **Adattamento algoritmico e apprendimento**  
  Nei modelli di *stochastic gradient descent* (SGD), la dinamica dei parametri $\theta$ durante l’ottimizzazione può essere descritta da un’equazione di tipo Langevin: $$\frac{d\theta}{dt} = -\nabla_\theta L(\theta) + \sqrt{2T}\,\eta(t)\;,$$dove $L(\theta)$ è la funzione di perdita e $T$ rappresenta una “temperatura” effettiva che quantifica l’intensità del rumore.  
  Le fluttuazioni $\eta(t)$ derivano dal fatto che, invece di calcolare il gradiente sull’intero insieme di dati, l’algoritmo lo stima ripetutamente su **piccoli sottoinsiemi casuali di esempi**, detti *minibatch*: ogni stima introduce quindi una variazione casuale nel gradiente.  
  Questa sorgente di rumore rende la traiettoria dei parametri stocastica e permette al sistema di esplorare più facilmente regioni diverse del paesaggio della funzione di perdita, evitando minimi locali.  
  L’analogia ha portato allo sviluppo dei metodi di **Langevin dynamics** in *machine learning*, dove il rumore non è un difetto numerico, ma uno strumento per migliorare la generalizzazione e la capacità esplorativa degli algoritmi.

---

### 5.5 Lettura trasversale

La forza del modello di Langevin risiede nella sua **universalità strutturale**:

| **Dominio** | **Variabile tipica** | **Interpretazione di $a(x,t)$** | **Interpretazione di $b(x,t)\eta(t)$** |
|:-------------|:---------------------|:-------------------------------|:--------------------------------------|
| Fisica | velocità, posizione | forza o gradiente di potenziale | urti molecolari, agitazione termica |
| Finanza | prezzo, tasso | rendimento medio, tendenza | volatilità di mercato |
| Sociologia | opinione, preferenza | attrazione verso il consenso | rumore informativo o esposizione casuale |
| Ecologia | popolazione, risorsa | crescita o interazione | fluttuazioni ambientali |
| Informatica / AI | peso o parametro | discesa del gradiente | rumore stocastico del campionamento |

---

### 5.6 Conclusione generale

L’equazione di Langevin, con le sue varianti e generalizzazioni, è oggi un **linguaggio universale della complessità**.  
Essa consente di modellizzare sistemi in cui l’incertezza non è un difetto o un disturbo, ma una parte integrante della dinamica:  
- nelle fluttuazioni dei mercati e nelle decisioni collettive,  
- nei cicli biologici e nei processi ecologici,  
- nei meccanismi di apprendimento e nei flussi informativi.

Il concetto chiave è che **ogni sistema complesso vive nella tensione tra ordine e rumore**:  
la componente deterministica guida la traiettoria, quella stocastica ne esplora lo spazio delle possibilità.  
In questa dialettica risiede la straordinaria potenza del formalismo di Langevin come strumento di unificazione scientifica.


## Appendice A: Lemma di Itô (regola della catena stocastica)

In questa appendice forniamo una derivazione didattica del **lemma di Itô** per funzioni sufficientemente regolari $f(x,t)$ dove $x_t$ soddisfa la SDE in notazione di Itô
$$
dx_t = a(x_t,t)\,dt + b(x_t,t)\,dW_t,
$$
con $W_t$ moto browniano standard. Presentiamo prima il caso unidimensionale, poi la forma multidimensionale.

---

### A.1 Idea di base: espansione di Taylor stocastica

Consideriamo l’incremento su un intervallo infinitesimo $[t,t+dt]$: $$df \equiv f(x_{t+dt},t+dt) - f(x_t,t).$$Applicando una **espansione di Taylor** fino ai termini d’ordine $dt$ (tenendo conto che $dW_t \sim \mathcal{O}(\sqrt{dt})$), si ottiene
$$df \approx \partial_t f\,dt + \partial_x f\,dx_t + \tfrac{1}{2}\,\partial_{xx} f\,(dx_t)^2.$$
Per la SDE data,$$dx_t = a\,dt + b\,dW_t \quad \Rightarrow \quad (dx_t)^2 = (a\,dt + b\,dW_t)^2 = a^2 (dt)^2 + 2ab\,dt\,dW_t + b^2 (dW_t)^2.$$Usando le **regole di calcolo di Itô**$$(dt)^2 = 0,\qquad dt\,dW_t=0,\qquad (dW_t)^2 = dt,$$segue$$(dx_t)^2 = b^2\,dt.$$Sostituendo:$$df = \partial_t f\,dt + \partial_x f\,(a\,dt + b\,dW_t) + \tfrac{1}{2}\,\partial_{xx} f\,b^2\,dt.$$Raggruppando i termini deterministici e stocastici,
$$\boxed{\; df(x_t,t) \;=\; \big(\partial_t f + a\,\partial_x f + \tfrac{1}{2}\,b^2\,\partial_{xx} f\big)\,dt \;+\; b\,\partial_x f\,dW_t. \;}$$

---

### A.2 Forma integrale (versione operativa)

Integrando tra $0$ e $t$ (con ipotesi standard di regolarità),$$f(x_t,t) = f(x_0,0) + \int_0^t \!\!\Big(\partial_s f + a\,\partial_x f + \tfrac{1}{2}\,b^2\,\partial_{xx} f\Big)(x_s,s)\,ds\;+\; \int_0^t \!\! b(x_s,s)\,\partial_x f(x_s,s)\,dW_s.$$Il secondo integrale è uno **integrale stocastico di Itô** a media nulla, mentre il primo fornisce il **drift medio** dell’osservabile trasformata $f(x_t,t)$.

---

### A.3 Caso multidimensionale

Sia $\mathbf{x}_t \in \mathbb{R}^n$ soluzione di $$d\mathbf{x}_t = \mathbf{a}(\mathbf{x}_t,t)\,dt + \mathbf{B}(\mathbf{x}_t,t)\,d\mathbf{W}_t,$$dove $\mathbf{W}_t \in \mathbb{R}^m$ ha componenti browniane indipendenti e $\mathbf{B}$ è matrice $n\times m$.  
Per una funzione sufficientemente regolare $f:\mathbb{R}^n\times \mathbb{R}\to\mathbb{R}$, indicando con $\nabla f$ il gradiente colonna e con $\nabla^2 f$ l’hessiano, $$\boxed{\; df = \Big(\partial_t f + \nabla f^{\!\top}\mathbf{a} + \tfrac{1}{2}\,\mathrm{Tr}\big[\mathbf{B}\mathbf{B}^{\!\top}\nabla^2 f\big]\Big)\,dt \;+\; (\nabla f)^{\!\top}\mathbf{B}\,d\mathbf{W}_t. \;}$$Qui la matrice di diffusione è $\mathbf{D}=\mathbf{B}\mathbf{B}^{\!\top}$, simmetrica semidefinita non negativa, e il termine di secondo ordine si compatta in $\tfrac{1}{2}\,\mathrm{Tr}(\mathbf{D}\nabla^2 f)$.

---

### A.4 Commenti su regolarità e ipotesi

Il lemma richiede ipotesi standard (ad esempio $a$, $b$ localmente lipschitziane e crescita lineare; $f$ con derivate fino al secondo ordine limitate o a crescita controllata) per garantire esistenza/unicità della soluzione della SDE e la validità dello scambio tra espansione e limite. In impostazioni più generali si ricorre alla teoria delle martingale e agli operatori di generatore infinitesimo.

---

### A.5 Esempi rapidi

1) **$f(x)=x^2$** con $dx=\mu\,dt+\sigma\,dW_t$:$$df = (2x\mu + \sigma^2)\,dt + 2x\sigma\,dW_t.$$In media: $\tfrac{d}{dt}\mathbb{E}[x_t^2] = 2\mu\,\mathbb{E}[x_t] + \sigma^2$.

2) **$f(x)=\ln x$** per **moto browniano geometrico** $dx=\mu x\,dt+\sigma x\,dW_t$ (con $x_t>0$): $$df = \Big(\mu - \tfrac{1}{2}\sigma^2\Big)\,dt + \sigma\,dW_t.$$Segue $\ln x_t = \ln x_0 + (\mu-\tfrac{1}{2}\sigma^2)t + \sigma W_t$ e dunque $x_t$ è lognormale.

---

### A.6 Itô vs Stratonovich: relazione di conversione

Se la SDE è interpretata in senso **Stratonovich**, $$dx_t = a^{(\mathrm{S})}(x_t,t)\,dt + b(x_t,t)\circ dW_t,$$allora l’equivalente in senso **Itô** ha drift corretto$$a^{(\mathrm{I})}(x,t) \;=\; a^{(\mathrm{S})}(x,t) \;+\; \tfrac{1}{2}\,b(x,t)\,\partial_x b(x,t),$$(caso scalare; in dimensione maggiore il termine correttivo è $\tfrac{1}{2}\sum_k B_{\cdot k}\,\nabla B_{\cdot k}$).  
Il lemma di Itô si applica **nella convenzione di Itô**; in Stratonovich vale la **regola classica della catena** senza il termine $\tfrac{1}{2}$ di correzione, a prezzo della correzione nel drift quando si converte fra le due convenzioni.

---

### A.7 Generatore infinitesimo e connessione operativa

Il lemma di Itô identifica il **generatore infinitesimo** $\mathcal{L}$ del processo: 
$$\mathcal{L}f \;=\; \partial_t f + a\,\partial_x f + \tfrac{1}{2}b^2\,\partial_{xx} f\quad\big(\text{unidimensionale}\big),$$ $$\qquad \mathcal{L}f \;=\; \partial_t f + \nabla f^{\!\top}\mathbf{a} + \tfrac{1}{2}\mathrm{Tr}[\mathbf{D}\nabla^2 f] \quad\big(\text{multidimensionale}\big).$$Questo operatore è il ponte verso l’equazione per le densità (Fokker–Planck), posta come **aggiunta** o **appendice** alla lezione principale: la Fokker–Planck è l’equazione **aggiunta** associata all’aggiunto $\mathcal{L}^\ast$ del generatore $\mathcal{L}$.

---

## Appendice B. Dalla SDE all’equazione di Fokker–Planck

In questa appendice viene formalizzato il **legame tra la descrizione stocastica (SDE o Langevin)** e la **descrizione deterministica in termini di densità di probabilità** (equazione di Fokker–Planck).  
L’obiettivo è mostrare come l’evoluzione collettiva di un sistema rumoroso derivi, in modo rigoroso, dalle proprietà medie delle traiettorie individuali.

---

### B.1 Dalle SDE alla Fokker–Planck: idea generale

Una SDE in notazione di Itô ha la forma: $$dx_t = a(x_t,t)\,dt + b(x_t,t)\,dW_t,$$dove:
- $a(x_t,t)$ è il **termine di drift** (deterministico),
- $b(x_t,t)$ è il **coefficiente di diffusione**,
- $dW_t$ rappresenta un incremento del moto browniano con $\langle dW_t \rangle = 0$ e $\langle dW_t^2 \rangle = dt$.

Le SDE descrivono l’evoluzione di singole traiettorie stocastiche $x(t)$, ma non dicono direttamente come evolve la **densità di probabilità** $P(x,t)$ delle possibili realizzazioni.

Sotto l’interpretazione di **Itô**, la distribuzione $P(x,t)$ soddisfa la **equazione di Fokker–Planck (FP)**:
$$\frac{\partial P}{\partial t} = -\frac{\partial}{\partial x}\left[a(x,t)P\right] + \frac{1}{2}\frac{\partial^2}{\partial x^2}\left[b^2(x,t)P\right].$$Il primo termine rappresenta il **trasporto convettivo** della densità dovuto al drift $a(x,t)$, mentre il secondo descrive la **diffusione** della densità dovuta al rumore stocastico di ampiezza $b(x,t)$.

---

### B.2 Relazione concettuale tra Langevin e Fokker–Planck

L’equazione di **Langevin** o la SDE forniscono la dinamica di **una singola traiettoria** nel tempo;  
la Fokker–Planck fornisce invece la **dinamica collettiva della probabilità** che tali traiettorie occupino una data regione dello spazio delle variabili.

> *Langevin agisce sullo spazio delle traiettorie, Fokker–Planck agisce sullo spazio delle distribuzioni.*

---

### B.3 Derivazione concettuale

Consideriamo la forma differenziale multidimensionale dell’equazione di Langevin: $$\frac{d\mathbf{x}}{dt} = \mathbf{f}(\mathbf{x},t) + \mathbf{G}(\mathbf{x},t)\,\boldsymbol{\eta}(t),$$con $\langle \eta_i(t)\eta_j(t') \rangle = \delta_{ij}\,\delta(t-t')$.  
Si desidera determinare come evolve nel tempo la densità $P(\mathbf{x},t)$.

Per una funzione osservabile $A(\mathbf{x})$, si definisce la media ensemble: $$\langle A(\mathbf{x}) \rangle = \int A(\mathbf{x})\, P(\mathbf{x},t)\, d\mathbf{x}.$$Derivando rispetto al tempo e sostituendo l’equazione di Langevin, si ottiene, mediante il lemma di Itô, $$\frac{d}{dt}\langle A(\mathbf{x}) \rangle = \int \left[\sum_i f_i(\mathbf{x},t)\frac{\partial A}{\partial x_i} + \frac{1}{2}\sum_{i,j} D_{ij}(\mathbf{x},t)\frac{\partial^2 A}{\partial x_i \partial x_j}\right] P(\mathbf{x},t)\, d\mathbf{x},$$dove $\mathbf{D}(\mathbf{x},t) = \mathbf{G}(\mathbf{x},t)\mathbf{G}^T(\mathbf{x},t)$ è la **matrice di diffusione**.

Integrando per parti e trascurando i termini di bordo si ottiene, per l’evoluzione di $P(\mathbf{x},t)$: $$\frac{\partial P}{\partial t} = -\sum_i \frac{\partial}{\partial x_i}\!\left[f_i(\mathbf{x},t)P\right] + \frac{1}{2}\sum_{i,j}\frac{\partial^2}{\partial x_i\,\partial x_j}\!\left[D_{ij}(\mathbf{x},t)P\right].$$

---

### B.4 Interpretazione fisica dei termini

- **Termine di deriva**  
  $-\partial_{x_i}[f_i P]$: descrive il **trasporto sistematico** della densità, dovuto a una forza o tendenza deterministica.

- **Termine diffusivo**  
  $\tfrac{1}{2}\partial_{x_i}\partial_{x_j}[D_{ij} P]$: rappresenta la **dispersione** della densità a causa del rumore.

La competizione tra i due meccanismi determina l’evoluzione complessiva e le condizioni di equilibrio del sistema.

---

### B.5 Caso unidimensionale con rumore additivo

Per la dinamica: $$\frac{dx}{dt} = f(x,t) + \sqrt{2D}\,\eta(t),$$la corrispondente Fokker–Planck è: $$\frac{\partial P}{\partial t} = -\frac{\partial}{\partial x}\left[f(x,t)P\right] + D\,\frac{\partial^2 P}{\partial x^2}.$$In equilibrio ($\partial_t P=0$) e per una forza derivante da potenziale $f(x) = -\frac{1}{\gamma}\frac{dU}{dx}$, si ottiene la soluzione stazionaria: $$P_{\mathrm{st}}(x) \propto \exp\!\left[-\frac{U(x)}{D\gamma}\right],$$ che coincide con la **distribuzione di Boltzmann** a temperatura effettiva $T_{\mathrm{eff}} = D\gamma$.

---

### B.6 Confronto strutturale tra Langevin e Fokker–Planck

| **Aspetto** | **Equazione di Langevin / SDE** | **Equazione di Fokker–Planck** | **Interpretazione** |
|:-------------|:--------------------------------|:--------------------------------|:--------------------|
| Variabile dinamica | $\mathbf{x}(t)$ | $P(\mathbf{x},t)$ | Stato singolo vs. densità di probabilità |
| Oggetto matematico | Equazione differenziale stocastica | PDE deterministica | Micro vs. macro |
| Termini principali | Drift $\mathbf{f}$ e rumore $\mathbf{G}\boldsymbol{\eta}$ | Deriva $-\partial_i[f_iP]$ e diffusione $\frac{1}{2}\partial_i\partial_j[D_{ij}P]$ | Flusso medio e spreading |
| Diffusione | $\mathbf{D} = \mathbf{G}\mathbf{G}^T$ | Compare nel secondo termine | Intensità delle fluttuazioni |
| Risultato | Cammini casuali $x(t)$ | Evoluzione di $P(x,t)$ | Processi individuali vs. collettivi |
| Equilibrio | $\dot{x}=0$ (media) | $\partial_t P=0$ | Stato stazionario |

---

### B.7 Sintesi concettuale

- L’equazione di **Langevin/SDE** fornisce una descrizione *microscopica*:  
  produce traiettorie individuali, adatte a simulazioni e osservabili di tipo temporale.

- L’equazione di **Fokker–Planck** fornisce una descrizione *macroscopica*:  
  spiega come evolve la densità di probabilità nel tempo e conduce naturalmente allo stato stazionario.

- Le due descrizioni sono **complementari** e connesse tramite il **generatore infinitesimo di Itô** e il suo **aggiunto**, da cui deriva la FP.

---

### B.8 Esempio di applicazione fisica: moto browniano in potenziale

Per una particella di coordinate $x(t)$ soggetta a $F(x)=-\partial_x U(x)$ e rumore additivo, si ha: $$\frac{dx}{dt} = -\frac{1}{\gamma}\frac{dU}{dx} + \sqrt{2D}\,\eta(t),$$da cui segue la Fokker–Planck:$$\frac{\partial P}{\partial t} = \frac{1}{\gamma}\frac{\partial}{\partial x}\!\left(\frac{dU}{dx} P\right) + D\frac{\partial^2 P}{\partial x^2}.$$La distribuzione converge asintoticamente a: $$P_{\mathrm{st}}(x) \propto e^{-U(x)/(D\gamma)},$$
che rappresenta la probabilità di equilibrio determinata dal bilancio tra **forze conservative** e **rumore diffusivo**.

---

### B.9 Visione d’insieme

| **Livello** | **Oggetto matematico** | **Equazione tipica** | **Descrizione** |
|:-------------|:-----------------------|:---------------------|:----------------|
| Microscopia | Traiettorie $x(t)$ | Langevin / SDE | Stocastica individuale |
| Mesoscopia | Densità $P(x,t)$ | Fokker–Planck | Deterministica collettiva |
| Macroscopia | Stato $P_{\mathrm{st}}(x)$ | $\partial_t P=0$ | Equilibrio stazionario |

---

### B.10 Osservazione conclusiva

L’equazione di Fokker–Planck è la “controparte deterministica” della dinamica di Langevin.  
Descrive l’evoluzione delle **densità di probabilità** invece delle singole traiettorie, fornendo un potente strumento per lo studio dell’equilibrio e delle transizioni stocastiche.  
È il punto d’incontro tra **teoria dei processi stocastici** e **fisica statistica**, ed è alla base di gran parte dei metodi di simulazione numerica e di analisi dei sistemi complessi.

## Appendice visiva: dal moto stocastico all’equilibrio

Per fissare le idee, riportiamo uno **schema concettuale** che sintetizza il legame tra la descrizione microscopica (traiettorie) e quella macroscopica (densità di probabilità), evidenziando il ruolo dell’equazione di Langevin, della SDE e della Fokker–Planck.


![Markov riducibile](immagini/DalMicroAlMacroLangevin){#fig:micro-macro-langevin}
*Figura: traiettorie stocastiche → densità temporale → equilibrio stazionario.*

---

### Approcci

- **Dal basso verso l’alto (bottom-up)**:  
  Si parte da simulazioni di singole traiettorie (equazione di Langevin / SDE) e, mediando su molte realizzazioni, si ricostruisce la densità $P(x,t)$ governata dalla Fokker–Planck.

- **Dall’alto verso il basso (top-down)**:  
  Si parte da una distribuzione iniziale $P(x,0)$ e si osserva la sua evoluzione deterministica nel tempo fino all’equilibrio.  
  In tal senso, la Fokker–Planck fornisce la descrizione “media” dei comportamenti che emergono dalle SDE.

---

### Sintesi logica del flusso

| **Livello** | **Oggetto matematico** | **Equazione** | **Tipo di descrizione** |
|:-------------|:-----------------------|:---------------|:------------------------|
| Microscopia | Traiettorie $x(t)$ | Equazione di Langevin / SDE | Stocastica, individuale |
| Mesoscopia | Densità $P(x,t)$ | Equazione di Fokker–Planck | Deterministica, collettiva |
| Macroscopia | Stato stazionario $P_{\mathrm{st}}(x)$ | Condizione $\partial_t P=0$ | Statistica d’equilibrio |

---

### Esempio interpretativo

- **SDE (simulazione singola):** mostra l’irregolarità e la fluttuazione delle traiettorie.
- **Fokker–Planck:** mostra come l’insieme di queste traiettorie forma progressivamente una distribuzione $P(x,t)$ che si allarga o si concentra.
- **Equilibrio:** in un potenziale $U(x)$, le regioni a energia bassa diventano più probabili, e $P(x,t)\to P_{\mathrm{st}}(x)\propto e^{-U(x)/(D\gamma)}$.

---



## Riferimenti

* Risken, H. *The Fokker–Planck Equation*, Springer (1989).

* Gardiner, C. W. *Handbook of Stochastic Methods*, Springer (2009).

* Kloeden, P. E., Platen, E. *Numerical Solution of Stochastic Differential Equations*, Springer (1992).

* van Kampen, N. G. *Stochastic Processes in Physics and Chemistry*, Elsevier (2007).

* Gillespie, D. T. (1996). *Exact numerical simulation of the Ornstein–Uhlenbeck process and its generalizations*. Phys. Rev. E.

