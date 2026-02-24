---
title: "01: Struttura deterministica dei sistemi stocastici"
author: "Antonio Scala"
date: "24 Feb 2026"
---

In molti modelli stocastici, la componente casuale si innesta su una struttura deterministica di base.  
Questa lezione fissa quella struttura: equilibri, stabilità, biforcazioni e (soprattutto) il fatto che ogni simulazione numerica continua è, in realtà, una dinamica discreta che approssima un flusso continuo.

L'obiettivo non è fare un corso completo di ODE, ma introdurre un linguaggio minimo e robusto, che verrà riutilizzato in modo sistematico quando aggiungeremo rumore diffuso, salti, metastabilità e dinamiche di escape.

### Obiettivi didattici specifici

Al termine, lo studente dovrà essere in grado di:

1. riconoscere e analizzare un sistema autonomo 1D $\dot x = f(x)$ tramite equilibri e stabilità locale;
2. interpretare dinamiche come discesa su un paesaggio di potenziale, collegando minimi, massimi e barriere a attrattori e separatrici;
3. descrivere biforcazioni elementari (transcritica e saddle--node) e il loro significato come soglie critiche e tipping;
4. costruire una discretizzazione temporale e il metodo di Eulero esplicito;
5. distinguere errore locale ed errore globale, e separare stabilità del modello da stabilità dello schema numerico;
6. collegare ODE e sistemi discreti come due facce della stessa pratica computazionale.

### Struttura della lezione

- **Parte I**: struttura qualitativa delle ODE 1D (equilibri, paesaggi, biforcazioni).  
- **Parte II**: integrazione numerica (discretizzazione, Eulero, errori e stabilità).  
- **Appendice**: dinamiche discrete e mappa concettuale ODE $\leftrightarrow$ sistemi discreti.

---

# PARTE I -- Struttura deterministica

## 1. Sistemi autonomi unidimensionali

**Obiettivo della sezione**  
Introdurre il concetto di dinamica deterministica continua nel caso più semplice, chiarendo:
* definizione di sistema autonomo 1D
* punti di equilibrio
* criterio locale di stabilità
* interpretazione geometrica tramite campo di direzioni

### 1.1 Sistema autonomo 1D e traiettorie

Un sistema autonomo unidimensionale è un'equazione del tipo
$$
\dot x = f(x),
$$
dove $x(t)$ è una variabile reale (stato del sistema) e $f$ è un campo di velocità che dipende solo da $x$ (non esplicitamente dal tempo).

Interpretazione geometrica: in ogni punto $x$ la funzione $f(x)$ dice se la traiettoria tende a crescere ($f(x)>0$) o decrescere ($f(x)<0$).  
In 1D la dinamica si legge spesso più facilmente con un diagramma su asse reale ("linea di fase") che con una soluzione analitica.

### 1.2 Equilibri e stabilità locale

Un punto $x^*$ è un equilibrio se
$$
f(x^*)=0.
$$

Per la stabilità locale si linearizza attorno a $x^*$:
$$
x(t) = x^* + \xi(t), \qquad |\xi|\ \text{piccolo}.
$$
Allora
$$
\dot \xi \approx f'(x^*)\,\xi.
$$

- Se $f'(x^*)<0$, le perturbazioni decadono: $x^*$ è **stabile** (attrattore).  
- Se $f'(x^*)>0$, le perturbazioni crescono: $x^*$ è **instabile** (repulsore).  
- Se $f'(x^*)=0$, il test lineare non basta: serve un'analisi non lineare (qui non approfondiamo).

**Rappresentazione su asse reale**  
Per ogni intervallo tra due zeri di $f$, si segna una freccia a destra se $f>0$ e a sinistra se $f<0$.  
Uno zero con frecce entranti è attrattore; uno zero con frecce uscenti è repulsore.

Esercizio rapido (mentale): scegli $f(x)=x(1-x)$. Trova gli equilibri e la stabilità con $f'(x^*)$.

---

## 2. Dinamica di gradiente e paesaggi

**Obiettivo della sezione**  
Mostrare che molte dinamiche possono essere interpretate come discesa lungo un paesaggio di potenziale:
$$
\dot x = -V'(x)
$$

### 2.1 Potenziale e monotonia di $V$

### 2. Dinamica di gradiente e paesaggi

Perché introdurre i sistemi di gradiente in un corso su modelli stocastici?  
Per due ragioni operative.

