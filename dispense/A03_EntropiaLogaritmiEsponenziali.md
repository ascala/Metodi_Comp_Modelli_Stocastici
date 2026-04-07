---
title: "A03: Logaritmi, entropia e principio di massima entropia"
author: "Antonio Scala"
date: ""
---

Questa appendice raccoglie alcuni strumenti concettuali che ricorrono continuamente in probabilità, statistica e modellizzazione stocastica: il logaritmo delle probabilità, la sorpresa associata a un evento, l’entropia come misura dell’incertezza e il principio di massima entropia come criterio di scelta in presenza di informazione incompleta. L’obiettivo non è presentare una teoria assiomatica completa, ma fornire una cassetta degli attrezzi utile per riconoscere perché queste quantità compaiano così spesso e come vadano interpretate operativamente.

Il filo conduttore è semplice: molte quantità probabilistiche si combinano moltiplicativamente, mentre i logaritmi le rendono additive. Da qui discendono due conseguenze fondamentali. La prima è che $-\log p$ si interpreta naturalmente come contenuto informativo o sorpresa di un evento. La seconda è che, mediando questa quantità, si ottiene l’entropia. Quando poi si cerca una distribuzione coerente con pochi vincoli ma senza introdurre ipotesi arbitrarie, il principio di massima entropia seleziona la distribuzione più "neutrale" compatibile con l’informazione disponibile.

### Obiettivi didattici specifici

1. Comprendere perché il logaritmo sia lo strumento naturale per trattare probabilità e likelihood.
2. Interpretare $-\log p$ come misura della sorpresa di un evento.
3. Introdurre l’entropia come media della sorpresa.
4. Collegare log-likelihood, inferenza statistica ed entropia.
5. Formulare operativamente il principio di massima entropia.
6. Riconoscere la comparsa di distribuzioni esponenziali come conseguenza di un problema di massimizzazione con vincoli.

### Struttura della appendice

La discussione è organizzata in sei parti:

1. **Perché i logaritmi compaiono continuamente** -- prodotti, somme e stabilità numerica.  
2. **Sorpresa e contenuto informativo** -- perché $-\log p$ è la scelta naturale.  
3. **Entropia** -- media della sorpresa e misura dell’incertezza.  
4. **Likelihood e log-likelihood** -- il linguaggio operativo dell’inferenza.  
5. **Massima entropia** -- formulazione con vincoli e moltiplicatori di Lagrange.  
6. **Diagnostica concettuale** -- errori di interpretazione tipici e controlli rapidi.  

---

## 1. Perché il logaritmo compare così spesso

In probabilità, quando si combinano eventi indipendenti, le probabilità si moltiplicano. Se $p_1,\dots,p_n$ sono probabilità associate a contributi indipendenti, allora la probabilità complessiva è
$$
P=\prod_{i=1}^n p_i.
$$
Questa forma è formalmente corretta ma poco comoda. Applicando il logaritmo si ottiene
$$
\log P=\sum_{i=1}^n \log p_i.
$$

Questa riscrittura è fondamentale per tre ragioni pratiche:

1. trasforma un prodotto in una somma;
2. evita problemi numerici dovuti al prodotto di molti numeri piccoli;
3. rende interpretabili i contributi individuali come termini additivi.

In altre parole, il logaritmo non serve solo a "semplificare i conti": rende visibile la struttura del problema.

### 1.1 Regola operativa

Quando una quantità probabilistica è costruita come prodotto di molti fattori, conviene quasi sempre passare al logaritmo.

Esempi tipici:

- probabilità di una sequenza di osservazioni indipendenti;
- likelihood di un campione;
- pesi di Boltzmann in fisica statistica;
- modelli esponenziali in inferenza e machine learning.

---

## 2. Sorpresa e contenuto informativo

L’idea intuitiva è che un evento raro sia più informativo di un evento quasi certo.  
Questa intuizione porta a introdurre la quantità

$$
I(p)=\log\frac{1}{p}=-\log p,
$$

