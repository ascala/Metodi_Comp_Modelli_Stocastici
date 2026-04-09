---
title: "A06: Geometric Brownian motion"
author: "Antonio Scala"
date: ""
---

# 1. Dal moto browniano alle equazioni differenziali stocastiche

In molti modelli dinamici si vuole descrivere l'evoluzione di una quantità $X_t$ soggetta a due effetti distinti:

* una tendenza sistematica o **deterministica**;
* una componente **aleatoria** dovuta a fluttuazioni microscopiche, errori, shock o interazioni non controllate.

Nel quadro delle equazioni differenziali stocastiche (SDE), questa idea si scrive nella forma
$$
dX_t = a(X_t,t),dt + b(X_t,t),dW_t,
$$
dove:

* $a(X_t,t)$ è il **termine di drift**;
* $b(X_t,t)$ è il **termine di diffusione** o intensità del rumore;
* $W_t$ è un **moto browniano standard**.

Il simbolo $dW_t$ non va interpretato come un differenziale ordinario. Esso rappresenta l'incremento del moto browniano su un intervallo di tempo piccolo $dt$, cioè
$$
W_{t+dt}-W_t.
$$
Poiché tali incrementi sono gaussiani con media nulla e varianza proporzionale a $dt$, si ha intuitivamente
$$
dW_t \sim \mathcal N(0,dt).
$$
Questo significa che il rumore è di ordine $\sqrt{dt}$, non di ordine $dt$.

# 2. Il moto browniano standard

Il **moto browniano standard** $W_t$ è un processo stocastico caratterizzato da queste proprietà:

1. $W_0=0$;
2. gli incrementi sono indipendenti;
3. per $s<t$, l'incremento $W_t-W_s$ è gaussiano con media $0$ e varianza $t-s$;
4. le traiettorie sono continue.

In particolare,
$$
W_t \sim \mathcal N(0,t),
$$
quindi
$$
\mathbb E[W_t]=0,
\qquad
\mathrm{Var}(W_t)=t.
$$

Il moto browniano rappresenta il modello canonico di fluttuazione accumulata nel tempo. La sua ampiezza tipica cresce come $\sqrt{t}$.

# 3. Il moto browniano con drift

La più semplice SDE è
$$
dX_t = \mu\,dt + \sigma\,dW_t,
$$
dove $\mu\in\mathbb R$ e $\sigma\ge 0$ sono costanti.

Questa equazione descrive una dinamica con:

* crescita lineare media di velocità $\mu$;
* fluttuazioni gaussiane di intensità $\sigma$.

Integrando tra $0$ e $t$ si ottiene
$$
X_t = X_0 + \mu t + \sigma W_t.
$$

Poiché $W_t$ è gaussiano, anche $X_t$ è gaussiano:
$$
X_t \sim \mathcal N(X_0+\mu t,\sigma^2 t).
$$

Dunque
$$
\mathbb E[X_t]=X_0+\mu t,
\qquad
\mathrm{Var}(X_t)=\sigma^2 t.
$$

Questo è il modello naturale quando il rumore si somma allo stato in modo additivo. Tuttavia, in molte applicazioni il rumore non agisce come una perturbazione assoluta, ma come una perturbazione **relativa** alla taglia del sistema.

# 4. Perché introdurre il moto browniano geometrico

In numerosi contesti -- finanza, crescita di popolazioni, diffusione di tecnologie, dinamica di grandezze positive -- è più naturale assumere che le variazioni casuali siano proporzionali al valore corrente della variabile.

In tal caso si scrive
$$
dX_t = \mu X_t,dt + \sigma X_t,dW_t.
$$

Questa è l'equazione del **moto browniano geometrico** (geometric Brownian motion, GBM).

Le due componenti sono entrambe proporzionali a $X_t$:

* il drift $\mu X_t,dt$ produce una crescita percentuale sistematica;
* il termine $\sigma X_t,dW_t$ produce una fluttuazione percentuale casuale.

Il nome "geometrico" deriva dal fatto che il processo agisce in modo naturale sul logaritmo della variabile.

# 5. Soluzione esplicita del moto browniano geometrico

Consideriamo l'SDE
$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t,
\qquad X_0>0.
$$

Per risolverla, conviene applicare la formula di Itô alla funzione
$$
f(x)=\log x.
$$

