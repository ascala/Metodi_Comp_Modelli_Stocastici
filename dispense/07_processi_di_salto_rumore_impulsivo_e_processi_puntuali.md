---
title: "07: Processi di salto, rumore impulsivo e processi puntuali"
author: "Antonio Scala"
date: ""
---

Molti sistemi non cambiano in modo graduale, ma attraverso shock: eventi rari e grandi, discontinuità, salti improvvisi.  
Le SDE con rumore browniano descrivono bene fluttuazioni piccole e frequenti, ma possono fallire quando la dinamica è guidata da estremi.  
In questa lezione introduciamo i processi di salto (Poisson e compound Poisson) e le SDE con salti (jump-diffusion) come quadro unificante per modellare discontinuità, code pesanti e tipping indotto da shock.

### Obiettivi didattici specifici

1. Capire la differenza concettuale tra diffusione (Browniano) e salti (Poisson/compound Poisson).  
2. Definire un processo di Poisson $N_t$ e un processo compound Poisson $J_t = \sum_{k=1}^{N_t} Y_k$.  
3. Introdurre processi a traiettoria a tratti deterministica con salti (PDMP) e jump-diffusion.  
4. Interpretare correttamente $X_{t^-}$ e il termine di salto come integrale rispetto a $dN_t$.  
5. Collegare salti e fenomeni osservabili: collassi istantanei, first passage time a code pesanti, metastabilità e limiti degli early warning.

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Perché servono i salti** -- diffusive vs shock-driven: cosa cattura il Browniano e cosa no.  
2. **Processi di Poisson e compound Poisson** -- tempi di salto e ampiezze casuali.  
3. **Processi dinamici con salti** -- PDMP e SDE con salti (jump-diffusion).  
4. **Osservabili computazionali** -- $P(\tau\le T)$, distribuzione di $\tau$, early warning, scaling.  
5. **Tre esempi guida** -- tipping con Allee/bistabilità, OU con shock, logistica con harvesting impulsivo.

---

## 1. Perché servono i salti: oltre il rumore gaussiano

Nel capitolo sul rumore e le SDE abbiamo introdotto modelli del tipo
$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t,
$$
dove il termine $dW_t$ rappresenta fluttuazioni piccole e frequenti. 

Questo formalismo è naturale quando gli shock elementari sono numerosi e di ampiezza piccola: un limite centrale rende plausibile un rumore gaussiano. Tuttavia, in molti contesti i cambiamenti più rilevanti arrivano da eventi rari e grandi:

- fallimenti, crisi di liquidità, gap di prezzo (finanza);
- eventi estremi ambientali, mortalità di massa, introduzioni improvvise di predatori (ecologia);
- shock infrastrutturali, cascati di guasti, blackouts (reti e ingegneria);
- super-spreading o variazioni brusche dei pattern di contatto (epidemiologia).

In questi casi una dinamica puramente diffusiva può produrre due tipi di errore concettuale:

1. **Sovrastimare la gradualità del tipping.** Con Browniano, il collasso tende a presentare segnali graduali (varianza crescente, critical slowing down). Con salti, un singolo evento può attraversare una soglia senza segnali anticipatori affidabili.
2. **Sottostimare le code e gli estremi.** I tempi di primo passaggio e le distribuzioni marginali possono assumere code pesanti quando la dinamica è dominata da eventi impulsivi.

Questa lezione introduce quindi processi con salti come oggetti intermedi tra:
- dinamiche continue con rumore gaussiano;
- dinamiche a eventi discreti su spazio degli stati discreto.

Nota di contesto: Gillespie/SSA riguarda tipicamente catene di Markov continue nel tempo su stati discreti (reaction networks). Qui useremo invece processi di salto su spazio degli stati continuo o misto; il riferimento a SSA resta soltanto concettuale, per distinguere gli oggetti.

---

## 2. Processo di Poisson e compound Poisson

### 2.1 Processo di Poisson $N_t$

Un processo di Poisson con intensità $\lambda>0$ è un processo di conteggio $N_t$ tale che:

1. $N_0 = 0$;
2. gli incrementi sono indipendenti;
3. per ogni $t$ e $h>0$:
   $$
   P(N_{t+h}-N_t = 1) = \lambda h + o(h), \qquad
   P(N_{t+h}-N_t \ge 2) = o(h).
   $$

Ne segue che per ogni $t$:
$$
N_t \sim \mathrm{Poisson}(\lambda t),
$$
e che i tempi di attesa tra salti sono esponenziali i.i.d. con parametro $\lambda$:
$$
\Delta T_k \sim \mathrm{Exp}(\lambda), \qquad
T_k = \sum_{i=1}^k \Delta T_i.
$$

Interpretazione operativa: il processo genera una sequenza di tempi casuali $T_1,T_2,\dots$ ai quali avvengono gli eventi.

### 2.2 Compound Poisson: ampiezze casuali $Y_k$

Molti shock non sono tutti uguali: l’evento avviene, ma la sua ampiezza è casuale.
Si definisce quindi un processo compound Poisson:
$$
J_t = \sum_{k=1}^{N_t} Y_k,
$$
dove $Y_k$ sono i.i.d. e indipendenti da $N_t$.

- $N_t$ decide *quando* accadono gli shock;
- $Y_k$ decide *quanto* sono grandi.

Momenti (quando esistono):
$$
\mathbb{E}[J_t] = \lambda t\,\mathbb{E}[Y], \qquad
\mathrm{Var}(J_t) = \lambda t\,\mathbb{E}[Y^2].
$$

Questo oggetto è già sufficiente a generare distribuzioni con code più pesanti di quelle gaussiane, a seconda della scelta della legge di $Y$.

---

## 3. Processi dinamici con salti: PDMP e jump-diffusion

### 3.1 PDMP: dinamica deterministica tra salti

Un processo a tratti deterministico (piecewise-deterministic Markov process, PDMP) ha la struttura:

- tra i salti, $X_t$ evolve secondo una ODE;
- ai salti, $X_t$ subisce un aggiornamento impulsivo.

Una forma semplice è:
$$
dX_t = a(X_t,t)\,dt + dJ_t,
$$
con $J_t$ compound Poisson.

Equivalentemente, al tempo di salto $T_k$ si applica:
$$
X_{T_k^+} = X_{T_k^-} + Y_k.
$$

Qui $X_{t^-}$ indica il limite sinistro della traiettoria: è essenziale perché la traiettoria è discontinua e l’aggiornamento deve riferirsi al valore immediatamente prima del salto.

### 3.2 Jump-diffusion: Browniano + salti

La jump-diffusion combina fluttuazioni diffuse e shock:
$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t + \kappa(X_{t^-},t)\,dN_t.
$$

- $dW_t$ produce variazioni continue;
- $dN_t$ produce salti di ampiezza deterministica $\kappa$ (jump di ampiezza fissata dallo stato).

Versione con ampiezze casuali (più realistica):
$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t + \int_{\mathbb{R}} \gamma(X_{t^-},t,y)\,\tilde{N}(dt,dy).
$$

Qui $\tilde{N}(dt,dy)$ è una misura di Poisson che conta salti nel tempo e nella dimensione $y$.
Per questa lezione basta l’interpretazione: si sommano contributi impulsivi di ampiezza $y$, modulati da $\gamma$.

---

## 4. Accenno "Lévy light": idea e contenuto della formula di Lévy--Khintchine

Un processo di Lévy è un processo a incrementi indipendenti e stazionari.
Il moto browniano è un processo di Lévy (continuo); anche il compound Poisson è un processo di Lévy (a salti).

L’idea unificante è che gli incrementi possono avere:

- una componente deterministica (drift);
- una componente gaussiana (diffusione);
- una componente di salti (misura di Lévy).

In forma concettuale, la tripla $(\mu,\sigma,\nu)$ descrive:
- drift $\mu$;
- intensità gaussiana $\sigma$;
- misura di Lévy $\nu$ che codifica frequenza e ampiezza dei salti.

La formula di Lévy--Khintchine dice che la funzione caratteristica degli incrementi è determinata da questa tripla.
In questa lezione la portiamo a casa come messaggio operativo:

> Browniano e compound Poisson non sono modelli “diversi”: sono due pezzi dello stesso oggetto (processi di Lévy). Una jump-diffusion li combina.

Non entriamo nei dettagli tecnici della misura $\nu$: l’uso pratico sarà simulare Poisson e compound Poisson, e sommarli al contributo diffusivo.

---

## 5. Osservabili computazionali: collasso, first passage, early warning, scaling

Molti problemi applicativi si riducono a osservabili di hitting/first passage rispetto a una soglia o a un insieme bersaglio.
Sia $A$ un insieme (ad esempio una soglia di collasso) e definiamo il tempo di primo passaggio:
$$
\tau = \inf\{t\ge 0: X_t \in A\}.
$$

Obiettivi computazionali principali:

1. **Probabilità di collasso entro orizzonte $T$:**
   $$
   P(\tau \le T).
   $$

2. **Distribuzione di $\tau$:**
   - istogramma empirico;
   - stima della funzione di sopravvivenza $P(\tau > t)$.

3. **Metastabilità e scaling:**
   - come varia il comportamento di $\tau$ con $\lambda$ (frequenza degli shock);
   - come varia con la distribuzione delle ampiezze $Y$ (tail e varianza di $Y$);
   - come cambia passando da diffusione pura a salti puri a jump-diffusion.

4. **Early warning e loro limiti:**
   Gli indicatori basati su varianza e autocorrelazione (che hanno senso nella narrazione del rumore diffuso e del critical slowing down) possono fallire quando:
   - l’evento dominante è un singolo salto;
   - la varianza cresce poco prima del collasso (o non cresce affatto);
   - la distribuzione ha code pesanti e gli estremi dominano.

Messaggio didattico: con salti, il collasso può essere "senza preavviso" nel senso statistico operativo, pur essendo perfettamente compatibile con un modello noto.

---

## 6. Discretizzazione numerica: split-step e simulazione dei salti

L’obiettivo qui non è costruire metodi sofisticati, ma fissare lo schema concettuale.

### 6.1 Jump-only (PDMP con compound Poisson)

Due modi equivalenti:

**(A) Event-driven (tempi esponenziali)**  
1. campiona il prossimo tempo di salto $\Delta T \sim \mathrm{Exp}(\lambda)$;  
2. integra la ODE tra $t$ e $t+\Delta T$;  
3. applica il salto $Y$ o $\gamma(\cdot,Y)$;  
4. ripeti.

**(B) Time-stepping (Bernoulli su $\Delta t$)**  
Per passo fisso $\Delta t$:
- integra la ODE per un passo;
- genera un Bernoulli con probabilità $\lambda \Delta t$ (se $\Delta t$ è piccolo);
- se l’evento accade, aggiungi il salto.

Il metodo (A) è concettualmente più pulito; il metodo (B) è semplice e compatibile con la pipeline SDE.

### 6.2 Jump-diffusion: Euler--Maruyama + salti (split-step)

Per una jump-diffusion:
$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t + dJ_t,
$$
con $J_t$ compound Poisson, lo schema split-step su passo $\Delta t$ è:

1. **diffusione (Euler--Maruyama):**
   $$
   X' = X + a(X,t)\Delta t + b(X,t)\sqrt{\Delta t}\,Z,\qquad Z\sim N(0,1);
   $$
2. **salti nel passo:**
   - campiona $K \sim \mathrm{Poisson}(\lambda \Delta t)$;
   - se $K>0$, applica $K$ salti con ampiezze i.i.d. $Y_1,\dots,Y_K$:
     $$
     X_{\text{new}} = X' + \sum_{i=1}^{K} Y_i.
     $$

Se la dinamica richiede vincoli (positività, soglie fisiche), qui si inserisce una regola esplicita di gestione del dominio, coerente con quanto discusso nella lezione sulla stabilità numerica. :contentReference[oaicite:3]{index=3}

---

## 7. Tre esempi guida

In tutti gli esempi consideriamo una soglia di collasso e misuriamo $\tau$ e $P(\tau\le T)$.
L’obiettivo è avere modelli semplici ma qualitativamente distinti.

