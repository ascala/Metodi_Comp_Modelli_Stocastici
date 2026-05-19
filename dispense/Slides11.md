---
title: "S11 -- Paesaggi di energia e modelli generativi"
author: "Antonio Scala"
date: ""
subtitle: "Metodi computazionali per modelli stocastici"
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

# Apertura

## Obiettivo della lezione

Una funzione di costo, energia o loss può essere usata non solo per scegliere una configurazione, ma anche per definire una distribuzione di probabilità.

$$
E(x)
\quad \longrightarrow \quad
p(x) = \frac{e^{-\beta E(x)}}{Z}
$$

**Idea centrale**

- stati a bassa energia $\rightarrow$ più probabili;
- stati ad alta energia $\rightarrow$ meno probabili;
- generare significa campionare dalla distribuzione definita dall'energia.

## Il filo conduttore

$$
\text{costo/loss}
\quad \longrightarrow \quad
\text{energia}
\quad \longrightarrow \quad
\text{distribuzione}
\quad \longrightarrow \quad
\text{modello generativo}
$$

Nella lezione useremo questo filo per collegare:

- energy-based models;
- reti di Hopfield;
- Boltzmann Machines;
- Gibbs sampling;
- contrastive divergence;
- Hamiltonian Monte Carlo.

## Tre problemi diversi

Una stessa energia può essere letta in tre modi.

| Lettura | Domanda | Oggetto |
|---|---|---|
| Ottimizzazione | qual è la configurazione migliore? | $\arg\min_x E(x)$ |
| Campionamento | quali configurazioni sono tipiche? | $p(x)\propto e^{-E(x)}$ |
| Generazione | come produrre nuovi esempi plausibili? | $p_\theta(x)$ appresa dai dati |

Questa lezione si concentra soprattutto sulle ultime due letture.

# 1. Da costo a probabilità

## Una funzione energia

Sia $\mathcal{X}$ uno spazio di configurazioni.

Una configurazione $x\in\mathcal{X}$ può essere:

- un vettore continuo;
- una configurazione binaria;
- una sequenza;
- una rete;
- un insieme di parametri;
- uno stato collettivo.

Introduciamo una funzione

$$
E:\mathcal{X}\to\mathbb{R}.
$$

Un valore basso di $E(x)$ indica maggiore compatibilità con modello, dati o vincoli.

## Pesi non normalizzati

A ogni configurazione associamo un peso positivo:

$$
\widetilde p(x)=e^{-\beta E(x)}.
$$

La tilde ricorda che non è ancora una probabilità normalizzata.

**Proprietà**

$$
\widetilde p(x)>0.
$$

Se $E(x)<E(y)$, allora

$$
\widetilde p(x)>\widetilde p(y).
$$

Diminuire l'energia aumenta la plausibilità relativa.

## Rapporti di probabilità

Il rapporto tra due pesi è

$$
\frac{\widetilde p(x)}{\widetilde p(y)}
=
\exp[-\beta(E(x)-E(y))].
$$

Quindi contano le **differenze di energia**, non il valore assoluto.

Se aggiungiamo una costante $c$ a tutte le energie,

$$
E'(x)=E(x)+c,
$$

i rapporti non cambiano.

L'energia definisce una scala relativa di plausibilità.

## Normalizzazione

Per ottenere una probabilità dividiamo per il peso totale.

Caso discreto: $Z=\sum_{x\in\mathcal{X}} e^{-\beta E(x)}.$

Caso continuo: $Z=\int_{\mathcal{X}} e^{-\beta E(x)}\,dx.$

Quindi

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

$Z$ è la **funzione di partizione**.

## Il ruolo di $\beta$

Il parametro $\beta$ controlla quanto la distribuzione è sensibile alle differenze di energia.

- $\beta=0$: tutti i pesi sono uguali;
- $\beta$ piccolo: distribuzione diffusa;
- $\beta$ grande: distribuzione concentrata sugli stati a bassa energia.

Spesso si introduce una temperatura $T$:

$$
\beta=\frac{1}{T}.
$$

Temperatura alta $\rightarrow$ distribuzione più diffusa.

Temperatura bassa $\rightarrow$ distribuzione più selettiva.