Poiché
$$
f'(x)=\frac{1}{x},
\qquad
f''(x)=-\frac{1}{x^2},
$$
la formula di Itô dà
$$
d(\log X_t)=f'(X_t),dX_t+\frac{1}{2}f''(X_t)(dX_t)^2.
$$

Ora,
$$
dX_t = \mu X_t,dt + \sigma X_t,dW_t,
$$
quindi
$$
(dX_t)^2 = \sigma^2 X_t^2,dt,
$$
perché nel calcolo di Itô vale $(dW_t)^2=dt$.

Sostituendo si ottiene
$$
d(\log X_t)=\frac{1}{X_t}(\mu X_t,dt+\sigma X_t,dW_t)-\frac{1}{2}\frac{1}{X_t^2}(\sigma^2 X_t^2,dt).
$$

Quindi
$$
d(\log X_t)=\left(\mu-\frac{\sigma^2}{2}\right)dt+\sigma,dW_t.
$$

Integrando tra $0$ e $t$,
$$
\log X_t - \log X_0 = \left(\mu-\frac{\sigma^2}{2}\right)t + \sigma W_t.
$$

Esponenziando,
$$
X_t = X_0\exp\!\left[\left(\mu-\frac{\sigma^2}{2}\right)t+\sigma W_t\right].
$$

Questa è la soluzione esplicita del moto browniano geometrico.

# 6. Distribuzione di $X_t$

Dalla formula precedente segue immediatamente che
$$
\log X_t = \log X_0 + \left(\mu-\frac{\sigma^2}{2}\right)t + \sigma W_t.
$$

Poiché $W_t\sim \mathcal N(0,t)$, si ha
$$
\log X_t \sim \mathcal N\!\left(\log X_0 + \left(\mu-\frac{\sigma^2}{2}\right)t\,,\,\sigma^2 t\right).
$$

Quindi $X_t$ ha distribuzione **lognormale**.

Questo punto è fondamentale: il logaritmo della variabile è gaussiano, ma la variabile stessa non lo è. La distribuzione di $X_t$ è asimmetrica e presenta una coda destra lunga.

# 7. Primo momento

Usando la soluzione esplicita,
$$
X_t = X_0\exp\!\left[\left(\mu-\frac{\sigma^2}{2}\right)t+\sigma W_t\right],
$$
si ottiene
$$
\mathbb E[X_t]
= X_0 e^{\left(\mu-\frac{\sigma^2}{2}\right)t}
\;\mathbb E\!\left[e^{\sigma W_t}\right].
$$

Poiché $W_t\sim \mathcal N(0,t)$ e per una gaussiana centrata vale
$$
\mathbb E[e^{aZ}] = e^{\frac{a^2}{2}\mathrm{Var}(Z)},
$$
si ha
$$
\mathbb E[e^{\sigma W_t}] = e^{\frac{\sigma^2 t}{2}}.
$$

Dunque
$$
\mathbb E[X_t]=X_0 e^{\mu t}.
$$

Questa formula è notevole: la media cresce con tasso $\mu$, esattamente come nel sistema deterministico
$$
\dot x = \mu x.
$$

# 8. Secondo momento e varianza

Elevando al quadrato la soluzione,
$$
X_t^2 = X_0^2\exp\!\left[2\left(\mu-\frac{\sigma^2}{2}\right)t+2\sigma W_t\right],
$$
si ottiene
$$
\mathbb E[X_t^2]
= X_0^2 e^{(2\mu-\sigma^2)t}\;\mathbb E[e^{2\sigma W_t}].
$$

Ancora una volta,
$$
\mathbb E[e^{2\sigma W_t}] = e^{\frac{(2\sigma)^2 t}{2}} = e^{2\sigma^2 t}\;.
$$

Quindi
$$
\mathbb E[X_t^2]=X_0^2\,e^{(2\mu+\sigma^2)t}.
$$

La varianza è allora
$$
\mathrm{Var}(X_t)=\mathbb E[X_t^2]-\bigl(\mathbb E[X_t]\bigr)^2
= X_0^2\,e^{2\mu t}\left(e^{\sigma^2 t}-1\right).
$$

Questa quantità cresce molto rapidamente con $\sigma$ e con $t$.

# 9. Media, mediana e moda

Per comprendere il comportamento del GBM non basta guardare la media. Poiché $X_t$ è lognormale, è utile confrontare tre quantità diverse.

## 9.1 Media

La media è
$$
\mathbb E[X_t]=X_0e^{\mu t}.
$$

