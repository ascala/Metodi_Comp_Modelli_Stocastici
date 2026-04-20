---
title: "LAB07: Branching, estinzione e funzione generatrice"
author: "Antonio Scala"
date: ""
---

# Obiettivi

In questo laboratorio studiamo il processo di Galton--Watson a tre livelli di descrizione progressivamente piu' astratti:

1. traiettorie singole;
2. statistiche empiriche su molte realizzazioni;
3. descrizione analitica tramite la funzione generatrice.

L'idea guida e' mostrare operativamente che:

- la media da sola non basta a descrivere il processo;
- l'estinzione puo' avvenire anche quando $m>1$;
- la funzione generatrice permette di calcolare in modo esatto ed efficiente la probabilita' di estinzione e la probabilita' di essere estinti alla generazione $t$.

Al termine del laboratorio dovreste essere in grado di:

1. simulare traiettorie di un processo di Galton--Watson;
2. stimare empiricamente la probabilita' di estinzione;
3. confrontare la crescita della media con la legge teorica $m^t$;
4. implementare la funzione generatrice per una distribuzione di offspring semplice;
5. calcolare la probabilita' di estinzione tramite iterazione del punto fisso $q_{n+1}=G(q_n)$;
6. calcolare $P(N_t=0)=G^{\circ t}(0)$ iterando numericamente $G$;
7. confrontare il risultato numerico con la stima Monte Carlo.

---

# Strategia del laboratorio

In questo laboratorio dovete tenere distinti tre livelli diversi di descrizione:

1. una singola traiettoria $N_t$;
2. una media o frequenza empirica ottenuta da molte traiettorie;
3. una quantita' calcolata direttamente tramite la funzione generatrice.

Una parte importante del laboratorio consiste proprio nel confrontare questi tre livelli e nel non confonderli.

# Il modello

Consideriamo un processo di Galton--Watson: il tempo e' discreto, scandito in generazioni $t=0,1,2,\dots$, e il numero di individui evolve secondo

$$
N_{t+1} = \sum_{i=1}^{N_t} K_i\;,
$$

dove i $K_i$ sono indipendenti e identicamente distribuiti con legge di offspring $(p_k)$.

La quantita' centrale della lezione e' la probabilita' di estinzione finale

$$
q = P(\exists\, t : N_t = 0 \mid N_0 = 1)\;,
$$

che soddisfa l'equazione ai punti fissi $q = G(q)$, dove

$$
G(s) = \sum_{k=0}^{\infty} p_k s^k
$$

e' la funzione generatrice dell'offspring.

# Distribuzione di offspring usata nel laboratorio

Per mantenere semplice la parte numerica, useremo principalmente la distribuzione binaria

$$
P(K=0) = 1-p\;, \qquad P(K=2) = p\;,
$$

con $p \in [0,1]$. Per questa distribuzione:

$$
G(s) = (1-p) + p\,s^2\;, \qquad m = 2p\;.
$$

I tre regimi corrispondono a:

- subcritico: $p < 1/2$, cioe' $m < 1$;
- critico: $p = 1/2$, cioe' $m = 1$;
- supercritico: $p > 1/2$, cioe' $m > 1$.

La probabilita' di estinzione vale:

$$
q = \begin{cases}
1 & \text{se } p \le 1/2\;, \\
\dfrac{1-p}{p} & \text{se } p > 1/2\;.
\end{cases}
$$

# Scheletro di codice

Il codice e' distribuito in quattro moduli, da completare nell'ordine:

1. `gw_core.py` -- campionamento dell'offspring e simulazione di una traiettoria;
2. `gw_simulation.py` -- simulazioni multiple e stime empiriche;
3. `gw_generating_function.py` -- funzione generatrice e iterazioni;
4. `gw_plots.py` -- grafici.

Ogni modulo importa dal precedente. Prima di passare alla parte successiva,
verificate che le funzioni del modulo corrente restituiscano risultati sensati
su qualche caso semplice.

---

# Parte A -- Traiettorie e loro variabilita'

## A1 -- Fascio di traiettorie

Per ciascuno dei tre valori

