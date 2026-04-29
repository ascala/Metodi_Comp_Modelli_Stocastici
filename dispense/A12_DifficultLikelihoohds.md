# Appendice -- Likelihood intrattabile, momenti simulati e ABC

## A.1 Perché la likelihood può diventare intrattabile

Nei modelli semplici, la likelihood si scrive esplicitamente:

- dati i.i.d.:
  $$
  L(\theta)=\prod_i p(y_i\mid \theta)
  $$

- processi markoviani:
  $$
  L(\theta)=p(y_0\mid\theta)\prod_t p(y_{t+1}\mid y_t,\theta)
  $$

- SDE discretizzate:
  ogni incremento fornisce un contributo gaussiano approssimato.

In molti modelli stocastici realistici, però, il modello è facile da simulare ma difficile da valutare probabilisticamente.

Esempi:

- modelli agent-based;
- modelli su reti;
- processi con variabili latenti non osservate;
- modelli epidemici con osservazioni parziali;
- modelli di opinione con interazioni microscopiche non osservate;
- processi di salto ad alta dimensionalità.

In questi casi sappiamo generare dati simulati da $p(y\mid\theta)$, ma non sappiamo calcolare esplicitamente $p(y\mid\theta)$.

Questa è la situazione tipica della likelihood intrattabile:

$$
\theta \longrightarrow \text{simulazione} \longrightarrow y^{\mathrm{sim}},
$$

ma non abbiamo una formula utilizzabile per

$$
p(y^{\mathrm{obs}}\mid \theta).
$$

## A.2 Idea generale dei metodi simulation-based

Quando la likelihood non è calcolabile, si può comunque usare il simulatore.

L'idea è confrontare i dati osservati con dati generati dal modello per diversi valori dei parametri.

Schema generale:

1. si sceglie un valore candidato $\theta$;
2. si simulano dati $y^{\mathrm{sim}}(\theta)$;
3. si confrontano i dati simulati con quelli osservati;
4. si preferiscono i valori di $\theta$ che producono simulazioni simili ai dati.

Il punto delicato è definire che cosa significhi "simile".

Confrontare direttamente tutte le traiettorie è spesso impossibile. Si scelgono quindi alcune statistiche riassuntive:

$$
S(y) = (S_1(y),S_2(y),\dots,S_k(y)).
$$

Esempi:

- media;
- varianza;
- autocorrelazione;
- distribuzione dei tempi di attesa;
- dimensione finale di un'epidemia;
- tempo al picco;
- numero di cluster;
- frazione di agenti in uno stato.

Il confronto non avviene più tra dati grezzi, ma tra statistiche:

$$
S(y^{\mathrm{obs}}) \quad \text{e} \quad S(y^{\mathrm{sim}}(\theta)).
$$

## A.3 Metodo dei momenti

Il metodo dei momenti classico stima i parametri imponendo che alcuni momenti teorici coincidano con i momenti empirici.

Se il modello predice

$$
m(\theta)=\mathbb{E}_{\theta}[S(Y)]
$$

e i dati osservati forniscono

$$
S_{\mathrm{obs}}=S(y^{\mathrm{obs}}),
$$

si cerca $\theta$ tale che

$$
m(\theta)\approx S_{\mathrm{obs}}.
$$

Quando il numero di momenti coincide con il numero di parametri, si può talvolta risolvere direttamente il sistema:

$$
m(\theta)=S_{\mathrm{obs}}.
$$

Quando i momenti sono più numerosi dei parametri, si minimizza una distanza:

$$
\hat\theta
=
\arg\min_{\theta}
\left[
S_{\mathrm{obs}}-m(\theta)
\right]^T
W
\left[
S_{\mathrm{obs}}-m(\theta)
\right],
$$

dove $W$ è una matrice di pesi.

## A.4 Metodo dei momenti simulati

Se $m(\theta)$ non è disponibile analiticamente, ma il modello è simulabile, si approssima il momento teorico con una media Monte Carlo.

Per ogni valore candidato $\theta$, si generano $M$ simulazioni indipendenti:

$$
y^{(1)}(\theta),\dots,y^{(M)}(\theta).
$$

Poi si calcola

$$
\hat m_M(\theta)
=
\frac{1}{M}
\sum_{r=1}^M S(y^{(r)}(\theta)).
$$

Lo stimatore SMM è

$$
\hat\theta_{\mathrm{SMM}}
=
\arg\min_{\theta}
\left[
S_{\mathrm{obs}}-\hat m_M(\theta)
\right]^T
W
\left[
S_{\mathrm{obs}}-\hat m_M(\theta)
\right].
$$

Interpretazione:

- la likelihood non viene calcolata;
- il simulatore sostituisce il calcolo analitico dei momenti;
- i parametri sono scelti perché riproducono statistiche osservate.

## A.5 Scelta delle statistiche riassuntive

La scelta di $S(y)$ è il cuore del metodo.

Statistiche troppo povere possono non identificare i parametri.  
Statistiche troppo numerose possono rendere il confronto instabile.

Buone statistiche dovrebbero essere:

1. informative rispetto ai parametri;
2. robuste al rumore;
3. facili da calcolare;
4. interpretabili;
5. possibilmente poco ridondanti.

Esempio: modello epidemico SIR stocastico.

Parametri:

$$
\theta=(\beta,\gamma).
$$

Statistiche possibili:

$$
S(y)=
\left(
\text{dimensione finale},
\text{tempo del picco},
\text{altezza del picco}
\right).
$$

La dimensione finale è sensibile a $R_0=\beta/\gamma$; il tempo del picco e l'altezza del picco aiutano a distinguere $\beta$ e $\gamma$.

