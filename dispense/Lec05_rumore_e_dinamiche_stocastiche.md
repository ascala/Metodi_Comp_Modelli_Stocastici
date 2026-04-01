---
title: "05: Rumore e dinamiche stocastiche"
author: ""
date: ""
---

In molti sistemi reali la dinamica osservata non è il risultato di una legge perfettamente deterministica. Anche quando esiste una tendenza media ben definita, il comportamento effettivo risente di fluttuazioni dovute a molte cause microscopiche, rapide, non osservabili nel dettaglio o semplicemente troppo numerose per essere modellate una per una. Le equazioni differenziali stocastiche (SDE, *stochastic differential equations*) nascono proprio per descrivere questa situazione: una componente regolare di evoluzione coesiste con una componente casuale.

Questa lezione introduce il formalismo di base delle SDE partendo dall’idea fisica di rumore bianco come forzante estremamente irregolare. Tale immagine è intuitivamente molto utile, ma non è sufficiente dal punto di vista matematico. Per ottenere una formulazione rigorosa bisogna passare dal rumore pensato come "funzione irregolare" al formalismo differenziale basato sul processo di Wiener. Da qui emergono naturalmente sia il calcolo di Ito sia il primo schema numerico fondamentale per la simulazione di traiettorie stocastiche: il metodo di Euler--Maruyama.

## Obiettivi della lezione

Al termine della lezione lo studente dovrebbe essere in grado di:

1. spiegare perché in molti sistemi dinamici sia naturale introdurre un termine di rumore;
2. distinguere fra rumore additivo e rumore moltiplicativo;
3. interpretare l’equazione di Langevin come prototipo di SDE;
4. comprendere perché il rumore bianco non possa essere trattato come una funzione ordinaria;
5. scrivere una SDE nella forma differenziale di Ito;
6. derivare in una dimensione la formula di Ito;
7. costruire lo schema di Euler--Maruyama;
8. distinguere tra accuratezza forte e accuratezza debole;
9. riconoscere esempi applicativi in diversi ambiti.

## Struttura

1. Perché introdurre il rumore nei modelli dinamici
2. Equazione di Langevin e prima forma intuitiva di SDE
3. Dal rumore bianco al processo di Wiener
4. Il calcolo di Ito
5. Integrazione numerica: Euler--Maruyama
6. Stabilità, accuratezza forte e debole
7. Esempi interdisciplinari
8. Sintesi finale

# 1. Perché introdurre il rumore nei modelli dinamici

In un modello deterministico, una volta assegnata la condizione iniziale, l’evoluzione futura è completamente fissata. Questa impostazione è spesso un primo passo utile, ma in molte situazioni reali non basta. Le variabili osservate fluttuano anche in presenza di condizioni iniziali molto simili, e tale variabilità non è un semplice errore sperimentale: è parte integrante del fenomeno.

Gli esempi sono numerosi.

In fisica, una particella immersa in un fluido subisce urti molecolari continui e irregolari. In chimica, il numero di collisioni efficaci in un intervallo di tempo piccolo non è perfettamente prevedibile. In biologia, l’espressione genica dipende da eventi discreti e rumorosi a livello cellulare. In finanza, i prezzi riflettono una sovrapposizione di decisioni eterogenee. Nelle scienze sociali, individui esposti allo stesso stimolo non reagiscono in modo perfettamente uniforme.

L’idea di base è allora la seguente: la dinamica osservata è il risultato della combinazione di

- una **parte sistematica**, che descrive la tendenza media;
- una **parte fluttuante**, che descrive l’effetto aggregato di molte cause irregolari.

Questa seconda componente viene chiamata **rumore**.

> **Idea chiave**  
> Il rumore non è necessariamente un difetto del modello. Spesso è il modo corretto di rappresentare l’effetto collettivo di molti gradi di libertà non risolti.

## 1.1 Rumore additivo e rumore moltiplicativo

Una prima distinzione importante riguarda il modo in cui il rumore entra nell’equazione.

Nel **rumore additivo**, l’intensità della fluttuazione non dipende dallo stato del sistema. Per esempio,

$$
dx = a(x,t)\,dt + \sigma\,dW_t.
$$

Nel **rumore moltiplicativo**, invece, l’intensità del rumore dipende dalla variabile stessa. Per esempio,

$$
dx = a(x,t)\,dt + \sigma x\,dW_t.
$$

Nel secondo caso, se $|x|$ aumenta, aumentano anche le fluttuazioni tipiche. Questo rende il problema qualitativamente più ricco e, come vedremo, rende importante specificare con precisione il significato dell’equazione.

# 2. Equazione di Langevin e prima forma intuitiva di SDE

