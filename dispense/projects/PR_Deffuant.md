---
title: "Project: Modello di Deffuant e dinamiche di opinione"
subtitle: "bounded confidence, transizioni di consenso e formazione dei cluster"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce il modello di Deffuant come caso di studio per un corso di metodi computazionali per modelli stocastici.

Gli obiettivi sono sei:

1. formalizzare la formazione dell'opinione come processo stocastico su uno spazio continuo;
2. derivare la transizione di fase tra consenso e frammentazione al variare della soglia di confidenza $\varepsilon$;
3. mostrare come la stessa struttura matematica descriva contesti apparentemente molto diversi — formazione del consenso scientifico e negoziazione tra parti con interessi diversi;
4. introdurre osservabili quantitative per misurare ordine, clustering e polarizzazione;
5. studiare il ruolo della topologia della rete di interazioni;
6. collegare il modello alla piu' ampia famiglia di modelli di opinion dynamics e alle dinamiche replicative.

Dal punto di vista del corso, questo progetto introduce una forma di stocasticita' diversa da quella degli altri modelli: la casualita' non sta nella dinamica delle singole variabili di stato, ma nella scelta di chi interagisce con chi. Il risultato collettivo — consenso o frammentazione — emerge da milioni di incontri casuali locali, nessuno dei quali e' di per se' decisivo.

# 2. Motivazione: due contesti, una matematica

## 2.1 Formazione del consenso scientifico

In una comunita' scientifica, i ricercatori hanno posizioni diverse su una questione controversa: per esempio, quanto e' efficace un intervento di salute pubblica, o quanto e' robusto un certo modello climatico. Le posizioni sono continue — non semplici pareri binari — e variano da scetticismo forte a fiducia forte.

I ricercatori interagiscono tra loro: leggono i lavori degli altri, partecipano a conferenze, condividono dati. Quando due ricercatori si confrontano, tendono ad avvicinarsi nelle proprie posizioni, ma solo se le loro opinioni di partenza non sono troppo distanti. Se la distanza e' grande, il confronto non produce convergenza: i due interlocutori rimangono ciascuno sulla propria posizione, magari irrigidendosi ulteriormente.

Questo meccanismo produce due esiti qualitativamente diversi a seconda di quanto e' ampia la "finestra di apertura" dei ricercatori:

- se i ricercatori sono abbastanza aperti a posizioni distanti dalla propria, la comunita' converge gradualmente verso un consenso;
- se i ricercatori accettano solo opinioni molto simili alla propria, si formano cluster isolati che smettono di comunicare tra loro: la comunita' si frammenta.

Il modello di Deffuant formalizza esattamente questo meccanismo.

## 2.2 Negoziazione e adozione di standard

Due aziende devono concordare un contratto di fornitura. Le loro posizioni iniziali su prezzo, tempi di consegna e garanzie sono distanti. La negoziazione procede attraverso incontri in cui ciascuna parte fa concessioni, avvicinandosi alla posizione dell'altra — ma solo entro certi limiti: se le posizioni sono troppo distanti, l'incontro si chiude senza accordo.

Lo stesso schema si applica all'adozione di standard tecnologici in un settore industriale: le aziende devono coordinarsi su un formato comune, ma ciascuna ha incentivi a mantenere il proprio standard proprietario. Se le posizioni iniziali sono abbastanza vicine, si raggiunge un accordo; se sono troppo distanti, il settore rimane frammentato in standard incompatibili.

In entrambi i casi, la struttura matematica e' identica a quella della formazione del consenso scientifico: agenti con posizioni continue su una variabile scalare, interazioni condizionate dalla vicinanza, transizione tra unificazione e frammentazione.

## 2.3 Il messaggio metodologico

Come per il bandit, il punto non e' che i due contesti siano identici nei dettagli. E' che la stessa struttura formale — agenti con opinioni continue, bounded confidence, incontri casuali, aggiornamento locale — si applica a entrambi, e che i risultati del modello (transizione di fase, dipendenza da $\varepsilon$, struttura dei cluster) si leggono in modo diretto in ciascun contesto.

# 3. Definizione formale del modello

## 3.1 Agenti e opinioni

Consideriamo una popolazione di $N$ agenti. Ogni agente $i$ e' caratterizzato da un'**opinione** $x_i \in [0, 1]$, un numero reale che rappresenta la sua posizione su una scala continua.

Inizialmente, le opinioni sono distribuite uniformemente:

$$
x_i(0) \sim U[0, 1], \qquad i = 1, \dots, N.
$$

L'intervallo $[0, 1]$ e' una convenzione: quel che conta e' che le opinioni siano continue e che la loro distanza sia misurabile.

**Interpretazione scientifica.** $x_i$ e' la stima che il ricercatore $i$ assegna all'efficacia di un intervento, su una scala da 0 (certamente inefficace) a 1 (certamente efficace).