Essa è molto sensibile agli eventi rari ma estremi.

## 9.2 Mediana

La mediana di una lognormale è l'esponenziale della media del logaritmo. Dunque
$$
\mathrm{Med}(X_t)=X_0e^{\left(\mu-\frac{\sigma^2}{2}\right)t}.
$$

Questa quantità rappresenta meglio una traiettoria "tipica".

## 9.3 Moda

Per una lognormale, la moda è
$$
\mathrm{Mode}(X_t)=X_0e^{\left(\mu-\frac{3\sigma^2}{2}\right)t}.
$$

La moda è il valore più probabile, cioè il picco della distribuzione.

# 10. Perché aumentando $\sigma$ le traiettorie tipiche vanno verso zero

A prima vista il risultato
$$
\mathbb E[X_t]=X_0e^{\mu t}
$$
può suggerire che il processo cresca mediamente come $e^{\mu t}$, e quindi che un rumore più intenso produca semplicemente fluttuazioni più grandi attorno a tale crescita.

Ma questa intuizione è incompleta.

Infatti la mediana è
$$
\mathrm{Med}(X_t)=X_0e^{\left(\mu-\frac{\sigma^2}{2}\right)t}.
$$

Quindi, se
$$
\mu-\frac{\sigma^2}{2}<0,
$$
la mediana decade esponenzialmente verso zero.

In altre parole, quando
$$
\sigma^2 > 2\mu,
$$
la maggior parte delle traiettorie tende a valori molto piccoli, anche se la media continua a crescere.

Questo non significa che il sistema abbia meno variabilità. Al contrario, la varianza cresce fortemente. Il punto è che la distribuzione diventa sempre più sbilanciata:

* moltissime traiettorie sono piccole;
* pochissime traiettorie sono enormi;
* queste poche traiettorie eccezionali trascinano la media verso l'alto.

Per questo motivo, la media non descrive il comportamento tipico osservabile in un campione finito di traiettorie.

# 11. Il comportamento quasi certo della traiettoria

La soluzione del GBM si può riscrivere come
$$
\frac{1}{t}\log X_t
= \frac{\log X_0}{t} + \mu-\frac{\sigma^2}{2} + \sigma\frac{W_t}{t}.
$$

Ora, per il moto browniano vale
$$
\frac{W_t}{t}\to 0
\qquad \text{quasi certamente, per } t\to\infty.
$$

Dunque
$$
\frac{1}{t}\log X_t \to \mu-\frac{\sigma^2}{2}
\qquad \text{quasi certamente.}
$$

Ne segue che il tasso di crescita temporale di una traiettoria singola è
$$
\mu-\frac{\sigma^2}{2}.
$$

Quindi:

* se $\mu>\sigma^2/2$, una traiettoria tipica cresce esponenzialmente;
* se $\mu<\sigma^2/2$, una traiettoria tipica decade verso zero.

Questo è uno dei messaggi più importanti dell'appendice: nel GBM il tasso di crescita della media e il tasso di crescita tipico non coincidono.

# 12. Un paradosso solo apparente

Possiamo riassumere così:

* la **media d'insieme** cresce come $e^{\mu t}$;
* la **traiettoria tipica** cresce come $e^{(\mu-\sigma^2/2)t}$;
* all'aumentare di $\sigma$, la differenza tra queste due grandezze aumenta.

Non c'è contraddizione. La differenza nasce dal fatto che il GBM produce una distribuzione molto asimmetrica, nella quale la media è dominata dalla coda destra.

Dal punto di vista empirico, se si simulano molte traiettorie per tempi lunghi e per valori grandi di $\sigma$, si osserva spesso che:

* quasi tutte le traiettorie sembrano piccole o decrescenti;
* raramente compare una traiettoria eccezionalmente grande;
* proprio queste poche traiettorie sono responsabili del valore medio elevato.

Questo spiega perché, guardando una figura con molte realizzazioni, si può avere l'impressione che il processo "vada a zero", anche quando la media teorica cresce.

# 13. Confronto con il caso additivo

Vale la pena confrontare il GBM con il moto browniano con drift:
$$
dX_t=\mu\,dt+\sigma\,dW_t.
$$

Nel caso additivo:

* la distribuzione resta gaussiana;
* media e valore tipico restano concettualmente vicini;
* il rumore allarga la distribuzione, ma non introduce la forte asimmetria del caso moltiplicativo.