$$
p = 0.3 \quad (m=0.6)\;, \qquad
p = 0.5 \quad (m=1.0)\;, \qquad
p = 0.7 \quad (m=1.4)\;,
$$

simulate 30 traiettorie con $N_0 = 1$ e $T = 20$ generazioni, e rappresentatele tutte sullo stesso grafico.

Aggiungete, sullo stesso grafico, la curva teorica della media:

$$
\mathbb{E}[N_t] = m^t.
$$

### Domande

1. Nel caso subcritico le traiettorie si comportano come ci si aspetta dalla media?
2. Nel caso critico la media e' costante: le traiettorie lo sono?
3. Nel caso supercritico quante traiettorie sopravvivono fino a $T=20$?
   Quante si estinguono nelle prime generazioni?
4. Cosa succede alla media empirica quando molte traiettorie si estinguono
   ma poche crescono molto?

## A2 -- Effetto della condizione iniziale

Ripetete A1 nel caso supercritico $p=0.7$ con

$$
N_0 = 1\;, \qquad N_0 = 5\;, \qquad N_0 = 20\;.
$$

### Domanda

Come cambia la probabilita' empirica di estinzione al crescere di $N_0$?
Riuscite a collegare la risposta alla formula $P(\text{estinzione} \mid N_0=n) = q^n$?

---

# Parte B -- Stime empiriche di estinzione e crescita

## B1 -- Stima della probabilita' di estinzione finale

Simulate $M = 1000$ traiettorie con $N_0=1$ e $T=50$ generazioni,
per valori di $p$ su una griglia da $0.1$ a $0.9$.

Per ogni valore di $p$, stimate

$$
\hat{q}(p) = \frac{\text{numero di traiettorie con } N_{50}=0}{M}\;.
$$

Rappresentate $\hat{q}(p)$ in funzione di $p$ e sovrapponete la curva teorica

$$
q(p) = \begin{cases} 
1 & p \le 1/2\;, \\ 
(1-p)/p & p > 1/2\;. 
\end{cases}
$$

### Domande

1. La stima empirica coincide con il valore teorico?
2. Come cambia la qualita' della stima aumentando $M$?
3. Perche' per $p$ vicino a $1/2$ la stima e' piu' rumorosa?

## B2 -- Crescita della media

Per $p = 0.7$, stimate la media empirica $\hat{\mathbb{E}}[N_t]$ a ogni generazione
su $M = 500$ traiettorie. Rappresentate nel grafico sia $\hat{\mathbb{E}}[N_t]$
che la legge teorica $m^t = (2p)^t$.

Ripetete il grafico calcolando anche la media condizionata alle sole traiettorie
ancora vive alla generazione $t$.

### Domande

1. La media empirica (su tutte le traiettorie) segue $m^t$? Per quante generazioni?
2. Come mai la media empirica puo' risultare molto rumorosa anche con $M=500$?
3. Cosa succede alla media condizionata ai sopravvissuti rispetto alla media totale?
4. Perche' "media crescente" non significa "sopravvivenza quasi certa"?

---

# Parte C -- Funzione generatrice e calcolo numerico dell'estinzione

## C1 -- Visualizzazione di $G$ e del punto fisso

Su una griglia di punti $s \in [0,1]$, disegnate:

- la curva $y = G(s) = (1-p) + p\,s^2$;
- la retta $y = s$.

Fate il grafico per i tre valori $p=0.3$, $p=0.5$, $p=0.7$.

### Domande

1. In quanti punti si intersecano la curva e la retta in ciascun caso?
2. La curva e' convessa? Riconoscete l'argomento geometrico della sezione 6.2 delle dispense?
3. Dove si trova il punto fisso $q<1$ nel caso supercritico?
   Corrisponde al valore analitico $(1-p)/p$?

## C2 -- Calcolo di $q$ tramite iterazione

La probabilita' di estinzione e' il piu' piccolo punto fisso di $G$ in $[0,1]$.
Partendo da $q_0 = 0$, iterate

$$
q_{n+1} = G(q_n)\;,
$$

