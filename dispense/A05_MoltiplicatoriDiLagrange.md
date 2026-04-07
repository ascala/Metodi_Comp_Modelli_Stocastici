---
title: "A05: Ottimizzazione vincolata, moltiplicatori di Lagrange e idea delle condizioni KKT"
author: "Antonio Scala"
date: ""
---

Questa appendice introduce in forma unitaria tre idee strettamente collegate: il metodo dei moltiplicatori di Lagrange per vincoli di uguaglianza, l’estensione ai vincoli di disuguaglianza tramite le condizioni di Karush--Kuhn--Tucker (KKT), e l’interpretazione geometrica e dinamica di questi strumenti. L’obiettivo non è sviluppare una teoria completa di ottimizzazione vincolata, ma fornire un quadro operativo e intuitivo che permetta di riconoscere quando e perché i vincoli modificano la condizione di equilibrio.

Il punto di partenza è semplice. In un problema di ottimizzazione libera, un estremo interno si cerca imponendo l’annullamento del gradiente della funzione obiettivo. Ma se le variabili devono soddisfare uno o più vincoli, non tutte le direzioni di variazione sono ammissibili: alcune sono proibite perché porterebbero fuori dal dominio consentito. In questo caso, il gradiente della funzione obiettivo non deve necessariamente annullarsi; deve invece essere bilanciato dai gradienti dei vincoli attivi.

Questa idea appare in molti contesti diversi. Compare nella massima entropia, nell’ottimizzazione su simplessi di probabilità, nei problemi economici con risorse limitate, nella meccanica con vincoli geometrici, e riappare anche, in forma più dinamica, quando si studiano flussi di gradiente o schemi numerici per SDE confinati in un dominio ammissibile.

### Obiettivi didattici specifici

1. Comprendere la differenza tra ottimizzazione libera e ottimizzazione vincolata.
2. Introdurre il metodo dei moltiplicatori di Lagrange per vincoli di uguaglianza.
3. Interpretare geometricamente la condizione di parallelismo tra gradienti.
4. Generalizzare l’idea a più vincoli.
5. Introdurre i vincoli di disuguaglianza e il concetto di vincolo attivo.
6. Presentare in forma elementare le condizioni di Karush--Kuhn--Tucker.
7. Collegare queste idee a dinamiche guidate da gradiente e a traiettorie vincolate.

### Struttura della appendice

La discussione è organizzata in nove parti:

1. **Perché servono metodi per l’ottimizzazione vincolata** -- differenza tra estremo libero ed estremo con vincoli.
2. **Moltiplicatori di Lagrange per vincoli di uguaglianza** -- costruzione e significato.
3. **Interpretazione geometrica** -- gradienti, piano tangente e direzioni ammissibili.
4. **Più vincoli di uguaglianza** -- estensione del metodo.
5. **Dal caso di uguaglianza ai vincoli di disuguaglianza** -- bordo, interno e vincoli attivi.
6. **Condizioni di Karush--Kuhn--Tucker** -- formulazione elementare e interpretazione.
7. **Esempi semplici** -- casi 1D e 2D per fissare le idee.
8. **Applicazione alla massima entropia** -- collegamento con il resto del corso.
9. **Collegamento con dinamiche vincolate e SDE** -- lettura dinamica dell’idea di vincolo.

---

## 1. Perché serve l’ottimizzazione vincolata

In un problema di ottimizzazione libera, per trovare un massimo o un minimo locale di una funzione $f(x_1,\dots,x_n)$ si cercano punti interni in cui
$$
\nabla f = 0.
$$
Questa condizione esprime il fatto che, in un estremo interno, non esiste alcuna direzione infinitesima in cui la funzione cresca o decresca al primo ordine. Per vedere perché, consideriamo una piccola variazione ammessa
$$
x \to x+\delta x\;.
$$
Sviluppando al primo ordine,
$$
f(x+\delta x)=f(x)+\nabla f(x)\cdot \delta x + O(\|\delta x\|^2).
$$
Al primo ordine, affinchè $x$ sia un punto stazionario, deve valere
$$
\nabla f(x)\cdot \delta x = 0\;,
$$
per qualsiasi $\delta x$, il che implica appunto $\nabla f(x) = 0$.

