---
title: "LAB06: Dalle traiettorie alla densità: Master Equation e Fokker--Planck"
author: "Antonio Scala"
date: ""
---

# Obiettivi del laboratorio

In questo laboratorio studieremo uno stesso fenomeno stocastico a tre livelli di descrizione:

1. tramite **traiettorie individuali** di un processo a salti su una griglia discreta;
2. tramite **evoluzione della probabilità di occupazione** dei siti, descritta da una master equation;
3. tramite il **limite continuo**, in cui la distribuzione evolve secondo una equazione di Fokker--Planck.

L'obiettivo non è soltanto implementare un codice, ma capire un passaggio concettuale fondamentale del corso:

* una singola traiettoria è irregolare;
* un insieme di traiettorie genera una distribuzione regolare;
* la distribuzione discreta evolve secondo una legge di bilancio;
* nel limite di griglia fine questa legge si riscrive come drift + diffusione.

Alla fine del laboratorio dovreste essere in grado di:

1. simulare un random walk continuo nel tempo su una catena 1D;
2. costruire l'istogramma della posizione a partire da molte traiettorie;
3. scrivere e integrare la master equation corrispondente;
4. confrontare istogramma empirico e soluzione della master equation;
5. riconoscere, nella dinamica discreta, i contributi di drift e diffusione;
6. collegare la struttura discreta alla Fokker--Planck continua;
7. verificare nel caso continuo elementare la crescita della varianza e il trasporto della media.

# Struttura del laboratorio

Il laboratorio è diviso in cinque parti:

* Parte 0 -- richiamo teorico essenziale;
* Parte A -- traiettorie di un processo a salti su griglia;
* Parte B -- master equation sullo stesso modello;
* Parte C -- passaggio concettuale al continuo;
* Parte D -- drift-diffusion continua e confronto con la soluzione teorica;
* Mini-appendice -- operatori discreti, smoothing, Laplaciano e drift.

# Parte 0 -- Richiamo teorico essenziale

## 0.1 Due livelli di descrizione

Consideriamo un sistema che evolve in modo casuale tra stati discreti.

Possiamo descriverlo in due modi diversi.

### Livello 1 -- traiettoria

Una singola realizzazione è una successione casuale di stati visitati nel tempo.

Per esempio,

$$
i_0 \to i_1 \to i_2 \to \cdots
$$

con tempi di salto casuali.

### Livello 2 -- distribuzione di probabilità

Se ripetiamo molte volte lo stesso esperimento, oppure ragioniamo in termini d'ensemble, introduciamo

$$
p_i(t) = P(X_t=i),
$$

cioè la probabilità che il sistema si trovi nel sito $i$ al tempo $t$.

Il vettore

$$
p(t) = (p_0(t),p_1(t),\dots,p_N(t))
$$

descrive la distribuzione del sistema sulla griglia.

## 0.2 Master equation come bilancio

Se il sistema può saltare da uno stato $i$ a uno stato $j$ con tasso $w_{i\to j}$, la probabilità $p_i(t)$ evolve secondo una legge di bilancio:

$$
\frac{dp_i}{dt} = \sum_{j\neq i}\bigl[w_{j\to i}p_j - w_{i\to j}p_i\bigr].
$$

Questa formula dice semplicemente:

* la probabilità di stare in $i$ aumenta per gli ingressi da altri stati;
* diminuisce per le uscite da $i$ verso altri stati.

## 0.3 Dal discreto al continuo

Se gli stati diventano molto fitti nello spazio e i salti diventano molto piccoli, allora la distribuzione discreta può essere approssimata da una densità continua $p(x,t)$.

Nel caso più semplice, la densità soddisfa una equazione di drift-diffusion:

$$
\partial_t p(x,t) = -a\,\partial_x p(x,t) + D\,\partial_x^2 p(x,t).
$$

Qui:

* il termine con derivata prima trasporta la distribuzione;
* il termine con derivata seconda la allarga e la smussa.

# Parte A -- Processo a salti su griglia 1D

## A.1 Modello

Consideriamo i siti

