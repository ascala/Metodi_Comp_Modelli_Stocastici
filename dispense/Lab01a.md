---
title: "LAB01a Struttura deterministica dei sistemi stocastici"
author: "Antonio Scala"
date: "5 Mar 2026"
---

# Obiettivi del laboratorio

In questo laboratorio useremo simulazioni numeriche (metodo di Eulero) e soluzioni esatte per:

1. verificare empiricamente che, per una ODE risolvibile esattamente, ridurre $\Delta t$ migliora l'approssimazione;
2. usare la teoria (equilibri e stabilità locale) per **predire** il comportamento qualitativo delle traiettorie;
3. imparare a “validare” un codice confrontando:
   - traiettorie numeriche (Euler) *vs* soluzione esatta (quando disponibile),
   - comportamento qualitativo *vs* fase-linea (phase diagram 1D) dedotta da $f(x;r)$.

Idea guida: una simulazione ODE con Eulero è una dinamica discreta
$$
x_{n+1}=x_n+\Delta t\, f(x_n;r),
$$
quindi la scelta di $\Delta t$ fa parte del modello computazionale.

---

# Parte A -- Eulero vs soluzione esatta: equazione test $\dot x=\lambda x$

## A1. Modello e soluzione esatta

Considera l'ODE
$$
\dot x = \lambda x, \qquad x(0)=x_0.
$$
La soluzione esatta è
$$
x(t)=x_0 e^{\lambda t}.
$$

## A2. Fase-linea e stabilità

Equilibrio: $x^*=0$.

Linearizzazione: $f'(x)=\lambda$. Quindi:
- se $\lambda<0$, $x^*=0$ è stabile (decadimento);
- se $\lambda>0$, $x^*=0$ è instabile (crescita).

In termini numerici, Eulero produce:
$$
x_{n+1}=(1+\lambda\Delta t)\,x_n.
$$
Quindi la stabilità numerica richiede $|1+\lambda\Delta t|<1$ quando $\lambda<0$ (vincolo sul passo).

## A3. Programma (file 01)

Usa lo script:
- `01_euler_vs_exact_exponential.py` 

Cosa fare:
1. modifica `dt_list` e osserva l'effetto su:
   - accuratezza,
   - stabilità numerica per passi grandi,
   - eventuali oscillazioni spurie (quando $1+\lambda\Delta t<0$).
2. stampa e interpreta l'errore finale $|x(T)-x_{\mathrm{exact}}(T)|$.

---

# Parte B -- Transcritical: $\dot N = rN - N^2$ (Euler *vs* soluzione esatta)

In questa parte NON partiamo dal diagramma di biforcazione “già fatto”: lo scopo è che lo studente lo ricostruisca
a partire da (i) equilibri e stabilità, (ii) osservazione delle traiettorie.

## B1. Modello, equilibri, stabilità locale (teoria)

ODE:
$$
\dot N=f(N;r)=rN-N^2 = N(r-N).
$$

Equilibri: risolvi $f(N;r)=0$:
$$
N_1^*(r)=0, \qquad N_2^*(r)=r.
$$

Derivata:
$$
f'(N;r)=r-2N.
$$

Valuta su ciascun equilibrio:
- su $N_1^*=0$: $f'(0;r)=r$  
  quindi $N=0$ è stabile per $r<0$, instabile per $r>0$;
- su $N_2^*=r$: $f'(r;r)=r-2r=-r$  
  quindi $N=r$ è stabile per $r>0$, instabile per $r<0$.

Questa è la “firma” della transcritical: scambio di stabilità tra i due rami in $r=0$.

## B2. Soluzione esatta (derivazione sintetica)

Separazione delle variabili:
$$
\frac{dN}{dt}=N(r-N)\quad \Rightarrow \quad
\frac{dN}{N(r-N)}=dt.
$$
Scomposizione in fratti semplici:
$$
\frac{1}{N(r-N)}=\frac{1}{r}\left(\frac{1}{N}+\frac{1}{r-N}\right),
$$
quindi
$$
\frac{1}{r}\left(\ln|N|-\ln|r-N|\right)=t+C.
$$
Da cui
$$
\frac{N}{r-N}=C e^{rt}.
$$
Imponendo $N(0)=N_0$ si ottiene $C=\frac{N_0}{r-N_0}$ e quindi, per $r\neq 0$,
$$
N(t)=\frac{rN_0}{N_0+(r-N_0)e^{-rt}}.
$$
Per $r=0$ la dinamica è $\dot N=-N^2$ e la soluzione è
$$
N(t)=\frac{N_0}{1+N_0 t}.
$$

## B3. Programma (file 02) e cosa verificare

Usa lo script minimale:
- `02_transcritical_bifurcation_and_trajectories.py`

Il programma disegna una traiettoria Euler (punti) contro la soluzione esatta (linea).
Cosa fare:

1. **Stabilità e attrazione verso equilibri**  
   prova:
   - $r<0$ con $N_0>0$ piccolo: deve andare verso $0$;
   - $r>0$ con $N_0>0$ piccolo: deve crescere verso $N=r$.

2. **Controllo numerico vs teoria**  
   cambia `dt` (es. 0.2, 0.1, 0.05, 0.02, 0.01) e osserva:
   - l'errore visivo Euler-vs-esatto,
   - eventuali deviazioni qualitative per passi troppo grandi.