1) **Molti modelli deterministici usati in applicazioni sono (o possono essere approssimati come) dinamiche che “scendono” lungo una funzione di energia/potenziale** (o che "salgono" lungo una funzione di **utilità/fitness**): questo rende immediato interpretare attrattori, barriere e bacini.  
2) **Quando aggiungeremo rumore**, la metafora del paesaggio diventa uno strumento quantitativo: la stabilità locale corrisponde a un minimo, una transizione tra stati a uno “scavalcamento” di barriera, e la metastabilità si legge come permanenza prolungata in una valle.

Detto questo, consideriamo ora una dinamica di gradiente nella forma standard:
$$
\dot x = -V'(x).
$$
Per una dinamica di gradiente in questa forma standard, lungo una traiettoria $x(t)$ vale
$$
\frac{d}{dt}V(x(t)) = V'(x(t))\,\dot x(t) = -\bigl(V'(x(t))\bigr)^2 \le 0.
$$

Quindi $V$ è una quantità che non aumenta nel tempo: la traiettoria scende verso valori più bassi del potenziale.

### 2.2 Minimi, massimi, barriere

Gli equilibri soddisfano $V'(x^*)=0$.

- Se $x^*$ è un **minimo locale** di $V$, allora è un attrattore (stabile).  
- Se $x^*$ è un **massimo locale** di $V$, allora è repulsore (instabile).  
- I massimi separano bacini di attrazione: sono barriere tra "valli" diverse.

Questa immagine è un ponte naturale verso la dinamica stocastica:
- con rumore diffuso, una traiettoria può "scavalcare" una barriera con una probabilità che dipende dall'intensità del rumore;
- con rumore impulsivo, un singolo salto può attraversare la barriera.

Nota utile in 1D: per molte ODE $\dot x = f(x)$ si può definire formalmente un potenziale
$$
V(x) = -\int^x f(u)\,du,
$$
così che $\dot x = -V'(x)$. Questo non implica che ogni modello sia "fisicamente" un gradiente, ma rende l'intuizione del paesaggio molto generale in 1D.

---

## 3. Biforcazione transcritica

**Obiettivo della sezione**  
Introdurre l’idea di cambiamento qualitativo della dinamica al variare di un parametro.

Modello guida:
$$
\dot N = rN - N^2
$$

che ha un collegamento diretto con:

* modelli di crescita
* branching
* soglia di sopravvivenza

### 3.1 Equilibri

Scriviamo
$$
\dot N = rN - N^2 = N(r-N).
$$
Gli equilibri sono:
$$
N^*_1 = 0, \qquad N^*_2 = r.
$$

### 3.2 Stabilità e scambio a $r=0$

La funzione è $f(N)=rN-N^2$, quindi
$$
f'(N)=r-2N.
$$

- In $N^*_1=0$:
  $$
  f'(0)=r.
  $$
  Quindi $N=0$ è stabile se $r<0$ e instabile se $r>0$.

- In $N^*_2=r$:
  $$
  f'(r)=r-2r=-r.
  $$
  Quindi $N=r$ è stabile se $r>0$ e instabile se $r<0$.

A $r=0$ avviene uno **scambio di stabilità** tra i due equilibri: questa è l'essenza della **biforcazione transcritica**.

Interpretazione: $r=0$ è una soglia.  
In molti modelli (crescita, epidemie, branching) una soglia separa regime di estinzione e regime di persistenza: qui lo si vede in forma deterministica e locale, tramite stabilità degli equilibri.

Esercizio rapido: disegna la linea di fase per $r<0$, $r=0$, $r>0$.

---

## 4. Biforcazione saddle--node e tipping

**Obiettivo della sezione**  
Mostrare come possano emergere e scomparire equilibri al variare di un parametro.

Modello guida:
$$
\dot x = r + x^2
$$


### 4.1 Esistenza degli equilibri

Gli equilibri soddisfano
$$
r + (x^*)^2 = 0 \quad \Rightarrow \quad (x^*)^2 = -r.
$$

- Se $r<0$, esistono due equilibri:
  $$
  x^*_\pm = \pm \sqrt{-r}.
  $$
- Se $r=0$, esiste un equilibrio doppio:
  $$
  x^*=0.
  $$
- Se $r>0$, non esistono equilibri reali.

### 4.2 Stabilità e collisione

Qui $f(x)=r+x^2$ e
$$
f'(x)=2x.
$$

Per $r<0$:

- in $x^*_-=-\sqrt{-r}$:
  $$
  f'(x^*_-)= -2\sqrt{-r} < 0,
  $$
  quindi è **stabile**;

- in $x^*_+=+\sqrt{-r}$:
  $$
  f'(x^*_+)= +2\sqrt{-r} > 0,
  $$
  quindi è **instabile**.

