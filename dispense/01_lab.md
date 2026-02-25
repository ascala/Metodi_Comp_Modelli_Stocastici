---
title: "Struttura deterministica dei sistemi stocastici (Laboratorio 01)"
author: "Antonio Scala"
date: "5 Apr 2026"
---

# Obiettivi del laboratorio

In questo laboratorio useremo simulazioni numeriche (metodo di Eulero) per:

1. verificare empiricamente che, per una ODE risolvibile esattamente, ridurre $\Delta t$ migliora l'approssimazione;
2. costruire una **mappa dei punti critici** (equilibri) in funzione di un parametro $r$, usando formule analitiche;
3. distinguere **esistenza** e **stabilita` locale** di un equilibrio tramite $f'(x^*)$;
4. visualizzare con traiettorie numeriche cosa succede **vicino agli equilibri** prima e dopo una transizione (tipping deterministico nel caso saddle--node).

L'idea guida è sempre la stessa: una simulazione di una ODE è una dinamica discreta
$$
x_{n+1}=x_n+f(x_n)\Delta t
$$
e quindi la scelta di $\Delta t$ e` parte del modello computazionale.

---

# Parte A -- Eulero vs soluzione esatta: equazione test $\dot x=\lambda x$

## A1. Modello e soluzione esatta

Considera l'ODE
$$
\dot x = \lambda x, \qquad x(0)=x_0.
$$

La soluzione esatta e`
$$
x(t)=x_0 e^{\lambda t}.
$$

## A2. Cosa verificare

1. Per $\Delta t$ piu` piccolo, le traiettorie di Eulero si avvicinano alla soluzione esatta.
2. (Consigliato) L'errore a tempo finale $T$ decresce al diminuire di $\Delta t$.

## A3. Pseudocodice
```

scegli parametri:
x0 = 1
lambda = -1 # prova anche lambda > 0, opzionale
T = 5
DTlist = [1, 0.5, 0.2, 0.1, 0.05]

definisci griglia temporale esatta (fine, non per forza legata a DTlist):
t_fine = lista di tempi da 0 a T (passo piccolo a scelta)
x_esatta(t) = x0 * exp(lambda * t)

per ogni DeltaT in DTlist:

    nsteps = T / DeltaT   (arrotonda in modo coerente)
    t = 0
    x = x0
    
    salva (t, x) in una lista (t_list, x_list)

    ripeti nsteps volte:
        x = x + DeltaT * (lambda * x)
        t = t + DeltaT
        salva (t, x)

errore_finale = | x - x0 * exp(lambda * T) |
stampa DeltaT, errore_finale
```

PRODUCI UN PLOT:
curva esatta $x(t)$ *vs* curve di Eulero per i diversi DeltaT

**Domanda guida (opzionale):** per $\lambda<0$ vedi oscillazioni spurie o divergenza per passi molto grandi? come lo riconosci dal fattore $(1+\lambda\Delta t)$?

---

# Parte B -- Biforcazione transcritica: mappa dei punti critici + traiettorie vicino agli equilibri

## B1. Modello

Considera
$$
\dot N = f(N;r)=rN-N^2 = N(r-N).
$$

Punti critici (equilibri), da $f(N;r)=0$:
$$
N_1^*(r)=0, \qquad N_2^*(r)=r.
$$

Derivata per stabilita` locale:
$$
f'(N;r)=r-2N.
$$

Criterio locale:
- $N^*$ stabile se $f'(N^*;r)<0$;
- $N^*$ instabile se $f'(N^*;r)>0$.

## B2. Mappa dei punti critici vs parametro $r$
```

scegli intervallo di parametro:
r_min, r_max
Nr = numero di punti della griglia
r_list = [r_min, r_min+dr, ..., r_max] con dr = (r_max-r_min)/(Nr-1)

inizializza due collezioni vuote:
STABILI = []
INSTABILI = []

per ogni r in r_list:

    # punti critici (formule analitiche)
    critici = [0, r]
    
    per ogni Nstar in critici:
    
        derivata = r - 2*Nstar
    
        se derivata < 0:
            aggiungi (r, Nstar) a STABILI
        altrimenti se derivata > 0:
            aggiungi (r, Nstar) a INSTABILI
        altrimenti:
            (caso marginale) annota separatamente
```

PRODUCI UN PLOT:
diagramma $(r, Nstar)$ con simboli diversi per STABILI e INSTABILI

## B3. Traiettorie prima/dopo la transizione, partendo vicino ai punti critici

Scegli due valori:
$$
r_{\mathrm{before}}=-\varepsilon,\qquad r_{\mathrm{after}}=+\varepsilon,
$$
con $\varepsilon>0$ piccolo.

Scegli un offset piccolo $\delta>0$ e costruisci condizioni iniziali "vicine" ai punti critici.
```

scegli:
eps = valore piccolo (es. 0.2)
r_before = -eps
r_after = +eps
delta = valore piccolo (es. 0.05)

scegli parametri numerici:
DeltaT = passo temporale (es. 0.01)
T = tempo finale

definisci elenco di condizioni iniziali (vicine agli equilibri):

# prima: vicine a N*=0 e N*=r_before
IC_before = [ 0 + delta, 0 - delta, r_before + delta, r_before - delta ]

# dopo: vicine a N*=0 e N*=r_after
IC_after  = [ 0 + delta, 0 - delta, r_after + delta, r_after - delta ]

