---
title: "Stabilità numerica e simulazioni affidabili"
author: ""
date: ""
---

# Stabilità numerica e simulazioni affidabili

Una simulazione non è mai esatta: produce un’approssimazione del modello matematico. Tuttavia, se lo schema numerico è stabile, piccoli errori locali non si amplificano e la traiettoria simulata resta “vicina” a quella teorica. Comprendere questo principio è essenziale per costruire modelli affidabili, anche quando non si dispone di una soluzione analitica. Evitare gli errori più comuni nelle simulazioni é fondamentale per progettare esperimenti numerici che diano risultati riproducibili e coerenti con il modello teorico.

### Obiettivi didattici specifici

1. Distinguere tra **errore numerico**, **errore di modellizzazione** e **rumore stocastico**.  
2. Comprendere in modo intuitivo il significato di **stabilità** di un algoritmo di simulazione.  
3. Imparare a scegliere un **passo temporale** appropriato e a verificarne la convergenza empiricamente.  
4. Riconoscere i segnali di instabilità o divergenza nei risultati.  
5. Applicare semplici strategie di controllo dell’errore e di confronto fra schemi numerici.

### Struttura della lezione

La lezione è articolata in cinque parti principali:

1. **Perché serve la stabilità numerica** – differenza fra errore casuale e errore sistematico.  
2. **Tipi di errore nelle simulazioni** – discretizzazione, arrotondamento, accumulo.  
3. **Come testare la stabilità di uno schema** – esempi pratici con simulazioni semplici.  
4. **Scelta del passo temporale e convergenza** – metodo empirico di verifica.  
5. **Esempi interdisciplinari** – modelli sociali, economici e fisici con rumore.

---

## 1. Perché serve la stabilità numerica

In ogni algoritmo iterativo, un piccolo errore introdotto a uno step può crescere nel tempo.  
In simulazioni deterministiche, questo accade quando il modello è rigido o quando il passo temporale utilizzato per integrare un’equazione differenziale è troppo grande; in simulazioni stocastiche, le fluttuazioni casuali possono amplificare l’instabilità numerica.

Esempio intuitivo: consideriamo la dinamica logistica **continua**  
$$\frac{dx}{dt} = r\,x(1 - x),$$  
e la sua discretizzazione tramite Eulero  (i.e. $x_{t+\Delta t} \approx x_t + \frac{dx}{dt}\,\Delta t$)  
$$x_{t+\Delta t} = x_t + r\,x_t(1 - x_t)\,\Delta t.$$  
Scelte troppo grandi di $$\Delta t$$ o valori eccessivi di $$r$$ possono generare oscillazioni spurie o divergenze, non presenti nella soluzione esatta dell’equazione differenziale.

---

### 1.1 Tipi di errore nelle simulazioni

1. **Errore di arrotondamento:** dovuto alla rappresentazione finita dei numeri nel computer.  
2. **Errore di discretizzazione:** deriva dal fatto che si sostituiscono derivate con differenze finite.  
3. **Errore di propagazione:** l’accumulo degli errori di passo porta la simulazione a deviare.  
4. **Errore statistico:** in presenza di rumore, ogni simulazione è una realizzazione diversa del processo.

In pratica, la stabilità significa che l’errore complessivo non cresce senza controllo quando si prosegue la simulazione.

---

### 1.2 Come testare la stabilità di uno schema

Un modo semplice per verificare la stabilità consiste nel simulare lo stesso processo con diversi passi temporali $\Delta t$ e confrontare le traiettorie ottenute. Se la simulazione è stabile, le traiettorie convergono a un comportamento comune.

Ad esempio, consideriamo l’equazione di decadimento esponenziale
$$\frac{dx}{dt} = -x,$$
che ammette la soluzione esatta $x(t) = e^{-t}$.  
La integriamo numericamente con lo schema di Eulero (in questo caso $x_{t+\Delta t} = x_t - x_t\,\Delta t.$) per mostrare come la stabilità dipenda dalla scelta del passo temporale $\Delta t$:

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_decay(dt, N):
    x = np.zeros(N)
    x[0] = 1.0
    for n in range(N-1):
        x[n+1] = x[n] - dt * x[n]  # semplice decadimento
    return x

for dt in [0.1, 0.9, 1.5]:
    N = int(10/dt)                 # simula fino a t=10
    t = np.linspace(0, 10, N)
    plt.plot(t, simulate_decay(dt, N), label=f"dt={dt}")
