---
title: "S06b Dalle SDE alla Fokker--Planck"
author: "Antonio Scala"
date: ""
theme: "boxes"
colortheme: "wolverine"
fontsize: 12pt
aspectratio: 169
slide-level: 2
---

## Obiettivi della lezione

**Idea centrale:** passare da una dinamica continua sulle traiettorie ad una dinamica sulla **densità di probabilità**.

**Obiettivi:**

* capire perché una ODE evolve anche una pdf iniziale
* derivare l'equazione di continuità per il caso deterministico
* interpretare il drift come trasporto della massa probabilistica
* introdurre il ruolo delle condizioni al bordo
* passare dalle SDE alla Fokker--Planck
* leggere drift e diffusione nella forma conservativa
* discutere casi semplici e distribuzioni stazionarie

---

## Dalla master equation al caso continuo

:::: {.columns}
::: {.column width="50%"}

#### Lezione precedente

* stati discreti
* tempo continuo
* processi di salto
* master equation

:::
::: {.column width="50%"}

#### Oggi

* stato continuo
* tempo continuo
* traiettorie lisce o rumorose
* equazione per la pdf

:::
::::

#### Domanda guida

Se conosco la legge delle traiettorie, come evolve una distribuzione iniziale $p(x,0)$?

---

## Una ODE evolve anche una distribuzione

Consideriamo

$$
\dot x = f(x,t).
$$

:::: {.columns}
::: {.column width="50%"}

#### Se conosco $x(0)=x_0$

* ottengo una traiettoria unica
* descrizione puntuale

:::
::: {.column width="50%"}

#### Se conosco $p(x,0)$

* ottengo una nuvola di traiettorie
* descrizione statistica

:::
::::

**Idea chiave:** una ODE non evolve solo punti singoli, ma trasporta anche una densità iniziale.

---

## Traiettoria singola e nuvola di punti

:::: {.columns}
::: {.column width="48%"}

![](immagini/PdfEvolutionODE.png){width=100%}

:::
::: {.column width="52%"}

#### Lettura della figura

* ogni punto iniziale segue il flusso deterministico
* l'intera nuvola viene trascinata dal campo
* la forma può traslare, comprimersi o deformarsi

#### Messaggio

La dinamica è deterministica sulle traiettorie, ma induce una dinamica non banale sulla pdf.

:::
::::

---

## Come derivare l'equazione per la pdf?

Il modo più pulito è partire da una osservabile regolare $\varphi(x)$.

Il suo valore medio rispetto a $p(x,t)$ è

$$
\langle \varphi \rangle_t = \int \varphi(x)\,p(x,t)\,dx.
$$

#### Strategia

1. derivo nel tempo il valore medio
2. uso la dinamica delle traiettorie
3. trasferisco le derivate da $\varphi$ a $p$
4. ottengo una equazione chiusa per $p(x,t)$

---

## Derivata temporale della media

Da un lato,

$$
\frac{d}{dt}\langle \varphi \rangle_t = \int \varphi(x)\,\partial_t p(x,t)\,dx.
$$

Dall'altro, lungo una traiettoria di $\dot x = f(x,t)$ vale

$$
\frac{d}{dt}\varphi(x(t)) = \nabla \varphi(x(t))\cdot f(x(t),t).
$$

Facendo la media:

$$
\frac{d}{dt}\langle \varphi \rangle_t =
\int \nabla \varphi(x)\cdot f(x,t)\,p(x,t)\,dx.
$$

---

## Integrazione per parti

Uguagliando le due espressioni:

$$
\int \varphi\,\partial_t p,dx = \int \nabla \varphi \cdot (fp)\,dx\;.
$$

Integrando per parti e trascurando i termini di bordo:

$$
\int \nabla \varphi \cdot (fp)\,dx = -\int \varphi,\nabla\cdot(fp)\,dx\;.
$$

Quindi

$$
\int \varphi(x)
\left[
\partial_t p(x,t)+\nabla\cdot(f(x,t)p(x,t))
\right]dx=0.
$$

---

## Equazione di continuità

Poiché la relazione vale per ogni osservabile regolare $\varphi$, segue

$$
\partial_t p(x,t) = -\nabla\cdot\bigl(f(x,t)p(x,t)\bigr).
$$

Definendo la corrente di probabilità

$$
J(x,t)=f(x,t)p(x,t),
$$

la forma diventa

$$
\partial_t p + \nabla\cdot J = 0.
$$

#### Messaggio

È una legge di conservazione: la probabilità non si crea né si distrugge, ma fluisce.

---

## Interpretazione: drift come trasporto

:::: {.columns}
::: {.column width="50%"}

#### Campo deterministico $f$

* trascina la massa probabilistica
* induce una corrente
* non introduce spreading casuale

:::
::: {.column width="50%"}

#### Conseguenza

* la pdf si muove
* può deformarsi
* ma il meccanismo è puramente di trasporto

:::
::::

