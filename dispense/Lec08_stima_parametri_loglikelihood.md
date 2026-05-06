---
title: "08: Stima dei parametri e log-likelihood"
author: "Antonio Scala"
date: ""
---

# Obiettivi della lezione

In questa lezione introduciamo il problema della **stima dei parametri** nei modelli stocastici. Nelle lezioni precedenti abbiamo imparato a costruire modelli probabilistici, a simulare traiettorie, a descrivere distribuzioni e a passare da dinamiche microscopiche a equazioni per la probabilità. Ora affrontiamo il problema inverso:

> dati osservati alcuni fenomeni, come possiamo stimare i parametri del modello che li ha generati?

Il concetto centrale sarà la **likelihood**, cioè la probabilità dei dati osservati vista come funzione dei parametri. Poiché i dati indipendenti producono prodotti di probabilità, lavoreremo quasi sempre con la **log-likelihood**, che trasforma questi prodotti in somme e rende il problema numericamente e concettualmente più trattabile.

Al termine della lezione lo studente dovrebbe essere in grado di:

1. distinguere tra modello, parametro, dato osservato e stimatore;
2. costruire la likelihood di un campione indipendente;
3. passare dalla likelihood alla log-likelihood;
4. calcolare stimatori di massima verosimiglianza in esempi elementari;
5. interpretare la stima di massima likelihood come problema di ottimizzazione;
6. collegare log-likelihood, cross-entropia e divergenza di Kullback--Leibler;
7. riconoscere il ruolo della curvatura della log-likelihood nell'incertezza della stima;
8. trattare dati non indipendenti tramite likelihood di traiettoria;
9. comprendere le principali patologie numeriche e statistiche della stima parametrica;
10. usare diagnostiche di confronto modello-dati;
11. riconoscere quando la likelihood è intrattabile e quando usare metodi simulation-based.

# Struttura della lezione

1. Il problema della stima parametrica
2. Likelihood e log-likelihood
3. Massima verosimiglianza
4. Esempi fondamentali: Bernoulli, Poisson, esponenziale, gaussiana
5. Score, Hessiano e informazione di Fisher
6. Incertezza della stima e approssimazione quadratica
7. Interpretazione informazionale: cross-entropia e divergenza KL
8. Dati dipendenti e likelihood di traiettoria
9. Stima nei processi di salto
10. Stima nelle SDE da dati discretizzati
11. Diagnostica, overfitting e problemi numerici
12. Confronto modello-dati e goodness-of-fit
13. Quando la likelihood è intrattabile
14. Sintesi finale
15. Esercizi

---

# 1. Il problema della stima parametrica

Un modello stocastico assegna probabilità agli esiti possibili. Spesso tale assegnazione dipende da uno o più parametri.

Indichiamo con

$$
\theta
$$

il parametro, o il vettore di parametri, del modello. Per esempio:

- in una Bernoulli, $\theta=p$ è la probabilità di successo;
- in una Poisson, $\theta=\lambda$ è il tasso medio di eventi;
- in una gaussiana, $\theta=(\mu,\sigma^2)$ contiene media e varianza;
- in una SDE, $\theta$ può contenere parametri di drift e diffusione;
- in una master equation, $\theta$ può contenere tassi di transizione.

Supponiamo ora di osservare dati

$$
x_1,x_2,\dots,x_n.
$$

La domanda inferenziale è:

> quali valori di $\theta$ rendono i dati osservati più plausibili sotto il modello?

Questa domanda è diversa dalla simulazione diretta.

Nella **simulazione diretta** conosciamo $\theta$ e generiamo dati.

Nella **stima parametrica** osserviamo dati e cerchiamo di risalire a $\theta$.

Schema concettuale:

$$
\theta \quad \longrightarrow \quad \text{modello probabilistico} \quad \longrightarrow \quad \text{dati}
$$

è il problema diretto, mentre

$$
\text{dati} \quad \longrightarrow \quad \text{stima di } \theta
$$

è il problema inverso.

## 1.1 Parametro vero e stimatore

In un'impostazione frequentista si immagina che esista un valore vero, ma ignoto, del parametro:

$$
\theta_0.
$$

I dati sono generati da quel valore, ma noi non lo conosciamo. Uno **stimatore** è una funzione dei dati:

$$
\hat\theta = \hat\theta(x_1,\dots,x_n).
$$

Poiché i dati sono casuali, anche lo stimatore è una variabile aleatoria. Questo punto è importante: la stima numerica ottenuta da un dataset è un numero, ma il metodo che l'ha prodotta ha una distribuzione campionaria.

## 1.2 Criteri desiderabili

Uno stimatore dovrebbe essere:

- **consistente**: tende al parametro vero quando il numero di dati cresce;
- **non distorto**, almeno asintoticamente: il suo valore medio coincide con il parametro vero;
- **efficiente**: ha varianza piccola rispetto all'informazione disponibile;
- **robusto**: non cambia drasticamente per piccole perturbazioni dei dati;
- **numericamente stabile**: può essere calcolato in modo affidabile.

La massima verosimiglianza fornisce un criterio generale e molto usato per costruire stimatori con buone proprietà asintotiche.

# 2. Likelihood e log-likelihood

Supponiamo che un singolo dato $x$ abbia densità o probabilità

$$
p(x\mid \theta).
$$

Se osserviamo un campione indipendente

$$
x_1,\dots,x_n,
$$

la probabilità congiunta dei dati è

$$
p(x_1,\dots,x_n\mid\theta)
=\prod_{i=1}^n p(x_i\mid\theta).
$$

Quando questa quantità viene vista come funzione di $\theta$, con i dati fissati, prende il nome di **likelihood**:

$$
L(\theta)=\prod_{i=1}^n p(x_i\mid\theta).
$$

La distinzione concettuale è sottile ma importante:

- $p(x\mid\theta)$ è una distribuzione in $x$, a parametro fissato;
- $L(\theta)$ è una funzione di $\theta$, a dati fissati.

La likelihood non è, in generale, una distribuzione di probabilità su $\theta$. Non deve integrare a uno rispetto a $\theta$.

## 2.1 Perché passare al logaritmo

La likelihood di molti dati indipendenti è un prodotto di molti fattori. Questo è scomodo per tre ragioni.

Primo, i prodotti di molte probabilità diventano numericamente piccolissimi e possono produrre underflow.

Secondo, le derivate di un prodotto sono meno maneggevoli delle derivate di una somma.

Terzo, vogliamo leggere il contributo di ciascun dato in modo additivo.

Per questo si definisce la **log-likelihood**:

$$
\ell(\theta)=\log L(\theta)=\sum_{i=1}^n \log p(x_i\mid\theta).
$$

Poiché il logaritmo è monotono crescente, massimizzare $L(\theta)$ equivale a massimizzare $\ell(\theta)$:

$$
\arg\max_\theta L(\theta)=\arg\max_\theta \ell(\theta).
$$

Il problema di trovare i parametri "migliori" si riconduce quindi ad un problema di ottimizzazione di $\ell(\theta)$. Non bisogna dimenticare però che in genere $\theta\in\Theta$ dove $\Theta$ può essere definito un dominio limitato; ad esempio, se il parametro è una probabilità, essa sarà un numero reale compreso fra zero e uno. Si tratta quindi di un problema di *ottimizzazione vincolata*. 

## 2.2 Negative log-likelihood

In ottimizzazione numerica è più comune minimizzare che massimizzare. Si introduce allora la **negative log-likelihood**:

$$
\mathcal{J}(\theta)=-\ell(\theta).
$$

La stima di massima verosimiglianza, indicata con MLE dall'inglese *maximum likelihood estimator*, si può quindi scrivere come

$$
\hat\theta_{\mathrm{MLE}}
=\arg\max_\theta \ell(\theta)
=\arg\min_\theta \mathcal{J}(\theta).
$$

Questa forma è particolarmente utile quando si usano algoritmi generali di ottimizzazione vincolata.

# 3. Massima verosimiglianza

Come introdotto nella sezione precedente, il principio di **massima verosimiglianza** consiste nello scegliere il parametro che rende massima la log-probabilità dei dati osservati:

$$
\hat\theta_{\mathrm{MLE}}=\arg\max_\theta \ell(\theta).
$$

Vediamo ora le condizioni necessarie per trovare questo massimo.

## 3.1 Condizione del primo ordine

Se $\theta$ è scalare e $\ell$ è derivabile, un massimo locale interno al dominio ammissibile $\Theta$ deve soddisfare

$$
\frac{d\ell}{d\theta}(\hat\theta)=0.
$$

La derivata della log-likelihood si chiama **score**:

$$
S(\theta)=\frac{d\ell}{d\theta}.
$$

