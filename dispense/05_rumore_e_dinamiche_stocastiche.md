---
title: "Rumore e dinamiche stocastiche"
author: ""
date: ""
---

# Rumore e dinamiche stocastiche

Il rumore non è soltanto un disturbo: in molti sistemi è parte integrante della dinamica.  
Nei modelli stocastici, l’incertezza è rappresentata esplicitamente, e il comportamento medio emerge da molte realizzazioni del processo. La teoria di Langevin fornisce un linguaggio unificato per descrivere questi fenomeni, dal moto delle particelle al comportamento collettivo di popolazioni e agenti.

### Obiettivi didattici specifici

1. Capire che cosa si intende per **rumore** in un sistema dinamico e da dove nasce.  
2. Distinguere fra **rumore additivo** e **rumore moltiplicativo**.  
3. Introdurre la forma concettuale dell’**equazione di Langevin**.  
4. Interpretare le traiettorie stocastiche come famiglie di possibili evoluzioni.  
5. Collegare le dinamiche stocastiche a fenomeni reali (fisici, biologici, sociali).

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Rumore e fluttuazioni nei modelli reali** – da errore sperimentale a fattore dinamico.  
2. **Concetto di equazione stocastica** – l’idea di evoluzione casuale nel tempo.  
3. **Equazione di Langevin** – modello base del moto browniano.  
4. **Simulazioni numeriche di traiettorie** – metodo di Euler–Maruyama (intuitivo).  
5. **Esempi interdisciplinari** – diffusione, apprendimento, mercati, reti sociali.

---

## 1. Rumore e fluttuazioni nei modelli reali

Quando si costruisce un modello dinamico ci si trova spesso a distinguere tra le componenti prevedibili dell evoluzione e quelle che riflettono variabilita intrinseca o fattori non osservati. In un modello deterministico ogni stato futuro e fissato una volta specificate le condizioni iniziali, ma molti sistemi reali mostrano deviazioni sistematiche da questa idealizzazione. Tali deviazioni non sono semplici imperfezioni sperimentali. In numerosi contesti rappresentano invece una componente strutturale della dinamica.

Nei sistemi fisici le collisioni molecolari avvengono con tempi ed intensitá che fluttuano attorno a valori medi. Nelle reazioni chimiche elementari il numero di urti efficaci varia casualmente da un intervallo temporale al successivo. In epidemiologia il momento esatto in cui un individuo infetto trasmette il contagio a un suscettibile dipende da interazioni irregolari e non sincronizzate. Nei mercati finanziari la sovrapposizione di scelte eterogenee produce oscillazioni nei prezzi anche in assenza di segnali macroeconomici evidenti. Nei sistemi sociali le risposte individuali a stimoli comuni manifestano una dispersione che non puó essere ridotta a un semplice errore di misura.

Il termine rumore indica l'effetto aggregato di tali cause non modellate che tuttavia presentano una regolarita statistica sufficiente per essere descritte mediante modelli probabilistici. Introdurre il rumore in un modello significa riconoscere che la dinamica osservata emerge dalla combinazione di una tendenza media e di fluttuazioni attorno ad essa. Questa distinzione permette di catturare fenomeni la cui variabilita non e un semplice dettaglio ma una proprieta fondamentale.

Una prima classificazione distingue tra rumore additivo e rumore moltiplicativo. Nel rumore additivo si introduce una perturbazione che non dipende dallo stato della variabile, e che agisce come un contributo esterno che si somma alla dinamica deterministica. Nel rumore moltiplicativo l´intensita delle fluttuazioni dipende invece dal valore della variabile stessa, come accade ad esempio nei processi di reazione popolazione in cui la variabilita delle trasformazioni aumenta al crescere del numero di individui disponibili. Questa distinzione é cruciale perche conduce a comportamenti qualitativamente diversi e richiede metodi di analisi e di simulazione appropriati.

---

## 2. Concetto di equazione stocastica

Il punto di partenza è il moto browniano, osservato da Robert Brown nel 1827 come movimento irregolare di minuscole particelle sospese in un fluido. Questo fenomeno, apparentemente caotico, si presta però a una lettura più generale: quando un sistema interagisce con un ambiente complesso composto da molti elementi, l’effetto complessivo di tali interazioni può essere trattato come una sorgente di variabilità non prevedibile nel dettaglio.

