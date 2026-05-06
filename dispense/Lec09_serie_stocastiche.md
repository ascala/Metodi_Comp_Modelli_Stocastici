---
title: "08: Serie stocastiche e modelli per dati temporali"
author: "Antonio Scala"
date: ""
---

Nelle lezioni precedenti abbiamo introdotto diversi processi stocastici come oggetti dinamici: catene di Markov, processi di salto, SDE, master equation, Fokker--Planck e branching process. In quei casi il punto di partenza era quasi sempre un modello noto, dal quale generare traiettorie o distribuzioni.

Qui cambiamo prospettiva. Supponiamo di osservare una sequenza temporale
$$
X_0,X_1,\dots,X_T,
$$
e di voler capire quale tipo di modello sia adatto a descriverla. Non partiamo quindi da una SDE continua già assegnata, ma dai dati temporali e dalle loro caratteristiche: memoria, trend, stazionarietà, asimmetria, code pesanti, volatilità variabile, salti, conteggi, regimi.

Una serie stocastica non è semplicemente una collezione di variabili aleatorie. L'ordine temporale contiene informazione. Due serie possono avere lo stesso istogramma ma dinamiche completamente diverse: una può essere indipendente, una persistente, una mean-reverting, una intermittente, una soggetta a shock rari ma grandi.

Questa lezione introduce una cassetta degli attrezzi modellistica per analizzare serie stocastiche discrete nel tempo. L'obiettivo non è fare un corso completo di time series, ma costruire un ponte operativo verso la stima dei parametri: prima di stimare un modello, bisogna sapere quale classe di modelli abbia senso provare.

## Obiettivi didattici specifici

Al termine della lezione lo studente dovrebbe essere in grado di:

1. distinguere campioni indipendenti e serie temporali dipendenti;
2. riconoscere memoria, trend, non stazionarietà e cambiamenti di scala;
3. usare autocorrelazione e autocorrelazione degli incrementi come strumenti diagnostici;
4. distinguere rumore bianco, random walk, AR, MA e ARMA;
5. capire il ruolo delle innovazioni non gaussiane e delle code pesanti;
6. riconoscere asimmetrie nella distribuzione e nella dinamica;
7. comprendere l'idea di volatilità condizionata e modelli ARCH/GARCH;
8. interpretare modelli a soglia, modelli con regimi e modelli per conteggi;
9. collegare la scelta del modello alla forma della likelihood nella lezione successiva.

## Struttura della lezione

1. Dati indipendenti e dati temporali
2. Diagnostica iniziale: scala, memoria, incrementi
3. Rumore bianco e innovazioni
4. Random walk e processi integrati
5. Modelli autoregressivi AR
6. Modelli a media mobile MA e ARMA
7. Innovazioni non gaussiane: code pesanti e outlier
8. Asimmetrie: distribuzione, dinamica e risposta agli shock
9. Volatilità condizionata: ARCH e GARCH
10. Modelli a soglia e cambiamenti di regime
11. Serie di conteggi e processi discreti nel tempo
12. Come scegliere un modello: diagnostica e compromessi
13. Ponte verso la stima dei parametri

---

# 1. Dati indipendenti e dati temporali

## 1.1 Campioni indipendenti

Un campione indipendente è una sequenza di osservazioni

$$
y_1,y_2,\dots,y_n
$$

che possiamo idealmente pensare come estrazioni ripetute dalla stessa distribuzione. Se le osservazioni sono indipendenti e identicamente distribuite, l'ordine in cui vengono scritte non contiene informazione.

In questo caso la struttura probabilistica è

$$
p(y_1,\dots,y_n)=\prod_{i=1}^n p(y_i).
$$

Rimescolare i dati non cambia il problema statistico.

## 1.2 Serie temporali

Una serie temporale è invece una sequenza ordinata,

$$
X_0,X_1,\dots,X_T,
$$

dove $X_t$ rappresenta lo stato osservato al tempo $t$.

In questo caso l'ordine è informativo. Rimescolare i dati distrugge la struttura temporale.

La fattorizzazione generale della probabilità congiunta è

$$
p(x_0,x_1,\dots,x_T)
= p(x_0)\prod_{t=0}^{T-1}p(x_{t+1}\mid x_t,x_{t-1},\dots,x_0).
$$

Questa formula è soltanto la regola della probabilità composta, ma chiarisce il punto: per modellare una serie bisogna specificare come il futuro dipende dal passato.

## 1.3 Il caso Markoviano come primo modello

Una semplificazione frequente è assumere che il futuro dipenda dal passato solo tramite lo stato presente:

$$
p(x_{t+1}\mid x_t,x_{t-1},\dots,x_0)=p(x_{t+1}\mid x_t).
$$

Allora

$$
p(x_0,x_1,\dots,x_T)
= p(x_0)\prod_{t=0}^{T-1}p(x_{t+1}\mid x_t).
$$

Questa è una struttura markoviana. Non implica che la serie sia indipendente: le osservazioni sono legate da transizioni condizionate.

