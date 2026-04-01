---
title: "08: Stima dei parametri e confronto modello-dati"
author: ""
date: ""
---

In un corso di metodi computazionali per modelli stocastici, la simulazione è spesso la direzione diretta: si fissano i parametri e si generano traiettorie. Ma nella pratica scientifica si percorre quasi sempre la direzione inversa: si osservano dati reali e si vogliono stimare i parametri del modello che li ha generati, oppure si vuole valutare quanto bene un modello proposto è compatibile con i dati osservati.

Questa lezione introduce il framework dell'inferenza per modelli stocastici. Il punto di partenza è la likelihood -- la probabilità dei dati come funzione dei parametri -- e il metodo della massima verosimiglianza come strumento di stima. Poi si discute come valutare la bontà di adattamento di un modello. Infine si affrontano i casi in cui la likelihood non è calcolabile analiticamente, che sono molto comuni nei modelli stocastici complessi, e si introducono metodi computazionali per aggirarli.

La struttura è la seguente: la teoria è sviluppata in modo generale, ma ogni concetto è illustrato con esempi tratti direttamente dai modelli del corso.

### Obiettivi didattici specifici

Al termine della lezione lo studente dovrà essere in grado di:

1. definire la likelihood e la log-likelihood per dati indipendenti e per processi stocastici;
2. impostare e risolvere numericamente il problema di massima verosimiglianza per modelli semplici;
3. interpretare la Fisher information come misura della precisione della stima;
4. confrontare un modello stocastico con dati tramite QQ-plot, KS test e altre diagnostiche;
5. applicare il metodo dei momenti simulati quando la likelihood è costosa o intrattabile;
6. comprendere la logica dell'ABC (Approximate Bayesian Computation) per modelli agent-based.

### Struttura

1. Dalla simulazione all'inferenza: la direzione inversa
2. Likelihood e log-likelihood
3. Massima verosimiglianza: teoria e pratica computazionale
4. Informazione di Fisher e precisione della stima
5. Confronto modello-dati: diagnostiche e goodness-of-fit
6. Quando la likelihood è intrattabile: momenti simulati
7. Approximate Bayesian Computation
8. Sintesi: quale metodo per quale modello

---

# 1. Dalla simulazione all'inferenza: la direzione inversa

In tutti i modelli visti finora abbiamo sempre operato nella direzione diretta:

$$
\text{parametri} \xrightarrow{\text{simulazione}} \text{dati simulati}.
$$

Nell'uso scientifico reale si percorre quasi sempre la direzione opposta:

$$
\text{dati osservati} \xrightarrow{\text{inferenza}} \text{stima dei parametri}.
$$

Questa inversione non è banale. Dato un insieme di osservazioni $y_1, y_2, \dots, y_n$, si vuole rispondere a domande del tipo:

- qual è il valore di $\lambda$ in un processo di Poisson che ha generato questa sequenza di eventi?
- quali sono il drift $\mu$ e la diffusione $\sigma$ della SDE che ha prodotto questa traiettoria?
- il modello SIR con parametri $\beta$ e $\gamma$ è compatibile con questa curva epidemica?

Due aspetti rendono l'inferenza per modelli stocastici diversa dall'inferenza classica.

**Stocasticità intrinseca.** Il modello non fa previsioni deterministiche ma probabilistiche. Non si cerca la previsione perfetta ma i parametri che rendono i dati osservati il più plausibili possibile.

**Likelihood spesso complicata.** Per molti modelli del corso -- processi di salto, SDE con rumore moltiplicativo, modelli agent-based -- la probabilità di osservare i dati come funzione dei parametri non ha una forma analitica semplice. Questo richiede metodi computazionali specifici.

# 2. Likelihood e log-likelihood

## 2.1 Definizione per dati indipendenti

Sia $y_1, \dots, y_n$ un campione di osservazioni indipendenti, ciascuna distribuita secondo una densità $p(y \mid \theta)$ parametrizzata da $\theta$.