**Idea chiave:** nel caso deterministico il drift è un trasporto della pdf.

---

## Caso semplice: drift costante

Se

$$
f(x,t)=v,
$$

l'equazione di continuità diventa

$$
\partial_t p + v\cdot \nabla p = 0.
$$

In una dimensione:

$$
\partial_t p + v\,\partial_x p = 0.
$$

La soluzione è una traslazione rigida della densità iniziale:

$$
p(x,t)=p(x-vt,0).
$$

---

## Traslazione rigida della pdf

:::: {.columns}
::: {.column width="52%"}

![](immagini/PdfEvolutionTranslate.png){width=100%}

:::
::: {.column width="48%"}

#### Lettura della figura

* il profilo non cambia forma
* tutto si trasla con velocità $v$
* nessun allargamento, nessuna diffusione

#### Messaggio

Il drift "puro" sposta la distribuzione. 

:::
::::

---

## In generale il trasporto non è rigido

Se il campo $f(x,t)$ varia nello spazio, la pdf può:

* traslare
* comprimersi
* espandersi
* deformarsi

#### Ma la struttura resta la stessa

$$
\partial_t p = -\nabla\cdot(fp).
$$

#### Punto concettuale

Il termine di drift produce **corrente** di probabilità.

---

## Conservazione della probabilità e bordo

Integrando su un dominio $\Omega$:

$$
\frac{d}{dt}\int_{\Omega} p(x,t)\,dx = -\int_{\Omega} \nabla\cdot J,dx.
$$

Con il teorema della divergenza:

$$
\frac{d}{dt}\int_{\Omega} p(x,t)\,dx =
-\int_{\partial \Omega} J\cdot n,dS.
$$

#### Conclusione

La variazione della massa probabilistica dipende interamente dal flusso al bordo.

---

## Casi tipici al bordo

:::: {.columns}
::: {.column width="50%"}

#### Probabilità conservata

* spazio infinito con decadimento sufficiente
* bordo riflettente: $J\cdot n = 0$
* condizioni periodiche

:::
::: {.column width="50%"}

#### Probabilità non conservata nel dominio

* bordo assorbente
* fuga della massa probabilistica
* problemi di primo passaggio / sopravvivenza

:::
::::

---

## Passaggio alle SDE

Ora aggiungiamo rumore alle traiettorie:

$$
dX_t = a(X_t,t)\,dt + B(X_t,t)\,dW_t.
$$

:::: {.columns}
::: {.column width="50%"}

#### Drift

$a(x,t)\,dt$ governa il trasporto

$\qquad$

:::
::: {.column width="50%"}

#### Rumore

$B(x,t)\,dW_t$ governa la dispersione

$\qquad$

:::
::::

### Effetto sulla pdf

Non c'è più solo trasporto: compare anche un termine diffusivo.

---

## Dalla SDE alla Fokker--Planck

Per una SDE di Itô

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t
$$

la densità $p(x,t)$ soddisfa

$$
\partial_t p(x,t) = -\partial_x\bigl(a(x,t)p(x,t)\bigr) + \frac{1}{2}\partial_x^2\bigl(b(x,t)^2 p(x,t)\bigr).
  $$

#### Struttura

* termine di drift: derivata prima
* termine di diffusione: derivata seconda

---

## Forma conservativa

La Fokker--Planck si può scrivere come

$$
\partial_t p = -\partial_x J,
$$

con corrente

$$
J(x,t)=a(x,t)p(x,t)-\frac{1}{2}\partial_x\bigl(b(x,t)^2 p(x,t)\bigr).
$$

#### Vantaggio

La struttura di continuità resta visibile anche nel caso stocastico.

---

## Drift e diffusione: ruoli diversi

:::: {.columns}
::: {.column width="50%"}

#### Drift

* sposta il centro della distribuzione
* induce corrente orientata
* riflette la tendenza media

:::
::: {.column width="50%"}

#### Diffusione

* allarga la distribuzione
* riduce i gradienti
* riflette le fluttuazioni casuali

:::
::::

---

## Caso semplice: coefficienti costanti

Consideriamo

$$
dX_t = v\,dt + \sigma\,dW_t.
$$

La Fokker--Planck diventa

$$
\partial_t p = -v\,\partial_x p + \frac{\sigma^2}{2}\partial_x^2 p.
$$

#### Lettura

* $v$ trasla la pdf
* $\sigma$ la allarga

È la combinazione di *advezione* e diffusione.

---

## Diffusione pura

Se il drift è nullo,

$$
dX_t = \sigma\,dW_t,
$$

allora

$$
\partial_t p = \frac{\sigma^2}{2}\partial_x^2 p.
$$

Questa è l'equazione del calore.

#### Messaggio

Il moto browniano puro corrisponde ad una diffusione della "massa" probabilistica.

---

## Stato stazionario

Una distribuzione stazionaria $p^*(x)$ soddisfa

$$
\partial_t p^*(x)=0.
$$

