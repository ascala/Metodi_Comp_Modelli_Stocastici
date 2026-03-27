---
title: "S05 Rumore e dinamiche stocastiche"
author: "Antonio Scala"
date: "27 mar 2026"
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

## Obiettivi della lezione

**Idea centrale:** introdurre il rumore nei modelli dinamici e costruire il passaggio da equazioni deterministiche a equazioni differenziali stocastiche.

**Obiettivi:**

- capire perché i modelli deterministici non bastano
- introdurre il rumore bianco come idealizzazione
- definire il processo di Wiener
- derivare la formula di Ito in una dimensione
- costruire lo schema di Euler--Maruyama
- distinguere accuratezza forte e debole
- discutere stabilità ed esempi applicativi

---

## Perché introdurre il rumore?

:::: {.columns}
::: {.column width="50%"}

**Modello deterministico**

- condizione iniziale fissata
- traiettoria unica
- nessuna fluttuazione

:::
::: {.column width="50%"}

**Sistemi reali**

- urti microscopici
- variabilità ambientale
- eterogeneità non osservata
- incertezza sperimentale

:::
::::

**Idea chiave:** la dinamica osservata combina una parte sistematica e una parte fluttuante.

---

## Esempi motivazionali

:::: {.columns}
::: {.column width="50%"}

- fisica: moto browniano
- chimica: collisioni e reazioni
- biologia: espressione genica
- ecologia: ambiente variabile

:::
::: {.column width="50%"}

- finanza: prezzi e volatilità
- ingegneria: disturbi e sensori
- neuroscienze: firing irregolare
- scienze sociali: eterogeneità individuale

:::
::::

---

## Rumore additivo e moltiplicativo

:::: {.columns}
::: {.column width="45%"}

#### Rumore additivo

$$
dx = a(x,t)\,dt + \sigma\,dW_t
$$

- intensità indipendente dallo stato
- stessa scala di fluttuazione per ogni $x$

:::
::: {.column width="50%"}

#### Rumore moltiplicativo

$$
dx = a(x,t)\,dt + \sigma x\,dW_t
$$

- intensità dipendente dallo stato
- comportamento qualitativamente più ricco

:::
::::

---

## Equazione di Langevin

Per la velocità $v(t)$ di una particella:

$$
m\,\frac{dv}{dt} = -\gamma v + \sigma\,\eta(t)
$$

- $-\gamma v$: attrito
- $\sigma$: intensità della forza casuale
- $\eta(t)$: rumore bianco

**Messaggio:** Langevin separa dissipazione e fluttuazione.

---

## Rumore bianco: immagine intuitiva

Formalmente si pensa a $\eta(t)$ come a una forzante con

$$
\langle \eta(t) \rangle = 0,
\qquad
\langle \eta(t)\eta(t') \rangle = \delta(t-t').
$$

Generalizzando:

$$
\frac{dx}{dt} = a(x,t) + b(x,t)\eta(t)
$$

**Ma:** questa scrittura non è ancora rigorosa.

---

## Perché il rumore bianco non è una funzione ordinaria

- $\eta(t)$ è troppo irregolare
- il calcolo differenziale usuale non si applica direttamente
- serve una formulazione in termini di incrementi

**Passo corretto:** introdurre il processo di Wiener.

---

## Il processo di Wiener

Si introduce $W_t$ tale che formalmente

$$
\eta(t) = \frac{dW_t}{dt}.
$$

:::: {.columns}
::: {.column width="50%"}

#### Definizione

- $W_0 = 0$
- incrementi indipendenti
- traiettorie continue
- incrementi gaussiani

:::
::: {.column width="50%"}

#### Proprietà

per $t>s$:

$$
W_t - W_s \sim \mathcal{N}(0,t-s)
$$

e formalmente

$$
\langle dW_t \rangle = 0,
\qquad
\langle dW_t^2 \rangle = dt
$$

:::
::::

---

## Forma generale di una SDE

Una SDE scalare in forma di Ito si scrive

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t
$$

:::: {.columns}
::: {.column width="50%"}

#### Drift

$$
a(x,t)\,dt
$$

- parte regolare
- tendenza media

:::
::: {.column width="50%"}

#### Diffusione

$$
b(x,t)\,dW_t
$$

- parte stocastica
- ampiezza delle fluttuazioni

:::
::::

---

## Perché $dW_t$ è dell'ordine di $\sqrt{dt}$

Su un intervallo piccolo $dt$:

$$
dW_t \sim \mathcal{N}(0,dt)
$$

quindi l'ampiezza tipica è

$$
|dW_t| \sim \sqrt{dt}.
$$

Da qui segue il fatto decisivo:

$$
(dW_t)^2 \sim dt.
$$

---

## Dal caso deterministico al caso stocastico

Nel caso deterministico:

$$
dx = a(x,t)\,dt
$$

e per $f(x,t)$ regolare:

$$
df = \frac{\partial f}{\partial t}\,dt
+ \frac{\partial f}{\partial x}\,dx
+ \text{ordini superiori}.
$$

Nel caso stocastico, se

$$
dx = a(x,t)\,dt + b(x,t)\,dW_t,
$$

il termine $(dx)^2$ non è trascurabile.

---

## Espansione rilevante

Si sviluppa fino all'ordine utile:

$$
df =
\frac{\partial f}{\partial t}\,dt
+ \frac{\partial f}{\partial x}\,dx
+ \frac{1}{2}\frac{\partial^2 f}{\partial x^2}(dx)^2.
$$

Il punto chiave è quindi calcolare $(dx)^2$.

---

## Regole differenziali di Ito

$$
dx = a\,dt + b\,dW_t \quad \Rightarrow \quad 
(dx)^2 = a^2dt^2 + 2ab\,dt\,dW_t + b^2(dW_t)^2
$$

Si usano le regole formali:

$$
dt^2 = 0,
\qquad
dt\,dW_t = 0,
\qquad
(dW_t)^2 = dt.
$$

ovvero trascuro i termini $\mathcal{O}(dt^2)$ e $\mathcal{O}(dt^{3/2})$; quindi

$$
(dx)^2 = b(x,t)^2\,dt.
$$

---

## Formula di Ito

Sostituendo, si ottiene

$$
df =
\left(
\frac{\partial f}{\partial t}
+
a(x,t)\frac{\partial f}{\partial x}
+
\frac{1}{2}b(x,t)^2\frac{\partial^2 f}{\partial x^2}
\right)dt
+
b(x,t)\frac{\partial f}{\partial x}\,dW_t.
$$

**Questa è la formula di Ito in una dimensione.**

---

## Esempio elementare: $f(x)=x^2$

Per

$$
f(x)=x^2 \quad \Rightarrow \quad
\frac{\partial f}{\partial x}=2x,
\qquad
\frac{\partial^2 f}{\partial x^2}=2.
$$

Quindi

$$
df = d(x^2) = 2x\,dx + b(x,t)^2\,dt.
$$

Compare un termine aggiuntivo che nel calcolo ordinario non c'è.

---

## Cosa bisogna ricordare di Ito

- il termine quadratico in $dW_t$ contribuisce a ordine $dt$
- per questo $(dx)^2$ non si elimina
- la regola della catena cambia
- il calcolo stocastico non è una copia del calcolo ordinario

---

## Dalla forma integrale allo schema discreto

Su $[t_n,t_{n+1}]$:

$$
x_{n+1} - x_n =
\int_{t_n}^{t_{n+1}} a(x_t,t)\,dt
+
\int_{t_n}^{t_{n+1}} b(x_t,t)\,dW_t.
$$

se indichiamo con $\Delta t_n=t_{n+1}-t_n$ ed approssimiamo i coefficienti all'inizio del passo come $a(x_t,t) \approx a(x_n,t_n)$, $b(x_t,t) \approx b(x_n,t_n)$, otteniamo

$$ x_{n+1} \approx x_n  + a(x_n,t_n) \Delta t_n + b(x_n,t_n)\int_{t_n}^{t_{n+1}} \,dW_t\;.$$

---

## Incrementi browniani discreti

Definiamo

$$
\Delta W_n = \int_{t_n}^{t_{n+1}} \,dW_t = W_{t_{n+1}} - W_{t_n}.
$$

Poiché

$$
\Delta W_n \sim \mathcal{N}(0,\Delta t_n),
$$

si può scrivere

$$
\Delta W_n = \sqrt{\Delta t}\,\xi_n,
\qquad
\xi_n \sim \mathcal{N}(0,1).
$$

---

## Schema di Euler--Maruyama

Lo schema diventa

$$
x_{n+1} = x_n
+ a(x_n,t_n)\Delta t
+ b(x_n,t_n)\Delta W_n.
$$

Equivalentemente,

$$
x_{n+1} = x_n
+ a(x_n,t_n)\Delta t
+ b(x_n,t_n)\sqrt{\Delta t}\,\xi_n.
$$

---

## Interpretazione dello schema

:::: {.columns}
::: {.column width="50%"}

#### Parte deterministica

$$
a(x_n,t_n)\Delta t
$$

- analoga al metodo di Eulero
- descrive la tendenza media

:::
::: {.column width="50%"}

#### Parte casuale

$$
b(x_n,t_n)\sqrt{\Delta t}\,\xi_n
$$

- fluttuazione sul singolo passo
- cambia da traiettoria a traiettoria

:::
::::

---

## Algoritmo minimo

- fissare $x_0$, $\Delta t$, $N$
- per $n=0,\dots,N-1$
  - estrarre $\xi_n \sim \mathcal{N}(0,1)$
  - porre $\Delta W_n = \sqrt{\Delta t}\,\xi_n$
  - aggiornare con Euler--Maruyama
- ripetere per ottenere più traiettorie

