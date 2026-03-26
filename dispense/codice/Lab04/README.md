# LAB04 -- Modello SIR: ODE, Gillespie e tau-leaping

Questa directory contiene i codici di supporto al laboratorio sul modello epidemico SIR in tre diversi livelli di descrizione:

1. **ODE deterministica** -- dinamica media continua;
2. **Gillespie** -- simulazione stocastica esatta a eventi discreti;
3. **tau-leaping** -- approssimazione stocastica a passi finiti;
4. **script di confronto** -- confronto grafico tra i tre approcci.

L'impostazione generale del laboratorio è descritta nel file `Lab04.md`, che esplicita obiettivi, contesto teorico e domande guida: confrontare dinamica media e dinamica stocastica, capire il ruolo della chiusura mean-field, e discutere quando il tau-leaping è accurato oppure no.

## Contenuto della directory

- `01_sir_ode.py`  
  Integra il sistema SIR deterministico con `solve_ivp` di SciPy e produce il grafico di $S(t)$, $I(t)$, $R(t)$.

- `02_sir_gillespie.py`  
  Simula una singola traiettoria stocastica del SIR con algoritmo di Gillespie e visualizza l'andamento di $I(t)$.

- `03_sir_tau_leaping.py`  
  Simula una singola traiettoria del SIR con schema tau-leaping a passo fisso `dt` e visualizza l'andamento di $I(t)$.

- `04_compare_methods.py`  
  Confronta ODE, Gillespie e tau-leaping su un insieme di repliche. Lo script calcola la soluzione ODE, genera più traiettorie stocastiche indipendenti, interpola le realizzazioni su una griglia temporale comune e mostra media e deviazione standard del numero di infetti.

- `Lab04.md`  
  Testo del laboratorio con richiamo teorico, consegna e commenti metodologici.

## Requisiti

I codici usano:

- `numpy`
- `matplotlib`
- `scipy` (solo per `01_sir_ode.py` e `04_compare_methods.py`)

Installazione rapida:

```bash
pip install numpy matplotlib scipy
```

## Esecuzione

Dalla directory dei file:

```bash
python 01_sir_ode.py
python 02_sir_gillespie.py
python 03_sir_tau_leaping.py
python 04_compare_methods.py
```

Ogni script genera direttamente una figura a schermo.

## Parametri usati nei file

Nei quattro script i parametri sono impostati direttamente nel codice. La scelta di default è:

- `beta = 0.5`
- `gamma = 0.2`
- `N = 200`
- condizioni iniziali: `S0 = 199`, `I0 = 1`, `R0 = 0`
- orizzonte temporale: `T = 60.0`

Nel file tau-leaping è inoltre fissato:

- `dt = 0.1`

Nel file di confronto è fissato:

- griglia temporale uniforme `t_grid`
- numero di repliche `M = 50`
- confronto delle medie del numero di infetti `I(t)`

Per esplorare altri regimi è sufficiente modificare questi valori all'inizio di ciascuno script.

## Logica dei quattro script

### 1. `01_sir_ode.py`

Implementa il sistema classico:

$$
\dot S = -\beta \frac{SI}{N}, \qquad
\dot I = \beta \frac{SI}{N} - \gamma I, \qquad
\dot R = \gamma I.
$$

È il modello deterministico ottenuto dalla chiusura mean-field discussa nel laboratorio. È utile come riferimento per la dinamica media, ma non descrive la variabilità tra realizzazioni né l'eventuale estinzione precoce dell'epidemia.

### 2. `02_sir_gillespie.py`

Usa i due eventi elementari del SIR discreto:

- **infezione** con tasso $a_1 = \beta SI/N$;
- **guarigione** con tasso $a_2 = \gamma I$.

Ad ogni iterazione:

1. calcola i tassi;
2. estrae il tempo del prossimo evento da una distribuzione esponenziale;
3. sceglie l'evento con probabilità proporzionali ai tassi;
4. aggiorna lo stato.

Questo script mostra una **singola traiettoria** e quindi mette in evidenza bene fluttuazioni, ritardi e variabilità della dinamica.

### 3. `03_sir_tau_leaping.py`

Avanza il tempo con un passo fisso `dt` e approssima il numero di infezioni e guarigioni in ciascun intervallo con variabili di Poisson. È più rapido del Gillespie quando molti eventi avvengono in tempi brevi, ma resta un'approssimazione.

**Nota importante:** nella versione presente qui non è implementato alcun controllo per impedire stati non fisici (ad esempio popolazioni negative) se il passo `dt` è troppo grande o se i conteggi Poisson sono troppo aggressivi. Per questo conviene usare lo script anche come punto di partenza per discutere i limiti del metodo.

### 4. `04_compare_methods.py`

È lo script più utile per il confronto finale. In particolare:

- integra la soluzione ODE;
- genera un ensemble di traiettorie Gillespie;
- genera un ensemble di traiettorie tau-leaping;
- interpola tutte le realizzazioni sulla stessa griglia temporale;
- calcola media e deviazione standard di $I(t)$;
- produce un grafico comparativo.

Questo file permette di vedere immediatamente una distinzione centrale del laboratorio: la soluzione ODE va confrontata più correttamente con una **media su repliche** che con una singola traiettoria stocastica.

## Suggerimento di uso didattico

Un ordine naturale di lavoro è il seguente:

1. eseguire `01_sir_ode.py` per fissare la dinamica media;
2. eseguire `02_sir_gillespie.py` più volte cambiando il seed per osservare la variabilità;
3. eseguire `03_sir_tau_leaping.py` variando `dt` per vedere quando l'approssimazione resta ragionevole;
4. usare `04_compare_methods.py` per il confronto finale tra media ODE e simulazioni stocastiche.

## Limiti attuali dei codici

Questi script sono volutamente semplici e pensati per il laboratorio, quindi presentano alcune limitazioni:

- i parametri sono hard-coded nei file;
- non c'è interfaccia da linea di comando;
- `03_sir_tau_leaping.py` non impone vincoli di positività;
- `04_compare_methods.py` confronta solo il numero di infetti, non tutte e tre le variabili;
- non vengono salvate automaticamente le figure su file.

## Estensioni naturali

Possibili sviluppi utili per esercizio o progetto:

- aggiungere argomenti da riga di comando (`argparse`);
- salvare grafici in formato PNG o PDF;
- confrontare sistematicamente diversi valori di `dt` nel tau-leaping;
- inserire controlli per evitare stati negativi;
- confrontare non solo le medie ma anche distribuzioni, bande percentile o tempi al picco;
- studiare l'effetto della taglia `N` sulla differenza tra ODE e dinamica stocastica.

## Riferimenti interni

Per la teoria e la consegna del laboratorio, vedere `Lab04.md`.
