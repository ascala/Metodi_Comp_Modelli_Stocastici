---
title: "A08: Tre derivazioni dell’equazione di Fokker--Planck"
author: "Antonio Scala"
date: ""
---

Questa appendice raccoglie tre strade complementari che portano all’equazione di Fokker--Planck:

1. la derivazione a partire da una SDE di Itô;
2. la derivazione tramite espansione di Kramers--Moyal;
3. la derivazione a partire dalla master equation.

L’obiettivo non è soltanto ottenere la formula finale, ma mostrare che essa emerge in modo coerente da tre punti di vista diversi:

- il punto di vista delle traiettorie continue rumorose;
- il punto di vista dei momenti degli incrementi;
- il punto di vista dei processi markoviani a salti.

In tutto il testo ci limitiamo al caso unidimensionale, che è il più adatto per fissare le idee senza caricare troppo la notazione.

# 1. Obiettivo comune

La forma che vogliamo ottenere è la seguente.  
Per un processo scalare $X_t$ con densità $p(x,t)$, l’equazione di Fokker--Planck è

$$
\partial_t p(x,t) =
-\partial_x\bigl(A(x,t)p(x,t)\bigr)
+ \frac{1}{2}\partial_x^2\bigl(B(x,t)p(x,t)\bigr),
$$

dove:

- $A(x,t)$ è il coefficiente di drift;
- $B(x,t)$ è il coefficiente diffusivo quadratico.

Nel caso di una SDE di Itô della forma

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t,
$$

si avrà

$$
A(x,t)=a(x,t)\;,
\qquad
B(x,t)=b(x,t)^2\;.
$$

In altre parole,

$$
\partial_t p = -\partial_x(ap) + \frac{1}{2}\partial_x^2(b^2 p)\;.
$$

Le tre derivazioni che seguono servono precisamente a giustificare questa struttura.

# 2. Derivazione da una SDE di Itô

## 2.1 Punto di partenza

Consideriamo la SDE scalare

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t\;.
$$

Supponiamo di voler capire come evolve nel tempo la densità $p(x,t)$ del processo $X_t$.

L’idea fondamentale è la seguente: invece di tentare di seguire direttamente l’evoluzione di $p$, studiamo l’evoluzione del valore atteso di una funzione test regolare $f(x,t)$, e poi trasferiamo le derivate da $f$ a $p$ mediante integrazione per parti.

## 2.2 Formula di Itô per una funzione test

Per una funzione sufficientemente regolare $f(x,t)$, la formula di Itô dà

$$
df(X_t,t) =
\left(
\partial_t f(X_t,t) + a(X_t,t)\partial_x f(X_t,t) 
+ \frac{1}{2}b(X_t,t)^2\partial_x^2 f(X_t,t)
\right)dt
+ b(X_t,t)\partial_x f(X_t,t)\,dW_t.
$$

Prendiamo ora il valore atteso. Poiché il termine in $dW_t$ ha media nulla, otteniamo

$$
\frac{d}{dt}\mathbb{E}[f(X_t,t)] = \mathbb{E}\left[
\partial_t f(X_t,t) + a(X_t,t)\partial_x f(X_t,t)
+ \frac{1}{2}b(X_t,t)^2\partial_x^2 f(X_t,t) \right]\;.
$$

## 2.3 Riscrittura in termini di densità

Per definizione di densità,

$$
\mathbb{E}[f(X_t,t)] = \int f(x,t)p(x,t)\,dx.
$$

Quindi

$$
\frac{d}{dt}\int f(x,t)p(x,t)\,dx = \int \left(
\partial_t f(x,t) + a(x,t)\partial_x f(x,t) 
+ \frac{1}{2}b(x,t)^2\partial_x^2 f(x,t)
\right)p(x,t)\,dx\;.
$$

Sviluppiamo il membro di sinistra:

$$
\frac{d}{dt}\int f p\,dx =
\int \partial_t f\, p\,dx + \int f\,\partial_t p\,dx\;.
$$

Sostituendo e cancellando i termini con $\partial_t f$, si ottiene

$$
\int f(x,t)\,\partial_t p(x,t)\,dx =
\int a(x,t)\partial_x f(x,t)\,p(x,t)\,dx
+ \frac{1}{2}\int b(x,t)^2\partial_x^2 f(x,t)\,p(x,t)\,dx\;.
$$

## 2.4 Integrazione per parti