**Interpretazione negoziale.** $x_i$ e' la posizione del negoziatore $i$ su una variabile contrattuale (ad esempio, il prezzo accettabile, normalizzato tra il minimo e il massimo possibile).

## 3.2 La regola di interazione

A ogni passo temporale:

1. si estraggono casualmente due agenti $i$ e $j$;
2. se la distanza tra le loro opinioni e' minore o uguale alla **soglia di confidenza** $\varepsilon$:

$$
|x_i - x_j| \le \varepsilon,
$$

allora le due opinioni si avvicinano reciprocamente:

$$
x_i \leftarrow x_i + \mu (x_j - x_i),
$$
$$
x_j \leftarrow x_j + \mu (x_i - x_j).
$$

3. se $|x_i - x_j| > \varepsilon$: nessuna modifica.

Il parametro $\mu \in (0, 0.5]$ e' la **velocita' di convergenza** o **tasso di compromesso**. Per $\mu = 0.5$ le due opinioni si fondono nella loro media; per $\mu$ piccolo si avvicinano di poco.

**Interpretazione.** La soglia $\varepsilon$ e' la "finestra di apertura" di ogni agente: si lascia influenzare solo da chi e' gia' abbastanza vicino. La distanza $1 - 2\varepsilon$ (approssimativamente) e' la "distanza di irrecuperabilita'": opinioni troppo lontane non convergono mai.

## 3.3 Il parametro $\mu$

Per $\mu = 0.5$, la regola diventa:

$$
x_i \leftarrow \frac{x_i + x_j}{2}, \qquad x_j \leftarrow \frac{x_i + x_j}{2}.
$$

Le due opinioni si fondono nella media aritmetica. Questo e' il caso piu' semplice e il piu' studiato.

Per $\mu < 0.5$, le due opinioni si avvicinano ma non si fondono. Questo e' piu' realistico: dopo un incontro, le posizioni convergono parzialmente, non completamente.

Per quasi tutte le analisi qualitative, il valore di $\mu$ non cambia la fenomenologia della transizione di fase (che dipende principalmente da $\varepsilon$), ma influisce sulla velocita' di convergenza.

## 3.4 Natura stocastica del modello

La stocasticita' del modello non sta nell'aggiornamento delle opinioni — che e' deterministico — ma nella **scelta casuale di quali agenti interagiscono** a ogni passo. Questo distingue il modello di Deffuant da altri modelli del corso:

- nelle SDE, il rumore e' nella dinamica individuale;
- nel modello di Vicsek, il rumore e' nell'allineamento angolare;
- in Deffuant, il rumore e' nella struttura delle interazioni.

Il risultato collettivo emerge dall'accumulo di molte interazioni casuali, nessuna delle quali e' di per se' determinante.

# 4. Fenomenologia: consenso e frammentazione

## 4.1 La transizione di fase

Il parametro piu' importante del modello e' la soglia di confidenza $\varepsilon$. Al variare di $\varepsilon$ si osservano due regimi qualitativamente diversi.

**Regime di consenso ($\varepsilon$ grande).** Se $\varepsilon$ e' grande, quasi tutte le coppie di agenti interagiscono. Le opinioni convergono verso un unico cluster centrale. Alla fine del processo, tutti gli agenti condividono la stessa opinione (o un'opinione molto simile).

**Regime di frammentazione ($\varepsilon$ piccolo).** Se $\varepsilon$ e' piccolo, solo le coppie molto vicine interagiscono. Si formano cluster separati di agenti con opinioni simili. I cluster non comunicano tra loro perche' la distanza tra cluster adiacenti supera $\varepsilon$. La distribuzione finale delle opinioni mostra picchi netti separati da gap vuoti.

**La transizione critica.** Esiste una soglia critica $\varepsilon_c$ che separa i due regimi. Per distribuzioni iniziali uniformi su $[0,1]$, il valore critico e' approssimativamente

$$
\varepsilon_c \approx \frac{1}{2k},
$$

dove $k$ e' il numero di cluster che si formano. In particolare, per $\varepsilon > 0.5$ il sistema converge quasi sempre a un unico consenso; per $\varepsilon < 0.5$ si formano piu' cluster.

Questa transizione e' uno dei risultati piu' importanti del modello: **non e' necessario che tutti siano molto chiusi per produrre polarizzazione**. Basta che la finestra di apertura sia inferiore alla meta' dell'intervallo delle opinioni.

## 4.2 Struttura dei cluster

Per $\varepsilon < 0.5$, il numero di cluster che si formano dipende da $\varepsilon$ in modo approssimato dalla relazione $k \approx 1/(2\varepsilon)$. Cluster piu' piccoli formano sistemi piu' polarizzati.

**Interpretazione scientifica.** Se i ricercatori accettano solo opinioni entro $\varepsilon = 0.2$ dalla propria, si formano circa due o tre scuole di pensiero che non comunicano piu' tra loro. Se $\varepsilon = 0.1$, le scuole diventano quattro o cinque. La frammentazione cresce al ridursi della apertura.

