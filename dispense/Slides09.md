---
title: "Lezione 09 -- Stima dei parametri e log-likelihood"
author: "Antonio Scala"
date: ""
subtitle: "Metodi computazionali per modelli stocastici"
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

# Obiettivi

## Obiettivi della lezione

In questa lezione introduciamo il problema della **stima dei parametri** nei modelli stocastici.

Alla fine della lezione dovremmo saper:

- costruire likelihood e log-likelihood;
- calcolare stimatori MLE in esempi elementari;
- interpretare score, Hessiano e informazione di Fisher;
- stimare parametri in catene di Markov, processi di salto e SDE;
- distinguere stima, incertezza, diagnostica e goodness-of-fit;
- riconoscere casi in cui la likelihood è intrattabile.

## Dal problema diretto al problema inverso

Problema diretto:

$$
\theta
\quad \longrightarrow \quad
\text{modello probabilistico}
\quad \longrightarrow \quad
\text{dati}
$$

Problema inverso:

$$
\text{dati}
\quad \longrightarrow \quad
\text{stima di } \theta
$$

Domanda guida:

> Quali valori di $\theta$ rendono i dati osservati più plausibili sotto il modello?

## Parametro, dati, stimatore

Supponiamo di osservare

$$
x_1,x_2,\dots,x_n.
$$

Il modello contiene un parametro, o vettore di parametri,

$$
\theta \in \Theta.
$$

Uno **stimatore** è una funzione dei dati:

$$
\hat\theta=\hat\theta(x_1,\dots,x_n).
$$

Poiché i dati sono casuali, anche $\hat\theta$ è una variabile aleatoria.

## Criteri desiderabili

Uno stimatore dovrebbe essere:

- **consistente**: tende al parametro vero per $n\to\infty$;
- **non distorto**, almeno asintoticamente;
- **efficiente**: usa bene l'informazione disponibile;
- **robusto**: non cambia drasticamente per piccole perturbazioni;
- **numericamente stabile**: è calcolabile in modo affidabile.

La massima verosimiglianza fornisce un criterio generale per costruire stimatori.

# Likelihood e log-likelihood

## Likelihood

Per un singolo dato:

$$
p(x\mid \theta).
$$

Per un campione indipendente:

$$
p(x_1,\dots,x_n\mid\theta)
=
\prod_{i=1}^n p(x_i\mid\theta).
$$

Vista come funzione di $\theta$, a dati fissati, questa quantità è la **likelihood**:

$$
L(\theta)=\prod_{i=1}^n p(x_i\mid\theta).
$$

## Distribuzione o likelihood?

Attenzione alla distinzione:

- $p(x\mid\theta)$ è una distribuzione in $x$, a parametro fissato;
- $L(\theta)$ è una funzione di $\theta$, a dati fissati.

In generale $L(\theta)$ **non** è una distribuzione di probabilità su $\theta$.

Non deve integrare a uno rispetto a $\theta$.

## Perché il logaritmo?

La likelihood di dati indipendenti è un prodotto:

$$
L(\theta)=\prod_{i=1}^n p(x_i\mid\theta).
$$

Il logaritmo trasforma prodotti in somme:

$$
\ell(\theta)=\log L(\theta)
=
\sum_{i=1}^n \log p(x_i\mid\theta).
$$

Vantaggi:

- maggiore stabilità numerica;
- derivate più semplici;
- contributi additivi dei singoli dati.

## Negative log-likelihood

Massimizzare $\ell$ equivale a massimizzare $L$, perché $\log$ è monotono crescente.

Spesso si minimizza invece la **negative log-likelihood**:

$$
\mathcal{J}(\theta)=-\ell(\theta).
$$

La stima di massima verosimiglianza, MLE, è

$$
\hat\theta_{\mathrm{MLE}}
=
\arg\max_{\theta\in\Theta}\ell(\theta)
=
\arg\min_{\theta\in\Theta}\mathcal{J}(\theta).
$$