La **likelihood** è la funzione

$$
L(\theta) = \prod_{i=1}^n p(y_i \mid \theta).
$$

Si legge come: la probabilità di osservare esattamente questo campione, al variare di $\theta$. Non è la probabilità di $\theta$ dati i dati -- quella è l'oggetto della statistica bayesiana -- ma la probabilità dei dati come funzione del parametro.

La **log-likelihood** è

$$
\ell(\theta) = \log L(\theta) = \sum_{i=1}^n \log p(y_i \mid \theta).
$$

Lavorare con la log-likelihood è quasi sempre preferibile: trasforma il prodotto in somma, evita underflow numerici, e spesso ha forma più semplice.

**Esempio: processo di Poisson.** Se si osservano $n$ intervalli tra eventi $\{s_1, \dots, s_n\}$ da un processo di Poisson omogeneo con tasso $\lambda$, si ha $p(s_i \mid \lambda) = \lambda e^{-\lambda s_i}$ e

$$
\ell(\lambda) = n \log \lambda - \lambda \sum_{i=1}^n s_i.
$$

Massimizzando si ottiene $\hat\lambda = n / \sum_i s_i = 1/\bar s$, il reciproco del tempo interarrivo medio. Intuitivo e semplice.

## 2.2 Likelihood per processi stocastici

Quando i dati non sono i.i.d. ma formano una sequenza temporale, la likelihood si fattorizza usando la probabilità condizionata:

$$
L(\theta) = p(y_1 \mid \theta) \prod_{t=2}^n p(y_t \mid y_1, \dots, y_{t-1}, \theta).
$$

Per una catena di Markov del primo ordine la memoria si riduce a un solo passo:

$$
L(\theta) = p(y_1 \mid \theta) \prod_{t=2}^n p(y_t \mid y_{t-1}, \theta).
$$

Questo schema si applica direttamente a molti modelli del corso.

**Esempio: SDE discrettizzata (Euler-Maruyama).** Per la SDE $dX_t = a(X_t;\theta) dt + b(X_t;\theta) dW_t$ osservata su una griglia $\{t_0, t_1, \dots, t_n\}$ con passo $\Delta t$, lo schema Euler-Maruyama implica

$$
X_{t+\Delta t} \mid X_t \sim \mathcal{N}\!\left(X_t + a(X_t;\theta)\Delta t,\; b(X_t;\theta)^2 \Delta t\right).
$$

La log-likelihood è quindi

$$
\ell(\theta) = -\frac{n}{2}\log(2\pi) - \sum_{t} \log b(X_t;\theta)\sqrt{\Delta t} - \sum_{t} \frac{(X_{t+\Delta t} - X_t - a(X_t;\theta)\Delta t)^2}{2\,b(X_t;\theta)^2\,\Delta t}.
$$

Ogni incremento osservato $\Delta X_t = X_{t+\Delta t} - X_t$ contribuisce alla likelihood come una gaussiana centrata sul drift atteso e con varianza proporzionale alla diffusione e al passo temporale.

**Esempio: processo puntuale con intensità condizionata.** Per una sequenza di eventi $\{t_1, \dots, t_n\}$ osservati su $[0,T]$ con intensità condizionata $\lambda^*(t)$, la log-likelihood è

$$
\ell(\theta) = \sum_{k=1}^n \log \lambda^*(t_k) - \int_0^T \lambda^*(t)\,dt.
$$

Il primo termine premia i modelli che assegnano alta intensità nei momenti in cui gli eventi accadono; il secondo penalizza i modelli che prevedono troppi eventi dove non ce ne sono. Per il kernel esponenziale del processo di Hawkes entrambi i termini si calcolano in $O(n)$ operazioni.

## 2.3 Likelihood per il processo di branching (Galton-Watson)