La condizione di massimo locale interno diventa

$$
S(\hat\theta)=0.
$$

Se $\theta$ è vettoriale,

$$
\theta=(\theta_1,\dots,\theta_d),
$$

lo score è il gradiente:

$$
S(\theta)=\nabla_\theta \ell(\theta),
$$

e la condizione diventa

$$
\nabla_\theta \ell(\hat\theta)=0.
$$

> **Approfondimento:** Nel caso in cui il massimo cada sul bordo $\partial\Theta$ del dominio ammissibile, la condizione di annullamento dello score non è più necessaria. Se il bordo è sufficientemente regolare da ammettere un (iper)piano tangente ben definito, allora la condizione corretta è che non esista alcuna direzione ammissibile lungo cui la log-likelihood possa aumentare al primo ordine. In termini geometrici, il gradiente $\nabla_\theta \ell(\hat\theta)$ non deve avere componenti tangenti al bordo ammissibile; esso può invece essere bilanciato dalla reazione del vincolo. Nel caso di vincoli lisci questa idea conduce alle condizioni di Karush--Kuhn--Tucker (vedi appendice sull'ottimizzazione).

## 3.2 Condizione del secondo ordine

Per avere un massimo locale, nel caso scalare serve

$$
\frac{d^2\ell}{d\theta^2}(\hat\theta)<0.
$$

Nel caso vettoriale, l'Hessiano

$$
H(\theta)=\nabla_\theta^2 \ell(\theta)
$$

deve essere definito negativo nel punto di massimo.

Questa curvatura non serve solo a verificare il massimo: contiene anche informazione sull'incertezza della stima.

> **Approfondimento:** Anche la condizione del secondo ordine va interpretata con cautela quando il massimo cade sul bordo di $\Theta$. In un massimo interno si richiede che l'Hessiano sia definito negativo in tutte le direzioni. In presenza di vincoli attivi, invece, non tutte le perturbazioni infinitesime sono ammissibili: la curvatura rilevante è quella della log-likelihood ristretta alle direzioni ammissibili, e in particolare alle direzioni tangenti al bordo. In forma geometrica, dopo che il gradiente è stato bilanciato dai vincoli attivi, la variazione quadratica deve essere non positiva per ogni direzione ammissibile al primo ordine. Anche questa è una delle componenti delle condizioni di ottimalità vincolata.

# 4. Esempi fondamentali

## 4.1 Bernoulli

Supponiamo di osservare

$$
x_i\in\{0,1\},
$$

con

$$
P(X_i=1)=p,
\qquad
P(X_i=0)=1-p.
$$

La probabilità di osservare $x_i$ è

$$
P(X_i=x_i\mid p)=p^{x_i}(1-p)^{1-x_i}.
$$

La likelihood del campione è

$$
L(p)=\prod_{i=1}^n p^{x_i}(1-p)^{1-x_i}.
$$

Definiamo

$$
k=\sum_{i=1}^n x_i,
$$

cioè il numero di successi. Allora

$$
L(p)=p^k(1-p)^{n-k}.
$$

La log-likelihood è

$$
\ell(p)=k\log p+(n-k)\log(1-p).
$$

Derivando:

$$
\ell'(p)=\frac{k}{p}-\frac{n-k}{1-p}.
$$

Ponendo $\ell'(p)=0$:

$$
\frac{k}{p}=\frac{n-k}{1-p}.
$$

Quindi

$$
k(1-p)=(n-k)p,
$$

cioè

$$
k=np.
$$

La stima di massima verosimiglianza è

$$
\hat p=\frac{k}{n}=\frac{1}{n}\sum_{i=1}^n x_i.
$$

Dunque, per una Bernoulli, la MLE della probabilità di successo è la frequenza empirica dei successi. Notare che in questo caso vale $\hat p\in [0,1]$ per cui il minimo è automaticamente definito nel dominio ammissibile.

## 4.2 Poisson

Supponiamo che

$$
X_i\sim \mathrm{Poisson}(\lambda),
$$

cioè

$$
P(X_i=x_i\mid\lambda)=\frac{\lambda^{x_i}e^{-\lambda}}{x_i!},
\qquad x_i=0,1,2,\dots.
$$

dove ovviamente deve valere $\lambda\geq 0$. La likelihood è

$$
L(\lambda)=\prod_{i=1}^n \frac{\lambda^{x_i}e^{-\lambda}}{x_i!}.
$$

La log-likelihood è

$$
\ell(\lambda)=\sum_{i=1}^n \left(x_i\log\lambda-\lambda-\log(x_i!)\right).
$$

Raccogliendo i termini che dipendono da $\lambda$:

$$
\ell(\lambda)=\left(\sum_{i=1}^n x_i\right)\log\lambda-n\lambda+\text{costante}.
$$

Derivando:

$$
\ell'(\lambda)=\frac{1}{\lambda}\sum_{i=1}^n x_i-n.
$$

Ponendo $\ell'(\lambda)=0$:

$$
\hat\lambda=\frac{1}{n}\sum_{i=1}^n x_i.
$$

Anche qui la MLE coincide con la media campionaria ed essendo $\hat \lambda \in \mathbb R^+$ appartiene al dominio ammissibile.

## 4.3 Distribuzione esponenziale

Supponiamo che i dati siano tempi di attesa indipendenti con densità

$$
p(t\mid\lambda)=\lambda e^{-\lambda t},
\qquad t\ge 0.
$$

La likelihood è

$$
L(\lambda)=\prod_{i=1}^n \lambda e^{-\lambda t_i}
=\lambda^n e^{-\lambda\sum_i t_i}.
$$

La log-likelihood è

$$
\ell(\lambda)=n\log\lambda-\lambda\sum_{i=1}^n t_i.
$$

Derivando:

$$
\ell'(\lambda)=\frac{n}{\lambda}-\sum_{i=1}^n t_i.
$$

Ponendo $\ell'(\lambda)=0$:

$$
\hat\lambda=\frac{n}{\sum_{i=1}^n t_i}=1\,/\,\bar t.
$$

Il tasso stimato è quindi l'inverso del tempo medio osservato.

Questa formula è molto naturale: se gli eventi arrivano spesso, i tempi di attesa sono piccoli e il tasso è grande; se gli eventi arrivano raramente, i tempi di attesa sono lunghi e il tasso è piccolo.

## 4.4 Gaussiana con varianza nota

Supponiamo

$$
X_i\sim \mathcal{N}(\mu,\sigma^2),
$$

con $\sigma^2$ nota e $\mu$ ignota. La densità è

$$
p(x_i\mid\mu)=\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left[-\frac{(x_i-\mu)^2}{2\sigma^2}\right].
$$

La log-likelihood è

$$
\ell(\mu)=
-\frac{n}{2}\log(2\pi\sigma^2)
-\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i-\mu)^2.
$$

Il primo termine non dipende da $\mu$. Massimizzare $\ell(\mu)$ equivale quindi a minimizzare

$$
\sum_{i=1}^n (x_i-\mu)^2.
$$

Derivando:

$$
\frac{d\ell}{d\mu}
=\frac{1}{\sigma^2}\sum_{i=1}^n (x_i-\mu).
$$

Ponendo a zero:

$$
\sum_{i=1}^n (x_i-\hat\mu)=0,
$$

quindi

$$
\hat\mu=\bar x=\frac{1}{n}\sum_{i=1}^n x_i.
$$

Poiché $\hat\mu\in\mathbb{R}$ non vi sono vincoli attivi sul dominio ammissibile, e il massimo è sempre interno.

## 4.5 Gaussiana con media e varianza ignote

Ora supponiamo che siano ignote sia $\mu$ sia $\sigma^2$. La log-likelihood è

$$
\ell(\mu,\sigma^2)=
-\frac{n}{2}\log(2\pi)
-\frac{n}{2}\log\sigma^2
-\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i-\mu)^2.
$$

La MLE della media è ancora

$$
\hat\mu=\bar x.
$$

Sostituendo questo valore, la MLE della varianza è

$$
\hat\sigma^2_{\mathrm{MLE}}
=\frac{1}{n}\sum_{i=1}^n (x_i-\bar x)^2.
$$

Questa stima usa il denominatore $n$, non $n-1$. Lo stimatore corretto non distorto della varianza usa invece $n-1$:

$$
s^2=\frac{1}{n-1}\sum_{i=1}^n (x_i-\bar x)^2.
$$

Questo esempio mostra una distinzione importante: la massima likelihood non garantisce automaticamente assenza di bias per campioni finiti. Le buone proprietà della MLE sono spesso asintotiche.

# 5. Score, Hessiano e informazione di Fisher

La log-likelihood contiene non solo il massimo, ma anche la forma locale attorno al massimo.

