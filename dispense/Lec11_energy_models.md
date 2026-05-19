---
title: "11 Paesaggi di energia e modelli generativi"
author: "Antonio Scala"
date: ""
---

# Obiettivi della lezione

In molti problemi computazionali una funzione di costo, energia o loss viene usata per valutare le configurazioni: alcune sono più stabili, più compatibili con i dati, più plausibili o più desiderabili di altre. Il passo che compiamo in questa lezione è trasformare questa funzione da semplice criterio di valutazione in uno strumento per definire una distribuzione di probabilità.

L'idea di base è semplice. Se a ogni configurazione $x$ associamo una quantità $E(x)$, possiamo assegnare probabilità maggiori agli stati con energia più bassa e probabilità minori agli stati con energia più alta. In questo modo il paesaggio non serve soltanto a cercare una configurazione ottima, ma diventa un modello probabilistico dell'intero spazio delle configurazioni.

Questa prospettiva è alla base degli **energy-based models**. Invece di specificare direttamente una procedura generativa esplicita, si definisce una funzione energia e si interpreta la distribuzione risultante come modello dei dati. Generare nuovi campioni significa allora esplorare il paesaggio in modo coerente con quella distribuzione.

La lezione introduce questo punto di vista attraverso alcuni esempi fondamentali: reti di Hopfield, Boltzmann Machines, Gibbs sampling, contrastive divergence e Hamiltonian Monte Carlo. Il filo conduttore è il passaggio:

$$
\text{funzione di costo} \quad \longrightarrow \quad \text{energia} \quad \longrightarrow \quad \text{distribuzione} \quad \longrightarrow \quad \text{modello generativo}.
$$

Al termine della lezione lo studente dovrebbe essere in grado di:

1. spiegare come una funzione energia possa definire una distribuzione di probabilità;

2. interpretare il ruolo della distribuzione di Boltzmann e della funzione di partizione;

3. distinguere fra minimizzare un'energia e campionare da una distribuzione associata all'energia;

4. descrivere il principio generale degli energy-based models;

5. interpretare una rete di Hopfield come modello di memoria basato su minimi di energia;

6. comprendere come una Boltzmann Machine estenda questa idea in senso probabilistico e generativo;

7. spiegare il ruolo del Gibbs sampling nel campionamento da modelli con molte variabili;

8. riconoscere perché la funzione di partizione rende difficile l'apprendimento;

9. descrivere l'idea della contrastive divergence come approssimazione pratica dell'apprendimento;

10. comprendere il principio dell'Hamiltonian Monte Carlo come metodo di campionamento in spazi continui ad alta dimensione;

11. collegare ottimizzazione, campionamento e generazione come tre letture diverse dello stesso paesaggio.

# Struttura

1. Paesaggi: da costo a probabilità

2. Distribuzione di Boltzmann e funzione di partizione

3. Energy-based models

4. Hopfield networks

5. Boltzmann Machines

6. Gibbs sampling

7. Apprendimento e problema di $Z$

8. Contrastive divergence

9. Hamiltonian Monte Carlo per spazi continui

10. Sintesi: ottimizzare, campionare, generare

# Introduzione

## Da una funzione obiettivo a un modello probabilistico

Una funzione di costo, energia o loss può essere usata in due modi diversi.

Il primo è cercare una configurazione particolarmente buona: una soluzione che minimizza il costo, massimizza una plausibilità o riduce una distanza dai dati. Questa lettura porta naturalmente a un problema di ottimizzazione.

Il secondo è più ambizioso. La stessa funzione può essere usata per assegnare probabilità a tutte le configurazioni possibili. In questo caso non interessa soltanto individuare una soluzione buona, ma costruire una distribuzione che dica quali configurazioni sono plausibili e con quale peso relativo.

La forma tipica è

$$
p(x) = \frac{e^{-\beta E(x)}}{Z}.
$$

Qui $E(x)$ assegna un'energia alla configurazione $x$, $\beta$ controlla quanto la distribuzione penalizza le configurazioni ad alta energia, e $Z$ è la costante di normalizzazione. Gli stati a bassa energia diventano più probabili; quelli ad alta energia diventano meno probabili.

Questo passaggio è il punto di partenza degli energy-based models. Il modello non specifica direttamente una ricetta esplicita per produrre dati. Specifica invece una funzione energia. Generare significa poi campionare configurazioni dalla distribuzione definita da quella energia.

## Perché non basta il minimo

In molti problemi una singola configurazione ottima non è una descrizione sufficiente. I dati possono essere compatibili con più spiegazioni. Un sistema può avere molte configurazioni plausibili. Un modello generativo deve produrre esempi diversi, non ripetere sempre la configurazione più probabile.

Questo è particolarmente importante quando vogliamo rappresentare variabilità. Un modello di immagini deve generare molte immagini plausibili. Un modello di reti deve generare molte reti compatibili con certe proprietà osservate. Un modello di scelte o comportamenti deve rappresentare una distribuzione di possibilità, non soltanto una scelta dominante.

La domanda quindi cambia:

> non solo quale configurazione è migliore?, ma quale distribuzione rende plausibili le configurazioni osservate?

## Il problema computazionale

Definire una distribuzione tramite un'energia è concettualmente semplice, ma computazionalmente difficile. La normalizzazione richiede di sommare o integrare il peso di tutte le configurazioni possibili:

$$
Z = \sum_x e^{-\beta E(x)}
$$

nel caso discreto, oppure

$$
Z = \int e^{-\beta E(x)},dx
$$

nel caso continuo.

In spazi grandi o ad alta dimensione, $Z$ è spesso intrattabile. Questo crea due problemi centrali:

1. campionare dalla distribuzione definita dall'energia;

2. apprendere i parametri dell'energia a partire dai dati.

Questa lezione è costruita attorno a questi due problemi. Le reti di Hopfield mostrano come un'energia possa rappresentare memoria. Le Boltzmann Machines trasformano questa idea in un modello probabilistico. Gibbs sampling fornisce un meccanismo locale di campionamento. La contrastive divergence offre un'approssimazione pratica per l'apprendimento. Hamiltonian Monte Carlo affronta il campionamento in spazi continui usando una dinamica ausiliaria.

Il filo conduttore non è più la ricerca di un minimo, ma la costruzione e l'uso di una distribuzione generativa definita da una funzione energia.

# 1. Paesaggi: da costo a probabilità

## 1.1 Una funzione energia come valutazione delle configurazioni

Sia $\mathcal{X}$ uno spazio di configurazioni. A seconda del problema, una configurazione $x\in\mathcal{X}$ può essere un vettore di variabili continue, una configurazione binaria, una sequenza, una partizione, una rete, un insieme di parametri o uno stato collettivo.

Introduciamo una funzione

$$
E:\mathcal{X}\to\mathbb{R}
$$

che assegna un valore numerico a ogni configurazione. Useremo il termine **energia** in senso ampio. Un valore basso di $E(x)$ indica che la configurazione è più compatibile con il modello, con i dati o con i vincoli del problema. Un valore alto indica invece una configurazione meno compatibile o meno plausibile.

In questa lettura, $E(x)$ non è ancora una probabilità. È una funzione di valutazione. Il passo successivo consiste nel trasformare questa valutazione in un peso probabilistico.

## 1.2 Pesi non normalizzati

A ogni configurazione associamo il peso

$$
\widetilde p(x)=e^{-\beta E(x)}.
$$

La tilde ricorda che $\widetilde p(x)$ non è ancora una probabilità normalizzata. È soltanto un peso positivo.

Questa scelta ha due proprietà importanti.

Primo, il peso è sempre positivo:

$$
\widetilde p(x)>0.
$$

Secondo, le configurazioni a energia più bassa ricevono peso maggiore. Se $E(x)<E(y)$, allora

$$
\widetilde p(x)>\widetilde p(y).
$$

Il passaggio dall'energia al peso è quindi monotono: diminuire l'energia aumenta la plausibilità relativa della configurazione.

## 1.3 Rapporti di probabilità

La quantità più semplice da interpretare non è il peso assoluto di una configurazione, ma il rapporto tra due pesi:

$$
\frac{\widetilde p(x)}{\widetilde p(y)}=exp[-\beta(E(x)-E(y))].
$$

Questo rapporto mostra che contano le differenze di energia, non il valore assoluto dell'energia. Se aggiungiamo una costante $c$ a tutte le energie,

$$
E'(x)=E(x)+c,
$$

i rapporti di probabilità non cambiano. Tutti i pesi vengono moltiplicati per lo stesso fattore $e^{-\beta c}$, che scompare nella normalizzazione.

Questo è un punto concettuale utile: l'energia definisce una scala relativa di plausibilità. La probabilità assoluta richiede invece una normalizzazione globale.

## 1.4 Normalizzazione

Per ottenere una distribuzione di probabilità dobbiamo dividere i pesi per la loro somma complessiva. Nel caso discreto definiamo

$$
Z=\sum_{x\in\mathcal{X}} e^{-\beta E(x)}.
$$

Allora

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

Nel caso continuo la somma è sostituita da un integrale:

$$
Z=\int_{\mathcal{X}} e^{-\beta E(x)},dx,
$$

con

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

La costante $Z$ prende spesso il nome di **funzione di partizione**. In questa sezione la trattiamo soltanto come fattore di normalizzazione. Il suo significato computazionale e statistico diventerà centrale nella sezione successiva.

## 1.5 Il ruolo di $\beta$

Il parametro $\beta$ controlla quanto la distribuzione è sensibile alle differenze di energia.

Se $\beta=0$, tutti i pesi sono uguali:

$$
e^{-\beta E(x)}=1.
$$

Nel caso discreto finito si ottiene una distribuzione uniforme. L'energia non influenza la probabilità.

Se $\beta$ è piccolo, le differenze di energia hanno un effetto debole. Configurazioni con energia diversa possono avere probabilità comparabili.

Se $\beta$ è grande, anche piccole differenze di energia producono grandi differenze di probabilità. La distribuzione diventa più selettiva e si concentra sulle configurazioni a energia più bassa.

Spesso si introduce una temperatura $T$ inversamente proporzionale a $\beta$:

$$
\beta = \frac{1}{T}.
$$

Temperatura alta significa distribuzione più diffusa; temperatura bassa significa distribuzione più concentrata.

## 1.6 Sintesi della sezione

Una funzione energia permette di passare da una valutazione delle configurazioni a una distribuzione di probabilità. Il passaggio avviene in tre mosse:

1. assegnare un'energia $E(x)$;

2. trasformarla in un peso positivo $e^{-\beta E(x)}$;

3. normalizzare i pesi tramite $Z$.

La formula finale è

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

Questa è la forma di base su cui si costruiscono gli energy-based models. La difficoltà principale non è scrivere la formula, ma calcolare, campionare e apprendere distribuzioni di questo tipo quando lo spazio delle configurazioni è grande.

# 2. Distribuzione di Boltzmann e funzione di partizione

## 2.1 La distribuzione di Boltzmann

Data una funzione energia $E(x)$, una distribuzione di probabilità naturale è

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

Questa forma è spesso chiamata **distribuzione di Boltzmann** o **distribuzione di Boltzmann--Gibbs**. Nel linguaggio fisico nasce come distribuzione di equilibrio di un sistema a temperatura fissata. In questa lezione la useremo in un senso più generale: è un modo per trasformare una funzione energia in una distribuzione su configurazioni.

Il significato intuitivo è diretto. Le configurazioni a bassa energia sono favorite, ma non necessariamente selezionate in modo esclusivo. Le configurazioni ad energia più alta non sono impossibili: ricevono semplicemente un peso esponenzialmente più piccolo. Il parametro $\beta$ regola quanto forte sia questa penalizzazione.

Questa forma è utile perché separa due elementi:

1. una parte **locale**, l'energia $E(x)$, che può essere valutata su una singola configurazione;
2. una parte **globale**, la normalizzazione $Z$, che dipende da tutte le configurazioni possibili.

Questa distinzione è il punto centrale della sezione.

## 2.2 La funzione di partizione

Nel caso discreto, la costante di normalizzazione è

$$
Z=\sum_{x\in\mathcal{X}} e^{-\beta E(x)}.
$$

Nel caso continuo, diventa

$$
Z=\int_{\mathcal{X}} e^{-\beta E(x)},dx.
$$

Questa quantità è chiamata **funzione di partizione**. Il nome viene dalla meccanica statistica, ma qui possiamo interpretarla in modo operativo: $Z$ è il peso totale di tutte le configurazioni possibili.

La normalizzazione serve a garantire che

$$
\sum_{x\in\mathcal{X}} p(x)=1
$$

nel caso discreto, oppure

$$
\int_{\mathcal{X}} p(x),dx=1
$$

nel caso continuo.

Senza $Z$, $e^{-\beta E(x)}$ fornisce soltanto un peso relativo. Con $Z$, questi pesi diventano probabilità.

## 2.3 Perché $Z$ è globale

La funzione energia può spesso essere calcolata facilmente per una singola configurazione. Se $x$ è dato, valutare $E(x)$ può essere relativamente semplice: basta applicare la funzione di costo, la loss, lo score o il modello.

La funzione di partizione richiede invece qualcosa di molto diverso: bisogna sommare o integrare il contributo di tutte le configurazioni.

Questo significa che $Z$ non è una proprietà di un singolo stato. È una proprietà dell'intero spazio delle configurazioni.

Questa differenza è fondamentale:

$$
E(x) \quad \text{è locale rispetto alla configurazione } x,
$$

mentre

$$
Z \quad \text{è globale rispetto allo spazio } \mathcal{X}.
$$

Nei problemi piccoli questa distinzione può sembrare innocua. Nei problemi realistici diventa invece decisiva. Se $\mathcal{X}$ contiene un numero enorme di configurazioni, calcolare $Z$ per somma diretta è impossibile. Se $\mathcal{X}$ è continuo e ad alta dimensione, calcolare l'integrale può essere altrettanto difficile.

## 2.4 Probabilità normalizzate e probabilità non normalizzate

Molti algoritmi non hanno bisogno di conoscere direttamente $Z$ per confrontare due configurazioni. Infatti, per due stati $x$ e $y$,

$$
\frac{p(x)}{p(y)}
= \frac{e^{-\beta E(x)}/Z}{e^{-\beta E(y)}/Z}
= e^{-\beta(E(x)-E(y))}.
$$

La costante $Z$ si cancella. Per questo motivo è spesso possibile costruire algoritmi di campionamento che usano soltanto la distribuzione non normalizzata

$$
\widetilde p(x)=e^{-\beta E(x)}.
$$

Questo è un punto pratico molto importante. Anche se non conosciamo $Z$, possiamo spesso confrontare configurazioni e costruire transizioni che dipendono solo da differenze di energia.

Tuttavia, l'assenza di $Z$ non è sempre innocua. Se vogliamo calcolare la probabilità assoluta di un dato, confrontare modelli diversi, stimare una likelihood normalizzata o apprendere parametri mediante massima verosimiglianza, $Z$ rientra nel problema in modo essenziale.

## 2.5 La log-probabilità

Prendendo il logaritmo della distribuzione di Boltzmann si ottiene

$$
\log p(x) = -\beta E(x) - \log Z.
$$

