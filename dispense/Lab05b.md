---
title: "LAB05b: mean reversion e preservazione della positività per rumore di tipo radice"
author: "Antonio Scala"
date: ""
---

# Obiettivi

In questo laboratorio studiamo numericamente una SDE che descrive una quantità non negativa soggetta a:

- richiamo verso un valore tipico;
- fluttuazioni casuali la cui intensità cresce come la radice quadrata dello stato.

Il modello è un primo esempio importante di processo di Feller/CIR.  
L'obiettivo non è ottenere formule chiuse per tutta la distribuzione, ma capire come la struttura dell'equazione influenzi le traiettorie e le approssimazioni numeriche.

Al termine del laboratorio dovreste essere in grado di:

1. simulare numericamente una SDE con rumore $\sqrt{X_t}$;
2. interpretare il significato del drift di richiamo;
3. riconoscere il ruolo speciale del bordo $X=0$;
4. osservare che Euler--Maruyama può produrre valori negativi;
5. confrontare diverse correzioni numeriche per preservare la non negatività;
6. verificare numericamente l'evoluzione teorica della media.

# Il modello

Consideriamo la SDE

$$
dX_t = \kappa(\theta-X_t)\,dt + \sigma\sqrt{X_t}\,dW_t,
\qquad X_0\ge 0.
$$

Qui:

- $\theta>0$ è il livello verso cui il drift tende a riportare il processo;
- $\kappa>0$ misura la forza del richiamo;
- $\sigma\ge 0$ controlla l'intensità del rumore.

## Interpretazione qualitativa

Il termine di drift è

$$
\kappa(\theta-X_t).
$$

Quindi:

- se $X_t<\theta$, il drift è positivo;
- se $X_t>\theta$, il drift è negativo.

Per questo si dice che il processo è **mean-reverting**: tende a tornare verso il livello $\theta$.

Il termine stocastico è

$$
\sigma\sqrt{X_t}\,dW_t.
$$

Questo significa che:

- il rumore è più debole quando $X_t$ è piccolo;
- il rumore si annulla formalmente in $X_t=0$;
- il bordo $X=0$ è quindi un punto speciale del modello.

# Parametri di lavoro

Usate inizialmente:

$$
X_0 = 1,
\qquad
\theta = 1,
\qquad
\kappa = 2,
\qquad
\sigma = 0.8,
\qquad
T = 2.
$$

Per le medie campionarie, usate ad esempio

$$
M = 10^3 \quad \text{oppure} \quad M = 10^4.
$$

Per la discretizzazione temporale, provate almeno

$$
N = 2^5,\;2^6,\;2^7,\;2^8,
\qquad
\Delta t = \frac{T}{N}.
$$

Successivamente esplorate anche valori più grandi di $\sigma$, ad esempio

$$
\sigma = 1.4,\;1.8,\;2.2.
$$

# Parte 1 -- Prime simulazioni e interpretazione qualitativa

## 1.1 Griglia temporale e incrementi browniani

Costruite una griglia uniforme

$$
t_n = n\Delta t,
\qquad n=0,\dots,N.
$$

Generate incrementi indipendenti

$$
\Delta W_n \sim \mathcal N(0,\Delta t).
$$

## 1.2 Schema di Euler--Maruyama

Applicate lo schema

$$
X_{n+1} = X_n + \kappa(\theta-X_n)\Delta t + \sigma\sqrt{X_n}\,\Delta W_n.
$$

Attenzione: questa formula ha senso soltanto finché $X_n\ge 0$.

## 1.3 Tracciare alcune traiettorie

Simulate alcune traiettorie singole e rappresentatele graficamente insieme alla retta orizzontale

$$
x=\theta.
$$

## Domande

1. Le traiettorie sembrano oscillare attorno a $\theta$?
2. Che effetto osservate aumentando $\kappa$?
3. Che effetto osservate aumentando $\sigma$?
4. Il processo sembra più simile a un GBM oppure a un processo con richiamo verso un livello medio?

# Parte 2 -- La media teorica