## 5.1 Score

Nel caso vettoriale, lo score è

$$
S(\theta)=\nabla_\theta\ell(\theta).
$$

Lo score misura quanto la log-likelihood cambia se modifichiamo leggermente il parametro.

Al massimo interno:

$$
S(\hat\theta)=0.
$$

## 5.2 Hessiano

L'Hessiano è

$$
H(\theta)=\nabla_\theta^2\ell(\theta).
$$

Se $\hat\theta$ è un massimo, $H(\hat\theta)$ è tipicamente definito negativo.

Si definisce spesso la matrice di informazione osservata come

$$
\mathcal{I}_{\mathrm{obs}}(\hat\theta)=-H(\hat\theta).
$$

Il segno meno serve a rendere positiva una curvatura che, per la log-likelihood al massimo, è negativa.

## 5.3 Informazione di Fisher

Per evitare ambiguità, distinguiamo prima l'informazione contenuta in una singola osservazione dall'informazione contenuta in un intero campione.

Consideriamo una singola osservazione $X$ con densità o probabilità

$$
p(x\mid\theta).
$$

Lo **score elementare** è il gradiente della log-probabilità della singola osservazione:

$$
s(x;\theta)=\nabla_\theta \log p(x\mid\theta).
$$

Questa quantità è un vettore nello spazio dei parametri. Per un dato osservato $x$, indica in quale direzione dello spazio dei parametri cresce più rapidamente la log-probabilità di osservare proprio quel dato.

L'**informazione di Fisher per singola osservazione** è definita come

$$
I_1(\theta) = \mathbb{E}_\theta\left[ s(X;\theta)s(X;\theta)^T \right].
$$

Questa formula ha una lettura geometrica naturale. Per ogni possibile osservazione $X$, lo score $s(X;\theta)$ è un vettore nello spazio dei parametri. L'informazione di Fisher è la media dei prodotti esterni $s(X;\theta)s(X;\theta)^T$. Nel caso di più parametri essa è quindi una matrice: gli elementi diagonali misurano l'informazione sulle singole direzioni parametriche, mentre gli elementi fuori diagonale misurano quanto le stime dei parametri siano accoppiate.

In particolare, se $u$ è una direzione (i.e. uno vettore unitario) nello spazio dei parametri, allora

$$
u^T I_1(\theta)u =
\mathbb{E}_\theta\left[
\bigl(u^T s(X;\theta)\bigr)^2
\right].
$$

Il termine $u^T s(X;\theta)$ è la variazione infinitesima della log-probabilità della singola osservazione quando il parametro viene perturbato nella direzione $u$. Quindi $u^T I_1(\theta)u$ misura quanto la distribuzione dei dati è sensibile, in media, a perturbazioni del parametro lungo quella direzione.

Se questa quantità è grande, piccole variazioni di $\theta$ lungo $u$ cambiano sensibilmente la distribuzione osservabile: quella direzione è statisticamente ben identificabile. Se invece è piccola, il modello cambia poco lungo quella direzione: la stima sarà più incerta.

In questo senso, la matrice di Fisher definisce una metrica locale sullo spazio dei parametri: due valori vicini di $\theta$ sono tanto più distinguibili statisticamente quanto più grande è la distanza misurata da $I_1(\theta)$.

> **Nota:** $u^T I_1(\theta)u$ è il valore medio del quadrato della componente dello score lungo la direzione $u$.

### Identità con l'Hessiano medio

Sotto opportune condizioni di regolarità, la stessa informazione elementare può essere scritta come

$$
I_1(\theta) = -\mathbb{E}_\theta\left[ \nabla_\theta^2 \log p(X\mid\theta) \right].
$$

Vediamo l'idea della dimostrazione.

Per semplicità scriviamo le componenti dello score come

$$
s_i(x;\theta)=\frac{\partial}{\partial\theta_i}\log p(x\mid\theta).
$$

Poiché

$$
s_i(x;\theta) =
\frac{1}{p(x\mid\theta)}
\frac{\partial p(x\mid\theta)}{\partial\theta_i},
$$

il valore atteso dello score è

$$
\mathbb{E}_\theta[s_i] = \int s_i(x;\theta)p(x\mid\theta)\,dx
= \int \frac{\partial p(x\mid\theta)}{\partial\theta_i} \,dx.
$$

Se possiamo scambiare derivata e integrale, allora

$$
\mathbb{E}_\theta[s_i] = \frac{\partial}{\partial\theta_i} \int p(x\mid\theta)\,dx.
$$

Ma la densità è normalizzata:

$$
\int p(x\mid\theta)\,dx=1.
$$

Quindi

$$
\mathbb{E}_\theta[s_i]=0.
$$

Ora deriviamo questa identità rispetto a un secondo parametro $\theta_j$:

$$
0 = \frac{\partial}{\partial\theta_j} \mathbb{E}_\theta[s_i]
= \frac{\partial}{\partial\theta_j} \int s_i(x;\theta)p(x\mid\theta)\,dx.
$$

Derivando il prodotto dentro l'integrale otteniamo

$$
0 = \int \frac{\partial s_i}{\partial\theta_j} p(x\mid\theta)\,dx
+ \int s_i(x;\theta) \frac{\partial p(x\mid\theta)}{\partial\theta_j} \,dx.
$$

Usando

$$
\frac{\partial p(x\mid\theta)}{\partial\theta_j} = p(x\mid\theta)s_j(x;\theta),
$$

segue che

$$
0 = \mathbb{E}_\theta\left[ \frac{\partial s_i}{\partial\theta_j} \right]
+ \mathbb{E}_\theta[s_i s_j].
$$

Pertanto

$$
\mathbb{E}_\theta[s_i s_j] = - \mathbb{E}_\theta\left[ \frac{\partial s_i}{\partial\theta_j} \right].
$$

Ma

$$
\frac{\partial s_i}{\partial\theta_j} = \frac{\partial^2}{\partial\theta_j\partial\theta_i} \log p(x\mid\theta).
$$

Quindi

$$
(I_1)_{ij}(\theta) = \mathbb{E}_\theta[s_i s_j]
= - \mathbb{E}_\theta\left[
\frac{\partial^2}{\partial\theta_j\partial\theta_i} \log p(X\mid\theta)
\right].
$$

In forma matriciale,

$$
I_1(\theta) =
-\mathbb{E}_\theta\left[ \nabla_\theta^2 \log p(X\mid\theta) \right].
$$

Questa identità mostra che l'informazione di Fisher può essere letta in due modi equivalenti:

- come varianza dello score, cioè come ampiezza media delle fluttuazioni del gradiente della log-probabilità;
- come curvatura media negativa della log-probabilità rispetto ai parametri.

> **Nota:** Qui $\nabla_\theta^2$ indica l'Hessiano rispetto ai parametri, non il Laplaciano. Se $\theta=(\theta_1,\dots,\theta_d)$, allora
> $$ \bigl(\nabla_\theta^2 f\bigr)_{ij} = \frac{\partial^2 f}{\partial\theta_i\partial\theta_j}. $$
> È quindi una matrice $d\times d$ di derivate seconde. Il Laplaciano sarebbe invece la traccia dell'Hessiano,
> $$\Delta_\theta f=\sum_{i=1}^d \frac{\partial^2 f}{\partial\theta_i^2}.$$

### Informazione del campione

Passiamo ora da una singola osservazione a un campione indipendente

$$
X_1,\dots,X_n.
$$

La log-likelihood totale è

$$
\ell_n(\theta)
= \sum_{k=1}^n \log p(X_k\mid\theta).
$$

Lo score totale è

$$
S_n(\theta)
= \nabla_\theta \ell_n(\theta)
= \sum_{k=1}^n s(X_k;\theta).
$$

L'informazione di Fisher del campione è

$$
I_n(\theta) = \mathbb{E}_\theta\left[ S_n(\theta)S_n(\theta)^T \right].
$$

Se le osservazioni sono indipendenti e identicamente distribuite, allora gli score elementari sono indipendenti e hanno media nulla. I termini incrociati hanno quindi media nulla, e rimane soltanto la somma delle informazioni elementari:

$$
I_n(\theta)=n I_1(\theta).
$$

In modo equivalente, usando l'identità con l'Hessiano medio,

$$
I_n(\theta)
= -\mathbb{E}_\theta\left[ \nabla_\theta^2 \ell_n(\theta) \right].
$$

Questa relazione spiega perché l'incertezza della stima diminuisce al crescere di $n$: l'informazione cresce linearmente con il numero di osservazioni, mentre la scala tipica dell'errore dello stimatore decresce come $1/\sqrt{n}$.

# 6. Incertezza della stima

