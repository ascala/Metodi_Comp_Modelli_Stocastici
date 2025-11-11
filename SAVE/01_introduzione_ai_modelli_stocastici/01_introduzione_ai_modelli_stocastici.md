
---
title: "Introduzione ai modelli stocastici"
date: ""
---

# Introduzione ai Modelli Stocastici

I modelli stocastici costituiscono un insieme di strumenti matematici per la descrizione e l’analisi di sistemi nei quali l’evoluzione temporale o spaziale è influenzata da componenti di natura aleatoria. A differenza dei modelli deterministici, nei quali uno stesso stato iniziale conduce sempre al medesimo risultato, i modelli stocastici introducono variabili casuali per rappresentare l’incertezza intrinseca dei fenomeni osservati.

L’approccio stocastico si fonda sulla teoria della probabilit\à e sulle sue estensioni analitiche e numeriche. I concetti centrali includono:

- le variabili aleatorie e le loro distribuzioni di probabilit\à;
- i processi stocastici, ossia famiglie di variabili aleatorie indicizzate da un parametro (tipicamente il tempo);
- le grandezze di interesse come medie, varianze, autocorrelazioni, funzioni di transizione e tempi di primo passaggio.

Tra le classi più studiate di processi stocastici si annoverano i processi di Poisson, le catene di Markov, i moti browniani e le loro generalizzazioni (ad esempio i processi di Lévy o le equazioni differenziali stocastiche).  
Ciascuno di questi modelli consente di rappresentare aspetti differenti della casualit\à: la discrezione o continuit\à degli stati, la presenza di memoria o di dipendenze temporali, la scala dei tempi e la natura dei rumori che perturbano il sistema.

Dal punto di vista applicativo, i modelli stocastici sono essenziali in molte discipline scientifiche e tecnologiche:

- in fisica, per lo studio della diffusione, del trasporto e dei fenomeni di rumore termico;
- in biologia, per modellizzare la dinamica delle popolazioni, le reazioni chimiche intracellulari e i processi epidemici;
- in finanza, per descrivere l’evoluzione dei prezzi e il rischio di mercato;
- in ingegneria e informatica, per l’analisi dei sistemi di code, delle reti di comunicazione e dei processi di affidabilit\à.

Dal punto di vista concettuale, l’uso di un modello stocastico implica un passaggio epistemologico importante: si rinuncia alla previsione puntuale per privilegiare la previsione statistica, cioè la stima di distribuzioni di probabilit\à o di momenti caratteristici.  
Tale impostazione consente non solo di rappresentare la variabilit\à osservata nei dati, ma anche di quantificare l’incertezza e valutare la robustezza delle previsioni.

In ambito computazionale, la simulazione di modelli stocastici richiede lo sviluppo di algoritmi di generazione di numeri casuali, metodi Monte Carlo, tecniche di integrazione stocastica e strategie di riduzione della varianza.  
La sinergia tra formulazione teorica e implementazione numerica costituisce oggi uno degli aspetti più fecondi della modellizzazione stocastica moderna.


## Obiettivi della lezione

- Comprendere la distinzione concettuale e formale tra modelli deterministici e stocastici.
- Introdurre il concetto di variabile aleatoria e distribuzione di probabilit\à.
- Definire un processo stocastico come famiglia di variabili aleatorie indicizzate nel tempo.
- Discutere i principali tipi di rumore (bianco, colorato) e il loro ruolo nella modellizzazione.
- Comprendere la differenza tra previsione deterministica e statistica.
- Collegare i modelli stocastici a esempi reali in fisica, biologia e finanza.
- Introdurre le basi concettuali per i metodi Monte Carlo e le catene di Markov.


## Motivazioni e concetti fondamentali

L’introduzione dei modelli stocastici nasce dall’esigenza di descrivere fenomeni in cui l’incertezza è parte integrante del sistema, non soltanto una limitazione della conoscenza.  
Esempi classici includono il moto browniano, le fluttuazioni di popolazione in biologia o la volatilit\à dei mercati finanziari.  
In ciascuno di questi casi, l’evoluzione del sistema non è completamente determinata dalle condizioni iniziali, ma influenzata da un insieme di eventi aleatori.

Un modello stocastico fornisce dunque una **descrizione probabilistica** dello stato del sistema, specificando le leggi di transizione e le propriet\à statistiche dei processi sottostanti.


## Variabili aleatorie e distribuzioni di probabilit\à

### Concetto generale