### 7.1 Bistabilità / Allee: tipping con soglia di collasso

Un prototipo in ecologia è una dinamica con effetto Allee: sotto una soglia, la crescita netta diventa negativa.
Un modello deterministico semplice è:
$$
\frac{dx}{dt} = r\,x\left(1-\frac{x}{K}\right)\left(\frac{x}{A}-1\right),
$$
dove $A$ è la soglia di Allee.

Versioni stocastiche:

- **diffusiva:**
  $$
  dX_t = f(X_t)\,dt + \sigma\,dW_t;
  $$
- **a salti:**
  $$
  dX_t = f(X_t)\,dt + dJ_t;
  $$
- **jump-diffusion:**
  $$
  dX_t = f(X_t)\,dt + \sigma\,dW_t + dJ_t.
  $$

Scelta del collasso: $A_{\text{coll}} = \{x \le x_c\}$ con $x_c$ vicino o sotto $A$.

Cosa osservare:
- nel caso diffusivo, tipping spesso preceduto da segnali graduali;
- nel caso a salti, collasso possibile con un singolo shock, anche quando $x$ è vicino allo stato alto;
- dipendenza forte da $\lambda$ e dalla tail di $Y$.

### 7.2 Ornstein--Uhlenbeck con shock: confronto pulito di code e hitting time

Processo OU (stabile e lineare):
$$
dX_t = -\theta(X_t - m)\,dt + \sigma\,dW_t.
$$

Aggiunta di shock:
$$
dX_t = -\theta(X_t - m)\,dt + \sigma\,dW_t + dJ_t.
$$

Soglia di collasso (esempio): $A_{\text{coll}} = \{x \le L\}$ con $L<m$.

Perché è un benchmark utile:
- senza salti, la distribuzione stazionaria è gaussiana;
- con salti, l’uscita oltre soglia può diventare dominata da un singolo evento;
- la distribuzione di $\tau$ cambia forma in modo netto (code più pesanti quando dominano i salti).

### 7.3 Logistica con harvesting impulsivo

Modello deterministico con harvesting continuo:
$$
\frac{dx}{dt} = r x\left(1-\frac{x}{K}\right) - h.
$$

Harvesting impulsivo: rimozioni episodiche (ad esempio eventi di pesca intensa, predazione episodica, shock di domanda/offerta).
Si modella come:
$$
dX_t = r X_t\left(1-\frac{X_t}{K}\right)\,dt - h\,dt - dJ_t,
$$
dove i salti sono negativi (rimozioni) e $J_t$ è compound Poisson con $Y_k \ge 0$.

Soglia di collasso: $A_{\text{coll}} = \{x \le x_c\}$.

Cosa osservare:
- con harvesting continuo, la transizione al collasso tende a essere più graduale;
- con harvesting impulsivo, il collasso può avvenire in un singolo episodio;
- la stima di $P(\tau\le T)$ è sensibile a $\lambda$ e alla coda di $Y$.

---

## 8. Takeaway: cosa aggiungono i salti rispetto alle SDE gaussiane

1. **Fenomeni qualitativi nuovi**: collassi istantanei, first passage con code pesanti, dominanza degli estremi.  
2. **Metastabilità diversa**: non solo fuga per accumulo di rumore diffuso, ma anche "fuga per evento raro".  
3. **Early warning meno robusti**: varianza e autocorrelazione non sono indicatori affidabili quando il collasso è shock-driven.  
4. **Unificazione concettuale**: Browniano e compound Poisson sono due componenti di processi di Lévy; la jump-diffusion li combina in modo naturale.

---

---

## Parte III: processi puntuali, intensità condizionata e thinning

Nelle sezioni precedenti il processo di Poisson $N_t$ era un ingrediente di una dinamica più ampia: contava i salti in una SDE o in un PDMP. In questa parte lo studiamo come oggetto autonomo. L'interesse non è la traiettoria di una variabile di stato, ma la sequenza degli istanti in cui avvengono gli eventi.

---