Einstein e Smoluchowski, nei primi anni del Novecento, mostrarono che il moto browniano può essere interpretato come il risultato di fluttuazioni microscopiche che, su scale temporali più lunghe, generano una dinamica di diffusione. La loro analisi mise in relazione l’irregolarità delle interazioni locali con una regolarità statistica a livello macroscopico. Paul Langevin riformulò queste idee introducendo un’equazione che combina una forza deterministica con un termine stocastico, fornendo un modello compatto per descrivere sistemi soggetti a variabilità rapida e non controllabile.

Per illustrare la struttura del modello, consideriamo una variabile che evolve nel tempo sotto l’azione di due contributi. Il primo è una tendenza sistematica che riflette meccanismi noti e riproducibili. Il secondo è un contributo casuale che rappresenta l’effetto aggregato di molte influenze piccole e indipendenti. Nel caso originario studiato da Langevin, la variabile è la velocità $v(t)$ di una particella di massa $m$, e l’equazione assume la forma

$$
m\,\frac{dv}{dt} = -\gamma v + \sqrt{2D\gamma^2}\,\eta(t)
$$

Langevin descriveva quindi la forza agente sulla particella come composta da due parti. La forza deterministica classica $-\gamma v$ rappresenta la viscosità del mezzo e descrive il contributo dissipativo che frena il moto della particella. La forza casuale $\sqrt{2D\gamma^2}\,\eta(t)$ rappresenta invece l’azione irregolare degli urti con le molecole dell’ambiente. Il parametro $D$ controlla l’intensità di queste fluttuazioni e definisce la scala della diffusione osservata.

Il processo $\eta(t)$ è modellato come rumore bianco gaussiano, un contributo variabile nel tempo con media nulla e correlazione concentrata nell’istante:

$$
\langle \eta(t) \rangle = 0, \qquad
\langle \eta(t)\eta(t') \rangle = \delta(t - t') .
$$

Queste proprietà esprimono l’idea che le fluttuazioni agiscano in modo rapido, imprevedibile e non correlato nel tempo. Pur essendo un’idealizzazione, questa scelta permette di rappresentare in maniera efficace molti fenomeni in cui il dettaglio delle interazioni elementari non è disponibile o non è rilevante rispetto al comportamento complessivo.

Questa prospettiva conduce allo studio delle equazioni differenziali stocastiche, che generalizzano le equazioni deterministiche introducendo un termine di rumore. In forma astratta, una variabile $x(t)$ che rappresenta una quantità osservabile (come la posizione di una particella, il numero di individui infetti, la concentrazione di una sostanza chimica o anche il prezzo di un’azione) può essere modellata come

$$
\frac{dx}{dt} = a(x,t) + b(x,t)\,\eta(t)
$$

dove $a(x,t)$ descrive la dinamica media del sistema e $b(x,t)\eta(t)$ rappresenta il contributo stocastico che introduce fluttuazioni. Questa forma sintetizza l’idea fondamentale delle  **equazioni differenziali stocastiche** (SDE, *Stochastic Differential Equations*) : l’evoluzione temporale di una variabile è il risultato combinato di un meccanismo sistematico (deterministico) e di un disturbo casuale (stocastico). Esse permettono di descrivere quantitativamente sistemi dinamici soggetti a **rumore aleatorio continuo nel tempo**; le traiettorie risultanti non sono quindi singole curve deterministiche ma famiglie di possibili evoluzioni, ciascuna delle quali riflette una realizzazione diversa del processo di rumore. L’idea di fondo è estendere le equazioni differenziali ordinarie (ODE) per includere, oltre al termine deterministico, un contributo dovuto al rumore, modellato tramite il **moto browniano** o processi affini.

---

## 3. Perché serve un nuovo formalismo: dal rumore bianco al calcolo di Ito

L’equazione stocastica scritta nella forma “alla Leibniz”

$$
dx = a(x,t)\,dt + b(x,t)\,\eta(t)\,dt
$$

è intuitiva ma non ancora rigorosa. Il motivo è che il processo $\eta(t)$, quando modellato come rumore bianco gaussiano, non può essere trattato come una funzione ordinaria del tempo: le sue realizzazioni sono estremamente irregolari, non possiedono derivata e presentano oscillazioni arbitrariamente rapide. Di conseguenza l’oggetto $\eta(t)$ non può essere manipolato come una quantità analoga a quelle che compaiono nelle equazioni differenziali classiche.