Se però le variabili devono soddisfare un vincolo, ad esempio
$$
g(x_1,\dots,x_n)=0,
$$
oppure un insieme di vincoli del tipo
$$
g_i(x)\le 0,
$$
non ci si può muovere arbitrariamente in tutte le direzioni. Le variazioni ammissibili sono ristrette a una regione più piccola dello spazio delle variabili: una curva, una superficie o, in generale, una ipersuperficie o un dominio delimitato dai vincoli. Quindi, dovrò considerare i $\delta x$ "compatibili" con il fatto che se $x$ soddisfa il vincolo, anche $x+\delta x$ dovrà soddisfarlo.

Di conseguenza, un estremo vincolato può trovarsi in un punto in cui il gradiente di $f$ non si annulla. Quello che conta è che non esistano variazioni ammissibili che migliorino il valore della funzione obiettivo al primo ordine.

Questa è l’idea che sta dietro sia ai moltiplicatori di Lagrange sia alle condizioni KKT.

---

## 2. Moltiplicatori di Lagrange: un vincolo di uguaglianza

Consideriamo il problema
$$
\text{trovare gli estremi di } f(x_1,\dots,x_n)
\quad \text{soggetti a} \quad
g(x_1,\dots,x_n)=0.
$$

### 2.1 Costruzione della Lagrangiana

Si introduce la funzione
$$
\mathcal{L}(x_1,\dots,x_n,\lambda) =
f(x_1,\dots,x_n)-\lambda\,g(x_1,\dots,x_n),
$$
dove $\lambda$ è il moltiplicatore di Lagrange.

L’idea è cercare i punti stazionari di $\mathcal{L}$ rispetto a tutte le variabili:
$$
\frac{\partial \mathcal{L}}{\partial x_i}=0
\qquad \text{per } i=1,\dots,n,
$$
e
$$
\frac{\partial \mathcal{L}}{\partial \lambda}=0.
$$

L’ultima equazione restituisce semplicemente il vincolo:
$$
\frac{\partial \mathcal{L}}{\partial \lambda}=-g(x)=0.
$$

Le derivate rispetto alle variabili $x_i$ forniscono invece
$$
\nabla f = \lambda \nabla g.
$$

Questa è la condizione fondamentale del metodo.

### 2.2 Significato della condizione

La relazione
$$
\nabla f = \lambda \nabla g
$$
dice che, in un punto ottimale vincolato, il gradiente della funzione obiettivo è parallelo al gradiente del vincolo.

Per vedere perché, consideriamo una piccola variazione ammessa
$$
x \to x+\delta x
$$
che lasci invariato il vincolo $g(x)=0$. Sviluppando al primo ordine,
$$
g(x+\delta x)=g(x)+\nabla g(x)\cdot \delta x + O(\|\delta x\|^2).
$$
Poiché sia $x$ sia $x+\delta x$ devono soddisfare il vincolo, si ha
$$
\nabla g(x)\cdot \delta x = 0
$$
al primo ordine.

Questo significa che gli spostamenti ammessi $\delta x$ sono ortogonali a $\nabla g(x)$, cioè tangenti alla superficie vincolata (i.e. i punti per cui $g(x)=0$).

Ora guardiamo la variazione di $f$:
$$
f(x+\delta x)=f(x)+\nabla f(x)\cdot \delta x + O(\|\delta x\|^2).
$$
Se $x$ è un estremo vincolato, questa variazione deve annullarsi al primo ordine per ogni spostamento ammesso. Dunque deve valere
$$
\nabla f(x)\cdot \delta x=0
$$
per ogni $\delta x$ tale che
$$
\nabla g(x)\cdot \delta x=0.
$$

Questo può accadere solo se $\nabla f(x)$ non ha componente tangente alla superficie del vincolo, ma è anch’esso normale ad essa. Poiché anche $\nabla g(x)$ è normale alla superficie $g(x)=0$, i due gradienti devono essere paralleli:
$$
\nabla f(x)=\lambda \nabla g(x).
$$

In altri termini, il gradiente della funzione obiettivo non deve avere componenti tangenti alla varietà ammissibile (cioè, in pratica, alla curva o alla (iper)superficie definita dai vincoli).

---

## 3. Interpretazione geometrica

La lettura geometrica del metodo è importante perché impedisce di usarlo come pura ricetta algebrica.