# 2. Boltzmann e funzione di partizione

## Distribuzione di Boltzmann

La forma

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}
$$

è la distribuzione di Boltzmann--Gibbs.

In questa lezione la usiamo in senso generale:

> una funzione energia definisce una distribuzione su configurazioni.

La formula separa due oggetti:

- $E(x)$: quantità locale, valutabile su una configurazione;
- $Z$: quantità globale, dipendente da tutto lo spazio.

## Perché $Z$ è globale

L'energia è locale rispetto allo stato:

$$
E(x) \quad \text{dipende dalla configurazione } x.
$$

La funzione di partizione è globale:

$$
Z=\sum_x e^{-\beta E(x)}
\quad \text{o} \quad
Z=\int e^{-\beta E(x)}\,dx.
$$

Deve sommare o integrare il peso di tutte le configurazioni.

Nei problemi realistici questa operazione può essere impossibile.

## Probabilità non normalizzate

Molti algoritmi usano solo rapporti:

$$
\frac{p(x)}{p(y)}
=
\frac{e^{-\beta E(x)}/Z}{e^{-\beta E(y)}/Z}
=
e^{-\beta(E(x)-E(y))}.
$$

La normalizzazione $Z$ si cancella.

Questo permette di usare la densità non normalizzata

$$
\widetilde p(x)=e^{-\beta E(x)}.
$$

Ma $Z$ torna centrale quando vogliamo likelihood, probabilità assolute o apprendimento dei parametri.

## Log-probabilità

Prendendo il logaritmo:

$$
\log p(x)=-\beta E(x)-\log Z.
$$

Due contributi:

- $-\beta E(x)$ dipende dalla configurazione osservata;
- $-\log Z$ dipende dall'intero modello.

Un modello non può rendere tutto molto probabile.

Se abbassa molte energie, aumenta anche $Z$.

La normalizzazione impone una competizione globale tra stati.

## Parametri e normalizzazione

Negli energy-based models:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

Con $Z_\theta=\sum_x e^{-E_\theta(x)} \quad \text{o} \quad Z_\theta=\int e^{-E_\theta(x)}\,dx.$

Cambiare $\theta$ modifica:

- l'energia dei dati;
- l'energia delle configurazioni non osservate;
- la normalizzazione $Z_\theta$.

L'apprendimento deve quindi agire in modo relativo, non assoluto.

# 3. Energy-based models

## Definizione

Un **energy-based model** definisce una distribuzione tramite una funzione energia parametrica:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

La forma è semplice ma generale. Possiamo rappresentare distribuzioni su:

- variabili continue;
- stati binari;
- immagini;
- reti;
- sequenze;
- variabili latenti;
- configurazioni collettive.

## Perché usare un'energia

Spesso è difficile scrivere direttamente una distribuzione normalizzata.

È più naturale costruire una funzione che misuri incompatibilità:

- immagine poco realistica;
- rete non coerente con certe proprietà;
- configurazione biologica instabile;
- stato sociale incompatibile con vincoli di interazione;
- parametro che spiega male i dati.

L'energia diventa una misura di implausibilità.

## Modello implicito

Un modello esplicito fornisce direttamente $p_\theta(x)$ normalizzata.

Un EBM fornisce prima un peso:

$$
\widetilde p_\theta(x)=e^{-E_\theta(x)}.
$$

Poi serve normalizzare:

$$
p_\theta(x)=\frac{\widetilde p_\theta(x)}{Z_\theta}.
$$

Il modello è quindi implicito:

- possiamo valutare pesi relativi;
- la probabilità assoluta richiede $Z_\theta$;
- campionamento e apprendimento diventano centrali.

## Generare campioni

Generare non significa trovare il minimo di $E_\theta(x)$.

Significa produrre configurazioni con frequenze coerenti con

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

Un modello generativo deve produrre varietà, non solo una configurazione ottima.

Se non sappiamo campionare da $p_\theta$, il modello è difficile da usare come generatore.

## Apprendere l'energia

Dato un dataset $\mathcal{D}=\{x^{(1)},\dots,x^{(n)}\},$ la log-likelihood è $\ell(\theta)=\sum_{i=1}^n \log p_\theta(x^{(i)}).$