3. **Ricostruzione del diagramma di biforcazione (compito concettuale)**  
   senza disegnare subito il bifurcation diagram, costruisci la fase-linea:
   - segno di $f(N;r)$ per $N<0$, $0<N<r$, $N>r$ (per $r>0$),
   - e analogamente per $r<0$.
   Da questo ottieni stabilità dei punti critici e quindi il diagramma.

Consegna minima (Parte B):
- 2 plot (o 1 plot ripetuto) per almeno due valori di $r$ (uno negativo, uno positivo) e due/tre scelte di `dt`;
- 5--8 righe: quali equilibri esistono? quali sono stabili? cosa si osserva nelle traiettorie?

---

# Parte C -- Saddle--node e tipping: $\dot x = r + x^2$ (Euler *vs* soluzione esatta)

Anche qui il focus è la lettura qualitativa delle traiettorie e la validazione numerica, non “fare una figura estetica”.

## C1. Modello, equilibri, stabilità locale (teoria)

ODE:
$$
\dot x=f(x;r)=r+x^2.
$$

Equilibri: risolvi $r+(x^*)^2=0$.
- per $r<0$:
  $$
  x^*_\pm(r)=\pm\sqrt{-r};
  $$
- per $r=0$: $x^*=0$ (doppio);
- per $r>0$: nessun equilibrio reale.

Derivata:
$$
f'(x;r)=2x.
$$
Quindi per $r<0$:
- $x^*_-(r)=-\sqrt{-r}$ è stabile (derivata negativa);
- $x^*_+(r)=+\sqrt{-r}$ è instabile (derivata positiva).

Per $r>0$ vale $f(x;r)>0$ per ogni $x$, quindi tutte le traiettorie aumentano e c'è “tipping” verso $+\infty$.

## C2. Soluzione esatta (derivazione sintetica, casi $r>0$, $r<0$, $r=0$)

Separazione:
$$
\frac{dx}{r+x^2}=dt.
$$

- Caso $r>0$, poni $r=a^2$:
  $$
  \int \frac{dx}{a^2+x^2}=\frac{1}{a}\arctan\left(\frac{x}{a}\right)=t+C
  $$
  quindi
  $$
  x(t)=a\tan\left(a t+\arctan\left(\frac{x_0}{a}\right)\right).
  $$
  Questa formula mostra anche il **blow-up in tempo finito** (asintoto della tangente).

- Caso $r=0$:
  $$
  \dot x=x^2 \Rightarrow \frac{dx}{x^2}=dt \Rightarrow -\frac{1}{x}=t+C
  $$
  dunque
  $$
  x(t)=\frac{x_0}{1-x_0 t}.
  $$

- Caso $r<0$, poni $r=-a^2$:
  $$
  \int \frac{dx}{x^2-a^2}=t+C,
  $$
  con soluzione equivalente (forme diverse sono accettabili), ad esempio:
  $$
  x(t)=a\,\frac{1+y(t)}{1-y(t)},\qquad
  y(t)=y_0 e^{2at},\qquad
  y_0=\frac{x_0-a}{x_0+a}.
  $$

## C3. Programma (file 03) e cosa verificare

Usa lo script minimale:
- `03_saddle_node_bifurcation_and_tipping.py`

Nota: per $r>0$ la soluzione esatta diverge in tempo finito, quindi nello script si usa una soglia `xmax` per fermare il plot e mantenere leggibile la scala.

Cosa fare:

1. **Prima della soglia ($r<0$)**  
   scegli $r<0$ e condizioni iniziali a sinistra/destra dell'instabile $+\sqrt{-r}$:
   - vicino a $-\sqrt{-r}$: rilassamento verso l'attrattore;
   - vicino a $+\sqrt{-r}$: repulsione (se superi la soglia, vai verso $+\infty$).

2. **Dopo la soglia ($r>0$)**  
   nessun equilibrio: osserva la crescita e la sensibilità del tempo di blow-up a $r$ e $x_0$.

3. **Validazione numerica**  
   cambia `dt` e confronta:
   - traiettoria Euler vs esatta,
   - stima del tempo di blow-up (quando la curva supera `xmax` oppure usando l'asintoto della formula con tangente).

Consegna minima (Parte C):
- 2 plot per $r<0$ e $r>0$ (o uno per ciascun caso), e almeno 2 scelte di `dt`;
- 5--8 righe: quali equilibri esistono (se esistono)? quali sono stabili? come cambia qualitativamente la dinamica attraversando $r=0$?

---

# Checklist finale (consegna)

1. **Parte A:** plot con $x(t)$ esatto e traiettorie di Eulero per vari $\Delta t$, piu` stampa dell'errore finale.
2. **Parte B:** per transcritical, confronto Euler-vs-esatto per almeno due $r$ e due dt, più ricostruzione (a parole) di equilibri e stabilità.
3. **Parte C:** per saddle--node, confronto Euler-vs-esatto (con soglia di plot) per $r<0$ e $r>0$, e discussione del tipping/blow-up.
4. Commento breve (max mezza pagina): come passi da $f(x;r)$ alla fase-linea e alla previsione qualitativa? come usi la soluzione esatta per “debuggare” Euler?