Una **variabile aleatoria** $X$ è una funzione che associa a ogni esito di un esperimento casuale $\omega$ appartenente a uno spazio di probabilit\à $(\Omega, \mathcal{F}, P)$ un valore numerico $X(\omega) \in \mathbb{R}$.  
Essa consente di formalizzare eventi casuali come oggetti matematici su cui è possibile calcolare medie, varianze e probabilit\à di insiemi di valori.

Le principali quantit\à descrittive di una variabile aleatoria sono:

- la **funzione di probabilit\à** (per variabili discrete) o la **densit\à di probabilit\à** (per variabili continue);
- la **funzione di distribuzione cumulativa** $F(x) = P(X \le x)$;
- i **momenti** $\langle X^n \rangle = \int x^n p(x)\,dx$ o $\sum_x x^n P(x)$;
- la **varianza** $\sigma^2 = \langle X^2 \rangle - \langle X \rangle^2$, che misura l’ampiezza delle fluttuazioni.

Una propriet\à fondamentale è la **normalizzazione**:

$$
\sum_x P(x) = 1 \quad \text{(discreta)}, \qquad \int_{-\infty}^{\infty} p(x)\,dx = 1 \quad \text{(continua)}.
$$


### Variabili discrete e continue

Le variabili aleatorie possono essere classificate in due grandi categorie.

#### Variabili discrete

L’insieme dei valori possibili è numerabile.  
Esempi:

- **Bernoulli**: $P(X=1)=p$, $P(X=0)=1-p$;
- **Binomiale**: $P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}$;
- **Poisson**: $P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}$.

Nel caso Poissoniano, $\lambda$ rappresenta il numero medio di eventi in un intervallo di tempo o spazio, e vale $\langle X \rangle = \lambda = \sigma^2$: la media coincide con la varianza.

#### Variabili continue

Il valore di $X$ può assumere infiniti valori in un intervallo.  
Esempi:

- **Uniforme** in $[a,b]$: $p(x)=1/(b-a)$;
- **Esponenziale**: $p(x)=\lambda e^{-\lambda x}$ per $x\ge 0$;
- **Normale (Gaussiana)**: $p(x)=\frac{1}{\sqrt{2\pi\sigma^2}} \exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]$.

La Gaussiana emerge come limite di molte distribuzioni per effetto del **teorema del limite centrale**: la somma di molte variabili indipendenti tende a una distribuzione normale, indipendentemente dalla forma delle distribuzioni di partenza.


### Propriet\à statistiche fondamentali

1. **Linearit\à della media**:

   $$
   \langle aX + bY \rangle = a\langle X\rangle + b\langle Y\rangle.
   $$

2. **Varianza di una combinazione lineare**:

   $$
   \mathrm{Var}(aX+bY)=a^2\mathrm{Var}(X)+b^2\mathrm{Var}(Y)+2ab\,\mathrm{Cov}(X,Y).
   $$

3. **Funzione caratteristica** (trasformata di Fourier della densit\à):

   $$
   \phi_X(k)=\langle e^{ikX}\rangle = \int e^{ikx}p(x)\,dx.
   $$

   Essa codifica tutti i momenti di $X$ e semplifica l’analisi di somme di variabili indipendenti:

   $$
   \phi_{X+Y}(k)=\phi_X(k)\phi_Y(k).
   $$


### Esempi e interpretazioni

| Distribuzione | Parametri | Media | Varianza | Applicazione tipica |
|----------------|------------|--------|-----------|----------------------|
| Bernoulli | $p$ | $p$ | $p(1-p)$ | Successo/fallimento |
| Binomiale | $n,p$ | $np$ | $np(1-p)$ | Numero di successi |
| Poisson | $\lambda$ | $\lambda$ | $\lambda$ | Conteggio di eventi rari |
| Esponenziale | $\lambda$ | $1/\lambda$ | $1/\lambda^2$ | Tempo d’attesa tra eventi |
| Normale | $\mu,\sigma$ | $\mu$ | $\sigma^2$ | Rumore additivo |
| Uniforme | $[a,b]$ | $(a+b)/2$ | $(b-a)^2/12$ | Campionamento uniforme |


### Dalla teoria alla simulazione

Per scopi computazionali, è spesso necessario **generare campioni casuali** secondo una distribuzione assegnata $p(x)$.  
Il punto di partenza è un **generatore uniforme** $U \in [0,1)$, da cui si ottiene $X = F^{-1}(U)$, dove $F^{-1}$ è la funzione inversa della distribuzione cumulativa.  
Questo principio, detto **metodo dell’inversione**, è alla base delle tecniche Monte Carlo.