### 3.1 Direzioni ammissibili

Il vincolo
$$
g(x)=0
$$
definisce una superficie nello spazio delle variabili. Le variazioni ammissibili sono quelle tangenti a questa superficie.

Il gradiente $\nabla g(x)$ è normale alla superficie, quindi individua la direzione in cui il vincolo cambia più rapidamente. I "movimenti" che lasciano invariato il vincolo sono quindi quei $\delta x$ ortogonali al gradiente.

### 3.2 Estremo vincolato

In un estremo vincolato, non deve esserci alcuna direzione tangente alla superficie lungo cui $f$ possa aumentare o diminuire al primo ordine. Perciò il gradiente $\nabla f$ non può avere componente tangenziale: deve essere interamente normale alla superficie.

Poiché anche $\nabla g$ è normale alla stessa superficie, i due gradienti devono essere paralleli.

### 3.3 Messaggio didattico

Il metodo dei moltiplicatori di Lagrange non "elimina" il vincolo. Rende calcolabile il fatto che, in presenza di un vincolo, solo certe variazioni sono consentite.

---

## 4. Più vincoli di uguaglianza

Supponiamo ora di avere più vincoli:
$$
g_1(x)=0,\qquad g_2(x)=0,\qquad \dots,\qquad g_m(x)=0.
$$

Si introduce allora la Lagrangiana
$$
\mathcal{L}(x,\lambda_1,\dots,\lambda_m) =
f(x)-\sum_{j=1}^m \lambda_j g_j(x).
$$

Imponendo la stazionarietà rispetto alle variabili $x$ e ai moltiplicatori $\lambda_j$ si ottiene
$$
\nabla f = \sum_{j=1}^m \lambda_j \nabla g_j,
$$
insieme ai vincoli
$$
g_j(x)=0, \qquad j=1,\dots,m.
$$

### 4.1 Interpretazione

Con più vincoli, il gradiente della funzione obiettivo deve appartenere allo spazio generato dai gradienti dei vincoli. Equivalentemente, non deve avere componenti tangenti all’intersezione delle superfici vincolari.

---

## 5. Vincoli di disuguaglianza e idea di vincolo attivo

Molti problemi reali non impongono uguaglianze esatte, ma limiti del tipo
$$
g_i(x)\le 0.
$$
Per esempio:

- positività: $x\ge 0$, che può essere scritta come $-x\le 0$;
- limiti di capacità: $x+y\le 1$;
- probabilità ammissibili: $p_i\ge 0$.

In questo contesto, un vincolo può essere:

- **inattivo** se nel punto considerato vale strettamente
  $$
  g_i(x)<0;
  $$
- **attivo** se il punto si trova esattamente sul bordo:
  $$
  g_i(x)=0.
  $$

### 5.1 Intuizione

Se il punto ottimo è interno alla regione ammissibile, i vincoli di disuguaglianza non "si sentono": localmente si può ancora muovere il punto in tutte le direzioni, e quindi vale la condizione libera
$$
\nabla f=0.
$$

Se invece l’ottimo cade sul bordo, allora alcune direzioni non sono più ammissibili. In quel caso il gradiente non deve annullarsi necessariamente: può essere bilanciato dalla reazione del vincolo attivo.

Questa è precisamente l’idea delle condizioni KKT.

---

## 6. Condizioni di Karush--Kuhn--Tucker

Consideriamo il problema
$$
\min_x f(x)
\qquad \text{soggetto a} \qquad
g_i(x)\le 0,\quad i=1,\dots,m.
$$

Le condizioni di Karush--Kuhn--Tucker, in forma elementare, sono:

### 6.1 Fattibilità primale

Il punto candidato deve essere ammissibile:
$$
g_i(x^\star)\le 0
\qquad \text{per ogni } i.
$$

### 6.2 Moltiplicatori non negativi

A ciascun vincolo è associato un moltiplicatore $\lambda_i$ tale che
$$
\lambda_i \ge 0.
$$

### 6.3 Stazionarietà

Nel punto ottimo il gradiente della funzione obiettivo è bilanciato dai gradienti dei vincoli:
$$
\nabla f(x^\star)+\sum_{i=1}^m \lambda_i \nabla g_i(x^\star)=0.
$$

