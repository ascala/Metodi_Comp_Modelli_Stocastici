---
title: "12: Sampling tramite dinamiche -- da Boltzmann a Langevin e dinamica molecolare"
author: "Antonio Scala"
date: ""
---
 
Dopo aver introdotto i processi stocastici fondamentali, le equazioni di Langevin, la master equation e la Fokker--Planck, e dopo aver discusso come stimare parametri da dati tramite likelihood e massima verosimiglianza, emerge una nuova domanda naturale:

> una volta assegnata una distribuzione target, oppure una funzione di energia che la definisce implicitamente, come si possono generare campioni, esplorare configurazioni tipiche e calcolare osservabili?

Questa dispensa affronta tale domanda mostrando che esiste un'idea unificante dietro oggetti che spesso vengono presentati in contesti diversi: la distribuzione di Boltzmann della fisica statistica, la dinamica molecolare, le equazioni di Langevin, il campionamento Monte Carlo in spazio continuo, e le Boltzmann machine nel machine learning.

Il punto concettuale centrale è il seguente. In molti problemi non vogliamo soltanto seguire una dinamica fisica reale; vogliamo anche costruire una dinamica artificiale che abbia come distribuzione stazionaria la misura che ci interessa campionare. In questo senso, una dinamica può essere usata non solo per descrivere il tempo, ma come strumento computazionale per esplorare uno spazio degli stati.

La dispensa è organizzata in modo da mettere in evidenza questa struttura comune. Partiremo dalla distribuzione di Boltzmann come ponte tra energia e probabilità. Passeremo poi al caso continuo, in cui la dinamica molecolare e la dinamica di Langevin forniscono meccanismi naturali di esplorazione di paesaggi energetici. Infine considereremo il caso discreto, in cui la stessa logica riappare nelle Boltzmann machine e nei metodi di campionamento come Metropolis e Gibbs sampling.

# Obiettivi didattici specifici

Al termine della dispensa lo studente dovrebbe essere in grado di:

1. comprendere perché una funzione di energia definisca naturalmente una distribuzione di probabilità di tipo Boltzmann;
2. distinguere tra dinamica fisica reale e dinamica artificiale usata per il campionamento;
3. interpretare la dinamica di Langevin come meccanismo di termalizzazione e come algoritmo di sampling;
4. collegare la Fokker--Planck alla misura stazionaria di Boltzmann;
5. scrivere e interpretare lo schema di Euler--Maruyama e l'Unadjusted Langevin Algorithm;
6. comprendere il ruolo della correzione Metropolis nel MALA;
7. leggere la dinamica molecolare come esplorazione di un paesaggio energetico a molti gradi di libertà;
8. capire come la distribuzione di Boltzmann riappaia in spazio discreto nelle Boltzmann machine;
9. interpretare il sampling come il ponte tra fisica statistica, inferenza e machine learning.

# Struttura della dispensa

1. Energia e distribuzioni target
2. La distribuzione di Boltzmann come ponte tra fisica e probabilità
3. Dinamica molecolare: traiettorie in un paesaggio energetico
4. Termalizzazione e dinamica di Langevin
5. Langevin Monte Carlo: campionamento in spazio continuo
6. Correzione Metropolis e varianti stocastiche
7. Boltzmann machine e sampling in spazio discreto
8. Confronto strutturale tra caso continuo e discreto
9. Applicazioni e sviluppi
10. Messaggio finale

# 1. Energia e distribuzioni target

In molti problemi scientifici e computazionali l'oggetto finale non è una singola traiettoria, ma una distribuzione di probabilità su uno spazio degli stati. Gli stati possono essere configurazioni atomiche, vettori continui di parametri, configurazioni binarie di una rete neurale, oppure configurazioni di un sistema statistico.

Molto spesso questa distribuzione non è data direttamente in forma normalizzata, ma attraverso una funzione di energia o di potenziale. Si scrive allora

$$
\pi(x) \propto e^{-\beta U(x)},
$$

dove:

* $x$ è lo stato del sistema;
* $U(x)$ è una funzione di energia, costo o potenziale;
* $\beta$ è un parametro inverso di temperatura;
* il simbolo $\propto$ indica che manca la costante di normalizzazione.

Questa forma compare in fisica statistica, dove $U$ è un'energia reale, ma anche in statistica bayesiana, in machine learning e in ottimizzazione stocastica, dove $U$ può essere interpretata come funzione obiettivo o energia efficace.

## 1.1 Perché il problema del campionamento è difficile

Anche quando la forma non normalizzata di $\pi(x)$ è nota, campionare direttamente da essa può essere molto difficile. Le cause principali sono:

* alta dimensionalità dello spazio degli stati;
* presenza di molti minimi locali della funzione $U$;
* costante di normalizzazione ignota;
* forte anisotropia o correlazione tra le variabili.

