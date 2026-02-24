---
title: "Introduzione ai modelli stocastici (Lezione 00)"
author: "Antonio Scala"
date: "24 Feb 2026"
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
---

# Obiettivi e struttura

## Obiettivi didattici specifici
- Distinguere tra modelli deterministici e stocastici
- Comprendere variabile aleatoria e distribuzione di probabilità
- Riconoscere principali classi di processi stocastici
- Interpretare ruolo di rumore e fluttuazioni nei sistemi dinamici
- Comprendere importanza dei metodi numerici (Monte Carlo, simulazioni)

## Struttura della lezione
1. Motivazioni e concetti fondamentali
2. Variabili aleatorie e distribuzioni di probabilità
3. Processi stocastici e proprietà
4. Rumore e media: dal determinismo alla fluttuazione
5. Modellizzazione stocastica: equazioni e interpretazioni

# Motivazioni e concetti fondamentali

## Perché introdurre la casualità nei modelli
- Nei modelli deterministici, stessi stati iniziali $\Rightarrow$ stesso esito
- Nei modelli stocastici si introducono variabili casuali per rappresentare:
  - incertezza intrinseca del fenomeno
  - fluttuazioni osservate
  - eventi aleatori che influenzano l'evoluzione

## Esempi applicativi (motivazione)
- Moto browniano
- Fluttuazioni di popolazione in biologia
- Volatilità dei mercati finanziari

## Descrizione probabilistica
Un modello stocastico fornisce una descrizione probabilistica dello stato del sistema:
- leggi di transizione
- proprietà statistiche del processo
- grandezze d'interesse: medie, varianze, autocorrelazioni, tempi di primo passaggio

# Variabili aleatorie e distribuzioni di probabilità

## Definizione di variabile aleatoria
Una variabile aleatoria $X$ è una funzione:
$$
X:\Omega \to \mathbb{R}, \quad X(\omega)\in \mathbb{R},
$$
definita su uno spazio di probabilità $(\Omega,\mathcal{F},P)$.

## Oggetti fondamentali
- Funzione di probabilità $P(x)$ (discreta) o densità $p(x)$ (continua)
- Funzione di distribuzione cumulativa:
$$
F(x) = P(X \le x)
$$
- Momenti:
$$
\langle X^n\rangle=\sum_x x^n P(x) \quad \text{(discreta)}, \qquad
\langle X^n\rangle=\int x^n p(x)\,dx \quad \text{(continua)}
$$
- Varianza:
$$
\sigma^2 = \langle X^2\rangle - \langle X\rangle^2
$$

## Normalizzazione
$$
\sum_x P(x)=1 \quad \text{(discreta)}, \qquad
\int_{-\infty}^{\infty} p(x)\,dx = 1 \quad \text{(continua)}.
$$

# Distribuzioni canoniche: discrete

## Variabili discrete: esempi
- Bernoulli:
$$
P(X=1)=p,\quad P(X=0)=1-p
$$
- Binomiale:
$$
P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}
$$
- Poisson:
$$
P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}
$$
Nel caso Poissoniano:
$$
\langle X\rangle = \lambda = \sigma^2
$$

# Distribuzioni canoniche: continue

## Variabili continue: esempi
- Uniforme in $[a,b]$:
$$
p(x)=\frac{1}{b-a}
$$
- Esponenziale ($x\ge 0$):
$$
p(x)=\lambda e^{-\lambda x}
$$
- Normale (Gaussiana):
$$
p(x)=\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

## Teorema del limite centrale (idea)

- Sia $X_1,\ldots,X_n$ i.i.d., $\langle X\rangle=\mu$, $\mathrm{Var}(X)=\sigma^2<\infty$.
$$
S_n=\sum_{i=1}^n X_i
$$
- Per $n\gg 1$: $S_n \approx N(n\mu,\,n\sigma^2)$.
- Fluttuazioni tipiche: $\mathrm{std}(S_n)=\sigma\sqrt{n}$.

# Proprietà statistiche fondamentali

## Linearità della media
$$
\langle aX + bY\rangle = a\langle X\rangle + b\langle Y\rangle
$$
* Vale sempre (non richiede indipendenza).