Quando $r$ cresce verso $0$ i due equilibri si avvicinano, collidono in $x=0$ e scompaiono per $r>0$: questa è la **biforcazione saddle--node**.

### 4.3 Tipping: significato qualitativo

Se il sistema era vicino all'equilibrio stabile (per $r<0$), l'aumento di $r$ può portare a una perdita improvvisa di equilibrio.  
Dopo la "collisione", non esiste più uno stato di riposo che trattenga la dinamica: la traiettoria è costretta a muoversi in modo qualitativamente diverso.

Questa è una forma elementare di **tipping deterministico**.  
Nella parte stocastica, l'idea si rafforza: anche prima della soglia deterministica, rumore diffuso o rumore impulsivo possono indurre la transizione tra bacini o l'uscita oltre una barriera.

Esercizio rapido: per $r<0$ disegna linea di fase e identifica il punto stabile e quello instabile.

---

# PARTE II -- Integrazione numerica delle ODE

## 5. Discretizzazione temporale

**Obiettivo della sezione**  
Passare dalla dinamica continua alla dinamica numerica.

### 5.1 Dal tempo continuo al tempo discreto

Un'equazione differenziale definisce una dinamica in tempo continuo, ma un computer può aggiornare lo stato solo a tempi discreti.

Si introduce una griglia temporale:
$$
t_n = t_0 + n\Delta t, \qquad n=0,1,2,\dots
$$
e si approssima $x(t_n)$ con una sequenza $x_n$.

Messaggio chiave: quando "simuliamo una ODE" stiamo in realtà simulando un sistema discreto che, nel limite $\Delta t \to 0$, approssima il flusso continuo.

---

## 6. Metodo di Eulero esplicito

**Obiettivo della sezione**  
Costruire il primo schema numerico:
$$
x_{n+1} = x_n + f(x_n)\Delta t
$$


### 6.1 Derivazione (sviluppo al primo ordine)

Per definizione
$$
\dot x(t_n) = \lim_{\Delta t\to 0}\frac{x(t_n+\Delta t)-x(t_n)}{\Delta t}.
$$
Sostituendo il limite con un'approssimazione a passo finito:
$$
\frac{x_{n+1}-x_n}{\Delta t} \approx f(x_n)
\quad \Rightarrow \quad
x_{n+1} = x_n + f(x_n)\Delta t.
$$

Questo è lo schema di Eulero esplicito.

### 6.2 Interpretazione geometrica

Lo schema usa la pendenza $f(x_n)$ nel punto corrente per costruire un passo lungo la tangente.  
È un metodo locale: "vede" solo la derivata in $x_n$.

### 6.3 Stabilità numerica: equazione test lineare

Per capire perché $\Delta t$ conta, consideriamo l'ODE:
$$
\dot x = \lambda x, \qquad \lambda \in \mathbb{R}.
$$
che ha come soluzione $x(t)=\exp(\lambda t)$ che diverge o decade a zero a seconda che $\lambda$  sia positivo o negativo. 

Per una condizione iniziale $x_0$, abbiamo la soluzione approssimata della nostra ODE a tempi discreti $t=n\Delta t$. Con Eulero:
$$
x_{n+1} = x_n + \lambda x_n \Delta t = (1+\lambda\Delta t)x_n.
$$
ovvero $x_{n} = (1+\lambda \frac{t}{n})^n$ che, per $\Delta t \to 0$ i.e. $n \to \infty$  converge a $\exp(\lambda t)$. 

Se $\lambda<0$ la soluzione continua decade. Perché anche la simulazione decada, serve:
$$
|1+\lambda \Delta t| < 1
\quad \Rightarrow \quad
0 < \Delta t < \frac{2}{|\lambda|}.
$$
Per $\Delta t$ troppo grandi, il sistema quindi non solo diverge al passo $n$-esimo come
 $|1+\lambda \Delta t|^n$, ma cambia anche di segno ($(1+\lambda \Delta t)^n$ è postivo/negativo per $n$ pari/dispari). Quindi anche un sistema deterministico stabile può essere reso instabile da una scelta troppo grande di $\Delta t$.

---

## 7. Errori numerici e stabilità

**Obiettivo della sezione**

* Definire errore locale
* Definire errore globale
* Mostrare che l’errore dipende da $\Delta t$
* Distinguere tra stabilità del modello e stabilità dello schema

### 7.1 Errore locale e errore globale