Il punto di partenza storico è il moto browniano. Una particella microscopica sospesa in un fluido non segue una traiettoria liscia e regolare, ma un moto irregolare dovuto agli urti con le molecole dell’ambiente. Langevin propose di descrivere questa situazione separando una componente dissipativa da una componente casuale.

Nel caso più semplice, per la velocità $v(t)$ di una particella di massa $m$, si scrive

$$
m\,\frac{dv}{dt} = -\gamma v + \sigma\,\eta(t),
$$

dove

- $-\gamma v$ rappresenta l’attrito viscoso;
- $\sigma$ misura l’intensità della forza casuale;
- $\eta(t)$ rappresenta il rumore bianco.

Dal punto di vista fisico, $\eta(t)$ viene pensato come una forzante molto irregolare, con media nulla e correlazione istantanea:

$$
\langle \eta(t) \rangle = 0,
\qquad
\langle \eta(t)\eta(t') \rangle = \delta(t-t').
$$

Generalizzando, si arriva alla forma intuitiva

$$
\frac{dx}{dt} = a(x,t) + b(x,t)\eta(t).
$$

Questa è la forma con cui storicamente si introduce una SDE: un termine di drift $a(x,t)$ descrive la tendenza media, mentre $b(x,t)\eta(t)$ rappresenta la parte fluttuante.

> **Osservazione**  
> Questa scrittura è molto utile per l’intuizione fisica. Tuttavia, non è ancora la formulazione matematica rigorosa.

# 3. Dal rumore bianco al processo di Wiener

## 3.1 Il rumore bianco come funzione estremamente irregolare

Dal punto di vista della fisica è naturale immaginare $\eta(t)$ come una funzione del tempo estremamente irregolare: cambia rapidamente, oscilla in modo imprevedibile, non presenta una struttura liscia. Questa immagine è importante, perché spiega bene che cosa si voglia modellare.

Ma proprio qui nasce il problema matematico. Se si scrive

$$
\frac{dx}{dt} = a(x,t) + b(x,t)\eta(t),
$$

si sta implicitamente trattando $\eta(t)$ come una funzione ordinaria. In realtà il rumore bianco gaussiano non è una funzione classica. È un oggetto troppo singolare per essere manipolato con il calcolo differenziale usuale.

In particolare, non ha senso attribuirgli le stesse proprietà di regolarità che si attribuiscono a una funzione liscia o anche solo continua. Per questo motivo la scrittura con $\eta(t)$ deve essere interpretata come una rappresentazione intuitiva, non come il punto di partenza rigoroso.

## 3.2 L’idea corretta: lavorare con gli incrementi

Per rendere la teoria ben definita si smette di ragionare sulla "funzione" $\eta(t)$ istante per istante e si passa invece ai suoi incrementi integrati. Si introduce allora un processo $W_t$, detto **processo di Wiener** o **moto browniano**, tale che formalmente

$$
\eta(t) = \frac{dW_t}{dt}.
$$

Questa relazione non va intesa in senso classico. Serve solo a motivare il passaggio al formalismo corretto.

Il processo di Wiener è definito dalle seguenti proprietà:

1. $W_0 = 0$;
2. gli incrementi su intervalli disgiunti sono indipendenti;
3. per $t > s$, l’incremento $W_t - W_s$ è distribuito normalmente con media nulla e varianza $t-s$.

In simboli,

$$
W_t - W_s \sim \mathcal{N}(0,t-s).
$$

Su un piccolo intervallo temporale $dt$, l’incremento infinitesimo $dW_t$ soddisfa quindi formalmente

$$
\langle dW_t \rangle = 0,
\qquad
\langle dW_t^2 \rangle = dt.
$$

## 3.3 Forma generale di una SDE e terminologia di base

Una volta introdotto il processo di Wiener $W_t$, la forma rigorosa di una equazione differenziale stocastica in una dimensione si scrive come

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t.
$$

Questa equazione contiene due contributi concettualmente distinti.

Il termine

$$
a(x,t)\,dt
$$

descrive la parte regolare dell’evoluzione e prende il nome di **drift**. Esso rappresenta la tendenza media del sistema in assenza di fluttuazioni.

Il termine

$$
b(x,t)\,dW_t
$$

descrive invece la parte stocastica della dinamica. La funzione $b(x,t)$ misura quanto intensamente il rumore agisce sul sistema e viene spesso chiamata **coefficiente di diffusione** oppure **coefficiente del rumore**.

In altre parole:

- $a(x,t)$ determina la direzione media dell’evoluzione;
- $b(x,t)$ determina l’ampiezza delle fluttuazioni casuali;
- $b(x,t)\,dW_t$ è il **termine stocastico** della SDE.

Se $b(x,t)$ è costante, il rumore è detto **additivo**. Se invece dipende dallo stato $x$, il rumore è detto **moltiplicativo**.