## 6.1 Approssimazione quadratica della log-likelihood

Vicino al massimo, possiamo sviluppare la log-likelihood in serie di Taylor:

$$
\ell(\theta)\approx \ell(\hat\theta)
+\frac{1}{2}(\theta-\hat\theta)^T H(\hat\theta)(\theta-\hat\theta),
$$

perché il termine lineare si annulla:

$$
\nabla_\theta\ell(\hat\theta)=0.
$$

Poiché $H(\hat\theta)$ ad un massimo è una matrice definita negativa, la log-likelihood decresce allontanandosi da $\hat\theta$.

Scrivendo

$$
\mathcal{I}_{\mathrm{obs}}(\hat\theta)=-H(\hat\theta),
$$

otteniamo

$$
\ell(\theta)\approx \ell(\hat\theta)
-\frac{1}{2}(\theta-\hat\theta)^T
\mathcal{I}_{\mathrm{obs}}(\hat\theta)
(\theta-\hat\theta).
$$

Questa formula mostra che la log-likelihood vicino al massimo ha forma approssimativamente parabolica.

## 6.2 Varianza asintotica

Per campioni grandi, sotto condizioni regolari,

$$
\hat\theta_{\mathrm{MLE}}
\approx
\mathcal{N}\left(\theta_0,\mathcal{I}(\theta_0)^{-1}\right);
$$

Nel caso i.i.d., $\mathcal{I}_n(\theta_0)=nI_1(\theta_0)$, dove $I_1(\theta_0)$ è l'informazione per singola osservazione, e quindi

$$
\hat\theta_{\mathrm{MLE}}
\approx
\mathcal{N}\left(\theta_0,\frac{1}{n}I_1(\theta_0)^{-1}\right).
$$
In pratica, però, non conosciamo il valore vero $\theta_0$ e quindi non possiamo calcolare direttamente l'informazione teorica $I_n(\theta_0)$. Usiamo allora la curvatura della log-likelihood osservata nel punto stimato.

Definiamo l'informazione osservata come

$$
\mathcal{I}_{\mathrm{obs}}(\hat\theta) = -\nabla_\theta^2 \ell_n(\hat\theta),
$$

dove $\ell_n$ è la log-likelihood totale del campione. L'idea è la seguente: vicino al massimo, la log-likelihood è approssimativamente quadratica,

$$
\ell_n(\theta) \approx
\ell_n(\hat\theta) -\frac{1}{2}(\theta-\hat\theta)^T\mathcal{I}_{\mathrm{obs}}(\hat\theta)(\theta-\hat\theta).
$$

Se la curvatura è grande, la log-likelihood scende rapidamente allontanandosi da $\hat\theta$: il massimo è ben localizzato e la stima è precisa. Se invece la curvatura è piccola, la log-likelihood è piatta: molti valori del parametro spiegano quasi ugualmente bene i dati, e la stima è incerta.

Per questo motivo si usa l'approssimazione

$$
\widehat{\mathrm{Cov}}(\hat\theta)
\approx
\mathcal{I}_{\mathrm{obs}}(\hat\theta)^{-1}.
$$

Qui $\widehat{\mathrm{Cov}}(\hat\theta)$ non è la covarianza dei dati, ma la covarianza stimata dello **stimatore** $\hat\theta$: misura l'incertezza sui parametri stimati. In altre parole, descrive quanto cambierebbe la stima se ripetessimo molte volte l'esperimento e ricalcolassimo ogni volta la MLE.

Nel caso di un solo parametro, questa matrice si riduce alla varianza stimata dello stimatore:

$$
\widehat{\mathrm{Var}}(\hat\theta) \approx \frac{1}{-\ell_n''(\hat\theta)}.
$$

## 6.3 Interpretazione geometrica

Una log-likelihood molto curva attorno al massimo implica una stima precisa: spostarsi anche poco da $\hat\theta$ peggiora molto l'accordo con i dati.

Una log-likelihood piatta implica una stima incerta: molti valori di $\theta$ spiegano quasi ugualmente bene i dati.

Questa geometria è essenziale nei modelli complessi, dove possono comparire:

- parametri debolmente identificabili;
- direzioni piatte nello spazio dei parametri;
- massimi multipli;
- forti correlazioni tra parametri.

# 7. Interpretazione informazionale

La massima likelihood non è soltanto una procedura di calcolo. Ha una interpretazione informazionale precisa.

Supponiamo di riassumere i dati tramite la loro distribuzione empirica $p_{\mathrm{data}}$, cioè tramite le frequenze osservate degli esiti, e supponiamo che il modello parametrico che stiamo testando assegni agli stessi esiti una distribuzione teorica $q_\theta$ per ogni valore di $\theta$.

La log-likelihood media può essere scritta come

$$
\frac{1}{n}\ell(\theta) = \sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

La negative log-likelihood media è quindi

$$
-\frac{1}{n}\ell(\theta) = -\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Questa quantità è la **cross-entropia** tra $p_{\mathrm{data}}$ e $q_\theta$:

$$
H(p_{\mathrm{data}},q_\theta) = -\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Per capire perché in seguito comparirà naturalmente la divergenza di Kullback--Leibler, partiamo da una domanda semplice: quanto costa descrivere dati generati da una distribuzione $p$ usando invece una distribuzione $q$?

Se un evento $x$ ha probabilità assegnata $q(x)$, la sorpresa associata all'osservazione di $x$ secondo il modello $q$ è

$$ -\log q(x).$$

Se però gli eventi sono generati dalla distribuzione vera $p$, la sorpresa media che otteniamo usando il modello $q$ è

$$ -\sum_x p(x)\log q(x). $$

Questa è la cross-entropia $H(p,q)$.

Se invece usassimo la distribuzione corretta $p$, la sorpresa media sarebbe

$$ -\sum_x p(x)\log p(x) = H(p), $$

cioè l'entropia di Shannon di $p$.

La differenza tra queste due quantità misura quindi l'eccesso di sorpresa, o costo informazionale medio, dovuto al fatto che usiamo $q$ al posto di $p$:

$$ H(p,q)-H(p). $$

Questa differenza è la **divergenza di Kullback--Leibler**:

$$
D_{\mathrm{KL}}(p\|q) = H(p,q)-H(p).
$$

Sviluppando,

$$
D_{\mathrm{KL}}(p\|q) =
-\sum_x p(x)\log q(x) + \sum_x p(x)\log p(x),
$$

cioè

$$
D_{\mathrm{KL}}(p\|q) = \sum_x p(x)\log\frac{p(x)}{q(x)}.
$$

Questa quantità è chiamata divergenza perché misura una discrepanza tra due distribuzioni: vale zero se $p=q$ e, sotto condizioni usuali, è positiva se $p$ e $q$ differiscono. Non è però una distanza nel senso geometrico usuale, perché in generale non è simmetrica:

$$ D_{\mathrm{KL}}(p\|q) \neq D_{\mathrm{KL}}(q\|p).$$

Nel nostro caso, prendiamo

$$ p=p_{\mathrm{data}}, \qquad q=q_\theta. $$

Allora

$$
D_{\mathrm{KL}}(p_{\mathrm{data}}\|q_\theta)
= \sum_x p_{\mathrm{data}}(x) \log\frac{p_{\mathrm{data}}(x)}{q_\theta(x)}.
$$

Sviluppando:

$$
D_{\mathrm{KL}}(p_{\mathrm{data}}\|q_\theta)
= \sum_x p_{\mathrm{data}}(x)\log p_{\mathrm{data}}(x)
- \sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Il primo termine dipende solo dai dati, non da $\theta$. Quindi, quando variamo $\theta$, minimizzare la divergenza KL equivale a minimizzare la cross-entropia:

$$
H(p_{\mathrm{data}},q_\theta) = -\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

Ma minimizzare questa quantità equivale a massimizzare la log-likelihood media:

$$
\sum_x p_{\mathrm{data}}(x)\log q_\theta(x).
$$

In formule:

$$
\hat\theta_{\mathrm{MLE}}
= \arg\max_\theta \ell(\theta)
= \arg\min_\theta H(p_{\mathrm{data}},q_\theta)
= \arg\min_\theta D_{\mathrm{KL}}(p_{\mathrm{data}}\|q_\theta).
$$

Messaggio concettuale:

> la MLE sceglie, dentro la famiglia parametrica, la distribuzione $q_\theta$ più vicina alla distribuzione empirica $p_{\mathrm{data}}$ nel senso della divergenza KL.

In questa interpretazione, la log-likelihood non è solo una funzione da ottimizzare: misura quanto il modello riduce la sorpresa media dei dati osservati.