Questa formula è particolarmente utile perché separa due contributi:

1. il termine $-\beta E(x)$, che dipende dalla configurazione osservata;
2. il termine $-\log Z$, che non dipende da $x$ ma dipende dalla funzione energia nel suo complesso.

Questa separazione è semplice ma profonda. Per una singola configurazione, diminuire l'energia aumenta la log-probabilità. Ma perché $p(x)$ sia una distribuzione normalizzata, bisogna anche tenere conto di quanto peso il modello assegna a tutte le altre configurazioni.

In altri termini, un modello non può rendere tutto molto probabile. Se abbassa l'energia di molte configurazioni, aumenta anche $Z$. La normalizzazione impone una competizione globale tra stati.

## 2.6 Parametri e dipendenza di $Z$

Negli energy-based models la funzione energia dipende da parametri:

$$
E_\theta(x).
$$

La distribuzione diventa

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},
$$

con

$$
Z_\theta=\sum_x e^{-E_\theta(x)}
$$

nel caso discreto, oppure

$$
Z_\theta=\int e^{-E_\theta(x)},dx
$$

nel caso continuo.

Qui, per semplicità, abbiamo assorbito $\beta$ nei parametri o nell'energia. Questa è una scelta frequente: invece di scrivere sempre $\beta E_\theta(x)$, si ridefinisce l'energia in modo che il fattore di scala sia incorporato in $\theta$.

Il punto importante è che $Z_\theta$ dipende dai parametri. Se cambiamo la funzione energia, cambiano i pesi di tutte le configurazioni, e quindi cambia anche la normalizzazione.

Questo rende l'apprendimento più difficile. Non basta abbassare l'energia dei dati osservati. Bisogna anche controllare come cambia il peso assegnato dal modello alle configurazioni non osservate.

## 2.7 Una tensione fondamentale

Quando osserviamo un dato $x^{(data)}$, vorremmo che il modello gli assegnasse alta probabilità. Questo significa rendere bassa la sua energia:

$$
E_\theta(x^{(data)}) \quad \text{piccola}.
$$

Ma la probabilità normalizzata è

$$
p_\theta(x^{(data)})=\frac{e^{-E_\theta(x^{(data)})}}{Z_\theta}.
$$

La probabilità aumenta se il numeratore cresce, ma diminuisce se cresce troppo anche $Z_\theta$. Dunque l'apprendimento deve bilanciare due effetti:

1. abbassare l'energia delle configurazioni osservate;
2. evitare di abbassare indiscriminatamente l'energia di troppe configurazioni non osservate.

Questa tensione è alla base dell'apprendimento negli energy-based models. In forma intuitiva:

> il modello deve rendere i dati più plausibili rispetto alle alternative, non semplicemente abbassare tutte le energie.

## 2.8 Sintesi della sezione

La distribuzione di Boltzmann trasforma una funzione energia in una distribuzione di probabilità:

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}.
$$

La funzione di partizione

$$
Z=\sum_x e^{-\beta E(x)}
$$

nel caso discreto, o

$$
Z=\int e^{-\beta E(x)},dx
$$

nel caso continuo, normalizza i pesi e rende la distribuzione ben definita.

Il problema è che $Z$ è una quantità globale: dipende da tutte le configurazioni possibili. Per questo motivo può essere intrattabile in spazi grandi o ad alta dimensione.

Questa osservazione prepara il passaggio agli energy-based models: modelli in cui è spesso facile valutare l'energia di una configurazione, ma difficile normalizzare, campionare e apprendere la distribuzione corrispondente.

# 3. Energy-based models

## 3.1 Definizione generale

Un **energy-based model** è un modello probabilistico che assegna probabilità alle configurazioni tramite una funzione energia parametrica.

Dato uno spazio di configurazioni $\mathcal{X}$, si introduce una funzione

$$
E_\theta(x),
$$

dove $\theta$ indica i parametri del modello. La distribuzione associata è

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},
$$

con

$$
Z_\theta=\sum_{x\in\mathcal{X}} e^{-E_\theta(x)}
$$

nel caso discreto, oppure

$$
Z_\theta=\int_{\mathcal{X}} e^{-E_\theta(x)},dx
$$

nel caso continuo.

Il modello è quindi definito da una funzione energia. Configurazioni a energia bassa ricevono probabilità alta; configurazioni a energia alta ricevono probabilità bassa.

La forma può sembrare semplice, ma è molto generale. Cambiando la forma di $E_\theta(x)$ si possono rappresentare distribuzioni molto diverse: distribuzioni su vettori continui, stati binari, immagini, sequenze, reti, variabili latenti o configurazioni collettive.

## 3.2 Perché definire una distribuzione tramite l'energia

In molti problemi è difficile specificare direttamente una distribuzione normalizzata $p_\theta(x)$. Può però essere più naturale costruire una funzione che valuta quanto una configurazione sia compatibile con certe regolarità.

Ad esempio:

* in un problema di immagini, una configurazione è plausibile se contiene strutture visive coerenti;
* in un problema di reti, una configurazione è plausibile se rispetta certe proprietà topologiche;
* in un problema biologico, una configurazione è plausibile se soddisfa vincoli funzionali o strutturali;
* in un problema sociale, una configurazione è plausibile se rispetta vincoli di interazione, compatibilità o coordinamento;
* in un problema di inferenza, una configurazione è plausibile se spiega bene i dati osservati.

In tutti questi casi l'energia agisce come una misura di incompatibilità. Più una configurazione viola le regolarità del modello, più alta sarà la sua energia.

Questa impostazione consente di separare due operazioni:

1. definire una funzione che valuta le configurazioni;
2. usare questa funzione per costruire una distribuzione generativa.

## 3.3 Modello esplicito e modello implicito

Un modello probabilistico può essere specificato in modi diversi.

In un modello esplicito, la probabilità $p_\theta(x)$ è data direttamente in forma normalizzata. Ad esempio, una gaussiana univariata è definita da una densità esplicita, e la normalizzazione è nota analiticamente.

In un energy-based model, invece, la distribuzione è specificata tramite una probabilità non normalizzata:

$$
\widetilde p_\theta(x)=e^{-E_\theta(x)}.
$$

La distribuzione normalizzata richiede

$$
p_\theta(x)=\frac{\widetilde p_\theta(x)}{Z_\theta}.
$$

Questo significa che l'energia definisce il modello in modo **implicito**. Possiamo valutare il peso relativo di una configurazione, ma per conoscere la probabilità assoluta dobbiamo conoscere $Z_\theta$.

Questa distinzione è importante. Gli energy-based models sono flessibili proprio perché non richiedono di costruire direttamente una distribuzione normalizzata semplice. Ma questa flessibilità produce difficoltà computazionali: normalizzare e campionare possono diventare problemi difficili.

## 3.4 Generare campioni

Un energy-based model diventa generativo se siamo in grado di produrre campioni dalla distribuzione $p_\theta(x)$.

Generare non significa trovare il minimo di $E_\theta(x)$. Significa produrre configurazioni distribuite secondo

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

Questa distinzione è essenziale. Se il modello ha appreso una distribuzione complessa, campioni diversi devono riflettere la variabilità della distribuzione. Un modello generativo non deve restituire sempre la configurazione più probabile, ma un insieme di configurazioni plausibili con la giusta frequenza relativa.

Per questo motivo, gli algoritmi di campionamento sono parte integrante degli energy-based models. Se sappiamo valutare $E_\theta(x)$ ma non sappiamo campionare da $p_\theta(x)$, il modello resta difficile da usare come generatore.

## 3.5 Apprendere l'energia dai dati

Supponiamo di osservare un dataset

$$
\mathcal{D}={x^{(1)},\dots,x^{(n)}}.
$$

L'obiettivo è scegliere i parametri $\theta$ in modo che i dati osservati abbiano alta probabilità sotto il modello. La log-likelihood è

$$
\ell(\theta)=\sum_{i=1}^n \log p_\theta(x^{(i)}).
$$

Usando la forma energetica,

$$
\log p_\theta(x^{(i)})=-E_\theta(x^{(i)})-\log Z_\theta.
$$

Quindi

$$
\ell(\theta)=-\sum_{i=1}^n E_\theta(x^{(i)})-n\log Z_\theta.
$$

Questa formula mostra chiaramente i due lati dell'apprendimento.

Il primo termine spinge ad abbassare l'energia dei dati osservati:

$$
-\sum_{i=1}^n E_\theta(x^{(i)}).
$$

Il secondo termine penalizza l'aumento del peso totale assegnato dal modello a tutte le configurazioni:

$$
-n\log Z_\theta.
$$

Senza il termine di normalizzazione, il problema sarebbe degenerato: basterebbe abbassare tutte le energie. Il termine $\log Z_\theta$ impedisce questa soluzione banale e costringe il modello a redistribuire la probabilità.

## 3.6 Interpretazione: dati contro modello

Il gradiente della log-likelihood ha una struttura molto importante. Senza entrare nei dettagli tecnici, esso confronta due medie:

1. una media calcolata sui dati;
2. una media calcolata sui campioni generati dal modello.

In forma schematica:

$$
\nabla_\theta \ell(\theta) =
-\sum_{i=1}^n \nabla_\theta E_\theta(x^{(i)})
+n\,\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(X)\right].
$$

Il primo termine dipende dalle configurazioni osservate. Il secondo dipende dalle configurazioni che il modello considera probabili.

Questa è una delle idee centrali degli energy-based models:

> apprendere significa rendere i dati più probabili rispetto alle configurazioni generate dal modello.

Se il modello assegna alta probabilità a configurazioni non osservate o non plausibili, il termine di modello corregge l'energia in modo da ridurne il peso. Se assegna energia troppo alta ai dati, il termine sui dati spinge nella direzione opposta.

## 3.7 Perché il gradiente è difficile

La difficoltà principale è il termine

$$
\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(X)\right].
$$

Questa media è rispetto alla distribuzione del modello. Per calcolarla esattamente bisognerebbe conoscere o campionare bene $p_\theta(x)$. Ma proprio questo è difficile quando $Z_\theta$ è intrattabile o quando lo spazio delle configurazioni è grande.

Quindi l'apprendimento richiede, direttamente o indirettamente, una procedura di campionamento.

Questo crea un ciclo caratteristico:

$$
\text{per apprendere serve campionare, ma per campionare bene serve un modello già ragionevole.}
$$

Molti algoritmi per energy-based models nascono per gestire questa tensione.

## 3.8 Esempi di funzioni energia

La forma specifica di $E_\theta(x)$ dipende dal problema. Alcuni esempi schematici sono:

### Modello quadratico continuo

Per una variabile continua $x\in\mathbb{R}^d$, un'energia quadratica può avere la forma

$$
E(x)=\frac{1}{2}(x-\mu)^T A (x-\mu).
$$

Se $A$ è definita positiva, questa energia produce una distribuzione gaussiana dopo normalizzazione.

### Modello binario con interazioni

Per variabili binarie $s_i\in\{-1,+1\}$, un'energia tipica è

$$
E(s)=-\sum_i h_i s_i - \frac{1}{2}\sum_{i,j}J_{ij}s_i s_j.
$$

I parametri $h_i$ descrivono tendenze individuali; i parametri $J_{ij}$ descrivono interazioni tra variabili. Questa struttura sarà alla base delle reti di Hopfield e delle Boltzmann Machines.

### Modello con variabili latenti

Se il modello contiene variabili osservate $v$ e variabili latenti $h$, l'energia può essere definita sullo stato congiunto:

$$
E_\theta(v,h).
$$

La probabilità delle variabili osservate si ottiene sommando o integrando sulle variabili latenti:

$$
p_\theta(v)=\sum_h p_\theta(v,h).
$$

Questo punto sarà importante per le Boltzmann Machines.

## 3.9 Sintesi della sezione

Un energy-based model definisce una distribuzione tramite una funzione energia parametrica:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

La forza del formalismo è la flessibilità: è spesso più semplice costruire una funzione che valuta configurazioni che scrivere direttamente una distribuzione normalizzata.

La difficoltà è computazionale: la normalizzazione $Z_\theta$, il campionamento da $p_\theta$ e il calcolo del gradiente della log-likelihood richiedono informazioni globali sulla distribuzione.

Le sezioni successive introducono due famiglie di modelli storicamente e concettualmente importanti: le reti di Hopfield, in cui l'energia organizza attrattori di memoria, e le Boltzmann Machines, in cui l'energia definisce una vera distribuzione generativa su variabili osservate e latenti.

# 4. Hopfield networks

## 4.1 Memoria associativa

Una **rete di Hopfield** è un modello semplice di memoria associativa. L'idea non è archiviare un'informazione in un indirizzo preciso, come avviene in una memoria digitale ordinaria, ma distribuire l'informazione nei pesi di interazione tra molte unità.

Una memoria associativa deve essere capace di completare o correggere un pattern parziale. Se il sistema riceve una configurazione iniziale rumorosa, incompleta o corrotta, la dinamica deve portarla verso una configurazione memorizzata.

Esempi intuitivi:

* riconoscere una parola anche se alcune lettere sono mancanti;
* riconoscere un'immagine anche se è parzialmente disturbata;
* ricostruire un pattern binario a partire da una versione corrotta;
* ritrovare uno stato collettivo coerente a partire da una configurazione iniziale disordinata.

Il punto importante è che la memoria non è localizzata in una singola variabile. È codificata nella struttura delle interazioni.

## 4.2 Stati binari

Consideriamo $N$ unità binarie

$$
s_i\in\{-1,+1\},
\qquad i=1,\dots,N.
$$

Una configurazione della rete è il vettore

$$
s=(s_1,\dots,s_N).
$$

Lo spazio degli stati contiene quindi $2^N$ configurazioni possibili. Anche per $N$ moderato, lo spazio cresce rapidamente.

Ogni unità interagisce con le altre tramite coefficienti $J_{ij}$. In genere si assume

$$
J_{ij}=J_{ji},
\qquad
J_{ii}=0.
$$

La simmetria dei pesi è importante perché consente di definire una funzione energia che diminuisce lungo la dinamica di aggiornamento. L'assenza di auto-interazione evita che una variabile influenzi direttamente sé stessa.

## 4.3 Energia della rete

La funzione energia della rete di Hopfield è

$$
E(s)=-\frac{1}{2}\sum_{i,j}J_{ij}s_i s_j - \sum_i h_i s_i.
$$

Il termine $J_{ij}s_i s_j$ misura il contributo dell'interazione tra le unità $i$ e $j$. Il fattore $1/2$ evita di contare due volte le coppie, dato che $J_{ij}=J_{ji}$.

Il termine $h_i$ è un campo esterno o bias locale. Se $h_i>0$, tende a favorire $s_i=+1$; se $h_i<0$, tende a favorire $s_i=-1$.

Nel caso più semplice si pone $h_i=0$, ottenendo

$$
E(s)=-\frac{1}{2}\sum_{i,j}J_{ij}s_i s_j.
$$

La rete evolve modificando gli stati $s_i$ in modo da ridurre, o almeno non aumentare, questa energia.

## 4.4 Campo locale

Per capire come aggiornare una singola unità, fissiamo tutte le altre variabili e guardiamo il contributo che agisce su $s_i$. Si definisce il **campo locale**