Poiché $\log p_\theta(x)=-E_\theta(x)-\log Z_\theta,$ abbiamo

$$
\ell(\theta)=
-\sum_{i=1}^n E_\theta(x^{(i)})
-n\log Z_\theta.
$$

Il primo termine abbassa l'energia dei dati.

Il secondo impedisce di abbassare tutte le energie insieme.

## Dati contro modello

Il gradiente ha la struttura schematica

$$
\nabla_\theta \ell(\theta)
=
-\sum_i \nabla_\theta E_\theta(x^{(i)})
+n\,\mathbb{E}_{p_\theta}
\left[\nabla_\theta E_\theta(X)\right].
$$

Interpretazione:

- termine sui dati: rendere i dati più probabili;
- termine sul modello: correggere ciò che il modello genera.
$$\;$$

> Apprendere significa confrontare dati osservati e configurazioni prodotte dal modello.

# 4. Hopfield networks

## Memoria associativa

Una rete di Hopfield è un modello di memoria associativa.

Non archivia un pattern in un indirizzo preciso.

Distribuisce la memoria nei pesi di interazione tra unità.

Compito tipico:

$$
\text{pattern corrotto}
\quad \longrightarrow \quad
\text{pattern memorizzato}.
$$

La rete completa o corregge configurazioni iniziali rumorose.

## Stati binari e interazioni

Consideriamo $N$ unità binarie:

$$
s_i\in\{-1,+1\},
\qquad i=1,
\dots,N.
$$

Una configurazione è

$$
s=(s_1,\dots,s_N).
$$

I pesi soddisfano di solito $J_{ij}=J_{ji}\;,\;J_{ii}=0.$

La simmetria consente di definire un'energia "conservativa" (path independent).

## Energia di Hopfield

La funzione energia è

$$
E(s)=-\frac{1}{2}\sum_{i,j}J_{ij}s_i s_j
-\sum_i h_i s_i.
$$

Senza bias (in fisica *campo esterno*):

$$
E(s)=-\frac{1}{2}\sum_{i,j}J_{ij}s_i s_j.
$$

La dinamica aggiorna localmente gli stati in modo da ridurre, o almeno non aumentare, l'energia.

## Campo locale

Il campo locale sull'unità $i$ è

$$
H_i(s)=\sum_j J_{ij}s_j+h_i.
$$

Regola deterministica:

$$
s_i \leftarrow \mathrm{sign}\,H_i(s).
$$

Se $H_i>0$, si favorisce $s_i=+1$.

Se $H_i<0$, si favorisce $s_i=-1$.

Ogni unità si allinea al campo generato dalle altre.

## Aggiornamento asincrono

Schema essenziale:

```text
scegli una configurazione iniziale s
ripeti:
    scegli un indice i
    calcola H_i(s)
    poni s_i <- sign H_i(s)
fino a convergenza
```

Con pesi simmetrici e aggiornamento asincrono, l'energia non aumenta.

Quindi la dinamica converge verso una configurazione stabile.

L'energia agisce come funzione di Lyapunov.

## Attrattori e memorie

Una configurazione stabile soddisfa

$$
s_i=\mathrm{sign}\left(\sum_j J_{ij}s_j+h_i\right)
\qquad \forall i.
$$

Le configurazioni stabili sono attrattori.

Per memorizzare pattern

$$
\xi^\mu=(\xi_1^\mu,\dots,\xi_N^\mu),
\qquad \mu=1,\dots,P,
$$

si scelgono i pesi in modo che questi pattern diventino attrattori.

## Regola di Hebb

Una scelta classica è

$$
J_{ij}=\frac{1}{N}\sum_{\mu=1}^P \xi_i^\mu \xi_j^\mu,
\qquad i\neq j,
$$

con

$$
J_{ii}=0.
$$

Interpretazione:

- unità spesso concordi $\rightarrow$ peso positivo;
- unità spesso discordi $\rightarrow$ peso negativo.

Le correlazioni nei pattern vengono incorporate nelle interazioni.

## Memorie spurie e capacità

Le reti di Hopfield possono generare attrattori non voluti.

Sono le **memorie spurie**.

Origine:

- combinazioni dei pattern memorizzati;
- interferenze tra pattern;
- troppi pattern rispetto a $N$.

La memoria distribuita non è gratuita.

Gli stessi pesi devono codificare molti pattern e possono produrre strutture collettive inattese.

## Ponte verso Boltzmann Machines

Hopfield usa un'energia, ma nella forma classica non è un modello generativo probabilistico.

- dinamica deterministica;
- convergenza verso attrattori;
- obiettivo: recupero di memorie.

Per ottenere un modello probabilistico si introducono aggiornamenti stocastici.

Da

$$
s_i=\mathrm{sign}\,H_i(s)
$$

passiamo a probabilità condizionate per i valori di $s_i$.

# 5. Boltzmann Machines

## Dalla memoria alla distribuzione

Una Boltzmann Machine conserva:

- variabili binarie;
- interazioni;
- funzione energia.

Ma cambia interpretazione:

$$
p(s)=\frac{e^{-E(s)}}{Z}.
$$

Gli stati non sono solo attrattori, sono campioni da una distribuzione.

Una memoria associativa recupera un pattern.

Una Boltzmann Machine genera configurazioni plausibili.

## Variabili visibili e nascoste

Distinguiamo:

- variabili visibili $v$: osservate nei dati;
- variabili nascoste $h$: fattori latenti.

Lo stato completo è

$$
s=(v,h).
$$

Distribuzione congiunta: $p(v,h)=e^{-E(v,h)}/Z.$

Distribuzione osservabile: $p(v)=\sum_h p(v,h).$

Il dato visibile somma tutte le spiegazioni latenti compatibili.

## Energia generale

Una forma generale contiene bias e interazioni:

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a
-\frac{1}{2}\sum_{i,j} A_{ij}v_i v_j
-\frac{1}{2}\sum_{a,b} B_{ab}h_a h_b.
$$

Termini:

- bias visibili;
- bias nascosti;
- interazioni visibile--nascosto;
- interazioni tra visibili;
- interazioni tra nascosti.

## Restricted Boltzmann Machine

In una RBM restano solo interazioni visibile--nascosto:

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a.
$$

La struttura è bipartita.

Non ci sono interazioni:

- tra visibili;
- tra nascosti.

Conseguenza: le condizionate fattorizzano.

## Condizionate nella RBM

Qui $v$ e $h$ sono vettori:

$$
v=(v_1,\dots,v_n),
\qquad
h=(h_1,\dots,h_m).
$$

Nel caso RBM, le probabilità condizionate si fattorizzano:

$$
p(h\mid v)=\prod_a p(h_a\mid v),
$$

$$
p(v\mid h)=\prod_i p(v_i\mid h).
$$

Fissato $v$, le variabili nascoste sono indipendenti condizionatamente a $v$.

Fissato $h$, le variabili visibili sono indipendenti condizionatamente a $h$.

## Forma logistica

Per variabili $0/1$:

$$
p(h_a=1\mid v)=
\sigma\left(c_a+\sum_i W_{ia}v_i\right),
$$

$$
p(v_i=1\mid h)=
\sigma\left(b_i+\sum_a W_{ia}h_a\right),
$$

con

$$
\sigma(z)=\frac{1}{1+e^{-z}}.
$$

Queste formule rendono semplice il campionamento a blocchi.

## Campionamento alternato

Schema RBM:

```text
inizializza v
ripeti:
    campiona h da p(h | v)
    campiona v da p(v | h)
```

La catena alterna:

$$
v^{(0)} \to h^{(0)} \to v^{(1)} \to h^{(1)} \to \cdots
$$

Dopo un numero sufficiente di passi, le configurazioni visibili possono essere usate come campioni del modello.

## Positive e negative phase

L'apprendimento confronta:

- ciò che accade sui dati;
- ciò che il modello genera.

**Positive phase**

Riduce l'energia delle configurazioni compatibili con i dati.

**Negative phase**

Aumenta relativamente l'energia delle configurazioni generate troppo facilmente dal modello.

Questa tensione porta al problema computazionale centrale: stimare la fase negativa.

# 6. Gibbs sampling

## Idea generale

Vogliamo campionare da $p(x)=e^{-E(x)}/Z$ con $x=(x_1,\dots,x_N)$.