L'interpretazione informazionale vale anche in presenza di dipendenza temporale, purché la likelihood sia costruita correttamente come likelihood di traiettoria. Questo è l'oggetto delle prossime sezioni.

# 8. Dati dipendenti e likelihood di traiettoria

Finora abbiamo assunto dati indipendenti. Nei modelli stocastici dinamici questa ipotesi è spesso falsa.

Una traiettoria osservata

$$
x_0,x_1,\dots,x_T
$$

contiene dipendenza temporale: il valore presente influenza il futuro.

Se il processo è markoviano a tempo discreto, la probabilità della traiettoria si fattorizza come

$$
P(x_0,x_1,\dots,x_T\mid\theta)
= P(x_0\mid\theta)
\prod_{t=0}^{T-1} P(x_{t+1}\mid x_t,\theta).
$$

La log-likelihood è

$$
\ell(\theta)
=\log P(x_0\mid\theta)
+\sum_{t=0}^{T-1}\log P(x_{t+1}\mid x_t,\theta).
$$

Se la distribuzione iniziale non dipende da $\theta$, oppure se il transiente iniziale viene trascurato, il termine $\log P(x_0\mid\theta)$ può essere ignorato nell'ottimizzazione.

## 8.1 Catena di Markov discreta

Supponiamo che lo spazio degli stati sia finito e che la matrice di transizione sia

$$
P_{ij}(\theta)=P(X_{t+1}=j\mid X_t=i,\theta).
$$

Se osserviamo una traiettoria, possiamo contare quante volte appare la transizione $i\to j$:

$$
N_{ij}=\#\{t: x_t=i,\ x_{t+1}=j\}.
$$

La log-likelihood diventa

$$
\ell(\theta)=\sum_{i,j}N_{ij}\log P_{ij}(\theta),
$$

a meno di termini iniziali.

Se non imponiamo alcuna forma parametrica particolare alla matrice di transizione, allora ogni riga di $P$ può essere stimata separatamente. L'unico vincolo è che, per ogni stato di partenza $i$, le probabilità di transizione verso tutti gli stati possibili siano non negative e sommino a uno:

$$
P_{ij}\ge 0,
\qquad
\sum_j P_{ij}=1.
$$

In questo senso diciamo che ogni riga della matrice $P$ è libera. In questo caso, la MLE è

$$
\hat P_{ij} = \frac{N_{ij}}{\sum_k N_{ik}},
$$

cioè la frequenza empirica della transizione $i\to j$ tra tutte le transizioni osservate in uscita dallo stato $i$.

> **Nota:** Se ogni riga della matrice $P$ è libera, possiamo stimare separatamente le probabilità di transizione in uscita da ciascuno stato $i$. Per una riga fissata, la parte rilevante della log-likelihood è
> $$\ell_i=\sum_j N_{ij}\log P_{ij},$$
>con il vincolo di normalizzazione $\sum_j P_{ij}=1$. Introduciamo allora un moltiplicatore di Lagrange $\lambda_i$ e consideriamo la Lagrangiana
> $$ \mathcal{L}_i = \sum_j N_{ij}\log P_{ij} - \lambda_i\left(\sum_j P_{ij}-1\right).$$
> La condizione del primo ordine rispetto a $P_{ij}$ dà
>$$\frac{N_{ij}}{P_{ij}}-\lambda_i=0,$$
>cioè $P_{ij}=N_{ij}\,/\,\lambda_i$. Imponendo la normalizzazione della riga si ottiene
>$$ \lambda_i=\sum_k N_{ik}, $$
>e dunque
>$$\hat P_{ij}=\frac{N_{ij}}{\sum_k N_{ik}}.$$
>Quindi la probabilità stimata di passare da $i$ a $j$ è la frequenza empirica della transizione $i\to j$ tra tutte le transizioni osservate in uscita da $i$.

## 8.2 Dipendenza e numero effettivo di dati

Quando i dati sono dipendenti, non bisogna interpretare $T$ osservazioni come $T$ dati indipendenti. L'autocorrelazione riduce l'informazione effettiva.

Questo è importante per:

- stimare correttamente gli errori standard;
- evitare eccessiva fiducia nella stima;
- valutare la qualità del campionamento;
- confrontare modelli dinamici.

In particolare, traiettorie fortemente autocorrelate possono contenere molta meno informazione di quanto suggerisca la loro lunghezza.

# 9. Stima nei processi di salto

Consideriamo ora un processo markoviano a tempo continuo con stati discreti e tassi di transizione

$$
w_{i\to j}(\theta).
$$

Supponiamo di osservare una traiettoria completa su un intervallo $[0,T]$, cioè:

- gli stati visitati;
- i tempi di permanenza in ciascuno stato;
- le transizioni effettivamente avvenute.

## 9.1 Likelihood di una traiettoria continua nel tempo

Supponiamo di osservare un singolo tratto di traiettoria: il sistema entra nello stato $i$, vi rimane per un tempo $\tau$, e poi compie un salto verso lo stato $j$.

Quando il sistema si trova in $i$, il tasso totale di uscita è

$$
r_i(\theta)=\sum_{k\ne i}w_{i\to k}(\theta).
$$

La densità del tempo di permanenza $\tau$ nello stato $i$ è

$$
r_i(\theta)e^{-r_i(\theta)\tau}.
$$

Condizionatamente al fatto che avvenga un salto in uscita da $i$, la probabilità che il salto sia proprio verso $j$ è

$$
\frac{w_{i\to j}(\theta)}{r_i(\theta)}.
$$

Quindi la densità congiunta di osservare una permanenza di durata $\tau$ in $i$ seguita da un salto $i\to j$ è

$$
r_i(\theta)e^{-r_i(\theta)\tau}
\frac{w_{i\to j}(\theta)}{r_i(\theta)}
= w_{i\to j}(\theta)e^{-r_i(\theta)\tau}.
$$

Questa è la likelihood elementare del tratto osservato:

$$
L_{i\to j}(\theta;\tau)
= w_{i\to j}(\theta)e^{-r_i(\theta)\tau}.
$$

Ora consideriamo una traiettoria completa osservata su $[0,T]$. Essa è composta da una successione di tratti:

$$
(i_0,\tau_0,i_1),
\quad
(i_1,\tau_1,i_2),
\quad
\dots,
\quad
(i_{M-1},\tau_{M-1},i_M),
$$

dove $\tau_m$ è il tempo trascorso nello stato $i_m$ prima del salto verso $i_{m+1}$.

Per ciascun tratto, il contributo alla likelihood è

$$
w_{i_m\to i_{m+1}}(\theta)
e^{-r_{i_m}(\theta)\tau_m}.
$$

Moltiplicando i contributi di tutti i tratti osservati, otteniamo

$$
L(\theta)
= \prod_{m=0}^{M-1}
w_{i_m\to i_{m+1}}(\theta)
e^{-r_{i_m}(\theta)\tau_m}.
$$

Separando il prodotto dei tassi dal prodotto degli esponenziali,

$$
L(\theta)
=\left[ \prod_{m=0}^{M-1} w_{i_m\to i_{m+1}}(\theta)\right]
\exp\left[ -\sum_{m=0}^{M-1} r_{i_m}(\theta)\tau_m\right].
$$

A questo punto raggruppiamo i termini. Sia $N_{ij}$ il numero di salti osservati da $i$ a $j$:

$$ N_{ij} = \#\{m: i_m=i,\, i_{m+1}=j\}. $$

Sia invece $T_i$ il tempo totale passato nello stato $i$:

$$ T_i = \sum_{m:\,i_m=i}\tau_m.$$

Allora

$$
\prod_{m=0}^{M-1} w_{i_m\to i_{m+1}}(\theta) = \prod_{i\ne j} w_{i\to j}(\theta)^{N_{ij}},
$$

mentre

$$ \sum_{m=0}^{M-1} r_{i_m}(\theta)\tau_m = \sum_i T_i r_i(\theta). $$

Quindi la likelihood della traiettoria completa diventa

$$
L(\theta) = \prod_{i\ne j} w_{i\to j}(\theta)^{N_{ij}}
\exp\left[ -\sum_i T_i r_i(\theta) \right].
$$

La log-likelihood è quindi

$$
\ell(\theta) =
\sum_{i\ne j}N_{ij}\log w_{i\to j}(\theta)
- \sum_i T_i r_i(\theta).
$$

## 9.2 Tassi liberi

Se ogni tasso $w_{i\to j}$ è un parametro libero, la log-likelihood è

$$
\ell=
\sum_{i\ne j}N_{ij}\log w_{i\to j} - \sum_i T_i\sum_{j\ne i}w_{i\to j}.
$$

Derivando rispetto a $w_{i\to j}$:

$$
\frac{\partial \ell}{\partial w_{i\to j}} = \frac{N_{ij}}{w_{i\to j}}-T_i.
$$

Ponendo a zero:

$$ \hat w_{i\to j}=\frac{N_{ij}}{T_i}. $$

Interpretazione:

> il tasso stimato è il numero di eventi osservati diviso per il tempo totale di esposizione allo stato di partenza.

Questa è una formula fondamentale. Ricorre in processi di Poisson, modelli epidemici, reazioni chimiche e processi di nascita--morte.

# 10. Stima nelle SDE da dati discretizzati

Consideriamo una SDE di Itô in una dimensione:

$$ dX_t=a(X_t,\theta)dt+b(X_t,\theta)dW_t. $$

Supponiamo di osservare la traiettoria a tempi discreti:

$$ t_0,t_1,\dots,t_N, \qquad \Delta t=t_{k+1}-t_k, $$

con dati

$$ x_0,x_1,\dots,x_N. $$

Per piccoli $\Delta t$, lo schema di Euler--Maruyama suggerisce l'approssimazione

$$ X_{k+1}\approx X_k+a(X_k,\theta)\Delta t +b(X_k,\theta)\sqrt{\Delta t}\,\xi_k, $$

con

$$ \xi_k\sim\mathcal{N}(0,1). $$

Quindi, condizionatamente a $X_k=x_k$,

$$ X_{k+1}\mid X_k=x_k \approx
\mathcal{N}\left( x_k+a(x_k,\theta)\Delta t, \; b(x_k,\theta)^2\Delta t \right).
$$
## 10.1 Log-likelihood approssimata

Per piccoli $\Delta t$, lo schema di Euler--Maruyama suggerisce che, condizionatamente a $X_k=x_k$,

$$ X_{k+1}\mid X_k=x_k \approx
\mathcal{N}\left( x_k+a(x_k,\theta)\Delta t, \; b(x_k,\theta)^2\Delta t \right).
$$

Questo non è un risultato esatto: è un'approssimazione valida per $\Delta t$ piccolo. Per alcuni modelli, come l'Ornstein--Uhlenbeck, la densità di transizione esatta è nota e permette di costruire una likelihood più accurata (si veda la nota nella sezione 10.3). In generale, però, l'approssimazione di Euler--Maruyama è lo strumento principale disponibile.

La log-likelihood approssimata è

$$
\ell(\theta)
\approx
-\frac{1}{2}\sum_{k=0}^{N-1}
\left[
\log\left(2\pi b(x_k,\theta)^2\Delta t\right)
+
\frac{\left(x_{k+1}-x_k-a(x_k,\theta)\Delta t\right)^2}{b(x_k,\theta)^2\Delta t}
\right].
$$

Questa formula trasforma la stima di un modello continuo in un problema di ottimizzazione su incrementi discreti.

## 10.2 Caso con diffusione costante nota

Se

$$
b(x,\theta)=\sigma
$$

è nota e costante, massimizzare la log-likelihood equivale a minimizzare

$$
\sum_{k=0}^{N-1}
\left(x_{k+1}-x_k-a(x_k,\theta)\Delta t\right)^2.
$$

La stima del drift diventa quindi un problema di regressione (in questo quadro di *minimi quadrati*) sugli incrementi.

Definendo

$$
\Delta x_k=x_{k+1}-x_k,
$$

abbiamo approssimativamente

$$
\frac{\Delta x_k}{\Delta t}=a(x_k,\theta)+\text{rumore di scala }\frac{1}{\sqrt{\Delta t}}.
$$

Bisogna però fare attenzione: dividere per $\Delta t$ amplifica il rumore. Per questo è spesso più stabile lavorare direttamente sugli incrementi $\Delta x_k$, in modo da avere 

$$
\Delta x_k=a(x_k,\theta)\,\Delta t+\text{rumore di scala }\sqrt{\Delta t}.
$$

## 10.3 Caso Ornstein--Uhlenbeck

Consideriamo

$$
dX_t=-\gamma X_t\,dt+\sigma dW_t.
$$

Usando Euler--Maruyama:

$$
X_{k+1}=X_k-\gamma X_k\Delta t+\sigma\sqrt{\Delta t}\,\xi_k.
$$

Quindi

$$
\Delta x_k=-\gamma x_k\Delta t+\sigma\sqrt{\Delta t}\,\xi_k.
$$

Se $\sigma$ è nota, la MLE di $\gamma$ coincide con il minimo quadrato di

$$
\Delta x_k+\gamma x_k\Delta t.
$$

Minimizziamo

$$
Q(\gamma)=\sum_k(\Delta x_k+\gamma x_k\Delta t)^2.
$$

Derivando:

$$
\frac{dQ}{d\gamma}
=2\sum_k(\Delta x_k+\gamma x_k\Delta t)x_k\Delta t.
$$

Ponendo a zero:

$$
\sum_k x_k\Delta x_k+\gamma\Delta t\sum_k x_k^2=0.
$$

Quindi

$$
\hat\gamma=
-\frac{\sum_k x_k\Delta x_k}{\Delta t\sum_k x_k^2}.
$$

Questa formula è utile didatticamente, ma va interpretata con cautela: essa deriva dalla likelihood approssimata di Euler--Maruyama. Per l'Ornstein--Uhlenbeck, invece, la densità di transizione esatta è nota esplicitamente -- cioè la funzione di Green della Fokker--Planck associata -- e può essere usata per costruire una likelihood più accurata quando il passo di campionamento $\Delta t$ non è infinitesimo.

> **Nota:** Nel caso dell'Ornstein--Uhlenbeck la likelihood non deve necessariamente essere costruita usando l'approssimazione di Euler--Maruyama. Infatti il propagatore esatto, cioè la densità di transizione $p(x_{k+1}\mid x_k)$, è noto ed è gaussiano:
> $$ X_{k+1}\mid X_k=x_k \sim \mathcal{N} \left( x_k e^{-\gamma\Delta t}\,,\, \frac{\sigma^2}{2\gamma} \left(1-e^{-2\gamma\Delta t}\right) \right).$$
> Poiché questa densità è esplicita, si può costruire direttamente la log-likelihood esatta della traiettoria discretamente osservata. Per $\Delta t$ piccolo, questa transizione si riduce all'approssimazione di Euler--Maruyama; per $\Delta t$ non infinitesimo, invece, il propagatore esatto fornisce una stima più accurata.

# 11. Diagnostica, overfitting e problemi numerici

La stima di parametri non è solo applicare una formula. Nei modelli realistici serve diagnostica.

## 11.1 Identificabilità

Un parametro è identificabile se valori diversi producono distribuzioni osservabili diverse.

Se due valori $\theta_1$ e $\theta_2$ generano la stessa distribuzione dei dati,

$$
p(x\mid\theta_1)=p(x\mid\theta_2),
$$

allora nessun metodo statistico può distinguerli dai dati.

Sintomi di non identificabilità:

- log-likelihood piatta lungo una direzione;
- Hessiano quasi singolare;
- forti correlazioni tra parametri;
- stime instabili al cambiare del campione;
- intervalli di confidenza enormi.

## 11.2 Massimi locali

Nei modelli non lineari, la log-likelihood può avere più massimi locali. In questo caso l'ottimizzazione dipende dal punto iniziale.

Buone pratiche:

- provare più inizializzazioni;
- visualizzare sezioni della log-likelihood;
- controllare il valore finale della funzione obiettivo;
- usare metodi globali quando necessario;
- verificare che il massimo trovato sia compatibile con il comportamento simulato del modello.

## 11.3 Vincoli sui parametri

Molti parametri hanno vincoli:

$$
\lambda>0,
\qquad
\sigma^2>0,
\qquad
0<p<1.
$$

Ignorare questi vincoli può produrre stime prive di senso.

Strategie comuni:

- parametrizzare $\lambda=e^\alpha$ per imporre positività;
- parametrizzare $p=1/(1+e^{-\alpha})$ per imporre $0<p<1$;
- usare ottimizzazione vincolata;
- aggiungere controlli numerici contro valori non ammissibili.

## 11.4 Underflow e stabilità numerica

Calcolare direttamente

$$
L(\theta)=\prod_i p(x_i\mid\theta)
$$

è spesso sbagliato numericamente. Anche probabilità moderate, moltiplicate molte volte, diventano più piccole della precisione macchina.

Regola pratica:

> non massimizzare mai prodotti di probabilità quando puoi massimizzare somme di log-probabilità.

## 11.5 Dati correlati

Se i dati sono autocorrelati, la log-likelihood indipendente

$$
\ell(\theta)=\sum_i\log p(x_i\mid\theta)
$$

è generalmente errata. Può dare stime distorte o incertezze troppo ottimistiche.