### 6.4 Complementarità

Per ogni vincolo vale
$$
\lambda_i\,g_i(x^\star)=0.
$$

Questa è la condizione più istruttiva. Significa che, per ciascun $i$, può accadere solo una delle due cose:

- o il vincolo è inattivo, cioè
  $$
  g_i(x^\star)<0,
  $$
  e allora necessariamente
  $$
  \lambda_i=0;
  $$
- oppure il vincolo è attivo, cioè
  $$
  g_i(x^\star)=0,
  $$
  e allora il moltiplicatore può essere positivo.

### 6.5 Interpretazione

La complementarità codifica un’idea semplice: un vincolo che non è toccato non esercita alcuna reazione; un vincolo che è attivo può invece controbilanciare la spinta del gradiente.

### 6.6 Confronto con Lagrange

Le condizioni di Lagrange sono il caso in cui i vincoli sono tutti di uguaglianza. Le condizioni KKT estendono questa logica ai vincoli di disuguaglianza, introducendo:

- la distinzione tra vincoli attivi e inattivi;
- il segno dei moltiplicatori;
- la complementarità.

---

## 7. Esempi semplici

## 7.1 Esempio 1 -- minimo su un vincolo di uguaglianza

Cerchiamo gli estremi di
$$
f(x,y)=x+y
$$
soggetti al vincolo
$$
x^2+y^2-1=0.
$$

La Lagrangiana è
$$
\mathcal{L}(x,y,\lambda)=x+y-\lambda(x^2+y^2-1).
$$

Le condizioni stazionarie sono
$$
1-2\lambda x=0,
$$
$$
1-2\lambda y=0,
$$
$$
x^2+y^2=1.
$$

Dalle prime due equazioni segue
$$
x=y.
$$
Sostituendo nel vincolo,
$$
2x^2=1,
$$
quindi
$$
x=y=\pm \frac{1}{\sqrt{2}}.
$$

I punti candidati sono dunque
$$
\left(\frac{1}{\sqrt{2}},\frac{1}{\sqrt{2}}\right)
\qquad \text{e} \qquad
\left(-\frac{1}{\sqrt{2}},-\frac{1}{\sqrt{2}}\right).
$$

Valutando $f$:
$$
f=\sqrt{2}
\qquad \text{e} \qquad
f=-\sqrt{2}.
$$

Quindi il massimo vincolato è $\sqrt{2}$ e il minimo vincolato è $-\sqrt{2}$.

---

## 7.2 Esempio 2 -- vincolo di disuguaglianza inattivo

Consideriamo
$$
\min_x (x-2)^2
\qquad \text{soggetto a} \qquad x\ge 0.
$$

Scriviamo il vincolo come
$$
g(x)=-x\le 0.
$$

La funzione obiettivo ha minimo libero in
$$
x=2,
$$
che è ammissibile. Dunque il vincolo è inattivo.

Le condizioni KKT danno infatti:

- fattibilità:
  $$
  -x\le 0;
  $$
- stazionarietà:
  $$
  2(x-2)-\lambda=0;
  $$
- complementarità:
  $$
  \lambda(-x)=0.
  $$

Per $x=2$ si ha $g(2)=-2<0$, quindi il vincolo non è attivo e necessariamente
$$
\lambda=0.
$$

Questo è il caso in cui il vincolo esiste, ma non modifica la soluzione.

---

## 7.3 Esempio 3 -- vincolo di disuguaglianza attivo

Ora consideriamo
$$
\min_x (x+1)^2
\qquad \text{soggetto a} \qquad x\ge 0.
$$

Ancora una volta scriviamo
$$
g(x)=-x\le 0.
$$

Il minimo libero della funzione sarebbe in
$$
x=-1,
$$
ma questo punto non è ammissibile. Il minimo vincolato deve quindi stare sul bordo:
$$
x^\star=0.
$$

Le condizioni KKT sono:

- fattibilità:
  $$
  -x\le 0;
  $$
- stazionarietà:
  $$
  2(x+1)-\lambda=0;
  $$
- complementarità:
  $$
  \lambda(-x)=0;
  $$
- non negatività:
  $$
  \lambda\ge 0.
  $$

Sostituendo $x^\star=0$ nella stazionarietà,
$$
2-\lambda=0,
$$
quindi
$$
\lambda=2>0.
$$

