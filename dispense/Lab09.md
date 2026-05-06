# LAB08: Analisi di serie stocastiche: ARMA, ARCH e GARCH

## Obiettivi

In questo laboratorio analizziamo serie temporali sintetiche generate da modelli stocastici discreti nel tempo.

L'obiettivo non e' soltanto stimare parametri, ma imparare a costruire una procedura completa di analisi:

1. osservare una serie temporale;
2. decidere se la serie e' stazionaria o se conviene passare agli incrementi;
3. distinguere memoria nella media e memoria nella varianza;
4. usare ACF, PACF, istogrammi e QQ-plot come strumenti diagnostici;
5. stimare modelli ARMA gaussiani tramite massima likelihood;
6. stimare modelli ARCH e GARCH gaussiani tramite massima likelihood;
7. analizzare i residui e i residui standardizzati;
8. decidere se il modello stimato ha davvero assorbito la struttura temporale dei dati.

Il laboratorio usa dati sintetici. Le serie sono state generate da modelli noti, ma il modello generatore non viene indicato nei file dati. Il compito e' ricostruire, tramite diagnostica e stima, quale classe di modello sia piu' plausibile.

## Il contesto

Una serie temporale non e' una semplice lista di numeri. L'ordine delle osservazioni contiene informazione.

Una sequenza
$$X_0, X_1, \ldots, X_T$$
puo' avere:

- dipendenza nei valori, cioe' memoria nella media;
- dipendenza nei quadrati, cioe' memoria nella scala delle fluttuazioni;
- distribuzione marginale non gaussiana;
- outlier o code pesanti;
- periodi tranquilli alternati a periodi turbolenti;
- non stazionarieta', con varianza che cresce nel tempo o trend deterministici.

In questo laboratorio ci concentriamo principalmente su due famiglie di modelli.

La prima famiglia e' quella dei modelli ARMA. Questi modelli cercano di descrivere la parte prevedibile della media condizionata:
$$\mathbb{E}[X_t \mid \mathcal{F}_{t-1}].$$

La seconda famiglia e' quella dei modelli ARCH/GARCH. Questi modelli cercano di descrivere la varianza condizionata:
$$\mathrm{Var}(X_t \mid \mathcal{F}_{t-1}) = \sigma_t^2.$$

Il punto concettuale piu' importante e' il seguente:

- una serie puo' avere autocorrelazione quasi nulla nei valori, ma forte autocorrelazione nei quadrati. In questo caso un modello ARMA puo' non essere sufficiente, mentre un modello ARCH/GARCH puo' catturare la dipendenza residua nella volatilita'.

C'e' pero' una domanda preliminare ad entrambe le famiglie: la serie e' stazionaria? Se non lo e', tanto ARMA quanto GARCH stimati direttamente sui valori producono risultati ingannevoli. La Parte 1bis introduce la diagnostica per decidere se lavorare sui valori o sugli incrementi.

## Organizzazione dei file

La cartella del laboratorio e' organizzata cosi':