# Massima verosimiglianza

## Condizione del primo ordine

Se $\theta$ è scalare e il massimo è interno a $\Theta$:

$$
\frac{d\ell}{d\theta}(\hat\theta)=0.
$$

La derivata della log-likelihood è lo **score**:

$$
S(\theta)=\frac{d\ell}{d\theta}.
$$

Quindi:

$$
S(\hat\theta)=0.
$$

## Caso vettoriale

Se

$$
\theta=(\theta_1,\dots,\theta_d),
$$

lo score è il gradiente:

$$
S(\theta)=\nabla_\theta \ell(\theta).
$$

Per un massimo interno:

$$
\nabla_\theta \ell(\hat\theta)=0.
$$

Se il massimo cade sul bordo di $\Theta$, la condizione corretta è che non esista alcuna direzione ammissibile lungo cui $\ell$ aumenti al primo ordine.

## Condizione del secondo ordine

Caso scalare:

$$
\frac{d^2\ell}{d\theta^2}(\hat\theta)<0.
$$

Caso vettoriale:

$$
H(\theta)=\nabla_\theta^2\ell(\theta)
$$

deve essere definito negativo al massimo interno.

La curvatura non serve solo a verificare il massimo: contiene informazione sull'incertezza della stima.

# Esempi fondamentali

## Bernoulli

:::: {.columns}
::: {.column width="50%"}

Dati:

$$
x_i\in\{0,1\},
\qquad
P(X_i=1)=p.
$$

Likelihood:

$$
L(p)=\prod_{i=1}^n p^{x_i}(1-p)^{1-x_i}.
$$
:::
::: {.column width="50%"}

Se

$$
k=\sum_i x_i,
$$

allora

$$
\ell(p)=k\log p+(n-k)\log(1-p).
$$

MLE:

$$
\hat p=\frac{k}{n}.
$$
:::
::::

## Poisson

Dati:

$$
X_i\sim \mathrm{Poisson}(\lambda),
\qquad
P(X_i=x_i\mid\lambda)=\frac{\lambda^{x_i}e^{-\lambda}}{x_i!}.
$$

Log-likelihood:

$$
\ell(\lambda)
=
\left(\sum_i x_i\right)\log\lambda
-
n\lambda
+
\text{costante}.
$$

MLE:

$$
\hat\lambda=\frac{1}{n}\sum_{i=1}^n x_i.
$$

## Esponenziale

:::: {.columns}
::: {.column width="50%"}

Tempi di attesa indipendenti:

$$
p(t\mid\lambda)=\lambda e^{-\lambda t},
\qquad t\ge 0.
$$

Likelihood:

$$
L(\lambda)=\lambda^n e^{-\lambda\sum_i t_i}.
$$

:::
::: {.column width="50%"}

Log-likelihood:

$$
\ell(\lambda)=n\log\lambda-\lambda\sum_i t_i.
$$

MLE:

$$
\hat\lambda=\frac{n}{\sum_i t_i}=\frac{1}{\bar t}.
$$

:::
::::

## Gaussiana con varianza nota

Dati con $\sigma^2$ nota:

$$
X_i\sim\mathcal{N}(\mu,\sigma^2),
$$

Log-likelihood:

$$
\ell(\mu)
=
-\frac{n}{2}\log(2\pi\sigma^2)
-
\frac{1}{2\sigma^2}\sum_i(x_i-\mu)^2.
$$

MLE:

$$
\hat\mu=\bar x.
$$

## Gaussiana con media e varianza ignote

Se $\mu$ e $\sigma^2$ sono ignote:

$$
\hat\mu=\bar x.
$$

La MLE della varianza è

$$
\hat\sigma^2_{\mathrm{MLE}}
=
\frac{1}{n}\sum_{i=1}^n(x_i-\bar x)^2.
$$

Attenzione:

$$
s^2=
\frac{1}{n-1}\sum_{i=1}^n(x_i-\bar x)^2
$$