$$
i = 0,1,\dots,N
$$

su una griglia lineare.

Dal sito interno $i$, il processo può:

* saltare a destra, $i\to i+1$, con tasso $r$;
* saltare a sinistra, $i\to i-1$, con tasso $\ell$.

Nel laboratorio conviene usare inizialmente **bordi riflettenti**, per non perdere massa probabilistica ai bordi. In pratica:

* se la traiettoria è in $0$, può solo andare a $1$;
* se è in $N$, può solo andare a $N-1$.

## A.2 Parametri suggeriti

Usate ad esempio:

$$
N=80,
\qquad
x_0 = N/2,
\qquad
T=5.
$$

Provate almeno due casi:

### Caso simmetrico

$$
r=\ell=1.
$$

### Caso con bias

$$
r=1.4,
\qquad
\ell=0.8.
$$

Per costruire istogrammi stabili, usate ad esempio

$$
M = 10^3 \quad \text{oppure} \quad M=10^4
$$

traiettorie indipendenti.

## A.3 Come simulare una traiettoria

Poiché il tempo è continuo e gli eventi avvengono a tassi assegnati, il tempo di attesa fino al prossimo salto è esponenziale.

Se il processo si trova in un sito interno, il tasso totale è

$$
a_0 = r+\ell.
$$

Quindi:

1. si estrae un tempo di attesa
   $$
   \tau \sim \mathrm{Exp}(a_0);
   $$
2. si sceglie la direzione del salto:

   * a destra con probabilità $r/a_0$;
   * a sinistra con probabilità $\ell/a_0$.

### Pseudocodice

```text
scegli N, r, ell, T, sito iniziale i0
poni t = 0
poni i = i0

mentre t < T:
    determina i tassi disponibili nello stato corrente

    se 0 < i < N:
        tasso_destra = r
        tasso_sinistra = ell

    se i = 0:
        tasso_destra = r
        tasso_sinistra = 0

    se i = N:
        tasso_destra = 0
        tasso_sinistra = ell

    a0 = tasso_destra + tasso_sinistra

    estrai tau da una esponenziale di media 1/a0
    poni t = t + tau

    se t > T:
        esci dal ciclo

    scegli il salto:
        destra con probabilita tasso_destra / a0
        sinistra con probabilita tasso_sinistra / a0

    aggiorna il sito i
```

## A.4 Compiti

1. Simulare una singola traiettoria e rappresentare il sito occupato in funzione del tempo.
2. Ripetere per diversi seed casuali.
3. Simulare molte traiettorie indipendenti.
4. Fissare alcuni tempi, ad esempio
   $$
   t=1\,;2\,;4
   $$
   e costruire l'istogramma della posizione.
5. Confrontare il caso simmetrico e quello con bias.

## A.5 Domande guida

1. Nel caso simmetrico, l'istogramma resta centrato attorno alla posizione iniziale?
2. Nel caso con bias, compare uno spostamento netto verso destra o verso sinistra?
3. Una singola traiettoria è sufficiente per descrivere bene la dinamica statistica?
4. Perché l'istogramma su molte traiettorie è molto più regolare della singola realizzazione?

# Parte B -- Master equation per lo stesso modello

## B.1 Equazione per i siti interni

Se $p_i(t)$ è la probabilità di occupare il sito $i$, per i siti interni vale

$$
\frac{dp_i}{dt} = r\,p_{i-1} + \ell\,p_{i+1} - (r+\ell)p_i\,
\qquad i=1,\dots,N-1.
$$

Interpretazione dei tre termini:

* $r\,p_{i-1}$ = flusso in ingresso da sinistra;
* $\ell\,p_{i+1}$ = flusso in ingresso da destra;
* $(r+\ell)p_i$ = flusso in uscita dal sito $i$.

## B.2 Condizioni al bordo riflettente

Se vogliamo conservare la probabilità totale nel dominio, una scelta semplice è usare un adattamento coerente ai bordi:

$$
\frac{dp_0}{dt} = \ell\,p_1 - r\,p_0,
$$