In questa forma, quindi, l’espressione $\,\eta(t)\,dt\,$ non è il prodotto di due infinitesimi ordinari, ma un modo informale per rappresentare un contributo stocastico infinitesimo con media nulla e varianza proporzionale all’intervallo di tempo considerato. Per passare a un trattamento matematicamente consistente si introduce un diverso approccio: invece di lavorare direttamente con $\eta(t)$, si considerano i suoi incrementi integrati, che sono oggetti ben definiti e con proprietà statistiche controllate.

Questo cambiamento porta alla forma differenziale usata nel calcolo stocastico, in cui il termine di rumore appare come un incremento casuale con varianza proporzionale a $dt$. L’equazione diventa così

$$
dx = a(x,t)\,dt + b(x,t)\,dW(t) ,
$$

dove $dW(t)$ rappresenta un incremento infinitesimo di un processo con media nulla e varianza $dt$. Il vantaggio di questa riscrittura è che gli incrementi $dW(t)$ hanno una definizione precisa e permettono di sviluppare un calcolo coerente, a partire dalle relazioni fondamentali

$$
\langle dW(t) \rangle = 0 , \qquad \langle dW(t)^2 \rangle = dt .
$$

Queste proprietà mostrano che $dW(t)$ è dell’ordine di $\sqrt{dt}$ e che il suo quadrato non è trascurabile, a differenza del calcolo ordinario in cui si assume $dt^2 = 0$.

Su queste basi nasce il calcolo di Ito, che definisce in modo rigoroso le regole per trattare i differenziali stocastici. Per una funzione sufficientemente regolare $f(x,t)$ si ottiene la formula di Ito

$$
df = \frac{\partial f}{\partial t}\,dt + \frac{\partial f}{\partial x}\,dx + \frac12\,\frac{\partial^2 f}{\partial x^2}\,b(x,t)^2\,dt ,
$$

che evidenzia il termine correttivo aggiuntivo, assente nel calcolo classico e dovuto al contributo di ordine $dW(t)^2 = dt$.

Accanto a questa interpretazione esiste anche quella di Stratonovich, indicata con

$$
dx = a_S(x,t)\,dt + b(x,t)\circ dW(t),
$$

più vicina alle regole del calcolo ordinario e spesso utilizzata quando il rumore deriva dal limite di segnali fisici con correlazione molto breve ma non nulla. Nel seguito adotteremo l’interpretazione di Ito, che è lo standard nella teoria matematica delle SDE e costituisce la base dei metodi di simulazione numerica come l’algoritmo di Euler–Maruyama.

---

## 4. Simulazioni numeriche di traiettorie: lo schema di Euler–Maruyama

Una volta introdotta l’equazione stocastica

$$
dx = a(x,t)\,dt + b(x,t)\,dW(t),
$$

il passo successivo è capire come approssimarla numericamente. L’idea di base è la stessa del metodo di Eulero per le ODE: suddividere l’intervallo temporale in passi di ampiezza $\Delta t$ e approssimare gli incrementi infinitesimi con valori discreti.

Nel caso stocastico, l’incremento del processo di Wiener su un passo di ampiezza $\Delta t$ è distribuito come una variabile gaussiana con media nulla e varianza $\Delta t$, cioè

$$
\Delta W_n \sim \mathcal{N}(0,\Delta t).
$$

Lo schema di Euler–Maruyama approssima la dinamica stocastica sostituendo $dW(t)$ con $\Delta W_n$ e valutando i coefficienti nel punto noto $x_n$. Si ottiene così la ricorrenza discreta

$$
x_{n+1}
= x_n
+ a(x_n,t_n)\,\Delta t
+ b(x_n,t_n)\,\Delta W_n .
$$

Se si scrive $\Delta W_n = \sqrt{\Delta t}\,\xi_n$ con $\xi_n \sim \mathcal{N}(0,1)$, la formula assume la forma più comune

$$
x_{n+1}
= x_n
+ a(x_n,t_n)\,\Delta t
+ b(x_n,t_n)\,\sqrt{\Delta t}\,\xi_n .
$$

Questo schema è l’analogo diretto del metodo di Eulero esplicito per le equazioni deterministiche, con l’aggiunta del termine stocastico che produce fluttuazioni passo per passo. Ogni realizzazione della sequenza $\xi_n$ genera una traiettoria diversa, ma l’insieme di tali traiettorie riproduce la dinamica media descritta dall’equazione di partenza.