Anche se non conosciamo una formula elementare per la traiettoria esatta, possiamo ricavare l'equazione per il valore atteso.

Partendo da
$$
dX_t = \kappa(\theta-X_t)\,dt + \sigma\sqrt{X_t}\,dW_t,
$$
e prendendo il valore atteso, si ottiene

$$
\frac{d}{dt}\mathbb E[X_t] = \kappa\bigl(\theta-\mathbb E[X_t]\bigr).
$$

La soluzione di questa ODE per il momento primo è

$$
\mathbb E[X_t] = \theta + (X_0-\theta)e^{-\kappa t}.
$$

Questa formula sarà il nostro riferimento teorico.

## 2.1 Verifica numerica della media

Simulate $M$ traiettorie e calcolate la media campionaria a ogni tempo di griglia:

$$
\overline X(t_n)=\frac{1}{M}\sum_{m=1}^M X_n^{(m)}.
$$

Confrontate poi $\overline X(t_n)$ con la curva teorica

$$
\theta + (X_0-\theta)e^{-\kappa t_n}.
$$

## Domande

1. La media empirica segue bene la curva teorica?
2. Che cosa cambia quando si aumenta il numero di traiettorie $M$?
3. Che cosa cambia quando si riduce $\Delta t$?

# Parte 3 -- Il problema della negatività numerica

Nel modello continuo la variabile è pensata come non negativa. Tuttavia lo schema di Euler--Maruyama può produrre valori negativi.

Infatti

$$
X_{n+1} = X_n + \kappa(\theta-X_n)\Delta t + \sigma\sqrt{X_n}\,\Delta W_n
$$

può diventare negativo se la fluttuazione casuale è sufficientemente grande in valore assoluto.

Questo crea un problema immediato: al passo successivo il termine

$$
\sqrt{X_{n+1}}
$$

non è più definito nei reali.

## 3.1 Esperimento numerico

Per ogni traiettoria, controllate se esiste almeno un indice $n$ tale che

$$
X_n<0.
$$

Definite la frequenza di negatività come