**Interpretazione negoziale.** Se le parti accettano di muoversi solo entro il 20% della distanza dalla propria posizione iniziale, il mercato si frammenta in gruppi di aziende che adottano standard incompatibili.

## 4.3 Dipendenza dalle condizioni iniziali

A differenza del modello di Vicsek o delle dinamiche replicative, il modello di Deffuant mostra una dipendenza relativamente debole dalle condizioni iniziali per distribuzioni iniziali omogenee. La struttura finale dipende principalmente da $\varepsilon$ e $\mu$.

Tuttavia, con distribuzioni iniziali non uniformi (ad esempio con cluster gia' presenti nelle opinioni iniziali, o con asimmetrie), l'esito finale puo' dipendere significativamente dalla configurazione iniziale.

# 5. Osservabili quantitative

## 5.1 Numero di cluster

Un cluster e' un insieme connesso di agenti con opinioni entro distanza $\varepsilon$ l'uno dall'altro (usando la stessa soglia del modello). Il numero di cluster $n_c$ misura il grado di frammentazione del sistema.

$$
n_c = 1: \text{ consenso}, \qquad n_c > 1: \text{ frammentazione}.
$$

## 5.2 Opinione media e varianza

L'opinione media:

$$
\bar x = \frac{1}{N} \sum_{i=1}^N x_i
$$

e' conservata nel tempo (ogni interazione somma zero alla media totale). Questo e' una proprieta' matematica della regola di aggiornamento simmetrica.

La varianza delle opinioni:

$$
\sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \bar x)^2
$$

e' invece decrescente nel tempo: le interazioni riducono sempre la dispersione delle opinioni. Questo fornisce un utile check numerico della simulazione.

## 5.3 Indice di polarizzazione

Una misura semplice di polarizzazione e' la distanza tra i cluster estremi:

$$
P = \max_i x_i - \min_i x_i
$$

nella distribuzione finale. Valori grandi indicano cluster molto distanti; valori vicini a zero indicano consenso.

Per una misura piu' robusta, si puo' usare la distanza tra il 10° e il 90° percentile della distribuzione finale.

## 5.4 Velocita' di convergenza

Si puo' misurare il numero di passi necessari per raggiungere lo stato finale (numero di cluster stabile). Questo dipende da $N$, $\varepsilon$ e $\mu$.

Per il caso $\mu = 0.5$, la convergenza e' tipicamente in $O(N^2)$ passi nel caso di consenso, e in $O(N)$ nel caso di frammentazione (i cluster si formano rapidamente e poi non cambiano piu').

## 5.5 Distribuzione delle opinioni

La visualizzazione piu' informativa e' l'istogramma delle opinioni al variare del tempo. Permette di vedere:

- la graduale concentrazione delle opinioni in cluster;
- il momento in cui i cluster si separano e smettono di interagire;
- la struttura finale stabile.

# 6. Il modello su rete

## 6.1 Motivazione

Nel modello base, ogni coppia di agenti ha la stessa probabilita' di interagire. Nella realta', le interazioni sono strutturate: si parla con chi e' vicino geograficamente, con i colleghi di lavoro, con chi si segue sui social media.

Si puo' introdurre una rete di interazioni: gli agenti sono i nodi, e a ogni passo si estrae casualmente un arco (coppia connessa) invece di una coppia qualsiasi.

## 6.2 Effetto della topologia

La topologia della rete influenza la fenomenologia in modo non banale.

**Grafo completo.** Tutti i nodi sono connessi. E' equivalente al modello base.

**Reticolo unidimensionale.** Ogni agente interagisce solo con i vicini immediati. La convergenza e' piu' lenta e i cluster sono piu' numerosi e piu' stabili, perche' le informazioni si propagano lentamente.

**Rete random (Erdos-Renyi).** Struttura intermedia. La convergenza dipende dalla densita' di archi.

**Rete scale-free.** Nodi ad alto grado (hub) accelerano la convergenza e tendono a trainare l'opinione di grandi porzioni della rete verso la propria posizione.

**Rete small-world.** La presenza di pochi archi lunghi (shortcuts) accelera molto la convergenza rispetto al reticolo, producendo risultati simili al grafo completo anche con molti meno archi.

## 6.3 Segregazione e echo chamber

Con reti in cui i nodi tendono a connettersi con nodi simili (assortative mixing), si formano facilmente echo chamber: regioni della rete in cui circolano solo opinioni simili. Questo amplifica la frammentazione e riduce la soglia critica di $\varepsilon$ per la formazione di cluster.

Questo e' uno dei meccanismi proposti per spiegare la polarizzazione nelle societa' in cui i social media incentivano la connessione con persone simili.

# 7. I due esempi a confronto

## 7.1 Struttura comune

