---
title: "LAB08: Analisi di serie stocastiche: ARMA, ARCH e GARCH"
author: ""
date: ""
---

# Obiettivi

In questo laboratorio analizziamo serie temporali sintetiche generate da modelli stocastici discreti nel tempo.

L'obiettivo non è soltanto stimare parametri, ma imparare a costruire una procedura completa di analisi:

1. osservare una serie temporale;
2. distinguere memoria nella media e memoria nella varianza;
3. usare ACF, PACF, istogrammi e QQ-plot come strumenti diagnostici;
4. stimare modelli ARMA gaussiani tramite massima likelihood;
5. stimare modelli ARCH e GARCH gaussiani tramite massima likelihood;
6. analizzare i residui e i residui standardizzati;
7. decidere se il modello stimato ha davvero assorbito la struttura temporale dei dati.

Il laboratorio usa dati sintetici. Questo significa che le serie sono state generate da modelli noti, ma il modello generatore non viene indicato nei file dati. Il compito è ricostruire, tramite diagnostica e stima, quale classe di modello sia più plausibile.

# Il contesto

Una serie temporale non è una semplice lista di numeri. L'ordine delle osservazioni contiene informazione.

Una sequenza

$$
X_0,X_1,\dots,X_T
$$

può avere:

- dipendenza nei valori, cioè memoria nella media;
- dipendenza nei quadrati, cioè memoria nella scala delle fluttuazioni;
- distribuzione marginale non gaussiana;
- outlier o code pesanti;
- periodi tranquilli alternati a periodi turbolenti.

In questo laboratorio ci concentriamo su due famiglie principali di modelli.

La prima famiglia è quella dei modelli ARMA. Questi modelli cercano di descrivere la parte prevedibile della media condizionata:

$$
\mathbb{E}[X_t\mid\mathcal{F}_{t-1}].
$$

La seconda famiglia è quella dei modelli ARCH/GARCH. Questi modelli cercano di descrivere la varianza condizionata:

$$
\mathrm{Var}(X_t\mid\mathcal{F}_{t-1})=\sigma_t^2.
$$

Il punto concettuale più importante è il seguente:

> una serie può avere autocorrelazione quasi nulla nei valori, ma forte autocorrelazione nei quadrati.

In questo caso un modello ARMA può non essere sufficiente, mentre un modello ARCH/GARCH può catturare la dipendenza residua nella volatilità.

# Organizzazione dei file

La cartella del laboratorio è organizzata così:

```text
Lab08/
|-- data/
|   |-- serie_01.csv
|   |-- serie_02.csv
|   |-- serie_03.csv
|   |-- serie_04.csv
|   |-- serie_05.csv
|   |-- serie_06.csv
|   |-- serie_07.csv
|   |-- serie_08.csv
|   `-- soluzioni_generative.csv
|-- diagnostics.py
|-- figures/
|   |-- serie_01.png
|   |-- serie_02.png
|   |-- serie_03.png
|   |-- serie_04.png
|   |-- serie_05.png
|   |-- serie_06.png
|   |-- serie_07.png
|   `-- serie_08.png
|-- fit_models.py
|-- main.py
|-- requirements.txt
`-- output/                 # creata automaticamente quando si esegue main.py
```

I file `serie_01.csv`, ..., `serie_08.csv` contengono le serie da analizzare.

Ogni file ha due colonne:

```text
t,x
0,...
1,...
2,...
...
```

La colonna `t` contiene l'indice temporale. La colonna `x` contiene il valore osservato.

La cartella `figures/` contiene grafici rapidi delle serie, generati al momento della costruzione dei dati. Queste figure sono utili per un controllo visivo iniziale, ma l'analisi vera e propria deve essere fatta con `main.py`, che produce le figure diagnostiche nella cartella `output/`.

Il file `data/soluzioni_generative.csv` contiene il modello generatore e i parametri delle serie. È una chiave per il docente e non dovrebbe essere usato dagli studenti durante l'analisi.

La cartella `output/` non è necessariamente presente all'inizio. Viene creata automaticamente dallo script quando si esegue `main.py`.

# Dipendenze Python

Per il laboratorio usiamo solo librerie standard per calcolo scientifico e ottimizzazione numerica:

```text
numpy
pandas
matplotlib
scipy
```

Il file `requirements.txt` deve contenere:

```text
numpy
pandas
matplotlib
scipy
```

Installazione:

```bash
pip install -r requirements.txt
```

oppure:

```bash
pip install numpy pandas matplotlib scipy
```

Non usiamo librerie specializzate come `statsmodels` o `arch` nel codice operativo del laboratorio. Esistono librerie professionali per stimare ARMA e GARCH, ma qui vogliamo vedere esplicitamente cosa viene calcolato: residui, varianze condizionate e log-likelihood.

# Come eseguire il laboratorio

Aprire un terminale nella cartella `Lab08/`, cioè nella cartella che contiene `main.py`, `fit_models.py` e `diagnostics.py`.

Eseguire:

```bash
python main.py
```

Nel file `main.py` si scelgono la serie da analizzare e la cartella di output:

```python
DATA_FILE = "data/serie_01.csv"
OUTPUT_DIR = "output/serie_01"
```

Si sceglie anche il modello ARMA da provare:

```python
ARMA_P = 1
ARMA_Q = 0
```

Per analizzare un'altra serie, modificare ad esempio:

```python
DATA_FILE = "data/serie_04.csv"
OUTPUT_DIR = "output/serie_04"
```

L'esecuzione produce figure e report nella cartella indicata da `OUTPUT_DIR`. Ad esempio, se `OUTPUT_DIR = "output/serie_01"`, lo script crea una cartella `output/serie_01/` con grafici e file di testo.

# Due tipi di diagnostica

È importante distinguere due passaggi diversi.

La diagnostica della serie osservata si fa una sola volta. Serve a capire quali strutture sono presenti nei dati:

- grafico della serie;
- istogramma;
- QQ-plot;
- ACF;
- PACF;
- ACF dei quadrati.

La diagnostica dei residui si fa invece dopo aver stimato un modello. Modelli diversi producono residui diversi, quindi è naturale confrontare i residui di ARMA, ARCH e GARCH.

Per i modelli ARCH/GARCH si guardano in particolare i residui standardizzati:

$$
z_t=\frac{\hat\varepsilon_t}{\hat\sigma_t}.
$$

Se il modello ha descritto bene la varianza condizionata, questi residui standardizzati dovrebbero somigliare a rumore bianco gaussiano.

Con la versione corrente del codice, una cartella di output tipica contiene:

```text
output/
`-- serie_01/
    |-- arch_standardized_acf_residui.png
    |-- arch_standardized_acf_residui_quadrati.png
    |-- arch_standardized_istogramma.png
    |-- arch_standardized_qqplot.png
    |-- arch_standardized_report.txt
    |-- arch_standardized_residui.png
    |-- arma_acf_residui.png
    |-- arma_acf_residui_quadrati.png
    |-- arma_istogramma.png
    |-- arma_qqplot.png
    |-- arma_report.txt
    |-- arma_residui.png
    |-- garch_standardized_acf_residui.png
    |-- garch_standardized_acf_residui_quadrati.png
    |-- garch_standardized_istogramma.png
    |-- garch_standardized_qqplot.png
    |-- garch_standardized_report.txt
    |-- garch_standardized_residui.png
    |-- raw_acf.png
    |-- raw_acf_quadrati.png
    |-- raw_istogramma.png
    |-- raw_pacf.png
    |-- raw_qqplot.png
    `-- raw_serie.png