Esempi pratici:

- Campionare una variabile esponenziale: $X = -\frac{1}{\lambda} \ln(1-U)$.
- Campionare una Gaussiana: trasformazione di Box–Muller o metodo di Marsaglia.

Questi concetti saranno approfonditi nella prossima lezione sui **Metodi Monte Carlo**, dove il calcolo di medie e integrali sar\à basato su campionamenti casuali da tali distribuzioni.


### Punti chiave

- Ogni variabile aleatoria è definita da una legge di probabilit\à normalizzata.
- I momenti e la funzione caratteristica descrivono completamente la distribuzione.
- Le distribuzioni canoniche emergono naturalmente in molti fenomeni fisici e computazionali.
- La simulazione di variabili casuali è il fondamento di tutti gli algoritmi stocastici.


## Processi stocastici: definizione e propriet\à

Un **processo stocastico** è una famiglia di variabili aleatorie $\{X(t)\}$ indicizzate dal tempo (o da un altro parametro).  
Un sistema stocastico può quindi essere visto come una sequenza temporale di variabili casuali correlate.

Caratteristiche principali:

- **Tempo discreto o continuo** ($t = 0,1,2,\ldots$ oppure $t \in \mathbb{R}^+$);
- **Spazio degli stati** discreto o continuo;
- **Dipendenza temporale**: la distribuzione a un tempo può dipendere da stati precedenti.

Un caso fondamentale è il **processo di Markov**, per il quale vale:

$$
P(X_{t+1}|X_t, X_{t-1}, \ldots) = P(X_{t+1}|X_t).
$$


## Rumore e media: dal determinismo alla fluttuazione

In molti modelli, l’evoluzione temporale di una variabile è descritta come:

$$
x_{t+1} = f(x_t) + \eta_t,
$$

dove $\eta_t$ rappresenta un termine di rumore.

Esempi:

- **Rumore bianco**: $\langle \eta_t \eta_{t'} \rangle = 2D \delta{t,t'}$;
- **Rumore colorato**: correlato nel tempo, con spettro non piatto.

Concetti chiave:

- **Media d’ensemble** $\langle x(t) \rangle$;
- **Media temporale** $\bar{x}_T = \frac{1}{T} \int_0^T x(t)\,dt$;
- **Ergodicit\à**: uguaglianza tra media temporale e media statistica.


## Modellizzazione stocastica e interpretazione

La modellizzazione stocastica combina la struttura dinamica deterministica con termini di rumore che rappresentano fluttuazioni, incertezze o interazioni non risolte.

Esempi:

- **Equazioni di Langevin** per il moto browniano;
- **Master equation** per transizioni tra stati discreti;
- **Fokker–Planck** per la distribuzione di probabilit\à nel tempo.

Questi modelli consentono di descrivere sia la **dinamica media** sia la **dispersione statistica** intorno ad essa.


## Esempi interdisciplinari

- **Fisica**: diffusione di una particella, rumore termico, dinamiche non lineari con rumore.
- **Biologia**: fluttuazioni nella crescita cellulare, modelli di reazioni chimiche intracellulari.
- **Finanza**: dinamica stocastica dei prezzi, modelli di rischio e volatilit\à.
- **Ingegneria**: affidabilit\à di sistemi complessi, traffico di rete, segnali rumorosi.


## Connessioni con i metodi numerici e le lezioni successive

I concetti introdotti in questa lezione costituiscono la base per:

- il **campionamento Monte Carlo** (lezione 02);
- le **catene di Markov** e l’**algoritmo di Metropolis–Hastings** (lezione 03);
- la **dinamica stocastica continua** tramite equazioni di Langevin (lezione 04);
- la **simulazione di eventi discreti** (lezione 06) e i modelli di **branching** (lezione 07).

Questa prima parte fornisce quindi il linguaggio formale e intuitivo che sar\à progressivamente approfondito nelle sezioni successive del corso.


## Riferimenti

- Gardiner, C. W. *Handbook of Stochastic Methods*. Springer.
- Van Kampen, N. G. *Stochastic Processes in Physics and Chemistry*. Elsevier.
- Gillespie, D. T. (1977). *Exact stochastic simulation of coupled chemical reactions*. _J. Phys. Chem._
- Ross, S. M. *Introduction to Probability Models*. Academic Press.
- Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. _SIAM Review._