Invece di campionare direttamente da $p(x_1,\dots,x_N)$, aggiorniamo una variabile alla volta:

$$
p(x_i\mid x_{-i}).
$$

Gibbs sampling trasforma un problema globale difficile in molti problemi condizionati più semplici.

## Condizionate senza $Z$

La condizionata è

$$
p(x_i\mid x_{-i})=
\frac{p(x_i,x_{-i})}{\sum_{x_i'}p(x_i',x_{-i})}.
$$

Usando $p(x)=e^{-E(x)}/Z$:

$$
p(x_i\mid x_{-i})=
\frac{e^{-E(x_i,x_{-i})}}
{\sum_{x_i'}e^{-E(x_i',x_{-i})}}.
$$

La funzione di partizione globale si cancella.

Il denominatore somma solo sui valori possibili di $x_i$.

## Caso binario

Per $s_i\in\{-1,+1\}$ e

$$
E_i(s_i)=-s_iH_i
$$

si ottiene

$$p(s_i=+1\mid s_{-i})=\frac{1}{1+e^{-2H_i}}$$

Confronto:

- Hopfield deterministico: $s_i=\mathrm{sign}(H_i)$;
- Gibbs: $s_i$ viene campionato con probabilità dipendente da $H_i$.

## Gibbs a blocchi nelle RBM

Nelle RBM:

$$
p(h\mid v)=\prod_a p(h_a\mid v),
$$

$$
p(v\mid h)=\prod_i p(v_i\mid h).
$$

Quindi possiamo aggiornare blocchi interi:

```text
campiona tutti gli h_a dato v
campiona tutti i v_i dato h
```

Questo rende le RBM più trattabili delle Boltzmann Machines generali.

## Burn-in, autocorrelazione, mixing

Gibbs produce una catena di Markov.

I campioni successivi non sono indipendenti.

Tre concetti pratici:

- **burn-in**: scartare la fase iniziale (*termalizzazione*);
- **autocorrelazione**: campioni vicini sono simili;
- **mixing**: capacità della catena di esplorare regioni diverse.

Se il mixing è lento, la negative phase viene stimata male.

## Perché serve nell'apprendimento

Gibbs sampling compare in due modi:

1. generare campioni dal modello;
2. stimare la *negative phase*.

Il problema è che una stima corretta richiederebbe catene lunghe.

La *contrastive divergence* nasce come scorciatoia:

- inizializza la catena sui dati;
- esegue pochi passi di Gibbs;
- usa le ricostruzioni come confronto approssimato.

# 7. Apprendimento e problema di $Z$

## Log-likelihood energetica

Per un dataset $\mathcal{D}=\{x^{(1)},\dots,x^{(n)}\}$ la log-likelihood è

$$
\ell(\theta)=\sum_{i=1}^n\log p_\theta(x^{(i)}).
$$

Poiché $\log p_\theta(x)=-E_\theta(x)-\log Z_\theta$, segue

$$
\ell(\theta)=
-\sum_{i=1}^n E_\theta(x^{(i)})
-n\log Z_\theta.
$$

## Perché $\log Z_\theta$ è necessario

Senza il termine di normalizzazione, basterebbe abbassare tutte le energie.

Ma abbassare tutte le energie della stessa quantità non cambia la distribuzione normalizzata.

$\log Z_\theta$ rende l'apprendimento probabilistico:

- non basta rendere i dati meno energetici;
- bisogna renderli più probabili rispetto alle alternative.

Aumentare la probabilità di alcuni stati significa redistribuire massa di probabilità.

## Gradiente

Per un singolo dato:

$$
\nabla_\theta \log p_\theta(x)=
-\nabla_\theta E_\theta(x)
+\mathbb{E}_{p_\theta}
\left[\nabla_\theta E_\theta\right].
$$

Per il dataset:

$$
\nabla_\theta \ell(\theta)=
-\sum_{i=1}^n \nabla_\theta E_\theta(x^{(i)})
+n\,\mathbb{E}_{p_\theta}
\left[\nabla_\theta E_\theta\right].
$$

È il confronto tra dati e modello.

## Medie dati e medie modello

Definiamo

