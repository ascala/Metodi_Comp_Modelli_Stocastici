---
title: "S04 Simulazioni di eventi discreti (Gillespie)"
author: "Antonio Scala"
date: ""
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

## Obiettivi della lezione

**Idea centrale:** simulare sistemi in cui l’evoluzione avviene tramite **eventi discreti nel tempo**.

**Obiettivi:**

- comprendere cosa è un processo a eventi discreti
- derivare il tempo di attesa esponenziale
- implementare il metodo di Gillespie
- capire quando e perché usare approssimazioni (tau-leaping)
- collegare modelli discreti e descrizioni continue

---

## Processi a eventi discreti

#### Definizione

Un sistema è descritto da:

- stato $x$
- eventi possibili $j=1,\dots,M$
- tassi $a_j(x)$
- regole di aggiornamento

#### Idea chiave

L’evoluzione è **stocastica**:

- quando accade un evento → casuale  
- quale evento accade → casuale  

---

## Esempi

#### Eventi discreti

- chimica: $A + B \to C$
- epidemie: $S \to I$
- code: $n \to n+1$

#### Punto comune

La dinamica è una sequenza di **salti casuali nel tempo**

---

## Tempo di attesa

#### Assunzione

Eventi con tasso costante $\lambda$ $\Rightarrow$ $\lambda dt$ è la probabilità di **un** evento in $[t,t+dt]$

#### Risultato

La probabilità $P(T<t)$ che sia avvenuto un evento al tempo $T<t$ soddisfa 
$$
P(T < t+dt) = P(T < t) +[1-P(T < t)] \lambda dt
$$
ovvero
$$
P(T < t) = 1 - e^{-\lambda t}
$$

Distribuzione **esponenziale** $$p(t) = \lambda e^{-\lambda t}$$

---

## Interpretazione

#### Proprietà chiave

- tempo medio/caratteristico: $\tau=1/\lambda$
- assenza di memoria

#### Significato

Il sistema “attende” un tempo casuale prima del prossimo evento

---

## Generazione del tempo

#### Metodo dell’inversione

Se $U \sim \mathrm{Unif}(0,1)$:

$$
\tau = -\frac{1}{\lambda}\ln U
$$

#### Idea

Trasformiamo uniforme → distribuzione esponenziale

---

## Metodo di Gillespie

:::: {.columns}
::: {.column width="50%"}

#### Idea generale

Simulare il sistema:

- un evento alla volta
- con tempi casuali esatti

#### Differenza dalle ODE

- ODE → tempo continuo deterministico  
- Gillespie → salti discreti casuali  

:::
::: {.column width="50%"}

![](immagini/StepDecay.png){width=80%}

:::
::::

---

## Tasso totale

:::: {.columns}
::: {.column width="50%"}

#### Sistema con $M$ eventi

$$
a_0(x) = \sum_{j=1}^{M} a_j(x)
$$
\medskip

dove $x$ indica lo stato del sistema ed i tassi possono dipendere da $x$

:::
::: {.column width="50%"}

#### Interpretazione

Tasso complessivo del sistema:
\medskip
* ogni evento ha una probabilità di accadere $a_i(x)dt$
* gli eventi sono scorrelati/indipendenti
*  la probabilità che accada **uno** degli eventi è $a_0(x)dt$

::: 
:::: 

---

## Passo di simulazione

:::: {.columns}
::: {.column width="60%"}

#### Due scelte casuali
\medskip
1. tempo del prossimo evento:

$$
\tau = \frac{1}{a_0(x)}\ln\!\left(\frac{1}{U_1}\right)
$$

2. evento selezionato:

$$
P(i) = \frac{a_i(x)}{a_0(x)}
$$
:::
::: {.column width="40%"}

Se un evento dei possibili eventi avviene in un intervallo $[t,t+dt]$, allora:
\medskip

* la probabilità dell'evento $i$ è proporzionale a $a_i\,dt$
* posso normalizzare dividento per $\sum_i a_i\,dt =a_0\,dt$
* la probabilità di $i$ è quindi $a_i\,dt/a_0\,dt = a_i/a_0$

:::
:::: 

---

## Aggiornamento

#### Evoluzione

- aggiorna stato $x$
- aggiorna tempo $t \to t+\tau$
- ripeti

#### Output

Traiettoria stocastica:

$$
(x_0,t_0),(x_1,t_1),\dots
$$

---

## Struttura del modello

:::: {.columns}
::: {.column width="60%"}

#### Due ingredienti
\medskip

1. tassi $a_j(x)$  
2. variazioni di stato $\nu_j$

#### Forma compatta

$$
x \to x + \nu_j
$$

:::
::: {.column width="40%"}

![](immagini/SaltiDiscretiEventDriven.png)

:::
::::

---

## Esempio SIR

#### Eventi
\medskip

- infezione:
$$
[S,I,R]\to[S-1,I+1,R]
$$

- guarigione:
$$
[S,I,R]\to[S,I-1,R+1]
$$

#### Tassi

$$
a_1=\beta SI/N,\quad a_2=\gamma I
$$

---

## Implementazione

#### Schema

- calcola $a_j(x)$  
- estrai $\tau$  
- scegli evento  
- aggiorna stato  

#### Idea

Codice molto semplice, modello generale

---

## Esempio semplice

#### Decadimento

$$
A \to \emptyset
$$

#### Tasso

$$
a(x)=\lambda A
$$

#### Risultato

- traiettorie a gradini  
- media esponenziale  

---

## Limite del metodo

#### Problema

Se i tassi sono grandi:

- troppi eventi
- simulazione lenta

---

## Tau-leaping

:::: {.columns}
::: {.column width="60%"}

#### Idea

Fisso un passo di simulazione $\tau$ ("salto" da $t$ a $t+\tau$ nella simulazione) e faccio avvenire più eventi insieme:

$$
k_j \sim \text{Poisson}(a_j(x)\Delta t)
$$
Condizioni di validità: $\tau$ tipicamente è "piccolo" nel senso che i tassi devono rimanere approssimativamente costanti negli intervalli di simulazione $[t_i,t_i+\tau]$

:::
::: {.column width="40%"}

#### Aggiornamento

Il nuovo stato è ottenuto combinado i contributi di tutti gli eventi che sono avvenuti nel "salto temporale"

$$
x \to x + \sum_j k_j \nu_j
$$

:::
::::

---

## Validità

#### Condizione chiave

Eventi **commutativi**

#### Significato

L’ordine degli eventi non cambia il risultato

---

## Quando funziona

#### Esempi

- reazioni chimiche
- modelli SIR
- nascita–morte

#### Struttura

Variazioni additive sui conteggi

---

## Collegamento continuo

#### Idea

Da Gillespie → equazioni continue

#### Risultato

$$
dx = f(x)dt + G(x)dW_t
$$

Equazioni di **Langevin**

---

## Interpretazione

#### Due livelli

- microscopico: eventi discreti  
- macroscopico: dinamica continua  

#### Messaggio

Gillespie = base teorica  
Langevin = strumento computazionale  

---

## Applicazioni

#### Chimica

- reazioni elementari
- regolazione genica
- sistemi cellulari

---

## Applicazioni

#### Epidemie

- modelli SIR
- reti di contatto
- estinzione stocastica

---

## Applicazioni

#### Sistemi sociali

- diffusione idee
- imitazione
- dinamiche di opinione

---

## Take-home message

- sistemi reali spesso evolvono per eventi discreti
- il tempo di attesa è esponenziale
- Gillespie simula esattamente il processo
- tau-leaping accelera la simulazione
- nel limite continuo → equazioni stocastiche