---
title: "07: Processi di salto, rumore impulsivo e jump-diffusion"
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

## Riferimenti

* Gardiner, C. *Handbook of Stochastic Methods*. Springer.  
* Van Kampen, N. G. *Stochastic Processes in Physics and Chemistry*. Elsevier.  
* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review.
* Cont, R., Rama. (2004). *Financial Modelling with Jump Processes*. Chapman & Hall/CRC.
* Applebaum, D. (2009). *Lévy Processes and Stochastic Calculus* (2nd ed.). Cambridge University Press.