> Idea chiave: nei dati temporali l'informazione non è solo nei valori osservati, ma anche nel modo in cui un valore segue il precedente.

# 2. Diagnostica iniziale: scala, memoria, incrementi

Prima di scegliere un modello conviene guardare la serie con alcune domande semplici.

## 2.1 La serie ha una scala stabile?

Un primo grafico è

$$
t \mapsto x_t.
$$

Da questo si cerca di capire se:

* la media appare costante;
* la varianza appare costante;
* sono presenti trend;
* esistono salti isolati;
* compaiono regimi diversi;
* l'ampiezza delle fluttuazioni cambia nel tempo.

Se la scala cambia, un modello stazionario semplice può essere inadeguato.

## 2.2 Valori o incrementi?

In molte serie è più informativo guardare gli incrementi

$$
\Delta X_t=X_{t+1}-X_t.
$$

Oppure, per grandezze positive come prezzi, dimensioni o concentrazioni, i ritorni logaritmici

$$
r_t=\log X_{t+1}-\log X_t.
$$

Un random walk ha valori non stazionari ma incrementi stazionari. Questo è un punto operativo importante: spesso non si modella direttamente $X_t$, ma la sua variazione.

## 2.3 Memoria lineare

La memoria lineare si valuta con l'autocorrelazione. Per una serie stazionaria con media $\mu$,

$$
C(k)=\mathbb{E}\big[(X_{t+k}-\mu)(X_t-\mu)\big]
$$

e

$$
\rho(k)=\frac{C(k)}{C(0)}.
$$

Se $\rho(k)$ decade lentamente, la serie ha memoria lunga o persistenza. Se decade rapidamente, la memoria lineare è breve.

## 2.4 Memoria non lineare

Una serie può avere autocorrelazione quasi nulla ma dipendenza temporale importante. Un esempio tipico sono molte serie finanziarie: i ritorni possono essere poco correlati, ma i ritorni assoluti o quadrati sono correlati.

Per questo si guardano anche:

$$
|X_t|,
\qquad
X_t^2,
\qquad
|\Delta X_t|,
\qquad
(\Delta X_t)^2.
$$

Se le ampiezze delle fluttuazioni sono correlate, serve un modello con volatilità variabile nel tempo.

# 3. Rumore bianco e innovazioni

## 3.1 Rumore bianco

Il modello più semplice è una sequenza di variabili indipendenti con media nulla e varianza costante:

$$
\eta_t,
\qquad
\mathbb{E}[\eta_t]=0,
\qquad
\mathrm{Var}(\eta_t)=\sigma^2,
\qquad
\mathbb{E}[\eta_t\eta_s]=0 \quad t\neq s.
$$

Se $\eta_t$ è gaussiano,

$$
\eta_t\sim \mathcal{N}(0,\sigma^2),
$$

si parla di rumore bianco gaussiano.

## 3.2 Innovazioni

Nei modelli di serie temporali il rumore bianco rappresenta spesso l'*innovazione*, cioè la parte nuova e non prevedibile al tempo $t$.

Un modello può essere scritto schematicamente come

$$
X_{t+1}=\text{parte prevedibile dal passato}+\text{innovazione}.
$$

La parte prevedibile descrive memoria, trend o ritorno alla media. L'innovazione descrive lo shock non anticipabile.

## 3.3 Perché non assumere sempre rumore gaussiano?

L'ipotesi gaussiana è comoda, ma non sempre realistica. Molte serie empiriche mostrano:

* code più pesanti della gaussiana;
* outlier frequenti;
* asimmetria;
* shock rari ma grandi;
* distribuzioni discrete o limitate.

In questi casi si possono usare innovazioni non gaussiane: Student-t, Laplace, miscele gaussiane, rumore asimmetrico, distribuzioni discrete.

> Idea chiave: la struttura temporale e la distribuzione delle innovazioni sono due ingredienti distinti del modello.

# 4. Random walk e processi integrati

## 4.1 Random walk

Un random walk è definito da

$$
X_{t+1}=X_t+\eta_t.
$$

Assumendo $X_0=0$,

$$
X_t=\sum_{k=0}^{t-1}\eta_k.
$$

Il processo accumula shock indipendenti.

## 4.2 Varianza crescente

Se

$$
\mathbb{E}[\eta_t]=0,
\qquad
\mathrm{Var}(\eta_t)=\sigma^2,
$$

allora

$$
\mathbb{E}[X_t]=0,
\qquad
\mathrm{Var}(X_t)=t\sigma^2.
$$

La varianza cresce nel tempo: il processo non è stazionario.

## 4.3 Random walk con drift

Aggiungendo un drift,

$$
X_{t+1}=X_t+\mu+\eta_t,
$$

si ottiene

$$
\mathbb{E}[X_t]=X_0+\mu t.
$$

Il drift introduce una tendenza sistematica, mentre il rumore produce dispersione attorno a tale tendenza.