## 9. La sequenza degli eventi come oggetto di studio

### 9.1 Processo puntuale

Un **processo puntuale** su $[0, \infty)$ è una sequenza aleatoria di tempi

$$
0 < t_1 < t_2 < t_3 < \cdots
$$

dove ogni $t_k$ è il tempo del $k$-esimo evento. L'oggetto primitivo non è più una traiettoria continua $X_t$, ma una collezione di istanti.

**Esempi concreti:**

- scosse di assestamento dopo un terremoto principale;
- messaggi ricevuti su una rete;
- reati registrati in una zona urbana in un arco di tempo;
- scariche di un neurone in un esperimento di elettrofisiologia;
- ordini di acquisto su un mercato finanziario ad alta frequenza.

In tutti questi casi la domanda non è "qual è il valore del sistema al tempo $t$?" ma "quanti eventi sono avvenuti, e quando?".

### 9.2 Dal processo di Poisson omogeneo al caso generale

Il processo di Poisson omogeneo con intensità $\lambda$ costante, già introdotto nella Sezione 2, è il processo puntuale più semplice. Ha tre proprietà che nella Sezione 2 abbiamo usato senza nominarle esplicitamente:

1. **stazionarietà degli incrementi**: la distribuzione del numero di eventi in $(s, s+h]$ dipende solo da $h$, non da $s$;
2. **indipendenza degli incrementi**: eventi in intervalli disgiunti sono indipendenti;
3. **intensità costante**: la probabilità di un evento in $(t, t+dt]$ è $\lambda \, dt + o(dt)$, indipendentemente da tutto il passato.

La terza proprietà è quella che vogliamo generalizzare: l'intensità non deve essere né costante nel tempo né indipendente dalla storia degli eventi precedenti.

---

## 10. Processo di Poisson non omogeneo

### 10.1 Intensità deterministica variabile nel tempo

Il **processo di Poisson non omogeneo** generalizza il caso omogeneo permettendo all'intensità di variare nel tempo in modo deterministico:

$$
P(\text{evento in } (t, t+dt]) = \lambda(t) \, dt + o(dt).
$$

La funzione $\lambda(t) \ge 0$ è chiamata **intensità** o **tasso di occorrenza**. Il numero di eventi nell'intervallo $(s, t]$ è una variabile di Poisson con media

$$
\Lambda(s, t) = \int_s^t \lambda(u) \, du.
$$

Questa quantità si chiama **misura di intensità cumulata**.

**Esempi concreti:**

- traffico telefonico: più chiamate nelle ore centrali della giornata, meno di notte;
- terremoti: la frequenza degli aftershocks decresce nel tempo seguendo la legge di Omori;
- visite a un sito web: picchi nelle ore di punta che seguono un profilo periodico;
- richieste a un server: raffiche durante eventi pubblici seguiti da periodi di calma.

### 10.2 Proprietà

Gli incrementi restano **indipendenti** in intervalli disgiunti, come nel caso omogeneo. Quello che cambia è solo l'intensità locale: la probabilità di un evento in $(t, t+dt]$ è $\lambda(t) \, dt$, non $\lambda \, dt$.

La distribuzione del tempo al primo evento a partire da $t=0$ non è più esponenziale. Se $\lambda(t)$ è variabile, la funzione di sopravvivenza del primo evento è

$$
P(t_1 > t) = \exp\!\left(-\int_0^t \lambda(u) \, du\right).
$$

Per $\lambda$ costante si recupera la distribuzione esponenziale.

### 10.3 Simulazione per inversione

Il modo più diretto per simulare un processo non omogeneo è l'**inversione della misura cumulata**. Se $\Lambda(t) = \int_0^t \lambda(u) \, du$ è invertibile, si genera $U \sim U[0,1]$ e si pone $t_1 = \Lambda^{-1}(-\log U)$.

Questo metodo richiede di calcolare e invertire $\Lambda$, e diventa scomodo quando $\lambda(t)$ ha forma complessa. Il metodo del thinning, che introduciamo tra poco, è molto più generale.

---

## 11. Intensità condizionata

### 11.1 La storia passata degli eventi

