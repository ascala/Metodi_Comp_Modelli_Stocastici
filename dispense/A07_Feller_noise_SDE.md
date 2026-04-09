---
title: "A07: SDE con rumore di Feller"
author: "Antonio Scala"
date: ""
---

# 1. Un nuovo tipo di rumore moltiplicativo

Dopo il moto browniano geometrico,
$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t,
$$
è naturale chiedersi che cosa accada quando il rumore non sia proporzionale a $X_t$, ma cresca più lentamente con lo stato.

Uno dei casi più importanti è l'equazione
$$
dX_t = (a+\mu X_t)\,dt + \sigma \sqrt{X_t}\,dW_t,
\qquad X_t\ge 0.
$$

Qui:

* $a$ è un termine costante nel drift;
* $\mu X_t$ è una parte lineare del drift;
* $\sigma\sqrt{X_t}$ è l'intensità del rumore.

Questo processo appartiene alla famiglia dei **processi di Feller**. In una parametrizzazione molto usata, soprattutto in probabilità e finanza, si scrive invece
$$
dX_t = \kappa(\theta-X_t),dt + \sigma\sqrt{X_t},dW_t,
$$
che è il **processo di Cox--Ingersoll--Ross** (CIR).

Le due forme sono equivalenti. Basta porre
$$
a = \kappa\theta,
\qquad
\mu=-\kappa.
$$

Nel seguito useremo soprattutto la forma
$$
dX_t = (a+\mu X_t)\,dt + \sigma\sqrt{X_t}\,dW_t,
$$
perché mette in evidenza in modo semplice la combinazione tra *drift affine* e *rumore sublineare*.

# 2. Perché questo modello è interessante

Questo processo è importante perché descrive una grandezza non negativa la cui intensità di rumore cresce con lo stato, ma in modo meno che proporzionale.

Il fattore $\sqrt{X_t}$ ha due effetti qualitativi fondamentali:

* quando $X_t$ è piccolo, anche il rumore è piccolo;
* quando $X_t$ cresce, il rumore cresce, ma non così rapidamente come nel caso lineare $\sigma X_t$.

Questo rende il modello molto diverso sia dal caso additivo
$$
dX_t=\mu\,dt+\sigma\,dW_t,
$$
sia dal moto browniano geometrico
$$
dX_t=\mu X_t\,dt+\sigma X_t\,dW_t.
$$

Il processo con rumore $\sqrt{X_t}$ compare in molti contesti:

* evoluzione di popolazioni o densità con fluttuazioni demografiche;
* modelli di intensità e tassi non negativi;
* finanza matematica, per tassi di interesse o volatilità;
* approssimazioni diffusive di processi di nascita e morte.

# 3. Positività e significato del bordo $X=0$

L'equazione
$$
dX_t = (a+\mu X_t)\,dt + \sigma\sqrt{X_t}\,dW_t
$$
ha senso naturale per $X_t\ge 0$, perché il coefficiente di diffusione contiene $\sqrt{X_t}$.

Questo già suggerisce che il punto $X=0$ abbia un ruolo speciale. Infatti:

* per $X_t>0$, il rumore è attivo;
* in $X_t=0$, il termine stocastico si annulla;
* l'evoluzione in prossimità dello zero dipende quindi soprattutto dal drift.

In particolare, quando $X_t$ è molto piccolo,
$$
dX_t \approx a\,dt + \sigma\sqrt{X_t}\,dW_t.
$$

Se $a>0$, il drift tende a respingere il processo lontano da zero. Se invece $a=0$, il bordo può diventare molto più delicato.

Uno dei temi centrali di questo modello è quindi il comportamento al bordo $X=0$.

# 4. Confronto intuitivo con il moto browniano geometrico

Vale la pena mettere subito a confronto i due casi.

## Moto browniano geometrico

$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t.
$$

* il rumore è proporzionale a $X_t$;
* il logaritmo del processo è gaussiano;
* la distribuzione è lognormale;
* la media e la traiettoria tipica possono divergere fortemente.

