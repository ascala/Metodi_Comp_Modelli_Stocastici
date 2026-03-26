---
title: "LAB05 SDE: convergenza forte, convergenza debole e preservazione della positività"
author: "Antonio Scala"
date: ""
---

# Obiettivi

In questo laboratorio studiamo numericamente una semplice equazione differenziale stocastica con rumore moltiplicativo. L’obiettivo non è soltanto implementare uno schema numerico, ma capire che cosa significhi davvero "approssimare bene" una SDE.

Al termine del laboratorio dovreste essere in grado di:

1. simulare una traiettoria browniana discreta;
2. implementare lo schema di Euler--Maruyama;
3. confrontare una soluzione numerica con una soluzione esatta;
4. distinguere tra convergenza forte e convergenza debole;
5. riconoscere un difetto qualitativo del metodo: la perdita di positività;
6. discutere una correzione naturale tramite cambio di variabile;
7. confrontare, come estensione, Euler--Maruyama e Milstein.

---

# Il modello

Consideriamo la SDE

$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t,
\qquad X_0>0.
$$

Questa equazione descrive una crescita proporzionale soggetta a rumore moltiplicativo. A seconda del contesto, $X_t$ può rappresentare una popolazione, una biomassa, un capitale o un’altra quantità naturalmente positiva.

## Soluzione esatta

La soluzione esatta è

$$
X_t = X_0 \exp\!\left[\left(\mu-\frac{\sigma^2}{2}\right)t + \sigma W_t\right].
$$

Quindi, se $X_0>0$, vale sempre

$$
X_t>0.
$$

Questa proprietà sarà centrale nel laboratorio.

# Parametri di lavoro

Usate inizialmente i seguenti valori:

$$
X_0 = 1,
\qquad
\mu = 0.2,
\qquad
\sigma = 0.8,
\qquad
T = 1.
$$

Per le quantità medie usate un numero di traiettorie sufficientemente grande, ad esempio

$$
M = 10^3 \quad \text{oppure} \quad M = 10^4.
$$

Provate poi anche valori più grandi di $\sigma$ per rendere più visibile il problema della perdita di positività.

# Parte 1 -- Moto browniano discreto e soluzione esatta

## 1.1 Griglia temporale

Costruite una griglia uniforme

$$
t_n = n\Delta t,
\qquad n=0,\dots,N,
\qquad \Delta t = \frac{T}{N}.
$$

Provate almeno i valori

$$
N = 2^4,\;2^5,\;2^6,\;2^7.
$$

## 1.2 Incrementi browniani

Generate incrementi indipendenti con legge

$$
\Delta W_n \sim \mathcal{N}(0,\Delta t).
$$

Ricostruite poi il cammino browniano discreto tramite

$$
W_{t_0}=0,
\qquad
W_{t_{n+1}}=W_{t_n}+\Delta W_n.
$$

## 1.3 Soluzione esatta sulla griglia

Usando il cammino browniano costruito, calcolate

$$
X_{t_n}^{\mathrm{exact}} = X_0 \exp\!\left[\left(\mu-\frac{\sigma^2}{2}\right)t_n 
+ \sigma W_{t_n}\right].
$$

# Domande

1. La traiettoria esatta resta sempre positiva?
2. La traiettoria appare liscia oppure irregolare?
3. Che cosa cambia se aumentate $\sigma$?

# Parte 2 -- Schema di Euler--Maruyama

## 2.1 Implementazione

Applicate lo schema di Euler--Maruyama:

$$
X_{n+1} = X_n + \mu X_n \Delta t + \sigma X_n \Delta W_n.
$$

Usate gli **stessi incrementi browniani** della Parte 1.

## 2.2 Confronto con la soluzione esatta

Per una singola realizzazione del rumore, disegnate sulla stessa figura:

- la traiettoria esatta;
- la traiettoria ottenuta con Euler--Maruyama.

Ripetete per diversi valori di $\Delta t$.

## Domande

1. Diminuendo $\Delta t$, la traiettoria numerica segue meglio quella esatta?
2. Euler--Maruyama preserva sempre la positività?
3. Compaiono valori negativi anche se la soluzione esatta è sempre positiva?

# Parte 3 -- Convergenza forte

## 3.1 Significato

La convergenza forte riguarda la qualità dell’approssimazione di una **singola traiettoria**, a parità di realizzazione del rumore.

In teoria si confrontano:

- la soluzione esatta $X_T$;
- la soluzione numerica $X_T^{(\Delta t)}$;

costruite usando lo **stesso** moto browniano.

Questo punto è essenziale. Se si usassero due rumori indipendenti, la differenza osservata mescolerebbe errore numerico e variabilità casuale, e non misurerebbe più correttamente la convergenza forte.