è invece lo stimatore non distorto della varianza.

# Score, Hessiano, Fisher

## Score e Hessiano

Score:

$$
S(\theta)=\nabla_\theta\ell(\theta).
$$

Hessiano:

$$
H(\theta)=\nabla_\theta^2\ell(\theta).
$$

Informazione osservata:

$$
\mathcal{I}_{\mathrm{obs}}(\hat\theta)
=
-H(\hat\theta).
$$

Il segno meno rende positiva la curvatura al massimo.

## Informazione di Fisher elementare

Per una singola osservazione $X$:

$$
s(x;\theta)=\nabla_\theta\log p(x\mid\theta).
$$

L'informazione di Fisher per singola osservazione è

$$
I_1(\theta)
=
\mathbb{E}_\theta[
s(X;\theta)s(X;\theta)^T
].
$$

Qui $s\,s^T$ è un prodotto esterno: se $\theta\in\mathbb{R}^d$, allora $I_1$ è una matrice $d\times d$.

## Interpretazione geometrica

Per una direzione unitaria $u$:

$$
u^T I_1(\theta)u
=
\mathbb{E}_\theta[
(u^T s(X;\theta))^2
].
$$

Quindi $u^T I_1u$ misura il valore medio del quadrato della componente dello score lungo $u$.

- grande: la distribuzione cambia molto lungo $u$;
- piccolo: il parametro è poco identificabile lungo $u$.

## Identità con l'Hessiano medio

Sotto condizioni regolari:

$$
I_1(\theta)
=
-\mathbb{E}_\theta[
\nabla_\theta^2\log p(X\mid\theta)
].
$$

Idea della dimostrazione:

$$
\mathbb{E}_\theta[s_i]
=
\int \frac{\partial p(x\mid\theta)}{\partial\theta_i}\,dx
=
\frac{\partial}{\partial\theta_i}
\int p(x\mid\theta)\,dx
=
0.
$$

Derivando ancora:

$$
\mathbb{E}_\theta[s_i s_j]
=
-
\mathbb{E}_\theta
\left[
\frac{\partial^2}{\partial\theta_j\partial\theta_i}
\log p(X\mid\theta)
\right].
$$

## Informazione del campione

Per un campione indipendente:

$$
\ell_n(\theta)=\sum_{k=1}^n\log p(X_k\mid\theta).
$$

Score totale:

$$
S_n(\theta)=\nabla_\theta \ell_n(\theta)
=
\sum_{k=1}^n s(X_k;\theta).
$$

Informazione totale:

$$
I_n(\theta)
=
\mathbb{E}_\theta[S_nS_n^T].
$$

(nel caso i.i.d.: $I_n(\theta)=nI_1(\theta).$)

# Incertezza della stima

## Approssimazione quadratica

Vicino al massimo:

$$
\ell_n(\theta)
\approx
\ell_n(\hat\theta)
-
\frac{1}{2}
(\theta-\hat\theta)^T
\mathcal{I}_{\mathrm{obs}}(\hat\theta)
(\theta-\hat\theta).
$$

Se la curvatura è grande, il massimo è ben localizzato.

Se la curvatura è piccola, la log-likelihood è piatta e la stima è incerta.

## Varianza asintotica

Per campioni grandi:

$$
\hat\theta_{\mathrm{MLE}}
\approx
\mathcal{N}
\left(
\theta_0,
I_n(\theta_0)^{-1}
\right).
$$

Nel caso i.i.d.:

$$
I_n(\theta_0)=nI_1(\theta_0),
$$

quindi

$$
\hat\theta_{\mathrm{MLE}}
\approx
\mathcal{N}
\left(
\theta_0,
\frac{1}{n}I_1(\theta_0)^{-1}
\right).
$$

## Covarianza dello stimatore

In pratica $\theta_0$ non è noto.

Si usa la curvatura osservata nel punto stimato:

$$
\mathcal{I}_{\mathrm{obs}}(\hat\theta)
=
-\nabla_\theta^2\ell_n(\hat\theta).
$$