$$
H_i(s)=\sum_j J_{ij}s_j+h_i.
$$

Questo campo sintetizza l'effetto delle altre unità sull'unità $i$.

Se $H_i(s)>0$, l'energia è ridotta scegliendo

$$
s_i=+1.
$$

Se $H_i(s)<0$, l'energia è ridotta scegliendo

$$
s_i=-1.
$$

La regola di aggiornamento deterministica è quindi

$$
s_i \leftarrow \mathrm{sign}\,H_i(s).
$$

Se il campo locale è nullo, si può lasciare invariato lo stato oppure scegliere una convenzione specifica.

## 4.5 Aggiornamento asincrono

Nella versione classica, le unità vengono aggiornate una alla volta. A ogni passo si sceglie un indice $i$ e si aggiorna $s_i$ usando il campo locale calcolato nello stato corrente.

Lo schema è:

```text
scegli una configurazione iniziale s
ripeti:
    scegli un indice i
    calcola H_i(s)
    poni s_i <- sign H_i(s)
fino a convergenza
```

Questo tipo di aggiornamento si chiama **asincrono**, perché non tutte le unità vengono aggiornate simultaneamente.

L'aggiornamento asincrono ha una proprietà fondamentale: se i pesi sono simmetrici e $J_{ii}=0$, ogni aggiornamento non aumenta l'energia. La dinamica converge quindi verso una configurazione stabile, cioè una configurazione che non cambia più sotto la regola di aggiornamento.

## 4.6 Perché l'energia non aumenta

Supponiamo di aggiornare solo la variabile $s_i$, lasciando fisse tutte le altre. Il contributo dell'energia che dipende da $s_i$ può essere scritto, a meno di termini indipendenti da $s_i$, come

$$
E_i(s_i)=-s_i H_i(s).
$$

Se scegliamo

$$
s_i=\mathrm{sign}\,H_i(s),
$$

allora il prodotto $s_iH_i(s)$ è non negativo e il termine $-s_iH_i(s)$ è il più piccolo possibile tra le due scelte $s_i=pm 1$.

Quindi l'aggiornamento locale sceglie il valore di $s_i$ che minimizza l'energia rispetto a quella singola variabile, tenendo fisse le altre.

Di conseguenza, l'energia totale non aumenta. Questo rende $E(s)$ una funzione di Lyapunov per la dinamica asincrona.

Il risultato è importante perché garantisce che la dinamica non oscilli indefinitamente tra configurazioni diverse, almeno nella versione asincrona con pesi simmetrici. In uno spazio finito, una sequenza di aggiornamenti che non aumenta l'energia deve prima o poi fermarsi in uno stato stabile.

## 4.7 Attrattori e memorie

Una configurazione stabile soddisfa

$$
s_i=\mathrm{sign}\left(\sum_j J_{ij}s_j+h_i\right)
\qquad \text{per ogni } i.
$$

Questa condizione dice che ogni unità è coerente con il campo generato dalle altre unità.

Le configurazioni stabili sono attrattori della dinamica. Se la rete viene inizializzata vicino a una di esse, la dinamica può convergere verso quello stato stabile.

Per usare la rete come memoria associativa, si scelgono i pesi $J_{ij}$ in modo che alcuni pattern desiderati diventino attrattori. Indichiamo questi pattern con

$$
\xi^\mu=(\xi_1^\mu,\dots,\xi_N^\mu),
\qquad
\mu=1,
\dots,P,
$$

dove $P$ è il numero di pattern da memorizzare.

L'obiettivo è costruire una rete tale che, se lo stato iniziale è una versione corrotta di $\xi^\mu$, la dinamica converga verso $\xi^\mu$.

## 4.8 Regola di Hebb

Una scelta classica dei pesi è la regola di Hebb:

$$
J_{ij}=\frac{1}{N}\sum_{\mu=1}^P \xi_i^\mu \xi_j^\mu,
\qquad i\neq j,
$$

con

$$
J_{ii}=0.
$$

L'interpretazione è semplice. Se due unità hanno spesso lo stesso segno nei pattern memorizzati, il peso tra loro diventa positivo. Se hanno spesso segno opposto, il peso diventa negativo.

In questo modo le interazioni rinforzano le correlazioni presenti nei pattern da memorizzare.

Questa regola non richiede un addestramento iterativo complesso. I pesi sono calcolati direttamente dai pattern. Per questo la rete di Hopfield è un modello molto trasparente dal punto di vista didattico: mostra come una memoria possa essere codificata nelle interazioni.

## 4.9 Recupero di un pattern

Dopo avere costruito i pesi, possiamo testare la rete partendo da una configurazione iniziale $s(0)$ ottenuta perturbando un pattern memorizzato. Ad esempio, si può prendere un pattern $\xi^\mu$ e invertire casualmente una frazione dei suoi bit.

La dinamica asincrona viene poi applicata fino alla convergenza. Se la rete funziona correttamente, lo stato finale sarà il pattern originale, o una configurazione molto vicina ad esso.

Il processo può essere interpretato come correzione di errore:

$$
\text{pattern corrotto} \quad \longrightarrow \quad \text{pattern memorizzato}.
$$

La rete non confronta esplicitamente lo stato iniziale con tutti i pattern. La convergenza emerge dalla dinamica locale delle unità.

## 4.10 Memorie spurie

Le reti di Hopfield non memorizzano soltanto i pattern desiderati. Possono comparire anche attrattori non voluti, detti **memorie spurie**.

Questi stati stabili possono derivare da combinazioni dei pattern memorizzati o da interferenze tra essi. Per esempio, se si memorizzano molti pattern, le interazioni costruite con la regola di Hebb possono generare stati stabili che non corrispondono ad alcun pattern originario.

Questo fenomeno ha un significato importante. Il paesaggio energetico non contiene soltanto ciò che abbiamo cercato di imporre. Contiene anche le conseguenze globali delle interazioni. In altri termini, programmare localmente i pesi produce una struttura collettiva che può includere attrattori inattesi.

Dal punto di vista dei modelli generativi, questo è un primo segnale di un tema più generale: quando si definisce un'energia, non si controllano soltanto i singoli esempi desiderati, ma l'intera distribuzione implicita sugli stati.

## 4.11 Capacità e interferenza

Una rete di Hopfield può memorizzare solo un numero limitato di pattern in modo affidabile. Se il numero di pattern cresce troppo rispetto a $N$, aumentano le interferenze e il recupero diventa meno accurato.

In termini qualitativi:

* pochi pattern: attrattori ben separati e recupero robusto;
* molti pattern: interferenza tra memorie e aumento degli attrattori spurii;
* troppi pattern: perdita della capacità di recupero affidabile.

Questo limite è utile didatticamente perché mostra che la memoria distribuita non è gratuita. Gli stessi pesi devono codificare più pattern, e quindi ogni nuovo pattern modifica il paesaggio già costruito dagli altri.

## 4.12 Hopfield network come energy-based model?

Una rete di Hopfield usa una funzione energia, ma nella sua forma classica non è ancora un modello generativo probabilistico nel senso pieno del termine.

La dinamica classica è deterministica: dato uno stato iniziale e una sequenza di aggiornamenti, la rete converge verso un attrattore. L'obiettivo principale è il recupero di memorie, non il campionamento da una distribuzione.

Tuttavia, la rete di Hopfield è un passaggio concettuale fondamentale perché introduce tre idee che saranno centrali nelle Boltzmann Machines:

1. uno stato globale composto da molte variabili;
2. un'energia definita tramite interazioni;
3. una dinamica locale basata sul campo generato dalle altre variabili.

Per trasformare questa struttura in un modello probabilistico, bisogna introdurre aggiornamenti stocastici. Invece di porre deterministicamente

$$
s_i=\mathrm{sign}\,H_i(s),
$$

si assegna una probabilità ai due valori possibili di $s_i$. Questo porta naturalmente alle Boltzmann Machines.

## 4.13 Sintesi della sezione

Una rete di Hopfield è un modello di memoria associativa basato su una funzione energia:

$$
E(s)=-\frac{1}{2}\sum_{i,j}J_{ij}s_i s_j - \sum_i h_i s_i.
$$

La dinamica aggiorna localmente le unità in modo da non aumentare l'energia. Gli stati stabili diventano attrattori, e possono essere interpretati come memorie.

La regola di Hebb costruisce i pesi a partire dai pattern da memorizzare:

$$
J_{ij}=\frac{1}{N}\sum_{\mu=1}^P \xi_i^\mu \xi_j^\mu.
$$

Il modello mostra come una funzione energia possa organizzare il comportamento collettivo di molte variabili. Il passo successivo è rendere questa dinamica probabilistica: non solo convergere verso attrattori, ma campionare stati secondo una distribuzione definita dall'energia.

# 5. Boltzmann Machines

## 5.1 Dalla memoria deterministica al modello probabilistico

Una Boltzmann Machine può essere vista come un'estensione probabilistica dell'idea introdotta dalle reti di Hopfield. Anche qui abbiamo molte variabili binarie, interazioni tra variabili e una funzione energia. La differenza fondamentale è che la dinamica non serve soltanto a convergere verso un attrattore stabile: serve a definire e campionare una distribuzione di probabilità.

In una rete di Hopfield classica, una configurazione iniziale evolve verso uno stato stabile. In una Boltzmann Machine, invece, gli stati vengono visitati con probabilità proporzionale a un peso di Boltzmann:

$$
p(s)=\frac{e^{-E(s)}}{Z}.
$$

Gli stati a bassa energia sono più frequenti, ma gli stati ad energia più alta possono ancora essere visitati. Il modello non produce una sola configurazione finale: produce campioni da una distribuzione.

Questo passaggio è essenziale per costruire modelli generativi. Una memoria associativa recupera un pattern; una Boltzmann Machine può generare molte configurazioni plausibili.

## 5.2 Variabili visibili e variabili nascoste

La Boltzmann Machine distingue spesso tra due tipi di variabili:

* variabili **visibili**, indicate con $v$, che rappresentano ciò che osserviamo nei dati;
* variabili **nascoste**, indicate con $h$, che rappresentano fattori latenti non osservati direttamente.

Lo stato completo del modello è quindi

$$
s=(v,h).
$$

La distribuzione congiunta è definita da un'energia sullo stato completo:

$$
p(v,h)=\frac{e^{-E(v,h)}}{Z}.
$$

La probabilità delle variabili visibili si ottiene sommando su tutte le configurazioni nascoste:

$$
p(v)=\sum_h p(v,h).
$$

Questo passaggio è centrale. Il modello assegna probabilità ai dati osservati non solo in base a una singola configurazione nascosta, ma sommando il contributo di tutte le spiegazioni latenti compatibili con $v$.

## 5.3 Energia di una Boltzmann Machine

In una Boltzmann Machine generale, le variabili possono interagire tra loro attraverso pesi simmetrici. Per variabili binarie $s_i\in\{-1,+1\}$, una forma tipica dell'energia è

$$
E(s)=-\sum_i b_i s_i - \frac{1}{2}\sum_{i,j}W_{ij}s_i s_j,
$$

con

$$
W_{ij}=W_{ji},
\qquad
W_{ii}=0.
$$

I parametri $b_i$ sono bias locali. I parametri $W_{ij}$ rappresentano interazioni tra variabili. Se $W_{ij}>0$, le configurazioni con $s_i$ e $s_j$ dello stesso segno tendono ad avere energia più bassa. Se $W_{ij}<0$, sono favorite configurazioni con segni opposti.

Quando distinguiamo variabili visibili e nascoste, possiamo scrivere l'energia in blocchi. Indicando con $v_i$ le variabili visibili e con $h_a$ le variabili nascoste, una forma generale contiene:

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a
-\frac{1}{2}\sum_{i,j} A_{ij}v_i v_j
-\frac{1}{2}\sum_{a,b} B_{ab}h_a h_b.
$$

I diversi termini rappresentano bias visibili, bias nascosti, interazioni visibile--nascosto, interazioni tra visibili e interazioni tra nascosti.

## 5.4 Restricted Boltzmann Machine

Una forma particolarmente importante è la **Restricted Boltzmann Machine** o RBM. In una RBM non ci sono interazioni tra variabili visibili e non ci sono interazioni tra variabili nascoste. Restano solo le interazioni tra visibili e nascoste.

L'energia diventa

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a.
$$

La struttura è bipartita: le unità visibili interagiscono con le unità nascoste, ma non direttamente tra loro; le unità nascoste interagiscono con le visibili, ma non direttamente tra loro.

Questa restrizione rende il modello molto più semplice da campionare. Condizionando sulle visibili, le unità nascoste diventano indipendenti tra loro. Condizionando sulle nascoste, le unità visibili diventano indipendenti tra loro.

In termini operativi:

$$
p(h\mid v)=\prod_a p(h_a\mid v),
$$

e

$$
p(v\mid h)=\prod_i p(v_i\mid h).
$$
Qui $v$ e $h$ indicano vettori, non singole variabili:
$$
v=(v_1,\dots,v_n), \qquad h=(h_1,\dots,h_m).
$$

Perciò $p(h\mid v)$ significa
$$
p(h_1,\dots,h_m\mid v_1,\dots,v_n).
$$

Quindi nel caso di una RBM, fissato $v$, le variabili $h_a$ sono indipendenti condizionatamente a $v$; fissato $h$, le variabili $v_i$ sono indipendenti condizionatamente a $h$. Questa proprietà è la ragione principale per cui le RBM sono state molto usate: permettono un Gibbs sampling a blocchi relativamente semplice.

## 5.5 Probabilità condizionate

Per fissare le idee, consideriamo variabili binarie in forma $0/1$. In una RBM con energia

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a,
$$

la probabilità che un'unità nascosta sia attiva, condizionata alle visibili, ha la forma

$$
p(h_a=1\mid v)=\sigma\left(c_a+\sum_i W_{ia}v_i\right),
$$

dove

$$
\sigma(z)=\frac{1}{1+e^{-z}}
$$

è la funzione logistica.

Analogamente,

$$
p(v_i=1\mid h)=\sigma\left(b_i+\sum_a W_{ia}h_a\right).
$$

Queste formule mostrano il ruolo delle unità nascoste. Ogni unità nascosta combina informazione da molte unità visibili. Ogni unità visibile, a sua volta, viene ricostruita a partire dalle unità nascoste.

## 5.6 Campionamento alternato

La struttura bipartita della RBM permette un campionamento alternato:

```text
inizializza v
ripeti:
    campiona h da p(h | v)
    campiona v da p(v | h)
```

Ogni passaggio aggiorna un intero blocco di variabili condizionando sull'altro blocco. Questo è un caso particolarmente semplice di Gibbs sampling.

La sequenza

$$
v^{(0)} \to h^{(0)} \to v^{(1)} \to h^{(1)} \to v^{(2)} \to \cdots
$$

produce una catena di configurazioni. Dopo un numero sufficiente di passi, in condizioni appropriate, le configurazioni visibili campionate possono essere considerate campioni dalla distribuzione del modello.

In pratica, la difficoltà è capire quanto a lungo bisogna campionare e quanto bene la catena esplori lo spazio delle configurazioni.

