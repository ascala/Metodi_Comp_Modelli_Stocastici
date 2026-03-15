---
title: "Laboratorio 02 -- Metodi Monte Carlo"
author: "Antonio Scala"
date: "17 Marzo 2026"
---

# Obiettivi del laboratorio

In questo laboratorio useremo il metodo Monte Carlo per stimare lo stesso integrale con tre strategie diverse.

L'obiettivo non e' solo ottenere il valore corretto, ma capire:

- come costruire uno stimatore Monte Carlo;
- come misurare l'errore statistico;
- come l'errore scala con $N$;
- come tecniche diverse possono ridurre la varianza.

Confronteremo tre metodi:

1. campionamento uniforme;
2. variabili antitetiche;
3. importance sampling.

# Il problema

Vogliamo stimare numericamente
$$
I = \int_0^1 \frac{1}{1+x^2}\,dx.
$$
Il valore esatto e'
$$
I = \frac{\pi}{4}.
$$
Questo permette di valutare direttamente l'errore degli stimatori.

# Parte A -- Monte Carlo diretto

Se $U \sim \mathrm{Unif}(0,1)$ allora
$$
I = \mathbb{E}\left[\frac{1}{1+U^2}\right].
$$
Uno stimatore Monte Carlo e' quindi
$$
\hat I_N =
\frac{1}{N}\sum_{i=1}^N
\frac{1}{1+U_i^2}
$$
con $U_i$ indipendenti uniformi in $[0,1]$.

## Compiti

1. Implementare lo stimatore.
2. Calcolare $\hat I_N$ per $N = 10, 10^2, 10^3, 10^4, 10^5$.
3. Confrontare il risultato con $\pi/4$.

## Pseudocodice

```text
function stima_uniforme(N):
    somma = 0
    for i in 1,...,N:
        u = uniforme(0,1)
        somma = somma + 1/(1+u^2)
    return somma / N
```

# Parte B -- Errore statistico e distribuzione dello stimatore

Uno stimatore Monte Carlo e' una media campionaria. Se la varianza della variabile campionata e' finita, la deviazione standard della media scala come
$$
\mathrm{std}(\hat I_N) \propto \frac{1}{\sqrt{N}}.
$$
In questa parte vogliamo verificare come scala l'errore statistico con $N$ e come e' distribuito lo stimatore $\hat I_N$.

## Distribuzione delle stime e scaling dell'errore

Per un valore fissato di $N$, ripetere la stima Monte Carlo $M$ volte (ad esempio $M=200$ oppure $M=500$), ottenendo una collezione di stime $\hat I_N^{(1)}, \hat I_N^{(2)}, \dots, \hat I_N^{(M)}$, e costruire l'istogramma. La distribuzione sembra approssimativamente gaussiana? Dove si trova il centro? Quanto e' larga? Ripetere per almeno due valori diversi di $N$.

Per studiare come cambia la dispersione, usare una lista di valori di $N$, ad esempio
$$
N = 20, 50, 100, 200, 500, 1000, 2000,
$$
e per ciascun valore calcolare la deviazione standard empirica delle $M$ stime. Costruire il grafico log--log di $\mathrm{std}(\hat I_N)$ vs $N$: se la teoria e' corretta, dovrebbe valere $\mathrm{std}(\hat I_N) \sim N^{-1/2}$, che nel grafico log--log corrisponde a una retta di pendenza $-1/2$. Eseguire un fit lineare e stimare la pendenza osservata.

L'istogramma delle stime mostra empiricamente il comportamento previsto dal teorema del limite centrale:
$$
\hat I_N \approx \mathcal{N}\!\left(I,\frac{\sigma^2}{N}\right).
$$

## Domande guida

1. La pendenza osservata e' vicina a $-1/2$?
2. Quanto rumore rimane nel grafico?
3. Che cosa succede se il numero di repliche $M$ e' troppo piccolo?
4. Aumentando $N$, cosa succede alla larghezza dell'istogramma delle stime?
5. Usando la varianza stimata, quanti campioni sono necessari affinche' l'errore statistico tipico sia dell'ordine di $10^{-3}$? Quanto aumenta $N$ se vogliamo migliorare la precisione di un fattore 10?