Per un processo di branching con distribuzione di prole $\{p_k\}$ osservato per $T$ generazioni, si contano le coppie $(N_t, N_{t+1})$. La log-likelihood è

$$
\ell = \sum_{t=1}^T \sum_{k=0}^\infty c_{t,k} \log p_k,
$$

dove $c_{t,k}$ è il numero di individui alla generazione $t$ che hanno prodotto esattamente $k$ discendenti. Se si osserva solo la dimensione totale per generazione (non i singoli alberi), la likelihood si complica e in generale non è trattabile analiticamente.

# 3. Massima verosimiglianza: teoria e pratica computazionale

## 3.1 Lo stimatore di massima verosimiglianza

Lo **stimatore di massima verosimiglianza** (MLE) è

$$
\hat\theta = \arg\max_\theta \ell(\theta).
$$

In alcuni casi la massimizzazione ha soluzione in forma chiusa. Negli altri è un problema di ottimizzazione numerica.

**Esempi con soluzione chiusa.** Per la distribuzione esponenziale: $\hat\lambda = 1/\bar s$. Per la distribuzione gaussiana: $\hat\mu = \bar y$, $\hat\sigma^2 = \frac{1}{n}\sum(y_i - \bar y)^2$. Per la distribuzione di Poisson: $\hat\lambda = \bar y$. Per il processo di Hawkes con kernel esponenziale: non c'è forma chiusa, serve ottimizzazione numerica.

## 3.2 Massimizzazione numerica

Quando la soluzione chiusa non esiste, si massimizza $\ell(\theta)$ numericamente. Per parametri con vincoli di positività (tassi, varianze, scale) conviene lavorare con la trasformazione logaritmica: $\phi = \log\theta$, ottimizzare in $\phi$ senza vincoli, poi riportare a $\theta = e^\phi$.

Il metodo L-BFGS-B di `scipy.optimize.minimize` (con segno cambiato perché minimizza) è la scelta standard per problemi con pochi parametri e log-likelihood differenziabile.

Una questione pratica importante: la log-likelihood di processi stocastici ha spesso più massimi locali, soprattutto con pochi dati. Conviene provare più punti di partenza e confrontare i risultati.

## 3.3 Il metodo dei momenti come alternativa semplice

Prima di ottimizzare la likelihood, vale sempre la pena provare il **metodo dei momenti**: si eguagliano i momenti teorici del modello alle loro controparti empiriche e si risolve per i parametri.

**Esempio: distribuzione di Weibull.** Se si osservano $n$ tempi di vita $\{t_1, \dots, t_n\}$ con distribuzione Weibull di forma $k$ e scala $\lambda$, i momenti teorici sono

$$
\mathbb{E}[T] = \lambda\,\Gamma(1+1/k), \qquad \mathbb{E}[T^2] = \lambda^2\,\Gamma(1+2/k).
$$

Eguagliando media e varianza empiriche ai valori teorici si ottiene un sistema di due equazioni in $k$ e $\lambda$, risolvibile numericamente.

Il metodo dei momenti è meno efficiente statisticamente del MLE (nel senso che usa meno informazione), ma è computazionalmente molto più semplice e spesso sufficiente come stima iniziale.

# 4. Informazione di Fisher e precisione della stima

## 4.1 Varianza dello stimatore MLE

Lo stimatore MLE ha due proprietà asintotiche fondamentali:

1. **consistenza**: $\hat\theta \to \theta_0$ quando $n \to \infty$, dove $\theta_0$ è il valore vero;
2. **normalità asintotica**: per $n$ grande,

$$
\hat\theta \approx \mathcal{N}\!\left(\theta_0, \frac{1}{n\,\mathcal{I}(\theta_0)}\right),
$$

dove $\mathcal{I}(\theta)$ è la **informazione di Fisher**.

## 4.2 Informazione di Fisher

La informazione di Fisher è