## 5.7 Interpretazione generativa

Una RBM può essere usata come modello generativo nel seguente senso:

1. si campiona una configurazione nascosta $h$;
2. si campiona una configurazione visibile $v$ condizionata a $h$;
3. il risultato $v$ è un campione generato dal modello.

Le variabili nascoste possono essere interpretate come fattori latenti che organizzano la variabilità osservata. Non devono necessariamente corrispondere a categorie interpretabili in modo diretto, ma possono catturare regolarità statistiche utili.

Ad esempio, in un dataset di immagini binarie, alcune unità nascoste possono attivarsi per tratti, bordi, combinazioni di pixel o strutture ricorrenti. In un dataset sociale o di rete, unità nascoste potrebbero rappresentare fattori latenti di affinità, appartenenza o compatibilità. In un dataset biologico, potrebbero rappresentare combinazioni funzionali o pattern di co-attivazione.

Il punto generale è che le variabili nascoste permettono al modello di rappresentare dipendenze tra variabili osservate. Anche se le variabili visibili sono indipendenti condizionatamente a $h$, marginalmente possono essere fortemente dipendenti.

## 5.8 Apprendimento: abbassare l'energia dei dati

L'apprendimento consiste nel modificare i parametri in modo che le configurazioni osservate diventino più probabili.

Per un dato visibile $v$, la probabilità del modello è

$$
p(v)=\sum_h \frac{e^{-E(v,h)}}{Z}.
$$

La somma sulle variabili nascoste tiene conto di tutte le configurazioni latenti compatibili con $v$.

Intuitivamente, l'apprendimento deve fare due cose:

1. abbassare l'energia delle configurazioni $(v,h)$ associate ai dati osservati;
2. alzare, relativamente, l'energia delle configurazioni che il modello genera ma che non assomigliano ai dati.

Questa seconda parte è essenziale. Se il modello si limitasse ad abbassare l'energia dei dati senza controllare il resto dello spazio, la normalizzazione cambierebbe e l'apprendimento non sarebbe ben definito.

## 5.9 Positive phase e negative phase

Nel linguaggio delle Boltzmann Machines si parla spesso di due fasi del gradiente.

La **positive phase** usa i dati. In questa fase, i parametri vengono aggiornati in modo da ridurre l'energia delle configurazioni compatibili con le osservazioni.

La **negative phase** usa campioni generati dal modello. In questa fase, i parametri vengono aggiornati in modo da aumentare l'energia delle configurazioni che il modello produce troppo facilmente.

Schematicamente:

$$
\text{positive phase}: \quad \text{rende i dati più probabili},
$$

$$
\text{negative phase}: \quad \text{corregge ciò che il modello genera da solo}.
$$

Questa distinzione è una delle idee più importanti delle Boltzmann Machines. L'apprendimento non è solo adattamento ai dati; è confronto tra dati e campioni del modello.

## 5.10 Perché l'apprendimento è difficile

L'apprendimento esatto di una Boltzmann Machine generale è difficile per due ragioni.

La prima è la funzione di partizione:

$$
Z=\sum_{v,h} e^{-E(v,h)}.
$$

Questa somma corre su tutte le configurazioni visibili e nascoste. Se il numero di variabili è grande, il numero di stati cresce esponenzialmente.

La seconda difficoltà è la negative phase. Per stimare correttamente ciò che il modello genera, bisognerebbe campionare dalla distribuzione del modello. Ma il campionamento può richiedere molte iterazioni, specialmente se la distribuzione ha modi separati o forte dipendenza tra variabili.

Per questo motivo, molte procedure pratiche usano approssimazioni. La più nota, nel contesto delle RBM, è la contrastive divergence che vedremo in seguito.

## 5.11 Boltzmann Machine e Hopfield network

È utile confrontare schematicamente i due modelli.

| Aspetto       | Hopfield network                      | Boltzmann Machine                                  |
| ------------- | ------------------------------------- | -------------------------------------------------- |
| Stato         | variabili binarie                     | variabili binarie, spesso visibili e nascoste      |
| Energia       | sì                                    | sì                                                 |
| Dinamica      | deterministica o quasi deterministica | stocastica                                         |
| Obiettivo     | recupero di pattern                   | modellare una distribuzione                        |
| Stati finali  | attrattori                            | campioni probabilistici                            |
| Apprendimento | spesso regola di Hebb                 | massimizzazione della likelihood o approssimazioni |

Il passaggio concettuale è quindi:

$$
\text{attrattori di memoria} \quad \longrightarrow \quad \text{distribuzione generativa}.
$$

La Boltzmann Machine conserva l'idea di energia su molte variabili, ma la interpreta probabilisticamente.

## 5.12 Sintesi della sezione

Una Boltzmann Machine definisce una distribuzione su variabili binarie tramite una funzione energia:

$$
p(s)=\frac{e^{-E(s)}}{Z}.
$$

Quando il modello contiene variabili visibili $v$ e nascoste $h$, la distribuzione congiunta è

$$
p(v,h)=\frac{e^{-E(v,h)}}{Z},
$$

mentre la probabilità dei dati visibili è

$$
p(v)=\sum_h p(v,h).
$$

Le Restricted Boltzmann Machines semplificano la struttura eliminando interazioni visibile--visibile e nascosto--nascosto. Questa restrizione rende semplici le distribuzioni condizionate $p(h\mid v)$ e $p(v\mid h)$, permettendo Gibbs sampling a blocchi.

L'apprendimento richiede un confronto tra dati e campioni generati dal modello. Questa tensione tra positive phase e negative phase conduce direttamente alla contrastive divergence, che sarà discussa dopo avere introdotto esplicitamente il Gibbs sampling.

# 6. Gibbs sampling

## 6.1 Perché serve Gibbs sampling

Negli energy-based models la distribuzione target ha spesso la forma

$$
p(x)=\frac{e^{-E(x)}}{Z}.
$$

In molti casi sappiamo calcolare l'energia $E(x)$ di una configurazione, ma non sappiamo generare direttamente campioni indipendenti da $p(x)$. Il problema diventa quindi costruire una procedura iterativa che produca configurazioni distribuite, almeno approssimativamente, secondo la distribuzione desiderata.

Il **Gibbs sampling** è una strategia naturale quando la configurazione è composta da molte variabili:

$$
x=(x_1,x_2,\dots,x_N).
$$

L'idea è aggiornare una variabile alla volta, o un blocco di variabili alla volta, campionando dalla distribuzione condizionata rispetto alle altre variabili.

Invece di campionare direttamente da $p(x_1,\dots,x_N)$, si campiona iterativamente da distribuzioni del tipo

$$
p(x_i\mid x_1,\dots,x_{i-1},x_{i+1},\dots,x_N).
$$

Quando queste distribuzioni condizionate sono semplici, Gibbs sampling trasforma un problema globale difficile in una sequenza di problemi locali più trattabili.

## 6.2 Aggiornamento di una variabile

Supponiamo che lo stato corrente sia

$$
x=(x_1,\dots,x_i,\dots,x_N).
$$

Un passo di Gibbs aggiorna la variabile $x_i$ campionando dalla distribuzione condizionata

$$
p(x_i\mid x_{-i}),
$$

dove $x_{-i}$ indica tutte le variabili tranne $x_i$.

Dopo l'aggiornamento, otteniamo un nuovo stato

$$
x'=(x_1,\dots,x_i',\dots,x_N),
$$

in cui solo la componente $i$ è cambiata.

Ripetendo questo procedimento per molte variabili e per molte iterazioni si ottiene una catena di configurazioni:

$$
x^{(0)},x^{(1)},x^{(2)},\dots\
$$

Se la catena è costruita correttamente e viene lasciata evolvere abbastanza a lungo, le configurazioni visitate possono essere usate come campioni dalla distribuzione target.

## 6.3 Perché le condizionate non richiedono sempre $Z$

Un vantaggio importante del Gibbs sampling è che le distribuzioni condizionate possono essere calcolate senza conoscere la funzione di partizione globale.

Consideriamo una distribuzione

$$
p(x)=\frac{e^{-E(x)}}{Z}.
$$

La condizionata di $x_i$ dato $x_{-i}$ è

$$
p(x_i\mid x_{-i})=
\frac{p(x_i,x_{-i})}{\sum_{x_i'}p(x_i',x_{-i})}.
$$

Sostituendo la forma energetica,

$$
p(x_i\mid x_{-i})=
\frac{e^{-E(x_i,x_{-i})}/Z}
{\sum_{x_i'}e^{-E(x_i',x_{-i})}/Z}.
$$

La normalizzazione globale $Z$ si cancella:

$$
p(x_i\mid x_{-i})=
\frac{e^{-E(x_i,x_{-i})}}
{\sum_{x_i'}e^{-E(x_i',x_{-i})}}.
$$

La somma al denominatore non corre su tutto lo spazio delle configurazioni, ma solo sui possibili valori della variabile $x_i$. Se $x_i$ è binaria, la somma contiene solo due termini.

Questo è il motivo per cui Gibbs sampling è così utile nei modelli con molte variabili discrete.

## 6.4 Caso binario

Consideriamo variabili binarie

$$
s_i\in\{-1,+1\}.
$$

Supponiamo che, fissate tutte le altre variabili, la parte dell'energia che dipende da $s_i$ sia

$$
E_i(s_i)=-s_i H_i,
$$

dove $H_i$ è il campo locale prodotto dalle altre variabili.

Allora

$$
p(s_i\mid s_{-i})
= \frac{e^{s_i H_i}}{e^{H_i}+e^{-H_i}}.
$$

In particolare,

$$
p(s_i=+1\mid s_{-i})=
\frac{e^{H_i}}{e^{H_i}+e^{-H_i}} =
\frac{1}{1+e^{-2H_i}}.
$$

Analogamente,

$$
p(s_i=-1\mid s_{-i})=
\frac{1}{1+e^{2H_i}}.
$$

Il confronto con l'aggiornamento deterministico è istruttivo. Una rete deterministica sceglierebbe

$$
s_i=\mathrm{sign}(H_i).
$$

Il Gibbs sampling sceglie invece $s_i=+1$ o $s_i=-1$ con probabilità dipendente dal campo locale. Se $H_i$ è molto positivo, $s_i=+1$ è quasi certo. Se $H_i$ è molto negativo, $s_i=-1$ è quasi certo. Se $H_i$ è vicino a zero, entrambe le scelte restano plausibili.

## 6.5 Caso $0/1$ e funzione logistica

Nelle Boltzmann Machines si usano spesso variabili binarie nella forma

$$
x_i\in\{0,1\}.
$$

In questo caso le probabilità condizionate assumono spesso una forma logistica. Se il campo efficace su $x_i$ è $a_i$, allora

$$
p(x_i=1\mid x_{-i})=\sigma(a_i),
$$

dove

$$
\sigma(a)=\frac{1}{1+e^{-a}}.
$$

Questa forma compare direttamente nelle Restricted Boltzmann Machines. Per le unità nascoste,

$$
p(h_a=1\mid v)=\sigma\left(c_a+\sum_i W_{ia}v_i\right),
$$

mentre per le unità visibili,

$$
p(v_i=1\mid h)=\sigma\left(b_i+\sum_a W_{ia}h_a\right).
$$

Il vantaggio operativo è notevole: dato un blocco, le variabili dell'altro blocco possono essere campionate in modo indipendente.

## 6.6 Gibbs sampling a blocchi nelle RBM

In una Restricted Boltzmann Machine non ci sono interazioni dirette tra unità dello stesso tipo. Per questo motivo,

$$
p(h\mid v)=\prod_a p(h_a\mid v)
$$

e

$$
p(v\mid h)=\prod_i p(v_i\mid h).
$$

Si può quindi aggiornare l'intero blocco nascosto in parallelo, e poi l'intero blocco visibile in parallelo.

Lo schema è:

```text
inizializza v
ripeti:
    campiona tutti gli h_a indipendentemente da p(h_a | v)
    campiona tutti i v_i indipendentemente da p(v_i | h)
```

La catena alterna stati visibili e nascosti:

$$
v^{(0)} \to h^{(0)} \to v^{(1)} \to h^{(1)} \to v^{(2)} \to \cdots
$$

Il fatto che gli aggiornamenti condizionati siano semplici è una delle ragioni principali per cui le RBM sono computazionalmente più trattabili delle Boltzmann Machines generali.

## 6.7 Burn-in e campioni correlati

Il Gibbs sampling produce una catena di Markov. Questo significa che i campioni successivi non sono indipendenti: ogni configurazione dipende dalla precedente.

Per usare la catena come generatore di campioni occorre tenere conto di due aspetti.

Il primo è il **burn-in** (ovvero la *termalizzazione*). Le prime configurazioni dipendono fortemente dallo stato iniziale e possono non rappresentare ancora bene la distribuzione target. In molte applicazioni si scartano i primi passi della catena.

Il secondo è l'**autocorrelazione**. Anche dopo il burn-in, configurazioni vicine nella catena possono essere molto simili. In questo caso il numero effettivo di campioni indipendenti è inferiore al numero di passi simulati.

Questi aspetti non sono dettagli tecnici secondari. Se la catena esplora lentamente lo spazio, le stime ottenute dai campioni possono essere distorte o molto rumorose.

## 6.8 Mixing

Il termine **mixing** descrive la capacità della catena di esplorare efficacemente la distribuzione target.

Una catena con buon mixing si sposta tra regioni diverse dello spazio delle configurazioni e dimentica rapidamente la condizione iniziale. Una catena con cattivo mixing resta a lungo confinata in una regione e produce campioni fortemente correlati.

Negli energy-based models il mixing può essere difficile perché la distribuzione può avere regioni di alta probabilità separate da regioni di bassa probabilità. Una dinamica locale, che cambia poche variabili alla volta, può impiegare molto tempo per passare da una regione all'altra.

Questo problema è particolarmente importante nell'apprendimento. Se la negative phase viene stimata usando campioni che non rappresentano bene la distribuzione del modello, il gradiente risultante può essere una cattiva approssimazione del gradiente vero.

## 6.9 Gibbs sampling e apprendimento

Nel contesto delle Boltzmann Machines, Gibbs sampling compare in due punti.

Primo, serve per generare campioni dal modello. Dopo l'apprendimento, questi campioni rappresentano configurazioni prodotte dalla distribuzione appresa.

Secondo, serve durante l'apprendimento per stimare il termine della negative phase. Questo termine richiede medie rispetto alla distribuzione del modello, che di solito non sono calcolabili esattamente.

Il problema pratico è che il Gibbs sampling esatto richiederebbe catene sufficientemente lunghe da raggiungere una buona approssimazione della distribuzione stazionaria. Questo può essere costoso.

La contrastive divergence nasce come risposta a questa difficoltà: invece di campionare fino all'equilibrio, parte dai dati e compie pochi passi di Gibbs.

## 6.10 Sintesi della sezione

Il Gibbs sampling è un metodo per campionare da una distribuzione complessa aggiornando una variabile, o un blocco di variabili, alla volta.

Per una distribuzione energetica

$$
p(x)=\frac{e^{-E(x)}}{Z},
$$

le distribuzioni condizionate possono spesso essere calcolate senza conoscere la normalizzazione globale $Z$.