```
Lab08/
|-- data/
|   |-- serie_01.csv
|   |-- ...
|   |-- serie_10.csv
|   `-- soluzioni_generative.csv
|-- diagnostics.py
|-- figures/
|   |-- serie_01.png
|   |-- ...
|   `-- serie_10.png
|-- fit_models.py
|-- main.py
|-- requirements.txt
`-- output/    # creata automaticamente quando si esegue main.py
```

I file `serie_01.csv`, ..., `serie_10.csv` contengono le serie da analizzare. Ogni file ha due colonne:

```
t,x
0,...
1,...
2,...
...
```

La colonna `t` contiene l'indice temporale. La colonna `x` contiene il valore osservato.

La cartella `figures/` contiene i grafici delle serie, generati al momento della costruzione dei dati. Queste figure sono utili per un controllo visivo iniziale, ma l'analisi vera e propria deve essere fatta con `main.py`, che produce le figure diagnostiche nella cartella `output/`.

Il file `data/soluzioni_generative.csv` contiene il modello generatore e i parametri delle serie. E' una chiave per il docente e non dovrebbe essere usato dagli studenti durante l'analisi.

La cartella `output/` non e' necessariamente presente all'inizio. Viene creata automaticamente dallo script quando si esegue `main.py`.

## Dipendenze Python

Per il laboratorio usiamo solo librerie standard per calcolo scientifico e ottimizzazione numerica:

```
numpy, pandas, matplotlib, scipy
```

Il file `requirements.txt` deve contenere:

```
numpy
pandas
matplotlib
scipy
```

Installazione con pip:

```
pip install -r requirements.txt
```

oppure:

```
pip install numpy pandas matplotlib scipy
```

Non usiamo librerie specializzate come `statsmodels` o `arch` nel codice operativo del laboratorio. Esistono librerie professionali per stimare ARMA e GARCH, ma qui vogliamo vedere esplicitamente cosa viene calcolato: residui, varianze condizionate e log-likelihood.

## Come eseguire il laboratorio

Aprire un terminale nella cartella `Lab08/`, cioe' nella cartella che contiene `main.py`, `fit_models.py` e `diagnostics.py`.

Eseguire:

```
python main.py
```

Nel file `main.py` si scelgono la serie da analizzare e la cartella di output:

```python
DATA_FILE = "data/serie_01.csv"
OUTPUT_DIR = "output/serie_01"
```

Si decide se lavorare sui valori o sugli incrementi (vedi Parte 1bis):

```python
USE_INCREMENTS = False
```

Si sceglie anche il modello ARMA da provare (in questo esempio un AR):

```python
ARMA_P = 1
ARMA_Q = 0
```

Per analizzare un'altra serie, modificare ad esempio:

```python
DATA_FILE = "data/serie_04.csv"
OUTPUT_DIR = "output/serie_04"
```

L'esecuzione produce figure e report nella cartella indicata da `OUTPUT_DIR`.

## Due tipi di diagnostica

E' importante distinguere due passaggi diversi.

La **diagnostica della serie osservata** si fa una sola volta. Serve a capire quali strutture sono presenti nei dati:

- grafico della serie;
- istogramma;
- QQ-plot;
- ACF;
- PACF;
- ACF dei quadrati;
- statistiche per blocchi (media e varianza su K blocchi consecutivi).

Se la diagnostica della serie osservata indica non stazionarieta' (Parte 1bis), si attiva `USE_INCREMENTS = True` e la diagnostica si ripete una seconda volta sugli incrementi $\Delta X_t = X_{t+1} - X_t$, con prefisso `inc_` invece di `raw_`.

La **diagnostica dei residui** si fa invece dopo aver stimato un modello. Modelli diversi producono residui diversi, quindi e' naturale confrontare i residui di ARMA, ARCH e GARCH.

Per i modelli ARCH/GARCH si guardano in particolare i residui standardizzati:
$$z_t = \frac{\hat{\varepsilon}_t}{\hat{\sigma}_t}.$$
Se il modello ha descritto bene la varianza condizionata, questi residui standardizzati dovrebbero somigliare a rumore bianco gaussiano.

Una cartella di output tipica contiene:

```
output/
`-- serie_XX/
    |-- raw_serie.png
    |-- raw_istogramma.png
    |-- raw_qqplot.png
    |-- raw_acf.png
    |-- raw_pacf.png
    |-- raw_acf_quadrati.png
    |-- raw_block_stats.png
    |-- inc_serie.png                    # solo se USE_INCREMENTS=True
    |-- inc_istogramma.png               # solo se USE_INCREMENTS=True
    |-- inc_qqplot.png                   # solo se USE_INCREMENTS=True
    |-- inc_acf.png                      # solo se USE_INCREMENTS=True
    |-- inc_pacf.png                     # solo se USE_INCREMENTS=True
    |-- inc_acf_quadrati.png             # solo se USE_INCREMENTS=True
    |-- inc_block_stats.png              # solo se USE_INCREMENTS=True
    |-- arma_residui.png
    |-- arma_istogramma.png
    |-- arma_qqplot.png
    |-- arma_acf_residui.png
    |-- arma_acf_residui_quadrati.png
    |-- arma_report.txt
    |-- arch_standardized_residui.png
    |-- arch_standardized_istogramma.png
    |-- arch_standardized_qqplot.png
    |-- arch_standardized_acf_residui.png
    |-- arch_standardized_acf_residui_quadrati.png
    |-- arch_standardized_report.txt
    |-- garch_standardized_residui.png
    |-- garch_standardized_istogramma.png
    |-- garch_standardized_qqplot.png
    |-- garch_standardized_acf_residui.png
    |-- garch_standardized_acf_residui_quadrati.png
    `-- garch_standardized_report.txt