---

## Cosa mostra una simulazione

- una singola traiettoria non è "la soluzione"
- la SDE definisce una famiglia di realizzazioni
- due simulazioni con gli stessi parametri danno curve diverse
- le quantità statistiche richiedono molte traiettorie

---

## Esempio guida: Ornstein--Uhlenbeck

Consideriamo

$$
dx = -\lambda x\,dt + \sigma\,dW_t,
\qquad \lambda > 0.
$$

- drift lineare di richiamo verso l'origine
- rumore additivo
- modello base per teoria e test numerici

---

## Stabilità di Euler--Maruyama

Applicando Euler--Maruyama:

$$
x_{n+1} = (1-\lambda \Delta t)x_n + \sigma \sqrt{\Delta t}\,\xi_n.
$$

Per evitare instabilità nella parte discreta:

$$
|1-\lambda \Delta t| < 1
$$

ossia

$$
0 < \Delta t < \frac{2}{\lambda}.
$$

---

## Accuratezza forte e debole

:::: {.columns}
::: {.column width="50%"}

#### Accuratezza forte

- interessa la singola traiettoria
- si confrontano realizzazioni costruite con lo stesso rumore
- per Euler--Maruyama: ordine forte $1/2$

:::
::: {.column width="50%"}

#### Accuratezza debole

- interessano medie e osservabili
- si confrontano quantità statistiche
- per Euler--Maruyama: ordine debole $1$

:::
::::

---

## Come si verificano in pratica

:::: {.columns}
::: {.column width="50%"}

#### Verifica forte

- stessa realizzazione browniana
- confronto con soluzione esatta
- oppure con soluzione di riferimento molto fine

:::
::: {.column width="50%"}

#### Verifica debole

- molte traiettorie indipendenti
- confronto di medie empiriche
- confronto di momenti o osservabili

:::
::::

---

## Ornstein--Uhlenbeck: media esatta

Per

$$
dx = -\lambda x\,dt + \sigma\,dW_t
$$

si ha

$$
x(t) = x_0 e^{-\lambda t}
+ \sigma \int_0^t e^{-\lambda (t-s)}\,dW_s
$$

e quindi

$$
\mathbb{E}[x(t)] = x_0 e^{-\lambda t}.
$$

Questa formula è utile per controllare la convergenza debole.

---

## Dove compaiono le SDE?

:::: {.columns}
::: {.column width="50%"}

### **Fisica**

$$
dx = v\,dt, \;
dv = -\gamma v\,dt - kx\,dt + \sigma\,dW_t
$$

### **Chimica**

$$
dx = -U'(x)\,dt + \sigma\,dW_t
$$

### **Biologia**

$$
dx = (\alpha - \beta x)\,dt + \sigma\,dW_t
$$

:::
::: {.column width="50%"}

### **Finanza**

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t
$$

### **Ecologia**

$$
dx = r x\left(1-\frac{x}{K}\right)dt + \sigma x\,dW_t
$$

### **Scienze sociali**

$$
dx = (-\gamma x + F(t))\,dt + \sigma\,dW_t
$$

:::
::::

---

## Take-home message

- il rumore descrive fluttuazioni reali, non solo errori
- l'immagine intuitiva parte da Langevin e dal rumore bianco
- la formulazione rigorosa usa il processo di Wiener
- il calcolo di Ito modifica la regola della catena
- Euler--Maruyama è il primo schema numerico fondamentale
- per le SDE va distinta accuratezza forte da accuratezza debole

---

## Prossima lezione

- equazione di Fokker--Planck
- schemi numerici più accurati
- SDE multidimensionali
- processi con salti

---

## Backup -- Ito e Stratonovich

:::: {.columns}
::: {.column width="50%"}

#### Ito

- coefficiente valutato all'inizio del passo
- naturale per probabilità e simulazione
- base di Euler--Maruyama

:::
::: {.column width="50%"}

#### Stratonovich

- valutazione simmetrica
- più vicino nella forma al calcolo ordinario
- non coincide con Ito

:::
::::

---

## Backup -- Formula di conversione

Se

$$
dx = a_S(x,t)\,dt + b(x,t)\circ dW_t,
$$

allora la forma equivalente di Ito è

$$
dx = a_I(x,t)\,dt + b(x,t)\,dW_t,
$$

con

$$
a_I(x,t) = a_S(x,t) + \frac{1}{2}b(x,t)\,\partial_x b(x,t).
$$

---

## Backup -- Milstein

Per la SDE scalare

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t,
$$

lo schema di Milstein è

$$
X_{n+1} = X_n
+ a(X_n,t_n)\Delta t
+ b(X_n,t_n)\Delta W_n
+ \frac{1}{2}b(X_n,t_n)\partial_x b(X_n,t_n)
\left((\Delta W_n)^2 - \Delta t\right).
$$

- migliora l'accuratezza forte
- naturale estensione di Euler--Maruyama