$$
p_{\mathrm{neg}}(\Delta t)=
\frac{\text{\# di traiettorie che diventano negative almeno una volta}}{M}.
$$

Studiate come varia rispetto a:

1. $\Delta t$;
2. $\sigma$;
3. $\kappa$.

## Domande

1. La frequenza di negatività diminuisce quando $\Delta t$ diminuisce?
2. Un rumore più intenso rende più probabile la comparsa di valori negativi?
3. Perché questo è un difetto grave dello schema numerico?

# Parte 4 -- Correzione 1: radice troncata

Una prima correzione semplice consiste nel sostituire

$$
\sqrt{X_n}
\quad \text{con} \quad
\sqrt{\max(X_n,0)}.
$$

Lo schema diventa quindi

$$
X_{n+1} = X_n + \kappa(\theta-X_n)\Delta t
+ \sigma\sqrt{\max(X_n,0)}\,\Delta W_n\;.
$$

Questo evita l'errore numerico immediato nel calcolo della radice, ma non garantisce ancora che $X_{n+1}\ge 0$.

## 4.1 Esperimento

Implementate questo schema e confrontatelo con Euler ingenuo.

## Domande

1. Lo schema continua a produrre valori negativi?
2. In che senso questo schema è più robusto?
3. Questa modifica cambia il modello continuo oppure è soltanto un artificio numerico?

# Parte 5 -- Correzione 2: proiezione sul semiasse positivo

Un'altra possibilità è proiettare il risultato del passo sul semiasse positivo.

Definite prima

$$
\widetilde X_{n+1} = X_n + \kappa(\theta-X_n)\Delta t
+ \sigma\sqrt{\max(X_n,0)}\,\Delta W_n,
$$

e poi imponete

$$
X_{n+1}=\max(0,\widetilde X_{n+1}).
$$

In questo modo la non negatività è garantita a ogni passo.

## 5.1 Esperimento

Implementate lo schema proiettato e confrontatelo con:

1. Euler ingenuo;
2. Euler con radice troncata.

## Domande

1. Questo schema preserva sempre la non negatività?
2. La media empirica viene alterata in modo visibile?
3. Si tratta di una correzione naturale oppure di una modifica un po' brutale?

# Parte 6 -- Confronto tra gli schemi

Confrontate i tre approcci:

1. Euler ingenuo;
2. Euler con radice troncata;
3. Euler con proiezione.

Per ciascuno osservate:

- stabilità numerica;
- frequenza di valori negativi;
- aderenza alla media teorica;
- aspetto qualitativo delle traiettorie.

## Suggerimento

Per rendere il confronto più chiaro, usate gli stessi incrementi browniani per i tre schemi.

## Domande

1. Quale metodo vi sembra più robusto?
2. Quale metodo vi sembra più fedele al modello continuo?
3. Preservare la non negatività basta da solo per dire che uno schema è buono?

# Parte 7 -- Ruolo dei parametri

Studiate separatamente l'effetto dei tre parametri principali.

## 7.1 Variare $\kappa$

Provate ad esempio

$$
\kappa = 0.5,\;1,\;2,\;4.
$$

Domande:

1. Le traiettorie tornano più rapidamente verso $\theta$ quando $\kappa$ aumenta?
2. La media teorica converge più rapidamente verso $\theta$?

## 7.2 Variare $\theta$

Provate ad esempio

$$
\theta = 0.5,\;1,\;2.
$$

Domande:

1. Cambia il livello attorno a cui il processo oscilla?
2. La curva teorica della media si adatta come previsto?

## 7.3 Variare $\sigma$

Provate ad esempio

$$
\sigma = 0.4,\;0.8,\;1.4,\;2.2.
$$

Domande:

1. Le fluttuazioni crescono con $\sigma$?
2. La frequenza di valori negativi numerici aumenta?
3. La media empirica resta ben approssimata anche quando le traiettorie diventano più irregolari?

# Parte 8 -- Un primo sguardo al momento secondo

Facoltativamente, potete studiare anche il momento secondo $\mathbb E[X_t^2]$.

Applicando Itô a $X_t^2$ si ottiene

$$
\frac{d}{dt}\mathbb E[X_t^2]
= (2\kappa\theta+\sigma^2)\mathbb E[X_t]
-2\kappa \mathbb E[X_t^2].
$$

Usando la formula già nota per $\mathbb E[X_t]$, si può quindi studiare anche numericamente l'evoluzione della varianza.

## Possibile attività

1. stimare numericamente $\mathbb E[X_t^2]$;
2. ricavare la varianza empirica;
3. confrontare diversi regimi di parametri.

Questa parte è facoltativa e serve soprattutto come estensione per chi procede più rapidamente.

# Parte 9 -- Discussione finale

Discutete i seguenti punti:

1. che cosa significa dire che il processo è mean-reverting;
2. perché il bordo $X=0$ è speciale;
3. perché uno schema numerico può violare una proprietà qualitativa del modello;
4. perché il confronto con la sola media non basta a giudicare la bontà di uno schema.

# Cosa dovreste aver capito alla fine

Al termine del laboratorio dovreste aver verificato che:

1. il drift $\kappa(\theta-X_t)$ produce richiamo verso il livello $\theta$;
2. il rumore $\sqrt{X_t}$ rende il bordo $X=0$ matematicamente delicato;
3. Euler--Maruyama può produrre valori negativi anche quando il modello continuo è pensato su $X_t\ge 0$;
4. correzioni numeriche semplici possono migliorare la robustezza, ma introducono compromessi;
5. anche senza conoscere la distribuzione completa del processo si può verificare numericamente una formula teorica per la media.

---

# Suggerimento per la consegna

Una breve relazione finale potrebbe contenere:

1. descrizione del modello e del significato dei parametri;
2. grafici di alcune traiettorie;
3. confronto tra media empirica e media teorica;
4. studio della frequenza di negatività;
5. confronto critico tra gli schemi numerici provati.