fino a convergenza (ad esempio finche' $|q_{n+1} - q_n| < 10^{-10}$).

Fate questo per $p = 0.3$, $p = 0.5$ e $p = 0.7$.

Visualizzate la convergenza rappresentando $q_n$ in funzione di $n$
e aggiungete come linea orizzontale il valore analitico.

### Domande

1. Quante iterazioni servono per raggiungere la convergenza nei tre casi?
2. La convergenza e' piu' lenta vicino a $p = 1/2$? Perche'?
3. Cosa succede se si parte da $q_0 = 1$ invece che da $q_0 = 0$?
   A quale punto fisso converge?

## C3 -- Probabilita' di estinzione entro $t$ generazioni

Ricordiamo che per $N_0=1$ la funzione generatrice di $N_t$ e'

$$
F_t(s) = G^{\circ t}(s)\;,
$$

dove $G^{\circ t}$ indica l'iterata $t$-esima di $G$. In particolare,

$$
P(N_t = 0) = F_t(0) = G^{\circ t}(0)\;.
$$

Calcolate $G^{\circ t}(0)$ per $t = 0, 1, \dots, 50$ nei tre casi.
Il calcolo e' semplice: si parte da $s_0 = 0$ e si itera $s_{t+1} = G(s_t)$.

Confrontate la curva $G^{\circ t}(0)$ con la frequenza empirica di estinzione
entro la generazione $t$ stimata nella Parte B.

### Domande

1. Le due curve (iterazione di $G$ e stima Monte Carlo) coincidono?
2. Nel caso subcritico, come si comporta $G^{\circ t}(0)$ per $t$ grande?
3. Nel caso supercritico, $G^{\circ t}(0)$ converge a $1$ oppure a un valore $<1$?
4. Qual e' il vantaggio computazionale dell'iterazione della generatrice
   rispetto al Monte Carlo?

---

# Parte D -- Estensione facoltativa

## D1 -- Distribuzione completa di $N_t$

Provate a ricavare numericamente la distribuzione completa di $N_t$
senza usare simulazioni, sfruttando il fatto che $N_{t+1}$ e' somma
di un numero casuale di variabili indipendenti con la distribuzione di offspring.

Troncate la distribuzione a un massimo $k_{\max}$ (ad esempio $50$ o $100$)
e iterate la convoluzione generazione per generazione.

## D2 -- Confronto con Monte Carlo

Rappresentate $P(N_t=k)$ per $t = 1, 3, 5, 10$ nel caso supercritico
e confrontate con un istogramma ottenuto da molte simulazioni Monte Carlo.

### Domande

1. La distribuzione di $N_t$ e' simmetrica?
2. Come cambia la distribuzione tra le realizzazioni che sopravvivono
   e quelle che si estinguono?
3. Qual e' il limite principale dell'approccio per convoluzione
   rispetto all'iterazione di $G^{\circ t}(0)$?

---

# Domande finali di discussione

1. Perche' il caso critico ($m=1$) e' qualitativamente diverso da un equilibrio stabile?
2. Perche' la media e' una descrizione insufficiente del processo di branching?
3. In che senso la funzione generatrice contiene piu' informazione della sola media?
4. Perche' l'equazione $q=G(q)$ e' un problema ai punti fissi e non un'equazione differenziale?
5. Cosa cambia se si parte da $N_0 > 1$ invece che da $N_0 = 1$?
   In particolare, come si esprime $P(\text{estinzione totale} \mid N_0 = n)$ in termini di $q$?
6. Come cambiano le risposte se si usa la distribuzione a tre valori $\{0,1,2\}$
   invece di quella binaria?

---

# Cosa dovreste aver capito alla fine

Al termine del laboratorio dovreste aver verificato che:

1. traiettorie con la stessa media possono avere esiti radicalmente diversi;
2. la media cresce come $m^t$, ma questo non implica sopravvivenza delle singole realizzazioni;
3. nel caso critico la media e' costante, ma l'estinzione e' comunque certa
   e i tempi di estinzione sono molto dispersi;
4. la probabilita' di estinzione si calcola in modo esatto iterando $G$ a partire da $0$;
5. l'iterazione della generatrice e' molto piu' efficiente del Monte Carlo
   per calcolare $P(N_t=0)$;
6. la convergenza del punto fisso $q_{n+1}=G(q_n)$ rallenta vicino alla soglia critica.