## Varianza e covarianza
* fluttuazioni
$$ 
\mathrm{def:} \quad \Delta X = X - \langle X \rangle, \quad \Delta Y = Y - \langle Y \rangle
$$
* varianza / covarianza
$$
\mathrm{Var(X)}\,=\,\langle \Delta X^2 \rangle  \qquad
$$
$$
\mathrm{Cov(X,Y)}\,=\, \langle \Delta X \Delta Y \rangle \,=\, \langle X Y \rangle \,-\, \langle X \rangle \langle Y \rangle
$$

* varianza di una combinazione lineare
$$
\mathrm{Var}(aX+bY) = a^2\mathrm{Var}(X)+b^2\mathrm{Var}(Y)+2ab\,\mathrm{Cov}(X,Y)
$$
* Caso indipendente: $\mathrm{Cov}(X,Y)=0$.

## Funzione caratteristica
$$
\phi_X(k)=\langle e^{ikX}\rangle = \int e^{ikx}p(x)\,dx
$$
Per somme di variabili indipendenti:
$$
\phi_{X+Y}(k)=\phi_X(k)\phi_Y(k)
$$

# Dalla teoria alla simulazione

## Generazione di campioni: metodo dell'inversione
Dato un generatore uniforme $U\in[0,1)$, definiamo
$$
X = F^{-1}(U)
$$
dove $F$ è la distribuzione cumulativa della distribuzione $p=F´$ che vogliamo generare.

$$u=F(x) \rightarrow p_X(x) = F'(x) = p(x)$$
quindi per generare numeri distribuiti secondo $p(x)$, devo essere in grado di (a) di costruire (anche numericamente) una $F(x)=\int^x p(y)dy$; (b) generare numeri $u$ uniformemente distribuiti; (c) implementare $F^{-1}$ in modo da trasformare $u$ in $x=F^{-1}(u)$

## Generazione di campioni: metodo dell'inversione

- Cambio di variabile:
$$
p_X(x)\,dx = p_U(u)\,du, \qquad du = F'(x)\,dx = p(x)\,dx.
$$
- Poiché $p_U(u)=1$ su $[0,1)$, segue:
$$
p_X(x)=p(x).
$$
* questa forma funziona quando $F$ è invertibile (monotona) e derivabile quasi ovunque; altrimenti si usa la dimostrazione via CDF:
  $$
  P(X\le x)=P(F^{-1}(U)\le x)=P(U\le F(x))=F(x)
  $$

## Esempi
- Esponenziale:
$$
X = -\frac{1}{\lambda}\ln(1-U)
$$
- Gaussiana: $F^{-1}$ non ha forma chiusa; si costruisce $Z\sim N(0,1)$ a partire da $U_1,U_2\sim\mathrm{Unif}[0,1)$.
    - Box--Muller:
$$
Z_1=\sqrt{-2\ln U_1}\cos(2\pi U_2),\qquad\
Z_2=\sqrt{-2\ln U_1}\sin(2\pi U_2).\
$$
    - Marsaglia (polar): stessa idea, evita $\sin/\cos$ (accetta/rifiuta in un disco).

## Collegamento con lezioni successive
- Generare campioni con una legge assegnata $\Rightarrow$ base dei metodi Monte Carlo.
- Stimare $\langle g(X)\rangle$ con medie campionarie e valutare l'errore statistico.
- Estensione: catene di Markov (MCMC) quando il campionamento diretto non è possibile.

# Processi stocastici: definizione e proprietà

## Definizione
Un processo stocastico è una famiglia di variabili aleatorie indicizzate:
$$
\{X(t)\}
$$
con $t$ (tipicamente) tempo.

## Caratteristiche principali
- Tempo discreto $t=0,1,2,\ldots$ o continuo $t\in\mathbb{R}^+$
- Spazio degli stati discreto o continuo
- Dipendenza temporale (correlazioni)

## Caso fondamentale: Markov
$$
P(X_{t+1}\mid X_t,X_{t-1},\ldots)=P(X_{t+1}\mid X_t)
$$
- Il futuro dipende dal passato solo tramite lo stato presente $X_t$.
- Tempo discreto: matrice di transizione $P_{ij}=P(X_{t+1}=j\mid X_t=i)$.

# Rumore e media

## Dinamica con rumore
$$
x_{t+1}=f(x_t)+\eta_t
$$
- $f(x_t)$: parte deterministica; $\eta_t$: rumore (shock) casuale.
- Tipicamente $\langle \eta_t\rangle=0$ e $\mathrm{Var}(\eta_t)$ fissa l'intensità delle fluttuazioni.