## Processo con rumore radice

$$
dX_t = (a+\mu X_t)\,dt + \sigma\sqrt{X_t}\,dW_t.
$$

* il rumore è proporzionale a $\sqrt{X_t}$;
* vicino a zero il rumore si spegne;
* il bordo $X=0$ ha un ruolo matematico essenziale;
* il processo resta naturalmente legato al semiasse positivo.

Per questa ragione il caso $\sqrt{X_t}$ è il modello naturale quando si vogliono descrivere quantità positive con fluttuazioni che nascono da meccanismi di conteggio o di campionamento.

# 5. Equazione di Fokker--Planck

All'SDE

$$
dX_t = (a+\mu X_t)\,dt + \sigma\sqrt{X_t}\,dW_t
$$

si associa l'equazione di Fokker--Planck per la densità $p(x,t)$:
$$
\partial_t p(x,t) = -\partial_x\bigl[(a+\mu x)\,p(x,t)\bigr] + \frac{1}{2}\partial_x^2\bigl[\sigma^2 x\,p(x,t)\bigr]
$$

il cui coefficiente diffusivo $b^2(x)=\sigma^2 x$ è lineare in $x$.

La corrente di probabilità corrispondente è
$$
J(x,t)=(a+\mu x)p(x,t)-\frac{1}{2}\partial_x\bigl(\sigma^2 x p(x,t)\bigr).
$$

Questa forma è particolarmente utile per studiare gli stati stazionari e il ruolo del bordo in $x=0$.

# 6. Equazione per il momento primo

Una delle quantità più semplici da calcolare è il momento primo. Prendiamo il valore atteso dell'SDE:
$$
dX_t=(a+\mu X_t)\,dt+\sigma\sqrt{X_t}\,dW_t.
$$

Poiché l'integrale stocastico ha media nulla, otteniamo
$$
\frac{d}{dt}\mathbb E[X_t] = a+\mu\mathbb E[X_t].
$$

Dunque il momento primo soddisfa una normale equazione differenziale lineare.

Se indichiamo con
$$
m_1(t)=\mathbb E[X_t]\;,
$$
il momento primo, allora
$$
m_1'(t)=a+\mu m_1(t).
$$

## Caso $\mu\neq 0$

La soluzione è
$$
\boxed{
\mathbb E[X_t]=X_0 e^{\mu t}+\frac{a}{\mu}\bigl(e^{\mu t}-1\bigr)
}.
$$

## Caso $\mu=0$

Si ottiene invece
$$
\boxed{
\mathbb E[X_t]=X_0+at
}.
$$

Questo è già un primo risultato importante: nonostante il rumore sia moltiplicativo, l'evoluzione del momento primo non coinvolge momenti di ordine superiore.

# 7. Equazione per il momento secondo

Per ottenere il momento secondo applichiamo la formula di Itô alla funzione
$$
f(x)=x^2.
$$

Poiché
$$
f'(x)=2x,
\qquad
f''(x)=2,
$$
si ha
$$
d(X_t^2)=2X_t\,dX_t + (dX_t)^2.
$$

Ora,
$$
dX_t=(a+\mu X_t)\,dt+\sigma\sqrt{X_t}\,dW_t,
$$
e quindi
$$
(dX_t)^2 = \sigma^2 X_t\,dt.
$$

Sostituendo,
$$
d(X_t^2)
=2X_t(a+\mu X_t)\,dt + 2\sigma X_t^{3/2}\,dW_t + \sigma^2 X_t\,dt.
$$

Raccogliendo i termini deterministici,
$$
d(X_t^2)=\bigl(\,(2a+\sigma^2)X_t+2\mu X_t^2\,\bigr)\,dt + 2\sigma X_t^{3/2}\,dW_t.
$$

Prendendo il valore atteso, otteniamo
$$
\frac{d}{dt}\mathbb E[X_t^2]=(2a+\sigma^2)\mathbb E[X_t]+2\mu\mathbb E[X_t^2].
$$

