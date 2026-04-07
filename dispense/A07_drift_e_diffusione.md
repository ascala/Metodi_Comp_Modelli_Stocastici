---
title: "A07: Operatori di drift e diffusione"
author: "Antonio Scala"
date: ""
---

# 1. Idea generale

In molte equazioni di evoluzione compare una struttura del tipo

$$
\partial_t p = Lp,
$$

dove $L$ è un operatore lineare che agisce sulla variabile spaziale.  
Formalmente, la soluzione con dato iniziale $p(x,0)=p_0(x)$ si scrive come

$$
p(t)=e^{tL}p_0.
$$

Questa formula è molto generale, ma il suo significato concreto dipende dalla natura dell’operatore $L$.

Nel caso della Fokker--Planck a coefficienti costanti, i due operatori elementari più importanti sono:

$$
L_{\mathrm{drift}}=-v\partial_x,
\qquad
L_{\mathrm{diff}}=D\partial_x^2.
$$

Essi descrivono due meccanismi profondamente diversi:

- il drift genera una **traslazione rigida** del profilo;
- la diffusione genera uno **spreading** o **smoothing** del profilo.

Per capire questa differenza, conviene partire da un ragionamento sulla forma funzionale delle soluzioni, e poi passare all’interpretazione operatoriale.

# 2. Drift puro: ansatz di profilo rigido

Consideriamo l’equazione

$$
\partial_t p(x,t) = -v\,\partial_x p(x,t),
\qquad v \in \mathbb{R}.
$$

Questa è l’equazione di trasporto con velocità costante.

## 2.1 Ansatz

Se il profilo viene semplicemente trasportato senza deformarsi, è naturale cercare una soluzione nella forma

$$
p(x,t)=f(x-ct),
$$

dove $f$ è una funzione arbitraria e $c$ è una velocità da determinare.

Questo è lo stesso tipo di ansatz usato per le onde viaggianti: la dipendenza da $x$ e $t$ avviene solo attraverso la combinazione $x-ct$.

## 2.2 Verifica

Poniamo

$$
\xi=x-ct,
\qquad
p(x,t)=f(\xi).
$$

Allora

$$
\partial_t p=-c\,f'(\xi),
\qquad
\partial_x p=f'(\xi).
$$

Sostituendo nell’equazione,

$$
-c\,f'(\xi)=-v\,f'(\xi).
$$

Per un profilo non banale si deve avere

$$
c=v.
$$

Quindi la soluzione generale ha la forma

$$
p(x,t)=f(x-vt).
$$

Imponendo il dato iniziale $p(x,0)=p_0(x)$, si ottiene

$$
p(x,t)=p_0(x-vt).
$$

## 2.3 Interpretazione

Il profilo iniziale viene traslato rigidamente:

- la forma si conserva;
- non compaiono allargamento o smoothing;
- il centro del profilo si muove con legge

$$
x(t)=x_0+vt.
$$

L’operatore $-v\partial_x$ genera quindi un trasporto uniforme.

# 3. Formalismo esponenziale per il drift

Scriviamo l’equazione come

$$
\partial_t p = L_{\mathrm{drift}}p,
\qquad
L_{\mathrm{drift}}=-v\partial_x.
$$

Formalmente,

$$
p(t)=e^{tL_{\mathrm{drift}}}p_0 = e^{-vt\partial_x}p_0.
$$

Ora, usando la serie di Taylor,

$$
e^{-vt\partial_x}f(x) 
= \sum_{n=0}^{\infty}\frac{(-vt)^n}{n!}\partial_x^n f(x)
= f(x-vt).
$$

Dunque l’esponenziale dell’operatore derivata prima agisce come una traslazione:

$$
e^{-vt\partial_x}f(x)=f(x-vt).
$$

Per questo si dice che $-v\partial_x$ è il generatore infinitesimo delle traslazioni uniformi.

# 4. Diffusione pura: perché l’ansatz di traslazione non basta

Consideriamo ora l’equazione del calore

$$
\partial_t p(x,t)=D\,\partial_x^2 p(x,t),
\qquad D>0.
$$

Se provassimo a usare lo stesso ansatz rigido,

$$
p(x,t)=f(x-ct),
$$

otterremmo

$$
\partial_t p=-c f'(\xi),
\qquad
\partial_x^2 p=f''(\xi),
$$

