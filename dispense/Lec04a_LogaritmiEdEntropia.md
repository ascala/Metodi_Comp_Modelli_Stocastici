---
title: "04a: Entropia, logaritmi e massima entropia"
author: "Antonio Scala"
date: ""
---

## 1. Perché compare il logaritmo?

In molti contesti -- dalla fisica alla statistica -- compaiono espressioni del tipo
$$
\log p \qquad \text{oppure} \qquad e^{-x}.
$$

Una domanda naturale è: perché lavorare con logaritmi o esponenziali invece che direttamente con le probabilità?

La risposta di base è che il logaritmo trasforma prodotti in somme.

Se eventi indipendenti hanno probabilità $p_1, p_2, \dots, p_n$, allora
$$
P = \prod_{i=1}^n p_i,
$$
mentre
$$
\log P = \sum_{i=1}^n \log p_i.
$$

Questo rende il logaritmo particolarmente naturale quando si combinano molti contributi elementari.

Ma c'è anche un'altra ragione importante: il logaritmo permette di quantificare la **sorpresa** associata a un evento.

## 2. Sorpresa matematica e informazione

Se un evento ha probabilità $p$, è naturale dire che esso è tanto più "sorprendente" quanto più $p$ è piccolo.

Una misura quantitativa semplice e molto utile della sorpresa è

$$
I(p) = \log \frac{1}{p} = -\log p.
$$

Questa funzione ha proprietà desiderabili:

1. se un evento è molto probabile ($p$ vicino a $1$), la sorpresa è piccola;
2. se un evento è raro ($p$ piccolo), la sorpresa è grande;
3. per eventi indipendenti la sorpresa totale è additiva:
   $$
   I(p_1p_2) = -\log(p_1p_2) = -\log p_1 - \log p_2 = I(p_1)+I(p_2).
   $$

Questa quantità è spesso chiamata **self-information** o **informazione di sorpresa**.

La scelta del logaritmo non è quindi arbitraria: è ciò che rende l'informazione additiva per eventi indipendenti.

## 3. Informazione di Shannon

Shannon formalizza questa idea definendo l'informazione associata a un evento $i$ di probabilità $p_i$ come
$$
I_i = -\log p_i.
$$

Questa definizione traduce in linguaggio matematico l'idea intuitiva che:

- eventi comuni portano poca informazione;
- eventi rari portano molta informazione.

Ad esempio, sapere che domani il Sole sorgerà contiene pochissima informazione; sapere che vincerò alla lotteria ne contiene molta di più.

## 4. Entropia come sorpresa media

Se una variabile casuale assume valori $i$ con probabilità $p_i$, la sorpresa media è

$$
H = \sum_i p_i I_i = -\sum_i p_i \log p_i.
$$

Questa è l'**entropia di Shannon**.

Interpretazione:

- misura l'incertezza media prima di osservare il risultato;
- è massima quando tutti gli esiti sono equiprobabili;
- è minima quando un esito è certo.

Quindi l'entropia non misura la sorpresa di un singolo evento, ma la **sorpresa media attesa** del sistema.

## 5. Perché proprio il logaritmo?

Il logaritmo non è una scelta decorativa o puramente tecnica.

È la funzione naturale quando vogliamo una quantità che:

- cresca al diminuire della probabilità;
- sia nulla per un evento certo;
- sia additiva per eventi indipendenti.

In questo senso, il logaritmo costruisce un ponte tra:

- probabilità;
- informazione;
- entropia;
- likelihood.

## 6. Da Shannon a Boltzmann--Gibbs

In meccanica statistica, l'entropia si scrive

$$
S = -k_B \sum_i p_i \ln p_i.
$$

Questa formula è formalmente identica a quella di Shannon, a meno della costante $k_B$.

Qui il logaritmo ha una doppia interpretazione:

- informazionale: misura incertezza o sorpresa media;
- fisica: codifica il numero effettivo di microstati compatibili con lo stato macroscopico.

