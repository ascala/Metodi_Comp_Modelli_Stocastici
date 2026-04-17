---
title: "A10: Esponenziale del generatore, spettro e caso tempo-dipendente"
author: "Antonio Scala"
date: ""
---

# Obiettivi dell'appendice

Questa appendice approfondisce la soluzione formale della master equation in due direzioni.

La prima riguarda il caso autonomo: mostriamo come la struttura spettrale del generatore $L$ permetta di scrivere $e^{tL}$ in modo esplicito e di interpretare fisicamente ogni modo di rilassamento.

La seconda riguarda il caso tempo-dipendente: spieghiamo perche' la sostituzione $L \to L(t)$ non permette di scrivere semplicemente $e^{\int L(s)\,ds}$, introduciamo l'esponenziale ordinato, e mostriamo come da esso discendano naturalmente i principali schemi numerici.

# 1. Sviluppo spettrale di $e^{tL}$

## 1.1 Diagonalizzazione del generatore

Supponiamo che $L$ sia diagonalizzabile. Indichiamo con $\lambda_k$ i suoi autovalori e con $v^{(k)}$ i corrispondenti autovettori destri:

$$
L v^{(k)} = \lambda_k v^{(k)}.
$$

Indichiamo con $u^{(k)}$ gli autovettori sinistri, cioe' le soluzioni di

$$
u^{(k)\top} L = \lambda_k u^{(k)\top},
$$

normalizzati in modo che

$$
u^{(k)\top} v^{(j)} = \delta_{kj}.
$$

Grazie a questa biortogonalita', la matrice $L$ si decompone come

$$
L = \sum_k \lambda_k\, v^{(k)} u^{(k)\top}.
$$

## 1.2 Esponenziale in forma spettrale

Dalla definizione di esponenziale di matrice e dalla decomposizione precedente segue immediatamente

$$
e^{tL} = \sum_k e^{\lambda_k t}\, v^{(k)} u^{(k)\top}.
$$

La soluzione della master equation diventa quindi

$$
p(t) = e^{tL} p(0) = \sum_k c_k\, e^{\lambda_k t}\, v^{(k)},
\qquad
c_k = u^{(k)\top} p(0).
$$

I coefficienti $c_k$ sono le proiezioni della condizione iniziale sui *modi* (i.e. gli autovettori) del sistema. Ogni modo evolve autonomamente, con la propria scala temporale $\tau_k = -1/\lambda_k$.

## 1.3 Struttura degli autovalori del generatore

La struttura di bilancio della master equation impone vincoli precisi sullo spettro di $L$.

**Autovalore nullo.** Esiste sempre almeno un autovalore $\lambda_0 = 0$. L'autovettore destro corrispondente e' la distribuzione stazionaria $p^*$; l'autovettore sinistro e' il vettore costante $(1,1,\dots,1)^\top$, che codifica la conservazione della probabilita'.

**Parte reale non positiva.** Tutti gli autovalori soddisfano $\mathrm{Re}(\lambda_k)
\le 0$. Questo segue dalla struttura di $L$: gli elementi fuori diagonale sono non negativi, quelli diagonali sono tali che ogni colonna somma a zero. Una matrice con questa struttura non può avere autovalori con parte reale positiva.

**Rilassamento verso lo stazionario.** Se $\lambda_0 = 0$ e' l'unico autovalore nullo (processo ergodico), allora per $t \to \infty$ tutti i modi transienti decadono e

$$
p(t) \;\xrightarrow{t \to \infty}\; c_0\, v^{(0)} = p^*.
$$

**Tempo di mescolamento.** La velocita' di convergenza alla stazionaria e' controllata dall'autovalore con $\mathrm{Re}(\lambda_k)$ piu' vicino a zero tra quelli diversi da $\lambda_0$. Lo indichiamo con $\lambda_1$ e definiamo la scala di rilassamento globale

$$
\tau_{\mathrm{mix}} = \frac{-1}{\mathrm{Re}(\lambda_1)}.
$$

Quanto piu' $|\lambda_1|$ e' piccolo, tanto piu' lentamente il sistema dimentica le
condizioni iniziali.

## 1.4 Esempio: il caso a due stati

Nel caso a due stati con tassi $\alpha$ e $\beta$, il generatore e'

$$
L =
\begin{pmatrix}
-\alpha & \beta \\
\alpha & -\beta
\end{pmatrix}.
$$

Gli autovalori sono $\lambda_0 = 0$ e $\lambda_1 = -(\alpha+\beta)$.

L'autovettore destro associato a $\lambda_0$ e' la distribuzione stazionaria

$$
v^{(0)} =
\frac{1}{\alpha+\beta}
\begin{pmatrix}\beta \\ \alpha\end{pmatrix}.
$$