Ora trasferiamo le derivate da $f$ a $p$, assumendo che i termini di bordo si annullino.

Per il termine con derivata prima,

$$
\int a\,p\,\partial_x f\,dx =
-\int f\,\partial_x(ap)\,dx\;.
$$

Per il termine con derivata seconda servono invece due integrazioni per parti:

$$
\int b^2 p\,\partial_x^2 f\,dx
= -\int \partial_x(b^2 p)\,\partial_x f\,dx
= \int f\,\partial_x^2(b^2 p)\,dx,
$$

sempre assumendo che i termini di bordo si annullino.

Quindi

$$
\int f\,\partial_t p\,dx =
\int f\left[-\partial_x(ap)+\frac{1}{2}\partial_x^2(b^2p)\right]dx\;.
$$

Poiché questo vale per ogni funzione test regolare $f$, concludiamo che

$$
\partial_t p = -\partial_x(ap)
+ \frac{1}{2}\partial_x^2(b^2p)\;.
$$

Questa è l’equazione di Fokker--Planck.

## 2.5 Commento concettuale

Questa derivazione è molto naturale se si parte dalle SDE.  
Il punto essenziale è che la formula di Itô produce automaticamente il termine diffusivo di secondo ordine, tramite il contributo

$$
(dW_t)^2 = dt\;.
$$

In questo approccio, la Fokker--Planck appare come la controparte dell’equazione stocastica a livello delle leggi di probabilità.

# 3. Derivazione tramite espansione di Kramers--Moyal

## 3.1 Idea generale

L’espansione di Kramers--Moyal parte non da una SDE, ma da una descrizione molto generale di processo markoviano continuo nel tempo.  
L’idea di fondo è studiare la statistica degli incrementi in un intervallo di tempo piccolo $\Delta t$.

Indichiamo con

$$
\Delta X = X_{t+\Delta t} - X_t.
$$

Condizionatamente al fatto che $X_t=x$, definiamo i momenti degli incrementi

$$
M_n(x,t;\Delta t) =
\mathbb{E}\big[(\Delta X)^n \mid X_t=x\big].
$$

Se per $\Delta t \to 0$ questi momenti scalano linearmente in $\Delta t$, introduciamo i coefficienti

$$
D^{(n)}(x,t) =
\frac{1}{n!}\lim_{\Delta t\to 0}\frac{M_n(x,t;\Delta t)}{\Delta t}.
$$

Essi sono i coefficienti della serie di Kramers--Moyal.

## 3.2 Forma generale della serie

La densità $p(x,t)$ soddisfa formalmente la serie

$$
\partial_t p(x,t) =
\sum_{n=1}^{\infty} (-\partial_x)^n \bigl(D^{(n)}(x,t)p(x,t)\bigr).
$$

Esplicitando i primi termini,

$$
\partial_t p =
-\partial_x\bigl(D^{(1)}p\bigr)
+ \partial_x^2\bigl(D^{(2)}p\bigr)
- \partial_x^3\bigl(D^{(3)}p\bigr)
+ \cdots
$$

La Fokker--Planck si ottiene quando la serie si tronca ai primi due termini.

## 3.3 Caso di un processo diffusivo

Per un processo diffusivo, gli incrementi su un intervallo breve hanno la struttura tipica

$$
\Delta X \approx a(x,t)\Delta t + b(x,t)\sqrt{\Delta t}\,\xi\;,
$$

dove $\xi$ è una variabile gaussiana standard.

Calcoliamo i primi momenti condizionati:

### Primo momento

$$
\mathbb{E}[\Delta X \mid X_t=x] =
a(x,t)\Delta t + o(\Delta t)\;.
$$

Quindi

$$
D^{(1)}(x,t)=a(x,t).
$$

### Secondo momento

Poiché il termine dominante nel quadrato è quello stocastico,

$$
\mathbb{E}[(\Delta X)^2 \mid X_t=x] =
b(x,t)^2\Delta t + o(\Delta t)\;.
$$

Quindi

$$
D^{(2)}(x,t)=\frac{1}{2}b(x,t)^2\;.
$$

### Momenti superiori

Per $n\ge 3$, gli incrementi di un processo diffusivo producono contributi di ordine più alto di $\Delta t$ e quindi

$$
D^{(n)}(x,t)=0
\qquad \text{per } n\ge 3\;.
$$

## 3.4 Conclusione