| Elemento | Consenso scientifico | Negoziazione / adozione di standard |
|---|---|---|
| Agente $i$ | ricercatore | azienda o negoziatore |
| Opinione $x_i$ | stima dell'efficacia di un intervento | posizione su una variabile contrattuale |
| Soglia $\varepsilon$ | apertura a posizioni distanti | disponibilita' a fare concessioni |
| Interazione | lettura di un paper, discussione a conferenza | incontro di negoziazione |
| Consenso | convergenza verso una posizione condivisa | accordo su uno standard comune |
| Frammentazione | scuole di pensiero incompatibili | standard incompatibili, mercato frammentato |

## 7.2 Differenze interpretative

**Velocita' delle interazioni.** Nel mondo scientifico, le interazioni avvengono su anni (pubblicazioni, citazioni, convegni). In una negoziazione commerciale, possono avvenire in giorni o settimane. Questo influenza il numero di passi $T$ della simulazione, ma non la fenomenologia qualitativa.

**Simmetria dell'aggiornamento.** Nel modello base l'aggiornamento e' simmetrico: entrambe le parti si avvicinano ugualmente. In una negoziazione reale c'e' spesso asimmetria di potere: la parte piu' forte si muove di meno, la parte piu' debole di piu'. Questo si modella con un $\mu$ asimmetrico:

$$
x_i \leftarrow x_i + \mu_i (x_j - x_i), \qquad x_j \leftarrow x_j + \mu_j (x_i - x_j),
$$

con $\mu_i \ne \mu_j$.

**Irreversibilita' della frammentazione.** Nel consenso scientifico, un cluster di ricercatori che ha smesso di comunicare con gli altri puo' tornare a farlo se emergono nuove evidenze che cambiano le posizioni. Questo richiederebbe un'estensione del modello con aggiornamenti esogeni delle opinioni. Nella negoziazione commerciale, un accordo non raggiunto ha spesso conseguenze irreversibili (si adotta uno standard alternativo, il contratto va a un concorrente).

**Eterogeneita' della soglia.** Nel mondo scientifico, diversi ricercatori hanno diversi livelli di apertura intellettuale. Si puo' introdurre una soglia individuale $\varepsilon_i$ estratta da una distribuzione. Anche pochi agenti con $\varepsilon$ molto alto (mediatori, revisori) possono connettere cluster altrimenti separati.

## 7.3 Il messaggio metodologico

La stessa dinamica di bounded confidence produce sia il consenso scientifico sia l'accordo negoziale come casi dello stesso meccanismo: agenti aperti al compromesso si avvicinano, agenti troppo distanti rimangono separati. La soglia $\varepsilon$ e' il parametro di controllo che determina quale dei due esiti prevale.

Questo mostra che la polarizzazione non e' una patologia legata a contenuti specifici, ma una proprieta' emergente di qualsiasi sistema in cui gli agenti aggiornano le proprie posizioni solo in risposta a posizioni abbastanza simili alle proprie.

# 8. Connessioni con altri modelli del corso

## 8.1 Dinamiche replicative

Le dinamiche replicative descrivono come cambiano le frequenze di diverse strategie in una popolazione. Il modello di Deffuant descrive come cambiano le opinioni continue. La differenza principale e' che nelle dinamiche replicative la variabile di stato e' discreta (frequenza di ogni strategia) e l'aggiornamento e' proporzionale alla fitness, mentre in Deffuant la variabile e' continua e l'aggiornamento dipende dalla vicinanza.

In entrambi i casi, il risultato collettivo — quali strategie/opinioni sopravvivono — emerge da interazioni locali senza direzione centrale.

## 8.2 Modello di March