Nelle Restricted Boltzmann Machines, la struttura bipartita rende particolarmente semplice il campionamento alternato:

$$
v \to h \to v \to h \to \cdots
$$

Il limite principale è che i campioni prodotti sono correlati e la catena può avere mixing lento. Questo rende costoso stimare correttamente le medie rispetto al modello.

La sezione successiva affronta precisamente questo problema dal punto di vista dell'apprendimento: come stimare i parametri quando la funzione di partizione è intrattabile e la negative phase richiede campionamento.

# 7. Apprendimento e problema di $Z$

## 7.1 Il problema di apprendere un'energia

In un energy-based model la distribuzione è definita da

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta},
$$

con

$$
Z_\theta=\sum_x e^{-E_\theta(x)}
$$

nel caso discreto, oppure

$$
Z_\theta=\int e^{-E_\theta(x)},dx
$$

nel caso continuo.

Il parametro $\theta$ controlla la forma dell'energia. Apprendere il modello significa scegliere $\theta$ in modo che le configurazioni osservate nei dati risultino probabili sotto $p_\theta$.

Il punto delicato è che cambiare $\theta$ modifica non solo l'energia dei dati osservati, ma anche l'energia di tutte le configurazioni non osservate. Di conseguenza, cambia anche $Z_\theta$.

L'apprendimento non consiste quindi semplicemente nell'abbassare l'energia dei dati. Bisogna abbassarla **relativamente** all'energia delle altre configurazioni.

## 7.2 Dataset e log-likelihood

Supponiamo di osservare un dataset

$$
\mathcal{D}={x^{(1)},\dots,x^{(n)}}.
$$

La log-likelihood del modello è

$$
\ell(\theta)=\sum_{i=1}^n \log p_\theta(x^{(i)}).
$$

Usando la forma energetica,

$$
\log p_\theta(x)= -E_\theta(x)-\log Z_\theta.
$$

Quindi

$$
\ell(\theta) =
-\sum_{i=1}^n E_\theta(x^{(i)})
-n\log Z_\theta.
$$

Questa formula contiene già tutta la struttura dell'apprendimento.

Il primo termine dipende solo dai dati osservati:

$$
-\sum_{i=1}^n E_\theta(x^{(i)}).
$$

Massimizzare questo termine spinge il modello ad abbassare l'energia delle configurazioni presenti nel dataset.

Il secondo termine,

$$
-n\log Z_\theta,
$$

dipende invece da tutte le configurazioni possibili. Serve a mantenere normalizzata la distribuzione e impedisce la soluzione banale in cui tutte le energie vengono abbassate insieme.

## 7.3 Perché il termine $\log Z_\theta$ è necessario

Immaginiamo di ignorare il termine $\log Z_\theta$ e di massimizzare solo

$$
-\sum_{i=1}^n E_\theta(x^{(i)}).
$$

Il modello potrebbe migliorare indefinitamente questo obiettivo abbassando l'energia dei dati. Ma una probabilità non dipende solo dall'energia assoluta di una configurazione: dipende dal confronto con il peso totale di tutte le configurazioni.

Se abbassiamo l'energia di tutti gli stati della stessa quantità, i pesi non normalizzati aumentano tutti dello stesso fattore, ma la distribuzione normalizzata non cambia. La normalizzazione elimina trasformazioni globali di questo tipo.

Il termine $\log Z_\theta$ è quindi ciò che rende l'apprendimento probabilistico, non solo energetico. Esso obbliga il modello a distribuire massa di probabilità: aumentare la probabilità di alcune configurazioni significa, in termini relativi, ridurre quella di altre.

## 7.4 Gradiente della log-likelihood

Per capire la struttura dell'apprendimento calcoliamo il gradiente della log-likelihood.

Partiamo da un singolo dato $x$. Si ha

$$
\log p_\theta(x)=-E_\theta(x)-\log Z_\theta.
$$

Derivando rispetto a $\theta$,

$$
\nabla_\theta \log p_\theta(x) = 
-\nabla_\theta E_\theta(x)
- \nabla_\theta \log Z_\theta.
$$

Ora calcoliamo il secondo termine. Nel caso discreto,

$$
Z_\theta=\sum_y e^{-E_\theta(y)}.
$$

Quindi

$$
\nabla_\theta Z_\theta =
\sum_y -\nabla_\theta E_\theta(y)\,e^{-E_\theta(y)}.
$$

Dividendo per $Z_\theta$ otteniamo

$$
\frac{1}{Z_\theta}\nabla_\theta Z_\theta =
\nabla_\theta \log Z_\theta =
-\sum_y p_\theta(y)\nabla_\theta E_\theta(y).
$$

Cioè

$$
\nabla_\theta \log Z_\theta =
-\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Sostituendo,

$$
\nabla_\theta \log p_\theta(x) =
-\nabla_\theta E_\theta(x)
+ \mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Per l'intero dataset,

$$
\nabla_\theta \ell(\theta) =
-\sum_{i=1}^n \nabla_\theta E_\theta(x^{(i)})
+n\,\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Questa formula è il cuore dell'apprendimento negli energy-based models.

## 7.5 Positive phase e negative phase

Il gradiente contiene due contributi.

Il primo contributo è calcolato sui dati:

$$
-\sum_{i=1}^n \nabla_\theta E_\theta(x^{(i)}).
$$

Questo termine spinge ad abbassare l'energia delle configurazioni osservate. Viene spesso chiamato **positive phase**, perché aumenta la probabilità dei dati.

Il secondo contributo è una media rispetto alla distribuzione del modello:

$$
n\,\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Questo termine corregge ciò che il modello considera probabile. Viene spesso chiamato **negative phase**, perché riduce la probabilità relativa delle configurazioni che il modello genera troppo facilmente.

In forma intuitiva:

$$
\text{positive phase} = \text{guarda i dati},
$$

$$
\text{negative phase} = \text{guarda il modello}.
$$

L'apprendimento confronta continuamente questi due oggetti: ciò che è osservato e ciò che il modello tende a produrre.

## 7.6 Dati contro modello

È utile riscrivere il gradiente in termini di medie. Definiamo la media empirica sui dati:

$$
\mathbb{E}_{data}[f(X)] = \frac{1}{n}\sum_{i=1}^n f(x^{(i)}).
$$

Allora il gradiente medio della log-likelihood può essere scritto come

$$
\frac{1}{n}\nabla_\theta \ell(\theta) =
-\mathbb{E}_{data}\left[\nabla_\theta E_\theta(X)\right]
+ \mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Questa forma mette in evidenza il confronto tra due distribuzioni:

1. la distribuzione empirica dei dati;
2. la distribuzione generata dal modello.

Al massimo della likelihood, idealmente, il modello riproduce le statistiche rilevanti dei dati. Se l'energia è parametrizzata in modo lineare rispetto ad alcune feature, questa condizione diventa un confronto tra feature osservate nei dati e feature attese sotto il modello.

## 7.7 Esempio: energia lineare nelle feature

Supponiamo che l'energia abbia la forma

$$
E_\theta(x)=-\sum_k \theta_k f_k(x),
$$

dove $f_k(x)$ sono feature della configurazione.

Allora

$$
\frac{\partial E_\theta(x)}{\partial \theta_k}=-f_k(x).
$$

Il gradiente medio diventa

$$
\frac{1}{n}\frac{\partial \ell}{\partial \theta_k} =
\mathbb{E}_{data}[f_k(X)]
- \mathbb{E}_{p_\theta}[f_k(Y)].
$$

Quindi l'apprendimento spinge il modello a soddisfare una condizione di matching:

$$
\mathbb{E}_{p_\theta}[f_k(Y)]
\approx
\mathbb{E}_{data}[f_k(X)].
$$

Questo risultato è importante perché collega gli energy-based models al principio di massima entropia e ai modelli esponenziali. Le feature specificano quali statistiche vogliamo riprodurre; l'energia assegna parametri a queste statistiche; la likelihood cerca un modello che le riproduca in media.

## 7.8 Il caso con variabili nascoste

Nelle Boltzmann Machines con variabili visibili $v$ e nascoste $h$, i dati riguardano solo $v$. La distribuzione osservabile è

$$
p_\theta(v)=\sum_h p_\theta(v,h).
$$

La log-probabilità di un dato visibile è

$$
\log p_\theta(v)=\log \sum_h e^{-E_\theta(v,h)} - \log Z_\theta.
$$

Il primo termine somma il contributo di tutte le configurazioni nascoste compatibili con $v$. È spesso utile introdurre la **free energy** associata alle variabili visibili:

$$
F_\theta(v)=-\log \sum_h e^{-E_\theta(v,h)}.
$$

Allora

$$
p_\theta(v)=\frac{e^{-F_\theta(v)}}{Z_\theta},
$$

con la stessa funzione di partizione globale

$$
Z_\theta=\sum_v e^{-F_\theta(v)} =
\sum_{v,h}e^{-E_\theta(v,h)}.
$$

La free energy è quindi l'energia efficace delle configurazioni visibili dopo avere sommato sulle variabili nascoste.

## 7.9 Perché la free energy è utile

La free energy permette di trattare un modello con variabili nascoste come un modello energetico sulle sole variabili osservate.

Una configurazione visibile $v$ ha bassa free energy se esistono molte configurazioni nascoste $h$ che la rendono plausibile, oppure se alcune configurazioni nascoste hanno energia molto bassa.

Questo è un punto concettuale importante. La probabilità di $v$ non dipende solo dalla migliore spiegazione nascosta, ma dal contributo complessivo delle spiegazioni nascoste.

In simboli:

$$
F_\theta(v)=-\log \sum_h e^{-E_\theta(v,h)}.
$$

La somma su $h$ aggrega tutte le spiegazioni latenti. Il logaritmo trasforma questo peso complessivo in un'energia efficace.

Nel caso delle RBM, questa quantità può essere calcolata in forma relativamente semplice perché le unità nascoste sono indipendenti condizionatamente a $v$. Questo rende più semplice trattare il termine sui dati. Il termine di modello, però, resta difficile perché richiede comunque medie rispetto alla distribuzione generata dal modello.

## 7.10 Il nodo computazionale

Il gradiente della log-likelihood richiede una media rispetto a $p_\theta$:

$$
\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Questa media è il vero collo di bottiglia computazionale. In linea di principio, si potrebbe calcolare sommando su tutte le configurazioni:

$$
\mathbb{E}_{p_\theta}[g(Y)] = \sum_y g(y)p_\theta(y).
$$

Ma questa somma è impraticabile quando lo spazio degli stati è grande. L'alternativa è stimarla mediante campioni generati dal modello:

$$
\mathbb{E}_{p_\theta}[g(Y)]
\approx
\frac{1}{M}\sum_{m=1}^M g(y^{(m)}),
\qquad
y^{(m)}\sim p_\theta.
$$
dove usiamo il formalismo di teoria della probabilità in cui il simbolo $\sim$ significa **“è distribuito secondo”**.

Quindi il problema dell'apprendimento si riduce in parte a un problema di campionamento. Se i campioni del modello sono buoni, la stima della negative phase è buona. Se il campionamento è lento o distorto, anche l'apprendimento può diventare lento o distorto.

## 7.11 Strategie possibili

Esistono diverse strategie per affrontare il problema.

Una prima possibilità è usare catene MCMC lunghe, cercando di approssimare accuratamente la distribuzione del modello. Questo è concettualmente pulito, ma può essere molto costoso.

Una seconda possibilità è mantenere catene persistenti durante l'apprendimento. Invece di ricominciare il campionamento da zero a ogni aggiornamento dei parametri, si continua a far evolvere catene già esistenti. Questa idea cerca di rendere meno costosa la negative phase.

Una terza possibilità è usare una catena breve inizializzata sui dati. Questa è l'idea alla base della contrastive divergence. Invece di pretendere campioni perfetti dal modello, si confrontano i dati con configurazioni ottenute dopo pochi passi di ricostruzione.

La contrastive divergence non va interpretata come campionamento esatto. È un'approssimazione pratica del gradiente, utile quando il campionamento completo sarebbe troppo costoso.

## 7.12 Sintesi della sezione

L'apprendimento di un energy-based model tramite massima likelihood porta alla log-likelihood

$$
\ell(\theta) =
-\sum_{i=1}^n E_\theta(x^{(i)})
-n\log Z_\theta.
$$

Il gradiente ha due parti:

$$
\frac{1}{n}\nabla_\theta \ell(\theta)  =
-\mathbb{E}_{data}\left[\nabla_\theta E_\theta(X)\right]
+\mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

La prima parte abbassa l'energia dei dati. La seconda parte corregge il modello usando configurazioni generate dalla distribuzione corrente.

Il problema computazionale nasce perché la seconda media richiede campionamento dal modello. Quando questo campionamento è costoso, servono approssimazioni.

La contrastive divergence è una di queste approssimazioni: usa pochi passi di Gibbs sampling a partire dai dati per ottenere un segnale di apprendimento pratico.

# 8. Contrastive divergence

## 8.1 Il problema pratico

L'apprendimento di una Boltzmann Machine richiede il gradiente della log-likelihood. Nella forma generale, questo gradiente contiene due contributi:

$$
\frac{1}{n}\nabla_\theta \ell(\theta)  =
-\mathbb{E}_{data}\left[\nabla_\theta E_\theta(X)\right]
+ \mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Il primo termine è una media sui dati osservati. Questo termine è relativamente semplice: il dataset è disponibile.

Il secondo termine è una media rispetto alla distribuzione del modello. Questo è il punto difficile. Per calcolarlo esattamente bisognerebbe sommare su tutte le configurazioni o generare campioni affidabili da $p_\theta$.

Nel caso di modelli grandi, entrambe le strategie possono essere troppo costose. Anche usando Gibbs sampling, una catena lunga fino all'equilibrio può richiedere molte iterazioni.

La **contrastive divergence** nasce come approssimazione pratica di questo problema.

## 8.2 L'idea di base

L'idea è sostituire i campioni esatti dal modello con campioni ottenuti dopo pochi passi di Gibbs sampling, partendo dai dati.

Invece di inizializzare la catena in uno stato casuale e aspettare che converga alla distribuzione del modello, si parte da una configurazione osservata $x^{(0)}$ e si applicano pochi passi della dinamica di campionamento:

$$
x^{(0)} \to x^{(1)} \to x^{(2)} \to \cdots \to x^{(k)}.
$$

Il punto iniziale $x^{(0)}$ è un dato reale. Il punto finale $x^{(k)}$ è una configurazione prodotta dal modello dopo $k$ passi di ricostruzione.

La contrastive divergence confronta questi due oggetti:

$$
\text{dato reale} \quad \text{versus} \quad \text{ricostruzione dopo pochi passi}.
$$

In forma intuitiva, il modello viene aggiornato in modo da rendere più probabili i dati e meno probabili le configurazioni verso cui il modello tende subito a muoversi partendo dai dati.

## 8.3 CD-k

La versione con $k$ passi di Gibbs sampling si indica spesso con **CD-k**.

Lo schema generale è:

```text
per ogni dato x^(0):
    inizializza la catena in x^(0)
    esegui k passi di Gibbs sampling
    ottieni x^(k)
    aggiorna i parametri confrontando x^(0) e x^(k)
```