La covarianza stimata dello stimatore è

$$
\widehat{\mathrm{Cov}}(\hat\theta)
\approx
\mathcal{I}_{\mathrm{obs}}(\hat\theta)^{-1}.
$$

Non è la covarianza dei dati: è l'incertezza sui parametri stimati.

# Interpretazione informazionale

## Distribuzione empirica e modello

Per semplicità consideriamo esiti discreti.

I dati definiscono una distribuzione empirica

$$
p_{\mathrm{data}}(x)
=
\frac{1}{n}
\sum_{i=1}^n \mathbf{1}_{x_i=x}.
$$

Il modello assegna una distribuzione teorica

$$
q_\theta(x).
$$

Allora

$$
\frac{1}{n}\ell(\theta)
=
\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

## Cross-entropia

La negative log-likelihood media è

$$
-\frac{1}{n}\ell(\theta)
=
-\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Questa è la cross-entropia:

$$
H(p_{\mathrm{data}},q_\theta)
=
-\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Interpretazione: sorpresa media dei dati se usiamo il modello $q_\theta$.

## Divergenza KL

La divergenza di Kullback--Leibler nasce come eccesso di sorpresa:

$$
D_{\mathrm{KL}}(p\|q)
=
H(p,q)-H(p).
$$

Equivalentemente:

$$
D_{\mathrm{KL}}(p\|q)
=
\sum_x p(x)\log\frac{p(x)}{q(x)}.
$$

È una divergenza, in generale non è una distanza:

$$
D_{\mathrm{KL}}(p\|q)\neq D_{\mathrm{KL}}(q\|p)
$$

## MLE come minimizzazione della KL

Nel nostro caso:

$$
p=p_{\mathrm{data}},
\qquad
q=q_\theta.
$$

Allora:

$$
D_{\mathrm{KL}}(p_{\mathrm{data}}\|q_\theta)
=
\sum_x p_{\mathrm{data}}(x)\log p_{\mathrm{data}}(x)
-
\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Il primo termine non dipende da $\theta$.

Quindi:

$$
\hat\theta_{\mathrm{MLE}}
=
\arg\max_\theta \ell(\theta)
=
\arg\min_\theta
D_{\mathrm{KL}}(p_{\mathrm{data}}\|q_\theta).
$$

# Dati dipendenti e traiettorie

## Likelihood di traiettoria

Per una traiettoria markoviana a tempo discreto:

$$
x_0,x_1,\dots,x_T,
$$

la probabilità si fattorizza come

$$
P(x_0,\dots,x_T\mid\theta)
=
P(x_0\mid\theta)
\prod_{t=0}^{T-1}
P(x_{t+1}\mid x_t,\theta).
$$

La log-likelihood è

$$
\ell(\theta)
=
\log P(x_0\mid\theta)
+
\sum_{t=0}^{T-1}
\log P(x_{t+1}\mid x_t,\theta).
$$

## Catena di Markov discreta

:::: {.columns}
::: {.column width="50%"}

Matrice di transizione:

$$
P_{ij}(\theta)
=
P(X_{t+1}=j\mid X_t=i,\theta).
$$

Conteggi di transizione:

$$
N_{ij}
=
\#\{t:x_t=i,\ x_{t+1}=j\}.
$$

:::
::: {.column width="50%"}

Log-likelihood:

$$
\ell(\theta)=\sum_{i,j}N_{ij}\log P_{ij}(\theta).
$$

Se ogni riga è libera:

$$
\hat P_{ij}
=
\frac{N_{ij}}{\sum_k N_{ik}}.
$$

:::
::::

## Dipendenza e informazione effettiva

Quando i dati sono dipendenti, $N$ osservazioni non equivalgono a $N$ dati indipendenti.

L'autocorrelazione riduce l'informazione effettiva.

Conseguenze:

- errori standard troppo ottimistici;
- sovrastima dell'informazione nei dati;
- diagnostica necessaria su autocorrelazione e mixing.