### Esempio in Python

Il codice seguente simula una SDE unidimensionale con drift $f(x)$ e intensità del rumore costante $\sigma$:

```python
import numpy as np
import matplotlib.pyplot as plt

def langevin(f, sigma, x0, dt, N):
    x = np.zeros(N)
    x[0] = x0
    for n in range(N-1):
        dW = np.sqrt(dt) * np.random.randn()
        x[n+1] = x[n] + f(x[n]) * dt + sigma * dW
    return x

# esempio: processo con drift negativo
f = lambda x: -0.5 * x
x = langevin(f, sigma=0.3, x0=1.0, dt=0.01, N=1000)

plt.plot(x)
plt.xlabel("passo temporale")
plt.ylabel("x")
plt.show()
```

Il risultato è una singola traiettoria generata dal rumore. Ripetendo la simulazione più volte si ottengono percorsi diversi, ma il comportamento medio riflette la dinamica della SDE da cui il modello è stato costruito.

### 4.1 Considerazioni sulla stabilità numerica

Lo schema di Euler–Maruyama è semplice da implementare, ma la sua stabilità non è garantita per qualunque scelta del passo $\Delta t$. A differenza del caso deterministico, infatti, la presenza del rumore modifica profondamente la risposta numerica del sistema.

Per fissare le idee, consideriamo la SDE lineare

$$
dx = -\lambda x\,dt + \sigma\,dW(t),
$$

che rappresenta il processo di Ornstein–Uhlenbeck. La soluzione esatta è stabile per qualunque $\lambda > 0$, ma la discretizzazione Euler–Maruyama è stabile solo se

$$
1 - \lambda\,\Delta t \quad \text{rimane in un intervallo compatibile con la dinamica stocastica}.
$$

In pratica, se $\Delta t$ è troppo grande, lo schema può produrre divergenze numeriche anche quando il modello continuo è perfettamente stabile.

La scelta del passo $\Delta t$ è quindi cruciale e dipende da diversi fattori:

1. **Stabilità del drift**. Processi con forze restauratrici molto intense richiedono passi più piccoli per evitare instabilità del termine $a(x,t)\,\Delta t$.

2. **Intensità del rumore**. Il termine $b(x,t)\,\sqrt{\Delta t}\,\xi_n$ introduce fluttuazioni proporzionali a $\sqrt{\Delta t}$; un passo troppo grande amplifica artificialmente le oscillazioni.

3. **Regione dello spazio degli stati**. In molte SDE (per esempio popolazioni o concentrazioni chimiche), valori negativi delle variabili non sono fisicamente significativi; Euler–Maruyama può violare la positività e richiedere varianti “positive”.

4. **Errore forte ed errore debole**. Lo schema è di ordine
   
   - $1/2$ in senso forte (accuratezza sulle traiettorie individuali),
   - $1$ in senso debole (accuratezza sulle medie e distribuzioni).
     Questo implica che, per ricostruire una singola traiettoria con buona risoluzione, occorrono passi più piccoli rispetto a quelli necessari per stime statistiche aggregate.

5. **Sensibilità ai coefficienti non regolari**. Se $a(x,t)$ o $b(x,t)$ sono molto ripidi o non lisci, il metodo può richiedere passi notevolmente più piccoli rispetto ai casi più regolari.

In sintesi, Euler–Maruyama è efficace e versatile, ma va utilizzato con attenzione. La stabilità dipende sia dal drift sia dall’intensità del rumore, e la scelta del passo temporale influenza direttamente la correttezza sia delle traiettorie sia delle distribuzioni simulate. Nelle sezioni successive verranno discussi metodi più robusti e criteri operativi per la scelta dei parametri numerici.

---

## 5. Esempi interdisciplinari

Le equazioni stocastiche costituiscono un linguaggio comune per descrivere sistemi nei quali una tendenza media è accompagnata da fluttuazioni non prevedibili nel dettaglio. Ogni disciplina introduce termini con significato specifico, ma la struttura concettuale rimane invariata: un drift che rappresenta la dinamica sistematica e un termine di rumore che sintetizza l’effetto di molte influenze piccole, rapide e irregolari.

### 5.1 Fisica: oscillatore armonico con rumore (e un primo esempio vettoriale)

Un modello semplice e molto utilizzato in fisica statistica è l’oscillatore armonico immerso in un ambiente termico. La variabile di stato è composta da posizione $x(t)$ e velocità $v(t)$, che evolvono secondo