Questa terminologia sarà utile anche più avanti: quando parleremo di integrali di Ito e di Stratonovich, la differenza riguarderà precisamente il modo in cui viene interpretato e discretizzato l’integrale stocastico associato al termine

$$
b(X_t,t)\,dW_t.
$$

## 3.4 Perché $dW_t$ è dell’ordine di $\sqrt{dt}$

Poiché la varianza di $dW_t$ è $dt$, la dimensione tipica delle sue fluttuazioni è dell’ordine di $\sqrt{dt}$. Questo non significa che $dW_t = \sqrt{dt}$, ma che la sua scala caratteristica è quella.

Ne segue che

$$
(dW_t)^2
$$

è dell’ordine di

$$
dt.
$$

Ed è proprio questa osservazione a rendere diverso il calcolo stocastico rispetto al calcolo ordinario. Nei passaggi algebrici, un termine quadratico in $dW_t$ non può essere semplicemente trascurato come si farebbe con $(dt)^2$.

> **Da ricordare**  
> Nel calcolo differenziale:
> - si mantengono i termini del primo ordine (ovvero in $dt$)
> - $dt^2$ si trascura.
> Nel calcolo stocastico:
> - si mantegono i termini fino al primo ordine (ovvero in $dW_t$ e $dt$)
> -  $dt^2$ si trascura;
> - $dt\,dW_t$ si trascura;
> - $(dW_t)^2$ invece contribuisce a ordine $dt$.

# 4. Il calcolo di Ito

## 4.1 Dal caso deterministico al caso stocastico

Nel caso deterministico, se 

$$
dx = a(x,t)\,dt,
$$

allora per una funzione regolare $f(x,t)$ vale la regola usuale

$$
df = \frac{\partial f}{\partial t}\,dt + \frac{\partial f}{\partial x}\,dx 
+ \text{termini di ordine superiore}.
$$

Nel caso stocastico, invece, bisogna tenere conto del fatto che il termine quadratico in $dx$ non sarà trascurabile, proprio perché $dx$ conterrà $dW_t$.

Supponiamo allora che

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t.
$$

Sviluppando $f(x+dx,t+dt)$ fino all’ordine rilevante, si ottiene

$$
df = \frac{\partial f}{\partial t}\,dt
+ \frac{\partial f}{\partial x}\,dx
+ \frac{1}{2}\frac{\partial^2 f}{\partial x^2}(dx)^2
+ \text{termini di ordine superiore}.
$$

## 4.2 Le regole differenziali di Ito

Per calcolare $(dx)^2$ usiamo la SDE:

$$
(dx)^2 = \left(a\,dt + b\,dW_t\right)^2.
$$

Sviluppando,

$$
(dx)^2 = a^2dt^2 + 2ab\,dt\,dW_t + b^2(dW_t)^2.
$$

A questo punto si usano le regole formali di Ito:

$$
dt^2 = 0,
\qquad
dt\,dW_t = 0,
\qquad
(dW_t)^2 = dt.
$$

Segue quindi

$$
(dx)^2 = b(x,t)^2\,dt.
$$

Sostituendo nell’espansione precedente otteniamo

$$
df =
\frac{\partial f}{\partial t}\,dt
+
\frac{\partial f}{\partial x}\,dx
+
\frac{1}{2}b(x,t)^2\frac{\partial^2 f}{\partial x^2}\,dt.
$$

Infine, sostituendo anche $dx$,

$$
df =
\left(
\frac{\partial f}{\partial t}
+
a(x,t)\frac{\partial f}{\partial x}
+
\frac{1}{2}b(x,t)^2\frac{\partial^2 f}{\partial x^2}
\right)dt
+
b(x,t)\frac{\partial f}{\partial x}\,dW_t.
$$

Questa è la **formula di Ito** in una dimensione.

## 4.3 Un esempio elementare: $f(x)=x^2$

Se $f(x)=x^2$, allora

$$
\frac{\partial f}{\partial x}=2x,
\qquad
\frac{\partial^2 f}{\partial x^2}=2.
$$

La formula di Ito diventa

$$
d(x^2) = 2x\,dx + b(x,t)^2\,dt.
$$

Il termine aggiuntivo $b(x,t)^2dt$ è precisamente il contributo che non apparirebbe nel calcolo ordinario.

Questo esempio è molto istruttivo, perché mostra in modo immediato che il calcolo stocastico non è una semplice imitazione del calcolo differenziale classico.

## 4.4 Nota su Ito e Stratonovich

Esiste anche un’altra interpretazione delle SDE, detta di Stratonovich, nella quale si scrive

$$
dx = a_S(x,t)\,dt + b(x,t)\circ dW_t.
$$