$$
\frac{dp_N}{dt} = r\,p_{N-1} - \ell\,p_N.
$$

In questo modo:

* dal bordo sinistro si può solo entrare nel dominio da $1$ o uscire verso $1$;
* dal bordo destro si può solo entrare da $N-1$ o uscire verso $N-1$.

## B.3 Condizione iniziale

Se tutte le traiettorie partono da un sito iniziale $i_0$, allora la distribuzione iniziale è concentrata in $i_0$:

$$
p_i(0)=\delta_{i,i_0}.
$$

## B.4 Forma matriciale

Il sistema si può scrivere come

$$
\dot p(t)=L p(t),
$$

dove $L$ è una matrice tridiagonale.

Per esempio, per i siti interni compaiono coefficienti:

* $r$ sotto la diagonale;
* $\ell$ sopra la diagonale;
* $-(r+\ell)$ sulla diagonale.

## B.5 Compiti

1. Costruire la matrice $L$ del processo.
2. Integrare numericamente il sistema
   $$
   \dot p = Lp
   $$
   fino al tempo finale $T$.
3. Verificare numericamente che
   $$
   \sum_i p_i(t)=1
   $$
   resti costante nel caso riflettente.
4. Confrontare $p_i(t)$ con l'istogramma ottenuto dalle simulazioni della Parte A.

## B.6 Suggerimento pratico

Per integrare il sistema potete:

* usare un integratore ODE standard;
* oppure, per tempi piccoli, usare un Euler esplicito con passo sufficientemente piccolo.

Nel secondo caso dovete controllare che:

* le probabilità restino non negative;
* la somma resti vicina a 1.

## B.7 Domande guida

1. Perché il confronto va fatto tra $p_i(t)$ e un istogramma su molte traiettorie, e non con una singola traiettoria?
2. In che senso la master equation è una legge di conservazione della probabilità?
3. Quale differenza osservate tra caso simmetrico e con bias a livello di distribuzione?
4. Il picco dell'istogramma si sposta? Si allarga? Entrambe le cose?

# Parte C -- Passaggio concettuale al continuo

## C.1 Dalla griglia alla coordinata spaziale

Associamo al sito $i$ la coordinata

$$
x_i = i\,\Delta x.
$$

Se la griglia è sufficientemente fine, possiamo pensare che la probabilità sul sito $i$ campioni una densità continua.

Non vogliamo qui fare una derivazione formale completa, ma mettere in evidenza la struttura che emerge.

## C.2 Riscrittura della master equation

Partiamo da

$$
\dot p_i = r\,p_{i-1}+\ell\,p_{i+1}-(r+\ell)p_i.
$$

Riscriviamola come somma di una parte antisimmetrica e una parte simmetrica:

$$
\dot p_i =
\frac{\ell-r}{2}(p_{i+1}-p_{i-1})
+ \frac{\ell+r}{2}(p_{i+1}+p_{i-1}-2p_i).
$$

Questa identità è molto importante.

* Il primo termine contiene una differenza antisimmetrica tra destra e sinistra.
* Il secondo contiene una differenza simmetrica centrata.

## C.3 Interpretazione

Quando $p_i$ è il campionamento di una funzione liscia $p(x,t)$, si ha qualitativamente:

$$
p_{i+1}-p_{i-1} \sim 2\Delta x\,\partial_x p,
$$

$$
p_{i+1} - 2 p_i + p_{i-1} \sim \Delta x^2\,\partial_x^2 p.
$$

Quindi:

* la parte antisimmetrica genera una derivata prima, cioè un **drift**;
* la parte simmetrica genera una derivata seconda, cioè una **diffusione**.

## C.4 Equazione continua attesa

Dalla decomposizione della sezione C.2, con griglia fissa di passo $\Delta x$, possiamo leggere direttamente i parametri della Fokker--Planck continua.

Il tempo medio tra due salti successivi in un sito interno vale

$$
\Delta t = \frac{1}{r+\ell}.
$$