Il modo transiente decade con scala temporale $\tau = 1/(\alpha+\beta)$, coerentemente con la soluzione diretta della sezione 4 della dispensa principale.

Lo sviluppo spettrale non aggiunge informazione nuova in questo caso, ma rende esplicita la decomposizione: la soluzione e' la sovrapposizione di uno stazionario e di un transitorio, ciascuno con il proprio peso determinato dalla condizione iniziale.

# 2. Il caso con generatore tempo-dipendente

## 2.1 Perche' $e^{\int L(s)\,ds}$ non e' la soluzione

Supponiamo ora che i tassi di transizione dipendano dal tempo. Il generatore diventa $L(t)$ e la master equation si scrive

$$
\dot p(t) = L(t)\, p(t).
$$

Nel caso autonomo la soluzione era $p(t) = e^{tL}p(0)$. Per verificarlo basta derivare termine a termine la serie corrispondente all'esponenziale di una matrice, ottenendo $\frac{d}{dt}e^{tL} = L e^{tL}$ e quindi $\dot p = L p$. Questo funziona perche' $L$ e' costante e la derivata dell'esponenziale rispetto al parametro che appare linearmente nell'esponente segue la regola usuale.

Nel caso tempo-dipendente si potrebbe tentare la formula analoga

$$
p(t) = \exp\!\left(\int_0^t L(s)\,ds\right) p(0)\,.
$$

Proviamo a verificarla derivando. Chiamiamo $M(t) = \int_0^t L(s)\,ds$, cosicche' la formula proposta e' $p(t) = e^{M(t)} p(0)$. La derivata di $e^{M(t)}$ rispetto a $t$ non e' semplicemente $\dot M(t)\, e^{M(t)} = L(t)\, e^{M(t)}$: questa
identita' vale per scalari, ma per matrici la derivata dell'esponenziale ha una forma piu' complessa che coinvolge tutti i termini della serie di potenze. In particolare,

$$
\frac{d}{dt} e^{M(t)} = L(t)\,e^{M(t)}
$$

e' vera solo se $L(t)$ e $M(t)$ si possono scambiare nell'ordine del prodotto per ogni $t$. Questo e' garantito nel caso autonomo ($L$ costante, per cui $M(t)=tL$ e' proporzionale a $L$ stessa), ma in generale non lo e'. La condizione $L(t)\,M(t) = M(t)\,L(t)$ ovvero $M$ e $L$ *commutano* si verifica calcolando il *commutatore* 

$$
[A,B] \overset{\mathrm{def}}{=} A\,B-B\,A
$$
e verificando che sia zero.

La formula $p(t) = e^{M(t)} p(0)$ e' quindi sbagliata nel caso tempo-dipendente.

## 2.2 L'esponenziale ordinato nel tempo

La soluzione formale esatta si scrive tramite l'**esponenziale ordinato nel tempo**:

$$
p(t) = \mathcal{T}\exp\!\left(\int_0^t L(s)\,ds\right) p(0).
$$

Il simbolo $\mathcal{T}$ indica che nelle espansioni in serie i fattori vanno moltiplicati con l'istante piu' recente sempre a sinistra. La definizione costruttiva e':

$$
\mathcal{T}\exp\!\left(\int_0^t L(s)\,ds\right)
= \lim_{N\to\infty}
e^{L(t_N)\Delta t}\cdots e^{L(t_1)\Delta t}\,e^{L(t_0)\Delta t},
$$

dove $\Delta t = t/N$ e $t_k = k\,\Delta t$. Ogni fattore propaga la distribuzione
sull'intervallino $[t_k, t_{k+1}]$ trattando $L$ come costante su quell'intervallo;
i fattori si compongono nell'ordine cronologico corretto.

Se i commutatori $[L(t), L(s)]$ sono nulli per ogni coppia $(t,s)$, l'ordine non importa e si recupera $e^{\int_0^t L(s)\,ds}$. Ad esempio, se $L(t)$ ha una forma del tipo $\lambda(t) f(A)$ con $A$ matrice costante e $\lambda(t)$ scalare, allora$[L(t), L(s)]=0$ e si può scrivere  

$$
p(t) = \exp\!\left(f(A)\int_0^t \lambda(s)\,ds\right) p(0).
$$

## 2.3 Serie di Magnus

Una rappresentazione alternativa e' la **serie di Magnus**, che scrive l'esponenziale ordinato come singolo esponenziale:

$$
\mathcal{T}\exp\!\left(\int_0^t L(s)\,ds\right) = e^{\Omega(t)}.
$$

Per scrivere i termini di questa serie occorre introdurre il **commutatore** di due
matrici $A$ e $B$, definito come

$$
[A,\, B] = AB - BA.
$$