La differenza tra Ito e Stratonovich non è solo notazionale: riguarda il modo in cui viene definito l’integrale stocastico associato al termine diffusivo

$$
b(X_t,t)\,dW_t.
$$

In una discretizzazione temporale con passi $[t_n,t_{n+1}]$:

- nell’interpretazione di **Ito** il coefficiente $b$ viene valutato all’inizio dell’intervallo;
- nell’interpretazione di **Stratonovich** si usa invece una valutazione simmetrica, che intuitivamente può essere pensata come una valutazione a mezzo intervallo.

Per questo motivo il formalismo di Stratonovich risulta più vicino, nella forma, al calcolo differenziale ordinario, mentre il formalismo di Ito è particolarmente naturale per l’analisi probabilistica e per la costruzione di schemi numerici semplici come Euler--Maruyama.

Per questa lezione adotteremo sistematicamente il formalismo di **Ito**.

# 5. Integrazione numerica: Euler--Maruyama

Una volta scritta la SDE nella forma

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t,
$$

il passo successivo è costruire un algoritmo di simulazione.

## 5.1 Dalla forma integrale allo schema discreto

Consideriamo un intervallo temporale $[t_n,t_{n+1}]$ di ampiezza $\Delta t$. Integrando formalmente la SDE si ha

$$
x_{n+1} - x_n = \int_{t_n}^{t_{n+1}} a(x_t,t)\,dt
+ \int_{t_n}^{t_{n+1}} b(x_t,t)\,dW_t.
$$

L’idea più semplice è -- coerentemente con Ito -- approssimare entrambi i coefficienti usando il valore all’inizio del passo:

$$
a(x_t,t) \approx a(x_n,t_n),
\qquad
b(x_t,t) \approx b(x_n,t_n).
$$

Si ottiene così

$$
x_{n+1} \approx x_n + a(x_n,t_n)\Delta t + b(x_n,t_n)\Delta W_n,
$$

dove

$$
\Delta W_n = W_{t_{n+1}} - W_{t_n}.
$$

Poiché gli incrementi browniani sono gaussiani indipendenti,

$$
\Delta W_n \sim \mathcal{N}(0,\Delta t).
$$

Possiamo quindi scrivere

$$
\Delta W_n = \sqrt{\Delta t}\,\xi_n,
\qquad
\xi_n \sim \mathcal{N}(0,1).
$$

Ne deriva lo schema di integrazione detto di di **Euler--Maruyama**:

$$
x_{n+1} = x_n
+ a(x_n,t_n)\Delta t
+ b(x_n,t_n)\sqrt{\Delta t}\,\xi_n.
$$

## 5.2 Interpretazione dello schema

Lo schema contiene due contributi:

1. un contributo deterministico,
   $$
   a(x_n,t_n)\Delta t,
   $$
   che è l’analogo del metodo di Eulero per le ODE;

2. un contributo casuale,
   $$
   b(x_n,t_n)\sqrt{\Delta t}\,\xi_n,
   $$
   che rappresenta la fluttuazione sul singolo passo temporale.

Ogni sequenza diversa di variabili gaussiane $\xi_n$ produce una traiettoria diversa. Per questo una SDE non genera una sola curva, ma un insieme di realizzazioni compatibili con la stessa legge dinamica.

## 5.3 Esempio minimale in Python