In un intervallo di tempo unitario avvengono mediamente $r+\ell$ salti, ciascuno di ampiezza $\Delta x$.
Lo spostamento medio per unita' di tempo e'

$$
v = (r - \ell)\,\Delta x,
$$

mentre la varianza accumulata per unita' di tempo e'

$$
D = \frac{r+\ell}{2}\,\Delta x^2.
$$

Con questi valori, la Fokker--Planck corrispondente alla master equation discreta e'

$$
\partial_t p = -v\,\partial_x p + D\,\partial_x^2 p.
$$

Osservazione importante: $v$ e' controllato dall'*asimmetria* tra i tassi, $D$ dalla loro *somma*.
Nel caso simmetrico $r = \ell$ si ha $v = 0$ e resta solo la diffusione.

Queste formule sono operative: fissati $r$, $\ell$ e $\Delta x$, si calcolano $v$ e $D$ e si sovrappone la gaussiana teorica

$$
p(x,t) = \frac{1}{\sqrt{4\pi D t}}
\exp\!\left[-\frac{(x - x_0 - v\,t)^2}{4Dt}\right]
$$

agli istogrammi ottenuti dalla master equation discreta, come verifica numerica del raccordo.

Questo e' il punto concettuale centrale del laboratorio:

> la Fokker--Planck continua non nasce dal nulla, ma e' gia' contenuta nella struttura locale della master equation discreta.

## C.5 Approfondimento -- il limite formale $\Delta x \to 0$

> **Nota**: questa sezione e' facoltativa. Mostra come le formule operative della sezione C.4 emergano da un limite formale rigoroso. Non e' necessaria per i compiti del laboratorio.

Le formule di C.4 sono operative per griglia fissa, ma non spiegano in quale senso la Fokker--Planck sia il *limite* della master equation quando la griglia diventa infinitamente fine. Vediamo come funziona questo limite.

### Il problema dello scaling

Quando $\Delta x \to 0$, i salti diventano sempre piu' piccoli. Per ottenere una dinamica non banale in questo limite, i tassi $r$ e $\ell$ devono crescere in modo da compensare.

La domanda e': a quale velocita' devono crescere?

### Scaling generale con drift e diffusione finiti

Supponiamo di voler ottenere nel limite  $\Delta x \to 0$ una Fokker--Planck con coefficienti $v$ e $D$ entrambi finiti e non nulli. Scriviamo

$$
r = \frac{\lambda}{\Delta x^2} + \frac{\mu}{2\,\Delta x},
\qquad
\ell = \frac{\lambda}{\Delta x^2} - \frac{\mu}{2\,\Delta x},
$$

con $\lambda > 0$ e $\mu$ costanti fissate indipendentemente da $\Delta x$.

Calcoliamo i parametri:

$$
D = \frac{r+\ell}{2}\,\Delta x^2
= \frac{1}{2}\cdot\frac{2\lambda}{\Delta x^2}\cdot\Delta x^2
= \lambda,
$$

$$
v = (r-\ell)\,\Delta x
= \frac{\mu}{\Delta x}\cdot\Delta x
= \mu.
$$

Entrambi finiti. Nel limite $\Delta x \to 0$ con questo scaling si ottiene la Fokker--Planck completa

$$
\partial_t p = -\mu\,\partial_x p + \lambda\,\partial_x^2 p.
$$

### Caso particolare: regime puramente diffusivo

Se invece $r = \ell = \lambda/\Delta x^2$, i due tassi sono uguali e l'asimmetria e' zero. Allora

$$
D = \lambda,
\qquad
v = 0.
$$

Nel limite si ottiene solo diffusione pura, senza drift.

### Messaggio

Perche' l'asimmetria deve scalare come $1/\Delta x$ e non come $1/\Delta x^2$?
Perche' il drift e' un effetto di *primo ordine* nello spazio ($\partial_x p$),
mentre la diffusione e' di *secondo ordine* ($\partial_x^2 p$). Ogni potenza di $\Delta x$ in piu' nel denominatore compensa esattamente una derivata spaziale in piu'. In altri termini: drift e diffusione vivono su scale spaziali diverse,
e lo scaling dei tassi riflette questa gerarchia.