```

## Modelli considerati

### Rumore bianco gaussiano

Il modello piu' semplice e':
$$X_t = \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \sigma^2),$$
con innovazioni indipendenti.

In questo caso ci aspettiamo:

- media circa nulla;
- varianza circa costante;
- ACF compatibile con zero;
- PACF compatibile con zero;
- ACF dei quadrati compatibile con zero;
- QQ-plot circa lineare se l'ipotesi gaussiana e' plausibile.

### AR(1)

Un modello autoregressivo di ordine 1 e':
$$X_t = c + \phi X_{t-1} + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \sigma^2).$$
Se $|\phi| < 1$, il processo e' stazionario.

Interpretazione:

- se $\phi > 0$, valori positivi tendono a essere seguiti da valori positivi;
- se $\phi < 0$, la serie tende ad alternare segno;
- se $|\phi|$ e' vicino a 1, la memoria decade lentamente.

Per un AR(1) stazionario ci aspettiamo una ACF che decade come $\rho(k) = \phi^k$.

### AR(p)

Un modello autoregressivo piu' generale e':
$$X_t = c + \phi_1 X_{t-1} + \phi_2 X_{t-2} + \cdots + \phi_p X_{t-p} + \varepsilon_t.$$
Qui la memoria della media e' distribuita su piu' ritardi. Puo' produrre persistenza lenta, oscillazioni smorzate, e forme di autocorrelazione piu' ricche rispetto ad AR(1).

### MA(1)

Un modello a media mobile di ordine 1 e':
$$X_t = \varepsilon_t + \theta \varepsilon_{t-1}.$$
La differenza importante rispetto ad AR(1) e' che nei modelli MA gli shock passati non sono osservati direttamente. Devono essere ricostruiti durante la stima. Per un MA(1) ideale, l'ACF si tronca dopo il primo lag.

### ARMA(p,q)

Il modello ARMA combina memoria dei valori e memoria degli shock:
$$X_t = c + \sum_{i=1}^{p} \phi_i X_{t-i} + \varepsilon_t + \sum_{j=1}^{q} \theta_j \varepsilon_{t-j}.$$
Un modello ARMA descrive dipendenza lineare nella media. Dopo la stima, i residui dovrebbero assomigliare a rumore bianco.

### ARCH(1)

Un modello ARCH(1) descrive memoria nella varianza condizionata:
$$X_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0,1),$$
con
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2.$$
Se lo shock precedente e' grande in valore assoluto, la varianza condizionata successiva aumenta.

### GARCH(1,1)

Un modello GARCH(1,1) aggiunge persistenza della volatilita':
$$X_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0,1),$$
con
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2.$$
La quantita' $\alpha + \beta$ misura la persistenza della volatilita'. Se e' vicina a 1, gli shock alla volatilita' decadono lentamente.

## Parte 1 -- Esplorazione preliminare

### 1.1 Scegliere una serie

Aprire `main.py` e scegliere una serie, per esempio:

```python
DATA_FILE = "data/serie_01.csv"
OUTPUT_DIR = "output/serie_01"
USE_INCREMENTS = False
```

Eseguire:

```
python main.py
```

Osservare i file prodotti in `output/serie_01/`.

### 1.2 Guardare la serie nel tempo

Aprire il grafico della serie osservata: `raw_serie.png`.

Domande:

1. La serie sembra oscillare o fluttuare attorno a una media stabile?
2. La scala delle fluttuazioni sembra costante?
3. Si vedono cluster di ampiezza, cioe' periodi tranquilli e periodi turbolenti?
4. Ci sono valori estremi isolati?
5. La serie sembra avere alternanza di segno?
6. La traiettoria deriva nel tempo o ritorna verso un livello centrale?

### 1.3 Istogramma e QQ-plot

Aprire l'istogramma e il QQ-plot della serie osservata: `raw_istogramma.png`, `raw_qqplot.png`.

Domande:

1. L'istogramma e' approssimativamente simmetrico?
2. La gaussiana sovrapposta descrive bene il centro della distribuzione?
3. Le code sembrano piu' pesanti di una gaussiana?
4. Nel QQ-plot i punti seguono la diagonale?
5. Le deviazioni, se presenti, sono al centro o nelle code?

## Parte 1bis -- Valori o incrementi?

Le Parti 2-5 di questo laboratorio assumono implicitamente che la serie analizzata sia stazionaria: media e varianza costanti nel tempo, autocorrelazioni che dipendono solo dal lag e non dal tempo. Tutti i modelli ARMA, ARCH e GARCH che stimeremo in seguito presuppongono questa proprieta'.

Le serie reali, pero', non sono sempre stazionarie. Una serie puo' presentare derive sistematiche, varianza crescente, o accumulare shock indipendenti come nel caso di un random walk. In questi casi e' spesso piu' utile lavorare non sui valori $X_t$ ma sui loro incrementi
$$\Delta X_t = X_{t+1} - X_t.$$
Questa parte introduce la diagnostica per decidere se la serie va analizzata direttamente o dopo differenziazione. La decisione e' preliminare a tutto il resto, e va presa prima di calcolare ACF, PACF o di stimare un modello.

### 1bis.1 Perche' la domanda e' importante

Considera un random walk:
$$X_{t+1} = X_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, \sigma^2).$$
Si dimostra facilmente che, partendo da $X_0 = 0$, $\mathrm{Var}(X_t) = t \sigma^2$: la varianza cresce linearmente nel tempo. Il processo non e' stazionario nei valori. Tuttavia, gli incrementi
$$\Delta X_t = \eta_t$$
sono per costruzione rumore bianco gaussiano: stazionari, indipendenti, identicamente distribuiti.

Se applichiamo un modello AR(1) ai valori di un random walk otteniamo tipicamente una stima $\hat{\phi}_1 \approx 1$. Il modello sembra "funzionare", ma il coefficiente vicino a uno e' in realta' il sintomo che il modello stazionario non e' quello giusto. Le proprieta' inferenziali standard, ovvero intervalli di confidenza e test, cessano di valere quando la stazionarieta' e' violata: in questa zona di parametri la teoria asintotica usuale non si applica.

Lavorare sugli incrementi rivela invece immediatamente che $\Delta X_t$ e' rumore bianco, e ci risparmia di stimare un AR(1) inadeguato.

### 1bis.2 Diagnostica visiva sulla traiettoria

Guardare `raw_serie.png` e' gia' diagnostico. Caratteristiche che suggeriscono di passare agli incrementi:

1. la serie non oscilla attorno a una media stabile, ma deriva nel tempo;
2. la varianza appare crescere con $t$;
3. la serie sembra "andare via" senza tornare verso un valore di riferimento;
4. la traiettoria assomiglia piu' a una passeggiata che a una sequenza di fluttuazioni attorno a una media.

Caratteristiche che invece suggeriscono di lavorare direttamente sui valori:

1. la serie oscilla attorno a una media chiaramente stabile;
2. la varianza appare costante nel tempo;
3. la serie ritorna periodicamente verso un livello centrale (mean reversion);
4. non c'e' trend evidente.

### 1bis.3 Diagnostica dall'ACF della serie

L'ACF dei valori fornisce un'indicazione piu' formale. Per una serie stazionaria con memoria breve, l'ACF decade rapidamente verso zero, e i valori rientrano nella banda di confidenza dopo pochi lag.

Per un random walk, invece:

1. l'ACF resta significativamente positiva per molti lag;
2. il decadimento e' lentissimo, quasi lineare;
3. anche a lag elevati i valori sono ben sopra la banda di confidenza.

Una ACF che resta alta su decine di lag e' un segnale forte di non stazionarieta', oppure che la stazionarieta' e' marginale (radice vicina al cerchio unitario).

### 1bis.4 Diagnostica sulla varianza locale

Un controllo pratico consiste nel dividere la serie in $K$ blocchi consecutivi di lunghezza uguale, e calcolare la varianza campionaria di ciascun blocco. Per una serie stazionaria queste varianze fluttuano attorno a un valore costante, a meno della variabilita' campionaria. Per un random walk, la varianza dei blocchi successivi cresce sistematicamente con il tempo.

Lo stesso confronto si puo' fare con la media o la mediana di ciascun blocco. Cambiamenti sistematici della media tra blocchi consecutivi sono un altro sintomo di non stazionarieta', ed eventualmente di presenza di un drift deterministico.

Lo script produce la figura `raw_block_stats.png` con due grafici a barre: media e varianza per blocco. Sotto le ipotesi di stazionarieta' le barre sono approssimativamente uguali. Crescite sistematiche tra il primo e l'ultimo blocco sono il segnale operativo principale.

### 1bis.5 Procedura pratica

Una procedura ragionevole per decidere se lavorare su $X_t$ o su $\Delta X_t$ e':

1. guardare `raw_serie.png`: la serie ha una media stabile o deriva nel tempo?
2. guardare `raw_acf.png`: l'ACF decade rapidamente o resta alta su molti lag?
3. guardare `raw_block_stats.png`: media e varianza per blocco sono stabili?
4. se i segnali concordano nell'indicare non stazionarieta', impostare `USE_INCREMENTS = True` in `main.py` e ri-eseguire;
5. esaminare i file prodotti con prefisso `inc_`: gli incrementi appaiono stazionari? in particolare, `inc_acf.png` e' compatibile con rumore bianco?
6. se gli incrementi appaiono stazionari, le Parti 2-5 procedono automaticamente sugli incrementi (ARMA, ARCH e GARCH vengono stimati su $\Delta X_t$);
7. se anche gli incrementi appaiono non stazionari, considerare una doppia differenziazione, ma con cautela: doppie differenze sono raramente necessarie e introducono autocorrelazione spuria.

### 1bis.6 Differenziazione spuria

Differenziare quando non serve ha un costo. Se $X_t$ e' gia' stazionario, applicare l'operazione di differenza introduce autocorrelazione negativa al lag 1 negli incrementi. In dettaglio: se $X_t$ e' rumore bianco con varianza $\sigma^2$, allora
$$\mathrm{Var}(\Delta X_t) = 2\sigma^2, \qquad \mathrm{Cov}(\Delta X_t, \Delta X_{t-1}) = -\sigma^2,$$
da cui
$$\rho_{\Delta X}(1) = -\frac{1}{2}.$$
Negli incrementi ottenuti per differenziazione di una serie stazionaria si manifesta dunque una struttura MA(1) artificiale, con autocorrelazione negativa al lag uno.

Per questo motivo la differenziazione non e' un trattamento preventivo o "di sicurezza": va applicata solo quando i segnali diagnostici la giustificano. Differenziare per default su una serie stazionaria peggiora la situazione invece di migliorarla.

### 1bis.7 Drift e sottrazione della media degli incrementi

Se la serie originale e' un random walk con drift,
$$X_{t+1} = X_t + \mu + \eta_t, \quad \mu \neq 0,$$
allora gli incrementi $\Delta X_t = \mu + \eta_t$ sono stazionari, ma con media non nulla.

In questo caso la diagnostica sugli incrementi mostrera':

- istogramma centrato attorno a $\mu$, non attorno a zero;
- ACF compatibile con rumore bianco;
- nessuna struttura nei quadrati.

Lo script `main.py` stampa la media campionaria degli incrementi e la confronta indicativamente con $\hat{\sigma}/\sqrt{n}$: se le due quantita' sono dello stesso ordine, la serie originale e' compatibile con un random walk puro; se la media e' nettamente piu' grande, c'e' drift deterministico.

Prima di procedere alla stima di un eventuale modello ARMA sugli incrementi, conviene sottrarre la media campionaria, oppure includere esplicitamente un termine costante nel modello. Lo script lo include gia' di default tramite il flag `include_constant=True` in `fit_arma_mle`.

### 1bis.8 Domande

1. Tra le serie del laboratorio, ci sono casi in cui la traiettoria sembra avere varianza che cresce nel tempo o derivare senza tornare verso un livello stabile? Quali?
2. L'ACF di queste serie decade lentamente o rapidamente?
3. Quale risultato vi aspettate calcolando media e varianza su 4-5 blocchi consecutivi di una serie stazionaria? E di un random walk?
4. Se applicate AR(1) direttamente ai valori di un random walk, che valore prevedete per il coefficiente $\hat{\phi}_1$?
5. Se differenziate una serie che era gia' rumore bianco, che ACF mostrano gli incrementi? Perche'?
6. Come distinguete operativamente un random walk puro da un random walk con drift?

### 1bis.9 Nota: test formali di radice unitaria

Le diagnostiche descritte qui sono grafiche e basate su statistiche locali. Esistono test formali di radice unitaria, ad esempio Augmented Dickey-Fuller (ADF) e KPSS, che riducono la decisione a un p-value. In questo laboratorio non li usiamo direttamente: l'obiettivo didattico e' capire quando la serie viola la stazionarieta' osservandone i sintomi, non ottenere una risposta automatica. Una volta acquisita la diagnostica visiva, applicare un test formale come complemento e' uno step naturale.

## Parte 2 -- ACF, PACF e memoria temporale

In questa parte si analizzano le ACF e PACF della serie sottoposta al modello, ovvero $X_t$ se `USE_INCREMENTS = False` o $\Delta X_t$ se `USE_INCREMENTS = True`. Per uniformita' di notazione, in questa sezione usiamo $X_t$ per indicare la serie effettivamente analizzata.

### 2.1 ACF della serie

Aprire l'ACF della serie analizzata: `raw_acf.png` (oppure `inc_acf.png`).

L'ACF misura la correlazione tra $X_t$ e $X_{t+k}$.

Domande:

1. L'ACF e' compatibile con zero per tutti i lag?
2. Decade lentamente?
3. Alterna segno?
4. Ha un picco forte solo al primo lag?
5. Sembra piu' compatibile con un modello AR o MA?

### 2.2 PACF della serie

Aprire la PACF: `raw_pacf.png` (oppure `inc_pacf.png`).

La PACF misura la correlazione al lag $k$ dopo aver rimosso l'effetto dei lag intermedi.

Regole diagnostiche orientative:

- AR(1): PACF significativa al lag 1, poi circa nulla;
- AR(p): PACF significativa fino al lag $p$, poi circa nulla;
- MA(q): ACF significativa fino al lag $q$, PACF che decade;
- ARMA(p,q): ACF e PACF spesso decadono entrambe.

Queste non sono regole assolute, ma aiutano a proporre modelli candidati.

### 2.3 ACF dei quadrati

Aprire l'ACF dei quadrati: `raw_acf_quadrati.png` (oppure `inc_acf_quadrati.png`).

Questa figura e' fondamentale per diagnosticare volatilita' condizionata.

Domande:

1. I valori $X_t$ hanno autocorrelazione?
2. I quadrati $X_t^2$ hanno autocorrelazione?
3. Se l'ACF di $X_t$ e' quasi nulla ma quella di $X_t^2$ e' significativa, che cosa suggerisce?
4. La serie sembra piu' adatta a un modello ARMA o a un modello ARCH/GARCH?

## Parte 3 -- Fit ARMA gaussiano

### 3.1 Scegliere un modello ARMA

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

```
python main.py
```

### 3.2 Leggere i parametri stimati

Nel terminale comparira' un report simile a:

```
ARMA(1,0) gaussiano
convergenza: True
log-likelihood: ...
constant = ...
phi_1 = ...
sigma = ...
```

La log-likelihood misura quanto i dati osservati sono plausibili sotto il modello stimato. A parita' di dati, una log-likelihood piu' alta indica un fit migliore, ma non basta da sola per scegliere sempre il modello: modelli piu' complessi tendono spesso a migliorare il fit anche quando aggiungono parametri non realmente necessari.

Domande:

1. L'ottimizzazione e' convergente?
2. I parametri stimati hanno segno e ordine di grandezza plausibili?
3. Se il modello e' AR(1), il coefficiente $\phi_1$ e' positivo o negativo?
4. Se $|\phi_1|$ e' vicino a 1, che cosa significa?
5. I residui migliorano passando da un modello piu' semplice a uno piu' complesso?

**Attenzione: $\hat{\phi}_1$ vicino al bound.** Lo script `fit_models.py` impone un vincolo $|\phi_i| \leq 0.98$ per ragioni di stabilita' numerica. Se la stima di $\hat{\phi}_1$ esce esattamente o quasi esattamente sul bound (ad esempio `phi_1 = 0.980000`), questo non e' un valore fisico ma un sintomo: l'ottimizzatore vorrebbe spingere il parametro oltre, perche' la serie non e' stazionaria. In questo caso torna alla Parte 1bis: la diagnostica della stazionarieta' va rifatta, e con tutta probabilita' bisogna passare agli incrementi (`USE_INCREMENTS = True`).

### 3.3 Residui ARMA

Dopo il fit ARMA, vengono prodotti file dei residui:

```
arma_residui.png
arma_istogramma.png
arma_qqplot.png
arma_acf_residui.png
arma_acf_residui_quadrati.png
arma_report.txt
```

Queste figure non sono una seconda diagnostica della serie originale: sono una diagnostica dei residui prodotti dal modello ARMA.

I residui ARMA sono

$$\hat{\varepsilon}_t = X_t - \hat{\mathbb{E}}[X_t \mid \mathcal{F}_{t-1}].$$

Domande:

1. I residui hanno media circa zero?
2. L'ACF dei residui e' compatibile con rumore bianco?
3. L'ACF dei residui quadrati e' compatibile con rumore bianco?
4. Il QQ-plot dei residui e' vicino alla diagonale?
5. Se i residui quadrati sono autocorrelati, cosa manca al modello ARMA?

## Parte 4 -- Fit ARCH(1)

### 4.1 Quando ha senso provare ARCH?

Un modello ARCH ha senso quando:

- la serie non mostra forte autocorrelazione nei valori;
- ma mostra autocorrelazione nei quadrati;
- la traiettoria presenta cluster di volatilita';
- ci sono periodi di fluttuazioni piccole alternati a periodi di fluttuazioni grandi.

Il modello ARCH(1) stimato dal codice e':
$$X_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0,1),$$
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2.$$

### 4.2 Leggere i parametri ARCH

Il report contiene:

```
ARCH(1) gaussiano
mu = ...
omega = ...
alpha = ...
```

Domande:

1. $\alpha$ e' vicino a zero oppure grande?
2. Se $\alpha$ e' grande, che cosa significa?
3. Il modello ARCH migliora la diagnostica dei residui quadrati?
4. I residui standardizzati sembrano piu' vicini a rumore bianco?

Anche qui un valore di $\alpha$ vicinissimo a 1 con `convergenza: False` puo' essere il sintomo di una non stazionarieta' non riconosciuta nei valori: in tal caso vale la pena tornare alla Parte 1bis.

### 4.3 Residui standardizzati

Per ARCH e GARCH non basta guardare i residui grezzi. Bisogna guardare i residui standardizzati:
$$z_t = \frac{\hat{\varepsilon}_t}{\hat{\sigma}_t}.$$
Se il modello della varianza condizionata e' adeguato, allora $z_t$ dovrebbe assomigliare a rumore bianco gaussiano con varianza circa 1.

Domande:

1. L'ACF di $z_t$ e' circa nulla?
2. L'ACF di $z_t^2$ e' circa nulla?
3. Il QQ-plot di $z_t$ e' circa gaussiano?
4. La varianza campionaria di $z_t$ e' vicina a 1?

## Parte 5 -- Fit GARCH(1,1)

### 5.1 Modello

Il modello GARCH(1,1) e':
$$X_t = \mu + \varepsilon_t, \quad \varepsilon_t = \sigma_t z_t, \quad z_t \sim \mathcal{N}(0,1),$$
$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2.$$
Rispetto ad ARCH(1), il GARCH(1,1) aggiunge il termine $\beta \sigma_{t-1}^2$, che produce persistenza della volatilita'.

### 5.2 Leggere i parametri GARCH

Il report contiene:

```
GARCH(1,1) gaussiano
mu = ...
omega = ...
alpha = ...
beta = ...
alpha + beta = ...
```

Domande:

1. $\alpha$ e' grande o piccolo?
2. $\beta$ e' grande o piccolo?
3. Quanto vale $\alpha + \beta$?
4. Se $\alpha + \beta$ e' vicino a 1, cosa significa?
5. Il GARCH migliora rispetto ad ARCH nella diagnostica dei residui quadrati?

### 5.3 Confronto ARCH/GARCH

Confrontare:

- log-likelihood;
- interpretazione dei parametri;
- ACF dei residui standardizzati;
- ACF dei quadrati dei residui standardizzati;
- QQ-plot.

Domande:

1. GARCH ha likelihood maggiore di ARCH?
2. La maggiore flessibilita' del GARCH migliora anche i residui standardizzati?
3. Restano tracce di struttura nei residui?
4. La maggiore complessita' del GARCH e' giustificata dalla diagnostica?

## Parte 6 -- Analisi di tutte le serie

Ripetere la pipeline per tutte le serie disponibili:

```
serie_01.csv
...
serie_10.csv
```

Per ciascuna serie, compilare una tabella del tipo:

| serie | valori o incrementi? | ACF valori | PACF valori | ACF quadrati | modello candidato | modello stimato | residui ok? |
|-------|---------------------|------------|-------------|--------------|-------------------|-----------------|-------------|
| 01    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 02    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 03    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 04    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 05    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 06    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 07    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 08    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 09    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |
| 10    | ...                 | ...        | ...         | ...          | ...               | ...             | ...         |

La prima colonna registra l'esito della diagnostica della Parte 1bis: per quali serie e' stato necessario passare agli incrementi?

Le serie non devono essere identificate solo guardando i parametri stimati. La diagnosi deve partire dai grafici e dai residui.

## Parte 7 -- Confronto tra modelli

Per almeno due serie, confrontare esplicitamente tre modelli:

1. ARMA semplice;
2. ARCH(1);
3. GARCH(1,1).

Per ciascun modello riportare:

- log-likelihood;
- interpretazione dei parametri;
- diagnostica dei residui.

Domande:

1. Quale modello produce residui piu' simili a rumore bianco?
2. Quale modello riduce meglio l'autocorrelazione dei quadrati dei residui?
3. Il modello con likelihood piu' alta ha anche residui migliori?
4. Se likelihood e diagnostica visuale non concordano, quale criterio considerate piu' importante?
5. Il modello piu' complesso e' sempre preferibile?

## Parte 8 -- Casi volutamente difficili

Tra le serie del laboratorio ci sono almeno due tipi di casi in cui i modelli ARMA, ARCH e GARCH gaussiani standard sono inadeguati. Il vostro compito non e' necessariamente trovare il modello vero, ma riconoscere che il modello stimato lascia una struttura non spiegata.

### 8.1 Volatilita' asimmetrica

Una delle serie puo' essere stata generata da un modello con volatilita' asimmetrica, in cui shock negativi aumentano la volatilita' futura piu' degli shock positivi della stessa ampiezza.

Segnali possibili:

- residui standardizzati con asimmetria;
- QQ-plot non lineare nelle code;
- ACF dei quadrati ancora significativa;
- modello GARCH simmetrico che cattura parte della volatilita' ma non tutta.

### 8.2 Non stazionarieta' apparentemente fittabile

Le serie non stazionarie (random walk e random walk con drift) costituiscono un secondo tipo di trappola. Stimando direttamente un AR(1) sui valori, il modello sembra produrre un fit ragionevole: convergenza positiva, residui con varianza coerente, QQ-plot accettabile.

I sintomi di errore sono pero' chiari, se sapete dove guardare:

- $\hat{\phi}_1$ stimato esattamente sul bound (ad esempio `0.980000` con il vincolo $|\phi_1| \leq 0.98$);
- p-value di Ljung-Box sui residui che resta piccolissimo, come se il modello non avesse rimosso nessuna autocorrelazione;
- ARCH che non converge oppure che dirige $\alpha \to 1$;
- nessun miglioramento visibile passando da AR(1) a ARMA(1,1) o ad AR(2).

E' una situazione qualitativamente diversa dal caso 8.1. La GJR-GARCH della serie con volatilita' asimmetrica e' un modello "quasi giusto" che lascia un residuo strutturato. Il random walk e' un modello "del tutto sbagliato", e la diagnostica della Parte 1bis lo rivela immediatamente. Imparare a riconoscere entrambi i casi e' parte dell'obiettivo del laboratorio.

### 8.3 Domande

1. Quale serie sembra piu' difficile da descrivere con i modelli disponibili?
2. Quale diagnostica lo mostra meglio?
3. Che tipo di estensione del modello sarebbe utile?
4. Servirebbe una volatilita' asimmetrica?
5. Servirebbe una differenziazione preliminare?
6. Servirebbe un cambio di regime?

## Relazione finale

Consegnare una breve relazione, non un elenco di grafici.

La relazione deve contenere:

1. una descrizione della procedura usata, comprensiva della diagnostica della Parte 1bis;
2. una tabella riassuntiva per tutte le serie;
3. un'analisi dettagliata di almeno due serie, di cui almeno una con esito diverso nella decisione valori/incrementi;
4. il confronto fra ARMA, ARCH e GARCH dove appropriato;
5. una discussione dei residui;
6. una conclusione critica.

### Struttura suggerita

1. Introduzione
   - Obiettivo del laboratorio.
   - Differenza tra memoria nella media e memoria nella varianza.
   - Ruolo della stazionarieta' come precondizione.
2. Metodi
   - Diagnostica preliminare e decisione valori/incrementi.
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
   - Quali serie hanno richiesto la differenziazione, e perche'?
6. Conclusioni
   - Messaggi principali.

## Domande finali

1. Qual e' la differenza tra memoria nella media e memoria nella varianza?
2. Come si riconosce una serie AR(1) positiva?
3. Come si riconosce una serie AR(1) negativa?
4. Perche' stimare un modello MA e' meno immediato che stimare un modello AR?
5. Che cosa significa che i residui sono rumore bianco?
6. Perche' bisogna guardare anche i quadrati dei residui?
7. Che cosa sono i residui standardizzati in un modello GARCH?
8. Che cosa significa $\alpha + \beta$ in un GARCH(1,1)?
9. Un modello con log-likelihood piu' alta e' sempre preferibile?
10. Se il QQ-plot dei residui mostra code pesanti, quale ipotesi del modello e' sospetta?
11. Come si riconosce una serie non stazionaria nei valori?
12. Cosa significa che il coefficiente $\hat{\phi}_1$ stimato e' molto vicino a 1, e cosa fareste in quel caso?
13. Differenziare una serie gia' stazionaria e' una operazione neutra? Perche'?

## Cosa dovreste aver capito alla fine

Al termine del laboratorio dovreste aver verificato che:

1. una serie temporale deve essere analizzata rispettando l'ordine temporale delle osservazioni;
2. la stazionarieta' va controllata prima di stimare un modello: un buon fit su una serie non stazionaria e' un'illusione, e si manifesta come parametri sui bound del vincolo o come ARCH che non converge;
3. l'ACF dei valori diagnostica memoria lineare nella media;
4. l'ACF dei quadrati diagnostica memoria nella scala delle fluttuazioni;
5. ARMA e GARCH rispondono a domande diverse;
6. la massima likelihood sceglie i parametri che rendono piu' plausibili i dati osservati sotto il modello;
7. i residui sono il punto decisivo della diagnostica;
8. un buon fit non significa solo parametri stimati, ma residui senza struttura temporale evidente;
9. modelli gaussiani semplici possono fallire nelle code, nelle asimmetrie o nei regimi non stazionari.

## Nota su alcuni indicatori non usati nel percorso principale

In statistica delle serie temporali si incontrano spesso altri indicatori diagnostici. Non sono indispensabili per questo laboratorio, ma e' utile sapere a cosa servono.

### Skewness e kurtosis

La skewness misura l'asimmetria empirica di una distribuzione. Per una gaussiana simmetrica e' circa zero. La kurtosis misura quanto la distribuzione concentri probabilita' nel centro e nelle code. Per una gaussiana vale circa 3, se si usa la definizione non-excess. Valori molto maggiori di 3 suggeriscono code pesanti o presenza di outlier.

Nel laboratorio queste informazioni sono gia' in parte visibili da istogrammi e QQ-plot.

### AIC e BIC

AIC e BIC sono criteri informativi per confrontare modelli con diverso numero di parametri. Partono dalla log-likelihood, ma penalizzano la complessita' del modello. Servono perche' un modello con piu' parametri tende quasi sempre ad adattarsi meglio ai dati, anche quando il miglioramento non e' sostanziale.

In questo laboratorio non li usiamo come criterio principale. Qui e' piu' importante capire la diagnostica dei residui: un modello e' utile se rimuove la struttura temporale che voleva spiegare.

### Test di Ljung-Box

Il test di Ljung-Box e' un test statistico per verificare se un insieme di autocorrelazioni fino a un certo lag e' compatibile con zero. Puo' essere applicato ai residui o ai quadrati dei residui.

Nel laboratorio usiamo soprattutto i grafici ACF. Il test di Ljung-Box e' la versione piu' formale della stessa domanda: resta autocorrelazione significativa?

### Test di radice unitaria

ADF (Augmented Dickey-Fuller) e KPSS sono test formali di stazionarieta'. Convertono la decisione "valori o incrementi?" della Parte 1bis in un p-value. Non li usiamo direttamente nel laboratorio, ma sono il complemento naturale della diagnostica visiva quando si lavora su dati reali.

## Nota sulle librerie professionali

In applicazioni reali, modelli ARMA/ARIMA e ARCH/GARCH vengono spesso stimati con librerie specializzate.

In Python, due librerie comuni sono:

- `statsmodels`, per AR, MA, ARMA/ARIMA e strumenti generali di analisi delle serie temporali;
- `arch`, per modelli ARCH/GARCH e varianti di volatilita' condizionata.

In questo laboratorio non le usiamo direttamente. Il motivo e' didattico: vogliamo vedere esplicitamente come si costruiscono residui, varianze condizionate e log-likelihood. Dopo aver capito questi passaggi, usare una libreria professionale diventa molto piu' sicuro.