La serie di Kramers--Moyal si riduce allora a

$$
\partial_t p = -\partial_x\bigl(a p\bigr)
+ \partial_x^2\left(\frac{1}{2}b^2 p\right)\;,
$$

cioè

$$
\partial_t p =-\partial_x(ap)
+ \frac{1}{2}\partial_x^2(b^2p)\;.
$$

Questa è di nuovo l’equazione di Fokker--Planck.

## 3.5 Commento concettuale

Questa derivazione è più generale della precedente.  
Non parte da una SDE già assegnata, ma dalla statistica locale degli incrementi.  
Il significato dei coefficienti è immediato:

- $D^{(1)}$ codifica il drift medio;
- $D^{(2)}$ codifica la dispersione quadratica degli incrementi;
- la scomparsa dei termini di ordine superiore caratterizza il regime diffusivo.

# 4. Derivazione dalla master equation

## 4.1 Punto di partenza discreto

Consideriamo ora un processo markoviano a salti.  
Per semplicità immaginiamo una variabile di stato continua o quasi continua $x$, soggetta a salti di ampiezza $r$.

Indichiamo con

$$
w(x;r)
$$

il tasso con cui, partendo dallo stato $x$, il sistema compie un salto di ampiezza $r$, cioè passa a $x+r$.

La densità $p(x,t)$ evolve allora secondo la master equation

$$
\partial_t p(x,t) = \int dr \, \bigl[w(x-r;r)p(x-r,t)-w(x;r)p(x,t)\bigr]\;.
$$

Qui il primo termine rappresenta il flusso in ingresso verso $x$, mentre il secondo è il flusso in uscita da $x$.

## 4.2 Ipotesi di piccoli salti

Per ottenere un limite continuo di tipo diffusivo, supponiamo che i salti tipici siano piccoli.  
Qui $r$ è trattato come parametro di salto, mentre lo sviluppo di Taylor è effettuato rispetto alla variabile spaziale $x$, cioè rispetto al primo argomento di $w$.

$$
w(x-r;r)p(x-r,t) = \sum_{n=0}^{\infty}
\frac{(-r)^n}{n!}\partial_x^n\bigl(w(x;r)p(x,t)\bigr);.
$$

Sostituendo nella master equation, il termine di ordine zero cancella esattamente il termine di uscita, e resta

$$
\partial_t p(x,t) = \sum_{n=1}^{\infty} \frac{(-1)^n}{n!}
\partial_x^n \left[ \int r^n w(x;r)\,dr\; p(x,t) \right]\;.
$$

## 4.3 Identificazione dei coefficienti

Definiamo ora i momenti dei salti

$$
a_n(x,t)=\int r^n w(x;r)\,dr.
$$

La serie precedente diventa

$$
\partial_t p
=
-\partial_x\bigl(a_1 p\bigr)
+
\frac{1}{2}\partial_x^2\bigl(a_2 p\bigr)
-
\frac{1}{3!}\partial_x^3\bigl(a_3 p\bigr)
+\cdots
$$

Questa è precisamente la serie di Kramers--Moyal ottenuta dalla master equation.

## 4.4 Limite diffusivo

Nel regime in cui i salti sono piccoli e i contributi di ordine superiore sono trascurabili, si tronca ai primi due termini:

$$
\partial_t p = -\partial_x\bigl(a_1 p\bigr)
+ \frac{1}{2}\partial_x^2\bigl(a_2 p\bigr)\;.
$$

Se identifichiamo

$$
A(x,t)=a_1(x,t)\;,
\quad
B(x,t)=a_2(x,t)\;,
$$

ritroviamo la forma standard

$$
\partial_t p = -\partial_x(Ap)
+ \frac{1}{2}\partial_x^2(Bp)\;.
$$

Questa è ancora una volta l’equazione di Fokker--Planck.

## 4.5 Commento concettuale

Questa derivazione è particolarmente importante perché mostra il legame tra:

- processi a salti;
- master equation;
- limite continuo diffusivo.

In altre parole, la Fokker--Planck non nasce soltanto dalle SDE: può essere vista anche come approssimazione continua di una dinamica markoviana discreta a eventi elementari.

# 5. Confronto tra le tre derivazioni

A questo punto è utile riassumere il significato delle tre strade percorse.

## 5.1 Strada 1: da Itô alla Fokker--Planck

Qui si parte da una SDE già data.  
La domanda è: quale PDE soddisfa la densità della soluzione?