## Esempi di rumore
- Rumore bianco:
$$
\langle \eta_t \eta_{t'} \rangle = 2D\,\delta_{t,t'}
$$
- Rumore colorato: correlato nel tempo (spettro non piatto)

## Medie ed ergodicità
- Media d'ensemble $\langle x(t)\rangle$
- Media temporale:
$$
\bar{x}_T=\frac{1}{T}\int_0^T x(t)\,dt
$$
- Ergodicità: uguaglianza tra media temporale e media statistica

# Modellizzazione stocastica e interpretazione

## Idea generale
Combinazione tra struttura deterministica e termini di rumore per rappresentare:

- fluttuazioni
- incertezze
- interazioni non risolte

## Fluttuazioni (intrinseche al fenomeno)

- Anche a condizioni controllate, l'esito varia: il modello descrive una *distribuzione*.
- Esempi:
  - conteggi di eventi rari (arrivi, click, guasti) -- variabilit\`a di conteggio;
  - fluttuazioni di traffico in rete (burstiness) attorno a un tasso medio.
- Struttura minima:
$$
\text{osservazione} = \text{segnale} + \text{rumore}.
$$

## Incertezze (parametri e dati)

- L'incertezza è in ciò che stimiamo: dati incompleti, misure imperfette, stime instabili.
- Esempi:
  - epidemiologia: tasso di trasmissione $\beta$ stimato da dati parziali;
  - economia: elasticità o trend stimati con intervalli ampi.
- Idea: parametri come variabili aleatorie:
$$
x_{t+1}=f(x_t;\theta), \qquad \theta \, \text{incerto}.
$$

## Interazioni non risolte (coarse-graining)

- Si modellano poche variabili; il resto viene assorbito in un termine efficace.
- Esempio (bagno termico): urti microscopici $\Rightarrow$ attrito + rumore
$$
\dot x = f(x)-\gamma x+\eta(t), \qquad \langle \eta(t)\rangle=0.
$$
- Esempio (trasmissione): interferenze e disturbi aggregati $\Rightarrow$ rumore additivo $\eta(t)$ sul segnale ricevuto.

## Formalismi principali: traiettorie e distribuzioni

- **Catena di Markov** (tempo discreto): traiettorie su stati discreti, con probabilit\`a di transizione.
- **Langevin** (tempo continuo): traiettorie su stati continui, con rumore.
- **Master equation**: evoluzione di $P(x,t)$ per stati discreti (tassi di transizione).
- **Fokker--Planck**: evoluzione di $p(x,t)$ per stati continui (limite diffusive).

- Tutti descrivono la *stessa informazione* (la legge del processo), ma in rappresentazioni diverse:
  - traiettorie $x(t)$ vs distribuzioni $p(x,t)$;
  - descrizione microscopica (transizioni) vs descrizione efficace (drift/diffusione).
- Alcune quantit\`a risultano pi\`u immediate in una forma che in un'altra (es. campionamento vs calcolo di $p(x,t)$).

# Esempi interdisciplinari (panoramica)

## Ambiti applicativi (esempi)

- Fisica: diffusione/trasporto, rumore termico.
- Biologia: dinamiche di popolazione, reazioni stocastiche.
- Finanza/Economia: prezzi, rischio/volatilit\`a.
- Ingegneria/Informatica: code, reti di comunicazione, affidabilit\`a.
- Scienze sociali/Comunicazione: diffusione di informazione/opinioni, adozione.
- Epidemiologia: contagi come processi di transizione (SIR stocastico).
- Neuroscienze: spike trains, rumore sinaptico.
- Ecologia/Ambiente: estinzioni, invasioni, variabilità climatica come rumore esogeno.
- Chimica/Materiali: cinetica di reazione e nucleazione (eventi rari, first-passage).

# Chiusura e raccordo

## What comes next

- Prima di introdurre il rumore in modo sistematico, fissiamo la base: modelli deterministici e loro dinamica.
- Per distinguere chiaramente
  - cosa produce la *struttura deterministica* (punti fissi, stabilità, attrattori, ...)
  - cosa aggiunge la *componente stocastica* $\eta_t$ (dispersione, probabilità di eventi rari, ...)
-  ripartiamo dai modelli deterministici continui e discreti
-  vedremo che un modello continuo va sempre discretizzato per essere simulato
-  osserveremo come la discretizzazione introduce un nuovo tipo di rumore, quello numerico