chiamata **sorpresa matematica**, **self-information** oppure **surprisal** dell’evento.

Questa definizione non è arbitraria.  
Essa emerge naturalmente se si richiede che una misura dell’informazione associata a un evento soddisfi alcune proprietà molto ragionevoli:

1. un evento certo non deve portare nuova informazione;
2. un evento più raro deve essere più informativo;
3. eventi indipendenti devono fornire un contenuto informativo totale pari alla somma dei contributi individuali.

Con queste richieste, la forma logaritmica è essenzialmente l’unica possibile, a meno di una costante moltiplicativa che dipende solo dalla scelta dell’unità di misura.

### 2.1 Proprietà fondamentali

#### Evento certo

Se $p=1$, allora
$$
I(1)=-\log 1=0.
$$

Questo riflette il fatto che un evento certo non ci dice nulla di nuovo.

#### Monotonia

Se $p$ diminuisce, $-\log p$ aumenta.  
Dunque eventi più rari sono più sorprendenti.

#### Additività per eventi indipendenti

Se due eventi indipendenti hanno probabilità $p_1$ e $p_2$, allora la probabilità congiunta è $p_1p_2$ e

$$
I(p_1p_2)=-\log(p_1p_2)=-\log p_1-\log p_2=I(p_1)+I(p_2).
$$

La sorpresa totale è quindi additiva.

### 2.2 Perché proprio il logaritmo?

Il punto decisivo è che la probabilità di eventi indipendenti si moltiplica, mentre una buona misura dell’informazione dovrebbe sommarsi.  
Il logaritmo è precisamente la trasformazione che converte prodotti in somme.

Per questo motivo, $-\log p$ non misura semplicemente la rarità di un evento, ma la rarità espressa nella scala additiva giusta per combinare contributi indipendenti.

### 2.3 Unità di misura

La base del logaritmo fissa l’unità in cui si misura l’informazione:

- base $2$ $\to$ informazione in **bit**;
- base $e$ $\to$ informazione in **nat**;
- base $10$ $\to$ informazione in **hartley** o **dit**.

La scelta della base cambia soltanto la scala numerica, non il contenuto concettuale.

---

## 3. Entropia come sorpresa media

Se una variabile aleatoria assume valori $i$ con probabilità $p_i$, la sorpresa associata all’esito $i$ è $-\log p_i$. Mediando rispetto alla distribuzione si ottiene
$$
H=-\sum_i p_i\log p_i.
$$
Questa è l’entropia di Shannon. In pratica, l’entropia misura la sorpresa media prodotta dalla sorgente.

### 3.1 Interpretazione operativa

L’entropia misura l’incertezza media della distribuzione.

- distribuzioni concentrate $\to$ entropia bassa;
- distribuzioni diffuse $\to$ entropia alta.

Non è quindi una misura del "disordine" in senso generico, ma della quantità media di informazione ottenuta osservando il risultato.

### 3.2 Casi limite utili

#### Evento certo

Se un solo esito ha probabilità $1$, allora
$$
H=0.
$$
Non c’è incertezza: nulla da apprendere.

#### Distribuzione uniforme

Se ci sono $M$ esiti equiprobabili, con $p_i=1/M$, allora
$$
H=\log M.
$$
L’entropia è massima perché non c’è alcun esito privilegiato.

### 3.3 Regola pratica

Quando si vuole quantificare "quanto una distribuzione sia incerta" senza privilegiare interpretazioni specifiche del fenomeno, l’entropia è spesso la misura di riferimento più naturale.

---

## 4. Likelihood e log-likelihood

Supponiamo di osservare dati indipendenti $x_1,\dots,x_n$ descritti da un modello parametrico con parametri $\theta$. La likelihood è
$$
L(\theta)=\prod_i p(x_i\mid\theta).
$$
Lavorare direttamente con questa quantità è possibile, ma quasi sempre scomodo. Si preferisce quindi la log-likelihood
$$
\ell(\theta)=\log L(\theta)=\sum_i \log p(x_i\mid\theta).
$$