Il passo concettuale più importante di questa sezione è il seguente: l'intensità con cui avvengono nuovi eventi può dipendere non solo dal tempo $t$, ma anche da tutti gli eventi avvenuti prima di $t$.

Definiamo la **storia** del processo fino al tempo $t$ (escluso) come

$$
\mathcal{H}_t = \{t_k : t_k < t\}.
$$

L'**intensità condizionata** è

$$
\lambda^*(t) = \lambda^*(t \mid \mathcal{H}_t),
$$

cioè la probabilità condizionata di un evento nell'istante successivo, dato tutto quello che è avvenuto prima:

$$
P(\text{evento in } (t, t+dt] \mid \mathcal{H}_t) = \lambda^*(t) \, dt + o(dt).
$$

Questa definizione unifica il caso omogeneo ($\lambda^* = \lambda$ costante, nessuna memoria), il caso non omogeneo ($\lambda^* = \lambda(t)$ deterministica, nessuna memoria degli eventi), e i processi con memoria come Hawkes ($\lambda^*$ dipende dalla storia).

### 11.2 Perché l'intensità condizionata è l'oggetto giusto

Nel caso del processo di Poisson omogeneo, conoscere la storia $\mathcal{H}_t$ non serve a nulla per prevedere il prossimo evento: gli incrementi futuri sono indipendenti dal passato. Ma in molti sistemi reali questo non è vero:

- **sismologia**: un terremoto aumenta la probabilità di scosse successive nelle ore e nei giorni seguenti;
- **criminalità**: un reato in una zona aumenta la probabilità di reati successivi nelle vicinanze;
- **neuroscienze**: una scarica neuronale modifica temporaneamente l'eccitabilità del neurone;
- **social media**: un post popolare genera una cascata di retweet che aumenta momentaneamente la probabilità di nuove condivisioni.

In tutti questi casi l'intensità condizionata $\lambda^*(t)$ cattura esattamente l'effetto della storia recente sulla probabilità di nuovi eventi.

### 11.3 Un esempio semplice: intensità che decade dopo ogni evento

Per fissare le idee, consideriamo un modello in cui ogni evento riduce momentaneamente la probabilità di nuovi eventi (ad esempio, un neurone che entra in periodo refrattario):

$$
\lambda^*(t) = \mu - \sum_{t_k < t} \alpha \, e^{-\beta(t - t_k)}, \qquad \lambda^*(t) \ge 0.
$$

Subito dopo ogni evento al tempo $t_k$, l'intensità si riduce di $\alpha$ e poi risale esponenzialmente verso $\mu$ con costante di tempo $1/\beta$.

Il caso opposto — ogni evento *aumenta* la probabilità di nuovi eventi — è il processo di Hawkes, che è la base del progetto omonimo del corso. Lì il segno del termine sommatoria è positivo:

$$
\lambda^*(t) = \mu + \sum_{t_k < t} \alpha \, e^{-\beta(t - t_k)}.
$$

La struttura matematica è identica; cambia solo il segno dell'effetto.

### 11.4 Requisiti di coerenza

Perché $\lambda^*(t)$ definisca un processo puntuale ben posto, occorre che:

1. $\lambda^*(t) \ge 0$ per ogni $t$ e ogni realizzazione della storia;
2. l'integrale $\int_0^T \lambda^*(t) \, dt < \infty$ quasi certamente per ogni $T$ finito.

La seconda condizione garantisce che il numero di eventi in ogni intervallo finito sia finito quasi certamente.

---

## 12. Il metodo del thinning (algoritmo di Ogata)

### 12.1 Il problema della simulazione

Come si simula un processo puntuale con intensità condizionata $\lambda^*(t)$?

Il problema è che $\lambda^*(t)$ cambia ogni volta che avviene un evento: dopo ogni $t_k$ l'intensità fa un salto e poi si evolve. Non si può usare direttamente l'inversione della misura cumulata perché $\Lambda(t) = \int_0^t \lambda^*(s) \, ds$ non è nota in anticipo — dipende dagli eventi futuri che stiamo cercando di generare.