In questi casi diventa naturale costruire una dinamica la cui distribuzione stazionaria sia proprio $\pi(x)$, e usare tale dinamica come strumento di campionamento.

# 2. La distribuzione di Boltzmann

La distribuzione di Boltzmann è la forma canonica che collega energia e probabilità. Per uno stato $x$ si scrive

$$
P(x)=\frac{1}{Z}e^{-\beta U(x)},
$$

dove

$$
Z = \int e^{-\beta U(x)}\,dx
$$

nel caso continuo, oppure

$$
Z = \sum_x e^{-\beta U(x)}
$$

nel caso discreto.

La quantità $Z$ è la funzione di partizione e serve a normalizzare la distribuzione.

## 2.1 Interpretazione

Il significato è immediato:

* stati a bassa energia hanno probabilità maggiore;
* stati ad alta energia sono soppressi esponenzialmente;
* la temperatura controlla il compromesso tra esplorazione e concentrazione.

Se $T$ è alta, oppure $\beta$ è piccolo, anche stati energeticamente sfavoriti vengono visitati con probabilità significativa. Se invece $T$ è bassa, la distribuzione si concentra vicino ai minimi di $U$.

## 2.2 Un ponte concettuale importante

Questa distribuzione non è soltanto un oggetto della fisica statistica. È un modello probabilistico generale per sistemi complessi con molte variabili interagenti. In questa dispensa essa fungerà da linguaggio comune per:

* la dinamica molecolare termalizzata;
* la dinamica di Langevin;
* il campionamento Monte Carlo in spazio continuo;
* le Boltzmann machine in spazio discreto.

# 3. Dinamica molecolare: traiettorie in un paesaggio energetico

La dinamica molecolare nasce come studio dell'evoluzione di un sistema di molte particelle soggette a forze conservative. Se le posizioni delle particelle sono indicate con $\mathbf{r}_1,\dots,\mathbf{r}_N$, e il potenziale totale è $U(\mathbf{r}_1,\dots,\mathbf{r}_N)$, le equazioni del moto sono

$$
m_i \frac{d^2 \mathbf{r}_i}{dt^2} = -\nabla_i U.
$$

Si tratta di una dinamica deterministica che conserva l'energia totale in assenza di dissipazione e rumore.

## 3.1 Perché la dinamica molecolare è rilevante qui

A prima vista la dinamica molecolare sembra diversa dai metodi di campionamento. In realtà introduce già tre ingredienti essenziali:

1. uno spazio degli stati ad alta dimensionalità;
2. una funzione di energia che governa la dinamica;
3. un problema di esplorazione di un paesaggio energetico complesso.

La differenza è che la dinamica molecolare pura evolve traiettorie meccaniche e, di per sé, non è il metodo più naturale per campionare la distribuzione canonica di Boltzmann. Per ottenere quest'ultima serve introdurre un contatto efficace con un bagno termico.

## 3.2 Termalizzazione

Per simulare un sistema a temperatura fissata si aggiungono meccanismi di termalizzazione, cioè dissipazione e rumore, oppure algoritmi di thermostatting. In questo modo la dinamica non conserva più semplicemente l'energia meccanica, ma diventa compatibile con una distribuzione di equilibrio canonica.

Questo passaggio conduce naturalmente alla dinamica di Langevin.

# 4. Dinamica di Langevin

La dinamica di Langevin aggiunge all'evoluzione deterministica due contributi fondamentali:

* un termine dissipativo;
* un termine di rumore termico.

Per una particella di massa $m$, posizione $x$ e velocità $v$, la forma standard è

$$
m\frac{dv}{dt} = -\gamma v - \nabla U(x) + \sqrt{2\gamma k_B T}\,\eta(t),
$$

dove $\eta(t)$ è un rumore bianco gaussiano.

## 4.1 Significato fisico

Il termine $-\gamma v$ rappresenta l'attrito con l'ambiente; il termine casuale rappresenta gli urti termici microscopici. La combinazione dei due produce una dinamica che, sotto ipotesi appropriate, converge a equilibrio termico.

## 4.2 Limite sovra-smorzato

Quando l'inerzia è trascurabile rispetto all'attrito, si ottiene una dinamica sovra-smorzata per la sola posizione:

$$
dX_t = -\nabla U(X_t)\,dt + \sqrt{\frac{2}{\beta}}\,dW_t.
$$

Questa equazione è cruciale perché è al tempo stesso:

* un modello fisico di particella termalizzata;
* una SDE con misura stazionaria di Boltzmann;
* la base di algoritmi di sampling in spazio continuo.

## 4.3 Collegamento con Fokker--Planck

La Fokker--Planck associata è

$$
\partial_t p = \nabla\cdot\bigl(p\,\nabla U\bigr) + \frac{1}{\beta}\Delta p.
$$