Qui il vincolo è attivo e il moltiplicatore è non nullo: il bordo reagisce e impedisce alla soluzione di scendere verso il minimo libero non ammissibile.

---

## 7.4 Esempio 4 -- minimo in due dimensioni con bordo attivo

Consideriamo
$$
\min_{x,y} \bigl((x-1)^2+(y+2)^2\bigr)
\qquad \text{soggetto a} \qquad y\ge 0.
$$

Il minimo libero è nel punto
$$
(1,-2),
$$
che non è ammissibile. Il minimo vincolato cade quindi sul bordo $y=0$.

Scriviamo il vincolo come
$$
g(x,y)=-y\le 0.
$$

La stazionarietà KKT è
$$
\nabla f + \lambda \nabla g = 0.
$$

Poiché
$$
\nabla f = \bigl(2(x-1),\,2(y+2)\bigr),
\qquad
\nabla g=(0,-1),
$$
si ottiene
$$
2(x-1)=0,
$$
$$
2(y+2)-\lambda=0.
$$

Dal primo segue
$$
x=1.
$$
Essendo il vincolo attivo,
$$
y=0,
$$
e quindi
$$
4-\lambda=0,
\qquad
\lambda=4.
$$

Il minimo vincolato è dunque
$$
(1,0).
$$

L’esempio mostra bene che sul bordo la dinamica resta libera lungo le direzioni tangenti, mentre la componente che spingerebbe fuori dominio viene compensata dal vincolo.

---

## 8. Applicazione alla massima entropia

Uno dei casi più importanti, nel contesto del corso, è la massimizzazione dell’entropia sotto vincoli.

Consideriamo una distribuzione discreta $p_1,\dots,p_n$ e vogliamo massimizzare
$$
H=-\sum_{i=1}^n p_i \log p_i
$$
sotto i vincoli
$$
\sum_{i=1}^n p_i = 1
$$
e
$$
\sum_{i=1}^n x_i p_i = m.
$$

Qui i vincoli sono di uguaglianza, quindi basta il metodo di Lagrange.

### 8.1 Lagrangiana

Introduciamo due moltiplicatori $\alpha$ e $\beta$ e scriviamo
$$
\mathcal{L} =
-\sum_{i=1}^n p_i\log p_i
-\alpha\left(\sum_{i=1}^n p_i-1\right)
-\beta\left(\sum_{i=1}^n x_i p_i-m\right).
$$

### 8.2 Condizioni stazionarie

Imponiamo
$$
\frac{\partial \mathcal{L}}{\partial p_i}=0.
$$
Otteniamo
$$
-(\log p_i+1)-\alpha-\beta x_i=0.
$$

Da qui segue
$$
\log p_i=-1-\alpha-\beta x_i,
$$
cioè
$$
p_i=e^{-1-\alpha-\beta x_i}.
$$

Assorbendo la costante comune nella normalizzazione si ottiene
$$
p_i \propto e^{-\beta x_i}.
$$

### 8.3 Nota sui vincoli di positività

In questo problema le condizioni $p_i\ge 0$ sono vincoli di disuguaglianza. Se la soluzione trovata ha tutte le probabilità strettamente positive, questi vincoli risultano inattivi e non modificano il calcolo. Se invece alcune componenti si annullano, allora la formulazione KKT diventa il linguaggio naturale per descrivere il problema completo.

---

## 9. Collegamento con dinamiche vincolate e SDE

Fin qui abbiamo parlato di problemi statici di ottimizzazione. La stessa struttura geometrica — gradiente della funzione obiettivo bilanciato dalla reazione normale al bordo — ricompare però anche in problemi dinamici, sia deterministici sia stocastici. Questa sezione sviluppa questo collegamento in modo sistematico, introducendo i tre meccanismi principali con cui si impone un vincolo su una traiettoria: la riflessione, la proiezione e la formulazione di Skorokhod.

---

### 9.1 Flusso di gradiente libero e vincolato

Consideriamo una dinamica deterministica del tipo
$$
\dot x = -\nabla V(x).
$$
In assenza di vincoli, la traiettoria segue la direzione di discesa più rapida del potenziale $V$. Se però imponiamo che la traiettoria resti in un dominio ammissibile
$$
D = \{x \in \mathbb{R}^d : g_i(x) \le 0,\; i = 1,\dots,p\},
$$
la dinamica deve essere modificata ogni volta che la traiettoria tende ad abbandonare $D$.