Il modello di March studia come la conoscenza organizzativa si formi attraverso l'interazione tra individui e un codice condiviso. La somiglianza con Deffuant e' nella struttura di aggiornamento: gli individui si avvicinano al codice (o ad altri individui), ma solo se la distanza e' entro certi limiti. La differenza e' che in March c'e' un mediatore esplicito (il codice organizzativo) e una variabile binaria (giusto/sbagliato rispetto alla realta' esterna).

## 8.3 Modello di Vicsek

Sia Vicsek che Deffuant producono una transizione di fase tra ordine (consenso/allineamento) e disordine (frammentazione/moto caotico). In Vicsek il parametro di controllo e' il rumore $\eta$; in Deffuant e' la soglia $\varepsilon$. In entrambi i casi, la transizione emerge da regole locali senza coordinazione centrale.

## 8.4 Epidemie su reti

La propagazione di un'opinione nella rete di Deffuant ha analogie con la diffusione di una malattia in un grafo. In entrambi i casi, la struttura della rete influenza la velocita' e l'estensione del contagio/convergenza. La differenza e' che la diffusione epidemica e' unidirezionale (suscettibile → infetto) mentre l'aggiornamento in Deffuant e' bidirezionale e simmetrico.

# 9. Domande scientifiche che il modello permette di studiare

Il modello e' utile per affrontare domande precise.

1. Come dipende il numero di cluster finali da $\varepsilon$? La relazione $k \approx 1/(2\varepsilon)$ e' verificata numericamente?
2. Esiste una transizione netta a $\varepsilon_c \approx 0.5$ o e' una transizione continua?
3. Come dipende la velocita' di convergenza da $N$, $\varepsilon$ e $\mu$?
4. Quanto e' sensibile il risultato finale alle condizioni iniziali (distribuzione non uniforme)?
5. Come la topologia della rete modifica la soglia critica e la struttura dei cluster?
6. L'introduzione di agenti con soglia alta (mediatori) puo' connettere cluster altrimenti separati?

# 10. Schema del laboratorio

## 10.1 Laboratorio 1 - Implementazione e visualizzazione della transizione

### Obiettivo

Implementare il modello di Deffuant e osservare la transizione tra consenso e frammentazione.

### Attivita'

1. implementare il modello con $N = 500$ agenti e $\mu = 0.5$;
2. simulare per $\varepsilon = 0.1$, $\varepsilon = 0.3$, $\varepsilon = 0.5$;
3. per ogni valore, visualizzare l'istogramma delle opinioni al tempo $t = 0$, $t = N$, $t = 10N$;
4. contare il numero di cluster finali.

### Domande guida

- per quale valore di $\varepsilon$ si forma un unico cluster?
- la transizione e' netta o graduale?
- quante iterazioni servono per raggiungere lo stato stabile?

### Output richiesto

- codice sorgente;
- istogrammi della distribuzione delle opinioni a diversi tempi per i tre valori di $\varepsilon$;
- tabella del numero di cluster in funzione di $\varepsilon$;
- commento interpretativo.

## 10.2 Laboratorio 2 - Mappa della transizione di fase

### Obiettivo

Costruire sistematicamente la relazione tra $\varepsilon$ e il numero di cluster finali.

### Attivita'

1. variare $\varepsilon$ su una griglia da 0.05 a 0.50 con passo 0.05;
2. per ogni valore, eseguire 20 run indipendenti;
3. stimare il numero medio di cluster finali e la varianza;
4. costruire il grafico di $n_c$ in funzione di $\varepsilon$.

### Domande guida

- la relazione $n_c \approx 1/(2\varepsilon)$ e' verificata?
- quanto e' variabile il numero di cluster tra run diverse con lo stesso $\varepsilon$?
- esiste una regione di $\varepsilon$ con alta variabilita' (zona di transizione)?

### Output richiesto

- grafico di $n_c(\varepsilon)$ con barre di errore;
- confronto con la formula teorica $k \approx 1/(2\varepsilon)$;
- commento sulla transizione.

## 10.3 Laboratorio 3 - Consenso scientifico vs negoziazione

### Obiettivo

Simulare i due contesti applicativi e mostrare come le stesse dinamiche producono risultati interpretabili in entrambi.

### Attivita'

**Contesto scientifico.**
1. inizializzare $N = 200$ ricercatori con opinioni uniformi su $[0,1]$;
2. simulare con $\varepsilon = 0.25$ (apertura moderata) e $\varepsilon = 0.15$ (apertura limitata);
3. misurare il numero di scuole di pensiero finali e la loro posizione.

**Contesto negoziale.**
4. inizializzare $N = 50$ aziende con posizioni uniformi su $[0,1]$;
5. simulare con $\mu$ asimmetrico: le aziende con posizioni alte si muovono meno ($\mu_i = 0.2$ se $x_i > 0.5$, $\mu_i = 0.5$ altrimenti);
6. confrontare con il caso simmetrico.

### Domande guida

- le due istanze del modello producono dinamiche visivamente diverse?
- l'asimmetria nel $\mu$ sposta il consenso verso uno dei due estremi?
- con $\varepsilon = 0.25$, quante scuole di pensiero si formano?

### Output richiesto

- istogrammi finali per i due contesti;
- confronto simmetrico vs asimmetrico;
- interpretazione in termini del contesto applicativo.

## 10.4 Laboratorio 4 - Effetto della rete

### Obiettivo

Confrontare la dinamica sul grafo completo, su un reticolo unidimensionale e su una rete small-world.

### Attivita'

1. implementare il modello su tre topologie con $N = 200$ agenti e $\varepsilon = 0.2$;
2. confrontare la velocita' di convergenza e il numero di cluster finali;
3. introdurre alcuni agenti con soglia alta ($\varepsilon_i = 0.5$) nella rete e verificare se riducono la frammentazione.

### Domande guida

- il reticolo unidimensionale frammenta di piu' del grafo completo?
- gli agenti con soglia alta (mediatori) riducono il numero di cluster?
- quanto sono necessari i mediatori? Quanti bastano?

### Output richiesto

- confronto delle distribuzioni finali per le tre topologie;
- esperimento con mediatori: numero di cluster vs numero di mediatori;
- commento sulla struttura della rete come fattore di polarizzazione.

# 11. Una possibile estensione teorica

## 11.1 Il modello di Hegselmann-Krause

Una variante molto studiata e' il modello di Hegselmann e Krause (HK), in cui ogni agente aggiorna la propria opinione come media di tutte le opinioni entro $\varepsilon$ dalla propria, non solo di quella di un singolo interlocutore casuale:

$$
x_i(t+1) = \frac{1}{|N_i(t)|} \sum_{j \in N_i(t)} x_j(t),
$$

dove $N_i(t) = \{j : |x_i(t) - x_j(t)| \le \varepsilon\}$.

Il modello HK e' deterministico (dati gli stati iniziali, la traiettoria e' determinata) mentre Deffuant e' stocastico (la scelta delle coppie e' casuale). Questa differenza produce risultati leggermente diversi nella struttura dei cluster, ma la fenomenologia qualitativa e' simile.