e quindi

$$
-c f'(\xi)=D f''(\xi).
$$

Questa non è un’identità valida per una funzione arbitraria $f$: seleziona solo profili molto particolari.

Quindi, a differenza del caso del drift, la diffusione **non conserva genericamente la forma del dato iniziale**.  
Il profilo non si muove come un blocco rigido: cambia forma, si allarga, si smussa.

Questo mostra che per la diffusione bisogna cercare una struttura funzionale diversa.

# 5. Ansatz autosimile per la diffusione

Poiché la diffusione non trasporta rigidamente il profilo, ma lo allarga nel tempo, un ansatz naturale è

$$
p(x,t)=A(t)\,\Phi\!\left(\frac{x}{\ell(t)}\right),
$$

dove:

- $A(t)$ controlla l’altezza;
- $\ell(t)$ controlla la larghezza;
- $\Phi$ è il profilo ridotto.

Questa è una forma autosimile: il profilo può mantenere una struttura generale, ma con una scala spaziale che evolve nel tempo.

## 5.1 Calcolo delle derivate

Poniamo

$$
\xi=\frac{x}{\ell(t)},
\qquad
p(x,t)=A(t)\Phi(\xi).
$$

Allora

$$
\partial_t p = A'(t)\Phi(\xi)
- A(t)\frac{\ell'(t)}{\ell(t)}\,\xi\,\Phi'(\xi),
$$

mentre

$$
\partial_x^2 p = A(t)\frac{1}{\ell(t)^2}\Phi''(\xi).
$$

Sostituendo nell’equazione del calore,

$$
A'(t)\Phi(\xi) - A(t)\frac{\ell'(t)}{\ell(t)}\,\xi\,\Phi'(\xi)
= D\,A(t)\frac{1}{\ell(t)^2}\Phi''(\xi).
$$

Perché questa relazione possa separarsi in una parte temporale e una parte dipendente da $\xi$, è necessario che i coefficienti temporali abbiano la stessa scala. Questo porta alla condizione