```python
import numpy as np
import matplotlib.pyplot as plt

def drift(x, t):
    return -0.5 * x

def diffusion(x, t):
    return 0.3

def euler_maruyama(x0, dt, N):
    t = np.linspace(0.0, N * dt, N + 1)
    x = np.zeros(N + 1)
    x[0] = x0

    for n in range(N):
        xi = np.random.randn()
        x[n + 1] = (
            x[n]
            + drift(x[n], t[n]) * dt
            + diffusion(x[n], t[n]) * np.sqrt(dt) * xi
        )

    return t, x

t, x = euler_maruyama(x0=1.0, dt=0.01, N=1000)

plt.plot(t, x)
plt.xlabel("tempo")
plt.ylabel("x(t)")
plt.show()
````

Questo codice produce una singola traiettoria. Ripetendo la simulazione si otterranno traiettorie diverse, tutte coerenti con la stessa SDE.

# 6. Stabilità, accuratezza forte e debole

## 6.1 Stabilità: il caso di Ornstein--Uhlenbeck

Consideriamo la SDE lineare

$$
dx = -\lambda x,dt + \sigma,dW_t,
\qquad \lambda > 0.
$$

Si tratta del processo di Ornstein--Uhlenbeck, che descrive una dinamica con richiamo verso l’origine e rumore additivo.

Applicando Euler--Maruyama si ottiene

$$
x_{n+1} = (1-\lambda\Delta t)x_n + \sigma\sqrt{\Delta t},\xi_n.
$$

Affinché la parte deterministica discreta non risulti instabile, è necessario che

$$
|1-\lambda\Delta t| < 1,
$$

ossia

$$
0 < \Delta t < \frac{2}{\lambda}.
$$

Questa condizione è un utile criterio pratico: se $\Delta t$ è troppo grande, la discretizzazione può introdurre oscillazioni o amplificazioni spurie che non appartengono alla dinamica continua.

## 6.2 Accuratezza forte

L’accuratezza forte misura quanto bene il metodo numerico riproduce una singola traiettoria della SDE.

In teoria, si confronta la soluzione numerica $X_T^{(\Delta t)}$ con la soluzione esatta $X_T$, costruite usando la stessa realizzazione del moto browniano. In pratica, quando la soluzione esatta non è disponibile in forma chiusa, si sostituisce $X_T$ con una soluzione di riferimento ottenuta con una discretizzazione molto più fine.

Per Euler--Maruyama, l’errore forte è di ordine $1/2$: ciò significa che, per $\Delta t$ piccolo,

$$
\mathbb{E}\big[|X_T - X_T^{(\Delta t)}|\big] \sim (\Delta t)^{1/2},
$$

oppure, in pratica numerica, che l’errore rispetto a una soluzione di riferimento molto accurata decresce tipicamente come $\Delta t^{1/2}$.

## 6.3 Accuratezza debole

L’**accuratezza debole** riguarda invece le quantità statistiche, come medie, momenti o aspettative di osservabili. In questo caso non interessa riprodurre bene ogni singola traiettoria, ma ottenere correttamente il comportamento medio dell’insieme.

Per Euler--Maruyama, l’ordine debole è

$$
1.
$$

Quindi, se il nostro obiettivo è stimare medie su molte traiettorie, il metodo converge più rapidamente di quanto non faccia nel senso forte.

> **Attenzione**
> "Approssimare bene una traiettoria" e "approssimare bene una media" sono due obiettivi diversi. Nelle SDE bisogna sempre chiedersi quale dei due sia rilevante per il problema studiato.

## 6.4 Esempio guida

Per la SDE di Ornstein--Uhlenbeck

$$
dx = -\lambda x\,dt + \sigma\,dW_t,
$$

la soluzione esatta è

$$
x(t) = x_0 e^{-\lambda t}
+ \sigma \int_0^t e^{-\lambda (t-s)}\,dW_s.
$$

Prendendo il valore atteso, il termine stocastico ha media nulla e si ottiene

$$
\mathbb{E}[x(t)] = x_0 e^{-\lambda t}.
$$

Questa formula è utile in pratica:

* per verificare la convergenza **forte** si confrontano traiettorie corrispondenti;
* per verificare la convergenza **debole** si confronta la media empirica di molte simulazioni con la quantità esatta $\mathbb{E}[x(t)]$.

# 7. Esempi interdisciplinari

Le SDE compaiono in molti contesti diversi. In tutti i casi ritroviamo la stessa struttura di base: un drift che descrive la tendenza media e una parte rumorosa che rappresenta fluttuazioni o incertezze.

## 7.1 Fisica: oscillatore armonico con rumore

Un oscillatore lineare immerso in un ambiente termico può essere modellato come

$$
dx = v\,dt,
\qquad
dv = -\gamma v\,dt - kx\,dt + \sigma\,dW_t.
$$

Il termine elastico $-kx$ tende a riportare il sistema verso l’equilibrio, il termine $-\gamma v$ rappresenta lo smorzamento, mentre $\sigma\,dW_t$ descrive le fluttuazioni termiche.

## 7.2 Chimica: dinamica attivata in un doppio pozzo

Per una coordinata di reazione soggetta a rumore termico si può scrivere

$$
dx = -U'(x)\,dt + \sigma\,dW_t,
$$

con

$$
U(x) = \frac{1}{4}x^4 - \frac{1}{2}x^2.
$$

In questo caso il drift tende a confinare il sistema in uno dei due pozzi di potenziale, mentre il rumore può indurre transizioni rare da un pozzo all’altro.

## 7.3 Biologia: espressione genica

Un modello minimale per la concentrazione di una proteina è

$$
dx = (\alpha - \beta x)\,dt + \sigma\,dW_t.
$$

Il termine $\alpha$ rappresenta la produzione media, il termine $\beta x$ la degradazione, mentre il rumore sintetizza la variabilità dovuta al carattere discreto e intermittente degli eventi biochimici.

## 7.4 Finanza: moto geometrico browniano

Un modello classico per il prezzo $S_t$ di un attivo è

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t.
$$

Qui il rumore è moltiplicativo: l’ampiezza delle fluttuazioni cresce con il livello del prezzo.

## 7.5 Ecologia: crescita logistica con rumore ambientale

Per una popolazione $x(t)$ si può usare

$$
dx = r x\left(1-\frac{x}{K}\right)dt + \sigma x\,dW_t.
$$

La parte deterministica è la crescita logistica (tasso di riproduzione $r$ e capacità del sistema $K$), mentre il termine moltiplicativo rappresenta variazioni ambientali che agiscono proporzionalmente alla popolazione presente.

## 7.6 Ingegneria: sistemi con disturbi e incertezza di misura

In molti problemi di controllo compare una dinamica del tipo

$$
dx = f(x,t)\,dt + G(x,t)\,dW_t,
$$

dove il secondo termine rappresenta disturbi esterni, rumore di attuazione o incertezza nei sensori.

## 7.7 Scienze sociali: propensioni individuali con fluttuazioni

Una variabile continua $x(t)$ che rappresenti opinione, preferenza o propensione a una scelta può essere modellata come

$$
dx = (-\gamma x + F(t))\,dt + \sigma\,dW_t,
$$

dove $F(t)$ descrive l’influenza esterna o sociale, mentre il termine rumoroso raccoglie la variabilità individuale non spiegata.

---

# 8. Sintesi finale

Le SDE nascono dall’esigenza di descrivere sistemi nei quali l’evoluzione non è governata soltanto da leggi medie, ma anche da fluttuazioni rapide e irregolari.

La fisica suggerisce naturalmente di introdurre una forzante casuale $\eta(t)$, pensata come funzione estremamente irregolare del tempo. Questa immagine è utile e va mantenuta a livello intuitivo. Tuttavia, per essere rigorosi, bisogna abbandonare l’idea di trattare $\eta(t)$ come una funzione ordinaria e passare invece al processo di Wiener $W_t$.

Questo conduce alla forma differenziale

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t,
$$

che è il punto di partenza del calcolo di Ito. La regola formale

$$
(dW_t)^2 = dt
$$

produce il termine correttivo caratteristico della formula di Ito e distingue nettamente il calcolo stocastico dal calcolo differenziale classico.

Dal punto di vista numerico, questa struttura porta in modo naturale allo schema di Euler--Maruyama,

$$
x_{n+1} = x_n
+ a(x_n,t_n)\Delta t
+ b(x_n,t_n)\sqrt{\Delta t},\xi_n,
$$

che è il primo strumento essenziale per simulare traiettorie di una SDE.

In sintesi, il percorso concettuale della lezione è il seguente:

1. il rumore viene introdotto per modellare fluttuazioni reali;
2. l’immagine fisica del rumore bianco suggerisce una forzante molto irregolare;
3. la formulazione rigorosa richiede il passaggio al processo di Wiener;
4. il calcolo di Ito fornisce le regole corrette di manipolazione;
5. Euler--Maruyama traduce il formalismo in un algoritmo.

Questa è la base naturale per gli sviluppi successivi del corso: equazione di Fokker--Planck, metodi numerici più accurati, SDE multidimensionali e processi con salti.

## Riferimenti essenziali

* Langevin, P. (1908). *Sur la théorie du mouvement brownien*. C. R. Acad. Sci. 146: 530--533.
* Gardiner, C. (2004). *Handbook of Stochastic Methods*. Springer.
* Risken, H. (1989). *The Fokker--Planck Equation*. Springer.
* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review, 43(3): 525--546.
* Gillespie, D. T. (2000). *The chemical Langevin equation*. J. Chem. Phys. 113(1): 297--306.

# Appendice -- Integrali stocastici e somme di Riemann

Per capire la differenza tra integrale di Ito e integrale di Stratonovich è utile partire dall’idea di approssimare un integrale tramite somme discrete, come si fa nel caso ordinario.

Consideriamo una partizione dell’intervallo $[0,T]$:

$$
0 = t_0 < t_1 < \cdots < t_N = T,
\qquad
\Delta t_n = t_{n+1} - t_n,
\qquad
\Delta W_n = W_{t_{n+1}} - W_{t_n}.
$$

Nel caso deterministico, un integrale di Riemann si costruisce come limite di somme del tipo

$$
\sum_{n=0}^{N-1} f(\tau_n)\,\Delta t_n,
$$

dove $\tau_n \in [t_n,t_{n+1}]$ è un punto scelto nel sottointervallo. Per funzioni regolari, il limite non dipende dalla scelta precisa di $\tau_n$.

Nel caso stocastico, invece, vogliamo definire un integrale del tipo

$$
\int_0^T b(X_t,t)\,dW_t.
$$

Qui la situazione cambia in modo sostanziale, perché il moto browniano è molto irregolare. Si considerano allora somme del tipo

$$
\sum_{n=0}^{N-1} b(X_{\tau_n},\tau_n)\,\Delta W_n.
$$

A differenza del caso ordinario, il limite dipende dalla scelta del punto $\tau_n$ nel sottointervallo.

## Integrale di Ito

Nell’interpretazione di Ito si sceglie il punto sinistro:

$$
\tau_n = t_n.
$$

Quindi l’integrale è definito come limite di somme del tipo

$$
\sum_{n=0}^{N-1} b(X_{t_n},t_n)\,\Delta W_n.
$$

In questa costruzione il coefficiente $b$ viene valutato all’inizio dell’intervallo. Questa scelta rende l’integrale particolarmente adatto all’analisi probabilistica, perché il fattore $b(X_{t_n},t_n)$ dipende solo dall’informazione disponibile fino al tempo $t_n$.

## Integrale di Stratonovich

Nell’interpretazione di Stratonovich si usa invece una discretizzazione simmetrica. In modo intuitivo, si può pensare a una valutazione al punto medio:

$$
\tau_n \approx \frac{t_n+t_{n+1}}{2}.
$$

Schematicamente, l’integrale corrisponde al limite di somme del tipo

$$
\sum_{n=0}^{N-1} b\!\left(X_{\frac{t_n+t_{n+1}}{2}}, \frac{t_n+t_{n+1}}{2}\right)\,\Delta W_n,
$$

oppure, in forma ancora più simmetrica, a medie tra estremo sinistro ed estremo destro

$$
\sum_{n=0}^{N-1} \frac{b(X_{t_n},t_n)+b(X_{t_{n+1}},t_{n+1})}{2}\,\Delta W_n.
$$

Questa scelta fa sì che il calcolo di Stratonovich assomigli di più al calcolo differenziale ordinario.

## Perché i due integrali non coincidono?

Nel calcolo ordinario, cambiando il punto di campionamento dentro ciascun sottointervallo si ottiene lo stesso limite, purché le funzioni siano abbastanza regolari. Nel caso stocastico questo non è più vero, perché gli incrementi browniani sono troppo irregolari: il processo ha variazione quadratica non nulla, e proprio questo genera la differenza tra Ito e Stratonovich.

In termini intuitivi:

- con **Ito** si guarda il coefficiente all’inizio del passo;
- con **Stratonovich** si usa una valutazione simmetrica, circa a mezzo intervallo.

Per questo i due formalismi portano a regole di calcolo diverse.

## Formula di conversione

Se una stessa dinamica è scritta in forma di Stratonovich come

$$
dx = a_S(x,t)\,dt + b(x,t)\circ dW_t,
$$

allora la forma equivalente di Ito è

$$
dx = a_I(x,t)\,dt + b(x,t)\,dW_t,
$$

con

$$
a_I(x,t) = a_S(x,t) + \frac{1}{2} b(x,t)\,\partial_x b(x,t).
$$

Quindi la differenza tra le due interpretazioni si traduce in un termine correttivo nel drift.

> **Da ricordare**
>
> - Ito: coefficiente valutato all’inizio dell’intervallo;
> - Stratonovich: coefficiente valutato in modo simmetrico, intuitivamente a mezzo intervallo;
> - per il moto browniano, queste due scelte non portano allo stesso limite;
> - la differenza si manifesta come un termine correttivo nel drift.

# Appendice -- Lo schema di Milstein nel caso scalare

Nella lezione principale abbiamo introdotto lo schema di Euler--Maruyama come metodo numerico piú semplice per integrare una SDE della forma

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t.
$$

Esistono però schemi leggermente piú accurati. Il piú importante, nel caso di una SDE scalare, è lo **schema di Milstein**, che aggiunge a Euler--Maruyama un termine correttivo legato alla dipendenza del coefficiente di rumore dalla variabile di stato.

In questa appendice ne presentiamo una derivazione elementare, sufficiente per capire la formula usata nel laboratorio.

## A.1 Punto di partenza

Scriviamo la SDE in forma integrale su un intervallo $[t_n,t_{n+1}]$ di ampiezza $\Delta t$:

$$
X_{n+1} - X_n =
\int_{t_n}^{t_{n+1}} a(X_s,s)\,ds
+ \int_{t_n}^{t_{n+1}} b(X_s,s)\,dW_s.
$$

Lo schema di Euler--Maruyama si ottiene sostituendo semplicemente

$$
a(X_s,s) \approx a(X_n,t_n),
\qquad
b(X_s,s) \approx b(X_n,t_n),
$$

da cui segue

$$
X_{n+1} = X_n
+ a(X_n,t_n)\Delta t
+ b(X_n,t_n)\Delta W_n,
$$

dove

$$
\Delta W_n = W_{t_{n+1}} - W_{t_n}.
$$

Questo schema è semplice, ma trascura il fatto che, se $b$ dipende da $X$, il coefficiente del rumore cambia già all’interno del passo temporale.

## A.2 Idea della correzione

Per migliorare l’approssimazione, nel termine stocastico sviluppiamo $b(X_s,s)$ intorno al punto iniziale del passo. Trascurando i contributi di ordine piú alto e concentrandoci sul caso scalare, si usa l’approssimazione

$$
b(X_s,s)
\approx
b(X_n,t_n)
+
\partial_x b(X_n,t_n)\,(X_s - X_n).
$$

A sua volta, al primo ordine stocastico,

$$
X_s - X_n \approx b(X_n,t_n)\,(W_s - W_{t_n}).
$$

Sostituendo nell’integrale stocastico si ottiene

$$
\int_{t_n}^{t_{n+1}} b(X_s,s)\,dW_s
\approx
b(X_n,t_n)\Delta W_n
+
b(X_n,t_n)\partial_x b(X_n,t_n)
\int_{t_n}^{t_{n+1}} (W_s - W_{t_n})\,dW_s.
$$

Resta dunque da calcolare l’integrale

$$
\int_{t_n}^{t_{n+1}} (W_s - W_{t_n})\,dW_s.
$$

## A.3 L’integrale chiave

Poniamo

$$
Y_s = W_s - W_{t_n}.
$$

Allora $dY_s = dW_s$ e, usando la formula di Ito per $Y_s^2$, si ha

$$
d(Y_s^2) = 2Y_s\,dW_s + ds.
$$

Integrando da $t_n$ a $t_{n+1}$,

$$
Y_{t_{n+1}}^2 - Y_{t_n}^2 = 2\int_{t_n}^{t_{n+1}} Y_s\,dW_s + \Delta t.
$$

Poiché $Y_{t_n}=0$ e $Y_{t_{n+1}}=\Delta W_n$, segue

$$
(\Delta W_n)^2 = 2\int_{t_n}^{t_{n+1}} (W_s - W_{t_n})\,dW_s + \Delta t.
$$

Quindi

$$
\int_{t_n}^{t_{n+1}} (W_s - W_{t_n})\,dW_s =
\frac{1}{2}\left((\Delta W_n)^2 - \Delta t\right).
$$

Questa è la correzione tipica che compare nello schema di Milstein.

## A.4 Formula finale di Milstein

Sostituendo il risultato precedente nell’approssimazione dell’integrale stocastico, si ottiene lo schema di Milstein:

$$
\begin{aligned}
X_{n+1} ={}& X_n
+ a(X_n,t_n)\,\Delta t
+ b(X_n,t_n)\,\Delta W_n +\\
&+ \frac{1}{2}\, b(X_n,t_n)\,\partial_x b(X_n,t_n)
\left((\Delta W_n)^2 - \Delta t\right).
\end{aligned}
$$

Rispetto a Euler--Maruyama compare dunque un termine aggiuntivo:

$$
\frac{1}{2} b(X_n,t_n)\partial_x b(X_n,t_n) \left((\Delta W_n)^2 - \Delta t\right),
$$

che tiene conto, al primo ordine utile, della variazione del coefficiente di rumore lungo il passo.

### A.5 Commento sull’accuratezza

Nel caso scalare, lo schema di Milstein migliora l’accuratezza forte rispetto a Euler--Maruyama:

- Euler--Maruyama ha ordine forte $1/2$;
- Milstein ha ordine forte $1$.

Per questo Milstein è spesso usato come primo miglioramento naturale di Euler--Maruyama quando si vuole approssimare meglio le singole traiettorie.

### A.6 Il caso del laboratorio

Nel laboratorio consideriamo la SDE

$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t.
$$

Qui

$$
a(x,t)=\mu x,
\qquad
b(x,t)=\sigma x,
\qquad
\partial_x b(x,t)=\sigma.
$$

Quindi lo schema di Milstein diventa

$$
X_{n+1} = X_n
+ \mu X_n\Delta t
+ \sigma X_n\Delta W_n
+ \frac{1}{2}\sigma^2 X_n\left((\Delta W_n)^2 - \Delta t\right).
$$

Questa è la formula che potrà essere usata come confronto con Euler--Maruyama.

### A.7 Osservazione finale

Lo schema di Milstein non risolve automaticamente tutti i problemi qualitativi di una discretizzazione. Per esempio, nel modello del laboratorio la soluzione esatta resta positiva, ma anche Milstein può produrre valori negativi per passi temporali non abbastanza piccoli. Il suo vantaggio principale è l’aumento di accuratezza forte, non la preservazione automatica della struttura del modello.