Nel caso di una RBM, il passaggio è spesso scritto in termini di visibili e nascosti:

```text
v^(0) = dato osservato
campiona h^(0) da p(h | v^(0))
campiona v^(1) da p(v | h^(0))
campiona h^(1) da p(h | v^(1))
...
dopo k ricostruzioni ottieni v^(k), h^(k)
```

Per CD-1, si usa una sola ricostruzione:

$$
v^{(0)} \to h^{(0)} \to v^{(1)} \to h^{(1)}.
$$

CD-1 è molto economica computazionalmente, ma è anche un'approssimazione più grossolana della negative phase.

## 8.4 Positive phase e fase ricostruttiva

Nel caso di una RBM con energia

$$
E(v,h)=
-\sum_i b_i v_i
-\sum_a c_a h_a
-\sum_{i,a} W_{ia}v_i h_a,
$$

l'aggiornamento dei pesi ha una forma intuitiva. Per il parametro $W_{ia}$, il termine rilevante è il prodotto $v_i h_a$.

L'aggiornamento ideale della likelihood confronta:

$$
\langle v_i h_a\rangle_{data}
\quad \text{e} \quad
\langle v_i h_a\rangle_{model}.
$$

La contrastive divergence sostituisce la media del modello con una media sui campioni ricostruiti dopo pochi passi:

$$
\Delta W_{ia} \propto
\langle v_i h_a\rangle_{data} - \langle v_i h_a\rangle_{CD-k}.
$$

Il primo termine misura quanto spesso l'unità visibile $i$ e l'unità nascosta $a$ sono attive quando si guarda ai dati. Il secondo termine misura quanto spesso lo sono nelle configurazioni prodotte dalla catena breve.

In modo analogo, per i bias si hanno aggiornamenti schematici del tipo

$$
\Delta b_i \propto \langle v_i\rangle_{data}-\langle v_i\rangle_{CD-k},
$$

e

$$
\Delta c_a \propto \langle h_a\rangle_{data}-\langle h_a\rangle_{CD-k}.
$$

Il modello viene quindi spinto a correggere le differenze tra dati e ricostruzioni.

## 8.5 Perché partire dai dati

Partire dai dati ha un vantaggio pratico: la catena inizia in una regione già plausibile dello spazio delle configurazioni.

Se il modello è ancora in fase di apprendimento, una catena inizializzata casualmente può produrre configurazioni molto lontane dai dati e richiedere molti passi per raggiungere regioni utili. Inizializzando dai dati, invece, si osserva come il modello deforma localmente le configurazioni osservate.

Se dopo pochi passi la catena ricostruisce configurazioni simili ai dati, il modello è localmente coerente con il dataset. Se invece le ricostruzioni si allontanano rapidamente, l'aggiornamento corregge i parametri.

Questa è l'intuizione della contrastive divergence: non si cerca subito di stimare perfettamente l'intera distribuzione del modello; si cerca di ridurre il contrasto tra i dati e ciò che il modello produce nelle loro vicinanze.

## 8.6 Che cosa approssima CD

La contrastive divergence non è, in generale, il gradiente esatto della log-likelihood. Essa sostituisce la negative phase esatta con una negative phase approssimata.

Il gradiente esatto richiederebbe campioni distribuiti secondo $p_\theta$. CD-k usa invece campioni ottenuti dopo $k$ passi di una catena inizializzata sui dati.

Quindi:

$$
\langle \cdot \rangle_{model}
\quad \text{viene sostituito da} \quad
\langle \cdot \rangle_{CD-k}.
$$

Se $k$ fosse molto grande e la catena avesse tempo di raggiungere l'equilibrio, la media CD-k si avvicinerebbe alla media del modello. Per $k$ piccolo, invece, la stima è distorta ma spesso utile dal punto di vista computazionale.

Questa è la natura della procedura: CD scambia accuratezza asintotica con efficienza pratica.

## 8.7 Interpretazione geometrica locale

Si può interpretare CD come una procedura che confronta i dati con le configurazioni verso cui il modello li sposta dopo pochi passi.

Se il modello assegna energia coerente con la struttura dei dati, una breve dinamica di Gibbs inizializzata sui dati dovrebbe produrre configurazioni simili ai dati stessi. Se invece il modello produce rapidamente configurazioni implausibili, il contrasto tra $x^{(0)}$ e $x^{(k)}$ fornisce un segnale di correzione.

Questa interpretazione è locale: CD-k non esplora necessariamente tutto lo spazio delle configurazioni. Esamina soprattutto il comportamento del modello vicino alla distribuzione empirica.

Per questo motivo può funzionare bene come procedura di apprendimento iniziale o pratica, ma non va confusa con una stima esatta del gradiente della likelihood.

## 8.8 CD-1 nelle RBM

Nel caso più comune, CD-1 per una RBM procede così.

Dato un esempio visibile $v^{(0)}$:

1. si campiona il blocco nascosto:

$$
h^{(0)}\sim p(h\mid v^{(0)});
$$

2. si ricostruisce il blocco visibile:

$$
v^{(1)}\sim p(v\mid h^{(0)});
$$

3. si campiona nuovamente il blocco nascosto:

$$
h^{(1)}\sim p(h\mid v^{(1)});
$$

4. si aggiornano i parametri confrontando le correlazioni $v^{(0)}h^{(0)}$ e $v^{(1)}h^{(1)}$.

Per i pesi:

$$
\Delta W_{ia} =
\eta\left( 
\langle v_i^{(0)}h_a^{(0)}\rangle - \langle v_i^{(1)}h_a^{(1)}\rangle
\right),
$$

dove $\eta$ è il learning rate e le medie sono calcolate sul mini-batch di dati.

La stessa logica vale per i bias visibili e nascosti:

$$
\Delta b_i =
\eta\left(
\langle v_i^{(0)}\rangle - \langle v_i^{(1)}\rangle
\right),
$$

$$
\Delta c_a =
\eta\left(
\langle h_a^{(0)}\rangle - \langle h_a^{(1)}\rangle
\right).
$$

Queste formule sono schematiche ma catturano il punto essenziale: i parametri vengono aggiornati per rendere le ricostruzioni più simili ai dati nelle statistiche rilevanti.

## 8.9 Limiti della contrastive divergence

La contrastive divergence è utile, ma ha limiti importanti.

Primo, non fornisce in generale il gradiente esatto della log-likelihood. L'aggiornamento è distorto perché la catena breve non campiona dalla distribuzione stazionaria del modello.

Secondo, può approssimare male la negative phase se il modello ha mixing lento. In quel caso, pochi passi di Gibbs esplorano solo una piccola regione dello spazio.

Terzo, CD può migliorare la qualità delle ricostruzioni senza necessariamente fornire una stima accurata della probabilità normalizzata dei dati.

Questi limiti non rendono CD inutile. Significano però che bisogna interpretarla correttamente: è un metodo pratico per apprendere modelli energetici, non una soluzione esatta del problema della likelihood.

## 8.10 Persistent contrastive divergence

Una variante importante è la **persistent contrastive divergence**. Invece di inizializzare la catena ogni volta dai dati, si mantengono una o più catene persistenti durante l'apprendimento.

A ogni aggiornamento dei parametri, le catene vengono fatte evolvere per pochi passi, ma non vengono reinizializzate. In questo modo possono seguire più da vicino la distribuzione del modello mentre i parametri cambiano gradualmente.

L'idea è ridurre il bias introdotto dall'inizializzazione continua sui dati. Le catene persistenti cercano di fornire campioni più rappresentativi della negative phase.

Naturalmente, anche questa strategia dipende dal mixing. Se la catena esplora male lo spazio, la stima resta problematica.

## 8.11 Sintesi della sezione

La contrastive divergence è un'approssimazione pratica dell'apprendimento negli energy-based models, particolarmente usata per le Restricted Boltzmann Machines.

Il gradiente esatto richiederebbe una positive phase sui dati e una negative phase sui campioni del modello. La negative phase è difficile perché richiede campionare da $p_\theta$.

CD-k sostituisce i campioni del modello con campioni ottenuti dopo $k$ passi di Gibbs sampling inizializzati dai dati:

$$
x^{(0)}_{data} \to x^{(k)}_{recon}.
$$

L'aggiornamento confronta statistiche dei dati e statistiche delle ricostruzioni:

$$
\Delta W_{ia} \propto
\langle v_i h_a\rangle_{data} - \langle v_i h_a\rangle_{CD-k}.
$$

Il metodo è efficiente ma approssimato. Funziona come scorciatoia computazionale per ottenere un segnale di apprendimento senza attendere il campionamento completo dalla distribuzione del modello.

# 9. Hamiltonian Monte Carlo per spazi continui

## 9.1 Perché serve un metodo diverso

Molti energy-based models sono definiti su spazi discreti, come configurazioni binarie o variabili categoriali. In questi casi, aggiornare una variabile alla volta può essere una strategia naturale. In altri problemi, però, lo spazio degli stati è continuo e ad alta dimensione.

Esempi tipici sono:

* parametri continui di un modello statistico;
* variabili latenti continue;
* configurazioni fisiche con posizioni e velocità;
* modelli bayesiani con molti parametri;
* distribuzioni continue definite da una negative log-likelihood o da una negative log-posterior.

In questi casi, una dinamica che propone piccoli passi casuali può essere inefficiente. La catena si muove lentamente, produce campioni fortemente correlati e può richiedere molte iterazioni per esplorare regioni lontane dello spazio.

Hamiltonian Monte Carlo, o HMC, nasce per affrontare questo problema. L'idea è usare l'informazione geometrica contenuta nel gradiente della distribuzione target per costruire proposte lunghe ma ancora plausibili.

## 9.2 Distribuzione target e energia potenziale

Supponiamo di voler campionare una distribuzione continua

$$
\pi(q),
$$

dove

$$
q\in\mathbb{R}^d
$$

è il vettore delle variabili da campionare.

In molti problemi conosciamo $\pi(q)$ solo a meno di una costante di normalizzazione:

$$
\pi(q)\propto e^{-U(q)}.
$$

La funzione

$$
U(q)=-\log \pi(q)+\text{costante}
$$

si interpreta come **energia potenziale**. La costante non è importante, perché non cambia i gradienti né i rapporti di probabilità.

Questa scrittura è perfettamente coerente con il linguaggio degli energy-based models: la densità target viene definita tramite un'energia.

## 9.3 Introduzione del momento ausiliario

HMC introduce una variabile ausiliaria di momento

$$
p\in\mathbb{R}^d.
$$

Attenzione alla notazione: qui $p$ indica il momento (in fisica: un oggetto con dimensione $massa \times velocita$), non una probabilità. Per evitare ambiguità, alcuni testi usano $r$ al posto di $p$. Qui manteniamo $p$ perché è la notazione standard in meccanica hamiltoniana.

Si definisce un'energia cinetica

$$
K(p)=\frac{1}{2}p^T M^{-1}p,
$$

dove $M$ è una matrice definita positiva, detta matrice di massa. Nel caso più semplice,

$$
M=I,
$$

e quindi

$$
K(p)=\frac{1}{2}p^T p.
$$

Il sistema esteso ha energia totale, o Hamiltoniana,

$$
H(q,p)=U(q)+K(p).
$$

La distribuzione congiunta su posizione e momento è

$$
\pi(q,p)\propto e^{-H(q,p)}=e^{-U(q)}e^{-K(p)}.
$$

Questa fattorizzazione implica che, marginalizzando sui momenti, si recupera la distribuzione desiderata su $q$.

## 9.4 Dinamica hamiltoniana

Una volta introdotta l'Hamiltoniana,

$$
H(q,p)=U(q)+K(p),
$$

si considerano le equazioni di Hamilton:

$$
\frac{dq}{dt}=\frac{\partial H}{\partial p},
\qquad
\frac{dp}{dt}=-\frac{\partial H}{\partial q}.
$$

Con energia cinetica quadratica,

$$
K(p)=\frac{1}{2}p^T M^{-1}p,
$$

si ottiene

$$
\frac{dq}{dt}=M^{-1}p,
$$

$$
\frac{dp}{dt}=-\nabla U(q).
$$

Questa dinamica usa il gradiente dell'energia potenziale per muovere il punto nello spazio. Invece di proporre un piccolo spostamento casuale, HMC simula un moto deterministico nello spazio esteso $(q,p)$.

## 9.5 Conservazione dell'Hamiltoniana

La dinamica hamiltoniana ideale conserva l'energia totale:

$$
H(q(t),p(t))=\text{costante}.
$$

Questo significa che il sistema può muoversi lungo superfici di energia costante, percorrendo distanze anche grandi senza cadere in regioni di probabilità troppo bassa.

Questa è la ragione intuitiva dell'efficienza di HMC. Il metodo usa il gradiente per costruire traiettorie coerenti con la geometria della distribuzione target. Le proposte possono essere lunghe, ma restano plausibili.

Inoltre, la dinamica hamiltoniana preserva il volume nello spazio delle fasi. Questa proprietà è importante perché consente di usare la dinamica come proposta all'interno di un algoritmo Monte Carlo senza distorcere la distribuzione target. Attenzione però che quando passiamo alla simulazione con passi discreti $\Delta t$ non tutti gli integratori numerici mantengono questa proprietà: gli schemi di integrazione che la preservano si dicono *simplettici*.

## 9.6 L'integratore leapfrog

Nella pratica, le equazioni di Hamilton non sono integrate esattamente. Si usa uno schema numerico, tipicamente il **leapfrog**.

Dato uno stato iniziale $(q,p)$, un passo leapfrog con passo temporale $\epsilon$ è:

$$
p\leftarrow p-\frac{\epsilon}{2}\nabla U(q),
$$

$$
q\leftarrow q+\epsilon M^{-1}p,
$$

$$
p\leftarrow p-\frac{\epsilon}{2}\nabla U(q).
$$

Ripetendo questo passo $L$ volte si ottiene una proposta $(q',p')$.

Il leapfrog è usato perché ha due proprietà importanti:

1. è reversibile;
2. preserva il volume nello spazio delle fasi.

Non conserva esattamente l'Hamiltoniana, ma per passi $\epsilon$ piccoli l'errore resta controllato. Questo errore viene corretto con un passo di accettazione. Notare che nelle simulazioni fisiche di sistemi di particelle in cui $t$ è un tempo "reale" il passo viene indicato con $\Delta t$ piuttosto che con $\epsilon$. 

## 9.7 Accettazione Metropolis

Poiché l'integrazione numerica introduce un errore, la proposta finale non conserva esattamente $H$. Per correggere questo errore si usa una probabilità di accettazione:

$$
\alpha = \min\lbrace\, 1 \,,\, \exp[-H(q',p')+H(q,p)] \,\rbrace.
$$

Se l'Hamiltoniana è quasi conservata, allora

$$
H(q',p')\approx H(q,p),
$$

e la probabilità di accettazione è vicina a uno.

Questo è uno dei vantaggi di HMC: quando l'integrazione è ben calibrata, si ottengono proposte lunghe con alta probabilità di accettazione.

## 9.8 Schema dell'algoritmo HMC