per ciascuna condizione iniziale N0 in IC_before:
    # integra con Eulero:
    t=0, N=N0
    ripeti finche t < T:
    N = N + DeltaT * (r_before*N - N*N)
    t = t + DeltaT
    salva (t, N)

per ciascuna condizione iniziale N0 in IC_after:
    # integra con Eulero:
    t=0, N=N0
    ripeti finche t < T:
        N = N + DeltaT * (r_after*N - N*N)
        t = t + DeltaT
    salva (t, N)

```

PRODUCI UN PLOT (anche con due pannelli):
* pannello 1: diagramma dei punti critici (da B2) + linea verticale in $r_{before}$ e $r_{after}$
* pannello 2: traiettorie $N(t)$ per $r_{before}$ e $r_{after}$ (etichette chiare)

**Consegna minima (per la Parte B):**
- una figura che mostri (i) punti critici stabili/instabili vs $r$, e (ii) traiettorie vicino agli equilibri per $r=\pm\varepsilon$;
- 3--5 righe di commento: dove avviene lo scambio di stabilità? cosa succede alle traiettorie vicino a ciascun ramo?

---

# Parte C -- Biforcazione saddle--node e tipping: mappa dei punti critici + traiettorie prima/dopo

## C1. Modello

Considera
$$
\dot x = f(x;r)=r+x^2.
$$

Punti critici: risolvi $r+(x^*)^2=0$.

- per $r<0$:
  $$
  x^*_\pm(r)=\pm\sqrt{-r};
  $$
- per $r=0$: $x^*=0$ (doppio);
- per $r>0$: nessun equilibrio reale.

Derivata per stabilita` locale:
$$
f'(x;r)=2x.
$$

Quindi, per $r<0$:
- $x^*_-(r)=-\sqrt{-r}$ e` stabile (derivata negativa);
- $x^*_+(r)=+\sqrt{-r}$ e` instabile (derivata positiva).

## C2. Mappa dei punti critici vs parametro $r$
```

scegli intervallo di parametro:
r_min, r_max
Nr
r_list = \[r_min, r_min+dr, ..., r_max]

inizializza:
STABILI = []
INSTABILI = []

per ogni r in r_list:
    se r < 0:
        a = sqrt(-r)
        critici = [-a, +a]
    altrimenti se r = 0:
        critici = [0]
    altrimenti:
        critici = []    # nessun punto critico

per ogni xstar in critici:
    derivata = 2*xstar
    se derivata < 0:
        aggiungi (r, xstar) a STABILI
    altrimenti se derivata > 0:
        aggiungi (r, xstar) a INSTABILI
    altrimenti:
        (caso marginale) annota separatamente
```

PRODUCI UN PLOT:
diagramma $(r, x^*)$ con simboli diversi per STABILI e INSTABILI

## C3. Traiettorie prima/dopo la transizione: tipping deterministico

Scegli di nuovo
$$
r_{\mathrm{before}}=-\varepsilon,\qquad r_{\mathrm{after}}=+\varepsilon.
$$

Qui la differenza chiave e` che per $r_{\mathrm{after}}>0$ **non ci sono equilibri**.
Quindi: dopo la transizione parti vicino alla posizione dell'attrattore che esisteva appena prima.
```

scegli:
eps = valore piccolo (es. 0.2)
r_before = -eps
r_after = +eps
delta = valore piccolo (es. 0.05)

scegli parametri numerici:
DeltaT
T

calcola punti critici "before" (analitici):
a = sqrt(-r_before)
x_stabile_before = -a
x_instabile_before = +a

definisci condizioni iniziali:

IC_before = [ x_stabile_before + delta, x_stabile_before - delta,
              x_instabile_before + delta, x_instabile_before - delta ]

# after: nessun equilibrio; parti vicino a dove stava il ramo stabile "prima"
IC_after  = [ x_stabile_before + delta, x_stabile_before - delta ]

# integra con Eulero per r_before:
per ciascun x0 in IC_before:
t=0, x=x0
ripeti finche t < T:
    x = x + DeltaT * (r_before + x*x)
    t = t + DeltaT
    salva (t, x)

# integra con Eulero per r_after:
per ciascun x0 in IC_after:
t=0, x=x0
ripeti finche t < T:
    x = x + DeltaT * (r_after + x*x)
    t = t + DeltaT
salva (t, x)

```

PRODUCI UN PLOT (anche con due pannelli):
* pannello 1: diagramma dei punti critici (da C2) + linea verticale in $r_{before}$ e $r_{after}$
* pannello 2: traiettorie $x(t)$ per $r_{before}$ e $r_{after}$

**Consegna minima (per la Parte C):**
- una figura che mostri (i) i rami stabili/instabili e la loro scomparsa a $r=0$, e (ii) l'effetto "prima/dopo" sulle traiettorie;
- 3--5 righe di commento: perchè dopo la transizione non puo` esserci rilassamento verso un equilibrio?

---

# Checklist finale (consegna)

1. **Parte A:** un plot con $x(t)$ esatto e le traiettorie di Eulero per vari $\Delta t$, piu` una piccola tabella (o print) con l'errore finale vs $\Delta t$.
2. **Parte B:** un plot che metta insieme mappa dei punti critici (stabili/instabili) e traiettorie vicino agli equilibri per $r=\pm\varepsilon$.
3. **Parte C:** un plot che metta insieme mappa dei punti critici (stabili/instabili) e traiettorie prima/dopo la soglia saddle--node.
4. Breve commento (massimo mezza pagina) che colleghi: esistenza/stabilita` degli equilibri -> comportamento delle traiettorie -> significato operativo di "tipping".
