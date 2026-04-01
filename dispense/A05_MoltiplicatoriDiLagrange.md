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

Fin qui abbiamo parlato di problemi statici di ottimizzazione. Tuttavia la stessa intuizione geometrica riappare anche in problemi dinamici.

### 9.1 Flusso di gradiente libero

Consideriamo una dinamica deterministica del tipo
$$
\dot x = -\nabla V(x).
$$
In assenza di vincoli, la traiettoria segue localmente la direzione di discesa più rapida del potenziale $V$.

### 9.2 Flusso di gradiente con vincoli

Se imponiamo che la traiettoria resti in un dominio ammissibile $D$, la dinamica non può più seguire ciecamente $-\nabla V(x)$ quando si trova sul bordo. La componente che spingerebbe fuori dal dominio deve essere soppressa, proiettata o compensata da una reazione normale al bordo.

Questa è la controparte dinamica dell’idea KKT:

- all’interno del dominio il vincolo è inattivo;
- sul bordo il vincolo diventa attivo;
- compare una reazione normale che impedisce l’uscita dalla regione ammissibile.

### 9.3 Collegamento con le SDE

Una dinamica stocastica del tipo
$$
dX_t = b(X_t)\,dt + \sigma(X_t)\,dW_t
$$
può essere soggetta a vincoli di positività o confinamento in un dominio. In questi casi, a livello numerico o concettuale, si introducono meccanismi di:

- riflessione al bordo;
- proiezione sul dominio ammissibile;
- correzione positiva degli step numerici;
- termini di reazione vincolare.

L’analogia con Lagrange/KKT non deve essere presa come identità formale, ma come guida geometrica: anche qui il vincolo agisce solo quando sta per essere violato, e la sua azione è diretta tipicamente lungo la normale al bordo.

### 9.4 Esempi nel contesto del corso

Questa idea è utile quando si studiano:

- SDE con vincoli di positività;
- processi confinati in un intervallo o in un dominio;
- dinamiche sul simplesso delle probabilità;
- schemi numerici che devono preservare massa, non negatività o normalizzazione.

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