## 11.2 Opinioni multidimensionali

Si possono estendere i modelli a opinioni vettoriali $\mathbf{x}_i \in [0,1]^d$, dove ogni dimensione rappresenta una questione diversa. La condizione di interazione diventa $\|\mathbf{x}_i - \mathbf{x}_j\| \le \varepsilon$.

Con opinioni multidimensionali emergono fenomeni nuovi: la correlazione tra dimensioni, la formazione di cluster in spazi ad alta dimensione, e la possibilita' di accordo parziale (le due parti si avvicinano su alcune dimensioni ma non su altre).

## 11.3 Rumore esogeno

Si puo' aggiungere un termine di rumore all'aggiornamento:

$$
x_i \leftarrow x_i + \mu(x_j - x_i) + \sigma \xi_i,
$$

dove $\xi_i \sim \mathcal{N}(0,1)$ e $\sigma$ controlla l'intensita' del rumore. Il rumore puo' far scappare agenti da cluster gia' formati, introducendo dinamiche piu' ricche e reversibilita'.

# 12. Perche' questo e' un buon case study per il corso

Questo progetto e' particolarmente adatto a un corso di metodi computazionali per modelli stocastici per almeno cinque ragioni.

Primo, introduce una forma di stocasticita' non ancora incontrata nel corso: il rumore nelle interazioni, non nella dinamica individuale. Questo amplia il vocabolario metodologico degli studenti.

Secondo, la transizione di fase a $\varepsilon_c$ e' molto visibile e numericamente robusta, il che rende il laboratorio immediatamente gratificante: si vede chiaramente il momento in cui il sistema passa da consenso a frammentazione.

Terzo, i due esempi applicativi — consenso scientifico e negoziazione — mostrano come la stessa dinamica si legga in contesti molto diversi, con implicazioni diverse.

Quarto, la dipendenza dalla topologia della rete collega il progetto al modulo sulle epidemie su reti, creando una connessione tematica naturale.

Quinto, il tema della polarizzazione e' di grande attualita' e ha un'interpretazione immediata per gli studenti, il che facilita la motivazione.

# 13. Conclusione

Il modello di Deffuant mostra come la polarizzazione possa emergere spontaneamente da una regola di interazione molto semplice: le opinioni convergono solo tra chi e' gia' abbastanza d'accordo. Non serve malevolenza, non servono algoritmi di raccomandazione, non servono polarizzatori esterni. Basta che la finestra di apertura sia inferiore alla meta' dello spazio delle opinioni.

Il messaggio concettuale piu' importante e' che la soglia $\varepsilon$ e' il parametro critico: al di sopra di $\varepsilon_c$, l'apertura e' sufficiente perche' le opinioni si fondano; al di sotto, la chiusura e' sufficiente perche' si formino cluster irreversibili.

Dal punto di vista metodologico, il progetto combina in modo naturale:

- definizione di un agente con stato continuo;
- regola di interazione condizionata (bounded confidence);
- stocasticita' nella scelta delle interazioni;
- transizione di fase collettiva;
- osservabili quantitative (cluster, varianza, polarizzazione);
- effetto della topologia della rete;
- due contesti applicativi con la stessa struttura formale.

# 14. Bibliografia minima

1. Deffuant, G., Neau, D., Amblard, F., and Weisbuch, G. (2000). Mixing Beliefs among Interacting Agents. Advances in Complex Systems, 3(1-4), 87-98.
2. Hegselmann, R., and Krause, U. (2002). Opinion Dynamics and Bounded Confidence Models, Analysis, and Simulation. Journal of Artificial Societies and Social Simulation, 5(3).
3. Weisbuch, G., Deffuant, G., Amblard, F., and Nadal, J.-P. (2002). Meet, Discuss, and Segregate! Complexity, 7(3), 55-63.
4. Lorenz, J. (2007). Continuous Opinion Dynamics under Bounded Confidence: A Survey. International Journal of Modern Physics C, 18(12), 1819-1838.
5. Flache, A., Macy, M., Feliciani, T., Chattoe-Brown, E., Deffuant, G., Huet, S., and Lorenz, J. (2017). Models of Social Influence: Towards the Next Frontiers. Journal of Artificial Societies and Social Simulation, 20(4).

---