```

# Modelli considerati

## Rumore bianco gaussiano

Il modello più semplice è

$$
X_t=\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal{N}(0,\sigma^2),
$$

con innovazioni indipendenti.

In questo caso ci aspettiamo:

- media circa nulla;
- varianza circa costante;
- ACF compatibile con zero;
- PACF compatibile con zero;
- ACF dei quadrati compatibile con zero;
- QQ-plot circa lineare se l'ipotesi gaussiana è plausibile.

## AR(1)

Un modello autoregressivo di ordine 1 è

$$
X_t=c+\phi X_{t-1}+\varepsilon_t,
\qquad
\varepsilon_t\sim\mathcal{N}(0,\sigma^2).
$$

Se $|\phi|<1$, il processo è stazionario.

Interpretazione:

- se $\phi>0$, valori positivi tendono a essere seguiti da valori positivi;
- se $\phi<0$, la serie tende ad alternare segno;
- se $|\phi|$ è vicino a 1, la memoria decade lentamente.

Per un AR(1) stazionario ci aspettiamo una ACF che decade approssimativamente come

$$
\rho(k)=\phi^k.
$$

## AR(p)

Un modello autoregressivo più generale è

$$
X_t=c+\phi_1X_{t-1}+\phi_2X_{t-2}+\dots+\phi_pX_{t-p}+\varepsilon_t.
$$

Qui la memoria della media è distribuita su più ritardi.

Può produrre:

- persistenza lenta;
- oscillazioni smorzate;
- forme di autocorrelazione più ricche rispetto ad AR(1).

## MA(1)

Un modello a media mobile di ordine 1 è

$$
X_t=\varepsilon_t+\theta\varepsilon_{t-1}.
$$

La differenza importante rispetto ad AR(1) è che nei modelli MA gli shock passati non sono osservati direttamente. Devono essere ricostruiti durante la stima.

Per un MA(1) ideale, l'ACF si tronca dopo il primo lag.

## ARMA(p,q)

Il modello ARMA combina memoria dei valori e memoria degli shock:

$$
X_t=c+
\sum_{i=1}^{p}\phi_iX_{t-i}
+
\varepsilon_t+
\sum_{j=1}^{q}\theta_j\varepsilon_{t-j}.
$$

Un modello ARMA descrive dipendenza lineare nella media. Dopo la stima, i residui dovrebbero assomigliare a rumore bianco.

## ARCH(1)

Un modello ARCH(1) descrive memoria nella varianza condizionata:

$$
X_t=\mu+\varepsilon_t,
\qquad
\varepsilon_t=\sigma_t z_t,
\qquad
z_t\sim\mathcal{N}(0,1),
$$

con

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2.
$$

Se lo shock precedente è grande in valore assoluto, la varianza condizionata successiva aumenta.

## GARCH(1,1)

Un modello GARCH(1,1) aggiunge persistenza della volatilità:

$$
X_t=\mu+\varepsilon_t,
\qquad
\varepsilon_t=\sigma_tz_t,
\qquad
z_t\sim\mathcal{N}(0,1),
$$

con

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2.
$$

La quantità

$$
\alpha+\beta
$$

misura la persistenza della volatilità. Se è vicina a 1, gli shock alla volatilità decadono lentamente.

# Parte 1 -- Esplorazione preliminare

## 1.1 Scegliere una serie

Aprire `main.py` e scegliere una serie, per esempio:

```python
DATA_FILE = "data/serie_01.csv"
OUTPUT_DIR = "output/serie_01"
```

Eseguire:

```bash
python main.py
```

Osservare i file prodotti in `output/serie_01/`.

## 1.2 Guardare la serie nel tempo

Aprire il grafico della serie osservata:

```text
raw_serie.png
```

Domande:

1. La serie sembra oscillare attorno a una media stabile?
2. La scala delle fluttuazioni sembra costante?
3. Si vedono cluster di ampiezza, cioè periodi tranquilli e periodi turbolenti?
4. Ci sono valori estremi isolati?
5. La serie sembra avere alternanza di segno?

## 1.3 Istogramma e QQ-plot

Aprire l'istogramma e il QQ-plot della serie osservata:

```text
raw_istogramma.png
raw_qqplot.png
```

Domande:

1. L'istogramma è approssimativamente simmetrico?
2. La gaussiana sovrapposta descrive bene il centro della distribuzione?
3. Le code sembrano più pesanti di una gaussiana?
4. Nel QQ-plot i punti seguono la diagonale?
5. Le deviazioni, se presenti, sono al centro o nelle code?

# Parte 2 -- ACF, PACF e memoria temporale

## 2.1 ACF della serie

Aprire l'ACF della serie osservata:

```text
raw_acf.png
```

L'ACF misura la correlazione tra $X_t$ e $X_{t+k}$.

Domande:

1. L'ACF è compatibile con zero per tutti i lag?
2. Decade lentamente?
3. Alterna segno?
4. Ha un picco forte solo al primo lag?
5. Sembra più compatibile con un modello AR o MA?

## 2.2 PACF della serie

Aprire la PACF della serie osservata:

```text
raw_pacf.png
```

La PACF misura la correlazione al lag $k$ dopo aver rimosso l'effetto dei lag intermedi.

Regole diagnostiche orientative:

- AR(1): PACF significativa al lag 1, poi circa nulla;
- AR(p): PACF significativa fino al lag $p$, poi circa nulla;
- MA(q): ACF significativa fino al lag $q$, PACF che decade;
- ARMA(p,q): ACF e PACF spesso decadono entrambe.

Queste non sono regole assolute, ma aiutano a proporre modelli candidati.

## 2.3 ACF dei quadrati

Aprire l'ACF dei quadrati:

```text
raw_acf_quadrati.png
```

Questa figura è fondamentale per diagnosticare volatilità condizionata.

Domande:

1. I valori $X_t$ hanno autocorrelazione?
2. I quadrati $X_t^2$ hanno autocorrelazione?
3. Se l'ACF di $X_t$ è quasi nulla ma quella di $X_t^2$ è significativa, che cosa suggerisce?
4. La serie sembra più adatta a un modello ARMA o a un modello ARCH/GARCH?

# Parte 3 -- Fit ARMA gaussiano

## 3.1 Scegliere un modello ARMA

Nel file `main.py`, modificare:

```python
ARMA_P = 1
ARMA_Q = 0
```

Esempi:

```python
# AR(1)
ARMA_P = 1
ARMA_Q = 0