La parentela tra entropia fisica e informazione non è quindi accidentale.

## 7. Massima entropia

Il principio di **massima entropia** (Jaynes) afferma:

> tra tutte le distribuzioni compatibili con i vincoli noti, si sceglie quella con entropia massima.

L'idea è che non dobbiamo introdurre struttura o informazione non giustificata dai dati disponibili.

Se conosco solo alcuni vincoli globali, la distribuzione più "onesta" è quella che resta il più possibile indeterminata pur rispettando quei vincoli.

In molti casi, questo principio porta naturalmente a distribuzioni esponenziali.

## 8. Likelihood e log-likelihood

In statistica, dati indipendenti $x_1, \dots, x_n$ generati da un modello con parametro $\theta$ hanno likelihood

$$
L(\theta) = \prod_{i=1}^n p(x_i \mid \theta).
$$

Si lavora quasi sempre con la **log-likelihood**:

$$
\ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log p(x_i \mid \theta).
$$

Anche qui il logaritmo appare perché rende additive quantità che, a livello probabilistico, nascono come prodotti.

## 9. Perché la log-likelihood è utile

La log-likelihood è preferita perché:

- trasforma prodotti in somme;
- è numericamente più stabile;
- semplifica derivate e ottimizzazione;
- rende evidente il contributo di ogni osservazione.

Inoltre, massimizzare la likelihood equivale a massimizzare la log-likelihood, perché il logaritmo è monotono crescente.

Questa è una delle ragioni per cui il logaritmo compare così spesso anche fuori dalla fisica statistica.

## 10. Collegamento concettuale

Entropia e log-likelihood sono profondamente collegate.

- la sorpresa di un singolo evento è $-\log p$;
- l'entropia è la media di $-\log p$;
- la log-likelihood è una somma di termini $\log p$.

In tutti questi casi, il logaritmo rende **additiva** una quantità fondamentale.

## 11. Messaggio finale

Il logaritmo compare in molti ambiti perché:

- rende additive quantità moltiplicative;
- misura la sorpresa matematica di un evento;
- permette di definire l'informazione e l'entropia;
- semplifica l'analisi statistica tramite la log-likelihood;
- emerge naturalmente dal principio di massima entropia.

Non è quindi una scelta tecnica arbitraria, ma una struttura molto generale dei sistemi probabilistici.

# Appendice -- Un esempio semplice di massima entropia con moltiplicatori di Lagrange

Mostriamo ora, in forma elementare, come il principio di Jaynes conduca a una distribuzione esponenziale.

Per evitare complicazioni funzionali, consideriamo un insieme **finito** di valori possibili
$$
x_1, x_2, \dots, x_n
$$
e cerchiamo le probabilità
$$
p_1, p_2, \dots, p_n
$$
che massimizzano l'entropia

$$
H = -\sum_{i=1}^n p_i \log p_i
$$

sotto i vincoli

$$
\sum_{i=1}^n p_i = 1
$$

(normalizzazione) e

$$
\sum_{i=1}^n p_i x_i = m,
$$

dove $m$ è il valore medio assegnato (o, in casi concreti,osservato/misurato).

## A.1 Richiamo: metodo dei moltiplicatori di Lagrange

Se vogliamo massimizzare una funzione $f(x_1,\dots,x_n)$ sotto vincoli
$$
g_1(x_1,\dots,x_n)=0,\qquad g_2(x_1,\dots,x_n)=0,
$$
introduciamo una funzione ausiliaria
$$
\mathcal{L} = f + \lambda_1 g_1 + \lambda_2 g_2
$$
e imponiamo che tutte le derivate parziali rispetto alle variabili e ai moltiplicatori siano nulle.

Qui le variabili sono le probabilità $p_i$, e i vincoli sono la normalizzazione e il valore medio fissato.

## A.2 Costruzione della lagrangiana

Definiamo