$$
dx = v\,dt, \qquad
dv = -\gamma\,v\,dt - k\,x\,dt + \sigma\,dW(t).
$$

Il termine $-k\,x$ rappresenta la forza elastica che tende a riportare l’oscillatore verso la posizione di equilibrio, mentre il termine $-\gamma\,v$ descrive l’azione dissipativa dell’ambiente, che smorza il movimento nel tempo. Il rumore $\sigma\,dW(t)$ introduce le fluttuazioni termiche dovute all’interazione con le molecole del mezzo circostante.

In questo modello il rumore agisce solo sulla velocità. Questa scelta riflette il fatto che, nelle scale fisiche in cui l’oscillatore è studiato (ad esempio un colloide in sospensione o un oscillatore meccanico microscopico), sono gli urti dell’ambiente a modificare direttamente la velocità, mentre la posizione viene influenzata in modo indiretto tramite la dinamica deterministica. In altri sistemi, o a scale diverse, il rumore potrebbe invece agire anche o solo sulla posizione.

Questa SDE può essere riscritta in forma compatta come equazione vettoriale. Definiamo

$$
X(t) = 
\begin{pmatrix}
x(t) \\
v(t)
\end{pmatrix}.
$$

Allora l’oscillatore armonico stocastico si scrive come

$$
dX = A\,X\,dt + B\,dW(t),
$$

dove

$$
A =
\begin{pmatrix}
0 & 1 \\
-k & -\gamma
\end{pmatrix},
\qquad
B =
\begin{pmatrix}
0 \\
\sigma
\end{pmatrix}.
$$

Questa notazione evidenzia due aspetti importanti:

1. **Struttura deterministica lineare.**  
   La matrice $A$ governa il comportamento medio del sistema, combinando oscillazione elastica e smorzamento.

2. **Rumore che agisce su una sola componente.**  
   La matrice $B$ mostra che la sorgente stocastica interviene direttamente solo sulla velocità $v(t)$, mentre la posizione $x(t)$ risente del rumore solo in modo indiretto, attraverso l’accoppiamento deterministico con la velocità.

La forma matriciale è utile perché generalizza immediatamente a sistemi con molte variabili, tipici della fisica dei sistemi complessi (dinamica molecolare lineare, reti lineari di oscillatori, modelli di vibrazioni, metodi di riduzione dimensionale). Inoltre facilita la connessione con la teoria dei processi gaussiani e dei sistemi lineari stocastici, permettendo analisi spettrali e soluzioni esplicite in termini di matrici di propagatore.

### 5.2 Chimica: dinamica attivata in un potenziale a doppio pozzo

Molte reazioni chimiche e processi molecolari sono descritti come transizioni fra stati metastabili separati da una barriera energetica. Un modello prototipico considera un potenziale a doppio pozzo

$$
U(x) = \frac{1}{4}x^4 - \frac{1}{2}x^2,
$$

con due minimi stabili in $x = \pm 1$. La dinamica sovra-smorzata di un reagente o di una coordinata molecolare è modellata dalla Langevin sovra-smorzata

$$
dx = -\nabla U(x)\,dt + \sigma\,dW(t),
$$

ossia

$$
dx = -(x^3 - x)\,dt + \sigma\,dW(t).
$$

Il termine $-U'(x)$ tende a mantenere il sistema in uno dei pozzi (stati metastabili), mentre $\sigma\,dW(t)$ rappresenta le fluttuazioni termiche che permettono, occasionalmente, di superare la barriera. Questo meccanismo è alla base del modello di Kramers per la **cinematica delle reazioni attivate**, e descrive fenomeni quali:

- la transizione tra conformazioni molecolari,
- lo scatto fra stati chimici in reazioni bistabili,
- la dinamica di attivazione termica in complessi instabili,
- la stabilità termica di stati attivati in chimica fisica.

In questo contesto il rumore fornisce l’energia necessaria per attraversare la barriera, mentre la parte deterministica del modello descrive il ritorno verso uno dei minimi.

### 5.2 Biologia: espressione genica e dinamiche cellulari

Nei processi cellulari la produzione di proteine avviene in modo discontinuo e soggetto a variabilità intrinseca. Un modello semplice per la concentrazione $x(t)$ di una proteina può assumere la forma

$$
dx = \bigl(\alpha - \beta x\bigr)\,dt + \sigma\,dW(t),
$$