## Suggerimento pratico (Python)

```python
import numpy as np
import matplotlib.pyplot as plt

# istogramma delle stime
plt.hist(stime, bins=20, density=True)
plt.axvline(np.pi/4, linestyle='--')
plt.xlabel('stima')
plt.ylabel('densita')
plt.show()

# deviazione standard empirica
sigma_emp = np.std(stime, ddof=1)
print(sigma_emp)

# grafico log--log
plt.loglog(Nlist, err, 'o-')
plt.xlabel('N')
plt.ylabel('std stimatore')
plt.show()
```

# Parte C -- Variabili antitetiche

La funzione $f(x) = 1/(1+x^2)$ e' monotona decrescente. Possiamo usare coppie antitetiche $(U,1-U)$ e costruire lo stimatore
$$
\hat I_N^{\mathrm{anti}} =
\frac{1}{N}\sum_{i=1}^N
\frac{f(U_i)+f(1-U_i)}{2}.
$$

## Compiti e domande

1. Implementare lo stimatore antitetico.
2. Ripetere gli esperimenti della Parte B.
3. Confrontare la deviazione standard con il metodo uniforme.
4. Lo stimatore e' corretto? La varianza e' minore? Di quanto migliora la precisione?

## Pseudocodice

```text
function stima_antitetica(N):
    somma = 0
    for i in 1,...,N:
        u = uniforme(0,1)
        y = 0.5*(1/(1+u^2) + 1/(1+(1-u)^2))
        somma = somma + y
    return somma / N
```

# Parte D -- Importance sampling

Se scegliamo una densita' $q(x)$ su $[0,1]$ possiamo scrivere
$$
I = \int_0^1 \frac{f(x)}{q(x)} q(x)\,dx = \mathbb{E}_q\!\left[\frac{f(X)}{q(X)}\right]
$$
con $X \sim q$. Usiamo $q(x) = 2(1-x)$, che e' una densita' valida su $[0,1]$ con funzione di ripartizione $F(x) = 2x - x^2$ e inversa $F^{-1}(u) = 1 - \sqrt{1-u}$.

Lo stimatore e'
$$
\hat I_N =
\frac{1}{N}\sum_{i=1}^N \frac{f(X_i)}{q(X_i)} =
\frac{1}{N}\sum_{i=1}^N \frac{1}{2(1-X_i)(1+X_i^2)}
$$
con $X_i$ campionati da $q$.

## Compiti e domande

1. Implementare lo stimatore.
2. Lo stimatore e' corretto? La varianza e' maggiore o minore del caso uniforme? Questa scelta di $q$ e' efficace?

## Pseudocodice

```text
function campiona_q():
    u = uniforme(0,1)
    return 1 - sqrt(1-u)

function stima_importance(N):
    somma = 0
    for i in 1,...,N:
        x = campiona_q()
        somma = somma + 1/((1+x^2) * 2*(1-x))
    return somma / N
```

# Parte E -- Confronto finale

Confrontare i tre metodi calcolando per ciascuno: media delle stime, deviazione standard, errore rispetto a $\pi/4$.

1. Quale metodo e' piu' efficiente?
2. Quale riduce maggiormente la varianza?
3. Quando conviene usare importance sampling?

# Estensione opzionale

Considerare la famiglia
$$
q_\alpha(x) = (\alpha+1)(1-x)^\alpha, \qquad \alpha > -1.
$$

1. Come si campiona da $q_\alpha$?
2. Esiste un valore di $\alpha$ che riduce ulteriormente la varianza?

# Consegna

Ogni gruppo deve produrre:

1. codice delle tre implementazioni;
2. grafico dell'errore statistico vs $N$;
3. tabella di confronto delle varianze;
4. breve commento sui risultati.