Il **metodo del thinning**, proposto da Ogata (1981), risolve questo problema in modo elegante usando un processo di Poisson omogeneo come processo ausiliario.

### 12.2 Idea del thinning

L'idea di base è semplice. Supponiamo di sapere che, nell'intervallo $(t, t + \delta]$, l'intensità condizionata soddisfa

$$
\lambda^*(s) \le \Lambda \qquad \text{per ogni } s \in (t, t+\delta].
$$

Allora possiamo simulare un processo di Poisson omogeneo con tasso $\Lambda$ nell'intervallo $(t, t+\delta]$ — facile, perché i tempi tra eventi sono esponenziali — e poi **assottigliare** (thin) questo processo: ogni evento candidato al tempo $s$ viene accettato con probabilità $\lambda^*(s) / \Lambda$ e rifiutato altrimenti.

Gli eventi accettati formano un processo con intensità $\lambda^*(t)$. Quelli rifiutati vengono scartati. Il risultato è corretto perché:

$$
P(\text{evento candidato accettato in } (s, s+ds]) = \Lambda \, ds \cdot \frac{\lambda^*(s)}{\Lambda} = \lambda^*(s) \, ds.
$$

### 12.3 Algoritmo per il caso con kernel esponenziale

Per un processo con intensità condizionata della forma

$$
\lambda^*(t) = \mu + \sum_{t_k < t} \alpha \, e^{-\beta(t - t_k)},
$$

l'algoritmo del thinning ha una forma particolarmente efficiente. Tra un evento e il successivo, l'intensità è **decrescente** (il termine della somma decade esponenzialmente). Quindi l'upper bound $\Lambda$ nell'intervallo che segue l'ultimo evento al tempo $t_{\text{last}}$ è semplicemente $\lambda^*(t_{\text{last}}^+)$, il valore subito dopo l'evento.

Lo schema è il seguente.

**Inizializzazione.** Poni $t = 0$, $\lambda^* = \mu$.

**Ciclo:**

1. Genera il tempo candidato: $\Delta \sim \mathrm{Exp}(\lambda^*)$, poni $t_{\mathrm{cand}} = t + \Delta$.
2. Calcola l'intensità effettiva al tempo candidato: $\lambda^*(t_{\mathrm{cand}})$ (l'intensità è decaduta esponenzialmente da $t$ a $t_{\mathrm{cand}}$).
3. Accetta $t_{\mathrm{cand}}$ come evento reale con probabilità $\lambda^*(t_{\mathrm{cand}}) / \lambda^*$.
4. Se accettato: registra $t_{\mathrm{cand}}$ come nuovo evento, aggiorna $\lambda^*$ aggiungendo $\alpha$ all'intensità corrente, poni $t = t_{\mathrm{cand}}$.
5. Se rifiutato: aggiorna solo il tempo corrente $t = t_{\mathrm{cand}}$ e l'intensità decaduta; ripeti dal punto 1 con il nuovo upper bound.
6. Fermati quando $t > T$.