Possibili rimedi:

- usare la likelihood di traiettoria;
- stimare il tempo di autocorrelazione;
- sottocampionare solo se giustificato;
- usare errori standard robusti;
- simulare dal modello stimato e confrontare autocorrelazioni empiriche.

## 11.6 Overfitting

Aumentare il numero di parametri migliora quasi sempre la likelihood sui dati di training, ma non necessariamente la capacità predittiva.

Per confrontare modelli con complessità diversa si usano criteri penalizzati che bilanciano adattamento ai dati e numero di parametri. I più comuni, AIC e BIC, sono introdotti nella sezione 12.5.

# 12. Confronto modello-dati e goodness-of-fit

Stimare i parametri non basta. Una volta ottenuto $\hat\theta$, bisogna chiedersi se il modello stimato sia effettivamente compatibile con i dati osservati.

Questa fase è detta **diagnostica del modello** o **goodness-of-fit**.

Il punto concettuale è importante:

> una stima di massima likelihood esiste quasi sempre, ma questo non significa che il modello sia buono.

Anche un modello sbagliato può avere un valore di $\hat\theta$ che massimizza la likelihood dentro la famiglia scelta. La domanda successiva è quindi:

> il modello con parametro $\hat\theta$ riproduce le proprietà statistiche rilevanti dei dati?

## 12.1 QQ-plot

Il **QQ-plot** confronta i quantili empirici dei dati con i quantili teorici del modello stimato.

Supponiamo di avere dati ordinati

$$
y_{(1)}\le y_{(2)}\le \cdots \le y_{(n)}.
$$

Se $F_{\hat\theta}$ è la CDF del modello stimato, i quantili teorici corrispondenti sono

$$
q_i=F_{\hat\theta}^{-1}\left(\frac{i-1/2}{n}\right).
$$

Si disegna quindi il grafico dei punti

$$
(q_i,y_{(i)}).
$$

Se il modello descrive bene i dati, i punti dovrebbero disporsi approssimativamente lungo la bisettrice.

Il QQ-plot è particolarmente utile per vedere discrepanze nelle code:

- code empiriche più pesanti del modello producono deviazioni alle estremità;
- asimmetrie non catturate dal modello producono curvature sistematiche;
- outlier appaiono come punti molto lontani dalla tendenza principale.

## 12.2 Test di Kolmogorov--Smirnov

Il test di Kolmogorov--Smirnov confronta la CDF empirica

$$
\hat F_n(x)
$$

con la CDF teorica del modello

$$
F_{\hat\theta}(x).
$$

La statistica del test è

$$
D_n=\sup_x |\hat F_n(x)-F_{\hat\theta}(x)|.
$$

Essa misura la massima distanza verticale tra le due funzioni di distribuzione.

Una cautela importante: nella forma standard, il test KS assume che i parametri del modello siano noti. Se invece $\hat\theta$ è stato stimato dagli stessi dati, la distribuzione nulla della statistica cambia. Di conseguenza, i p-value standard possono essere fuorvianti.

In pratica, per un uso didattico, il KS test è utile come diagnostica esplorativa, ma non va trattato come verdetto automatico.

## 12.3 Residui trasformati per processi puntuali

Per processi puntuali, come eventi osservati nel tempo, esiste una diagnostica molto elegante.

Supponiamo di osservare eventi ai tempi

$$
t_1,t_2,\dots,t_n
$$

su un intervallo $[0,T]$, e di avere un modello con intensità condizionata stimata

$$
\lambda_{\hat\theta}^*(t).
$$

Si definisce la variabile trasformata

$$
\tau_k = \int_0^{t_k}\lambda_{\hat\theta}^*(s)\,ds.
$$

Questa quantità non ha le dimensioni di un tempo fisico: poiché $\lambda_{\hat\theta}^*(s)$ è un tasso, l'integrale $\lambda_{\hat\theta}^*(s)\,ds$ è adimensionale. La variabile $\tau_k$ rappresenta quindi il numero atteso cumulativo di eventi fino al tempo $t_k$ secondo il modello stimato. Per questo viene talvolta chiamata *tempo trasformato* o *tempo operativo*: non misura il tempo in unità fisiche, ma il tempo nella scala interna del processo di eventi.

Se il modello è corretto, gli eventi trasformati

$$
\tau_1,\tau_2,\dots
$$

si comportano come gli eventi di un processo di Poisson omogeneo di tasso $1$ rispetto alla variabile $\tau$. Equivalentemente, gli incrementi

$$
z_k =\tau_k-\tau_{k-1}
= \int_{t_{k-1}}^{t_k}\lambda_{\hat\theta}^*(s)\,ds
$$

dovrebbero essere indipendenti e distribuiti come

$$ z_k\sim \mathrm{Exp}(1). $$

Quindi si può costruire un QQ-plot degli $z_k$ contro una distribuzione esponenziale standard. Se i residui trasformati non sono esponenziali, il modello non sta catturando correttamente la struttura temporale degli eventi.

## 12.4 Confronto tra dati osservati e dati simulati

Quando il modello è simulabile, una diagnostica molto naturale è il confronto tra dati osservati e dati simulati.

La procedura è:

1. stimare $\hat\theta$;
2. simulare molte traiettorie dal modello con parametro $\hat\theta$;
3. calcolare sulle simulazioni le stesse statistiche osservate nei dati reali;
4. confrontare distribuzioni empiriche, momenti, autocorrelazioni, tempi di primo passaggio o altre quantità rilevanti.

Questo è spesso più informativo di un singolo valore di likelihood, perché permette di controllare proprietà specifiche del fenomeno.

Esempi:

- per una SDE: media, varianza, distribuzione marginale, autocorrelazione;
- per un processo di salto: numero di eventi, tempi di attesa, occupazione degli stati;
- per un modello epidemico: picco, tempo del picco, dimensione finale dell'epidemia;
- per un agent-based model: distribuzione finale degli stati, clustering, tempo di convergenza.

## 12.5 AIC e BIC

Quando si confrontano modelli diversi, non basta scegliere quello con log-likelihood più alta. Un modello con più parametri tende quasi sempre ad adattarsi meglio ai dati, anche quando la complessità aggiuntiva non è realmente giustificata.

Per questo si usano criteri penalizzati.

L'**Akaike Information Criterion** è

$$
\mathrm{AIC}=2k-2\ell(\hat\theta),
$$

dove $k$ è il numero di parametri.

Il **Bayesian Information Criterion** è

$$
\mathrm{BIC}=k\log n-2\ell(\hat\theta),
$$

dove $n$ è il numero di osservazioni.

In entrambi i casi, valori più bassi indicano un compromesso migliore tra adattamento e complessità.

BIC penalizza la complessità più fortemente di AIC quando $n$ è grande.

# 13. Quando la likelihood è intrattabile

Nei modelli semplici, la likelihood si può scrivere esplicitamente. Questo accade per Bernoulli, Poisson, gaussiane, catene di Markov finite osservate completamente, processi di salto con traiettorie complete e alcune SDE osservate su griglie fini.

Nei modelli stocastici complessi, però, la likelihood può essere impossibile o molto costosa da calcolare.

Questo accade quando:

- alcune variabili sono latenti o non osservate;
- si osservano solo statistiche aggregate della traiettoria;
- lo spazio degli stati è enorme;
- il modello è agent-based;
- la dinamica è simulabile, ma la densità di probabilità dei dati non è nota;
- la likelihood richiede una somma o un integrale su troppe configurazioni nascoste.

In questi casi bisogna cambiare strategia.

L'idea generale diventa:

> se non posso calcolare la probabilità dei dati, posso comunque simulare il modello e confrontare dati simulati e dati osservati.

## 13.1 Metodo dei momenti simulati

Il **metodo dei momenti simulati** confronta statistiche riassuntive dei dati osservati con le stesse statistiche calcolate su simulazioni del modello.

Sia

$$
m_{\mathrm{obs}}
$$

un vettore di statistiche osservate. Per esempio:

$$
m_{\mathrm{obs}}=(\text{media},\text{varianza},\text{autocorrelazione a lag }1).
$$

Per ogni valore del parametro $\theta$, simuliamo il modello e calcoliamo le stesse statistiche:

$$
m_{\mathrm{sim}}(\theta).
$$

Lo stimatore sceglie il parametro che minimizza una distanza tra statistiche osservate e simulate:

$$
\hat\theta_{\mathrm{SMM}}
=
\arg\min_\theta
\left[m_{\mathrm{obs}}-m_{\mathrm{sim}}(\theta)\right]^T
W
\left[m_{\mathrm{obs}}-m_{\mathrm{sim}}(\theta)\right].
$$