## 4.4 Processi integrati

Un processo può essere non stazionario nei livelli ma stazionario nelle differenze. Si dice allora che è integrato di ordine uno, informalmente $I(1)$.

In pratica:

$$
X_t \text{ non stazionario},
\qquad
\Delta X_t \text{ stazionario}.
$$

Questo caso è molto frequente in serie economiche, finanziarie e demografiche.

# 5. Modelli autoregressivi AR

## 5.1 AR(1)

Il modello autoregressivo più semplice è

$$
X_{t+1}=c+aX_t+\eta_t.
$$

Se $|a|<1$, il processo è stazionario con media

$$
\mu=\frac{c}{1-a}.
$$

> **Dimostrazione:** All'equilibrio stazionario il valore atteso non cambia nel tempo, ovvero $\mathbb{E}[X_{t+1}] = \mathbb{E}[X_t] = \mu$. Prendendo il valore atteso di entrambi i membri e usando $\mathbb{E}[\eta_t]=0$
>
> $$\mu = c + a\mu \implies \mu(1-a) = c \implies \mu = \frac{c}{1-a}.$$
>
> La condizione $|a|<1$ garantisce che $1-a\ne 0$ e che le deviazioni dalla media si contraggono nel tempo.

Il processo può essere quindi scritto come ritorno verso una media

$$X_{t+1}=\mu+a\cdot(X_t-\mu)+\eta_t$$

con il parametro $a$ che controlla la persistenza.

## 5.2 Interpretazione del coefficiente autoregressivo

* $a=0$: nessuna memoria lineare;
* $0<a<1$: persistenza positiva;
* $a\approx 1$: memoria lunga e quasi random walk;
* $a<0$: alternanza, anticorrelazione;
* $|a|>1$: instabilità.

Per un AR(1) stazionario,

$$
\rho(k)=a^k.
$$
> **Dimostrazione.** Per un AR(1) stazionario con media zero (senza perdita di generalità, $c=0$) si ha $X_{t+1}=aX_t+\eta_t$ con $\eta_t$ indipendente dal passato. L'autocovarianza al lag $k$ è $\gamma(k)=\mathbb{E}[X_tX_{t-k}]$. Moltiplicando entrambi i membri per $X{t-k}$ e prendendo il valore atteso:
>
> $$\gamma(k)=\mathbb{E}[X_tX_{t-k}]=a\mathbb{E}[X_{t-1}X{t-k}]+\mathbb{E}[\eta_tX{t-k}]=a\gamma(k-1),$$
>
> dove l'ultimo termine si annulla perché $\eta_t$ è indipendente da $X_{t-k}$ per $k\geq1$. La ricorrenza $\gamma(k)=a\gamma(k-1)$ si itera fino a ottenere $\gamma(k)=a^k\gamma(0)$. Dividendo per la varianza $\gamma(0)$:
>
>$$\rho(k)=\frac{\gamma(k)}{\gamma(0)}=a^k$$
>
> Quindi l'autocorrelazione decade esponenzialmente.

## 5.3 AR(p)

Un modello autoregressivo di ordine $p$ usa più valori passati:

$$
X_t=c+a_1X_{t-1}+a_2X_{t-2}+\dots+a_pX_{t-p}+\eta_t.
$$

Questo permette dinamiche più ricche:

* oscillazioni smorzate;
* memoria distribuita su più ritardi;
* risposta più lenta agli shock;
* autocorrelazioni non puramente esponenziali.

## 5.4 Interpretazione dinamica

Un modello AR non descrive solo correlazione statistica. Può essere letto come un modello dinamico discreto: il valore presente viene aggiornato in base a una combinazione del passato più uno shock.

Questa interpretazione lo collega naturalmente ai modelli dinamici del corso, ma senza dover passare necessariamente da una SDE continua.

# 6. Modelli a media mobile MA e ARMA

## 6.1 Modello MA(1)

Nel modello autoregressivo il valore dipende dai valori passati della serie. Nel modello a media mobile (MA sta per *Moving Average*), invece, il valore dipende dagli shock passati.

Il modello MA(1) è

$$
X_t=\eta_t+b\eta_{t-1}.
$$

Qui la memoria non è nello stato osservato, ma nell'effetto persistente degli shock.

## 6.2 MA(q)

Più in generale,

$$
X_t=\eta_t+b_1\eta_{t-1}+\dots+b_q\eta_{t-q}.
$$

Uno shock non influenza solo il tempo in cui avviene, ma anche alcuni tempi successivi.

## 6.3 Differenza intuitiva tra AR e MA

Nel modello AR, la serie si autoalimenta:

$$
X_t \leftarrow X_{t-1},X_{t-2},\dots
$$

Nel modello MA, la serie è una sovrapposizione filtrata di shock:

$$
X_t \leftarrow \eta_t,\eta_{t-1},\dots
$$

Entrambe le strutture producono memoria, ma con meccanismi diversi.

## 6.4 ARMA(p,q)