$$
\mathcal{I}(\theta) = -\mathbb{E}\!\left[\frac{\partial^2 \log p(y \mid \theta)}{\partial \theta^2}\right] = \mathbb{E}\!\left[\left(\frac{\partial \log p(y \mid \theta)}{\partial \theta}\right)^2\right].
$$

Misura la curvatura media della log-likelihood attorno al vero parametro: una curvatura alta significa che la likelihood è molto concentrata attorno al massimo, quindi la stima è precisa; una curvatura bassa significa che la likelihood è piatta e la stima è imprecisa.

**Esempio: processo di Poisson.** Per $n$ osservazioni indipendenti da $\mathrm{Exp}(\lambda)$, la log-likelihood è $\ell(\lambda) = n\log\lambda - \lambda\sum s_i$. La sua derivata seconda è $\ell''(\lambda) = -n/\lambda^2$. Quindi $\mathcal{I}(\lambda) = 1/\lambda^2$ e la varianza asintotica di $\hat\lambda$ è $\lambda^2/n$. Con più dati la stima migliora come $1/\sqrt{n}$.

## 4.3 Standard error numerico

Quando la forma analitica di $\mathcal{I}(\theta)$ non è disponibile, si stima la varianza dello stimatore numericamente come l'inverso della derivata seconda (Hessiana) della log-likelihood valutata in $\hat\theta$:

$$
\widehat{\mathrm{Var}}(\hat\theta) \approx \left(-\ell''(\hat\theta)\right)^{-1}.
$$

In Python, `scipy.optimize.minimize` restituisce (opzionalmente) la Hessiana numerica. In alternativa si usa `numdifftools.Hessian` per calcolarla.

## 4.4 Intervalli di confidenza

Un intervallo di confidenza approssimato al 95% per $\theta$ è

$$
\hat\theta \pm 1.96 \cdot \widehat{\mathrm{se}}(\hat\theta),
$$

dove $\widehat{\mathrm{se}} = \sqrt{\widehat{\mathrm{Var}}(\hat\theta)}$.

Questo funziona bene quando la distribuzione asintotica gaussiana è una buona approssimazione, cioè quando $n$ è sufficientemente grande. Per campioni piccoli o parametri con vincoli, si preferisce il **profile likelihood** o metodi bootstrap.

# 5. Confronto modello-dati: diagnostiche e goodness-of-fit

Stimare i parametri è solo il primo passo. Il secondo è verificare che il modello con i parametri stimati sia effettivamente compatibile con i dati. Questa fase si chiama **goodness-of-fit** o diagnostica del modello.

## 5.1 Il QQ-plot

Il QQ-plot (quantile-quantile plot) confronta i quantili empirici dei dati con i quantili teorici del modello. Se il modello è corretto, i punti cadono approssimativamente sulla bisettrice.

**Come costruirlo.** Si ordinano i dati: $y_{(1)} \le y_{(2)} \le \dots \le y_{(n)}$. Si calcolano i quantili teorici corrispondenti: $q_i = F^{-1}((i-0.5)/n)$, dove $F^{-1}$ è il quantile della distribuzione con i parametri stimati. Si traccia il grafico $(q_i, y_{(i)})$.

Il QQ-plot è molto sensibile alle code: se i dati hanno code più pesanti del modello, i punti nelle estremità si allontanano dalla bisettrice verso l'alto a destra e verso il basso a sinistra.

## 5.2 Il test di Kolmogorov-Smirnov

Il test KS misura la distanza massima tra la CDF empirica $\hat F_n$ e la CDF teorica $F_\theta$:

$$
D_n = \sup_x \left|\hat F_n(x) - F_\theta(x)\right|.
$$

Sotto l'ipotesi nulla che i dati siano generati da $F_\theta$, la distribuzione di $D_n$ è nota (per campioni grandi). Si calcola il p-value corrispondente al valore osservato.