Per questo, quando si confrontano discretizzazioni con passi diversi, si costruisce prima una traiettoria browniana su una griglia molto fine e poi si ottengono le griglie più grosse sommando opportunamente gli incrementi fini.

### Costruire lo stesso rumore su griglie diverse

```text
Scegli T e un passo fine dt
Calcola Nfine = T / dt

Per j = 0, ..., Nfine - 1:
    genera un incremento fine dW[j] con distribuzione N(0, dt)

Per ogni passo temporale più grande Dt:
    scegli un intero m tale che Dt = m Dt
    poni N = T / Dt

    Per n = 0, ..., N - 1:
        definisci l'incremento grossolano
        DW[n] = somma degli m incrementi fini consecutivi
                contenuti nell'n-esimo blocco
````

In particolare, se $\Delta t = 4\,\delta t$, allora

$$\Delta W_n=\delta W_{4n}+\delta W_{4n+1}+\delta W_{4n+2}+\delta W_{4n+3}\;.$$

In questo modo tutte le discretizzazioni sono costruite sullo stesso cammino browniano sottostante.

## 3.2 Errore forte

Per ogni traiettoria $m$, definite

$$e_{forte}^{(m)}(\Delta t)=\lvert X_T^{(m),exact}- X_T^{(m),EM}\rvert $$
Poi mediate su $M$ traiettorie:

$$E_{forte}^{(m)}(\Delta t)=\frac{1}{M}\sum e_{forte}^{(m)}(\Delta t)$$

### Stima numerica dell’errore forte

```
Fissa un valore di dt
Poni errore_totale = 0

Ripeti per m = 1, ..., M traiettorie:
    genera una traiettoria browniana fine
    costruisci, per somma a blocchi, gli incrementi dW
    corrispondenti al passo dt

    calcola la soluzione esatta al tempo finale T
    usando il rumore costruito sopra

    calcola la soluzione numerica di Euler--Maruyama
    usando gli stessi incrementi dW

    calcola l'errore finale
    e = | Xexact(T) - XEM(T) |

    aggiorna errore_totale = errore_totale + e

Alla fine:
    Eforte(dt) = errore_totale / M