L'analogia con le condizioni KKT è immediata:

- all'interno di $D$, tutti i vincoli sono inattivi e la dinamica è quella libera: $\dot x = -\nabla V(x)$;
- sul bordo $\partial D$, i vincoli attivi reagiscono aggiungendo una componente normale che impedisce l'uscita;
- il moltiplicatore di Lagrange corrisponde all'intensità di questa reazione.

La condizione di stazionarietà KKT è quindi la versione *statica* di un principio che, in forma dinamica, descrive la traiettoria vincolata sul bordo.

---

### 9.2 Problema di Skorokhod: formulazione precisa

La formulazione rigorosa delle traiettorie vincolate per un processo stocastico è dovuta a Skorokhod. Consideriamo il caso più semplice: un dominio $D = [0, +\infty)$ in una dimensione.

Si vuole costruire un processo $X_t \ge 0$ che segua una data dinamica stocastica, ma resti sempre non negativo. Formalmente, si chiede di trovare una coppia $(X_t, L_t)$ tale che:

1. $X_t = X_0 + \int_0^t b(X_s)\,ds + \int_0^t \sigma(X_s)\,dW_s + L_t$;
2. $X_t \ge 0$ per ogni $t \ge 0$;
3. $L_t$ è non decrescente, con $L_0 = 0$;
4. $L_t$ cresce solo quando $X_t = 0$:
$$
\int_0^\infty \mathbf{1}_{\{X_t > 0\}}\,dL_t = 0.
$$

Il processo $L_t$ è il **tempo locale al bordo**: misura quanto a lungo la traiettoria ha premuto contro il vincolo $x = 0$. La quarta condizione è precisamente la condizione di complementarità KKT in forma dinamica: il vincolo reagisce solo quando è attivo.

#### Unicità e interpretazione

Sotto condizioni di regolarità su $b$ e $\sigma$, la soluzione $(X_t, L_t)$ esiste ed è unica. Il processo $X_t$ si chiama **processo riflesso** al bordo.

Geometricamente: ogni volta che la traiettoria raggiungerebbe un valore negativo, viene "rimbalzata" verso l'interno del dominio con un impulso normale al bordo. La normalità è esattamente la stessa proprietà geometrica che caratterizza i moltiplicatori di Lagrange.

---

### 9.3 Riflessione al bordo

#### Caso scalare

Il caso $D = [0,+\infty)$ ammette una formula esplicita. Se $Y_t$ è il processo "libero"
$$
Y_t = X_0 + \int_0^t b(Y_s)\,ds + \int_0^t \sigma(Y_s)\,dW_s,
$$
allora il processo riflesso è
$$
X_t = Y_t - \min_{0 \le s \le t} Y_s \wedge 0,
$$
dove la sottrazione del minimo corrente garantisce che $X_t \ge 0$ in ogni istante.

Per un intervallo $D = [a, b]$, la riflessione diventa bilaterale: il processo rimbalza sia sul bordo inferiore $a$ sia su quello superiore $b$.

#### Caso multidimensionale

In $\mathbb{R}^d$, per un dominio convesso $D$ con bordo liscio, la riflessione è sempre nella direzione della normale uscente $n(x)$ al punto di contatto $x \in \partial D$. La traiettoria vincolata soddisfa
$$
dX_t = b(X_t)\,dt + \sigma(X_t)\,dW_t + n(X_t)\,dL_t,
$$
dove $dL_t \ge 0$ e $dL_t > 0$ solo quando $X_t \in \partial D$.

Questo è esattamente il meccanismo KKT: la reazione è normale al bordo, con intensità non negativa che si attiva solo quando il vincolo è attivo.

---

### 9.4 Proiezione sul dominio ammissibile

Un secondo meccanismo, più adatto alla discretizzazione numerica, è la **proiezione**.

#### Idea di base

Dato un dominio $D$, la proiezione di un punto $y \notin D$ su $D$ è
$$
\Pi_D(y) = \arg\min_{x \in D} \|x - y\|.
$$