Nel caso geometrico, invece:

* il processo resta positivo se $X_0>0$;
* la distribuzione è lognormale;
* la media può essere molto diversa dal comportamento più probabile.

Questa differenza rende il moto browniano geometrico un esempio particolarmente istruttivo di dinamica stocastica con rumore moltiplicativo.

# 14. Conclusione

Il moto browniano geometrico mostra in modo elementare ma profondo che, in presenza di rumore moltiplicativo, la nozione di "crescita media" può essere fuorviante se la si interpreta come comportamento tipico del sistema.

Nel caso
$$
dX_t=\mu X_t\,dt+\sigma X_t\,dW_t,
$$
la soluzione è esplicita e consente di vedere chiaramente che:

* la media vale $X_0e^{\mu t}$;
* la mediana vale $X_0e^{(\mu-\sigma^2/2)t}$;
* la moda vale $X_0e^{(\mu-3\sigma^2/2)t}$.

Di conseguenza, aumentando $\sigma$ non si riducono le fluttuazioni: si accentua piuttosto la separazione tra ciò che è tipico e ciò che domina la media.

È proprio questa separazione a rendere il GBM un modello fondamentale nello studio delle SDE con rumore moltiplicativo.

# 15 L'esponenziale di una variabile normale

In più punti dell'analisi del moto browniano geometrico compare una quantità del tipo
$$
\mathbb E[e^{aZ}],
$$
dove $Z$ è una variabile normale. Deriviamo ora esplicitamente la formula, usando il completamento del quadrato.

Sia
$$
Z\sim \mathcal N(m,s^2).
$$
Allora la sua densità è
$$
f_Z(z)=\frac{1}{\sqrt{2\pi s^2}}\exp\!\left(-\frac{(z-m)^2}{2s^2}\right).
$$

Vogliamo calcolare
$$
\mathbb E[e^{aZ}] = \int_{-\infty}^{+\infty} e^{az} f_Z(z)\,dz\;.
$$

Sostituendo la densità,
$$
\mathbb E[e^{aZ}] = \frac{1}{\sqrt{2\pi s^2}}
\int_{-\infty}^{+\infty}
\exp\!\left(az-\frac{(z-m)^2}{2s^2}\right)dz\;.
$$

Completiamo ora il quadrato nell'esponente. Scriviamo
$$
az-\frac{(z-m)^2}{2s^2} = -\frac{1}{2s^2}\bigl[(z-m)^2-2as^2 z\bigr].
$$

Sviluppando il termine tra parentesi,
$$
(z-m)^2-2as^2 z = z^2-2(m+as^2)z+m^2.
$$

Ora aggiungiamo e togliamo $(m+as^2)^2$:
$$
z^2-2(m+as^2)z+m^2 = \bigl(z-(m+as^2)\bigr)^2-(m+as^2)^2+m^2.
$$

Sostituendo, otteniamo
$$
az-\frac{(z-m)^2}{2s^2} = -\frac{\bigl(z-(m+as^2)\bigr)^2}{2s^2}
+\frac{(m+as^2)^2-m^2}{2s^2}\;.
$$

Poiché
$$
(m+as^2)^2-m^2=2ams^2+a^2s^4,
$$
segue che
$$
\frac{(m+as^2)^2-m^2}{2s^2}=am+\frac{a^2s^2}{2}.
$$

Dunque
$$
az-\frac{(z-m)^2}{2s^2} = -\frac{\bigl(z-(m+as^2)\bigr)^2}{2s^2}
+am+\frac{a^2s^2}{2}\;.
$$

L'integrale si riscrive allora come
$$
\mathbb E[e^{aZ}] = \exp\!\left(am+\frac{a^2s^2}{2}\right)
\frac{1}{\sqrt{2\pi s^2}}
\int_{-\infty}^{+\infty}
\exp\!\left(-\frac{\bigl(z-(m+as^2)\bigr)^2}{2s^2}\right)dz.
$$

L'integrale rimanente vale $1$, perché è l'integrale della densità di una normale di media $m+as^2$ e varianza $s^2$. Quindi otteniamo la formula finale:
$$
\boxed{
\mathbb E[e^{aZ}] = \exp\!\left(am+\frac{a^2s^2}{2}\right)
}.
$$

Nel caso centrato, cioè per $Z\sim \mathcal N(0,s^2)$, essa diventa
$$
\boxed{
\mathbb E[e^{aZ}] = e^{\frac{a^2s^2}{2}}
}.
$$