$$
\mathbb{E}_{data}[f(X)] = \frac{1}{n}\sum_{i=1}^n f(x^{(i)}).
$$

Allora

$$
\frac{1}{n}\nabla_\theta\ell(\theta)=
-\mathbb{E}_{data}\left[\nabla_\theta E_\theta(X)\right]
+\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta\right].
$$

La prima media è facile: abbiamo i dati.

La seconda è difficile: richiede campioni dal modello.

## Energia lineare nelle feature

Se

$$
E_\theta(x)=-\sum_k\theta_k f_k(x),
$$

allora

$$
\frac{1}{n}\frac{\partial\ell}{\partial\theta_k}=
\mathbb{E}_{data}[f_k(X)]-\mathbb{E}_{p_\theta}[f_k].
$$

L'apprendimento spinge verso

$$
\mathbb{E}_{p_\theta}[f_k(Y)] \approx \mathbb{E}_{data}[f_k(X)].
$$

Interpretazione: matching tra statistiche osservate e statistiche generate.

## Variabili nascoste e free energy

Per variabili visibili $v$ e nascoste $h$:

$$
p_\theta(v)=\sum_h p_\theta(v,h).
$$

Definiamo la free energy sommando le "spiegazioni latenti":

$$
F_\theta(v)=-\log\sum_h e^{-E_\theta(v,h)}.
$$

Allora

$$
p_\theta(v)=e^{-F_\theta(v)}/Z_\theta.
$$

La free energy è l'energia efficace delle variabili visibili.

## Il collo di bottiglia

Il termine difficile da calcolare è

$$
\mathbb{E}_{p_\theta}[g] = \sum_y g(y)p_\theta(y).
$$

Se lo spazio è grande, la somma è impraticabile.

La stimiamo con campioni:

$$
\mathbb{E}_{p_\theta}[g] \approx \frac{1}{M}\sum_{m=1}^M g(y^{(m)}),
\qquad
Y^{(m)}\sim p_\theta.
$$

Il simbolo $\sim$ significa “è distribuito secondo”.

Il problema dell'apprendimento diventa un problema di campionamento.

## Strategie

Tre possibilità:

1. **catene lunghe**: più accurate, ma costose;
2. **catene persistenti**: non ripartono da zero a ogni aggiornamento;
3. **catene brevi inizializzate sui dati**: idea alla base della contrastive divergence.

La contrastive divergence non è campionamento esatto.

È un'approssimazione pratica del gradiente quando la negative phase è troppo costosa.

# 8. Contrastive divergence

## Problema pratico

Il gradiente esatto richiede:

$$
\mathbb{E}_{data}[\cdot]
\qquad \text{e} \qquad
\mathbb{E}_{p_\theta}[\cdot].
$$

La media sui dati è disponibile.

La media sul modello richiede campioni da $p_\theta$.

Se campionare fino all'equilibrio è troppo costoso, serve un'approssimazione.

La contrastive divergence sostituisce la *negative phase* esatta con una *negative phase* "breve".

## Idea di base

- Si parte da un dato reale $x^{(0)}$

- Si fanno pochi passi di Gibbs: $x^{(0)}\to x^{(1)}\to \cdots \to x^{(k)}$

Si confrontano:

$$
\text{dato reale}
\quad \text{VS} \quad
\text{ricostruzione dopo pochi passi}.
$$

Il modello viene aggiornato per rendere i dati più probabili delle ricostruzioni indesiderate.

## CD-k

Schema:

```text
per ogni dato x^(0):
    inizializza la catena in x^(0)
    esegui k passi di Gibbs sampling
    ottieni x^(k)
    aggiorna i parametri confrontando x^(0) e x^(k)
```

Nel caso CD-1 per una RBM:

$$
v^{(0)} \to h^{(0)} \to v^{(1)} \to h^{(1)}.
$$

CD-1 è economica, ma più approssimata.

## Aggiornamento dei pesi

Per una RBM, il parametro $W_{ia}$ è associato al prodotto $v_i h_a$.

L'aggiornamento ideale confronta

$$
\langle v_i h_a\rangle_{data}
\quad \text{e} \quad
\langle v_i h_a\rangle_{model}.
$$