**Nota importante.** Il test KS nella sua forma standard assume che i parametri $\theta$ siano noti, non stimati dai dati. Quando si usano i parametri stimati con MLE, il test diventa conservativo (il p-value è sovrastimato). Per parametri stimati, il test di Anderson-Darling o il test di Cramér-von Mises sono più appropriati.

## 5.3 Diagnostica per processi puntuali: residui trasformati

Per un processo puntuale con intensità condizionata $\lambda^*(t)$, il **teorema di rescaling** (Papangelou, 1972) dice che se il modello è corretto, i tempi trasformati

$$
\tau_k = \int_0^{t_k} \lambda^*(s)\,ds
$$

formano un processo di Poisson omogeneo con tasso 1. Quindi i tempi inter-evento trasformati $\tau_k - \tau_{k-1}$ devono essere distribuiti come $\mathrm{Exp}(1)$.

La diagnostica consiste nel calcolare i residui trasformati e verificare questa proprietà con un QQ-plot o un test KS contro $\mathrm{Exp}(1)$. Se il grafico mostra deviazioni sistematiche (punti curvi invece che sulla bisettrice), il modello è mal specificato -- ad esempio il kernel ha la forma sbagliata, o mancano covariate.

## 5.4 Confronto tra distribuzioni simulate e osservate

Per i modelli in cui si può simulare facilmente ma la CDF teorica non è disponibile in forma chiusa -- come i modelli agent-based (Vicsek, March, Deffuant) -- si confrontano le distribuzioni empiriche di dati reali e dati simulati.

Il procedimento è:

1. stimare i parametri con il metodo dei momenti o con MLE approssimata;
2. simulare $M$ traiettorie con quei parametri;
3. raccogliere una statistica di interesse (ad esempio la distribuzione del parametro d'ordine finale, o la distribuzione dei tempi di primo passaggio);
4. confrontare con la distribuzione della stessa statistica nei dati reali tramite QQ-plot o KS test.

Se le due distribuzioni concordano, il modello è almeno non rifiutato dai dati. Questo non prova che il modello sia corretto -- altri modelli potrebbero produrre la stessa distribuzione -- ma è la forma più onesta di confronto disponibile quando la likelihood è intrattabile.

## 5.5 AIC e BIC per la selezione del modello

Quando si confrontano più modelli alternativi, non basta guardare il valore della log-likelihood al massimo: un modello con più parametri si adatta sempre meglio ai dati. Si usano criteri penalizzati:

$$
\mathrm{AIC} = -2\ell(\hat\theta) + 2p,
$$

$$
\mathrm{BIC} = -2\ell(\hat\theta) + p\log n,
$$

dove $p$ è il numero di parametri. Si preferisce il modello con AIC (o BIC) minore. BIC penalizza i modelli complessi più di AIC ed è asintoticamente consistente nella selezione del modello vero.

# 6. Quando la likelihood è intrattabile: momenti simulati

## 6.1 Il problema della likelihood intrattabile

Per molti modelli del corso, la likelihood non è disponibile in forma analitica. Questo accade quando:

- il modello ha variabili latenti non osservate (ad esempio, si osserva solo la dimensione della popolazione, non i singoli alberi di discendenza nel branching);
- il modello è un agente-based con molte interazioni locali (Vicsek, March, Deffuant);
- la likelihood richiede di sommare su uno spazio di stati esponenzialmente grande.

In questi casi non si può massimizzare la likelihood direttamente. Si usano approcci che la aggirano.

## 6.2 Il metodo dei momenti simulati (SMM)

L'idea è semplice: invece di confrontare la likelihood dei dati, si confrontano statistiche aggregate (momenti o altre quantità sommarie) calcolate sui dati reali con le stesse statistiche calcolate su dati simulati.

Sia $m_{\mathrm{obs}}$ un vettore di statistiche osservate (ad esempio: media, varianza, autocorrelazione a lag 1, percentile 90%). Sia $m_{\mathrm{sim}}(\theta)$ la stessa statistica calcolata su dati simulati con parametri $\theta$.

Lo stimatore SMM minimizza la distanza quadratica pesata:

$$
\hat\theta_{\mathrm{SMM}} = \arg\min_\theta \left[m_{\mathrm{obs}} - m_{\mathrm{sim}}(\theta)\right]^T W \left[m_{\mathrm{obs}} - m_{\mathrm{sim}}(\theta)\right],
$$

dove $W$ è una matrice di pesi (spesso l'identità in prima approssimazione).

**Come si calcola $m_{\mathrm{sim}}(\theta)$ in pratica.** Per ogni valore di $\theta$ nel processo di ottimizzazione, si generano $M$ traiettorie simulate, si calcolano le statistiche su ognuna, e si fa la media. Con $M$ grande, $m_{\mathrm{sim}}(\theta)$ è una stima precisa dell'atteso.

**Scelta delle statistiche.** Le statistiche scelte devono essere **informative** rispetto ai parametri di interesse -- cioè sensibili alle variazioni di $\theta$ -- e **riproducibili** dalla simulazione. Statistiche naturali per i modelli del corso includono:

- per le SDE: media, varianza e autocorrelazione a diversi lag della traiettoria discreta;
- per i processi di branching: numero medio di discendenti, varianza della dimensione per generazione;
- per i modelli agent-based: distribuzione del parametro d'ordine finale, tempo di convergenza.

**Esempio: modello di Deffuant.** Si osservano dati empirici sulla distribuzione delle opinioni in una comunità (ad esempio da survey). Si vogliono stimare $\varepsilon$ e $\mu$. La likelihood è intrattabile. Si usano come statistiche: il numero di cluster finali, la deviazione standard delle opinioni finali, la posizione del cluster maggioritario. Per ogni coppia $(\varepsilon, \mu)$ si simula il modello $M$ volte e si confrontano queste statistiche con quelle osservate.

## 6.3 Ottimizzazione del SMM

Il problema di minimizzazione del SMM ha due difficoltà pratiche.

**Rumore nella simulazione.** $m_{\mathrm{sim}}(\theta)$ è una media su $M$ simulazioni, quindi è rumorosa. Il paesaggio di ottimizzazione è rumoroso. Metodi gradient-free come Nelder-Mead o simulated annealing funzionano meglio dei metodi basati sul gradiente.

**Costo computazionale.** Ogni valutazione della funzione obiettivo richiede $M$ simulazioni. Per modelli lenti e $M$ grande, l'ottimizzazione può essere costosa. Si inizia con $M$ piccolo per esplorare, poi si affina con $M$ grande vicino al minimo.

# 7. Approximate Bayesian Computation

## 7.1 L'idea bayesiana

Nel framework bayesiano, si vuole calcolare la distribuzione a posteriori dei parametri dati i dati:

$$
p(\theta \mid y_{\mathrm{obs}}) \propto p(y_{\mathrm{obs}} \mid \theta) \cdot p(\theta),
$$

dove $p(\theta)$ è il prior e $p(y_{\mathrm{obs}} \mid \theta) = L(\theta)$ è la likelihood.

Se la likelihood è nota, si usa MCMC per campionare dalla posteriore (come visto nella Lec03). Se la likelihood è intrattabile, questo non funziona direttamente.

## 7.2 ABC rejection sampler

L'**Approximate Bayesian Computation** (ABC) aggira il calcolo della likelihood sostituendolo con un confronto tra dati osservati e dati simulati.

Lo schema di base (ABC rejection) è:

1. campiona $\theta \sim p(\theta)$ dal prior;
2. simula dati $y_{\mathrm{sim}} \sim p(\cdot \mid \theta)$;
3. calcola una statistica sommaria $s(y_{\mathrm{sim}})$ e confronta con $s(y_{\mathrm{obs}})$;
4. accetta $\theta$ se $d(s(y_{\mathrm{sim}}), s(y_{\mathrm{obs}})) \le \varepsilon_{\mathrm{ABC}}$;
5. ripeti finche' non si hanno abbastanza campioni accettati.

I campioni accettati formano un'approssimazione della posteriore $p(\theta \mid y_{\mathrm{obs}})$ -- tanto più fedele quanto più piccolo è $\varepsilon_{\mathrm{ABC}}$ e quanto più informativa è la statistica sommaria $s$.

**Il parametro $\varepsilon_{\mathrm{ABC}}$.** Con $\varepsilon_{\mathrm{ABC}} = 0$ si accetterebbe solo quando $y_{\mathrm{sim}} = y_{\mathrm{obs}}$ esattamente -- impossibile per dati continui. Con $\varepsilon_{\mathrm{ABC}}$ grande si accettano molti campioni ma la posteriore è troppo piatta. Il valore di $\varepsilon_{\mathrm{ABC}}$ si sceglie come compromesso tra precisione e tasso di accettazione.

**Scelta della statistica sommaria.** Come per SMM, la statistica sommaria deve essere informativa rispetto ai parametri. Se $s$ è una statistica sufficiente, ABC con $\varepsilon_{\mathrm{ABC}} \to 0$ converge alla vera posteriore. In pratica le statistiche sufficienti non esistono per la maggior parte dei modelli complessi e si usano statistiche euristiche.

## 7.3 Limiti dell'ABC

L'ABC rejection sampler ha un tasso di accettazione che può essere molto basso in spazi di parametri ad alta dimensione. Varianti più efficienti -- ABC-MCMC, ABC-SMC (Sequential Monte Carlo) -- migliorano questo aspetto ma sono più complesse da implementare.

In alternativa, per modelli simulabili ma con likelihood intrattabile, il **metodo della verosimiglianza sintetica** (synthetic likelihood) sostituisce la likelihood vera con una gaussiana multivariata centrata su $m_{\mathrm{sim}}(\theta)$, che è spesso una buona approssimazione.

# 8. Sintesi: quale metodo per quale modello

La tabella seguente riassume quale approccio usare in funzione della disponibilità della likelihood e della complessità del modello.

| Modello | Likelihood | Metodo consigliato |
|---|---|---|
| Poisson omogeneo | analitica, semplice | MLE in forma chiusa |
| Distribuzione Weibull, Gamma | analitica | MLE numerico o momenti |
| SDE osservata su griglia fine | gaussiana per incrementi | MLE numerico (Euler-Maruyama) |
| Processo di Hawkes (kernel esponenziale) | analitica, $O(n)$ | MLE numerico |
| SDE con osservazioni sparse o rumorose | intrattabile | SMM o filtro particellare |
| Branching (solo dimensioni aggregate) | intrattabile | SMM |
| Modelli agent-based (Vicsek, March, Deffuant) | intrattabile | SMM o ABC |
| Qualsiasi modello, approccio bayesiano | intrattabile | ABC rejection o ABC-MCMC |

Il principio guida è sempre lo stesso: usare il metodo piu' semplice che sia adeguato al problema. La complessita' computazionale si giustifica solo quando metodi piu' semplici sono insufficienti.

## Riferimenti

* Pawitan, Y. (2001). *In All Likelihood: Statistical Modelling and Inference Using Likelihood*. Oxford University Press.
* Sisson, S. A., Fan, Y., and Beaumont, M. A. (2018). *Handbook of Approximate Bayesian Computation*. CRC Press.
* Iacus, S. M. (2008). *Simulation and Inference for Stochastic Differential Equations*. Springer.
* Daley, D. J., and Vere-Jones, D. (2003). *An Introduction to the Theory of Point Processes*. Springer.
* McFadden, D. (1989). A Method of Simulated Moments for Estimation of Discrete Response Models without Numerical Integration. *Econometrica*, 57(5), 995--1026.
* Beaumont, M. A., Zhang, W., and Balding, D. J. (2002). Approximate Bayesian Computation in Population Genetics. *Genetics*, 162(4), 2025--2035.

---

# Appendice A -- Calcolo numerico della log-likelihood: schemi pratici

## A.1 Schema generale

Per qualsiasi modello con likelihood fattorizzabile, lo schema di calcolo è:

```python
def log_likelihood(theta, data):
    ll = 0.0
    for obs in data:
        ll += log_prob(obs, theta)
    return ll
```

dove `log_prob` calcola $\log p(y \mid \theta)$ per una singola osservazione.

## A.2 Processo di Poisson: stima di lambda

```python
import math

def log_likelihood_poisson(lam, inter_arrival_times):
    n = len(inter_arrival_times)
    total = sum(inter_arrival_times)
    return n * math.log(lam) - lam * total

def mle_poisson(inter_arrival_times):
    return len(inter_arrival_times) / sum(inter_arrival_times)
```

## A.3 SDE (Euler-Maruyama): stima di drift e diffusione

Per la SDE $dX = a(X;\theta)dt + b(X;\theta)dW$ su una griglia di passo $\Delta t$:

```python
def log_likelihood_sde(theta, trajectory, dt):
    a_func, b_func = theta
    ll = 0.0

    for i in range(len(trajectory) - 1):
        x = trajectory[i]
        x_next = trajectory[i + 1]

        mean = x + a_func(x) * dt
        std = b_func(x) * math.sqrt(dt)

        ll += log_normal(x_next, mean, std)

    return ll

def log_normal(x, mean, std):
    return (-0.5 * math.log(2 * math.pi)
            - math.log(std)
            - 0.5 * ((x - mean) / std) ** 2)
```

## A.4 Ottimizzazione numerica

```python
from scipy.optimize import minimize

def fit_model(log_likelihood_func, theta_init, data, bounds=None):
    def neg_ll(theta):
        return -log_likelihood_func(theta, data)

    result = minimize(
        neg_ll,
        x0=theta_init,
        method='L-BFGS-B',
        bounds=bounds
    )

    return result.x, result.fun
```

## A.5 Residui trasformati per processi puntuali

```python
def transformed_residuals(events, intensity_func, T):
    taus = []
    cumulative = 0.0

    for k in range(len(events)):
        t_prev = events[k - 1] if k > 0 else 0.0
        t_k = events[k]

        # integra l'intensita' da t_prev a t_k numericamente
        n_steps = 100
        dt = (t_k - t_prev) / n_steps
        integral = sum(intensity_func(t_prev + j * dt) * dt
                       for j in range(n_steps))

        cumulative += integral
        taus.append(cumulative)

    return taus
```

I tempi inter-evento trasformati `[taus[k] - taus[k-1] for k in range(1, len(taus))]` devono essere distribuiti come Exp(1) se il modello e' corretto.

## A.6 Simulazione per SMM

```python
def smm_objective(theta, obs_stats, n_simulations, simulator_func, stats_func):
    sim_stats_list = []

    for _ in range(n_simulations):
        sim_data = simulator_func(theta)
        sim_stats_list.append(stats_func(sim_data))

    sim_stats_mean = [
        sum(s[i] for s in sim_stats_list) / n_simulations
        for i in range(len(obs_stats))
    ]

    return sum((obs_stats[i] - sim_stats_mean[i]) ** 2
               for i in range(len(obs_stats)))
```

## A.7 ABC rejection sampler

```python
def abc_rejection(prior_sampler, simulator, summary_stats,
                  obs_stats, epsilon, n_accepted):
    accepted = []

    while len(accepted) < n_accepted:
        theta = prior_sampler()
        sim_data = simulator(theta)
        sim_stats = summary_stats(sim_data)

        distance = math.sqrt(sum((obs_stats[i] - sim_stats[i]) ** 2
                                  for i in range(len(obs_stats))))

        if distance <= epsilon:
            accepted.append(theta)

    return accepted
```