Nel caso più semplice, $W$ è l'identità.

## 13.2 Scelta delle statistiche

La scelta delle statistiche è il punto cruciale.

Devono essere:

- informative rispetto ai parametri;
- robuste al rumore campionario;
- riproducibili tramite simulazione;
- non eccessivamente ridondanti;
- interpretabili nel contesto del modello.

Per esempio:

- in una SDE, media, varianza e autocorrelazione possono informare su drift e diffusione;
- in un processo di branching, media e varianza della popolazione per generazione informano sul numero medio di discendenti;
- in un modello agent-based, cluster finali, polarizzazione o tempi di convergenza possono informare sui parametri di interazione.

Il limite del metodo è chiaro: se le statistiche scelte non catturano aspetti importanti dei dati, la stima può essere fuorviante.

## 13.3 Approximate Bayesian Computation

L'**Approximate Bayesian Computation** (ABC) è un approccio bayesiano per modelli simulabili ma con likelihood intrattabile.

Nel quadro bayesiano si vorrebbe calcolare

$$
p(\theta\mid y_{\mathrm{obs}})
\propto
p(y_{\mathrm{obs}}\mid\theta)p(\theta),
$$

ma il termine

$$
p(y_{\mathrm{obs}}\mid\theta)
$$

è proprio la likelihood, che in questo caso non sappiamo valutare.

ABC evita di calcolare la likelihood. Usa invece la simulazione.

Lo schema più semplice è l'**ABC rejection sampler**:

1. estrai un parametro dal prior:
   $$
   \theta\sim p(\theta);
   $$
2. simula dati dal modello:
   $$
   y_{\mathrm{sim}}\sim p(\cdot\mid\theta);
   $$
3. calcola statistiche riassuntive:
   $$
   s(y_{\mathrm{sim}}),\qquad s(y_{\mathrm{obs}});
   $$
4. accetta $\theta$ se
   $$
   d\bigl(s(y_{\mathrm{sim}}),s(y_{\mathrm{obs}})\bigr)
   \le \varepsilon;
   $$
5. ripeti fino a ottenere molti parametri accettati.

I parametri accettati approssimano la distribuzione a posteriori.

## 13.4 Il ruolo di $\varepsilon$

Il parametro

$$
\varepsilon
$$

controlla quanto i dati simulati devono essere vicini ai dati osservati.

Se $\varepsilon$ è molto piccolo, l'approssimazione è più accurata, ma il tasso di accettazione può diventare bassissimo.

Se $\varepsilon$ è grande, si accettano molti parametri, ma la posteriore approssimata è troppo larga e poco informativa.

ABC richiede quindi un compromesso tra accuratezza e costo computazionale.

## 13.5 ABC come idea finale della lezione

In questa lezione ABC non va visto come un nuovo argomento da sviluppare tecnicamente in dettaglio, ma come una conclusione naturale del percorso.

Abbiamo tre livelli:

1. **Likelihood esplicita**: si usa MLE direttamente.
2. **Likelihood approssimata**: si usa una transizione approssimata, come Euler--Maruyama per SDE.
3. **Likelihood intrattabile ma simulazione possibile**: si usano SMM, ABC o metodi simulation-based.

ABC è quindi utile come messaggio finale:

> nei modelli stocastici complessi, la simulazione non serve solo a generare esempi, ma diventa parte dell'inferenza.

# 14. Sintesi finale

La stima dei parametri trasforma la modellizzazione stocastica in un problema inverso. Il modello assegna probabilità ai dati; la likelihood usa i dati osservati per valutare quali parametri li rendono più plausibili.

La log-likelihood è lo strumento operativo fondamentale perché:

- trasforma prodotti in somme;
- evita instabilità numeriche;
- semplifica derivate e ottimizzazione;
- consente una interpretazione informazionale;
- collega inferenza, entropia e divergenza KL.

La massima verosimiglianza produce stimatori naturali in molti modelli elementari: frequenze empiriche per Bernoulli e catene di Markov, medie campionarie per Poisson e gaussiane, tassi evento/tempo per processi di salto.

Nei modelli dinamici, però, la dipendenza temporale è essenziale. Non basta moltiplicare densità marginali: bisogna costruire la likelihood della traiettoria o una sua approssimazione coerente.

Dopo la stima, bisogna confrontare il modello con i dati tramite diagnostiche: QQ-plot, distribuzioni simulate, autocorrelazioni, residui trasformati e criteri penalizzati come AIC e BIC.

Infine, quando la likelihood è intrattabile ma il modello è simulabile, la simulazione diventa uno strumento inferenziale. Metodi come i momenti simulati e ABC permettono di stimare o restringere i parametri confrontando statistiche osservate e simulate.

Il messaggio conclusivo è quindi:

> l'inferenza nei modelli stocastici non è separata dalla simulazione; nei modelli complessi, spesso passa proprio attraverso di essa.

---

# 15. Esercizi

## Esercizio 1 -- Bernoulli

Si osservano $n=100$ prove Bernoulli, con $k=37$ successi.

1. Scrivere la likelihood.
2. Scrivere la log-likelihood.
3. Calcolare la MLE di $p$.
4. Calcolare la seconda derivata della log-likelihood nel massimo.

## Esercizio 2 -- Poisson

Si osservano i conteggi

$$
3,2,4,1,0,3,5,2.
$$

1. Scrivere la log-likelihood per $\lambda$.
2. Calcolare $\hat\lambda$.
3. Interpretare il risultato come media empirica.

## Esercizio 3 -- Tempi di attesa esponenziali

Si osservano tempi di attesa

$$
0.4,\ 1.2,\ 0.7,\ 0.3,\ 1.0.
$$

1. Scrivere la log-likelihood.
2. Calcolare la MLE del tasso $\lambda$.
3. Spiegare perché il tasso stimato è l'inverso del tempo medio.

## Esercizio 4 -- Catena di Markov

Una traiettoria osservata visita gli stati $A$ e $B$. Si contano le transizioni:

$$
N_{AA}=10,
\qquad
N_{AB}=5,
\qquad
N_{BA}=4,
\qquad
N_{BB}=11.
$$

1. Stimare la matrice di transizione.
2. Verificare che ogni riga sommi a uno.
3. Discutere che cosa accade se da uno stato si osservano pochissime uscite.

## Esercizio 5 -- Processo di salto a due stati

Un processo a due stati ha tassi

$$
w_{1\to 2}=\alpha,
\qquad
w_{2\to 1}=\beta.
$$

In una traiettoria osservata si misurano:

$$
N_{12}=18,
\qquad
T_1=9.0,
\qquad
N_{21}=12,
\qquad
T_2=8.0.
$$

1. Scrivere la log-likelihood.
2. Calcolare $\hat\alpha$ e $\hat\beta$.
3. Interpretare le stime come eventi per unità di tempo.

## Esercizio 6 -- SDE con drift lineare

Si considera l'approssimazione discreta

$$
X_{k+1}=X_k-\gamma X_k\Delta t+\sigma\sqrt{\Delta t}\xi_k.
$$

Assumendo $\sigma$ nota:

1. scrivere la log-likelihood approssimata;
2. derivare la formula della MLE di $\gamma$;
3. discutere perché la stima può essere sensibile a $\Delta t$.

## Esercizio 7 -- Diagnostica

Per un modello con due parametri, l'Hessiano negativo della log-likelihood nel massimo è

$$
\mathcal{I}_{\mathrm{obs}}
=\begin{pmatrix}
100 & 95 \\
95 & 91
\end{pmatrix}.
$$

1. Discutere qualitativamente se i parametri sono fortemente correlati.
2. Spiegare perché una matrice quasi singolare indica possibile non identificabilità.
3. Proporre due controlli diagnostici.

## Esercizio 8 -- Goodness-of-fit

Si stima un modello esponenziale per tempi di attesa osservati.

1. Descrivere come costruire un QQ-plot.
2. Spiegare quali deviazioni indicano code più pesanti del modello.
3. Discutere perché un buon valore di likelihood non garantisce automaticamente un buon adattamento.

## Esercizio 9 -- Momenti simulati

Un modello agent-based non ha likelihood calcolabile, ma può essere simulato.

1. Proporre tre statistiche riassuntive utili.
2. Scrivere la funzione obiettivo del metodo dei momenti simulati.
3. Discutere perché la scelta delle statistiche è cruciale.

## Esercizio 10 -- ABC

Si vuole stimare un parametro $\theta$ di un modello simulabile ma con likelihood intrattabile.

1. Scrivere lo schema dell'ABC rejection sampler.
2. Spiegare il ruolo della soglia $\varepsilon$.
3. Discutere il compromesso tra accuratezza e tasso di accettazione.