## A.6 Approximate Bayesian Computation

ABC nasce in un contesto bayesiano.

Si parte da una distribuzione a priori sui parametri:

$$
\pi(\theta).
$$

Se la likelihood fosse disponibile, il posterior sarebbe

$$
\pi(\theta\mid y^{\mathrm{obs}})
\propto
p(y^{\mathrm{obs}}\mid\theta)\pi(\theta).
$$

Quando $p(y^{\mathrm{obs}}\mid\theta)$ è intrattabile, ABC sostituisce il calcolo della likelihood con una procedura di simulazione e accettazione.

Algoritmo ABC rejection:

1. estrai un parametro
   $$
   \theta \sim \pi(\theta);
   $$

2. simula dati dal modello
   $$
   y^{\mathrm{sim}}\sim p(\cdot\mid\theta);
   $$

3. calcola le statistiche
   $$
   S(y^{\mathrm{sim}}), \qquad S(y^{\mathrm{obs}});
   $$

4. accetta $\theta$ se
   $$
   d\left(S(y^{\mathrm{sim}}),S(y^{\mathrm{obs}})\right)<\varepsilon.
   $$

I parametri accettati approssimano il posterior.

## A.7 Ruolo della soglia $\varepsilon$

La soglia $\varepsilon$ controlla il compromesso tra accuratezza e costo computazionale.

Se $\varepsilon$ è grande:

- si accettano molti parametri;
- il metodo è efficiente;
- l'approssimazione è grossolana.

Se $\varepsilon$ è piccola:

- si accettano pochi parametri;
- il metodo è costoso;
- l'approssimazione è più vicina al posterior ideale.

Nel limite ideale,

$$
\varepsilon \to 0,
$$

e se le statistiche $S(y)$ sono sufficienti, ABC recupera il posterior esatto. Nella pratica, però, le statistiche raramente sono sufficienti e $\varepsilon$ non può essere troppo piccola.

## A.8 Distanza fra dati osservati e simulati

Una scelta comune è la distanza euclidea normalizzata:

$$
d(S_{\mathrm{sim}},S_{\mathrm{obs}})
=
\sqrt{
\sum_{j=1}^k
\left(
\frac{
S_j^{\mathrm{sim}}-S_j^{\mathrm{obs}}
}{
s_j
}
\right)^2
},
$$

dove $s_j$ è una scala caratteristica della statistica $j$.

La normalizzazione è essenziale: senza di essa, statistiche con valori numericamente grandi dominano la distanza.

Una scelta più generale usa una matrice di pesi:

$$
d^2
=
(S_{\mathrm{sim}}-S_{\mathrm{obs}})^T
W
(S_{\mathrm{sim}}-S_{\mathrm{obs}}).
$$

## A.9 Differenza concettuale fra SMM e ABC

SMM produce tipicamente una stima puntuale:

$$
\hat\theta_{\mathrm{SMM}}.
$$

ABC produce invece un insieme di parametri accettati, interpretabile come approssimazione della distribuzione posterior:

$$
\pi_{\varepsilon}(\theta\mid S(y^{\mathrm{obs}})).
$$

In forma sintetica:

| Metodo | Output                               | Filosofia                            | Oggetto confrontato    |
| ------ | ------------------------------------ | ------------------------------------ | ---------------------- |
| MLE    | stima puntuale                       | massimizzare la likelihood           | dati osservati         |
| SMM    | stima puntuale                       | riprodurre statistiche osservate     | momenti/statistiche    |
| ABC    | distribuzione posterior approssimata | accettare simulazioni simili ai dati | statistiche e distanza |

## A.10 Esempio didattico: modello di opinioni di Deffuant

Nel modello di Deffuant, ogni agente ha un'opinione continua $x_i\in[0,1]$.

A ogni passo:

1. si scelgono due agenti $i,j$;
2. se
   $$
   |x_i-x_j|<\epsilon,
   $$
   interagiscono;
3. le opinioni si avvicinano:
   $$
   x_i \leftarrow x_i + \mu(x_j-x_i),
   $$
   $$
   x_j \leftarrow x_j + \mu(x_i-x_j).
   $$

I parametri sono:

$$
\theta=(\epsilon,\mu).
$$

La likelihood della configurazione finale è difficile da scrivere, perché dipende da una lunga storia di interazioni non osservate.

Tuttavia il modello è facile da simulare.

Statistiche possibili:

$$
S(y)=
\left(
\text{numero di cluster},
\text{varianza finale},
\text{polarizzazione}
\right).
$$

Si può quindi stimare $\epsilon$ e $\mu$ cercando simulazioni che riproducano queste statistiche.

## A.11 Limiti dei metodi likelihood-free

I metodi likelihood-free sono potenti ma non gratuiti.

Problemi principali:

1. costo computazionale elevato;
2. dipendenza forte dalla scelta delle statistiche;
3. perdita di informazione rispetto ai dati completi;
4. difficoltà di identificabilità;
5. sensibilità alla distanza scelta;
6. incertezza Monte Carlo dovuta al numero finito di simulazioni.

Una buona pratica è sempre controllare se parametri diversi producono statistiche simili. In tal caso il problema è poco identificabile.

## A.12 Messaggio finale

I metodi SMM e ABC sono utili quando:

- il modello è facile da simulare;
- la likelihood è assente, costosa o intrattabile;
- esistono statistiche riassuntive informative;
- si accetta un compromesso fra rigore analitico e praticabilità computazionale.

La domanda operativa diventa:

non "qual è la probabilità esatta dei dati?",

ma

"quali parametri producono simulazioni statisticamente simili ai dati osservati?".