---

# Appendice -- Compito addizionale: medie con peso di Boltzmann

In molte applicazioni interessa stimare quantita' del tipo
$$
\langle O \rangle =
\frac{\int O(x)e^{-V(x)}\,dx}{\int e^{-V(x)}\,dx}.
$$
In questa appendice proponiamo due casi: buca parabolica e doppia buca. L'obiettivo e' capire come stimare numeratore, denominatore e rapporto, come propagare l'errore, e come sfruttare simmetria, correlazione tra stime e decomposizione dell'integrale in sottointervalli.

# 1. Formula generale

Definiamo
$$
A = \int O(x)e^{-V(x)}\,dx,
\qquad
Z = \int e^{-V(x)}\,dx,
\qquad
\langle O \rangle = \frac{A}{Z}.
$$
Stimiamo separatamente $\hat A$ e $\hat Z$, e poi costruiamo
$$
\widehat{\langle O \rangle} = \frac{\hat A}{\hat Z}.
$$

# 2. Errore del rapporto

Sia $R = A/Z$. Sviluppando al primo ordine attorno ai valori medi di $A$ e $Z$:
$$
\delta R \approx
\frac{\partial R}{\partial A}\,\delta A
+
\frac{\partial R}{\partial Z}\,\delta Z
= \frac{1}{Z}\,\delta A - \frac{A}{Z^2}\,\delta Z.
$$
Passando alla varianza:

$$
\mathrm{Var}(R) \approx \frac{\mathrm{Var}(A)}{Z^2} + \frac{A^2}{Z^4}\mathrm{Var}(Z) - 2\frac{A}{Z^3}\mathrm{Cov}(A,Z).
$$

Dividendo per $R^2 = A^2/Z^2$ si ottiene la forma relativa

$$
\frac{\mathrm{Var}(R)}{R^2} \approx \frac{\mathrm{Var}(A)}{A^2} +
\frac{\mathrm{Var}(Z)}{Z^2} - 2\frac{\mathrm{Cov}(A,Z)}{AZ}.
$$

## Osservazioni

1. Questa formula deriva da uno sviluppo al primo ordine, quindi e' affidabile quando le fluttuazioni di $A$ e $Z$ sono piccole rispetto ai loro valori medi. Se gli errori sono grandi oppure se $Z$ puo' avvicinarsi a zero, l'approssimazione puo' non essere adeguata.
2. Se si usano gli stessi numeri casuali per stimare $\hat A$ e $\hat Z$, si introduce correlazione. Se la covarianza e' positiva, il termine finale riduce la varianza del rapporto: usare gli stessi campioni puo' migliorare la precisione.

# 3. Simmetria del potenziale

Se il potenziale e' pari, $V(-x)=V(x)$, anche il peso di Boltzmann e' pari. Ogni osservabile $f$ si puo' decomporre in una parte pari e una dispari:
$$
f(x)=f_{\mathrm{sym}}(x)+f_{\mathrm{asym}}(x),
$$
con
$$
f_{\mathrm{sym}}(x)=\frac{f(x)+f(-x)}{2},
\qquad
f_{\mathrm{asym}}(x)=\frac{f(x)-f(-x)}{2}.
$$
Su un intervallo simmetrico $[-L,L]$ la parte dispari non contribuisce:
$$
\int_{-L}^L f(x)e^{-V(x)}\,dx =
2\int_0^L f_{\mathrm{sym}}(x)e^{-V(x)}\,dx.
$$
Se il potenziale e' simmetrico, si puo' quindi dimezzare il dominio di integrazione.

# 4. Caso A -- Buca parabolica

## Potenziale e stimatori