Se definiamo il momento secondo
$$
m_2(t)=\mathbb E[X_t^2],
$$
segue che
$$
m_2'(t)=(2a+\sigma^2)m_1(t)+2\mu m_2(t).
$$

Questa equazione, insieme a quella per $m_1$, permette di ricavare la varianza.

# 8. Struttura gerarchica dei momenti

In realtà tutti i momenti del processo soddisfano una gerarchia chiusa. Se si applica Itô a
$$
f(x)=x^n,
$$
si ottiene una relazione del tipo
$$
\frac{d}{dt}\mathbb E[X_t^n] = \alpha_n\mathbb E[X_t^{n-1}]+\beta_n\mathbb E[X_t^n]\;,
$$
con coefficienti espliciti dipendenti da $a$, $\mu$, $\sigma$ e $n$.

Questo è un tratto molto interessante del modello: il coefficiente diffusivo $\sqrt{X_t}$ produce una chiusura naturale della gerarchia dei momenti, a differenza di altri rumori moltiplicativi più generali.

Più precisamente, per $n\ge 1$ si trova
$$
\frac{d}{dt}\mathbb E[X_t^n] = \left(na+\frac{n(n-1)}{2}\sigma^2\right)\mathbb E[X_t^{n-1}] + n\mu\mathbb E[X_t^n].
$$

# 9. Caso mean-reverting

Il caso più importante in pratica è quello in cui il drift spinge il processo verso un valore caratteristico. Ciò accade quando
$$
\mu<0.
$$

È allora comodo riscrivere
$$
\mu=-\kappa,
\qquad
\kappa>0.
$$

L'SDE diventa
$$
dX_t=(a-\kappa X_t)\,dt + \sigma\sqrt{X_t}\,dW_t.
$$

Ponendo
$$
a=\kappa\theta,
$$
si ottiene la forma standard CIR:
$$
\boxed{
dX_t = \kappa(\theta-X_t)\,dt + \sigma\sqrt{X_t}\,dW_t
}.
$$

Qui:

* $\theta$ è il livello verso cui il drift tende a riportare il processo;
* $\kappa$ misura la velocità di rilassamento;
* $\sigma$ controlla l'intensità del rumore.

Nel caso CIR, il momento primo soddisfa
$$
\frac{d}{dt}\mathbb E[X_t]=\kappa\theta-\kappa\mathbb E[X_t],
$$
quindi
$$
\boxed{
\mathbb E[X_t]=\theta + (X_0-\theta)e^{-\kappa t}
}.
$$

Questo mostra chiaramente il significato di $\theta$: esso è il valore medio stazionario.

# 10. Stato stazionario dalla corrente nulla

Cerchiamo ora una densità stazionaria $p_{\mathrm{st}}(x)$ nel caso mean-reverting, cioè con $\mu<0$.

In regime stazionario si ha
$$
\partial_t p_{\mathrm{st}}=0.
$$

Se inoltre imponiamo corrente nulla,
$$
J(x)=0,
$$
allora dalla formula della corrente otteniamo
$$
(a+\mu x)p_{\mathrm{st}}(x)-\frac{1}{2}\frac{d}{dx}\bigl(\,\sigma^2 x p_{\mathrm{st}}(x)\,\bigr)=0.
$$

Riscriviamo questa equazione come
$$
\frac{d}{dx}\bigl(x\,p_{\mathrm{st}}(x)\bigr)=\frac{2}{\sigma^2}(a+\mu x)\,p_{\mathrm{st}}(x).
$$

Ponendo
$$
q(x)=x\,p_{\mathrm{st}}(x),
$$
si ha
$$
p_{\mathrm{st}}(x)=\frac{q(x)}{x},
$$
quindi
$$
q'(x)=\frac{2}{\sigma^2}(a+\mu x)\frac{q(x)}{x}.
$$