### 4.1 Perché si usa la log-likelihood

- sostituisce un prodotto con una somma;
- è più stabile numericamente;
- è più facile da derivare e ottimizzare;
- separa il contributo delle singole osservazioni.

Dal punto di vista dell’ottimizzazione, massimizzare $L(\theta)$ o $\ell(\theta)$ è equivalente, perché il logaritmo è monotono crescente.

### 4.2 Connessione profonda tra log-likelihood, entropia e divergenza di Kullback--Leibler

Il legame tra log-likelihood ed entropia non è solo formale. C'è una struttura comune più profonda, che emerge non appena si introduce la nozione di **divergenza di Kullback--Leibler** (KL). Una volta fatta questa connessione, massimizzare la likelihood, minimizzare la cross-entropia e minimizzare la divergenza KL diventano tre formulazioni dello stesso principio inferenziale.

---

#### Divergenza di Kullback--Leibler

Siano $p$ e $q$ due distribuzioni di probabilità sullo stesso spazio discreto. La divergenza di Kullback--Leibler da $q$ a $p$ è definita come
$$
D_{\mathrm{KL}}(p \| q) = \sum_i p_i \log \frac{p_i}{q_i}.
$$

Questa quantità misura quanto $q$ si discosta da $p$, visto attraverso gli occhi di $p$.

Alcune proprietà fondamentali:

**Non negatività (disuguaglianza di Gibbs):**
$$
D_{\mathrm{KL}}(p \| q) \ge 0,
$$
con uguaglianza se e solo se $p = q$ in ogni punto.

*Dimostrazione elementare.* Per la disuguaglianza $\log x \le x - 1$ (valida per $x > 0$, con uguaglianza solo in $x = 1$):
$$
-D_{\mathrm{KL}}(p \| q) = \sum_i p_i \log \frac{q_i}{p_i} \le \sum_i p_i \left(\frac{q_i}{p_i} - 1\right) = \sum_i q_i - \sum_i p_i = 0.
$$

**Asimmetria:** in generale $D_{\mathrm{KL}}(p \| q) \neq D_{\mathrm{KL}}(q \| p)$. La divergenza KL non è una distanza in senso metrico.

**Interpretazione informazionale:** $D_{\mathrm{KL}}(p \| q)$ misura il costo medio in informazione per usare il codice ottimale per $q$ quando la distribuzione vera è $p$.

---

#### Decomposizione: cross-entropia = entropia + divergenza KL

Espandendo il logaritmo nella definizione della divergenza:
$$
D_{\mathrm{KL}}(p \| q) = \sum_i p_i \log p_i - \sum_i p_i \log q_i = -H(p) + H(p, q),
$$
dove si è introdotta la **cross-entropia** di $q$ rispetto a $p$:
$$
H(p, q) = -\sum_i p_i \log q_i.
$$

Questa decomposizione mostra tre quantità in relazione:

- $H(p)$: entropia di $p$, misura l'incertezza intrinseca della distribuzione vera;
- $H(p, q)$: cross-entropia, misura il costo medio di usare $q$ per descrivere dati generati da $p$;
- $D_{\mathrm{KL}}(p \| q)$: il surplus di incertezza dovuto all'uso di $q$ invece di $p$.

Poiché $H(p)$ non dipende da $q$, minimizzare la cross-entropia rispetto a $q$ è equivalente a minimizzare la divergenza KL.

---

#### Massima likelihood = minimizzazione della divergenza KL

Sia $p_{\mathrm{data}}$ la distribuzione empirica del campione osservato $x_1, \dots, x_n$:
$$
p_{\mathrm{data}}(x) = \frac{1}{n}\sum_{i=1}^n \mathbf{1}_{x = x_i}.
$$

La log-likelihood del modello $q_\theta$ sul campione è
$$
\ell(\theta) = \sum_{i=1}^n \log q_\theta(x_i) = n \sum_x p_{\mathrm{data}}(x) \log q_\theta(x) = -n \, H(p_{\mathrm{data}}, q_\theta).
$$