plt.xlabel("tempo")
plt.ylabel("x(t)")
plt.legend()
plt.show()
```

Un $\Delta t$ troppo grande produce oscillazioni o valori negativi: segno di instabilità.

---

### 1.3. Scelta del passo temporale e convergenza

Non esiste una regola universale, ma si possono seguire alcune linee guida pratiche:

* Ridurre $\Delta t$ fino a che il risultato non cambia più in modo significativo.

* Confrontare la simulazione numerica con un caso analitico semplice, se disponibile.

* Osservare grandezze aggregate (es. medie o varianze) invece delle singole traiettorie.

* Ripetere la simulazione più volte per stimare la variabilità dovuta al rumore.

Il concetto chiave è la **convergenza empirica**: uno schema è accettabile se le sue stime si stabilizzano al diminuire del passo temporale.

***

### 1.4 Esempi interdisciplinari

* **Epidemiologia:** la scelta di un passo temporale troppo grande in un modello SIR può far scomparire o amplificare artificialmente un’epidemia.

* **Economia:** nei modelli di aspettative adattive, una discretizzazione eccessiva può creare cicli spurii.

* **Fisica:** nel moto browniano simulato con un rumore gaussiano, la stabilità determina se l’energia media resta costante o diverge.

* **Social network:** nelle simulazioni agent–based, una dinamica instabile può portare a polarizzazioni artificiali dovute non al modello, ma al numerico.

---

## Diagnostica e misurazione dell’instabilità nelle simulazioni stocastiche

A differenza delle simulazioni deterministiche, dove l’instabilità si manifesta spesso con divergenze numeriche esplicite, nei modelli stocastici l’instabilità può assumere forme più subdole: distribuzioni errate, varianze anomale, drift sistematici o stati fisicamente impossibili. Per questo motivo è necessario disporre di strumenti dedicati alla diagnosi e alla quantificazione dell’instabilità. Questa sezione presenta tecniche operative che permettono di individuare precocemente problemi numerici e di valutarne l’impatto sulla validità statistica della simulazione.

### 1. Controllo di dominio e stati fisicamente impossibili

La verifica più immediata consiste nell’osservare se la simulazione produce stati inammissibili per il modello:

* valori negativi in processi demografici o epidemiologici;
* concentrazioni o probabilità fuori intervallo;
* esplosioni numeriche non previste dal modello teorico.

La presenza anche occasionale di tali valori indica una violazione del dominio ammesso e suggerisce instabilità locale dello schema numerico.

### 2. Confronto con quantità analitiche (medie, varianze, distribuzioni)

Molti modelli stocastici ammettono soluzioni analitiche per alcuni momenti o per la distribuzione in casi limite. Anche quando la soluzione completa non è nota, è spesso disponibile almeno la dinamica della media o della varianza.

Per diagnosticare instabilità si confrontano:

* $\mathbb{E}[X_t]$ simulata vs. teorica;
* $\mathrm{Var}[X_t]$ simulata vs. teorica;
* distribuzioni empiriche vs. distribuzioni note (colonne di Poisson, gamma, lognormale).

Differenze sistematiche crescenti al variare del passo temporale sono segnale di instabilità.

### 3. Analisi di convergenza empirica

Una simulazione stocastica è stabile se i risultati convergono, in senso statistico, al diminuire di $\Delta t$ o del passo di salto. Le tecniche più utilizzate includono:

* **Convergenza forte empirica:** confronto tra traiettorie simulate con passi diversi (ad esempio $\Delta t$ e $\Delta t/2$) e misura dell’errore atteso assoluto.

* **Convergenza debole empirica:** confronto tra le distribuzioni ottenute per passi progressivamente più piccoli, tramite distanza di Kolmogorov o Wasserstein.

* **Step-doubling:** una simulazione con $\Delta t$ viene confrontata con due step consecutivi di $\Delta t/2$. Se i risultati differiscono in modo significativo, lo schema non è stabile o la scelta del passo non è appropriata.

### 4. Replica delle simulazioni e sensibilità al seme

Poiché i modelli stocastici dipendono dal generatore pseudocasuale, è utile diagnosticare instabilità numerica anche tramite replicazioni multiple:

* differenze qualitative tra repliche con lo stesso seme indicano errori numerici;
* differenze anomale tra repliche con semi diversi suggeriscono accumulo di drift numerico o errata rappresentazione delle fluttuazioni.

Una simulazione affidabile deve produrre distribuzioni stabili al variare del seme.

### 5. Monitoraggio della varianza e della crescita del rumore

La varianza numerica è un indicatore particolarmente sensibile dell’instabilità di una SDE o di un processo di salto. Segnali tipici:

* varianza empirica molto maggiore di quella prevista dal modello;
* crescita della varianza più rapida del previsto in sistemi lineari;
* oscillazioni violente dovute a fluttuazioni non fisiche introdotte dallo schema.

Il controllo della varianza permette di identificare errori di discretizzazione che non sono immediatamente visibili nella media.

### 6. Test sugli invarianti del modello

Molti sistemi stocastici possiedono invarianti: massa totale, energia media, distribuzione di equilibrio, momento di ordine zero, o conservazione di un vincolo geometrico.

Una simulazione stabile deve preservare (o approssimare correttamente) tali invarianti.

Esempi:

* per l’equazione di Langevin, l’energia cinetica media deve tendere verso $kT$;  
* per un processo di reazione chiuso, la massa totale deve rimanere costante;  
* per una SDE ergodica, la distribuzione a lungo tempo deve coincidere con quella teorica.

Deviazioni persistenti indicano instabilità numerica o scelta errata del passo temporale.

### 7. Conclusioni operative

La diagnosi dell’instabilità nelle simulazioni stocastiche richiede un approccio
multifattoriale, basato su:

* controllo del dominio e dei vincoli fisici;
* confronto con momenti e distribuzioni teoriche;
* test di convergenza forte e debole;
* replicazioni con semi diversi;
* verifica degli invarianti del modello.

Solo una combinazione coerente di queste tecniche permette di garantire che la simulazione sia non solo numericamente stabile, ma anche statisticamente affidabile e coerente con la dinamica stocastica teorica.

--- 

### 7.6 Stabilità nelle simulazioni Monte Carlo e MCMC

Nelle simulazioni Monte Carlo basate su catene di Markov (MCMC), il concetto di stabilità non è di tipo numerico, poiché non si discretizza un’equazione differenziale. La stabilità riguarda invece la capacità della catena di esplorare correttamente lo spazio degli stati e di convergere alla distribuzione invariante desiderata.

Una catena è considerata stabile se:

* evita stati assorbenti non intenzionali (catene “bloccate” in una regione);
* non presenta autocorrelazione eccessiva fra i campioni;
* ha un tasso di accettazione coerente con la proposta (né troppo alto né troppo basso);
* converge in modo riproducibile al diminuire del burn–in;
* riproduce correttamente le statistiche note della distribuzione target.

Segnali tipici di instabilità includono:

* **mixing lento**, con catena che esplora male lo spazio degli stati;
* **autocorrelazione lunga**, che riduce il numero effettivo di campioni indipendenti;
* **accettanza degenerata**, fino a zero o quasi, nei metodi Metropolis;
* **dipendenza forte dal punto iniziale**, sintomo di mancata convergenza;
* **varianza Monte Carlo sovrastimata o sottostimata**, indice di esplorazione inadeguata.

La diagnostica dell’instabilità nelle MCMC comprende:

* confronto di più catene con inizializzazioni diverse;
* stime del tempo di mescolanza e dell’effettivo numero di campioni indipendenti;
* analisi dell’autocorrelazione e della funzione di autocovarianza;
* misure di distanza fra catene (Gelman–Rubin $\hat{R}$);
* confronto con quantità note (momenti, simmetrie, invarianti della distribuzione).

Una simulazione MCMC stabile deve quindi garantire sia una corretta convergenza all’invariante teorico sia una buona esplorazione statistica dello spazio degli stati.

---

## Best practices per simulazioni stocastiche: checklist operativa

Le simulazioni stocastiche richiedono attenzione sia alla stabilità numerica sia alla riproducibilità statistica. Questa checklist raccoglie le pratiche essenziali che consentono di evitare errori frequenti e di garantire risultati affidabili.

### 1. Struttura del modello e dominio degli stati

- [ ] Verificare se le variabili devono rimanere non negative (popolazioni, densità, concentrazioni) e scegliere schemi che preservino la positività.
- [ ] Identificare eventuali invarianti (massa totale, energia media, distribuzioni di  equilibrio) e controllarli durante la simulazione.
- [ ] Esaminare la presenza di bordi sensibili (ad esempio $x=0$ per processi con $\sqrt{x}$) per scegliere schemi robusti vicino al bordo.

### 2. Scelta del metodo numerico

- [ ] Usare Eulero–Maruyama solo con cautela: evitare diffusione moltiplicativa e regioni vicine al bordo.
- [ ] Preferire Milstein o varianti positive quando è necessaria la conservazione del  dominio.
- [ ] Utilizzare SSA per processi di salto quando è essenziale garantire esattezza e evitare stati negativi.
- [ ] Adottare tau–leaping adattivo, binomiale o con vincoli per controllare variazioni di massa e reazioni consumanti.
- [ ] Nei sistemi stiff, applicare schemi impliciti, semi-impliciti o split-step per ottenere stabilità senza imporre passi eccessivamente piccoli.
  Per MCMC:
- [ ] Verificare che la proposta sia calibrata (ampiezza, direzione, adattività controllata).
- [ ] Assicurarsi che la catena sia ergodica e non presenti stati assorbenti artificiali.
- [ ] Evitare proposte troppo locali (mixing lento) o troppo aggressive (accettanza nulla).

### 3. Scelta e verifica del passo temporale

- [ ] Eseguire test di convergenza empirica riducendo progressivamente $\Delta t$ e verificando che i risultati si stabilizzino.
- [ ] Applicare lo step-doubling (confronto tra $\Delta t$ e due passi di $\Delta t/2$).
- [ ] Monitorare la stabilità della varianza e l’assenza di oscillazioni non fisiche.
- [ ] Utilizzare passi temporali adattivi nei modelli con dinamiche diverse su scale temporali molto differenti.
  Per MCMC: 
- [ ] Regolare l’ampiezza della proposta per ottenere un tasso di accettazione adeguato.
- [ ] Verificare il decadimento dell’autocorrelazione come analogon della “stabilità numerica”.
- [ ] Stimare ESS (Effective Sample Size) per valutare la stabilità statistica della catena.

### 4. Diagnostica statistica

- [ ] Confrontare media, varianza e distribuzioni empiriche con soluzioni analitiche note o casi limite verificabili.

- [ ] Verificare gli invarianti del modello (energia, massa, distribuzione di equilibrio).

- [ ] Controllare la sensibilità al seme pseudocasuale mediante repliche con semi diversi.

- [ ] Identificare eventuali drift sistematici o deviazioni crescenti nel lungo tempo.
  Per MCMC:

- [ ] Confrontare più catene indipendenti (criterio di Gelman–Rubin $\hat{R}$).

- [ ] Analizzare traceplots, autocorrelation plots, e mixing tra regioni dello spazio degli stati.
  
  ### 5. Qualità del generatore pseudocasuale

- [ ] Usare generatori con periodo lungo e buona indipendenza statistica.

- [ ] Controllare che il seeding sia esplicito e documentato.

- [ ] Salvare lo stato del generatore per garantire riproducibilità totale.

### 6. Robustezza computazionale

- [ ] Evitare stati fuori dominio (valori negativi, probabilità oltre 1): se si verificano, adottare schemi correttivi o cambi di variabile.
- [ ] Assicurarsi che i tempi di simulazione non saturino la precisione numerica del formato floating-point.
- [ ] Verificare la stabilità del codice in presenza di valori molto piccoli o molto grandi.

### 7. Documentazione e riproducibilità

- [ ] Salvare tutti i parametri di simulazione, inclusi $\Delta t$, numero di passi, seme del generatore, schema numerico e versione del software.
- [ ] Annotare eventuali warning numerici o condizioni che richiedono attenzione (riduzioni automatiche di $\Delta t$, riflessioni al bordo, correzioni di positività).
- [ ] Creare script che riproducano l’intera pipeline (parametri → simulazione → analisi) senza intervento manuale.

### 8. Verifica finale

- [ ] La simulazione converge all’aumentare della risoluzione temporale?
- [ ] La distribuzione simulata coincide con quella teorica o attesa?
- [ ] Gli invarianti sono rispettati?
- [ ] La riproducibilità è garantita?
  per MCMC:
- [ ] Le catene MCMC convergono alla stessa distribuzione da punti iniziali diversi?
- [ ] L’autocorrelazione è ragionevole e l’ESS non è troppo basso?
- [ ] Il tasso di accettazione è in un intervallo plausibile (p.es. 0.2–0.5 per Metropolis RW)?

Una simulazione stocastica affidabile è quella che soddisfa l’intera checklist.  
L’adozione sistematica di queste norme riduce drasticamente il rischio di artefatti numerici e garantisce risultati solidi dal punto di vista statistico e scientifico.

---

## Riferimenti

* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review, 43(3): 525–546.

* Press, W. H. et al. *Numerical Recipes: The Art of Scientific Computing*, Cambridge University Press.

* Gardiner, C. (2004). *Handbook of Stochastic Methods*, Springer.

* LeVeque, R. J. (2007). *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM.

* Gillespie, D. T. (2000). *The chemical Langevin equation*. J. Chem. Phys. 113(1): 297–306.

---

## Stabilità nei metodi di salto: Gillespie, tau–leaping e problemi pratici

I metodi di salto per processi stocastici discreti, come il metodo di Gillespie (SSA) e i suoi estesi tau–leaping, sono spesso considerati intrinsecamente stabili poiché generano tempi d’attesa esatti e rispettano la struttura del processo di reazione. Tuttavia, nella pratica numerica esistono numerosi meccanismi che possono introdurre instabilità o artefatti statistici se non si adottano adeguate precauzioni. Questa sezione illustra i principali problemi e le tecniche operative per evitarli.

### 1. Stabilità del metodo di Gillespie (SSA)

Il metodo SSA è, per costruzione, esatto: ad ogni passo si campiona il tempo della prossima reazione e il tipo di reazione secondo la distribuzione esponenziale corretta. Non presenta errori di discretizzazione temporale. Tuttavia, alcune fonti di instabilità possono comunque emergere nella pratica:

* **Arrotondamenti numerici sulle propensities:** quando alcune propensities diventano molto piccole, le differenze numeriche possono annullarle artificialmente. Ciò conduce a reazioni “bloccate” o sospese.  
* **Modelli rigidi (stiff):** se sono presenti reazioni molto veloci e molto lente, i tempi d’attesa diventano estremamente piccoli per lunghi intervalli. Il metodo resta esatto, ma il costo computazionale cresce in modo insostenibile, e la simulazione può accumulare errori numerici nella gestione del tempo.  
* **Generatori pseudocasuali inadeguati:** la qualità del generatore influenza direttamente la distribuzione dei tempi d’attesa. Periodi troppo corti o correlazioni interne possono introdurre artefatti nelle statistiche aggregate.

Nei sistemi stiff, la stabilità del SSA non è in discussione, ma è messa in crisi la sua efficienza: una simulazione troppo lenta può portare a errori nella gestione numerica del tempo o della memoria.

### 2. Instabilità nel tau–leaping

Il metodo tau–leaping introduce un passo temporale $\tau$ all’interno del quale si assume che le propensities rimangano quasi costanti. In questo intervallo si campiona il numero di occorrenze di ogni reazione come variabile di Poisson:
$$\Delta R_j \sim \text{Poisson}(a_j(x_t)\,\tau).$$  
Questa approssimazione può essere molto efficiente, ma è sensibile alla scelta di $\tau$ e può introdurre instabilità.

#### Problema 1: stati negativi

Se una reazione consuma un reagente e $\Delta R_j$ è troppo grande, il nuovo stato può diventare negativo:
$$x' = x - \nu_j \Delta R_j < 0.$$
Questo è uno degli errori più comuni del tau–leaping.

**Tecniche per evitarlo:**

* **Tau–leaping con vincoli:** si riduce $\tau$ fino a garantire che la reazione non consumi più di quanto disponibile.  
* **Tau–leaping binomiale:** invece di usare Poisson, si usa una distribuzione binomiale che impone un limite superiore sul numero di reazioni consumanti.  
* **Suddivisione delle reazioni veloci e lente:** se una reazione è molto rapida e può consumare una grande frazione dei reagenti, va trattata separatamente o mantenuta esplicita tramite SSA.[^SSA]

[^SSA] SSA sta per *Stochastic Simulation Algorithm*, ossia il metodo di Gillespie.  
È l’algoritmo esatto per simulare un processo di reazione stocastico: ad ogni passo campiona il tempo della prossima reazione da una distribuzione esponenziale e seleziona quale reazione avviene secondo le propensities correnti. Poiché ogni evento è generato singolarmente, il metodo rispetta perfettamente la struttura del processo e garantisce che non si verifichino stati negativi o salti non fisici.
Quando una reazione è molto veloce o consuma rapidamente i reagenti, mantenerla esplicita tramite SSA significa simularla con il metodo esatto, senza approssimazioni del tipo Poisson o tau–leaping, evitando così instabilità numeriche.

#### Problema 2: variazione eccessiva delle propensities

L’assunzione fondamentale è che le propensities non cambino troppo durante l’intervallo di salto. Se questa ipotesi fallisce, il tau–leaping produce drift sistematico e distribuzioni spurie.

Questo accade tipicamente quando:

* una reazione cambia rapidamente il numero di particelle;  
* si attraversano regioni del dominio dove una propensity passa da piccola a grande;  
* il sistema presenta retroazioni forti (feedback non lineari).

**Tecniche di stabilizzazione:**

* **Tau adattivo:** scegliere $\tau$ come la massima quantità di tempo per cui tutte le propensities cambiano meno di una soglia prefissata.  
* **Step-doubling:** eseguire due passi di lunghezza $\tau/2$ e confrontarli con un passo singolo di lunghezza $\tau$; se differiscono troppo, ridurre $\tau$.

#### Problema 3: sistemi rigidi (stiff)

In presenza di reazioni veloci e lente, anche il tau–leaping si deteriora: le reazioni veloci fanno diventare $\tau$ estremamente piccolo, distruggendo il vantaggio di efficienza.

**Tecnica operativa: implicit tau–leaping**
Si approssimano le propensities nel futuro (formule implicite) per evitare che reazioni veloci schiaccino troppo il passo temporale. Lo schema conserva la stabilità anche quando il sistema è rigido, ma richiede la soluzione di sistemi lineari o non lineari ad ogni passo.

### 3. Diagnostica dell’instabilità nei metodi di salto

Per individuare instabilità:

* Monitorare se qualche stato diventa negativo o assume valori irrealistici.  
* Confrontare le statistiche (medie, varianze) con una simulazione SSA per piccoli sistemi.  
* Eseguire più simulazioni con lo stesso seme e con semi diversi; divergenze qualitative indicano instabilità.  
* Verificare che l’aumento della precisione (riducendo $\tau$) porti alla convergenza empirica della distribuzione.

### 4. Conclusioni operative

I metodi di salto sono potenti e rigorosi, ma richiedono attenzione per evitare errori tipici:

* usare SSA quando possibile;  
* usare tau–leaping solo se si può controllare la variazione delle propensities;  
* garantire la positività degli stati;  
* adottare strategie adattive e confronti regolari con un metodo esatto.

Una gestione corretta di questi aspetti assicura simulazioni stocastiche stabili, efficienti e statisticamente affidabili.

---

## Stabilità nei modelli stocastici

La stabilità numerica nei modelli stocastici presenta caratteristiche proprie, distinte dal caso deterministico. In una simulazione stocastica, l’algoritmo deve riprodurre correttamente non soltanto la traiettoria media del processo, ma anche la struttura delle fluttuazioni, la distribuzione degli stati e la loro evoluzione nel tempo. Per questa ragione, un algoritmo può risultare formalmente corretto nel limite $\Delta t \to 0$ oppure nel limite in cui il numero di eventi tende all’infinito, ma comportarsi in modo del tutto inaffidabile per valori realistici dei parametri numerici. Comprendere tali meccanismi è essenziale per progettare simulazioni riproducibili, prive di artefatti e coerenti con il modello teorico.

### 1. Struttura matematica dei processi stocastici

Un processo stocastico continuo soddisfa, nella sua forma generale, un’equazione differenziale stocastica del tipo
$$dX_t = a(X_t)\,dt + b(X_t)\,dW_t,$$
mentre un processo di salto è descritto da un insieme di reazioni con propensities $a_j(x)$ e incrementi discreti. In entrambi i casi, la stabilità numerica richiede che lo schema di simulazione rispetti proprietà fondamentali del processo, come la positività degli stati, la scala temporale delle fluttuazioni e l’eventuale conservazione della massa. Se tali proprietà vengono violate, gli artefatti numerici si propagano rapidamente e producono distribuzioni spurie o traiettorie non fisicamente significative.

### 2. Perché la stabilità è più delicata rispetto al caso deterministico

Nel caso deterministico, l’errore di discretizzazione si accumula nel tempo ma mantiene una forma relativamente controllabile. Nei modelli stocastici, invece, l’errore numerico interagisce con il rumore stesso, modificandone intensità e struttura. Il termine diffusivo $b(X_t)\,dW_t$ fa sì che un errore del passo temporale si converta immediatamente in un errore di varianza, con conseguenze che non possono essere compensate riducendo il rumore. Inoltre, processi con diffusione moltiplicativa (ad esempio con $b(x) = \sqrt{x}$) diventano sensibili ai bordi del dominio e conducono facilmente a stati negativi se lo schema non è costruito in modo da preservare le proprietà del processo.

Per chiarire questo punto, consideriamo due esempi esplicativi.

**Esempio 1: processo di Feller (o Cox–Ingersoll–Ross)**
$$dX_t = \kappa(\theta - X_t)\,dt + \sigma\sqrt{X_t}\,dW_t.$$
La soluzione teorica garantisce $X_t \ge 0$ per ogni $t$. Tuttavia, se si applica lo schema di Eulero–Maruyama,
$$X_{t+\Delta t} = X_t + \kappa(\theta - X_t)\Delta t + \sigma\sqrt{X_t}\,\sqrt{\Delta t}\,Z,$$
il termine $\sqrt{X_t}$ diventa estremamente piccolo quando $X_t$ si avvicina a $0$, mentre la fluttuazione $\sqrt{\Delta t}\,Z$ rimane dell’ordine di $\sqrt{\Delta t}$. Anche un singolo campione $Z < 0$ di grande modulo può trascinare numericamente $X_{t+\Delta t}$ in valori negativi, che sono matematicamente proibiti dal modello ma permessi dallo schema numerico. Questo è un esempio tipico di instabilità locale dovuta alla diffusione moltiplicativa vicino al bordo.

**Esempio 2: equazione di Langevin per una variabile vincolata**
Consideriamo una dinamica stocastica che rappresenta una quantità sempre positiva, ad esempio la densità di un reagente:
$$dX_t = -\lambda X_t\,dt + \sigma\,dW_t.$$
La soluzione continua permette valori arbitrariamente piccoli, ma non negativi se il modello rappresenta una grandezza fisica. Con lo schema di Eulero,
$$X_{t+\Delta t} = X_t - \lambda X_t\Delta t + \sigma\sqrt{\Delta t}\,Z,$$
la fluttuazione additiva $\sigma\sqrt{\Delta t}\,Z$ non dipende dal valore di $X_t$. Quando $X_t$ è piccolo (ad esempio in fase di estinzione o decadimento), anche una fluttuazione casuale moderata può portare $X_{t+\Delta t}$ sotto zero. Questo effetto è puramente numerico: il modello teorico non prevede variabili negative, ma la discretizzazione sì, se non è stabilizzata.

In entrambi gli esempi, il problema nasce dal fatto che vicino al bordo (ad esempio $X = 0$) la dinamica del modello continuo e quella dello schema numerico hanno scale diverse: la parte deterministica tende a riportare il processo verso il dominio ammesso, mentre il termine stocastico discretizzato può spingerlo fuori. Una simulazione stabile deve quindi preservare la struttura del dominio, introducendo schemi che garantiscano la positività oppure trasformazioni di variabili che rendano la dinamica numericamente robusta.

### 3. Ruolo della scala dei tempi

I modelli stocastici presentano spesso dinamiche con scale temporali molto differenti: reazioni veloci e lente, tassi di decadimento grandi e piccoli, fluttuazioni locali e cambiamenti su larga scala. Uno schema numerico stabile deve essere in grado di rappresentare correttamente tali scale senza introdurre oscillazioni non fisiche o drift sistematici. Ad esempio, nel tau–leaping o nei metodi di Eulero–Maruyama, una scelta eccessiva di $\Delta t$ comporta un errore di ordine superiore nella deriva e un errore moltiplicativo nella diffusione, che alterano in modo permanente la statistica delle traiettorie simulate.

### 4. Stabilità come coerenza statistica

Nel contesto stocastico, la stabilità non coincide con la mera assenza di divergenze numeriche, bensì con la coerenza statistica del risultato. Uno schema è stabile se produce, per passi temporali sufficientemente piccoli, distribuzioni empiriche e momenti che convergono verso quelli previsti dalla teoria. In altre parole, la traiettoria numerica non deve soltanto convergere verso la soluzione attesa del modello continuo, ma deve riprodurre le proprietà probabilistiche del processo: medie, varianze, code della distribuzione e, quando rilevanti, gli invarianti di equilibrio.

### 5. Conseguenze pratiche

La mancanza di stabilità nei modelli stocastici si manifesta in modi caratteristici: la produzione di stati negativi in sistemi demografici o epidemiologici; la crescita artificiale della varianza in simulazioni di Langevin; la distorsione dei tempi d’attesa nei processi di salto; la comparsa di polarizzazioni spurie in modelli agent–based. Una simulazione stocastica instabile può apparire qualitativamente plausibile pur essendo completamente errata dal punto di vista statistico, con conseguenze particolarmente gravi quando i risultati vengono utilizzati per confronti empirici o per scopi predittivi.

---

## Stabilità nelle SDE: Eulero–Maruyama, Milstein, schemi positivi e stiffness

Le equazioni differenziali stocastiche (SDE) descrivono processi in cui la dinamica
deterministica è combinata con un rumore di tipo Wiener. Un modello generale ha la forma
$$dX_t = a(X_t)\,dt + b(X_t)\,dW_t,$$
dove $a(x)$ è il drift e $b(x)$ è l’intensità del rumore. La simulazione numerica richiede
di approssimare l’integrale stocastico e di controllare la stabilità statistica del metodo.
Gli schemi più comuni sono Eulero–Maruyama e Milstein, ma la loro applicabilità dipende
fortemente dalla struttura del modello.

### 1. Metodo di Eulero–Maruyama

Il metodo di Eulero–Maruyama (EM) approssima la dinamica con
$$X_{t+\Delta t} = X_t + a(X_t)\,\Delta t + b(X_t)\sqrt{\Delta t}\,Z,$$
dove $Z\sim N(0,1)$. È il metodo più semplice, ma anche il più fragile dal punto di vista
della stabilità.

**Problemi tipici**

* Stati negativi quando $b(x)$ o $a(x)$ dipendono da $x$ in modo non lineare.
* Drift numerico nel lungo tempo (ad esempio derapata dell’energia in Langevin).
* Errori di varianza: la diffusione viene sovrastimata o sottostimata a seconda di $\Delta t$.
* Scarso comportamento vicino ai bordi del dominio, specialmente in presenza di $\sqrt{x}$.

**Quando è accettabile**

* Diffusione additiva ($b(x)$ costante).  
* Dinamiche lontane dai bordi.  
* Sistemi non rigidi (non stiff).

### 2. Metodo di Milstein

Il metodo di Milstein aggiunge un termine correttivo per la derivata di $b(x)$, ottenendo
un ordine di convergenza più elevato:
$$X_{t+\Delta t} = X_t + a(X_t)\,\Delta t + b(X_t)\sqrt{\Delta t}\,Z

+ \frac12 b(X_t)b'(X_t)(Z^2 - 1)\Delta t.$$

**Vantaggi**

* Migliore accuratezza rispetto a EM.  
* Migliore stabilità quando $b(x)$ varia rapidamente.  
* Riduzione degli errori di varianza.

**Limiti**

* Richiede il calcolo di $b'(x)$ e può essere instabile in prossimità di singolarità o
  di regioni dove $b(x)$ è molto piccolo.

### 3. Schemi positivi

Molti modelli stocastici rappresentano quantità fisiche non negative (densità,
popolazioni, variabili finanziarie). Tuttavia, gli schemi standard possono generare valori
negativi. Per prevenire questo problema sono stati sviluppati schemi “positivi” o
“conservativi”.

**Esempi di tecniche per preservare la positività**

* **Milstein positivo**: variante che applica correzioni quando $X_{t+\Delta t}<0$ o usa
  trasformazioni logaritmiche.  
* **Trasformazioni di variabile**: simulare $Y_t = \log X_t$ quando l’SDE è di tipo
  moltiplicativo, poi ricostruire $X_t = e^{Y_t}$.  
* **Riflessione al bordo**: se $X_t$ rappresenta una quantità fisica con limite inferiore
  $0$, sostituire i valori negativi con il punto di riflessione ($X\mapsto |X|$ o
  $X\mapsto 0$).  
* **Schemi per processi di Feller** (come CIR/Feller Square Root Process), che garantiscono
  la positività tramite aggiornamenti non lineari specializzati.

Queste tecniche evitano che una singola fluttuazione numerica distrugga la validità
fisica della simulazione.

### 4. Stiffness nelle SDE

Un sistema stocastico è stiff quando il drift $a(x)$ contiene scale temporali molto
diverse, oppure quando la diffusione $b(x)$ è forte in alcune regioni e debole in altre.
In tali casi, Eulero–Maruyama diventa inefficiente o del tutto instabile.

**Esempi di stiffness**

* Potenziali ripidi: $a(x) = -V'(x)$ con $V(x)$ molto curvo.  
* Equazioni di Langevin con forte attrito $\gamma$: la scala del moto inerziale è
  molto diversa da quella diffusiva.  
* SDE con crescita esplosiva quando $x$ è grande.

**Conseguenze sulla simulazione**

* Necessità di usare $\Delta t$ molto piccoli per evitare divergenze.  
* Deriva numerica verso regioni non fisiche.  
* Eccessiva amplificazione della diffusione.

### 5. Rimedi per la stiffness

Esistono tecniche efficaci per stabilizzare la simulazione:

* **Schemi semi-impliciti**:
  $$X_{t+\Delta t} = X_t + a(X_{t+\Delta t})\,\Delta t + b(X_t)\sqrt{\Delta t}\,Z.$$
  In questi metodi il drift viene trattato implicitamente mentre il termine stocastico  resta esplicito, con un sensibile miglioramento della stabilità nei sistemi stiff.
  Tuttavia, determinare $X_{t+\Delta t}$ richiede la soluzione di un’equazione (lineare o non lineare a seconda di $a(x)$), introducendo lo stesso tipo di complessità computazionale tipico degli schemi impliciti per equazioni differenziali deterministiche: la maggiore stabilità viene ottenuta al prezzo di un costo numerico più elevato.

* **Split–step methods**: si separano i contributi del drift e della diffusione:
  
  1. si aggiorna il drift con un metodo implicito;  
  2. si aggiunge separatamente il contributo stocastico.

* **Metodi simmetrici o geometrici** per Langevin, come BBK[^BBK] o BAOAB[^BAOAB], che preservano sia l’energia sia la distribuzione di equilibrio. Questi schemi derivano da una discretizzazione strutturata dell’equazione di Langevin, che separa deterministicamente le componenti di drift, dissipazione e rumore. Tale struttura permette di mantenere invarianti geometrici del sistema (ad esempio la simmetria temporale o la misura di equilibrio di Boltzmann) molto meglio dei metodi espliciti classici. Questi schemi sono particolarmente utili quando la simulazione deve rispettare in modo accurato la termodinamica del sistema: riducono la deriva dell’energia, controllano l’effetto cumulato del rumore e preservano la distribuzione in equilibrio senza imporre passi temporali eccessivamente piccoli.

[^BBK]*Nel metodo BBK*, largamente utilizzato in dinamica molecolare, il contributo del rumore e la dissipazione vengono trattati in modo accoppiato, ottenendo una buona conservazione dell’energia e una dinamica più realistica rispetto ai metodi completamente espliciti.

[^BAOAB]*Nel caso del metodo BAOAB*, la dinamica viene scomposta in cinque sotto-passaggi (drift–dissipazione–rumore–dissipazione–drift) disposti in modo simmetrico. Questa simmetria impedisce la deriva numerica dell’energia e garantisce una riproduzione fedele della distribuzione di equilibrio anche per valori relativamente grandi di $\Delta t$.

### 6. Conclusioni operative

Per simulazioni stocastiche stabili:

* evitare Eulero–Maruyama vicino ai bordi o con diffusione moltiplicativa;  
* usare Milstein o varianti positive quando è essenziale mantenere la non negatività;  
* adottare schemi impliciti o split-step nei sistemi stiff;  
* verificare sempre la convergenza empirica al diminuire di $\Delta t$.

Una scelta accorta dello schema numerico è cruciale per ottenere simulazioni di SDE accurate, stabili e statisticamente coerenti.

---

## Appendice 7.D — Stabilità e tuning nelle simulazioni MCMC

Le simulazioni Monte Carlo basate su catene di Markov (MCMC) richiedono un’analisi della
stabilità concettualmente distinta da quella delle SDE e dei processi di salto. Qui non
esistono passi temporali nel senso classico, né problemi di bordi o di discretizzazione.
La “stabilità” riguarda invece la capacità della catena di:

1. esplorare correttamente lo spazio degli stati (mixing);
2. convergere alla distribuzione invariante;
3. produrre campioni statisticamente affidabili con varianza effettiva controllata.

Questa appendice fornisce un insieme di criteri e tecniche pratiche per diagnosticare e
correggere problemi di instabilità nelle catene MCMC.

---

### D.1 Instabilità tipiche nelle catene MCMC

Le situazioni più comuni che indicano instabilità o inefficienza sono:

* **Mixing lento**: la catena rimane intrappolata a lungo in una regione dello spazio.
* **Accettanza degenerata**: troppo bassa (catena bloccata) o troppo alta (proposte
  troppo piccole).
* **Autocorrelazione elevata**: pochi campioni effettivamente indipendenti.
* **Dipendenza forte dal punto iniziale**: la catena non raggiunge l’invariante.
* **Burn–in insufficiente o eccessivo**: stadi transitori non eliminati oppure
  eliminati inutilmente.
* **Esplorazione anisotropa**: in alta dimensione la catena si muove bene lungo alcuni
  assi e malissimo lungo altri.

La stabilità algoritmica riguarda quindi principalmente l’**ergodicità** e la qualità
dell’esplorazione dello spazio degli stati.

---

### D.2 Tasso di accettazione ottimale

Una diagnosi immediata dell’instabilità nei metodi di Metropolis è il **tasso di
accettazione**, cioè la frazione di proposte accettate. Valori non appropriati indicano
instabilità statistica:

* **accettanza troppo bassa (< 10%)**: proposte troppo “aggressive”, catena bloccata;
* **accettanza troppo alta (> 70%)**: proposte troppo piccole, esplorazione lenta.

Risultati classici indicano valori ottimali approssimativi:

* **Metropolis random-walk in bassa dimensione**: circa $$0.44$$;
* **Metropolis random-walk in alta dimensione**: circa $$0.234$$;
* **Metropolis adattivo ben calibrato**: valori intermedi.

Questi risultati, seppur asintotici, offrono una guida robusta per evitare instabilità.

---

### D.3 Autocorrelazione e Effective Sample Size (ESS)

L’autocorrelazione fra campioni successivi è un indicatore fondamentale di stabilità
statistica. Una catena con autocorrelazione elevata produce molti campioni ma pochissima
informazione indipendente.

L’**Effective Sample Size (ESS)** quantifica il numero di campioni realmente utili:
$$\mathrm{ESS} \approx \frac{N}{1 + 2 \sum_{k\ge1} \rho(k)},$$
dove $$\rho(k)$$ è la funzione di autocorrelazione al lag $$k$$.

* **ESS basso** → catena instabile o mal calibrata.
* **ESS elevato** → campioni informativi e catena ben mescolata.

Monitorare l’ESS è essenziale per valutare la stabilità pratica della simulazione.

---

### D.4 Diagnostica multi–catena

Per valutare la convergenza e la stabilità, è utile confrontare più catene indipendenti:

* inizializzate in punti diversi dello spazio degli stati;
* generate con semi pseudocasuali differenti;
* confrontate tramite statistiche aggregate (medie, varianze);
* confrontate tramite distanze fra distribuzioni empiriche.

Un criterio standard è la statistica di Gelman–Rubin,
$$\hat{R},$$
che confronta varianza intra-catena e inter-catena. Valori $$\hat{R} \approx 1$$ indicano
stabilità e convergenza; valori significativamente maggiori suggeriscono instabilità.

---

### D.5 Tuning delle proposte: scale e direzioni

Molti problemi di instabilità nascono da proposte mal calibrate.

**Fattori critici**

* **Ampiezza**: passi troppo piccoli → mixing lento; troppo grandi → troppi rifiuti.
* **Orientamento**: in alta dimensione, una proposta isotropa è inefficiente.
* **Regolazione automatica**: l’adattività deve essere controllata e teoricamente
  giustificata per non violare la convergenza della catena.

Tecniche tipiche per migliorare la stabilità:

* scalare la matrice di covarianza della proposta in base alle correlazioni osservate;
* adottare proposte anisotrope;
* utilizzare Metropolis adattivo con criteri conservativi di aggiornamento.

---

### D.6 Rimedi strutturali per migliorare la stabilità

In presenza di instabilità persistente, è possibile adottare strategie più avanzate:

* **Parallel tempering**: più catene a temperature diverse scambiano stati, migliorando
  l’esplorazione in spazi multimodali.
* **Overrelaxation**: riduce autocorrelazione alternando mosse correlate.
* **Hamiltonian Monte Carlo (HMC)**: sfrutta dinamica quasi deterministica per superare
  barriere energetiche, migliorando stabilità e mixing.
* **Gibbs sampling bloccato**: raggruppare variabili fortemente correlate evita catene
  degeneri.

Queste tecniche aumentano la stabilità algoritmica, specialmente in alta dimensione o in
spazi multimodali.

---

### D.7 Segnali grafici per diagnosticare instabilità

Strumenti visuali indispensabili:

* **trace plot**: una catena stabile deve oscillare liberamente nella regione target;
* **autocorrelation plot**: il decadimento deve essere rapido;
* **histogrammi marginali**: confronti fra catene diverse rivelano differenze sospette;
* **scatter plot** delle variabili correlate: mostra problemi di esplorazione anisotropa.

Visualizzazioni incoerenti rivelano immediatamente problemi di instabilità o di mancata
convergenza.

---

### D.8 Conclusioni operative

Una simulazione MCMC è considerata stabile quando:

* ha un tasso di accettazione ragionevole;
* mostra mixing adeguato e autocorrelazione moderata;
* produce un ESS sufficientemente elevato;
* converge in modo coerente da inizializzazioni diverse;
* rispetta proprietà analitiche note della distribuzione target;
* presenta indicatori grafici chiari e coerenti.

Questa appendice fornisce quindi un quadro operativo per garantire che le simulazioni
MCMC siano non solo formalmente corrette, ma anche statisticamente solide e
scientificamente affidabili.

---