# Processi di salto

## Tassi di transizione

Consideriamo un processo markoviano a tempo continuo con stati discreti.

Tassi:

$$
w_{i\to j}(\theta).
$$

Tasso totale di uscita da $i$:

$$
r_i(\theta)=\sum_{j\ne i}w_{i\to j}(\theta).
$$

Tempo di permanenza in $i$:

$$
p(\tau\mid i)=r_i e^{-r_i\tau}.
$$

## Likelihood elementare

Probabilità che il salto sia verso $j$:

$$
\frac{w_{i\to j}}{r_i}.
$$

Densità congiunta: permanenza $\tau$ in $i$ e salto $i\to j$:

$$
r_i e^{-r_i\tau}
\frac{w_{i\to j}}{r_i}
=
w_{i\to j}e^{-r_i\tau}.
$$

Likelihood elementare:

$$
L_{i\to j}(\theta;\tau)
=
w_{i\to j}(\theta)e^{-r_i(\theta)\tau}.
$$

## Traiettoria completa

Se la traiettoria è composta da tratti

$$
(i_0,\tau_0,i_1),\dots,(i_{M-1},\tau_{M-1},i_M),
$$

allora

$$
L(\theta)
=
\prod_{m=0}^{M-1}
w_{i_m\to i_{m+1}}(\theta)
e^{-r_{i_m}(\theta)\tau_m}.
$$

Raggruppando:

$$
L(\theta)
=
\prod_{i\ne j}
w_{i\to j}(\theta)^{N_{ij}}
\exp\left[
-\sum_i T_i r_i(\theta)
\right].
$$

## Log-likelihood e stima dei tassi

:::: {.columns}
::: {.column width="50%"}

Log-likelihood:

$$
\ell(\theta)
=
\sum_{i\ne j}
N_{ij}\log w_{i\to j}(\theta)
-
\sum_i T_i r_i(\theta).
$$

Se i tassi sono liberi:

$$
r_i=\sum_{j\ne i}w_{i\to j}.
$$

:::
::: {.column width="50%"}

Allora

$$
\frac{\partial\ell}{\partial w_{i\to j}}
=
\frac{N_{ij}}{w_{i\to j}}
-
T_i.
$$

MLE:

$$
\hat w_{i\to j}
=
\frac{N_{ij}}{T_i}.
$$

:::
::::

# SDE osservate a tempi discreti

## Euler--Maruyama come likelihood approssimata

:::: {.columns}
::: {.column width="45%"}

SDE:

$$
dX_t=a(X_t,\theta)dt+b(X_t,\theta)dW_t.
$$

Per piccoli $\Delta t$:

$$
X_{k+1}
\approx
X_k+a(X_k,\theta)\Delta t
+
b(X_k,\theta)\sqrt{\Delta t}\xi_k,
$$

con

$$
\xi_k\sim\mathcal{N}(0,1).
$$

:::
::: {.column width="55%"}

Quindi:

$$
X_{k+1}\mid X_k=x_k
\approx
\mathcal{N}
\left(
x_k+a(x_k,\theta)\Delta t,
b(x_k,\theta)^2\Delta t
\right).
$$

:::
::::

## Log-likelihood approssimata

La log-likelihood approssimata è

$$
\ell(\theta)
\approx
-\frac{1}{2}
\sum_{k=0}^{N-1}
\left[
\log(2\pi b_k^2\Delta t)
+
\frac{
(x_{k+1}-x_k-a_k\Delta t)^2
}{
b_k^2\Delta t
}
\right],
$$

dove

$$
a_k=a(x_k,\theta),
\qquad
b_k=b(x_k,\theta).
$$

## Drift come regressione sugli incrementi

Se $b(x,\theta)=\sigma$ è nota e costante:

$$
\Delta x_k
=
a(x_k,\theta)\Delta t
+
\sigma\sqrt{\Delta t}\xi_k.
$$