Massimizzare $\ell(\theta)$ rispetto a $\theta$ equivale quindi a minimizzare la cross-entropia $H(p_{\mathrm{data}}, q_\theta)$, e quindi --- poiché $H(p_{\mathrm{data}})$ non dipende da $\theta$ --- a minimizzare la divergenza KL:
$$
\hat\theta_{\mathrm{MLE}} = \arg\min_\theta D_{\mathrm{KL}}(p_{\mathrm{data}} \| q_\theta).
$$

**Messaggio:** la stima di massima verosimiglianza non è un criterio arbitrario. È la scelta del modello $q_\theta$ che, tra tutte le possibili distribuzioni della famiglia parametrica, è più vicina alla distribuzione empirica nel senso della divergenza KL.

---

#### Connessione con la massima entropia

C'è anche un collegamento con il principio di massima entropia discusso nella Sezione 5. Consideriamo il problema duale: invece di fissare il modello e trovare i parametri, fissiamo i vincoli e cerchiamo la distribuzione.

Il principio di massima entropia seleziona
$$
p^* = \arg\max_{p : \text{vincoli}} H(p).
$$

Si può dimostrare che questa è equivalente a
$$
p^* = \arg\min_{p : \text{vincoli}} D_{\mathrm{KL}}(p \| u),
$$
dove $u$ è la distribuzione uniforme. In altre parole, la distribuzione di massima entropia è la più vicina all'uniforme (la distribuzione "di default" priva di struttura) compatibile con i vincoli assegnati. Questo chiarisce il significato del principio: si sceglie la distribuzione meno informativa oltre i vincoli, e "meno informativa" significa "più vicina all'uniforme" nel senso KL.

---

#### Riepilogo delle equivalenze

| Formulazione | Quantità ottimizzata |
|---|---|
| Massima likelihood | $\max_\theta \sum_i \log q_\theta(x_i)$ |
| Minima cross-entropia | $\min_\theta H(p_{\mathrm{data}}, q_\theta)$ |
| Minima divergenza KL | $\min_\theta D_{\mathrm{KL}}(p_{\mathrm{data}} \| q_\theta)$ |
| Massima entropia (duale) | $\min_p D_{\mathrm{KL}}(p \| u)$ sotto vincoli |

Le prime tre colonne sono lo stesso problema sotto nomi diversi. La quarta è il problema duale, dove si ottimizza sulla distribuzione invece che sui parametri.

---

#### Nota diagnostica

Un errore frequente è confondere la direzione della divergenza KL. Le due direzioni $D_{\mathrm{KL}}(p \| q)$ e $D_{\mathrm{KL}}(q \| p)$ hanno comportamenti molto diversi:

- $D_{\mathrm{KL}}(p \| q)$ penalizza fortemente le zone dove $p > 0$ ma $q \approx 0$: il modello deve assegnare probabilità ovunque la distribuzione vera è positiva;
- $D_{\mathrm{KL}}(q \| p)$ penalizza zone dove $q > 0$ ma $p \approx 0$: il modello tende a concentrarsi su una sola moda della distribuzione vera.

La scelta della direzione non è neutra. La MLE utilizza la direzione $D_{\mathrm{KL}}(p_{\mathrm{data}} \| q_\theta)$, che forza il modello a coprire il supporto dei dati.


---

## 5. Principio di massima entropia

Il principio di massima entropia risponde a una domanda pratica: se conosciamo solo alcuni vincoli su un sistema, quale distribuzione dobbiamo scegliere?

La risposta è: tra tutte le distribuzioni compatibili con quei vincoli, si sceglie quella che massimizza l’entropia. Questa è la distribuzione che incorpora l’informazione disponibile senza aggiungere struttura arbitraria.

### 5.1 Formulazione tipica