CD-k sostituisce la media del modello con la media sulle ricostruzioni:

$$
\Delta W_{ia} \propto \langle v_i h_a\rangle_{data} - \langle v_i h_a\rangle_{CD-k}.
$$

## CD-1 nelle RBM

Dato $v^{(0)}$:

1. campiona $h^{(0)}\sim p(h\mid v^{(0)})$

2. ricostruisci $v^{(1)}\sim p(v\mid h^{(0)})$

3. campiona $h^{(1)}\sim p(h\mid v^{(1)})$

4. confronta le correlazioni $v^{(0)}h^{(0)}$ e $v^{(1)}h^{(1)}$.

## Perché partire dai dati

Partire dai dati inizializza la catena in una regione plausibile.

Se il modello è buono, pochi passi producono ricostruzioni simili ai dati.

Se il modello è cattivo, le ricostruzioni si allontanano e forniscono un segnale di correzione.

CD-k osserva il comportamento locale del modello vicino alla distribuzione empirica.

Non esplora necessariamente tutto lo spazio.

## Limiti

La contrastive divergence:

- non fornisce in generale il gradiente esatto della likelihood;
- può essere distorta se $k$ è piccolo;
- può fallire se il mixing è lento;
- può migliorare le ricostruzioni senza stimare bene la probabilità normalizzata.

È una procedura pratica, non una soluzione esatta.

## Persistent contrastive divergence

Una variante mantiene catene persistenti durante l'apprendimento.

Invece di ripartire dai dati:

- le catene vengono conservate;
- a ogni aggiornamento fanno pochi passi;
- seguono gradualmente la distribuzione del modello.

L'obiettivo è stimare meglio la negative phase.

Anche qui il limite resta il mixing della catena.

# 9. Hamiltonian Monte Carlo

## Spazi continui

Gibbs è naturale per variabili discrete o aggiornabili per blocchi.

Per variabili continue ad alta dimensione, piccoli passi casuali possono essere inefficienti.

HMC usa gradienti per costruire proposte lunghe ma plausibili.

Esempi:

- parametri continui;
- variabili latenti continue;
- modelli bayesiani;
- distribuzioni definite da negative log-likelihood o negative log-posterior.

## Target ed energia potenziale

- Vogliamo campionare $\quad \pi(q), \qquad q\in\mathbb{R}^d.$

- Spesso conosciamo solo $\pi(q)\propto e^{-U(q)}.$

Definiamo

$$
U(q)=-\log\pi(q)+\text{costante}.
$$

$U(q)$ è l'energia potenziale.

La costante non conta per gradienti e rapporti.

## Momento ausiliario

Introduciamo un *momento* $p\in\mathbb{R}^d.$ (qui $p$ è momento "*massa*$\times$*velocità*", non probabilità).

- Energia cinetica $\qquad K(p)=\frac{1}{2}p^T M^{-1}p$

- Hamiltoniana $\qquad H(q,p)=U(q)+K(p)$

Distribuzione congiunta:

$$
\pi(q,p)\propto e^{-H(q,p)}
$$

Marginalizzando su $p$, si recupera la distribuzione target su $q$.

## Dinamica hamiltoniana

Le equazioni sono

$$
\frac{dq}{dt}=\frac{\partial H}{\partial p}\qquad,
\qquad \frac{dp}{dt}=-\frac{\partial H}{\partial q}.
$$

Con energia cinetica quadratica:

$$
\frac{dq}{dt}=M^{-1}p\qquad, \qquad \frac{dp}{dt}=-\nabla U(q)
$$

La dinamica usa il gradiente per muovere il punto nello spazio.

## Leapfrog

Un passo leapfrog con passo $\epsilon$:

$$
p\leftarrow p-\frac{\epsilon}{2}\nabla U(q),\qquad
q\leftarrow q+\epsilon M^{-1}p,\qquad
p\leftarrow p-\frac{\epsilon}{2}\nabla U(q).
$$

Ripetendo $L$ passi si ottiene una proposta $(q',p')$.

Leapfrog è reversibile e preserva il il volume dello spazio delle fasi.

L'errore sull'Hamiltoniana viene corretto con accettazione Metropolis.

## Accettazione

La proposta viene accettata con probabilità