Combinando le due idee si ottiene il modello ARMA:

$$
X_t=c+\sum_{i=1}^p a_iX_{t-i}+\eta_t+
\sum_{j=1}^q b_j\eta_{t-j}.
$$

I modelli ARMA sono utili per serie stazionarie con memoria lineare. L'AR descrive la persistenza dello stato; l'MA descrive la persistenza degli shock.

## 6.5 Quando usare ARMA

ARMA è appropriato quando:

* la serie è approssimativamente stazionaria;
* l'autocorrelazione mostra struttura non banale;
* gli shock hanno effetto transitorio;
* non c'è evidenza forte di volatilità variabile, soglie o regimi.

Se invece la varianza cambia nel tempo o gli shock estremi sono frequenti, serve estendere il modello.

# 7. Innovazioni non gaussiane: code pesanti e outlier

## 7.1 Il limite della gaussiana

Molti modelli base assumono

$$
\eta_t\sim \mathcal{N}(0,\sigma^2).
$$

Questa ipotesi rende la likelihood semplice e spesso permette stime efficienti. Tuttavia, la gaussiana assegna probabilità molto piccola agli eventi estremi.

In molte serie reali, gli eventi estremi sono più frequenti di quanto previsto dalla gaussiana.

## 7.2 Innovazioni Student-t

Una scelta comune per descrivere code pesanti è la distribuzione di Student:

$$
\eta_t\sim t_\nu(0,s).
$$

Il parametro $\nu$ controlla lo spessore delle code. Per $\nu$ grande la distribuzione si avvicina alla gaussiana; per $\nu$ piccolo le code sono più pesanti.

Questa scelta è utile quando la dinamica media è ragionevolmente descritta da un AR o ARMA, ma i residui mostrano outlier troppo frequenti.

## 7.3 Innovazioni di Laplace

La distribuzione di Laplace ha densità proporzionale a

$$
\exp\left(-\frac{|x|}{b}\right).
$$

Ha code più pesanti della gaussiana e un picco più marcato attorno a zero. Può essere utile quando molti incrementi sono piccoli ma gli scarti grandi sono più frequenti del previsto.

## 7.4 Miscele gaussiane

Un'altra possibilità è usare una miscela:

$$
\eta_t \sim (1-\pi)\mathcal{N}(0,\sigma_1^2)+\pi\mathcal{N}(0,\sigma_2^2),
\qquad
\sigma_2^2\gg\sigma_1^2.
$$

Interpretazione:

* la maggior parte del tempo il sistema subisce shock ordinari;
* con piccola probabilità subisce shock anomali o estremi.

Questa è una forma semplice di modello con eventi rari.

## 7.5 Diagnostica delle code

Per capire se la gaussiana è inadeguata si usano:

* istogramma dei residui;
* QQ-plot contro gaussiana;
* frequenza di outlier normalizzati;
* confronto tra varianza e deviazione assoluta media;
* stabilità delle stime rispetto alla rimozione di pochi punti estremi.

Se pochi punti dominano la stima, un modello gaussiano può essere fragile.

## 7.6 Il QQ-plot come diagnostica delle code

Il QQ-plot, o quantile--quantile plot, è uno strumento grafico per confrontare la distribuzione empirica dei residui con una distribuzione teorica di riferimento. Nel nostro caso la scelta più comune è confrontare i residui standardizzati con una gaussiana standard.

Supponiamo di avere residui standardizzati

$$z_1,z_2,...,z_n\;.$$

Li ordiniamo in modo crescente:

$$z_{k_1}\leq z_{k_2} \leq...\leq z_{k_n}$$

dove $k_1,\ldots,k_n$ è la permutazione di $1,\ldots,n$ che ordina gli $z_i$

A ciascun valore ordinato associamo una probabilità cumulativa empirica, ad esempio

$$ p_i  =(i-1/2)/n$$

e calcoliamo il quantile teorico gaussiano corrispondente:

$$ q_i=\Phi^{-1}(p_i)\;,$$

dove $\Phi^{-1}$ è l'inversa della funzione di distribuzione cumulativa $\Phi$ della normale standard.

Il QQ-plot rappresenta quindi i punti

$$ (q_i,z_{k_i})\;.$$

Se i residui sono compatibili con una distribuzione gaussiana, i punti si dispongono approssimativamente lungo una retta. Se invece le code empiriche sono più pesanti di quelle gaussiane, i punti si allontanano dalla retta soprattutto agli estremi: nella coda sinistra tendono a stare sotto la retta, mentre nella coda destra tendono a stare sopra la retta.

Questa forma indica che gli eventi estremi osservati sono più grandi, in valore assoluto, di quelli che ci si aspetterebbe sotto ipotesi gaussiana. In tal caso la parte dinamica del modello può anche essere ragionevole, ma la distribuzione dell'innovazione è inadeguata.

Il QQ-plot è quindi particolarmente utile perché separa due domande:

1. il modello ha catturato la dipendenza temporale?
2. la distribuzione scelta per le innovazioni descrive bene gli shock estremi?

Un istogramma può nascondere le code, perché gli eventi estremi sono pochi. Il QQ-plot, invece, rende visibile proprio il comportamento degli estremi. Per questo è uno strumento naturale per decidere se passare da innovazioni gaussiane a innovazioni Student-t, Laplace, miscele gaussiane o altre distribuzioni con code più pesanti.

# 8. Asimmetrie: distribuzione, dinamica e risposta agli shock

## 8.1 Asimmetria distributiva

Una serie o i suoi incrementi possono avere distribuzione asimmetrica. Questo significa che shock positivi e negativi non hanno la stessa struttura probabilistica.

La simmetria gaussiana implica che deviazioni positive e negative della stessa ampiezza siano ugualmente probabili. Molti fenomeni non rispettano questa proprietà.

Esempi:

* perdite finanziarie estreme più frequenti dei guadagni estremi;
* tempi di attesa positivi con coda lunga;
* conteggi con asimmetria destra;
* crescita demografica con rari collassi;
* segnali fisici con bursts positivi.

## 8.2 Innovazioni asimmetriche

Un modo semplice per introdurre asimmetria è usare innovazioni non simmetriche. Per esempio:

* distribuzione skew-normal;
* distribuzione skew-t;
* distribuzione gamma centrata;
* rumore a salti con ampiezze positive e negative diverse.

Formalmente il modello può restare lineare nella parte dinamica,

$$
X_t=c+aX_{t-1}+\eta_t,
$$

ma con $\eta_t$ non simmetrico.

## 8.3 Asimmetria dinamica

L'asimmetria può riguardare non solo la distribuzione degli shock, ma anche la risposta del sistema.

Per esempio, il ritorno alla media può essere più rapido sopra la media che sotto la media:

$$
X_{t+1}-\mu=
\begin{cases}
a_+(X_t-\mu)+\eta_t, & X_t\ge \mu,\\
a_-(X_t-\mu)+\eta_t, & X_t<\mu.
\end{cases}
$$

Se $a_+\neq a_-$, il sistema ha una dinamica asimmetrica.

## 8.4 Risposta asimmetrica agli shock

In alcune serie, shock negativi aumentano la variabilità futura più degli shock positivi. Questo effetto è tipico di molte serie finanziarie, ma l'idea è più generale: eventi di segno diverso possono avere impatti diversi sulla dinamica successiva.

Questa osservazione porta ai modelli di volatilità asimmetrica, discussi più avanti.

## 8.5 Diagnostica dell'asimmetria

Segnali utili:

* istogramma non simmetrico;
* media e mediana molto diverse;
* QQ-plot con deviazioni diverse nelle due code;
* distribuzione dei residui positiva e negativa con scale diverse;
* scatter plot $X_t$ vs $X_{t+1}$ con pendenze diverse sopra e sotto una soglia.

Il QQ-plot discusso nella sezione precedente è utile anche per diagnosticare l'asimmetria. Se entrambe le code si allontanano dalla retta in modo simile, il problema principale può essere la presenza di code pesanti simmetriche. Se invece una sola coda devia in modo marcato, oppure le due code deviano con intensità diversa, allora la distribuzione delle innovazioni non è soltanto non gaussiana, ma anche asimmetrica.

Questa distinzione è importante nella scelta del modello: code pesanti simmetriche suggeriscono distribuzioni come Student-t o Laplace, mentre deviazioni asimmetriche suggeriscono innovazioni skew, rumore a salti asimmetrici o modelli con risposta diversa agli shock positivi e negativi.

# 9. Volatilità condizionata: ARCH e GARCH

## 9.1 Il problema

Una serie può avere media quasi imprevedibile ma ampiezza delle fluttuazioni prevedibile. Per semplificare la notazione, indichiamo con $\mathcal{F}_t$ l'informazione disponibile fino al tempo $t$. > Senza tale notazione per un ARMA(p,q) avremo dovuto indicare esplicitamente nelle formule i valori passati $X_{t-1},\ldots,X_{t-p}$ e  $\eta_{t-1},\ldots,\eta_{t-q}$. 

Per esempio, potremmo avere

$$
\mathbb{E}[X_{t+1}\mid \mathcal{F}_t]\approx 0,
$$

ma la varianza condizionata

$$
\mathrm{Var}(X_{t+1}\mid \mathcal{F}_t) = \sigma_t^2
$$

cambia nel tempo.

In altre parole: non sappiamo prevedere bene il segno del prossimo shock, ma possiamo prevedere se il prossimo periodo sarà tranquillo o turbolento.

## 9.2 Clustering della volatilità

In molte serie gli shock grandi tendono a raggrupparsi. Periodi di grande variabilità sono seguiti da altri periodi di grande variabilità; periodi tranquilli da altri periodi tranquilli.

Questo fenomeno si chiama clustering della volatilità.

La diagnostica tipica è:

* autocorrelazione debole di $X_t$;
* autocorrelazione positiva di $X_t^2$ o $|X_t|$.

## 9.3 Modello ARCH(1)

Un modello ARCH(1) scrive

$$
X_t=\sigma_t\eta_t,
$$

dove $\eta_t$ è rumore bianco con media zero e varianza unitaria, mentre

$$
\sigma_t^2=\alpha_0+\alpha_1X_{t-1}^2.
$$

La varianza condizionata dipende dallo shock quadratico precedente.

Se $X_{t-1}^2$ è grande, ci aspettiamo una varianza alta al tempo successivo.

> Nota: **ARCH** sta per *Autoregressive Conditionally Heteroskedastic*: 
>* Autoregressive: la varianza condizionata segue una dinamica autoregressiva.
>* Conditionally: l'eteroschedasticità è condizionata alla storia osservata, non è fissa.
>* Heteroskedastic: la varianza non è costante nel tempo.

## 9.4 Modello GARCH(1,1)

Il modello GARCH(1,1) aggiunge persistenza nella varianza:

$$
X_t=\sigma_t\eta_t,
$$

$$
\sigma_t^2=\alpha_0+\alpha_1X_{t-1}^2+\beta_1\sigma_{t-1}^2.
$$

Qui la volatilità corrente dipende sia dallo shock passato sia dalla volatilità passata.

Questo produce cluster di volatilità più persistenti.

> Nota; **GARCH** aggiunge ad **ARCH** la G di Generalized: invece di dipendere solo dai quadrati passati dei residui (come in ARCH), la varianza condizionata dipende anche dai propri valori passati, analogamente a come un ARMA generalizza un AR.

## 9.5 Innovazioni non gaussiane nei GARCH

Anche nei modelli GARCH si può scegliere la distribuzione di $\eta_t$.

Una scelta gaussiana può sottostimare gli eventi estremi. Per questo spesso si usano innovazioni Student-t o skew-t.

Quindi un modello può combinare:

* dipendenza temporale nella varianza;
* code pesanti;
* asimmetria.

## 9.6 Modelli asimmetrici di volatilità

Per rappresentare risposte diverse a shock positivi e negativi si possono introdurre termini asimmetrici.

Un esempio schematico è

$$
\sigma_t^2 =
\alpha_0 +
\alpha_1 X_{t-1}^2 +
\gamma X_{t-1}^2\,\mathbf{1}_{\{X_{t-1}<0\}} +
\beta_1\sigma_{t-1}^2.
$$

Dove $\mathbf{1}_{\{x<0\}}$ è una *funzione indicatrice* che vale $1$ se $x<0$, 0 altrimenti. Quindi

* Se $X_{t-1}\ge 0$, il termine quadratico entra con coefficiente $\alpha_1$.
* Se $X_{t-1}<0$, il termine quadratico entra con coefficiente $\alpha_1+\gamma$.

Quando $\gamma>0$, shock negativi aumentano la volatilità futura più degli shock positivi della stessa ampiezza. Per garantire $\sigma_t^2\ge 0$ servono condizioni sui parametri, ad esempio
$\alpha_0>0$, $\alpha_1\ge 0$, $\beta_1\ge 0$ e $\alpha_1+\gamma\ge 0$.

# 10. Modelli a soglia e cambiamenti di regime

## 10.1 Perché introdurre soglie

Molti sistemi non rispondono allo stesso modo in tutte le regioni dello spazio degli stati.

Esempi:

* un sistema ecologico può avere dinamiche diverse sopra o sotto una soglia critica;
* un mercato può comportarsi diversamente in periodi normali e di crisi;
* un processo sociale può accelerare oltre una soglia di attenzione;
* una popolazione può collassare sotto una soglia minima.

Un modello lineare globale può non catturare questi comportamenti.

## 10.2 Threshold autoregressive model

Un modello autoregressivo a soglia può essere scritto come

$$
X_{t+1}=\begin{cases}
c_1+a_1X_t+\eta_t, & X_t\le r,\\
c_2+a_2X_t+\eta_t, & X_t>r.
\end{cases}
$$

La dinamica cambia quando $X_t$ attraversa la soglia $r$.

Questo permette ritorni alla media diversi, persistenza diversa o instabilità locale in regioni diverse.

## 10.3 Modelli a regimi latenti

A volte il regime non è osservato direttamente. Si introduce allora una variabile nascosta $S_t$ che indica il regime:

$$
S_t\in\{1,2,\dots,K\}.
$$

Condizionatamente al regime, la serie segue un modello diverso:

$$
X_t=c_{S_t}+a_{S_t}X_{t-1}+\eta_t.
$$

Il regime $S_t$ può evolvere come una catena di Markov.

Questi modelli sono utili per descrivere alternanza tra periodi normali e periodi anomali.

## 10.4 Diagnostica dei regimi

Segnali di possibili regimi:

* cambiamenti persistenti di media;
* cambiamenti persistenti di varianza;
* cluster di outlier;
* relazione $X_t$--$X_{t+1}$ diversa in regioni diverse;
* residui non omogenei nel tempo.

# 11. Serie di conteggi e processi discreti nel tempo

## 11.1 Quando i dati sono conteggi

Molte serie temporali non sono continue, ma discrete e non negative:

$$
X_t\in\{0,1,2,\dots\}.
$$

Esempi:

* numero giornaliero di eventi;
* arrivi in una coda;
* nuovi casi in un'epidemia;
* numero di messaggi o interazioni;
* conteggio di guasti;
* citazioni o menzioni nel tempo.

In questi casi un modello gaussiano può essere inappropriato, soprattutto quando i conteggi sono piccoli.

## 11.2 Poisson autoregressivo condizionato

Un'idea semplice è modellare il conteggio come Poisson condizionato al passato:

$$
X_t\mid \mathcal{F}_{t-1}\sim \mathrm{Poisson}(\lambda_t),
$$

con intensità variabile nel tempo, ad esempio

$$
\lambda_t=\omega+\alpha X_{t-1}+\beta\lambda_{t-1}.
$$

Questo è analogo a un GARCH per conteggi: l'intensità corrente dipende dagli eventi passati e dall'intensità passata.

> **Nota.** L'idea di un tasso che dipende dallo stato corrente del sistema è la stessa alla base del tau-leaping (vedi simulazioni di eventi discreti / metodo di Gillespie) e dei processi di salto in tempo continuo (vedi processi di salto e master equation). La differenza è che qui $\lambda_t$ ha una propria dinamica con memoria esplicita su $\lambda_{t-1}$, mentre nei modelli event-driven il tasso viene ricalcolato localmente ad ogni evento.

## 11.3 Sovradispersione

Nel modello di Poisson condizionato vale

$$
X_t\mid\mathcal{F}_{t-1}\sim \mathrm{Poisson}(\lambda_t),
$$

quindi

$$
\mathbb{E}[X_t\mid\mathcal{F}_{t-1}] =
\mathrm{Var}(X_t\mid\mathcal{F}_{t-1}) =
\lambda_t.
$$

Molti dati reali mostrano invece una varianza empirica maggiore della media. Questo fenomeno si chiama sovradispersione.

In tal caso si possono usare modelli binomiali negativi:

$$
X_t\mid\mathcal{F}_{t-1}\sim \mathrm{NegBin}(m_t,k),
$$

che permettono varianza superiore alla media.

> **Nota sulla distribuzione binomiale negativa.** Con la notazione $\mathrm{NegBin}(m,k)$ indichiamo qui una distribuzione per conteggi non negativi con media $m$ e parametro di dispersione $k>0$. Una parametrizzazione comune è
> $$
\mathbb{E}[X]=m,
\qquad
\mathrm{Var}(X)=m+\frac{m^2}{k}.
$$
> con funzione di massa di probabilità
>  $$ 
P(X=j) = \binom{j+k-1}{j}\left(\frac{k}{k+m}\right)^k\left(\frac{m}{k+m}\right)^j, \qquad j=0,1,2,\dots
$$
> * Per $k\to\infty$ la varianza tende a $m$ e si recupera il comportamento poissoniano.
> * Per $k$ piccolo la varianza è molto più grande della media, quindi la distribuzione descrive dati sovradispersi.

## 11.4 Zeri in eccesso

Alcune serie presentano molti più zeri di quelli previsti da un modello Poisson o binomiale negativo.

In questo caso si possono usare modelli zero-inflated: con una certa probabilità il processo è in uno stato inattivo che produce zero, altrimenti genera conteggi secondo una distribuzione ordinaria.

## 11.5 Collegamento con processi di eventi

Le serie di conteggi possono derivare da processi puntuali osservati in finestre temporali. Per esempio, se $N(t)$ è un processo di conteggio, possiamo osservare

$$
X_k=N((k+1)\Delta t)-N(k\Delta t).
$$

La scelta della finestra $\Delta t$ modifica la struttura della serie: finestre troppo piccole producono molti zeri; finestre troppo grandi nascondono la dinamica fine degli eventi.

# 12. Come scegliere un modello: diagnostica e compromessi

Non esiste un modello universalmente corretto. La scelta dipende dalla domanda scientifica, dalla scala dei dati e dalle proprietà empiriche della serie.

## 12.1 Domande operative

Prima di scegliere un modello conviene chiedere:

1. La variabile è continua, positiva, discreta o limitata?
2. La serie appare stazionaria?
3. È più naturale modellare i livelli o gli incrementi?
4. Esiste autocorrelazione nei valori?
5. Esiste autocorrelazione nei quadrati o nei valori assoluti?
6. I residui sono gaussiani o hanno code pesanti?
7. La distribuzione è simmetrica?
8. Ci sono soglie o regimi?
9. Esistono vincoli fisici o interpretativi?
10. L'obiettivo è previsione, interpretazione o stima di parametri meccanicistici?