La struttura mostra chiaramente l'interazione tra drift e diffusione:

* il drift spinge verso regioni a energia più bassa;
* la diffusione termica sparge la massa probabilistica.

La distribuzione stazionaria è proprio

$$
p^*(x) \propto e^{-\beta U(x)}.
$$

Questo è il punto centrale: la dinamica di Langevin può essere usata per campionare la misura di Boltzmann senza conoscere esplicitamente la costante di normalizzazione.

# 5. Langevin Monte Carlo

Se l'obiettivo non è simulare una particella reale, ma generare campioni da una distribuzione target

$$
\pi(x) \propto e^{-U(x)}\;,
$$

allora la SDE di Langevin può essere reinterpretata come algoritmo di campionamento.

Nel caso più semplice si considera

$$
dX_t = -\nabla U(X_t)\,dt + \sqrt{2}\,dW_t\;,
$$

la cui distribuzione stazionaria è proporzionale a $e^{-U(x)}$.

## 5.1 Discretizzazione: ULA

Applicando Euler--Maruyama con passo $h$ si ottiene

$$
X_{k+1} = X_k - h\nabla U(X_k) + \sqrt{2h}\,\xi_k,
$$

dove $\xi_k \sim \mathcal{N}(0,I)$.

Questo schema è noto come Unadjusted Langevin Algorithm (ULA).

Il suo significato è molto intuitivo:

* il gradiente $-\nabla U$ spinge verso regioni di energia più bassa;
* il rumore gaussiano evita che la dinamica collassi semplicemente in un minimo locale;
* il risultato è una esplorazione stocastica del paesaggio energetico.

## 5.2 Il problema del bias di discretizzazione

Poiché ULA nasce da una discretizzazione a passo finito, la sua distribuzione invariante non coincide in generale esattamente con la target desiderata. Il bias si riduce per passi piccoli, ma non scompare del tutto a passo fissato.

Questo conduce alla variante corretta tramite Metropolis.

# 6. MALA e gradienti stocastici

## 6.1 MALA

Nel Metropolis-Adjusted Langevin Algorithm (MALA) si usa il passo di Langevin come proposta in un algoritmo di Metropolis--Hastings. La proposta è gaussiana centrata in

$$
x - h\nabla U(x),
$$

con covarianza proporzionale a $2hI$. Un opportuno passo di accettazione corregge il bias dovuto alla discretizzazione e rende la catena esattamente invariante rispetto alla target.

## 6.2 Significato concettuale

MALA è un ottimo esempio del dialogo tra due idee già introdotte nel corso:

* usare una dinamica continua per costruire una proposta intelligente;
* usare un meccanismo di accettazione/rifiuto per correggere l'errore numerico.

## 6.3 SGLD

Quando l'energia $U$ è una somma su un dataset grande,

$$
U(x)=\sum_{i=1}^N U_i(x),
$$

calcolare il gradiente completo può essere troppo costoso. Si usa allora una stima rumorosa del gradiente, ottenendo la Stochastic Gradient Langevin Dynamics (SGLD). Qui il rumore deriva sia dalla dinamica di Langevin sia dall'approssimazione del gradiente tramite minibatch.

Questo porta il quadro di Langevin direttamente nell'apprendimento statistico su larga scala.

# 7. Boltzmann machine

Passiamo ora al caso discreto. Una Boltzmann machine è una rete di variabili binarie $s_i \in {0,1}$ o ${-1,+1}$, dotata di una funzione di energia del tipo

$$
E(s) = -\frac12 \sum_{i,j} w_{ij} s_i s_j - \sum_i b_i s_i.
$$

La distribuzione associata è

$$
P(s)=\frac{1}{Z}e^{-E(s)/T}.
$$

## 7.1 Che cosa rappresenta

In questo contesto:

* i pesi $w_{ij}$ codificano le interazioni tra unità;
* i bias $b_i$ rappresentano termini locali;
* l'energia misura quanto una configurazione sia compatibile con la struttura appresa.

Il principio è lo stesso della fisica statistica: configurazioni a energia bassa sono più probabili.

## 7.2 Perché il sampling è essenziale

La funzione di partizione

$$
Z = \sum_s e^{-E(s)/T}
$$

è in generale inaccessibile, perché richiede una somma su un numero esponenziale di configurazioni. Per questo il campionamento è parte integrante sia dell'uso sia dell'apprendimento delle Boltzmann machine.

## 7.3 Gibbs e Metropolis

Le configurazioni vengono esplorate mediante aggiornamenti stocastici locali. Due approcci fondamentali sono:

* **Metropolis**, che propone una modifica locale e la accetta con probabilità dipendente da $\Delta E$;
* **Gibbs sampling**, che aggiorna una variabile alla volta usando la sua probabilità condizionata.