Se $D$ è convesso, la proiezione esiste ed è unica.

#### Schema di Eulero proiettato

Partendo da $X_0 \in D$, si costruisce la traiettoria discreta come segue. A ogni passo:

1. si esegue un passo di Eulero--Maruyama "libero":
$$
\tilde X_{n+1} = X_n + b(X_n)\Delta t + \sigma(X_n)\Delta W_n;
$$
2. se $\tilde X_{n+1} \notin D$, si proietta:
$$
X_{n+1} = \Pi_D(\tilde X_{n+1}).
$$

Questo schema garantisce $X_n \in D$ per ogni $n$ ed è semplice da implementare. Per i casi più usati in pratica, la proiezione ha forma esplicita.

#### Proiezione su casi pratici

**Semiretta non negativa** $D = [0, +\infty)$:
$$
\Pi_D(y) = \max(y, 0).
$$

**Intervallo** $D = [a, b]$:
$$
\Pi_D(y) = \min(\max(y, a), b).
$$

**Simplesso delle probabilità** $D = \{p \in \mathbb{R}^n : p_i \ge 0,\; \sum_i p_i = 1\}$:

La proiezione non è banale in forma analitica, ma si calcola efficientemente con un algoritmo basato sull'ordinamento delle componenti. Questo dominio compare naturalmente nelle dinamiche su distribuzioni di probabilità.

**Palla euclidea** $D = \{x : \|x\| \le r\}$:
$$
\Pi_D(y) = r\,\frac{y}{\|y\|} \quad \text{se } \|y\| > r, \qquad \Pi_D(y) = y \quad \text{altrimenti}.
$$

#### Relazione con Lagrange/KKT

Geometricamente, la proiezione è il gradiente del quadrato della distanza da $D$. La correzione applicata al punto esterno è sempre diretta verso la normale al bordo nel punto di proiezione. Si ritrovano quindi, ancora una volta, le stesse direzioni geometriche delle condizioni KKT.

---

### 9.5 Confronto tra riflessione, proiezione e termine di drift

I tre meccanismi si comportano diversamente sul bordo e hanno implicazioni diverse per la distribuzione stazionaria.

**Riflessione (Skorokhod):** è la formulazione continua e matematicamente rigorosa. La traiettoria scivola lungo il bordo senza penetrarlo. Il processo stazionario, quando esiste, rispecchia correttamente la distribuzione target confinata su $D$.

**Proiezione (schema discreto):** è più semplice da implementare numericamente. Introduce un piccolo errore di discretizzazione legato al passo $\Delta t$, ma converge alla traiettoria riflessa al diminuire del passo.

**Termine di drift correttivo:** in alcuni schemi, specialmente per processi di diffusione su semirette, si aggiunge un termine di deriva che "spinge" la traiettoria verso l'interno del dominio prima che raggiunga il bordo. Per esempio, nei processi di Bessel o nelle SDE di tipo Cox--Ingersoll--Ross, la non negatività è preservata da un drift della forma $\alpha/x$ che diverge al bordo, rendendo impossibile il raggiungimento di $x = 0$.

---

### 9.6 Esempio numerico: moto browniano riflesso su $[0,1]$

Consideriamo il moto browniano standard $dX_t = dW_t$ con riflessione in $x = 0$ e $x = 1$.

La distribuzione stazionaria attesa è la distribuzione uniforme su $[0,1]$: in assenza di derive, non c'è alcun punto privilegiato dell'intervallo.

**Schema di Euler proiettato** con passo $\Delta t$:

```python
import numpy as np

def brownian_reflected(T, dt, x0=0.5, seed=None):
    rng = np.random.default_rng(seed)
    N = int(T / dt)
    X = np.zeros(N)
    X[0] = x0
    for n in range(N - 1):
        X[n+1] = X[n] + rng.normal(scale=np.sqrt(dt))
        X[n+1] = np.clip(X[n+1], 0.0, 1.0)   # proiezione su [0,1]
    return X
```

La chiamata `np.clip` implementa $\Pi_{[0,1]}$ in una riga. Per verificare la correttezza dello schema, è sufficiente controllare che l'istogramma della traiettoria lunga converga alla distribuzione uniforme su $[0,1]$.

---

### 9.7 Connessione con lo schema numerico per SDE e diagnostica