Uno schema essenziale di HMC è il seguente:

```text
scegli uno stato iniziale q
ripeti:
    campiona un momento p da una gaussiana
    simula L passi di dinamica hamiltoniana con leapfrog
    ottieni una proposta (q', p')
    accetta o rifiuta q' con probabilità Metropolis
```

La nuova variabile di momento viene campionata a ogni iterazione, tipicamente da

$$
p\sim \mathcal{N}(0,M).
$$

Questa randomizzazione permette alla catena di esplorare direzioni diverse. La parte hamiltoniana produce invece una proposta guidata dal gradiente.

Il campione finale è la sequenza delle posizioni $q$, mentre i momenti $p$ sono variabili ausiliarie e vengono scartati dopo ogni iterazione.

## 9.9 Scelta dei parametri numerici

HMC richiede alcune scelte pratiche.

Il passo $\epsilon$ controlla la precisione dell'integrazione. Se $\epsilon$ è troppo grande, l'errore sull'Hamiltoniana cresce e molte proposte vengono rifiutate. Se $\epsilon$ è troppo piccolo, le traiettorie sono accurate ma costose.

Il numero di passi $L$ controlla la lunghezza della traiettoria. Se $L$ è troppo piccolo, il metodo si comporta quasi come una dinamica locale. Se $L$ è troppo grande, si spende molto costo computazionale e si può rischiare di percorrere traiettorie inutilmente lunghe.

La matrice di massa $M$ controlla la scala dei momenti e quindi la geometria effettiva del moto. Una scelta adeguata di $M$ può migliorare molto l'efficienza del campionamento, soprattutto quando le variabili hanno scale diverse o sono fortemente correlate.

Queste scelte rendono HMC più complesso da implementare rispetto a metodi più elementari, ma anche molto più efficiente in molti problemi continui ad alta dimensione.

## 9.10 HMC e energy-based models

HMC si inserisce naturalmente nel linguaggio degli energy-based models. Se una distribuzione continua è definita da

$$
p_\theta(q)=\frac{e^{-E_\theta(q)}}{Z_\theta},
$$

possiamo porre

$$
U(q)=E_\theta(q).
$$

Il gradiente

$$
\nabla U(q)=\nabla E_\theta(q)
$$

fornisce l'informazione necessaria per costruire la dinamica hamiltoniana.

Questo è utile quando l'energia è differenziabile rispetto alle variabili continue. In tal caso, HMC permette di campionare dalla distribuzione definita dall'energia senza conoscere esplicitamente $Z_\theta$.

La costante di normalizzazione non compare nel gradiente:

$$
\nabla_q \log p_\theta(q) =
-\nabla_q E_\theta(q),
$$

perché $Z_\theta$ non dipende da $q$.

Questo è uno dei motivi per cui HMC è particolarmente importante nei problemi bayesiani e nei modelli continui: richiede il gradiente della log-densità non normalizzata, non la normalizzazione globale.

## 9.11 Differenza rispetto a Gibbs sampling

Gibbs sampling e HMC affrontano lo stesso problema generale, ma sono adatti a situazioni diverse.

Gibbs sampling è naturale quando:

* le variabili sono discrete o aggiornabili per blocchi;
* le distribuzioni condizionate sono semplici;
* è facile campionare una variabile alla volta dato il resto.

HMC è naturale quando:

* le variabili sono continue;
* la distribuzione è differenziabile;
* il gradiente dell'energia è disponibile;
* aggiornamenti locali casuali sarebbero troppo lenti.

In breve:

$$
\text{Gibbs usa condizionate locali},
\qquad
\text{HMC usa gradienti e dinamica continua}.
$$

Entrambi, però, condividono lo stesso obiettivo: produrre campioni da una distribuzione complessa definita implicitamente.

## 9.12 Limiti di HMC

HMC non è una soluzione universale.

Primo, richiede gradienti. Se l'energia non è differenziabile, oppure se le variabili sono discrete, HMC non si applica direttamente.

Secondo, richiede una buona scelta dei parametri numerici. Passo di integrazione, lunghezza della traiettoria e matrice di massa influenzano fortemente l'efficienza.

Terzo, in distribuzioni con geometria molto complicata, regioni strette, code forti o forti curvature locali, anche HMC può diventare difficile da calibrare.

Infine, ogni passo può essere costoso, perché richiede più valutazioni del gradiente.

Il vantaggio è che, quando applicabile, HMC può produrre campioni molto meno correlati rispetto a una dinamica locale casuale.

## 9.13 Sintesi della sezione

Hamiltonian Monte Carlo è un metodo di campionamento per distribuzioni continue definite tramite una energia potenziale

$$
U(q)=-\log \pi(q)+\text{costante}.
$$

Introduce momenti ausiliari $p$ e una Hamiltoniana

$$
H(q,p)=U(q)+K(p).
$$

La dinamica hamiltoniana propone mosse lunghe guidate dal gradiente di $U(q)$, mentre il passo di accettazione corregge l'errore numerico dell'integrazione.

Il metodo è particolarmente utile quando:

* lo spazio è continuo e ad alta dimensione;
* la distribuzione target è nota a meno di una normalizzazione;
* il gradiente della log-densità non normalizzata è disponibile.

Nel quadro degli energy-based models, HMC mostra che campionare da un'energia non significa necessariamente aggiornare variabili una alla volta. Quando lo spazio è continuo, si può usare la geometria del paesaggio per costruire proposte efficienti.

# 10. Sintesi: ottimizzare, campionare, generare

## 10.1 Tre domande diverse

Una stessa funzione energia può essere usata per formulare tre problemi diversi.

Il primo è un problema di ottimizzazione:

$$
x^\star \in \arg\min_x E(x).
$$

La domanda è:

> qual è la configurazione migliore?

Il secondo è un problema di campionamento:

$$
p(x)=\frac{e^{-E(x)}}{Z}.
$$

La domanda è:

> come posso generare configurazioni con frequenza coerente con questa distribuzione?

Il terzo è un problema di apprendimento generativo:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

La domanda è:

> come devo scegliere i parametri dell'energia perché il modello produca configurazioni simili ai dati?

Queste tre domande sono collegate, ma non coincidono. Cercare il minimo, campionare una distribuzione e apprendere un modello generativo sono operazioni diverse.

## 10.2 Ottimizzare

Ottimizzare significa cercare configurazioni a energia bassa. Il risultato tipico è una soluzione, o un insieme ristretto di soluzioni:

$$
x^\star = \arg\min_x E(x).
$$

Questa lettura è appropriata quando serve una decisione puntuale: scegliere un percorso, stimare un parametro, trovare una configurazione fattibile, minimizzare una loss.

Il rischio è ridurre troppo il problema. Se molte configurazioni sono plausibili o se l'incertezza è importante, un singolo minimo può essere una descrizione insufficiente.

## 10.3 Campionare

Campionare significa produrre configurazioni distribuite secondo una probabilità assegnata. Se la probabilità è definita da un'energia,

$$
p(x)=\frac{e^{-E(x)}}{Z},
$$

allora configurazioni a energia più bassa saranno più frequenti, ma configurazioni ad energia più alta potranno comunque apparire.

Il campionamento non cerca necessariamente la configurazione migliore. Cerca invece di rappresentare l'intera distribuzione.

Questo è importante quando vogliamo stimare medie, incertezze, variabilità, correlazioni o configurazioni tipiche:

$$
\mathbb{E}_p[f(X)] = \sum_x f(x)p(x) \approx \frac{1}{M}\sum_{m=1}^M f(x^{(m)}),
$$

con campioni generati secondo $p$.

Nei modelli discreti, Gibbs sampling aggiorna variabili o blocchi di variabili usando distribuzioni condizionate. Nei modelli continui differenziabili, Hamiltonian Monte Carlo usa gradienti e dinamica ausiliaria per proporre mosse più efficienti.

## 10.4 Generare

Generare significa usare un modello per produrre nuovi esempi plausibili.

Negli energy-based models, il modello non fornisce direttamente una procedura esplicita di generazione. Definisce invece una distribuzione tramite un'energia parametrica:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

Una volta appresa l'energia, generare significa campionare da $p_\theta$.

Questo punto distingue un modello generativo da un semplice ottimizzatore. Un generatore non deve restituire sempre la configurazione più probabile. Deve produrre una varietà di configurazioni coerenti con la distribuzione appresa.

Per questo motivo, apprendimento e campionamento sono strettamente legati. Se non sappiamo campionare dal modello, è difficile usarlo come generatore. Se non sappiamo stimare il comportamento del modello, è difficile apprendere correttamente i parametri.

## 10.5 La funzione di partizione come nodo comune

La funzione di partizione

$$
Z_\theta=\sum_x e^{-E_\theta(x)}
$$

nel caso discreto, oppure

$$
Z_\theta=\int e^{-E_\theta(x)},dx
$$

nel caso continuo, è il nodo comune di molti problemi.

Serve a normalizzare la distribuzione:

$$
p_\theta(x)=\frac{e^{-E_\theta(x)}}{Z_\theta}.
$$

Ma è spesso difficile da calcolare, perché richiede una somma o un integrale su tutto lo spazio delle configurazioni.

Questa difficoltà ha tre conseguenze.

- Primo, rende difficile calcolare probabilità assolute.
- Secondo, rende difficile confrontare modelli tramite likelihood normalizzate.
- Terzo, rende difficile calcolare il gradiente esatto della log-likelihood, perché compare una media rispetto alla distribuzione del modello.

Molti algoritmi nascono per aggirare o approssimare questo problema.

## 10.6 Dati e modello

L'apprendimento di un energy-based model tramite massima likelihood porta al gradiente medio

$$
\frac{1}{n}\nabla_\theta \ell(\theta) =
-\mathbb{E}_{data}\left[\nabla_\theta E_\theta(X)\right]
+ \mathbb{E}_{p_\theta}\left[\nabla_\theta E_\theta(Y)\right].
$$

Questa formula riassume il problema.

Il primo termine guarda i dati e spinge ad abbassarne l'energia. Il secondo guarda ciò che il modello genera e corregge la distribuzione implicita.

In forma concettuale:

$$
\text{apprendimento} = \text{confronto tra dati e modello}.
$$

Se il modello genera configurazioni diverse dai dati, la negative phase produce un segnale di correzione. Se il modello riproduce bene le statistiche rilevanti dei dati, il gradiente tende a ridursi.

## 10.7 Ruolo dei modelli studiati

I modelli e gli algoritmi discussi nella lezione hanno ruoli diversi.

| Oggetto                      | Ruolo concettuale                   | Idea chiave                              |
| ---------------------------- | ----------------------------------- | ---------------------------------------- |
| Energy-based model           | modello probabilistico implicito    | una energia definisce una distribuzione  |
| Hopfield network             | memoria associativa                 | attrattori come pattern memorizzati      |
| Boltzmann Machine            | modello generativo probabilistico   | stati campionati con peso di Boltzmann   |
| Restricted Boltzmann Machine | Boltzmann Machine bipartita         | condizionate semplici e Gibbs a blocchi  |
| Gibbs sampling               | campionamento discreto/condizionato | aggiornare variabili usando condizionate |
| Contrastive divergence       | apprendimento approssimato          | confrontare dati e ricostruzioni brevi   |
| Hamiltonian Monte Carlo      | campionamento continuo              | usare gradienti e dinamica ausiliaria    |

Questa tabella non va letta come una lista di tecniche separate. Sono variazioni su un tema comune: come usare una funzione energia per rappresentare, campionare o apprendere una distribuzione.

## 10.8 Una mappa operativa

Possiamo riassumere il flusso logico così:

```text
funzione energia
      |
      v
pesi non normalizzati
      |
      v
funzione di partizione
      |
      v
distribuzione di probabilità
      |
      +--> campionamento
      |
      +--> apprendimento
      |
      +--> generazione
```

Oppure, in forma matematica:

$$
E_\theta(x)
\quad \longrightarrow \quad
\widetilde p_\theta(x)=e^{-E_\theta(x)}
\quad \longrightarrow \quad
p_\theta(x)=\frac{\widetilde p_\theta(x)}{Z_\theta}.
$$

Una volta definita $p_\theta$, possiamo:

* campionare configurazioni;
* stimare medie e osservabili;
* generare nuovi esempi;
* confrontare il modello con i dati;
* aggiornare i parametri.

## 10.9 Errori concettuali comuni

Ci sono alcune confusioni da evitare.

### Energia bassa non significa probabilità uno

Una configurazione a energia bassa è favorita, ma non necessariamente certa. La probabilità dipende anche dalle altre configurazioni e dalla normalizzazione globale.

### Generare non significa minimizzare

Un modello generativo non deve sempre produrre il minimo dell'energia. Deve produrre campioni con frequenze coerenti con la distribuzione.

### Una probabilità non normalizzata non è ancora una probabilità

Il peso

$$ e^{-E(x)} $$

è positivo e utile, ma diventa probabilità solo dopo divisione per $Z$.

### La funzione di partizione non è un dettaglio tecnico

$Z$ determina la normalizzazione e compare nell'apprendimento. Anche quando si cancella nei rapporti di probabilità, può riapparire nel calcolo della likelihood e del gradiente.

### Una ricostruzione non è un campione indipendente dal modello

Nella contrastive divergence, le configurazioni dopo pochi passi di Gibbs non sono campioni esatti dalla distribuzione del modello. Sono approssimazioni utili, ma vanno interpretate con cautela.

## 10.10 Chiusura

Il punto centrale della lezione è che una funzione energia non serve soltanto a scegliere configurazioni buone. Può diventare il modo con cui definiamo una distribuzione di probabilità.

Questo passaggio cambia la prospettiva.

Nell'ottimizzazione, il paesaggio serve a trovare una configurazione.

Nel campionamento, il paesaggio serve a esplorare una distribuzione.

Nei modelli generativi, il paesaggio viene appreso dai dati per produrre nuove configurazioni plausibili.

La stessa struttura matematica collega quindi tre attività:

$$
\text{ottimizzare},
\qquad
\text{campionare},
\qquad
\text{generare}.
$$

Questa connessione è uno dei motivi per cui gli energy-based models sono un ponte naturale tra meccanica statistica, inferenza, machine learning e modellizzazione computazionale.

# Appendice -- Applicazioni di energy-based models e metodi di campionamento

## 1. Obiettivo dell'appendice

Questa appendice offre una panoramica delle applicazioni dei metodi discussi nella lezione: energy-based models, reti di Hopfield, Boltzmann Machines, Gibbs sampling, contrastive divergence e Hamiltonian Monte Carlo.

L'obiettivo non è fornire una rassegna esaustiva, ma mostrare perché lo stesso formalismo compaia in campi molto diversi. Il punto comune è l'uso di una funzione energia, costo, loss o negative log-probability per assegnare plausibilità alle configurazioni e, quando possibile, generare campioni da una distribuzione.

In molte applicazioni lo schema astratto è:

$$
E(x) \quad \longrightarrow \quad p(x) \propto e^{-E(x)}.
$$

Il significato di $x$ cambia da un campo all'altro. Può essere una configurazione fisica, un'immagine, una sequenza, una rete, un vettore di parametri, una struttura biologica, una scelta collettiva o uno stato latente. La struttura matematica, però, resta simile: configurazioni più compatibili con il modello ricevono energia più bassa e quindi probabilità maggiore.