Gli incrementi osservati $\Delta x_k$ sono la variabile risposta.

La previsione del modello è

$$
a(x_k,\theta)\Delta t.
$$

La MLE minimizza

$$
\sum_k
[
\Delta x_k-a(x_k,\theta)\Delta t
]^2.
$$

## Ornstein--Uhlenbeck

:::: {.columns}
::: {.column width="50%"}

SDE:

$$
dX_t=-\gamma X_t\,dt+\sigma dW_t.
$$

Euler--Maruyama:

$$
\Delta x_k
=
-\gamma x_k\Delta t
+
\sigma\sqrt{\Delta t}\xi_k.
$$

:::
::: {.column width="50%"}

Se $\sigma$ è nota:

$$
Q(\gamma)=
\sum_k(\Delta x_k+\gamma x_k\Delta t)^2.
$$

MLE approssimata:

$$
\hat\gamma
=
-\frac{\sum_k x_k\Delta x_k}
{\Delta t\sum_k x_k^2}.
$$

:::
::::

## Nota sul propagatore esatto

Per Ornstein--Uhlenbeck il propagatore esatto è noto:

$$
X_{k+1}\mid X_k=x_k
\sim
\mathcal{N}
\left(
x_ke^{-\gamma\Delta t},
\frac{\sigma^2}{2\gamma}(1-e^{-2\gamma\Delta t})
\right).
$$

Quindi si può costruire una likelihood esatta della traiettoria discretamente osservata.

Per $\Delta t$ piccolo si recupera Euler--Maruyama; per $\Delta t$ non infinitesimo il propagatore esatto è preferibile.

# Diagnostica e confronto modello-dati

## Problemi tipici

La stima non basta: serve diagnostica.

Patologie frequenti:

- parametri non identificabili;
- massimi locali;
- vincoli ignorati;
- underflow nella likelihood;
- dati correlati trattati come indipendenti;
- overfitting.

## Identificabilità

Un parametro è identificabile se valori diversi producono distribuzioni osservabili diverse.

Se

$$
p(x\mid\theta_1)=p(x\mid\theta_2),
$$

allora nessun metodo può distinguere $\theta_1$ da $\theta_2$ usando quei dati.

Segnali:

- log-likelihood piatta;
- Hessiano quasi singolare;
- forti correlazioni tra parametri;
- stime instabili.

## Goodness-of-fit

Dopo aver stimato $\hat\theta$:

> Il modello con parametro $\hat\theta$ riproduce le proprietà statistiche rilevanti dei dati?

Strumenti:

- QQ-plot;
- test KS, con cautela se i parametri sono stimati dagli stessi dati;
- confronto tra dati osservati e simulati;
- residui trasformati per processi puntuali;
- AIC e BIC per confronto tra modelli.

## Residui trasformati

Per eventi ai tempi $t_k$ con intensità condizionata stimata $\lambda_{\hat\theta}^*(t)$:

$$
\tau_k
=
\int_0^{t_k}
\lambda_{\hat\theta}^*(s)\,ds.
$$

Questa variabile è adimensionale: è il numero atteso cumulativo di eventi fino a $t_k$.

Se il modello è corretto:

$$
z_k=\tau_k-\tau_{k-1}
\sim
\mathrm{Exp}(1).
$$

Quindi si può usare un QQ-plot contro una esponenziale standard.

## AIC e BIC

Un modello con più parametri tende ad avere likelihood più alta.

Criteri penalizzati:

$$
\mathrm{AIC}
=
2k-2\ell(\hat\theta),
$$

$$
\mathrm{BIC}
=
k\log n-2\ell(\hat\theta).
$$

Valori più bassi indicano un compromesso migliore tra adattamento e complessità.

# Likelihood intrattabile

## Quando la likelihood non si calcola

La likelihood può essere intrattabile quando:

- ci sono variabili latenti;
- si osservano solo statistiche aggregate;
- lo spazio degli stati è enorme;
- il modello è agent-based;
- la dinamica è simulabile ma la densità dei dati non è nota.