dove $\alpha$ è il tasso medio di produzione, $\beta x$ il tasso medio di degradazione e il termine stocastico rappresenta le fluttuazioni dovute al numero discreto di eventi di trascrizione e traduzione. Tali modelli descrivono bene l’ampia variabilità misurata in cellule geneticamente identiche.

### 5.3 Economia e finanza: moto geometrico browniano

Nei mercati finanziari si modellano spesso i prezzi come grandezze che crescono in media ma sono soggette a shock improvvisi. Il modello classico per il prezzo $S_t$ di un attivo rischioso è il moto geometrico browniano

$$
dS_t = \mu\,S_t\,dt + \sigma\,S_t\,dW(t),
$$

in cui $\mu$ rappresenta il tasso di crescita medio (drift) e $\sigma S_t dW(t)$ la componente di volatilità che amplifica il rumore in proporzione al livello del prezzo. Questo modello costituisce la base di molte equazioni di valutazione in finanza quantitativa.

### 5.4 Ecologia: popolazioni e dinamiche ambientali

Le popolazioni biologiche sono soggette a variabilità ambientale e demografica. Un modello stocastico per la popolazione $x(t)$ può essere

$$
dx = r\,x\,(1 - x/K)\,dt + \sigma\,x\,dW(t),
$$

dove $r$ è il tasso di crescita, $K$ la capacità portante dell’ambiente e $\sigma x dW(t)$ rappresenta fluttuazioni proporzionali alla dimensione della popolazione, ad esempio dovute a condizioni ambientali imprevedibili. Il rumore moltiplicativo cattura l’idea che le oscillazioni siano più intense nelle popolazioni numerose.

### 5.5 Ingegneria: sistemi con rumore di misura e attuatori imperfetti

Nei sistemi di controllo ingegneristici le SDE descrivono l’evoluzione di segnali affetti da rumore sensoristico o da imperfezioni nella risposta degli attuatori. Un modello tipico per la dinamica di uno stato $x(t)$ è

$$
dx = f(x,t)\,dt + G(x,t)\,dW(t),
$$

dove $f(x,t)$ rappresenta la dinamica deterministica del sistema (ad esempio un modello meccanico o elettrico) e $G(x,t)dW(t)$ sintetizza il rumore di misura, le vibrazioni o l’incertezza sulle forze applicate. Questo formalismo è alla base dei filtri di stima come il filtro di Kalman esteso o il filtro di Kalman stocastico.

### 5.6 Scienze sociali e reti: diffusione dell’informazione e scelte individuali

Nei sistemi sociali le decisioni individuali variano nel tempo a causa di stimoli esterni, incertezza, imitazione o esposizione casuale all’informazione. Un modello continuo della propensione $x(t)$ di un individuo a compiere una certa scelta può essere

$$
dx = \bigl(-\gamma x + F(t)\bigr)\,dt + \sigma\,dW(t),
$$

dove $F(t)$ rappresenta l’influenza sociale o informativa (notizie, contatti, opinioni del vicinato) e il termine stocastico descrive la variabilità imprevedibile del comportamento. Nei modelli di diffusione su reti, gli agenti possono essere trattati come particelle che si muovono in modo casuale su un grafo, propagando informazione in modo analogo ai processi diffusivi.

---

Questi esempi mostrano come la stessa struttura matematica possa descrivere fenomeni molto diversi, fornendo un linguaggio unificato per lo studio di sistemi complessi in cui la componente stocastica non è un semplice disturbo, ma una parte fondamentale della dinamica.

---

## Riferimenti

* Langevin, P. (1908). *Sur la théorie du mouvement brownien*. C. R. Acad. Sci. 146: 530–533.
* Gardiner, C. (2004). *Handbook of Stochastic Methods*. Springer.
* Risken, H. (1989). *The Fokker–Planck Equation*. Springer.
* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review, 43(3): 525–546.
* Gillespie, D. T. (2000). *The chemical Langevin equation*. J. Chem. Phys. 113(1): 297–306.

---

### Appendice: il formalismo di Leibniz e la formula di Ito

Prima di introdurre il calcolo stocastico, è utile ricordare come funziona il formalismo di Leibniz nelle equazioni differenziali ordinarie. Consideriamo una semplice ODE

$$
\frac{dx}{dt} = a(x,t).
$$

Scritta “alla Leibniz”, questa relazione diventa

$$
dx = a(x,t)\,dt,
$$