Considerare $V(x)=x^2/2$ su un intervallo simmetrico $[-x_{\max},x_{\max}]$ con $x_{\max}$ abbastanza grande da rendere trascurabile il contributo delle code. Con $X \sim \mathrm{Unif}([-x_{\max},x_{\max}])$:
$$
\hat A =
\frac{2x_{\max}}{N}\sum_{i=1}^N O(X_i)e^{-V(X_i)},
\qquad
\hat Z =
\frac{2x_{\max}}{N}\sum_{i=1}^N e^{-V(X_i)},
\qquad
\widehat{\langle O\rangle}=\frac{\hat A}{\hat Z}.
$$
Usare almeno due osservabili tra $O(x)=x$, $O(x)=x^2$, $O(x)=x^4$.

## Consegne e domande

1. Scegliere $x_{\max}$ e motivare la scelta.
2. Stimare $\hat A$, $\hat Z$ e $\widehat{\langle O\rangle}$.
3. Stimare l'errore del rapporto usando la formula con covarianza.
4. Confrontare campioni indipendenti vs stessi campioni per $\hat A$ e $\hat Z$: la precisione migliora?
5. Ripetere il calcolo con: intervallo completo, coppie antitetiche $(x,-x)$, semiasse positivo con la formula di simmetria.
6. Per $O(x)=x$, che cosa ci si aspetta? Per $O(x)=x^2$, quanto aiuta la simmetria?

# 5. Caso B -- Doppia buca

## Potenziale e consegne

Considerare $V(x)=a(x^2-b^2)^2$ con $a=1$, $b=1$, su un intervallo simmetrico $[-x_{\max},x_{\max}]$. Definire $A$, $Z$ e $\langle O\rangle$ come nel caso precedente.

1. Ripetere il calcolo fatto per la buca parabolica.
2. Usare almeno un'osservabile pari e una dispari.
3. Verificare l'effetto della simmetria.
4. Confrontare campioni indipendenti e campioni condivisi tra numeratore e denominatore.

# 6. Decomposizione a pezzi

Scrivere $A=\sum_j A_j$, $Z=\sum_j Z_j$ dove $A_j$ e $Z_j$ sono gli integrali ristretti a sottointervalli $I_j$ che formano una partizione di $[-x_{\max},x_{\max}]$. Ad esempio, dividere in tre parti: regione sinistra, centrale, destra.

## Consegne e domande

1. Stimare separatamente i contributi di ciascun sottointervallo, sommarli e confrontare con la stima globale.
2. Dove si concentra il contributo maggiore a $Z$? E ad $A$?
3. Conviene assegnare lo stesso numero di campioni a tutti i sottointervalli?
4. In quali regioni la precisione locale e' piu' importante?

## Pseudocodice

```text
function stima_A_Z(N, xmin, xmax, O, V):
    somma_A = 0; somma_Z = 0
    for i in 1,...,N:
        x = uniforme(xmin, xmax)
        w = exp(-V(x))
        somma_A = somma_A + O(x)*w
        somma_Z = somma_Z + w
    A_hat = (xmax-xmin) * somma_A / N
    Z_hat = (xmax-xmin) * somma_Z / N
    return A_hat, Z_hat

function stima_a_pezzi(Nlist, intervalli, O, V):
    A_tot = 0; Z_tot = 0
    for ogni intervallo I_j:
        A_j, Z_j = stima_A_Z(Nlist[j], I_j.min, I_j.max, O, V)
        A_tot = A_tot + A_j
        Z_tot = Z_tot + Z_j
    return A_tot / Z_tot
```

# 7. Consegna e domande finali

Ogni studente o gruppo deve produrre: scelta del potenziale e dell'osservabile; scelta di $x_{\max}$ e motivazione; stima di $\hat A$, $\hat Z$ e del rapporto con il relativo errore; confronto tra campioni indipendenti, campioni condivisi, uso della simmetria e integrazione a pezzi nella doppia buca; breve commento finale.

1. Qual e' l'effetto della simmetria del potenziale?
2. Qual e' l'effetto della covarianza tra numeratore e denominatore?
3. Quando conviene usare gli stessi numeri casuali?
4. Nel caso della doppia buca, dove conviene concentrare il campionamento?