$$
\alpha=\min\{1,\exp[-H(q',p')+H(q,p)]\}.
$$

Se l'integrazione conserva quasi l'Hamiltoniana,

$$
H(q',p')\approx H(q,p),
$$

allora $\alpha$ è vicina a uno.

HMC può quindi proporre mosse lunghe con alta probabilità di accettazione.

## Schema HMC

```text
scegli uno stato iniziale q
ripeti:
    campiona un momento p da una gaussiana
    simula L passi leapfrog
    ottieni una proposta (q',p')
    accetta o rifiuta q'
```

A ogni iterazione vale:

$$
p\sim\mathcal{N}(0,M).
$$

La sequenza finale dei campioni è la sequenza delle posizioni $q$.

I momenti sono ausiliari.

## HMC ed energy-based models

Se $p_\theta(q)=e^{-E_\theta(q)}/Z_\theta$

- poniamo $U(q)=E_\theta(q)$

- il gradiente richiesto è $\nabla U(q)=\nabla E_\theta(q)$

La normalizzazione non compare nel gradiente:

$$
\nabla_q\log p_\theta(q)=
-\nabla_q E_\theta(q).
$$

HMC richiede la log-densità non normalizzata e il suo gradiente.

## Gibbs vs HMC

| Metodo | Naturale quando | Usa |
|---|---|---|
| Gibbs sampling | variabili discrete o blocchi condizionati | distribuzioni condizionate |
| HMC | variabili continue differenziabili | gradienti e dinamica ausiliaria |

Entrambi campionano da distribuzioni complesse definite implicitamente.

Ma sfruttano strutture diverse del problema.

## Limiti di HMC

HMC richiede:

- variabili continue;
- energia differenziabile;
- gradienti calcolabili;
- scelta adeguata di passo, lunghezza e massa.

Può essere difficile con:

- geometrie complicate;
- code forti;
- curvature molto diverse;
- regioni strette;
- gradienti costosi.

Quando funziona, produce campioni meno correlati di molte dinamiche locali.

# 10. Sintesi finale

## Ruolo dei metodi

| Oggetto | Ruolo | Idea chiave |
|---|---|---|
| EBM | modello implicito | un'energia definisce una distribuzione |
| Hopfield | memoria associativa | attrattori come pattern memorizzati |
| Boltzmann Machine | modello generativo | campioni con peso di Boltzmann |
| RBM | BM bipartita | condizionate semplici |
| Gibbs | campionamento discreto | aggiornare da condizionate |
| CD | apprendimento approssimato | dati vs ricostruzioni |
| HMC | campionamento continuo | gradienti e dinamica |

## Errori concettuali da evitare

- Energia bassa non significa probabilità uno.
- Generare non significa minimizzare.
- Una probabilità non normalizzata non è ancora una probabilità.
- La funzione di partizione non è un dettaglio tecnico.
- Una ricostruzione CD non è un campione indipendente dal modello.

Il punto chiave è distinguere configurazioni ottime, configurazioni tipiche e configurazioni generate.

## Applicazioni: una carrellata

Lo stesso linguaggio compare in molti campi.

| Campo | Configurazione | Energia/costo | Uso |
|---|---|---|---|
| Fisica | microstato | energia | equilibrio |
| ML | dato/latente | energy/loss | generazione |
| Bayes | parametri | negative log-posterior | incertezza |
| Neuroscienze | pattern | energia attrattiva | memoria |
| Biologia | sequenza/conformazione | score | compatibilità |
| Reti | grafo/partizione | score negativo | ensemble |
| Scienze sociali | scelta/stato/rete | disutilità/distanza | scenari |
| Visione | immagine/segmentazione | data term + prior | ricostruzione |

## Chiusura

Una funzione energia può essere usata per:

1. cercare configurazioni a bassa energia;
2. campionare configurazioni con probabilità proporzionale a $e^{-E(x)}$;
3. apprendere un modello generativo dai dati.

La stessa struttura matematica collega:

$$
\text{ottimizzare},
\qquad
\text{campionare},
\qquad
\text{generare}.
$$

Questo è il ponte tra meccanica statistica, inferenza, machine learning e modellizzazione computazionale.