che può essere manipolata come un differenziale ordinario. Ad esempio, per una funzione abbastanza regolare $f(x,t)$, l’espansione di Taylor fornisce

$$
df = \frac{\partial f}{\partial t}\,dt
     + \frac{\partial f}{\partial x}\,dx,
$$

e sostituendo $dx = a(x,t)\,dt$ si ottiene

$$
df = \left(
       \frac{\partial f}{\partial t}
       + a(x,t)\,\frac{\partial f}{\partial x}
     \right) dt .
$$

In una ODE classica, i termini quadratici negli infinitesimi vengono sempre trascurati, poiché si assume che

$$
dt^2 = 0.
$$

Questo è il punto in cui la situazione cambia nel caso stocastico: quando compaiono incrementi irregolari come quelli associati al rumore, un termine come $(dx)^2$ non è più trascurabile.

---

Consideriamo ora un’equazione differenziale stocastica in forma di Ito

$$
dx = a(x,t)\,dt + b(x,t)\,dW(t),
$$

dove $W(t)$ è un processo con incrementi a media nulla e varianza $dt$, cioè

$$
\langle dW(t) \rangle = 0, \qquad \langle dW(t)^2 \rangle = dt.
$$

Nel formalismo di Leibniz si usa l’idea che $dx$ sia un differenziale infinitesimo, ma nel caso stocastico è necessario specificare anche come si comportano i prodotti di questi infinitesimi. Le regole fondamentali sono:

1. $dt^2 = 0$ (come nel calcolo ordinario),
2. $dt\,dW(t) = 0$,
3. $dW(t)^2 = dt$ (novità essenziale).

L’ultima regola incorpora il fatto che la varianza dell’incremento $dW(t)$ è proporzionale a $dt$.

Prendiamo ora una funzione sufficientemente regolare $f(x,t)$ e sviluppiamola al primo ordine in $dt$ usando un’espansione di Taylor:

$$
df = f(x+dx,t+dt) - f(x,t).
$$

L’espansione di Taylor, fino ai termini d’ordine non superiore a $dt$, dà

$$
df = \frac{\partial f}{\partial t}\,dt
     + \frac{\partial f}{\partial x}\,dx
     + \frac12\,\frac{\partial^2 f}{\partial x^2}\,(dx)^2
     + \text{termini di ordine superiore}.
$$

Nel calcolo ordinario si scarterebbero i termini contenenti $(dx)^2$, ma qui $dx$ contiene un contributo di ordine $\sqrt{dt}$, quindi $(dx)^2$ è dell’ordine di $dt$ e non può essere trascurato.

Da $dx = a(x,t)\,dt + b(x,t)\,dW(t)$ otteniamo

$$
(dx)^2 =
a(x,t)^2\,dt^2
+ 2\,a(x,t)\,b(x,t)\,dt\,dW(t)
+ b(x,t)^2\,dW(t)^2 .
$$

Applicando le regole sugli infinitesimi,

- $dt^2 = 0$,
- $dt\,dW(t) = 0$,
- $dW(t)^2 = dt$,

si ricava

$$
(dx)^2 = b(x,t)^2\,dt.
$$

Inserendo questa espressione nell’espansione di $df$ si ottiene finalmente la formula di Ito:

$$
df =
\frac{\partial f}{\partial t}\,dt
+ \frac{\partial f}{\partial x}\,dx
+ \frac12\,\frac{\partial^2 f}{\partial x^2}\,b(x,t)^2\,dt .
$$

Sostituendo anche $dx = a(x,t)\,dt + b(x,t)\,dW(t)$ si arriva alla forma completa

$$
df =
\left(
\frac{\partial f}{\partial t}
+ a(x,t)\,\frac{\partial f}{\partial x}
+ \frac12\,b(x,t)^2\,\frac{\partial^2 f}{\partial x^2}
\right) dt
+ b(x,t)\,\frac{\partial f}{\partial x}\,dW(t).
$$

che mostra esplicitamente sia il contributo deterministico (proporzionale a $dt$) sia il contributo stocastico (proporzionale a $dW(t)$).

### Appendice: differenza tra errore forte ed errore debole

Nelle equazioni deterministiche l’errore numerico è definito in modo univoco, ma nelle SDE esistono due nozioni diverse di accuratezza:

- **Errore forte (strong error)**: misura quanto bene il metodo approssima *una singola traiettoria*. Formalmente richiede che la distanza media tra la soluzione esatta e quella numerica, *<u>nello stesso scenario di rumore</u>*, sia piccola. Lo schema di Euler–Maruyama ha ordine $1/2$ in questo senso: l’errore tipico scala come $\Delta t^{1/2}$. Questo significa che per dimezzare l’errore richiede di dividere il passo per un fattore 4 (e quindi moltiplicare per quattro la lunghezza della simulazione).

- **Errore debole (weak error)**: misura quanto bene il metodo approssima *le quantità statistiche*, ad esempio medie, varianze, o distribuzioni della soluzione. Non richiede che la singola traiettoria sia accurata, ma solo che la simulazione collettiva riproduca le aspettative corrette. In questo senso Euler–Maruyama è di ordine $1$: l’errore sulle medie scala come $\Delta t$.

Questa distinzione è cruciale nell’uso pratico. Se l’obiettivo è studiare l’evoluzione media o stimare grandezze aggregate tramite molte simulazioni indipendenti, si può usare un passo $\Delta t$ relativamente più grande, perché l’errore debole diminuisce rapidamente. Se invece interessa seguire nel dettaglio una singola traiettoria (ad esempio in modelli di apprendimento online o in dinamiche di controllo), occorre scegliere un passo molto più piccolo per compensare l’ordine $1/2$ dell’errore forte. 

Per illustrare la distinzione, consideriamo la SDE lineare

$$
dx = -\lambda x\,dt + \sigma\,dW(t),
$$

nota come processo di Ornstein–Uhlenbeck. La soluzione esatta è nota, il che rende semplice confrontare la simulazione numerica con il comportamento reale.

**Errore forte (traiettoria individuale).**  
Per confrontare due simulazioni con passi diversi, ad esempio $\Delta t = 10^{-3}$ e $\Delta t = 10^{-2}$, è fondamentale utilizzare la **stessa realizzazione del rumore**. Ciò significa che gli incrementi più grandi devono essere costruiti come somma dei più piccoli. Se indichiamo con $\Delta W_n$ gli incrementi generati con passo $\Delta t$, allora per il passo dieci volte più grande si impone

$$
\Delta W^{(10\Delta t)}_k
= \sum_{j=1}^{10} \Delta W^{(\Delta t)}_{10k+j}.
$$

In questo modo entrambe le simulazioni vedono esattamente lo stesso rumore, solo campionato con granularità diversa.

Anche in queste condizioni:

- le due traiettorie **non coincidono**,
- la simulazione con $\Delta t$ più grande presenta oscillazioni artificiali,
- riducendo $\Delta t$ la convergenza è lenta, poiché l’errore forte scala come $\Delta t^{1/2}$.

Questo riflette il fatto che, per approssimare accuratamente una singola traiettoria, è necessario scegliere un passo temporale molto piccolo.

In altre parole, la traiettoria numerica approssima bene quella esatta solo se il passo è molto piccolo. Questo è tipico delle simulazioni in cui interessa seguire la dinamica dettagliata di un singolo percorso.

**Errore debole (statistiche di molte traiettorie).**  
Ora generiamo molte simulazioni indipendenti e calcoliamo, a ogni istante, la media empirica delle soluzioni. Per una SDE come quella sopra, la media esatta soddisfa l’ODE

$$
\frac{d}{dt}\,\mathbb{E}[x(t)] = -\lambda\,\mathbb{E}[x(t)],
$$

quindi ha andamento puramente deterministico. Se confrontiamo la media numerica ottenuta con passi diversi, osserviamo che:

- anche con passi relativamente grandi, ad esempio $\Delta t = 10^{-2}$ o $\Delta t = 5\cdot 10^{-2}$,  
  **la media simulata coincide quasi perfettamente con quella teorica**;

- aumentando il numero di traiettorie la convergenza migliora rapidamente;

- l’errore sulla media scala come $\Delta t$, quindi si riduce molto più velocemente rispetto all’errore forte.

In sintesi:

- **errore forte**: convergenza lenta, richiede piccoli passi, importante se si vogliono traiettorie individuali accurate;
- **errore debole**: convergenza veloce, permette passi più grandi, importante quando si studiano medie, varianze e distribuzioni.

Questo esempio chiarisce perché, nelle simulazioni Monte Carlo per SDE, la scelta del passo temporale dipende strettamente dal tipo di osservabile che si vuole stimare.