# MA(1)
ARMA_P = 0
ARMA_Q = 1

# ARMA(1,1)
ARMA_P = 1
ARMA_Q = 1

# AR(2)
ARMA_P = 2
ARMA_Q = 0
```

Eseguire di nuovo:

```bash
python main.py
```

## 3.2 Leggere i parametri stimati

Nel terminale comparirà un report simile a:

```text
ARMA(1,0) gaussiano
convergenza: True
log-likelihood: ...
constant = ...
phi_1 = ...
sigma = ...
```

La log-likelihood misura quanto i dati osservati sono plausibili sotto il modello stimato. A parità di dati, una log-likelihood più alta indica un fit migliore, ma non basta da sola per scegliere sempre il modello: modelli più complessi tendono spesso a migliorare il fit anche quando aggiungono parametri non realmente necessari.

Domande:

1. L'ottimizzazione è convergente?
2. I parametri stimati hanno segno e ordine di grandezza plausibili?
3. Se il modello è AR(1), il coefficiente $\phi_1$ è positivo o negativo?
4. Se $|\phi_1|$ è vicino a 1, che cosa significa?
5. I residui migliorano passando da un modello più semplice a uno più complesso?

## 3.3 Residui ARMA

Dopo il fit ARMA, vengono prodotti file dei residui:

```text
arma_residui.png
arma_istogramma.png
arma_qqplot.png
arma_acf_residui.png
arma_acf_residui_quadrati.png
arma_report.txt
```

Queste figure non sono una seconda diagnostica della serie originale: sono una diagnostica dei residui prodotti dal modello ARMA.

I residui ARMA sono

$$
\hat\varepsilon_t=X_t-\widehat{\mathbb{E}}[X_t\mid\mathcal{F}_{t-1}].
$$

Domande:

1. I residui hanno media circa zero?
2. L'ACF dei residui è compatibile con rumore bianco?
3. L'ACF dei residui quadrati è compatibile con rumore bianco?
4. Il QQ-plot dei residui è vicino alla diagonale?
5. Se i residui quadrati sono autocorrelati, cosa manca al modello ARMA?

# Parte 4 -- Fit ARCH(1)

## 4.1 Quando ha senso provare ARCH?

Un modello ARCH ha senso quando:

- la serie non mostra forte autocorrelazione nei valori;
- ma mostra autocorrelazione nei quadrati;
- la traiettoria presenta cluster di volatilità;
- ci sono periodi di fluttuazioni piccole alternati a periodi di fluttuazioni grandi.

Il modello ARCH(1) stimato dal codice è

$$
X_t=\mu+\varepsilon_t,
\qquad
\varepsilon_t=\sigma_tz_t,
\qquad
z_t\sim\mathcal{N}(0,1),
$$

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2.
$$

## 4.2 Leggere i parametri ARCH

Il report contiene:

```text
ARCH(1) gaussiano
mu = ...
omega = ...
alpha = ...
```

Domande:

1. $\alpha$ è vicino a zero oppure grande?
2. Se $\alpha$ è grande, che cosa significa?
3. Il modello ARCH migliora la diagnostica dei residui quadrati?
4. I residui standardizzati sembrano più vicini a rumore bianco?

## 4.3 Residui standardizzati

Per ARCH e GARCH non basta guardare i residui grezzi. Bisogna guardare i residui standardizzati:

$$
z_t=\frac{\hat\varepsilon_t}{\hat\sigma_t}.
$$

Se il modello della varianza condizionata è adeguato, allora $z_t$ dovrebbe assomigliare a rumore bianco gaussiano con varianza circa 1.

Domande:

1. L'ACF di $z_t$ è circa nulla?
2. L'ACF di $z_t^2$ è circa nulla?
3. Il QQ-plot di $z_t$ è circa gaussiano?
4. La varianza campionaria di $z_t$ è vicina a 1?

# Parte 5 -- Fit GARCH(1,1)

## 5.1 Modello

Il modello GARCH(1,1) è

$$
X_t=\mu+\varepsilon_t,
\qquad
\varepsilon_t=\sigma_tz_t,
\qquad
z_t\sim\mathcal{N}(0,1),
$$

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2.
$$

Rispetto ad ARCH(1), il GARCH(1,1) aggiunge il termine $\beta\sigma_{t-1}^2$, che produce persistenza della volatilità.

## 5.2 Leggere i parametri GARCH

Il report contiene:

```text
GARCH(1,1) gaussiano
mu = ...
omega = ...
alpha = ...
beta = ...
alpha + beta = ...
```

Domande:

1. $\alpha$ è grande o piccolo?
2. $\beta$ è grande o piccolo?
3. Quanto vale $\alpha+\beta$?
4. Se $\alpha+\beta$ è vicino a 1, cosa significa?
5. Il GARCH migliora rispetto ad ARCH nella diagnostica dei residui quadrati?

## 5.3 Confronto ARCH/GARCH

Confrontare:

- log-likelihood;
- interpretazione dei parametri;
- ACF dei residui standardizzati;
- ACF dei quadrati dei residui standardizzati;
- QQ-plot.

Domande:

1. GARCH ha likelihood maggiore di ARCH?
2. La maggiore flessibilità del GARCH migliora anche i residui standardizzati?
3. Restano tracce di struttura nei residui?
4. La maggiore complessità del GARCH è giustificata dalla diagnostica?

# Parte 6 -- Analisi di tutte le serie

Ripetere la pipeline per tutte le serie disponibili:

```text
serie_01.csv
serie_02.csv
serie_03.csv
serie_04.csv
serie_05.csv
serie_06.csv
serie_07.csv
serie_08.csv
```

Per ciascuna serie, compilare una tabella del tipo:

| serie | ACF valori | PACF valori | ACF quadrati | modello candidato | modello stimato | residui ok? |
|---|---|---|---|---|---|---|
| 01 | ... | ... | ... | ... | ... | ... |
| 02 | ... | ... | ... | ... | ... | ... |
| 03 | ... | ... | ... | ... | ... | ... |
| 04 | ... | ... | ... | ... | ... | ... |
| 05 | ... | ... | ... | ... | ... | ... |
| 06 | ... | ... | ... | ... | ... | ... |
| 07 | ... | ... | ... | ... | ... | ... |
| 08 | ... | ... | ... | ... | ... | ... |

Le serie non devono essere identificate solo guardando i parametri stimati. La diagnosi deve partire dai grafici e dai residui.

# Parte 7 -- Confronto tra modelli

Per almeno due serie, confrontare esplicitamente tre modelli:

1. ARMA semplice;
2. ARCH(1);
3. GARCH(1,1).

Per ciascun modello riportare:

- log-likelihood;
- interpretazione dei parametri;
- diagnostica dei residui.

Domande:

1. Quale modello produce residui più simili a rumore bianco?
2. Quale modello riduce meglio l'autocorrelazione dei quadrati dei residui?
3. Il modello con likelihood più alta ha anche residui migliori?
4. Se likelihood e diagnostica visuale non concordano, quale criterio considerate più importante?
5. Il modello più complesso è sempre preferibile?

# Parte 8 -- Caso volutamente difficile

Una delle serie può essere stata generata da un modello che non appartiene esattamente alle classi ARMA, ARCH o GARCH simmetrico standard.

Il vostro compito non è necessariamente trovare il modello vero, ma riconoscere che il modello stimato lascia una struttura non spiegata.

Segnali possibili:

- residui standardizzati con asimmetria;
- QQ-plot non lineare nelle code;
- ACF dei quadrati ancora significativa;
- parametri instabili o poco plausibili;
- modello GARCH che cattura parte della volatilità ma non tutta.

Domande:

1. Quale serie sembra più difficile da descrivere con i modelli disponibili?
2. Quale diagnostica lo mostra meglio?
3. Che tipo di estensione del modello sarebbe utile?
4. Servirebbe una volatilità asimmetrica?
5. Servirebbe un cambio di regime?

# Relazione finale

Consegnare una breve relazione, non un elenco di grafici.

La relazione deve contenere:

1. una descrizione della procedura usata;
2. una tabella riassuntiva per tutte le serie;
3. un'analisi dettagliata di almeno due serie;
4. il confronto fra ARMA, ARCH e GARCH dove appropriato;
5. una discussione dei residui;
6. una conclusione critica.

## Struttura suggerita

```text
1. Introduzione
   - Obiettivo del laboratorio.
   - Differenza tra memoria nella media e memoria nella varianza.