- **Errore locale di troncamento**: l'errore commesso in un singolo passo assumendo di partire dal valore esatto $x(t_n)$.  
  Per Eulero, usando lo sviluppo di Taylor, è tipicamente dell'ordine
  $$
  O(\Delta t^2).
  $$

- **Errore globale**: l'errore accumulato dopo molti passi fino a un tempo fissato $T$.  
  Per Eulero, in condizioni regolari, è tipicamente
  $$
  O(\Delta t).
  $$

Idea essenziale: ridurre $\Delta t$ riduce l'errore, ma aumenta il costo computazionale e può introdurre problemi pratici (tempo di esecuzione, accumulo di arrotondamenti).

### 7.2 Stabilità del modello vs stabilità dello schema

- **Stabilità del modello (dinamica)**: riguarda proprietà intrinseche della ODE (attrattori, equilibri, bacini).  
- **Stabilità dello schema (numerica)**: riguarda la capacità dell'algoritmo di non amplificare errori e di riprodurre correttamente la dinamica per $\Delta t$ finito.

Esempio concettuale:
- un equilibrio può essere stabile per la ODE,
- ma la discretizzazione con Eulero può generare oscillazioni spurie o divergenza se $\Delta t$ è troppo grande.

### 7.3 Implicazione operativa: test di convergenza

Una buona pratica computazionale è verificare empiricamente la convergenza:
- simulare con $\Delta t$ e con $\Delta t/2$;
- controllare che traiettorie e osservabili (ad esempio valore finale, tempi di primo passaggio, medie su insiemi) non cambino in modo significativo.

Questo criterio tornerà identico nelle SDE e nei processi di salto: cambia l'oggetto, ma resta la logica.

---

# APPENDICE -- Sistemi discreti

## A1. Equazioni alle differenze

**Obiettivo della sezione**

Far vedere come anche per l'analogo discreto di una ODE:
$$
x_{n+1} = g(x_n)
$$
si definiscono
* punti fissi
* stabilità via $|g'(x^*)| < 1$


### A1.1 Punti fissi e stabilità

Un punto fisso $x^*$ soddisfa
$$
x^* = g(x^*).
$$

Linearizzando:
$$
x_n = x^* + \xi_n,
$$
si ottiene
$$
\xi_{n+1} \approx g'(x^*)\,\xi_n.
$$

Quindi:
- se $|g'(x^*)|<1$ il punto fisso è stabile;
- se $|g'(x^*)|>1$ è instabile.

Confronto con ODE: per $\dot x=f(x)$ la stabilità locale dipende dal segno di $f'(x^*)$; per le differenze dipende dal modulo $|g'(x^*)|$.

---

## A2. Mapping ODE ↔ sistemi discreti

**Obiettivo della sezione**

Mostrare che:

* ogni ODE discretizzata genera un sistema discreto
* ogni sistema discreto può essere interpretato come dinamica approssimata

### A2.1 ODE $\to$ discreto (discretizzazione)

Partendo da $\dot x=f(x)$, la discretizzazione di Eulero produce
$$
x_{n+1} = x_n + f(x_n)\Delta t,
$$
che è un sistema discreto del tipo $x_{n+1}=g(x_n)$ con
$$
g(x)=x+f(x)\Delta t.
$$

Quindi una scelta di schema numerico equivale a scegliere una mappa discreta che approssima il flusso continuo.

### A2.2 Discreto $\to$ ODE (interpretazione)

Al contrario, se abbiamo una dinamica discreta $x_{n+1}=g(x_n)$ e i passi sono piccoli, si può leggere l'incremento per passo come una "velocità media":
$$
\frac{x_{n+1}-x_n}{\Delta t} \approx f(x_n),
$$
dove
$$
f(x) \approx \frac{g(x)-x}{\Delta t}.
$$

Questo rende esplicito il punto concettuale: quando lavoriamo al computer, siamo sempre nel dominio delle dinamiche discrete, e le ODE entrano come limite o come modello ideale.

---

## Riferimenti

* Strogatz, S. H. *Nonlinear Dynamics and Chaos*. Westview Press.  
* Hirsch, M. W., Smale, S., Devaney, R. L. *Differential Equations, Dynamical Systems, and an Introduction to Chaos*. Academic Press.  
* Hairer, E., Nørsett, S. P., Wanner, G. *Solving Ordinary Differential Equations I: Nonstiff Problems*. Springer.  
* LeVeque, R. J. *Finite Difference Methods for Ordinary and Partial Differential Equations*. SIAM.  
* Press, W. H. et al. *Numerical Recipes: The Art of Scientific Computing*. Cambridge University Press.