Nelle simulazioni di SDE vincolate, la scelta del meccanismo di imposizione del vincolo influenza:

- la **distribuzione stazionaria** simulata: la proiezione con passo grande introduce distorsioni vicino al bordo;
- la **varianza** delle stime: traiettorie che "rimbalzano" frequentemente sul bordo hanno autocorrelazione più alta;
- la **positività** di grandezze fisiche: concentrazioni, probabilità, popolazioni richiedono $X_t \ge 0$.

**Segnali di allarme pratici:**

- valori negativi o fuori dominio anche dopo la proiezione: indica un errore di implementazione;
- distribuzione stazionaria sistematicamente distorta rispetto a quella teorica: indica passo $\Delta t$ troppo grande o schema inadatto;
- accumulo di massa artificiale al bordo: può indicare che il drift non è bilanciato correttamente con la riflessione.

La checklist diagnostica dell'Appendice A02 si applica direttamente: verificare la convergenza empirica al diminuire di $\Delta t$, confrontare momenti simulati con quelli teorici, e controllare che il processo resti nel dominio ammissibile.

---

### 9.8 Take-home message della sezione

- Le condizioni KKT non sono solo uno strumento statico: la reazione normale al bordo ricompare nelle dinamiche stocastiche come meccanismo di riflessione o proiezione.
- Il problema di Skorokhod è la formulazione rigorosa della traiettoria stocastica vincolata: il termine $L_t$ è il moltiplicatore di Lagrange dinamico, che agisce solo quando il vincolo è attivo.
- La proiezione è l'implementazione numerica più diretta: ad ogni passo, se la traiettoria esce dal dominio, viene riportata al punto più vicino sul bordo con una correzione normale.
- Per domini convessi con forma semplice (semiretta, intervallo, palla, simplesso), la proiezione ha formula esplicita.
- La distribuzione stazionaria del processo vincolato dipende dalla correttezza dello schema numerico: passi troppo grandi o proiezioni mal calibrate distorcono le statistiche.

---

## 10. Errori tipici e controlli rapidi

### 10.1 Dimenticare di imporre il vincolo

Risolvere la sola equazione di stazionarietà non basta. Occorre sempre reimporre esplicitamente i vincoli.

### 10.2 Confondere punti candidati con soluzioni definitive

Lagrange e KKT forniscono condizioni necessarie in molti casi, ma i punti trovati vanno poi interpretati: possono essere minimi, massimi o punti di sella.

### 10.3 Dimenticare la distinzione tra vincolo attivo e inattivo

Nei problemi con disuguaglianze, non tutti i vincoli contano allo stesso modo nel punto ottimo. La complementarità è precisamente ciò che distingue i due casi.

### 10.4 Perdere il significato geometrico

Usare il metodo come pura manipolazione algebrica porta facilmente a errori. La domanda guida deve sempre essere: quali direzioni di variazione sono realmente ammissibili?

### 10.5 Checklist minima

Quando affronti un problema di ottimizzazione vincolata, conviene controllare sempre:

- [ ] Qual è la funzione obiettivo?
- [ ] I vincoli sono uguaglianze, disuguaglianze, o entrambi?
- [ ] La Lagrangiana è stata scritta correttamente?
- [ ] Tutte le condizioni di stazionarietà sono state imposte?
- [ ] È stata imposta la fattibilità del punto candidato?
- [ ] Nei vincoli di disuguaglianza, quali sono attivi e quali no?
- [ ] È stata verificata la complementarità?
- [ ] I punti trovati sono davvero massimi o minimi?

---

## 11. Take-home message

- I moltiplicatori di Lagrange trattano vincoli di uguaglianza.
- Le condizioni KKT estendono la stessa logica ai vincoli di disuguaglianza.
- In un estremo vincolato, il gradiente della funzione obiettivo non deve avere componenti lungo le direzioni ammissibili.
- Un vincolo inattivo non reagisce; un vincolo attivo può invece bilanciare il gradiente.
- Questa idea geometrica riappare anche nelle dinamiche vincolate e negli schemi numerici per processi che devono restare in un dominio ammissibile.
- Nel caso della massima entropia, la distribuzione esponenziale emerge proprio dall’applicazione del metodo di Lagrange ai vincoli di normalizzazione e valor medio.