# Parte D -- Drift-diffusion continua

Per vedere il caso continuo in una forma già chiusa e confrontabile con teoria esplicita, consideriamo ora un processo continuo nel tempo e nello spazio.

## D.1 Modello continuo

Prendiamo la SDE

$$
dX_t = a\,dt + \sqrt{2D}\,dW_t,
$$

dove:

* $a$ è il drift costante;
* $D>0$ è il coefficiente diffusivo;
* $W_t$ è un moto browniano standard.

## D.2 Discretizzazione per simulare le traiettorie

Su una griglia temporale uniforme,

$$
t_n = n\Delta t\,,
\qquad n=0,1,\dots,N_t,
$$

la dinamica si simula con

$$
X_{n+1} = X_n + a\,\Delta t + \sqrt{2D\Delta t}\,\eta_n,
\qquad
\eta_n \sim \mathcal N(0,1).
$$

## D.3 Fokker--Planck associata

La densità di probabilità soddisfa

$$
\partial_t p(x,t) = -a\,\partial_x p(x,t) + D\,\partial_x^2 p(x,t).
$$

Se la condizione iniziale è concentrata in $x_0$, la soluzione è

$$
p(x,t) = \frac{1}{\sqrt{4\pi Dt}}
\exp\!\left[-\frac{(x-x_0-at)^2}{4Dt}\right].
$$

Questa formula mostra in modo molto chiaro i due effetti distinti:

* il centro della distribuzione si sposta con velocità $a$;
* la larghezza cresce nel tempo per effetto della diffusione.

## D.4 Momenti teorici

Per questo processo vale

$$
\mathbb E[X_t] = x_0 + at,
$$

$$
\mathrm{Var}(X_t)=2Dt.
$$

## D.5 Parametri suggeriti

Usate ad esempio

$$
x_0 = 0,
\qquad
T=3,
\qquad
\Delta t = 10^{-3},
\qquad
M = 10^4.
$$

Provate almeno due casi:

### Solo diffusione

$$
a=0,
\qquad
D=1.
$$

### Drift + diffusione

$$
a=1,
\qquad
D=1.
$$

## D.6 Compiti

1. Simulare molte traiettorie della SDE.
2. Costruire istogrammi di $X_t$ a tempi fissati.
3. Sovrapporre la gaussiana teorica.
4. Stimare empiricamente media e varianza.
5. Verificare se i dati simulati sono coerenti con
   $$
   \mathbb E[X_t]=x_0+at,
   \qquad
   \mathrm{Var}(X_t)=2Dt.
   $$

## D.7 Domande guida

1. Quando $a=0$, l'istogramma resta centrato ma si allarga?
2. Quando $a\neq 0$, il centro si muove come previsto?
3. La larghezza cresce linearmente in $t$ oppure come $\sqrt{t}$? Attenzione a distinguere tra varianza e scala tipica.
4. In che senso questa dinamica continua è l'analogo della master equation biasata studiata sulla griglia?

# Confronto finale tra i tre livelli di descrizione

A questo punto avete visto tre oggetti diversi ma collegati.

## Livello 1 -- traiettorie

Le traiettorie individuali mostrano la casualità evento per evento oppure incremento per incremento.

## Livello 2 -- probabilità discreta

La master equation descrive come la probabilità si redistribuisce tra siti discreti.

## Livello 3 -- densità continua

La Fokker--Planck descrive il trasporto e la diffusione di una densità nello spazio continuo.

## Domande conclusive

1. Quale informazione fornisce una singola traiettoria che non si vede subito nella pdf?
2. Quale informazione fornisce la pdf che non si vede bene in una singola traiettoria?
3. Perché la master equation è una naturale equazione di conservazione?
4. In che senso il limite continuo separa chiaramente drift e diffusione?
5. Quale parte della dinamica è legata alla simmetria tra salti destra/sinistra, e quale alla loro asimmetria?

# Mini-appendice -- Operatori discreti, smoothing, Laplaciano e drift