Punti forti:

- è la via più diretta se il modello è già scritto come SDE;
- mette in evidenza il ruolo del calcolo di Itô;
- spiega in modo trasparente l’origine del termine diffusivo di secondo ordine.

## 5.2 Strada 2: da Kramers--Moyal alla Fokker--Planck

Qui si parte dalla statistica locale degli incrementi.

Punti forti:

- è più generale;
- chiarisce il significato dei coefficienti di drift e diffusione come momenti degli incrementi;
- mostra che la Fokker--Planck è un caso particolare di una serie più ampia.

## 5.3 Strada 3: dalla master equation alla Fokker--Planck

Qui si parte da un processo di salto con bilancio di entrata e uscita.

Punti forti:

- collega direttamente Markov continuo nel tempo, Gillespie e limite continuo;
- mostra come la Fokker--Planck emerga come approssimazione di piccoli salti;
- rende esplicito il passaggio dal discreto al continuo.

# 6. Dove interviene l’ipotesi fisica o modellistica

Le tre derivazioni non sono soltanto tre formalismi equivalenti: ciascuna mette in evidenza un punto in cui entra una scelta modellistica.

## 6.1 Nella derivazione da Itô

La scelta modellistica è assumere che il processo sia ben descritto da una SDE con rumore browniano.  
Questa è già un’ipotesi di limite continuo e di rumore diffuso.

## 6.2 Nella derivazione da Kramers--Moyal

La scelta modellistica è assumere che i primi due momenti degli incrementi dominino e che gli ordini superiori siano trascurabili.

## 6.3 Nella derivazione dalla master equation

La scelta modellistica è assumere che i salti elementari siano piccoli rispetto alla scala macroscopica su cui vogliamo descrivere la dinamica.  
Se i salti grandi restano rilevanti, il troncamento diffusivo non è più giustificato.

# 7. Avvertenze sul troncamento

Il passaggio dalla serie completa di Kramers--Moyal alla Fokker--Planck non è automatico in tutti i problemi.

Se i salti non sono piccoli, o se momenti di ordine superiore restano importanti, la serie non può essere troncata in modo innocuo al secondo ordine.  
In tali casi la dinamica effettiva può richiedere:

- una master equation esplicita;
- un’equazione integro-differenziale;
- oppure modelli con rumore non gaussiano o processi di Lévy.

La Fokker--Planck è quindi estremamente importante, ma va interpretata come descrizione efficace del regime diffusivo, non come forma universale di ogni dinamica stocastica.

# 8. Formula finale e lettura unificata

Tutte e tre le derivazioni portano alla stessa forma:

$$
\partial_t p(x,t) = -\partial_x\bigl(A(x,t)p(x,t)\bigr)
+ \frac{1}{2}\partial_x^2\bigl(B(x,t)p(x,t)\bigr)\;.
$$

Nel caso di una SDE di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t\;,
$$

si ha

$$
A(x,t)=a(x,t)\;,
\quad
B(x,t)=b(x,t)^2\;.
$$

Possiamo quindi leggere l’equazione in tre modi equivalenti:

- come equazione per la densità di una SDE;
- come troncamento al secondo ordine della serie di Kramers--Moyal;
- come limite continuo di piccoli salti della master equation.

# 9. Messaggio finale

Il valore didattico di queste tre derivazioni non sta solo nell’ottenere la stessa formula, ma nel mostrare che la Fokker--Planck occupa una posizione centrale nella teoria dei processi stocastici.

Essa è infatti il punto di incontro tra:

- traiettorie rumorose continue;
- espansioni locali degli incrementi;
- dinamiche markoviane a salti.

Per questo la Fokker--Planck non è soltanto una PDE tra le altre: è un vero ponte concettuale tra diversi livelli di descrizione dello stesso fenomeno stocastico.

## Take home messages

1. La derivazione da Itô è la più naturale quando il modello è già scritto come SDE.
2. La derivazione via Kramers--Moyal mostra che drift e diffusione sono i primi due momenti degli incrementi.
3. La derivazione dalla master equation mostra come la Fokker--Planck emerga dal limite continuo di piccoli salti.
4. Le tre derivazioni sono coerenti fra loro e descrivono lo stesso regime diffusivo.
5. Il troncamento al secondo ordine è un’ipotesi modellistica, non una verità automatica in ogni processo stocastico.