Nel caso delle Boltzmann machine, Gibbs sampling è particolarmente naturale perché l'aggiornamento di una singola unità ha una forma logistica esplicita.

# 8. Caso continuo e caso discreto: stessa struttura

A questo punto la parentela tra i vari oggetti dovrebbe essere visibile.

## 8.1 Caso continuo

* stato: $x \in \mathbb{R}^d$;
* energia: $U(x)$;
* distribuzione target: $\pi(x) \propto e^{-U(x)}$;
* dinamica di sampling: Langevin, ULA, MALA.

## 8.2 Caso discreto

* stato: configurazione binaria $s$;
* energia: $E(s)$;
* distribuzione target: $P(s) \propto e^{-E(s)/T}$;
* dinamica di sampling: Gibbs, Metropolis.

## 8.3 Idea unificante

In entrambi i casi:

1. una energia definisce una distribuzione target;
2. il campionamento diretto è difficile;
3. si costruisce una dinamica stocastica che esplora lo spazio degli stati;
4. la distribuzione stazionaria di tale dinamica coincide con la distribuzione desiderata.

Questo è il messaggio concettuale più importante dell'intera dispensa.

# 9. Relazione con la stima dei parametri

Il collegamento con la lezione precedente sulla stima dei parametri è diretto.

Se un modello probabilistico dipende da parametri $\theta$, la likelihood richiede spesso di valutare o approssimare quantità rispetto a una distribuzione target. In modelli energetici, modelli latenti, distribuzioni bayesiane ad alta dimensione e modelli di fisica statistica, tale distribuzione è spesso campionabile solo tramite algoritmi dinamici.

In altre parole:

* la stima dei parametri risponde alla domanda "quale modello spiega i dati?";
* il sampling tramite dinamiche risponde alla domanda "dato il modello, come ne esploro la distribuzione?".

Le due componenti formano quindi una coppia naturale.

# 10. Applicazioni e sviluppi

## 10.1 Fisica computazionale

* simulazione di sistemi termalizzati;
* campionamento di misure canoniche;
* studio di paesaggi energetici e metastabilità.

## 10.2 Statistica computazionale e Bayesian inference

* campionamento da posteriori complesse;
* metodi di Langevin e Hamiltonian Monte Carlo;
* valutazione di medie e intervalli credibili.

## 10.3 Machine learning

* Boltzmann machine e Restricted Boltzmann Machine;
* energy-based models;
* apprendimento con gradienti stocastici rumorosi.

## 10.4 Sistemi a molti agenti

La lettura in termini di paesaggio energetico e distribuzione stazionaria può essere estesa anche a modelli collettivi, sociali o biologici, quando la dinamica può essere reinterpretata come esplorazione di configurazioni favorite o sfavorite.

# 11. Che cosa non va confuso

Per chiudere, è utile distinguere chiaramente tre livelli che spesso vengono mescolati.

## 11.1 Dinamica fisica reale

Nel caso della dinamica molecolare, l'obiettivo principale può essere descrivere l'evoluzione temporale di un sistema reale.

## 11.2 Dinamica termalizzata

Nel caso della dinamica di Langevin, si descrive ancora una dinamica fisica, ma con accoppiamento a un bagno termico.

## 11.3 Dinamica artificiale di campionamento

Nel caso di ULA, MALA, Gibbs o Metropolis, la dinamica è spesso soprattutto uno strumento computazionale. Non la si introduce perché il sistema "segua davvero" quella legge nel tempo, ma perché essa ha la distribuzione stazionaria desiderata.

Questa distinzione è fondamentale per evitare confusioni tra modellizzazione fisica e algoritmi di inferenza.

# 12. Messaggio finale

La dinamica molecolare, la dinamica di Langevin, il Langevin Monte Carlo e le Boltzmann machine appartengono a contesti diversi, ma condividono una stessa architettura concettuale.

In tutti i casi si parte da uno spazio degli stati e da una energia o funzione potenziale che induce una distribuzione target. Quando il campionamento diretto è impraticabile, si costruisce una dinamica che esplora tale spazio e che, a lungo tempo, visita gli stati con la frequenza corretta.

Il sampling tramite dinamiche è quindi il punto di incontro tra:

* fisica statistica,
* processi stocastici,
* metodi Monte Carlo,
* inferenza statistica,
* machine learning.

Questa è la ragione per cui tali tecniche meritano di essere studiate insieme, come capitolo unitario e non come argomenti isolati.

# Possibili sviluppi successivi

I temi naturali che possono seguire questa dispensa sono:

1. Hamiltonian Monte Carlo e dinamiche conservative per il sampling;
2. simulated annealing e paesaggi complessi;
3. modelli generativi basati su SDE e diffusion models;
4. metastabilità, tempi di escape e transizioni rare.