Segue
$$
\frac{q'(x)}{q(x)}=\frac{2a}{\sigma^2}\frac{1}{x}+\frac{2\mu}{\sigma^2}.
$$

Integrando,
$$
\log q(x)=\frac{2a}{\sigma^2}\log x + \frac{2\mu}{\sigma^2}x + C.
$$

Dunque
$$
q(x)=C x^{2a/\sigma^2} e^{(2\mu/\sigma^2)x},
$$
e perciò
$$
p_{\mathrm{st}}(x)=C x^{\frac{2a}{\sigma^2}-1} e^{\frac{2\mu}{\sigma^2}x}.
$$

Affinché questa densità sia normalizzabile su $[0,\infty)$, occorre avere
$$
\mu<0.
$$

In tal caso, scrivendo $\mu=-\kappa$ con $\kappa>0$, si ottiene
$$
p_{\mathrm{st}}(x)=C x^{\frac{2a}{\sigma^2}-1} e^{-\frac{2\kappa}{\sigma^2}x}.
$$

Questa è una densità gamma.

# 11. Forma esplicita dello stato stazionario

Confrontando con la densità gamma
$$
f(x)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x},
\qquad x>0,
$$
riconosciamo i parametri
$$
\alpha=\frac{2a}{\sigma^2},
\qquad
\beta=\frac{2\kappa}{\sigma^2}
\quad \text{quando } \mu=-\kappa<0.
$$

Quindi
$$
\boxed{
p_{\mathrm{st}}(x)=
\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x}
}
$$
con
$$
\alpha=\frac{2a}{\sigma^2},
\qquad
\beta=\frac{-2\mu}{\sigma^2}.
$$

Nel linguaggio del processo CIR, usando $a=\kappa\theta$, diventa
$$
\alpha=\frac{2\kappa\theta}{\sigma^2},
\qquad
\beta=\frac{2\kappa}{\sigma^2}.
$$

La media stazionaria della gamma è
$$
\frac{\alpha}{\beta}=\theta,
$$
come ci si aspetta dal calcolo del momento primo.

# 12. Comportamento vicino a zero

La forma della densità stazionaria vicino a zero è
$$
p_{\mathrm{st}}(x)\sim x^{\frac{2a}{\sigma^2}-1}
\qquad \text{per } x\to 0^+.
$$

Quindi il comportamento dipende dal valore del rapporto
$$
\frac{2a}{\sigma^2}.
$$

## Se $2a/\sigma^2>1$

La densità va a zero in $x=0$.

## Se $2a/\sigma^2=1$

La densità tende a una costante finita in $x=0$.

## Se $0<2a/\sigma^2<1$

La densità diverge in $x=0$, ma resta integrabile.

Questo mostra che lo zero può essere un punto fortemente "attrattivo" dal punto di vista probabilistico, anche quando il processo ammette uno stato stazionario normale.

# 13. La condizione di Feller

Un risultato classico afferma che, nel processo CIR
$$
dX_t = \kappa(\theta-X_t),dt + \sigma\sqrt{X_t},dW_t,
$$
se vale la condizione
$$
\boxed{
2\kappa\theta \ge \sigma^2
}
$$
allora il processo, partendo da $X_0>0$, non raggiunge zero.

Poiché $a=\kappa\theta$, questa condizione equivale a
$$
\boxed{
2a\ge \sigma^2
}.
$$

Essa esprime il fatto che il drift repulsivo vicino allo zero è sufficientemente forte da compensare le fluttuazioni.

Se invece
$$
2a<\sigma^2,
$$
lo zero può diventare accessibile.

Dal punto di vista qualitativo, questa condizione segna il confine tra due regimi:

* uno in cui il processo resta strettamente positivo;
* uno in cui può arrivare arbitrariamente vicino a zero, o persino toccarlo.

# 14. Media e varianza nello stato stazionario

Nel caso mean-reverting con stato stazionario gamma, si possono ricavare facilmente media e varianza.