Il commutatore misura quanto $A$ e $B$ non si scambiano nell'ordine del prodotto: e' nullo se e solo se $AB = BA$. E' proprio la non-nullita' di $[L(t), L(s)]$ per $t
\neq s$ che rende impossibile ridurre l'esponenziale ordinato a un semplice esponenziale dell'integrale.

L'esponente $\Omega(t)$ e' dato da una serie di integrali annidati di commutatori:

$$
\Omega(t) = \underbrace{\int_0^t L(s)\,ds}_{\Omega_1}
- \frac{1}{2}\underbrace{\int_0^t\!\int_0^{s_1}[L(s_1),L(s_2)]\,ds_2\,ds_1}_{\Omega_2} + \cdots
$$

Il primo termine $\Omega_1$ e' la semplice media temporale del generatore. I termini $\Omega_2, \Omega_3, \ldots$ correggono per la non-commutativita' di $L$ a tempi
diversi. Se il generatore varia lentamente, i commutatori $[L(s_1), L(s_2)]$ sono piccoli e la serie converge rapidamente al primo termine.

# 3. Approssimazioni numeriche

Le rappresentazioni del caso tempo-dipendente suggeriscono naturalmente diversi schemi per l'integrazione numerica della master equation.

## 3.1 Splitting di Lie

La costruzione dell'esponenziale ordinato per prodotto finito porta direttamente allo **splitting di Lie**: si approssima

$$
p(t + \Delta t) \approx e^{L(t)\,\Delta t}\, p(t).
$$

A ogni passo si propaga la distribuzione con il generatore "congelato" al valore corrente. L'errore locale e' $O((\Delta t)^2)$, legato al commutatore trascurato; l'errore globale su un intervallo fisso e' quindi $O(\Delta t)$.

Il vantaggio e' che la matrice $e^{L(t)\Delta t}$ e' una matrice stocastica: mappa
distribuzioni di probabilita' in distribuzioni di probabilita', cioe' preserva la non-negativita' e la normalizzazione per qualunque $\Delta t > 0$.

## 3.2 Schema di Eulero esplicito

Se si approssima anche l'esponenziale al primo ordine,

$$
e^{L(t)\Delta t} \approx I + L(t)\,\Delta t,
$$

si ottiene lo **schema di Eulero esplicito**:

$$
p(t+\Delta t) \approx \bigl(I + L(t)\,\Delta t\bigr)\, p(t).
$$

Questo e' lo stesso schema che si userebbe per qualunque ODE lineare. L'ordine di accuratezza rimane $O(\Delta t)$, ma ora compare un vincolo aggiuntivo: la matrice $I + L(t)\Delta t$ puo' avere elementi negativi se $\Delta t$ e' troppo grande, violando la non-negativita' della distribuzione.

La condizione sufficiente per la non-negativita' discende dagli elementi diagonali:

$$
1 + L_{ii}\,\Delta t \ge 0
\quad \Longrightarrow \quad
\Delta t \le \frac{1}{\max_i |L_{ii}|} = \frac{1}{\max_i \sum_{j \neq i} w_{i\to j}}.
$$

Questa e' la condizione di stabilita' (analoga alla condizione CFL nei metodi alle differenze finite per PDE iperboliche) per lo schema di Eulero applicato alla master equation.

## 3.3 Magnus al primo ordine

Se $L(t)$ varia lentamente, si puo' usare il primo termine della serie di Magnus sull'intervallo $[t, t+\Delta t]$:

$$
p(t+\Delta t) \approx \exp\!\left(\bar L\,\Delta t\right) p(t),
\qquad
\bar L = \frac{1}{\Delta t}\int_t^{t+\Delta t} L(s)\,ds.
$$

Questo schema e' ancora del primo ordine, ma tiene conto della variazione media di $L$ sull'intervallo invece di congelarlo al valore iniziale. Ha senso quando $L(t)$ e' nota analiticamente o quando il suo integrale e' calcolabile a basso costo.

## 3.4 Riepilogo

| Schema | Aggiornamento | Ordine | Conserva $p \ge 0$? |
|---|---|---|---|
| Eulero esplicito | $(I + L\Delta t)\,p$ | 1 | solo se $\Delta t \le 1/\max_i \vert L_{ii} \vert$ |
| Splitting di Lie | $e^{L(t)\Delta t}\,p$ | 1 | sempre |
| Magnus ordine 1 | $e^{\bar L\Delta t}\,p$ | 1 | sempre |

Tutti gli schemi sono del primo ordine in $\Delta t$. Per ordini superiori occorre
includere i commutatori (termini di Magnus di ordine piu' alto) o usare metodi di Runge--Kutta adattati alle equazioni matriciali.

> **Nota.** Nel caso autonomo ($L$ costante) tutti gli schemi coincidono e la soluzione esatta $e^{tL}p(0)$ non e' un'approssimazione ma la soluzione precisa, per qualunque $t$.