Questa mini-appendice serve a chiarire perché certe combinazioni locali sui punti vicini della griglia siano l'analogo discreto di operatori differenziali continui.

## M.1 Il termine simmetrico come smoothing discreto

Sia $x_i$ una quantità definita sui siti di una griglia uniforme.

Consideriamo la combinazione

$$
x_{i+1}+x_{i-1}-2x_i.
$$

Questa misura quanto il valore nel sito $i$ differisce dalla media dei suoi vicini. Infatti,

$$
\frac{x_{i+1}+x_{i-1}}{2}-x_i =
\frac{1}{2}(x_{i+1}+x_{i-1}-2x_i).
$$

Quindi:

* se $x_i$ è maggiore della media dei vicini, allora
  $$
  x_{i+1}+x_{i-1}-2x_i < 0;
  $$
* se $x_i$ è minore della media dei vicini, allora
  $$
  x_{i+1}+x_{i-1}-2x_i > 0.
  $$

Per questo motivo, un'evoluzione del tipo

$$
\dot x_i = \kappa\,(x_{i+1}+x_{i-1}-2x_i)
$$

fa da **smoothing**:

* i picchi tendono a scendere;
* le valli tendono a salire;
* il profilo si smussa nel tempo.

Questo è l'analogo discreto della diffusione.

## M.2 Collegamento con il Laplaciano continuo

Supponiamo di approssimare una funzione $u$ "liscia" su una griglia $x_i = i\,\Delta x$. Sviluppando in Taylor attorno a $x_i$,

$$
u(x_i+\Delta x)=u(x_i)+\Delta x\,u'(x_i)+\frac{\Delta x^2}{2}u''(x_i)+O(\Delta x^3),
$$

$$
u(x_i-\Delta x)=u(x_i)-\Delta x\,u'(x_i)+\frac{\Delta x^2}{2}u''(x_i)+O(\Delta x^3).
$$

Sommando le due espressioni,

$$
u(x_i+\Delta x)+u(x_i-\Delta x)-2u(x_i)
= u''(x_i)\, \Delta x^2 + O(\Delta x^4).
$$

Quindi

$$
\frac{u(x_{i+1})+u(x_{i-1})-2u(x_i)}{\Delta x^2}
\longrightarrow
\partial_x^2 u(x)
$$

quando $\Delta x \to 0$. Dunque, la combinazione simmetrica a tre punti è la discretizzazione standard del Laplaciano 1D.

## M.3 Il termine antisimmetrico come derivata prima

Consideriamo ora $u(x_{i+1})-u(x_{i-1})$. Ancora da Taylor,

$$
u(x_i+\Delta x)-u(x_i-\Delta x)
= 2\,u'(x_i)\,\Delta x+O(\Delta x^3).
$$

Perciò

$$
\frac{u(x_{i+1})-u(x_{i-1})}{2\,\Delta x}
\longrightarrow  \partial_x u(x).
$$

Questa è la discretizzazione centrata della derivata prima.

Nel limite continuo, questo è il termine che genera il **drift**.

## M.4 Decomposizione di un operatore locale a tre punti

Indichiamo con $u_i=u(x_i)$ e consideriamo una combinazione generale

$$
a\,u_{i+1}+b\,u_i+c\,u_{i-1}.
$$

La si può sempre riscrivere come

$$
a u_{i+1}+b u_i+c u_{i-1}
= \frac{a-c}{2}(u_{i+1}-u_{i-1})
+ \frac{a+c}{2}(u_{i+1}+u_{i-1}-2u_i)
+ (a+b+c)u_i.
$$

Questa formula è molto utile perché separa automaticamente:

1. **parte antisimmetrica**
   $$
   \frac{a-c}{2}(u_{i+1}-u_{i-1}),
   $$
   che nel continuo porta a una derivata prima;
2. **parte simmetrica**
   $$
   \frac{a+c}{2}(u_{i+1}+u_{i-1}-2u_i),
   $$
   che nel continuo porta a una derivata seconda;