**Perché funziona.** Il candidato viene generato dal processo omogeneo con tasso $\Lambda = \lambda^*(t)$ (valore corrente dell'upper bound). L'accettazione con probabilità $\lambda^*(t_{\mathrm{cand}}) / \Lambda$ corregge per il fatto che l'intensità reale è minore del bound. Il risultato è un processo con la corretta intensità condizionata.

### 12.4 Pseudocodice

```python
def simulate_hawkes(mu, alpha, beta, T):
    events = []
    t = 0.0
    lambda_star = mu  # intensita' corrente (upper bound)

    while t < T:
        # genera il candidato
        dt = random.expovariate(lambda_star)
        t_cand = t + dt

        if t_cand > T:
            break

        # intensita' effettiva al tempo candidato
        # (il termine della somma e' decaduto esponenzialmente)
        lambda_at_cand = mu + (lambda_star - mu) * math.exp(-beta * dt)

        # accetta o rifiuta
        if random.random() < lambda_at_cand / lambda_star:
            # evento accettato
            events.append(t_cand)
            lambda_star = lambda_at_cand + alpha  # aggiorna con il salto
        else:
            # evento rifiutato: aggiorna solo l'upper bound
            lambda_star = lambda_at_cand

        t = t_cand

    return events
```

Il codice sfrutta il fatto che, con il kernel esponenziale, l'intensità tra due eventi consecutivi si calcola in modo ricorsivo senza riscorrere tutta la storia: basta tenere traccia del valore corrente di $\lambda^*$ e aggiornarlo esponenzialmente.

### 12.5 Efficienza

Per il kernel esponenziale l'algoritmo è molto efficiente: l'upper bound $\Lambda = \lambda^*(t)$ è esattamente il valore corrente dell'intensità, che decresce tra un evento e il successivo. Di conseguenza la probabilità di accettazione dei candidati è in media alta, e pochi eventi vengono rifiutati.

Per kernel con code pesanti (come la legge di potenza usata nella sismologia), l'intensità non decade rapidamente e l'upper bound può essere molto lontano dal valore effettivo. In quel caso l'algoritmo è meno efficiente e si usano varianti adattive.

---

## 13. Dalla jump-diffusion ai processi puntuali: un confronto

Vale la pena fermarsi a confrontare le due prospettive sulla stocasticità discreta introdotte in questa dispensa.

Nella **jump-diffusion** (Parte II), i salti sono un ingrediente di una dinamica continua: il processo $X_t$ ha traiettorie quasi continue puntualmente interrotte da salti. L'oggetto di studio è la traiettoria di $X_t$, e i salti modificano una variabile di stato continua. Le domande tipiche riguardano il first passage time, la distribuzione stazionaria, la probabilità di collasso.

Nel **processo puntuale** (questa parte), la sequenza $\{t_k\}$ è l'oggetto primario. Non c'è una variabile di stato continua: ciò che conta è quando avvengono gli eventi, quanti ne avvengono in un intervallo, e come la storia degli eventi passati modifica la probabilità di quelli futuri. Le domande tipiche riguardano il tasso di occorrenza, il clustering temporale, la struttura di dipendenza tra eventi.

La differenza è concettuale prima che tecnica. In entrambi i casi il processo di Poisson è il mattone di base, ma il modo in cui viene usato è diverso: come generatore di salti in una SDE, oppure come processo ausiliario nel thinning per simulare sequenze di eventi con memoria.

---

## 14. Takeaway: cosa aggiunge la Parte III

1. **Processo puntuale come oggetto autonomo**: la sequenza degli eventi, non la traiettoria di una variabile di stato, è l'oggetto di interesse.
2. **Poisson non omogeneo**: l'intensità può variare nel tempo in modo deterministico; gli incrementi restano indipendenti ma con media variabile.
3. **Intensità condizionata**: l'intensità può dipendere dalla storia degli eventi passati, catturando fenomeni come aftershocks, near-repeat, propagazione di informazione.
4. **Thinning di Ogata**: un metodo elegante per simulare qualsiasi processo puntuale con intensità condizionata, basato su un processo omogeneo ausiliario e accettazione/rifiuto.
5. **Ponte verso Hawkes**: il processo di Hawkes è un processo puntuale con intensità condizionata della forma $\mu + \sum_{t_k < t} \phi(t - t_k)$; gli strumenti di questa sezione sono esattamente quelli necessari per definirlo, simularlo e interpretarlo.

---

## Riferimenti

* Gardiner, C. *Handbook of Stochastic Methods*. Springer.  
* Van Kampen, N. G. *Stochastic Processes in Physics and Chemistry*. Elsevier.  
* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review.
* Cont, R., Rama. (2004). *Financial Modelling with Jump Processes*. Chapman & Hall/CRC.
* Applebaum, D. (2009). *Lévy Processes and Stochastic Calculus* (2nd ed.). Cambridge University Press.
* Ogata, Y. (1981). On Lewis' Simulation Method for Point Processes. *IEEE Transactions on Information Theory*, 27(1), 23--31.
* Daley, D. J., and Vere-Jones, D. (2003). *An Introduction to the Theory of Point Processes*, Vol. I. Springer.