Poiché per una gamma con parametri $(\alpha,\beta)$ vale
$$
\mathbb E[X]=\frac{\alpha}{\beta},
\qquad
\mathrm{Var}(X)=\frac{\alpha}{\beta^2},
$$
qui otteniamo
$$
\mathbb E[X]_{\mathrm{st}} = \frac{2a/\sigma^2}{(-2\mu)/\sigma^2} = -\frac{a}{\mu},
$$
valida per $\mu<0$.

Nel caso CIR, cioè $\mu=-\kappa$ e $a=\kappa\theta$, questo diventa
$$
\boxed{
\mathbb E[X]_{\mathrm{st}}=\theta
}.
$$

Analogamente,
$$
\mathrm{Var}(X)_{\mathrm{st}}
= \frac{\alpha}{\beta^2}
= \frac{2a/\sigma^2}{\left((-2\mu)/\sigma^2\right)^2}
= \frac{2a}{\sigma^2}\,\frac{\sigma^4}{4\mu^2}
= \frac{a\sigma^2}{2\mu^2},
\qquad \mu<0.
$$
con $\mu<0$, cioè
$$
\boxed{
\mathrm{Var}(X)_{\mathrm{st}}=
\frac{a\sigma^2}{2\mu^2}
}.
$$

Nel caso CIR questo si scrive
$$
\boxed{
\mathrm{Var}(X)_{\mathrm{st}}=
\frac{\theta\sigma^2}{2\kappa}
}.
$$

# 15. Interpretazione fisica e probabilistica

Il processo con rumore $\sqrt{X_t}$ può essere interpretato come una descrizione continua di una quantità positiva soggetta a due meccanismi concorrenti:

* una tendenza deterministica lineare a crescere o rilassare;
* una fluttuazione la cui intensità è legata al numero di eventi elementari che accadono nell'unità di tempo.

Il fattore $\sqrt{X_t}$ è infatti tipico dei limiti diffusivi di processi di conteggio: quando il numero di eventi elementari è proporzionale a $X_t$, la fluttuazione assoluta è dell'ordine della radice quadrata del numero di eventi, quindi dell'ordine di $\sqrt{X_t}$.

Questo spiega perché il modello compaia naturalmente come limite continuo di processi di nascita e morte.

# 16. Differenze principali rispetto al GBM

È utile concludere con un confronto sintetico con il moto browniano geometrico.

## GBM

$$
dX_t=\mu X_t,dt+\sigma X_t,dW_t
$$

* soluzione esplicita in forma esponenziale;
* distribuzione lognormale;
* forte separazione tra media e traiettoria tipica;
* il rumore cresce linearmente con lo stato.

## Processo con rumore radice

$$
dX_t=(a+\mu X_t),dt+\sigma\sqrt{X_t},dW_t
$$

* il processo resta naturalmente non negativo;
* il rumore si spegne vicino a zero;
* il bordo $x=0$ è cruciale;
* nel caso mean-reverting esiste uno stato stazionario gamma;
* la condizione $2a\ge \sigma^2$ controlla l'inaccessibilità di zero.

Questa seconda classe di modelli è quindi particolarmente importante quando la positività della variabile e il comportamento vicino al bordo sono aspetti centrali del problema.

# 17. Conclusione

L'equazione
$$
dX_t=(a+\mu X_t),dt+\sigma\sqrt{X_t},dW_t
$$
fornisce un esempio fondamentale di SDE con rumore moltiplicativo sublineare.

A differenza del moto browniano geometrico, qui il punto centrale non è la lognormalità, ma piuttosto:

* la positività del processo;
* il ruolo speciale del bordo $X=0$;
* la chiusura gerarchica dei momenti;
* l'emergere di una distribuzione stazionaria gamma nel regime mean-reverting.

Per questi motivi il processo di Feller/CIR occupa un posto centrale nello studio delle SDE su domini positivi e nei modelli diffusi in fisica, probabilità applicata e finanza matematica.