Questa è esattamente la formula usata per calcolare i momenti del moto browniano geometrico.

# 16 Media, mediana e moda di una variabile lognormale

Supponiamo ora che una variabile aleatoria $X$ sia della forma
$$
X=e^Y,
$$
dove
$$
Y\sim \mathcal N(m,s^2).
$$
In questo caso si dice che $X$ ha distribuzione **lognormale**.

Il fatto che il logaritmo di $X$ sia normale permette di ricavare in modo semplice diverse quantità caratteristiche.

## Media

Per definizione,
$$
X=e^Y.
$$
Quindi
$$
\mathbb E[X]=\mathbb E[e^Y].
$$

Applicando la formula ricavata sopra con $a=1$, otteniamo
$$
\boxed{
\mathbb E[X]=e^{m+s^2/2}
}.
$$

## Mediana

La mediana è il valore $x_{1/2}$ tale che
$$
\mathbb P(X\le x_{1/2})=\frac{1}{2}.
$$

Poiché $X=e^Y$ ed esponenziale e logaritmo sono funzioni monotone crescenti,
$$
\mathbb P(X\le x)=\mathbb P(e^Y\le x)=\mathbb P(Y\le \log x).
$$

La condizione di mediana diventa quindi
$$
\mathbb P(Y\le \log x_{1/2})=\frac{1}{2}.
$$

Ma per una normale la mediana coincide con la media, cioè con $m$. Dunque
$$
\log x_{1/2}=m,
$$
e quindi
$$
\boxed{
\mathrm{Med}(X)=e^m
}.
$$

## Moda

La moda è il punto in cui la densità è massima. Ricaviamo prima la densità della lognormale.

Poiché $Y=\log X$, usando il cambiamento di variabile si ottiene
$$
f_X(x)=\frac{1}{x\sqrt{2\pi s^2}}\exp\!\left(-\frac{(\log x-m)^2}{2s^2}\right),
\qquad x>0.
$$

Per trovare la moda, conviene massimizzare il logaritmo della densità:
$$
\ell(x)=\log f_X(x).
$$
A meno di costanti additive indipendenti da $x$,
$$
\ell(x)=-\log x-\frac{(\log x-m)^2}{2s^2}.
$$

Derivando rispetto a $x$,
$$
\ell'(x)=-\frac{1}{x}-\frac{1}{2s^2}\,2(\log x-m)\frac{1}{x}.
$$

Quindi
$$
\ell'(x)=-\frac{1}{x}\left[1+\frac{\log x-m}{s^2}\right].
$$

Ponendo $\ell'(x)=0$, otteniamo
$$
1+\frac{\log x-m}{s^2}=0,
$$
cioè
$$
\log x=m-s^2.
$$

Pertanto la moda è
$$
\boxed{
\mathrm{Mode}(X)=e^{m-s^2}
}.
$$

# 17 Applicazione al moto browniano geometrico

Nel moto browniano geometrico si ha
$$
X_t = X_0\exp\!\left[\left(\mu-\frac{\sigma^2}{2}\right)t+\sigma W_t\right].
$$

Quindi
$$
\log X_t = \log X_0 + \left(\mu-\frac{\sigma^2}{2}\right)t + \sigma W_t.
$$

Poiché $W_t\sim \mathcal N(0,t)$, segue che $\log X_t$ è normale con parametri
$$
m=\log X_0 + \left(\mu-\frac{\sigma^2}{2}\right)t\;,
\qquad
s^2=\sigma^2 t.
$$

Applicando le formule generali della lognormale, otteniamo:

## Media

$$
\mathbb E[X_t]=e^{m+s^2/2}
= e^{\log X_0 + \left(\mu-\frac{\sigma^2}{2}\right)t + \frac{\sigma^2 t}{2}}
= X_0 e^{\mu t}.
$$

## Mediana

$$
\mathrm{Med}(X_t)=e^m
= X_0 e^{\left(\mu-\frac{\sigma^2}{2}\right)t}.
$$

## Moda

$$
\mathrm{Mode}(X_t)=e^{m-s^2}
= X_0 e^{\left(\mu-\frac{3\sigma^2}{2}\right)t}.
$$

Queste tre formule mostrano in modo particolarmente chiaro la differenza tra valore medio, valore tipico e valore più probabile nel moto browniano geometrico.