2. Metodi
   - ACF, PACF, QQ-plot.
   - Fit ARMA.
   - Fit ARCH/GARCH.
   - Diagnostica dei residui.

3. Risultati sintetici
   - Tabella per tutte le serie.

4. Analisi dettagliata
   - Serie scelta 1.
   - Serie scelta 2.

5. Discussione
   - Quali modelli funzionano bene?
   - Dove falliscono?
   - Che cosa mostrano i residui?

6. Conclusioni
   - Messaggi principali.
```

# Domande finali

1. Qual è la differenza tra memoria nella media e memoria nella varianza?
2. Come si riconosce una serie AR(1) positiva?
3. Come si riconosce una serie AR(1) negativa?
4. Perché stimare un modello MA è meno immediato che stimare un modello AR?
5. Che cosa significa che i residui sono rumore bianco?
6. Perché bisogna guardare anche i quadrati dei residui?
7. Che cosa sono i residui standardizzati in un modello GARCH?
8. Che cosa significa $\alpha+\beta$ in un GARCH(1,1)?
9. Un modello con log-likelihood più alta è sempre preferibile?
10. Se il QQ-plot dei residui mostra code pesanti, quale ipotesi del modello è sospetta?

# Cosa dovreste aver capito alla fine

Al termine del laboratorio dovreste aver verificato che:

1. una serie temporale deve essere analizzata rispettando l'ordine temporale delle osservazioni;
2. l'ACF dei valori diagnostica memoria lineare nella media;
3. l'ACF dei quadrati diagnostica memoria nella scala delle fluttuazioni;
4. ARMA e GARCH rispondono a domande diverse;
5. la massima likelihood sceglie i parametri che rendono più plausibili i dati osservati sotto il modello;
6. i residui sono il punto decisivo della diagnostica;
7. un buon fit non significa solo parametri stimati, ma residui senza struttura temporale evidente;
8. modelli gaussiani semplici possono fallire nelle code, nelle asimmetrie o nei regimi non stazionari.

# Nota su alcuni indicatori non usati nel percorso principale

In statistica delle serie temporali si incontrano spesso altri indicatori diagnostici. Non sono indispensabili per questo laboratorio, ma è utile sapere a cosa servono.

## Skewness e kurtosis

La skewness misura l'asimmetria empirica di una distribuzione. Per una gaussiana simmetrica è circa zero.

La kurtosis misura quanto la distribuzione concentri probabilità nel centro e nelle code. Per una gaussiana vale circa 3, se si usa la definizione non-excess. Valori molto maggiori di 3 suggeriscono code pesanti o presenza di outlier.

Nel laboratorio queste informazioni sono già in parte visibili da istogrammi e QQ-plot.

## AIC e BIC

AIC e BIC sono criteri informativi per confrontare modelli con diverso numero di parametri. Partono dalla log-likelihood, ma penalizzano la complessità del modello. Servono perché un modello con più parametri tende quasi sempre ad adattarsi meglio ai dati, anche quando il miglioramento non è sostanziale.

In questo laboratorio non li usiamo come criterio principale. Qui è più importante capire la diagnostica dei residui: un modello è utile se rimuove la struttura temporale che voleva spiegare.

## Test di Ljung-Box

Il test di Ljung-Box è un test statistico per verificare se un insieme di autocorrelazioni fino a un certo lag è compatibile con zero. Può essere applicato ai residui o ai quadrati dei residui.

Nel laboratorio usiamo soprattutto i grafici ACF. Il test di Ljung-Box è la versione più formale della stessa domanda: resta autocorrelazione significativa?

# Nota sulle librerie professionali

In applicazioni reali, modelli ARMA/ARIMA e ARCH/GARCH vengono spesso stimati con librerie specializzate.

In Python, due librerie comuni sono:

- `statsmodels`, per AR, MA, ARMA/ARIMA e strumenti generali di analisi delle serie temporali;
- `arch`, per modelli ARCH/GARCH e varianti di volatilità condizionata.

In questo laboratorio non le usiamo direttamente. Il motivo è didattico: vogliamo vedere esplicitamente come si costruiscono residui, varianze condizionate e log-likelihood. Dopo aver capito questi passaggi, usare una libreria professionale diventa molto più sicuro.