# Appendice A. Implementazione in Python: struttura del codice

Questa appendice propone una struttura semplice per implementare il modello di Deffuant e le analisi associate.

## A.1 Librerie minime

```python
import random
import math
import statistics
import matplotlib.pyplot as plt
```

## A.2 Inizializzazione

```python
def initialize_opinions(N):
    return [random.random() for _ in range(N)]
```

## A.3 Un passo del modello di Deffuant

```python
def deffuant_step(opinions, epsilon, mu=0.5):
    N = len(opinions)
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)

    while j == i:
        j = random.randint(0, N - 1)

    if abs(opinions[i] - opinions[j]) <= epsilon:
        diff = opinions[j] - opinions[i]
        opinions[i] += mu * diff
        opinions[j] -= mu * diff

    return opinions
```

## A.4 Simulazione completa

```python
def simulate_deffuant(N, epsilon, mu=0.5, T_factor=200):
    T = T_factor * N
    opinions = initialize_opinions(N)
    history = [opinions[:]]

    for t in range(T):
        opinions = deffuant_step(opinions, epsilon, mu)

        if t % N == 0:
            history.append(opinions[:])

    return opinions, history
```

Il parametro `T_factor` controlla quante iterazioni per agente. Con `T_factor = 200` si eseguono $200N$ passi, sufficienti per la convergenza nella maggior parte dei casi.

## A.5 Conteggio dei cluster

```python
def count_clusters(opinions, epsilon):
    sorted_ops = sorted(opinions)
    n_clusters = 1

    for i in range(1, len(sorted_ops)):
        if sorted_ops[i] - sorted_ops[i - 1] > epsilon:
            n_clusters += 1

    return n_clusters


def cluster_positions(opinions, epsilon):
    sorted_ops = sorted(opinions)
    clusters = []
    current_cluster = [sorted_ops[0]]

    for i in range(1, len(sorted_ops)):
        if sorted_ops[i] - sorted_ops[i - 1] > epsilon:
            clusters.append(current_cluster)
            current_cluster = [sorted_ops[i]]
        else:
            current_cluster.append(sorted_ops[i])

    clusters.append(current_cluster)
    return clusters
```

## A.6 Visualizzazione dell'evoluzione

```python
def plot_opinion_evolution(history, epsilon, title="Evoluzione delle opinioni"):
    n_snapshots = len(history)
    fig, axes = plt.subplots(1, n_snapshots, figsize=(4 * n_snapshots, 4),
                              sharey=True)

    for idx, (ax, opinions) in enumerate(zip(axes, history)):
        ax.hist(opinions, bins=40, range=(0, 1),
                orientation='horizontal', density=True)
        ax.set_ylim(0, 1)
        ax.set_title(f"t = {idx}")
        ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.3)

    axes[0].set_ylabel("opinione")
    fig.suptitle(f"{title} (epsilon={epsilon})")
    plt.tight_layout()
    plt.show()
```

## A.7 Mappa della transizione di fase

```python
def phase_diagram(N, epsilon_values, n_runs=20, mu=0.5, T_factor=200):
    mean_clusters = []
    std_clusters = []

    for epsilon in epsilon_values:
        cluster_counts = []

        for run in range(n_runs):
            final_opinions, _ = simulate_deffuant(N, epsilon, mu, T_factor)
            n_c = count_clusters(final_opinions, epsilon)
            cluster_counts.append(n_c)

        mean_clusters.append(statistics.mean(cluster_counts))
        std_clusters.append(statistics.stdev(cluster_counts)
                             if len(cluster_counts) > 1 else 0.0)

    return mean_clusters, std_clusters


def plot_phase_diagram(epsilon_values, mean_clusters, std_clusters):
    theoretical = [1.0 / (2.0 * eps) for eps in epsilon_values]

    plt.errorbar(epsilon_values, mean_clusters,
                 yerr=std_clusters, fmt='o-', label="simulazione")
    plt.plot(epsilon_values, theoretical, '--', label="teorico 1/(2eps)")
    plt.xlabel("soglia di confidenza epsilon")
    plt.ylabel("numero di cluster")
    plt.title("Transizione di fase nel modello di Deffuant")
    plt.legend()
    plt.show()
```

## A.8 Versione con mu asimmetrico (contesto negoziale)

```python
def deffuant_step_asymmetric(opinions, epsilon, mu_func):
    N = len(opinions)
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)

    while j == i:
        j = random.randint(0, N - 1)

    if abs(opinions[i] - opinions[j]) <= epsilon:
        mu_i = mu_func(opinions[i])
        mu_j = mu_func(opinions[j])

        diff = opinions[j] - opinions[i]
        opinions[i] += mu_i * diff
        opinions[j] -= mu_j * diff

    return opinions


def simulate_deffuant_asymmetric(N, epsilon, mu_func, T_factor=200):
    T = T_factor * N
    opinions = initialize_opinions(N)
    history = [opinions[:]]

    for t in range(T):
        opinions = deffuant_step_asymmetric(opinions, epsilon, mu_func)

        if t % N == 0:
            history.append(opinions[:])

    return opinions, history
```