## 2. Fisica statistica e sistemi complessi

Il contesto originario delle distribuzioni di Boltzmann è la fisica statistica. Qui una configurazione $x$ rappresenta un microstato del sistema, e l'energia $E(x)$ descrive il costo fisico associato a quel microstato.

La distribuzione

$$
p(x)=\frac{e^{-\beta E(x)}}{Z}
$$

rappresenta la probabilità di osservare il sistema in equilibrio termico.

Applicazioni tipiche includono:

* modelli di spin, come Ising e Potts;
* transizioni di fase;
* sistemi magnetici;
* fluidi e materiali complessi;
* vetri di spin e paesaggi energetici frustrati;
* polimeri e macromolecole;
* fenomeni critici e scaling.

In questi problemi il campionamento è spesso necessario perché lo spazio dei microstati è enorme. Metodi Monte Carlo, Gibbs sampling e varianti di Metropolis permettono di stimare medie termodinamiche, correlazioni e proprietà macroscopiche.

Il collegamento con gli energy-based models moderni è concettuale: in entrambi i casi una funzione energia definisce una distribuzione su uno spazio di configurazioni. Cambia l'interpretazione del sistema, ma non il meccanismo matematico di base.

## 3. Machine learning generativo

Nel machine learning, gli energy-based models sono usati per modellare distribuzioni complesse di dati.

Qui $x$ può rappresentare:

* un'immagine;
* una sequenza;
* un vettore di caratteristiche;
* una configurazione binaria;
* una coppia input-output;
* una rappresentazione latente.

L'energia $E_\theta(x)$ viene appresa dai dati. Configurazioni simili a quelle osservate devono ricevere energia bassa; configurazioni implausibili devono ricevere energia alta.

Applicazioni storiche e concettuali includono:

* Boltzmann Machines;
* Restricted Boltzmann Machines;
* Deep Belief Networks;
* modelli generativi su immagini binarie o continue;
* modelli di rappresentazione latente;
* pretraining non supervisionato;
* modellizzazione di distribuzioni multimodali.

Le RBM sono state importanti perché rendono semplici le distribuzioni condizionate tra visibili e nascosti. Questo permette Gibbs sampling a blocchi e procedure di apprendimento approssimato come la contrastive divergence.

Oggi molti modelli generativi moderni usano architetture diverse, ma l'idea energetica resta rilevante: definire una funzione che valuta la plausibilità di una configurazione e usare tale funzione per guidare campionamento, apprendimento o correzione.

## 4. Inferenza bayesiana e statistica computazionale

In inferenza bayesiana, l'obiettivo è campionare dalla distribuzione a posteriori dei parametri:

$$
p(\theta\mid data) \propto p(data\mid \theta)p(\theta).
$$

Prendendo il logaritmo negativo, si ottiene una energia efficace:

$$
U(\theta)=-\log p(data\mid \theta)-\log p(\theta)+\text{costante}.
$$

Campionare dalla posterior diventa quindi equivalente a campionare da

$$
p(\theta\mid data)\propto e^{-U(\theta)}.
$$

Questo è il contesto naturale di Hamiltonian Monte Carlo. HMC è particolarmente utile quando:

* i parametri sono continui;
* la dimensione è alta;
* il gradiente della log-posterior è disponibile;
* la distribuzione è fortemente correlata o non isotropa;
* le stime puntuali non bastano e serve quantificare l'incertezza.

Applicazioni tipiche includono:

* modelli gerarchici bayesiani;
* regressione bayesiana;
* modelli epidemiologici con parametri incerti;
* modelli ecologici;
* modelli econometrici;
* modelli di misura con variabili latenti;
* inferenza in modelli dinamici.

In questo contesto, l'energia non è fisica: è una negative log-posterior. Tuttavia, la struttura matematica è la stessa.

## 5. Neuroscienze, memoria e reti neurali ricorrenti

Le reti di Hopfield sono nate come modello astratto di memoria associativa. Il problema non è generare campioni da una distribuzione, ma recuperare pattern memorizzati a partire da input incompleti o rumorosi.

Applicazioni e interpretazioni includono:

* memoria associativa;
* completamento di pattern;
* correzione di errori;
* modelli semplificati di richiamo mnemonico;
* dinamiche attrattive in reti neurali;
* interpretazione di stati cognitivi come attrattori;
* modelli di decisione collettiva in reti di unità interagenti.

In questi modelli, i pattern memorizzati corrispondono a configurazioni stabili della dinamica. L'energia agisce come funzione di Lyapunov: la dinamica tende a ridurla fino a raggiungere uno stato stabile.

Il valore didattico delle reti di Hopfield è duplice. Da un lato mostrano come una memoria possa essere distribuita nei pesi di interazione. Dall'altro preparano l'idea che un'energia su molte variabili possa organizzare il comportamento collettivo del sistema.

## 6. Ottimizzazione combinatoria e problemi di vincolo

Molti problemi combinatori possono essere formulati assegnando un costo o un'energia a ogni configurazione candidata.

Esempi:

* soddisfacibilità booleana;
* graph colouring;
* travelling salesman problem;
* assegnamento di risorse;
* scheduling;
* routing;
* selezione di sottoinsiemi;
* partizionamento di grafi;
* problemi di matching;
* progettazione di reti.

In questi casi l'energia misura violazioni di vincoli, lunghezza di un percorso, costo operativo, incompatibilità o qualità della soluzione.

L'uso probabilistico dell'energia permette di esplorare configurazioni non ottimali ma informative. Questo è utile quando il minimo globale è difficile da trovare, quando esistono molte soluzioni quasi equivalenti o quando interessa descrivere l'insieme delle soluzioni plausibili.

Metodi come Gibbs sampling, simulated annealing, parallel tempering e altre dinamiche stocastiche possono essere letti come modi diversi di esplorare distribuzioni definite da funzioni di costo.

## 7. Biologia computazionale e bioinformatica

In biologia computazionale, molte strutture possono essere descritte tramite paesaggi di energia o score.

Esempi di configurazioni $x$ includono:

* conformazioni di proteine;
* sequenze biologiche;
* reti regolatorie;
* stati di espressione genica;
* strutture di RNA;
* configurazioni di interazione molecolare;
* alberi o grafi evolutivi.

L'energia o score misura compatibilità strutturale, stabilità, affinità, vincoli funzionali o accordo con dati sperimentali.

Applicazioni tipiche includono:

* predizione di strutture;
* modellizzazione di famiglie di sequenze;
* inferenza di interazioni tra siti;
* campionamento di conformazioni;
* modelli di coevoluzione;
* ricostruzione di reti biologiche;
* analisi di paesaggi adattativi.

In questi problemi è spesso importante non trovare una sola configurazione ottima, ma esplorare un insieme di configurazioni compatibili. Ad esempio, una proteina può avere molte conformazioni accessibili; una famiglia di sequenze può essere descritta da vincoli statistici; una rete biologica può avere molte strutture plausibili date osservazioni rumorose.

## 8. Chimica computazionale e materiali

In chimica e scienza dei materiali, le configurazioni rappresentano posizioni atomiche, stati molecolari, conformazioni o configurazioni cristalline. L'energia può derivare da potenziali empirici, modelli quantistici approssimati o simulazioni più dettagliate.

Applicazioni includono:

* campionamento conformazionale;
* stima di energie libere;
* studio di reazioni chimiche;
* transizioni tra stati metastabili;
* progettazione di materiali;
* analisi di difetti e configurazioni cristalline;
* dinamica molecolare;
* docking molecolare.

In questi contesti la funzione di partizione e la free energy hanno significato fisico diretto. Il campionamento è necessario perché le proprietà osservabili dipendono da insiemi di configurazioni, non da una sola geometria minima.

Hamiltonian Monte Carlo e metodi affini si collegano naturalmente alla dinamica molecolare, anche se gli obiettivi possono essere diversi: in un caso si vuole simulare una dinamica fisica, nell'altro costruire un algoritmo efficiente di campionamento.

## 9. Reti complesse e modelli di grafi

Anche le reti possono essere modellate tramite funzioni energia. In questo caso una configurazione $x$ può essere:

* una rete completa;
* una partizione dei nodi;
* una configurazione di comunità;
* un insieme di archi;
* uno stato dinamico sui nodi;
* una configurazione multilivello o multilayer.

L'energia può misurare:

* distanza da proprietà osservate;
* violazione di vincoli sui gradi;
* modularità negativa;
* costo di connessione;
* incompatibilità tra attributi e legami;
* tensione tra struttura locale e globale.

Applicazioni includono:

* modelli esponenziali di grafi casuali;
* community detection probabilistica;
* inferenza di reti;
* campionamento di ensemble di grafi con vincoli;
* null models per reti;
* ricostruzione di reti parzialmente osservate;
* studio di polarizzazione, clustering e segmentazione.

Il vantaggio del formalismo energetico è che permette di passare da una singola rete osservata a un ensemble di reti plausibili. Questo è importante quando i dati sono incompleti, rumorosi o quando molte strutture diverse sono compatibili con gli stessi vincoli osservati.

## 10. Economia, finanza e scienze sociali

In economia e scienze sociali, le configurazioni possono rappresentare scelte individuali, allocazioni, stati collettivi, strategie, reti di interazione o parametri latenti.

Una funzione energia può essere interpretata come:

* costo;
* disutilità;
* tensione sociale;
* incompatibilità con vincoli;
* negative log-likelihood;
* distanza dai dati;
* rischio o penalizzazione.

Applicazioni possibili includono:

* modelli di scelta discreta;
* modelli di interazione sociale;
* dinamiche di opinione;
* segmentazione di popolazioni;
* inferenza di preferenze latenti;
* allocazione di portafoglio sotto vincoli;
* modelli di rischio;
* simulazioni agent-based calibrate su dati;
* reti economiche e finanziarie.

In questi campi è spesso fuorviante cercare una sola configurazione ottima. I dati sociali ed economici sono eterogenei, rumorosi e spesso compatibili con molte spiegazioni. Una distribuzione su configurazioni può quindi essere più informativa di una soluzione puntuale.

Il formalismo energetico è utile soprattutto quando si vuole combinare vincoli, interazioni e incertezza in un unico quadro probabilistico.

## 11. Linguaggio, sequenze e modelli simbolici

Le sequenze simboliche possono essere trattate come configurazioni discrete.

Esempi:

* sequenze di parole;
* sequenze di caratteri;
* sequenze biologiche;
* sequenze di eventi;
* traiettorie discrete;
* log di attività;
* clickstream;
* successioni di stati sociali o comportamentali.

Un'energia può misurare la non plausibilità di una sequenza: violazioni grammaticali, incompatibilità tra elementi, scarsa coerenza con pattern osservati o distanza da vincoli strutturali.

Applicazioni includono:

* modellizzazione di sequenze;
* completamento di sequenze;
* correzione di errori;
* analisi di anomalie;
* generazione condizionata;
* inferenza di stati latenti;
* modelli di dipendenza tra posizioni.

Anche se oggi molte applicazioni linguistiche usano architetture neurali autoregressive o transformer, il linguaggio energetico resta utile per formulare modelli che assegnano uno score globale a una sequenza, soprattutto quando si vogliono incorporare vincoli espliciti.

## 12. Visione artificiale e ricostruzione di immagini

In visione artificiale, le configurazioni possono essere immagini, segmentazioni, campi di etichette, mappe di profondità o ricostruzioni.

Una funzione energia può combinare:

* fedeltà ai dati osservati;
* regolarità spaziale;
* penalizzazione di discontinuità;
* compatibilità tra pixel vicini;
* vincoli geometrici;
* prior sulle immagini plausibili.

Applicazioni storiche includono:

* denoising;
* inpainting;
* segmentazione;
* stereo vision;
* ricostruzione;
* modelli di Markov random fields;
* classificazione strutturata;
* generazione di immagini.

In questi problemi è naturale interpretare una buona ricostruzione come configurazione a bassa energia. Tuttavia, quando l'osservazione è rumorosa o incompleta, possono esistere molte ricostruzioni plausibili. Una distribuzione energetica permette di rappresentare questa incertezza.

## 13. Diagnostica, anomalie e modelli di plausibilità

Un energy-based model può essere usato anche senza generare campioni perfetti. Poiché assegna un'energia alle configurazioni, può servire come modello di plausibilità.

Configurazioni ad alta energia possono essere interpretate come:

* anomalie;
* osservazioni fuori distribuzione;
* stati incompatibili con i dati storici;
* segnali rari;
* configurazioni da sottoporre ad attenzione.

Applicazioni possibili includono:

* anomaly detection;
* controllo qualità;
* cybersecurity;
* monitoraggio di infrastrutture;
* diagnosi di sistemi complessi;
* rilevazione di pattern atipici in reti o serie temporali;
* identificazione di configurazioni improbabili in dati sociali o economici.

In questi casi, il valore assoluto dell'energia va interpretato con cautela. Spesso è più utile confrontare energie relative, distribuzioni empiriche degli score o deviazioni rispetto a configurazioni tipiche.

## 14. Una tabella riassuntiva

| Campo                | Configurazione $x$          | Energia/costo          | Uso principale                     |
| -------------------- | --------------------------- | ---------------------- | ---------------------------------- |
| Fisica statistica    | microstato                  | energia fisica         | equilibrio, medie, transizioni     |
| Machine learning     | dato o stato latente        | energy/loss            | generazione, rappresentazione      |
| Statistica bayesiana | parametri                   | negative log-posterior | inferenza e incertezza             |
| Neuroscienze         | pattern neurale             | energia attrattiva     | memoria associativa                |
| Ottimizzazione       | soluzione candidata         | costo                  | ricerca di soluzioni               |
| Biologia             | sequenza/conformazione/rete | score o energia        | struttura, funzione, compatibilità |
| Chimica/materiali    | configurazione molecolare   | energia potenziale     | conformazioni, free energy         |
| Reti                 | grafo o partizione          | score negativo         | ensemble, comunità, inferenza      |
| Economia/sociale     | scelta/stato/rete           | disutilità o distanza  | eterogeneità, vincoli, scenari     |
| Visione artificiale  | immagine/segmentazione      | data term + prior      | ricostruzione, denoising           |
| Anomaly detection    | osservazione                | implausibilità         | rilevazione di outlier             |

## 15. Messaggio finale

La stessa forma matematica compare in campi molto diversi perché risponde a un problema generale:

> come assegnare plausibilità a configurazioni complesse quando non possiamo descrivere direttamente tutte le probabilità?

La risposta degli energy-based methods è costruire una funzione energia. Questa funzione può derivare da una teoria fisica, da un modello statistico, da una loss appresa, da vincoli strutturali o da dati empirici.

Una volta definita l'energia, si aprono tre possibilità:

1. cercare configurazioni a bassa energia;
2. campionare configurazioni con probabilità proporzionale a $e^{-E(x)}$;
3. apprendere l'energia dai dati per costruire un modello generativo.

Le applicazioni cambiano, ma il nucleo concettuale resta lo stesso: una funzione energia trasforma un problema di valutazione in un problema probabilistico.