```

Per questo modello la soluzione esatta è nota in forma chiusa. In problemi più generali, quando la soluzione esatta non è disponibile, si usa spesso al suo posto una soluzione di riferimento ottenuta su una griglia molto più fine.

## 3.3 Esperimento

Calcolate $E_{\mathrm{forte}}(\Delta t)$ per diversi passi temporali e costruite un grafico log--log di

$$
E_{\mathrm{forte}}(\Delta t)
\quad \text{contro} \quad
\Delta t.
$$

## Domande

1. Il grafico suggerisce una legge di potenza?
2. La pendenza osservata è circa $1/2$?
3. Perché qui è essenziale usare lo stesso rumore nella traiettoria esatta e in quella numerica?

---

# Parte 4 -- Convergenza debole

## 4.1 Significato

La convergenza debole riguarda la riproduzione corretta delle **quantità statistiche**, non della singola traiettoria.

Nel caso della convergenza debole non è essenziale accoppiare traiettoria per traiettoria le diverse discretizzazioni tramite lo stesso rumore: ciò che conta è stimare correttamente le medie statistiche su un numero sufficientemente grande di realizzazioni.

## 4.2 Valori teorici

Per il modello assegnato vale

$$
\mathbb{E}[X_T] = X_0 e^{\mu T}.
$$

Vale inoltre

$$
\mathbb{E}[X_T^2] = X_0^2 e^{(2\mu+\sigma^2)T}.
$$

## 4.3 Errore debole

Stimate numericamente la media campionaria

$$
\overline{X_T}^{\,(\Delta t)} =
\frac{1}{M}\sum_{m=1}^M X_T^{(m),\mathrm{EM}}.
$$

Definite quindi l’errore debole

$$
E_{\mathrm{debole}}(\Delta t) =
\left|
\overline{X_T}^{\,(\Delta t)} - X_0 e^{\mu T}
\right|.
$$

Facoltativamente, ripetete l’analisi anche per il secondo momento.

## Domande

1. L’errore debole decresce più rapidamente dell’errore forte?
2. La pendenza osservata è compatibile con ordine $1$?
3. Perché un metodo può essere impreciso sulle traiettorie singole ma ragionevolmente accurato sulle medie?

# Parte 5 -- Attraversamenti non fisici dello zero

## 5.1 Il problema

La soluzione esatta resta positiva, ma lo schema di Euler--Maruyama può produrre valori negativi.

Infatti

$$
X_{n+1} =
X_n + \mu X_n \Delta t + \sigma X_n \Delta W_n =
X_n\left(1+\mu\Delta t+\sigma\Delta W_n\right).
$$

Quindi può accadere che

$$
1+\mu\Delta t+\sigma\Delta W_n < 0.
$$

## 5.2 Esperimento numerico

Per ciascuna traiettoria, controllate se esiste almeno un indice $n$ tale che

$$
X_n<0.
$$

Definite allora la frequenza di perdita di positività:

$$
p_{\mathrm{neg}}(\Delta t) =
\frac{\text{numero di traiettorie con almeno un valore negativo}}{M}.
$$

Studiate come varia al cambiare di:

1. $\Delta t$;
2. $\sigma$.

Osservazione: per studiare la frequenza di perdita di positività non è necessario confrontare ogni traiettoria con una traiettoria esatta. Qui interessa una proprietà qualitativa dello schema numerico, cioè la comparsa di valori negativi.

## Domande

1. La frequenza di attraversamento dello zero diminuisce quando $\Delta t$ diminuisce?
2. Che effetto ha un aumento di $\sigma$?
3. Perché questo comportamento è problematico dal punto di vista del modello?

# Parte 6 -- Correzione tramite trasformazione logaritmica

## 6.1 Cambio di variabile

Ponete

$$
Y_t = \log X_t.
$$

Usando la formula di Ito, mostrate che $Y_t$ soddisfa

$$
dY_t = \left(\mu-\frac{\sigma^2}{2}\right)dt + \sigma\,dW_t.
$$

## 6.2 Schema numerico

Applicate ora un passo di Eulero a questa equazione:

$$
Y_{n+1} =
Y_n + \left(\mu-\frac{\sigma^2}{2}\right)\Delta t + \sigma \Delta W_n.
$$

Poi ricostruite

$$
X_{n+1}=e^{Y_{n+1}}.
$$

## Domande

1. Questo schema preserva la positività?
2. Come si confronta con Euler--Maruyama standard?
3. In questo caso il cambio di variabile è una semplice correzione numerica oppure sfrutta una struttura esatta del modello?

# Parte 7 -- Correzione euristica con proiezione

## 7.1 Schema proiettato

Definite prima il passo non corretto di Euler--Maruyama:

$$
\widetilde X_{n+1}
=
X_n + \mu X_n\Delta t + \sigma X_n\Delta W_n.
$$

Poi imponete

$$
X_{n+1}=\max(0,\widetilde X_{n+1}).
$$

# Domande

1. La non negatività è ora garantita?
2. Questa correzione altera il valore medio?
3. Si tratta di una modifica naturale del modello oppure di un artificio numerico?

# Parte 8 -- Discussione finale

Confrontate i seguenti approcci:

1. soluzione esatta;
2. Euler--Maruyama;
3. schema logaritmico;
4. eventuale schema proiettato.

Discutete i seguenti punti:

- accuratezza sulle traiettorie;
- accuratezza sulle medie;
- preservazione della positività;
- semplicità di implementazione;
- fedeltà al modello continuo.

---

# Esercizio supplementare -- Ripetere tutto con Milstein

Per la SDE

$$
dX_t = \mu X_t\,dt + \sigma X_t\,dW_t,
$$

lo schema di Milstein (vedi dispense) è

$$
X_{n+1} = X_n
+ \mu X_n\Delta t
+ \sigma X_n\Delta W_n
+ \frac{1}{2}\sigma^2 X_n\left((\Delta W_n)^2-\Delta t\right).
$$

Infatti qui

$$
b(x,t)=\sigma x,
\qquad
\partial_x\,b(x,t)=\sigma.
$$

## Consegne

1. Implementate lo schema di Milstein.
2. Confrontatelo con la soluzione esatta sulla stessa realizzazione del rumore.
3. Ripetete lo studio della convergenza forte.
4. Ripetete lo studio della convergenza debole.
5. Verificate se Milstein riduce il problema della perdita di positività.
6. Confrontate Milstein con Euler--Maruyama e con lo schema logaritmico.

## Domande guida

1. La convergenza forte osservata è migliore di quella di Euler--Maruyama?
2. Le medie migliorano in modo evidente?
3. Milstein preserva automaticamente la positività?
4. Per questo modello specifico, quale metodo vi sembra più naturale?

---

# Cosa dovreste aver capito alla fine

Al termine del laboratorio dovreste aver verificato che:

1. Euler--Maruyama converge fortemente con ordine circa $1/2$;
2. la convergenza debole è migliore della convergenza forte;
3. convergere non significa automaticamente rispettare le proprietà qualitative del modello;
4. la positività può essere violata da una discretizzazione ingenua;
5. un cambio di variabile ben scelto può essere più efficace di una correzione ad hoc;
6. Milstein migliora l’accuratezza forte, ma non risolve automaticamente ogni problema strutturale.