Esempio di uso — aziende con posizioni alte si muovono meno:

```python
def mu_negotiation(x):
    return 0.2 if x > 0.5 else 0.5

final, history = simulate_deffuant_asymmetric(
    N=100, epsilon=0.3, mu_func=mu_negotiation
)
```

## A.9 Modello su rete

```python
def build_ring_network(N):
    adjacency = {i: [(i - 1) % N, (i + 1) % N] for i in range(N)}
    return adjacency


def build_complete_network(N):
    adjacency = {i: [j for j in range(N) if j != i] for i in range(N)}
    return adjacency


def build_small_world_network(N, k=4, p_rewire=0.1):
    adjacency = {i: [] for i in range(N)}

    for i in range(N):
        for delta in range(1, k // 2 + 1):
            j = (i + delta) % N
            adjacency[i].append(j)
            adjacency[j].append(i)

    edges = [(i, j) for i in range(N) for j in adjacency[i] if j > i]
    for i, j in edges:
        if random.random() < p_rewire:
            new_j = random.randint(0, N - 1)
            while new_j == i or new_j in adjacency[i]:
                new_j = random.randint(0, N - 1)
            adjacency[i].remove(j)
            adjacency[j].remove(i)
            adjacency[i].append(new_j)
            adjacency[new_j].append(i)

    return adjacency


def deffuant_step_network(opinions, epsilon, adjacency, mu=0.5):
    N = len(opinions)
    i = random.randint(0, N - 1)

    if not adjacency[i]:
        return opinions

    j = random.choice(adjacency[i])

    if abs(opinions[i] - opinions[j]) <= epsilon:
        diff = opinions[j] - opinions[i]
        opinions[i] += mu * diff
        opinions[j] -= mu * diff

    return opinions


def simulate_deffuant_network(N, epsilon, adjacency, mu=0.5, T_factor=200):
    T = T_factor * N
    opinions = initialize_opinions(N)

    for t in range(T):
        opinions = deffuant_step_network(opinions, epsilon, adjacency, mu)

    return opinions
```

## A.10 Esperimento con mediatori

```python
def simulate_with_mediators(N, epsilon_base, n_mediators,
                             epsilon_mediator=0.5, mu=0.5, T_factor=200):
    T = T_factor * N
    opinions = initialize_opinions(N)

    mediator_indices = random.sample(range(N), n_mediators)
    epsilons = [epsilon_base] * N
    for idx in mediator_indices:
        epsilons[idx] = epsilon_mediator

    for t in range(T):
        i = random.randint(0, N - 1)
        j = random.randint(0, N - 1)
        while j == i:
            j = random.randint(0, N - 1)

        eps_ij = min(epsilons[i], epsilons[j])

        if abs(opinions[i] - opinions[j]) <= eps_ij:
            diff = opinions[j] - opinions[i]
            opinions[i] += mu * diff
            opinions[j] -= mu * diff

    return opinions, count_clusters(opinions, epsilon_base)
```

## A.11 Esempio completo

```python
if __name__ == "__main__":
    N = 500
    mu = 0.5

    print("=== Visualizzazione della transizione ===")
    for eps in [0.1, 0.3, 0.5]:
        final, history = simulate_deffuant(N, epsilon=eps, mu=mu)
        n_c = count_clusters(final, eps)
        print(f"  epsilon={eps}: {n_c} cluster finali")
        plot_opinion_evolution(
            history[::max(1, len(history) // 5)],
            epsilon=eps,
            title=f"Deffuant (eps={eps})"
        )

    print("\n=== Diagramma di fase ===")
    eps_values = [0.05 * k for k in range(1, 11)]
    mean_c, std_c = phase_diagram(N=300, epsilon_values=eps_values, n_runs=20)
    plot_phase_diagram(eps_values, mean_c, std_c)

    print("\n=== Effetto della rete ===")
    for name, adj in [
        ("completo", build_complete_network(N)),
        ("anello", build_ring_network(N)),
        ("small world", build_small_world_network(N, k=4, p_rewire=0.1))
    ]:
        final = simulate_deffuant_network(N, epsilon=0.2, adjacency=adj)
        n_c = count_clusters(final, 0.2)
        print(f"  rete {name}: {n_c} cluster finali")
```

## A.12 Conclusione dell'appendice

L'implementazione proposta e' volutamente semplice: il modello base si scrive in una ventina di righe. La complessita' del progetto sta nella fenomenologia — la transizione di fase, il diagramma dei cluster, l'effetto della rete — non nell'implementazione.

Il punto metodologico centrale e' che la stocasticita' e' nella scelta di chi interagisce con chi, non nelle opinioni stesse. Questo rende il codice molto piu' semplice di un'SDE o di una simulazione a eventi discreti, pur producendo comportamenti collettivi ricchi e non banali.