$$
\frac{\ell'(t)}{\ell(t)} \sim \frac{D}{\ell(t)^2},
$$

cioè

$$
\ell'(t)\,\ell(t)\sim D.
$$

Integrando, si ottiene a livello di ordine di grandezza

$$
\ell(t)^2\sim Dt,
$$

e quindi

$$
\ell(t)\sim \sqrt{Dt}.
$$

## 5.2 Significato

La diffusione produce dunque una lunghezza caratteristica che cresce come

$$
\sqrt{Dt}.
$$

Questo è il segno distintivo della dinamica diffusiva:

- nel trasporto la distanza tipica cresce come $t$;
- nella diffusione cresce come $\sqrt{t}$.

# 6. La soluzione fondamentale: la gaussiana

L’ansatz autosimile suggerisce che la soluzione fondamentale dell’equazione del calore abbia una forma che si allarga come $\sqrt{Dt}$.  
In effetti, per il dato iniziale puntuale

$$
p(x,0)=\delta(x),
$$

si ottiene

$$
p(x,t)=
\frac{1}{\sqrt{4\pi Dt}}
\exp\!\left(-\frac{x^2}{4Dt}\right).
$$

Questa soluzione mostra esplicitamente che:

- la massa totale resta costante;
- il picco massimo si abbassa nel tempo;
- la larghezza cresce come $\sqrt{Dt}$.

La gaussiana è quindi il profilo fondamentale generato dall’operatore diffusivo.

# 7. Formalismo esponenziale per la diffusione

Anche nel caso diffusivo la soluzione si scrive formalmente come esponenziale di operatore:

$$
p(t)=e^{tL_{\mathrm{diff}}}p_0,
\qquad
L_{\mathrm{diff}}=D\partial_x^2.
$$

Quindi

$$
p(t)=e^{tD\partial_x^2}p_0.
$$

La differenza rispetto al drift non è nel formalismo, ma nell’azione concreta dell’esponenziale.

Per il drift,

$$
e^{-tv\partial_x}p_0(x)=p_0(x-vt),
$$

cioè una traslazione rigida.

Per la diffusione, invece,

$$
e^{tD\partial_x^2}p_0
$$

non produce una traslazione, ma una convoluzione con il kernel del calore.

# 8. L’esponenziale diffusivo come convoluzione gaussiana

Si ha infatti

$$
(e^{tD\partial_x^2}p_0)(x) =
\int_{\mathbb{R}}
\frac{1}{\sqrt{4\pi Dt}}
\exp\!\left(-\frac{(x-y)^2}{4Dt}\right)
p_0(y)\,dy.
$$

Cioè

$$
e^{tD\partial_x^2}p_0 = G_t * p_0,
$$

dove

$$
G_t(x)=\frac{1}{\sqrt{4\pi Dt}}e^{-x^2/(4Dt)}.
$$

Questa formula dice che il valore della soluzione in $x$ e al tempo $t$ è una media pesata dei valori iniziali vicini a $x$, con un peso gaussiano la cui larghezza cresce nel tempo.

In altre parole, l’operatore diffusivo sostituisce il profilo iniziale con una versione sempre più liscia e allargata.

# 9. Interpretazione in termini di frequenze

L’azione dell’operatore esponenziale diffusivo si capisce bene anche in trasformata di Fourier.

Se

$$
\widehat{p}(k,t)=\mathcal{F}[p(\cdot,t)](k),
$$

allora dall’equazione del calore segue

$$
\partial_t \widehat{p}(k,t) = -Dk^2 \widehat{p}(k,t),
$$

da cui

$$
\widehat{p}(k,t) = e^{-Dk^2 t}\widehat{p_0}(k).
$$

Questa formula mostra che le componenti ad alta frequenza, cioè i dettagli fini del profilo, vengono smorzate più rapidamente.  
La diffusione è quindi un meccanismo di smoothing.

# 10. Interpretazione locale della derivata seconda

Il significato geometrico di $\partial_x^2$ si vede anche localmente.

Poiché

$$
\partial_t p = D\partial_x^2 p,
$$

si ha:

- in un massimo locale, $\partial_x^2 p<0$, quindi $\partial_t p<0$: il massimo si "svuota";
- in un minimo locale, $\partial_x^2 p>0$, quindi $\partial_t p>0$: il minimo si "riempie".

Dunque la diffusione riduce i contrasti spaziali e tende ad appiattire il profilo.

# 11. Gruppo per il drift, semigruppo per la diffusione

Nel caso del drift, l’evoluzione è invertibile: una traslazione può essere annullata da una traslazione opposta.  
Formalmente, l’operatore

$$
e^{-tv\partial_x}
$$

fa parte di un gruppo.

Nel caso della diffusione, invece, l’evoluzione liscia il dato iniziale e perde informazione fine.  
Formalmente si ha un semigruppo

$$
e^{tD\partial_x^2},
\qquad t\ge 0,
$$

ma non un gruppo invertibile ben posto per tempi negativi.

Per questo si parla di **semigruppo del calore**.

# 12. Confronto finale

## Drift

Per

$$
\partial_t p=-v\partial_x p
$$

la soluzione è

$$
p(x,t)=p_0(x-vt).
$$

Quindi:

- la forma si conserva;
- il profilo si sposta rigidamente;
- la scala spaziale caratteristica cresce come $t$.

## Diffusione

Per

$$
\partial_t p=D\partial_x^2 p
$$

la soluzione è

$$
p(x,t)=e^{tD\partial_x^2}p_0
=
G_t*p_0.
$$

Quindi:

- la forma non si conserva in generale;
- il profilo si allarga e si liscia;
- la scala spaziale cresce come $\sqrt{Dt}$.

# 13. Messaggio conclusivo

I due operatori elementari

$$
-v\partial_x
\qquad\text{e}\qquad
D\partial_x^2
$$

hanno la stessa struttura formale di generatori di evoluzione, perché in entrambi i casi la soluzione si scrive come esponenziale di operatore:

$$
p(t)=e^{tL}p_0.
$$

Ma il loro effetto geometrico è completamente diverso.

- La derivata prima genera una **traslazione coerente** del profilo.
- La derivata seconda genera una **redistribuzione locale** della massa, cioè diffusione e smoothing.

Questa distinzione permette di leggere in modo intuitivo la Fokker--Planck

$$
\partial_t p = -\partial_x(ap) + \partial_x^2(Dp),
$$

in cui il primo termine trasporta la probabilità, mentre il secondo la redistribuisce diffusivamente.