Nel caso discreto, si vuole massimizzare
$$
H=-\sum_i p_i\log p_i
$$
sotto i vincoli
$$
\sum_i p_i=1
$$
e, ad esempio,
$$
\sum_i x_i p_i=m.
$$

Si introduce allora la Lagrangiana
$$
\mathcal{L} =
-\sum_i p_i\log p_i
-\alpha\left(\sum_i p_i-1\right)
-\beta\left(\sum_i x_i p_i-m\right).
$$

Imponendo la stazionarietà rispetto ai $p_i$ si ottiene una distribuzione della forma
$$
p_i\propto e^{-\beta x_i}.
$$
#### Nota metodologica

Il problema di massimizzare l’entropia sotto vincoli è un caso particolare di ottimizzazione vincolata. Lo strumento standard per trattarlo è il metodo dei moltiplicatori di Lagrange, richiamato in modo generale nell’Appendice A05. Qui ci limitiamo a usarlo operativamente per derivare la forma della distribuzione di massima entropia.

### 5.2 Messaggio importante

La forma esponenziale non viene ipotizzata a priori. Emerge come soluzione del problema di massimizzazione dell’entropia sotto vincoli lineari.

### 5.3 Determinazione del parametro $\beta$

Il parametro $\beta$ si fissa imponendo il vincolo sul valor medio:
$$
\sum_i x_i\frac{e^{-\beta x_i}}{Z(\beta)}=m,
$$
dove
$$
Z(\beta)=\sum_i e^{-\beta x_i}.
$$

In generale questa equazione è non lineare e va risolta numericamente. Questo è uno dei punti di contatto più diretti tra teoria dell’informazione e metodi numerici.

---

## 6. Cassetta degli attrezzi concettuale

Questa sezione riassume quando usare quali idee.

### 6.1 Quando passare ai logaritmi

Conviene usare i logaritmi quando:

- si stanno moltiplicando molte probabilità;
- si sta costruendo una likelihood;
- si vogliono sommare contributi indipendenti;
- si temono problemi di underflow numerico.

### 6.2 Quando pensare in termini di entropia

Conviene usare l’entropia quando:

- si vuole misurare l’incertezza di una distribuzione;
- si vogliono confrontare distribuzioni più o meno concentrate;
- si cerca una distribuzione "neutrale" data informazione incompleta;
- si sta lavorando con principi di inferenza non arbitrari.

### 6.3 Quando usare la massima entropia

Il principio di massima entropia è appropriato quando:

- si conoscono pochi vincoli macroscopici;
- non si vuole introdurre struttura ulteriore non giustificata;
- si cerca una distribuzione coerente ma il meno possibile informativa oltre i vincoli dati.

---

## 7. Diagnostica rapida: errori concettuali tipici

### 7.1 Confondere probabilità alta con informazione alta

È il contrario: eventi molto probabili portano poca informazione, eventi rari ne portano di più.

### 7.2 Interpretare l’entropia come "disordine" senza contesto

Questa è una scorciatoia intuitiva, ma rischiosa. Operativamente, l’entropia è una misura di incertezza media.

### 7.3 Pensare che la forma esponenziale sia sempre un’assunzione empirica

In molti casi non è un’assunzione, ma la conseguenza di un problema di massima entropia con vincoli lineari.

### 7.4 Dimenticare la normalizzazione

Ogni distribuzione ottenuta via massima entropia richiede una costante di normalizzazione, spesso indicata con $Z$. Trascurarla equivale a non avere ancora una vera distribuzione di probabilità.

---

## 8. Take-home message

- Il logaritmo trasforma prodotti di probabilità in somme e rende il problema trattabile.
- La quantità $-\log p$ misura la sorpresa di un evento.
- L’entropia è la sorpresa media, quindi una misura naturale dell’incertezza.
- La log-likelihood è la forma operativa standard nell’inferenza statistica.
- Il principio di massima entropia seleziona la distribuzione meno arbitraria compatibile con i vincoli disponibili.
- Le distribuzioni esponenziali emergono naturalmente da questo principio, non come pura convenzione.