## 12.2 Tabella orientativa

| Evidenza empirica                    | Classe di modello candidata               |
| ------------------------------------ | ----------------------------------------- |
| Nessuna memoria evidente             | rumore bianco                             |
| Trend stocastico, varianza crescente | random walk / processo integrato          |
| Autocorrelazione nei valori          | AR / ARMA                                 |
| Shock con effetto transitorio        | MA / ARMA                                 |
| Code pesanti nei residui             | innovazioni Student-t / Laplace / miscele |
| Asimmetria nei residui               | innovazioni skew / rumore asimmetrico     |
| Autocorrelazione nei quadrati        | ARCH / GARCH                              |
| Shock negativi più destabilizzanti   | GARCH asimmetrico                         |
| Dinamica diversa sopra/sotto soglia  | threshold AR                              |
| Alternanza tra fasi                  | modelli a regimi / Markov switching       |
| Conteggi non negativi                | Poisson autoregressivo / NegBin           |
| Molti zeri                           | zero-inflated models                      |

## 12.3 Parsimonia

Aggiungere complessità migliora spesso l'adattamento apparente, ma può peggiorare interpretabilità e robustezza.

Una regola pratica è partire dal modello più semplice capace di riprodurre le caratteristiche essenziali della serie, poi aggiungere complessità solo se i residui mostrano struttura sistematica.

La sequenza tipica è:

1. modello semplice;
2. stima;
3. residui;
4. diagnostica dei residui;
5. eventuale estensione del modello.

# 13. Stima dei parametri

Per le serie stocastiche diventa centrale stimare i parametri. Ciò avviene massimizzando la *likelihood* del modello usato, ovvero una funzione che misura quanto sia probabile che la serie osservata sia stata generata dati dei parametri. La forma della likelihood dipende quindi dalla classe di modello scelta.

## 13.1 Dati indipendenti

Se i dati sono indipendenti,

$$
p(y_1,\dots,y_n\mid\theta)=\prod_{i=1}^n p(y_i\mid\theta).
$$

La log-likelihood è

$$
\ell(\theta)=\sum_{i=1}^n\log p(y_i\mid\theta).
$$

## 13.2 Modelli condizionati al passato

Per una serie temporale, si scrive invece

$$
p(x_0,x_1,\dots,x_T\mid\theta) =
p(x_0\mid\theta)
\prod_{t=1}^T p(x_t\mid x_{t-1},x_{t-2},\dots;\theta).
$$

Nei modelli ARMA, GARCH, a soglia o per conteggi, la densità condizionata cambia forma, ma la logica è la stessa: ogni termine della likelihood descrive la distribuzione del prossimo valore dato il passato osservato.

## 13.3 Esempi di densità condizionata

* AR(1) gaussiano$$
X_t\mid X_{t-1}\sim
\mathcal{N}(c+aX_{t-1},\sigma^2).
$$

* AR(1) con innovazioni Student-t $$
X_t-(c+aX_{t-1})\sim t_\nu(0,s).
$$

* GARCH $$
X_t\mid\mathcal{F}_{t-1}\sim
\mathcal{N}(0,\sigma_t^2),
$$ con $$
\sigma_t^2=\alpha_0+\alpha_1X_{t-1}^2+\beta_1\sigma_{t-1}^2.
$$

* Conteggi Poisson condizionati $$
X_t\mid\mathcal{F}_{t-1}\sim\mathrm{Poisson}(\lambda_t).
$$

## 13.4 Messaggio finale

La stima dei parametri non inizia dall'ottimizzazione numerica. Inizia dalla scelta di una struttura probabilistica coerente con i dati.

Per una serie temporale dobbiamo decidere:

* che cosa è prevedibile dal passato;
* che cosa resta come innovazione;
* quale distribuzione ha l'innovazione;
* se la varianza è costante o variabile;
* se la dinamica è simmetrica o asimmetrica;
* se esistono soglie, regimi o vincoli discreti.

Solo dopo queste scelte ha senso scrivere una likelihood e stimare i parametri.

---

# Sintesi operativa

Una serie stocastica è una traiettoria osservata nel tempo. La sua analisi richiede di modellare sia la dipendenza temporale sia la distribuzione degli shock.

I modelli AR, MA e ARMA descrivono memoria lineare nei valori e negli shock. I modelli con innovazioni non gaussiane descrivono outlier, code pesanti e asimmetrie. I modelli ARCH/GARCH descrivono volatilità variabile nel tempo. I modelli a soglia e a regimi rappresentano dinamiche che cambiano in diverse regioni o fasi. I modelli per conteggi rispettano la natura discreta e non negativa di molte serie empiriche.

La diagnostica preliminare -- grafico della serie, incrementi, autocorrelazione, residui, code, volatilità e asimmetrie -- guida la scelta della classe di modelli.

La lezione successiva userà queste classi per costruire likelihood, stimatori di massima verosimiglianza e diagnostiche modello-dati.