Quindi

$$
-\partial_x\bigl(a p^*\bigr) + \frac{1}{2}\partial_x^2\bigl(b^2 p^*\bigr)=0.
  $$

Oppure, in termini di corrente,

$$
\partial_x J^*(x)=0
$$

Condizione sufficiente ma non necessaria è flusso netto  zero $J^*(x)=0$

---

## Caso di drift gradiente

Se il drift ha la forma $a(x)=-V'(x)$ con diffusione costante $b(x)=\sigma$, allora la stazionaria a corrente nulla soddisfa

$$
0 = -a(x)p^*(x) + \frac{\sigma^2}{2}\partial_x p^*(x).
$$

Da cui segue

$$
p^*(x) \propto e^{-2V(x)/\sigma^2}.
$$

#### Messaggio

Il paesaggio di potenziale controlla la distribuzione di equilibrio.

---

## Equazione sulle traiettorie vs equazione sulla pdf

:::: {.columns}
::: {.column width="50%"}

#### SDE

$$
dX_t = a\,dt + b,dW_t
$$

* evolve realizzazioni singole
* oggetto naturale per simulare traiettorie

:::
::: {.column width="50%"}

#### Fokker--Planck

$$
\partial_t p = -\partial_x(ap)+\frac12\partial_x^2(b^2p)
$$

* evolve la distribuzione
* oggetto naturale per medie e statistiche

:::
::::

---

## Collegamento con accuratezza forte e debole

:::: {.columns}
::: {.column width="50%"}

#### Accuratezza forte

* confronta traiettorie
* rilevante per il pathwise error

:::
::: {.column width="50%"}

#### Accuratezza debole

* confronta distribuzioni o medie
* rilevante per osservabili statistiche

:::
::::

#### Punto concettuale

La distinzione forte/debole riflette la differenza tra livello delle traiettorie e livello delle pdf.

---

## Take-home message

* una ODE trasporta anche una distribuzione iniziale
* nel caso deterministico la pdf soddisfa una equazione di continuità
* il drift genera corrente di probabilità
* le condizioni al bordo controllano la conservazione della massa
* una SDE aggiunge spreading casuale alle traiettorie
* la Fokker--Planck è la controparte sulla pdf della SDE
* drift e diffusione corrispondono a trasporto e spreading

---

## Prossima lezione / sviluppi

* soluzioni esplicite in casi speciali
* distribuzioni stazionarie e tempi di rilassamento
* collegamenti con operatori, propagatori e spettri
* esempi: moto browniano geometrico, rumore di Feller

---

## Backup -- Formula generale multidimensionale

Per

$$
dX_t = a(X_t,t)\,dt + B(X_t,t)\,dW_t,
$$

con

$$
D(x,t)=\frac12 B(x,t)B(x,t)^\top,
$$

la Fokker--Planck è

$$
\partial_t p = -\sum_i \partial_i(a_i p) + \sum_{i,j} \partial_i\partial_j(D_{ij}p).
$$

---

## Backup -- Caso deterministico come caso limite

Se si "spegne" il rumore,

$$
b(x,t)=0
$$

la Fokker--Planck si riduce a

$$
\partial_t p = -\partial_x(ap)
$$

cioè all'equazione di continuità deterministica.

#### Messaggio

L'equazione di continuità è il caso senza diffusione della Fokker--Planck.

---

## Backup -- Diffusione costante e coefficiente diffusivo

Per

$$
dX_t = a(X_t,t)\,dt + b(X_t,t)\,dW_t,
$$

il coefficiente diffusivo della PDE è

$$
D(x,t)=\frac{1}{2}b(x,t)^2.
$$

Nel caso di rumore additivo costante,

$$
D=\frac{\sigma^2}{2}.
$$

---

## Backup -- Corrente stazionaria nulla

Se in stazionario imponiamo

$$
J^*(x)=0,
$$

allora

$$
a(x)p^*(x)-\frac12\partial_x\bigl(b(x)^2 p^*(x)\bigr)=0.
$$

Questo è spesso il modo più semplice per trovare la distribuzione di equilibrio.

---

## Backup -- Confronto strutturale con la master equation

:::: {.columns}
::: {.column width="50%"}

#### Master equation

$$
\dot p_i = \sum_j (\text{ingressi} - \text{uscite})
$$

* stati discreti
* salti
* flussi tra stati

$p_i$ varia se il bilancio fra entrate e uscite per lo stato $i$ non è nullo (analogo della divergenza)

:::
::: {.column width="50%"}

#### Fokker--Planck

$$
\partial_t p = -\partial_x J
$$

* stato continuo
* traiettorie continue rumorose
* flusso nello spazio degli stati

$p(x)$ varia se la divergenza di $J$ non è nulla (ovvero qualcosa esce/entra nella regione intorno ad $x$)

:::
::::

#### Messaggio

La Fokker--Planck è l'analogo continuo della master equation.