$$
\mathcal{L}(p_1,\dots,p_n,\alpha,\beta) =
-\sum_{i=1}^n p_i\log p_i
-\alpha\left(\sum_{i=1}^n p_i - 1\right)
-\beta\left(\sum_{i=1}^n p_i x_i - m\right).
$$

I segni davanti ad $\alpha$ e $\beta$ sono convenzionali: cambierebbe solo la notazione finale.

## A.3 Condizione di stazionarietà

Deriviamo rispetto a ciascun $p_i$:

$$
\frac{\partial \mathcal{L}}{\partial p_i} =
-(\log p_i + 1) - \alpha - \beta x_i.
$$

Ponendo questa derivata uguale a zero otteniamo

$$
-(\log p_i + 1) - \alpha - \beta x_i = 0,
$$

cioè

$$
\log p_i = -1 - \alpha - \beta x_i.
$$

Esponenziando,

$$
p_i = e^{-1-\alpha-\beta x_i}.
$$
Le equazioni ottenute derivando rispetto ai moltiplicatori $\alpha$ e $\beta$ restituiscono semplicemente i vincoli originali:
$$
\sum_{i=1}^n p_i = 1,
\qquad
\sum_{i=1}^n p_i x_i = m.
$$
Nel seguito usiamo il primo per determinare la costante di normalizzazione e il secondo per fissare il valore di $\beta$.

## A.4 Determinazione della costante

Possiamo riscrivere il prefattore costante come una nuova costante di normalizzazione:

$$
p_i = C e^{-\beta x_i};
$$

usando il vincolo di normalizzazione:

$$
\sum_{i=1}^n p_i = 1
\quad \Rightarrow \quad
C \sum_{i=1}^n e^{-\beta x_i} = 1.
$$

Quindi

$$
C = \frac{1}{Z(\beta)},
\qquad
Z(\beta) = \sum_{i=1}^n e^{-\beta x_i}.
$$

La distribuzione finale è dunque

$$
p_i = \frac{e^{-\beta x_i}}{Z(\beta)}.
$$

Il parametro $\beta$ va poi scelto in modo che sia soddisfatto il vincolo sul valore medio

$$
\sum_{i=1}^n x_i p_i = m.
$$

Sostituendo la forma trovata per $p_i$,

$$
p_i = \frac{e^{-\beta x_i}}{Z(\beta)},
\qquad
Z(\beta) = \sum_{i=1}^n e^{-\beta x_i},
$$

si ottiene una relazione che lega $\beta$ al valore medio:

$$
\sum_{i=1}^n x_i \frac{e^{-\beta x_i}}{Z(\beta)} = m.
$$

Questa è un’equazione per $\beta$, che in generale non si risolve in forma esplicita, ma può essere risolta numericamente (ad esempio con metodi iterativi).

In modo equivalente, si può osservare che

$$
\langle x \rangle = -\frac{d}{d\beta} \log Z(\beta),
$$

quindi $\beta$ è determinato imponendo che questa quantità sia uguale a $m$.

## A.5 Interpretazione

Abbiamo ottenuto una distribuzione esponenziale non perché l'abbiamo ipotizzata, ma perché è la soluzione del problema:

- massimizzare l'incertezza;
- mantenendo fissati solo normalizzazione e valore medio.

Questa è l'idea centrale del principio di Jaynes.

In meccanica statistica, se $x_i$ viene interpretata come energia $E_i$, si ottiene la distribuzione di Boltzmann:

$$
p_i = \frac{e^{-\beta E_i}}{Z(\beta)}.
$$

## A.6 Take home message

Questo esempio mostra tre idee importanti:

1. il logaritmo compare naturalmente nell'entropia;
2. l'esponenziale compare naturalmente come soluzione del problema di massimo;
3. i moltiplicatori di Lagrange permettono di incorporare i vincoli in modo sistematico.

Per questo entropia, logaritmi ed esponenziali tendono a comparire insieme in molti contesti diversi.