Idea generale:

> se non posso calcolare la probabilità dei dati, posso simulare il modello e confrontare dati simulati e osservati.

## Metodo dei momenti simulati

Sia $m_{\mathrm{obs}}$ un vettore di statistiche osservate.

Per ogni $\theta$, simuliamo il modello e calcoliamo

$$
m_{\mathrm{sim}}(\theta).
$$

Scegliamo $\theta$ minimizzando

$$
\hat\theta_{\mathrm{SMM}}
=
\arg\min_\theta
[m_{\mathrm{obs}}-m_{\mathrm{sim}}(\theta)]^T
W
[m_{\mathrm{obs}}-m_{\mathrm{sim}}(\theta)].
$$

Il punto cruciale è la scelta delle statistiche.

## Approximate Bayesian Computation

ABC è un approccio bayesiano per modelli simulabili con likelihood intrattabile.

Schema rejection:

1. estrai $\theta\sim p(\theta)$;
2. simula $y_{\mathrm{sim}}\sim p(\cdot\mid\theta)$;
3. calcola $s(y_{\mathrm{sim}})$ e $s(y_{\mathrm{obs}})$;
4. accetta $\theta$ se

$$
d(s(y_{\mathrm{sim}}),s(y_{\mathrm{obs}}))
\le \varepsilon.
$$

I parametri accettati approssimano la posteriore.

## Il ruolo di $\varepsilon$

La soglia $\varepsilon$ controlla la tolleranza.

- $\varepsilon$ piccolo: approssimazione più accurata, accettazione rara;
- $\varepsilon$ grande: più accettazioni, posteriore meno informativa.

ABC conclude il percorso:

1. likelihood esplicita -- MLE;
2. likelihood approssimata -- Euler--Maruyama;
3. likelihood intrattabile -- simulazione, SMM, ABC.

# Sintesi

## Messaggi finali

La log-likelihood è lo strumento operativo centrale perché:

- trasforma prodotti in somme;
- evita instabilità numeriche;
- permette ottimizzazione e derivate;
- collega inferenza, entropia e KL.

La MLE produce stimatori naturali:

- frequenze empiriche;
- medie campionarie;
- tassi evento/tempo;
- parametri di drift e diffusione.

## Dai dati indipendenti ai modelli dinamici

Per dati indipendenti:

$$
\ell(\theta)=\sum_i\log p(x_i\mid\theta).
$$

Per traiettorie dinamiche:

$$
\ell(\theta)=
\log P(x_0\mid\theta)
+
\sum_t\log P(x_{t+1}\mid x_t,\theta).
$$

Nei modelli continui:

- processi di salto: likelihood da tempi di permanenza e salti;
- SDE: likelihood approssimata o propagatore esatto.

## Ultimo messaggio

La stima parametrica non è solo calcolo di una formula.

Richiede:

- costruzione corretta della likelihood;
- gestione dei vincoli;
- stima dell'incertezza;
- diagnostica modello-dati;
- attenzione a dipendenza, autocorrelazione e simulazione.

Nei modelli complessi, l'inferenza non è separata dalla simulazione: spesso passa proprio attraverso di essa.

# Esercizi

## Esercizi proposti

1. Bernoulli: derivare $\hat p=k/n$.
2. Poisson: stimare $\lambda$ da conteggi osservati.
3. Esponenziale: stimare $\lambda=1/\bar t$.
4. Catena di Markov: stimare $\hat P_{ij}$ dai conteggi.
5. Processo di salto: stimare $\hat w_{i\to j}=N_{ij}/T_i$.
6. SDE lineare: derivare la MLE approssimata di $\gamma$.
7. Diagnostica: interpretare un Hessiano quasi singolare.
8. Goodness-of-fit: costruire un QQ-plot.
9. Momenti simulati: scegliere statistiche informative.
10. ABC: discutere il ruolo di $\varepsilon$.