3. **parte locale**
   $$
   (a+b+c)u_i,
   $$
   che rappresenta un termine di crescita, decadimento o sorgente locale.

## M.5 Interpretazione continua

Se si dividono i termini per le corrette potenze di $\Delta x$, la combinazione precedente suggerisce una forma continua del tipo

$$
\alpha\,\partial_x u + \beta\,\partial_x^2 u + \gamma\,u.
$$

In altre parole, già a livello discreto un operatore locale a tre punti contiene i mattoni di base di:

* drift;
* diffusione;
* reazione locale.

## M.6 Applicazione alla master equation del random walk con bias

Torniamo alla master equation

$$
\dot p_i = r\,p_{i-1}+\ell\,p_{i+1}-(r+\ell)p_i.
$$

Qui i coefficienti sono

$$
a=\ell,
\qquad
b=-(r+\ell),
\qquad
c=r.
$$

Applicando la decomposizione generale otteniamo

$$
\dot p_i 
= \frac{\ell-r}{2}(p_{i+1}-p_{i-1})
+ \frac{\ell+r}{2}(p_{i+1}+p_{i-1}-2p_i).
$$

Questa formula mostra in modo trasparente che:

* la differenza tra tassi destra e sinistra controlla il **drift**;
* la somma dei tassi controlla la **diffusione**.

Più precisamente:

* se $r=\ell$, resta solo la parte simmetrica e la dinamica è puramente diffusiva;
* se $r\neq \ell$, compare anche una parte di trasporto.

## M.7 Messaggio finale della mini-appendice

Il punto da fissare è il seguente:

* **simmetria tra vicini** $\to$ smoothing $\to$ Laplaciano $\to$ diffusione;
* **asimmetria tra vicini** $\to$ derivata prima $\to$ drift.

Questa è esattamente la struttura che ritroviamo nella Fokker--Planck continua.

# Suggerimenti pratici di implementazione

1. Tenete separati i codici per:

   * simulazione di traiettorie discrete;
   * integrazione della master equation;
   * simulazione della SDE continua.

2. Controllate sempre:

   * normalizzazione delle probabilità nella master equation;
   * numero di traiettorie usate per gli istogrammi;
   * stabilità rispetto a scelta di passo temporale o numero di campioni.

3. Quando confrontate istogrammi e teoria, ricordate che:

   * una singola traiettoria non va confrontata con una pdf;
   * serve un numero sufficientemente grande di realizzazioni.

# Appendice avanzata -- formulazione sparsa e confronto tra propagatori

> **Nota**: questa appendice e' facoltativa e ha carattere avanzato. Presuppone familiarita' con matrici sparse, operator splitting ed esponenziale di matrice. Non e' necessaria per completare le parti A--D del laboratorio. E' pensata per chi vuole approfondire il legame tra struttura dell'operatore e metodi numerici per l'evoluzione temporale.

In questa parte riformuliamo la dinamica discreta in linguaggio matriciale, mettendo in evidenza la struttura locale a tre punti del generatore e confrontando tre strategie numeriche diverse per l'evoluzione temporale.

L'obiettivo e' capire non solo che cosa si stia integrando, ma anche come la struttura dell'operatore suggerisca metodi numerici diversi.

## E.1 Il generatore come matrice sparsa tridiagonale

Per il random walk con bias con bordi riflettenti, la master equation si scrive in forma compatta come

$$
\dot p = L\,p,
$$

dove $L$ e' una matrice tridiagonale.

Per N+1 siti, L contiene solo pochi elementi non nulli per riga o colonna. Questo è il contesto naturale per usare una matrice sparsa invece di una matrice densa.

### Compiti

1. Costruire L in formato sparso.
2. Verificare che il numero di elementi non nulli cresca linearmente con N.
3. Confrontare, almeno qualitativamente, il costo di memoria di una rappresentazione densa e di una rappresentazione sparsa.

## E.2 Scomposizione del generatore in parte di drift e parte diffusiva

Usando la decomposizione vista nella mini-appendice, il generatore può essere scritto come somma di due pezzi:

* una parte di drift, antisimmetrica tra vicini;
* una parte diffusiva, simmetrica di smoothing.

Per i siti interni:

* la parte di drift è proporzionale a $(p_{i+1} - p_{i-1})$;
* la parte diffusiva è proporzionale a $(p_{i+1} + p_{i-1} - 2 p_i)$.

### Compiti

1. Costruire separatamente le due matrici sparse $L_{drift}$ e $L_{diff}$.
2. Verificare che $L = L_{drift} + L_{diff}$.
3. Discutere quale delle due parti è responsabile dello spostamento del baricentro e quale dell'allargamento della distribuzione.

## E.3 Tre strategie di evoluzione temporale

Vogliamo confrontare tre metodi diversi per approssimare l'evoluzione nel tempo della distribuzione.

### Metodo 1 -- Euler esplicito

Usare l'aggiornamento:

$$
p^{(n+1)} = p^{n} + \Delta t\,L p^n.
$$

È il metodo più semplice, ma richiede attenzione a:

* scelta di $\Delta t$;
* possibili probabilità negative;
* accuratezza limitata.

### Metodo 2 -- operator splitting

Usare la scomposizione $L = L_{drift} + L_{diff}$ e approssimare il propagatore come prodotto di due propagatori più semplici.

Per esempio:

* splitting di primo ordine: applicare prima il blocco di drift e poi il blocco diffusivo;
* splitting simmetrico di Strang: mezzo passo di drift, un passo diffusivo, mezzo passo di drift.

Se non si vogliono costruire esponenziali esatti dei blocchi, si possono anche usare sottopassi numerici distinti, purché sia chiaro che si sta realizzando una dinamica "spezzata".

### Metodo 3 -- full propagator

Usare direttamente il propagatore del sistema lineare, cioè l'esponenziale del generatore applicato al vettore iniziale.

Questo è il riferimento più naturale dal punto di vista formale, perché per un sistema lineare autonomo la soluzione esatta è data proprio dal propagatore del generatore.

Nel caso numerico, si può:

* costruire la matrice esponenziale per sistemi piccoli o moderati;
* oppure applicare l'azione dell'esponenziale sul vettore senza formare l'intera matrice piena.

## E.4 Compiti

1. Costruire il generatore sparso $L$.
2. Costruire la decomposizione $L = L_{drift} + L_{diff}$.
3. Evolvere la stessa condizione iniziale con:

   * Euler esplicito;
   * operator splitting;
   * full propagator.
4. Confrontare i tre risultati agli stessi tempi.
5. Misurare almeno una quantità d'errore, ad esempio una norma L1 oppure L2 rispetto a una soluzione di riferimento.
6. Verificare quale metodo preserva meglio:

   * la normalizzazione;
   * la non negatività;
   * la forma della distribuzione.

## E.5 Domande guida

1. Perché una matrice sparsa è la rappresentazione naturale di questo problema?
2. Euler esplicito introduce probabilità negative per passi troppo grandi?
3. Il full propagator conserva meglio la struttura probabilistica?
4. Lo splitting separa in modo utile il trasporto e lo smoothing?
5. Quale metodo è più conveniente se N cresce molto?

## E.6 Commento concettuale

Questo esercizio mostra un punto importante: la master equation non è solo una equazione differenziale per probabilità, ma anche un problema di evoluzione lineare generato da un operatore sparso locale.

Passare alla rappresentazione sparsa rende visibile sia:

* la struttura del modello;
* il legame con metodi numerici più avanzati basati sul propagatore.

# Possibili estensioni facoltative

1. Provare bordi assorbenti invece di riflettenti.
2. Provare condizioni periodiche al bordo
3. Studiare il rilassamento verso una distribuzione stazionaria su dominio finito con drift nullo.
4. Integrare direttamente una Fokker--Planck su griglia spaziale e confrontarla con gli istogrammi della SDE.
5. Esplorare il caso in cui i tassi dipendono dal sito $i$.

Queste estensioni non sono necessarie per il laboratorio base, ma chiariscono come la struttura vista qui si generalizzi a casi più ricchi.
