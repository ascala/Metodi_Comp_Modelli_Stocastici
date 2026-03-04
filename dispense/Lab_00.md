---
title: "Introduzione ai modelli stocastici (Laboratorio 00)"
author: "Antonio Scala"
date: "25 Feb 2026"
---

# Obiettivi del laboratorio
In questo laboratorio useremo simulazioni numeriche per verificare tre fatti “universali” quando le variabili sono indipendenti e con varianza finita:

1. **Somme di variabili "well behaved"** $\Rightarrow$ convergenza (dopo riscalamento) a una **gaussiana** (Teorema del Limite Centrale).
2. **Errore sulla media**: $\mathrm{std}(\bar X_n)\propto n^{-1/2}$.
3. **Random walk**: ampiezza tipica $\propto t^{1/2}$ (diffusione).

Poi vedremo due estensioni:
* Un caso semplice in cui la somma scala come $n^\gamma$ con $\gamma\ne 1/2$ (code pesanti).
* Come costruire **due variabili correlate** partendo da due indipendenti, e come si generalizza a $n$ gaussiane.

# Parte A -- Somme e TLC: verso la gaussiana

### A1. Setup
Scegli una variabile $X$ **non gaussiana**, ma con varianza finita, ad esempio:
- uniforme $X\sim \mathrm{Unif}(0,1)$, oppure
- esponenziale (se vuoi richiamare il metodo dell’inversione).

Definisci:
$$
S_n=\sum_{i=1}^n X_i,\qquad
Z_n=\frac{S_n-n\mu}{\sigma\sqrt{n}},
$$
dove $\mu=E[X]$ e $\sigma^2=\mathrm{Var}(X)$.

### A2. Cosa verificare
Per $n$ crescente, l’istogramma di $Z_n$ tende a $N(0,1)$.

### A3. Pseudocodice
```

scegli X con mu, sigma noti
Nlist = [1,2,5,10,20,50,100]
M = grande (es. 10000)

for n in Nlist:
	lista_Z = []
	ripeti M volte:
		genera X_1,...,X_n i.i.d.
		S = somma(X_i)
		Z = (S - n*mu)/(sigma*sqrt(n))
		appendi Z a lista_Z
istogramma(lista_Z) e confronta con gaussiana standard

```

## Parte B -- Errore della media: legge $n^{-1/2}$

### B1. Idea
Ripetendo molte volte la stima della media campionaria
$$
\bar X_n=\frac1n\sum_{i=1}^n X_i,
$$
la dispersione delle $\bar X_n$ decresce come
$$
\mathrm{std}(\bar X_n)=\frac{\sigma}{\sqrt{n}}
\quad\Rightarrow\quad
\log \mathrm{std}(\bar X_n)\simeq -\frac12\log n + \mathrm{cost}.
$$
ovvero un plot in scala log-log dell'errore sulla media vs il numero di campioni deve approssimare una retta con pendenza $-1/2$.

### B2. Pseudocodice
```

scegli X con varianza finita
Nlist = [10,20,50,100,200,500,1000]
M = grande

for n in Nlist:
	lista_m = []
	ripeti M volte:
	genera X_1,...,X_n i.i.d.
	m = media(X_i)
	appendi m a lista_m
	err[n] = std(lista_m)

grafico log-log di err vs n
stima pendenza (fit lineare) -> atteso -1/2

```

**Domanda guida:** cosa cambia se prendi $X$ con varianza molto grande (ma finita)? quante repliche $M$ servono per vedere bene la pendenza?

---

## Parte C -- Random walk: diffusione $\sim t^{1/2}$

### C1. Modello
Considera un random walk 1D:
$$
X_{t+1}=X_t+\eta_t,\qquad \eta_t\in\{-1,+1\},\qquad P(\eta_t=\pm1)=\frac12,\qquad X_0=0.
$$

### C2. Due verifiche numeriche
1. **Gaussiana per $X_t/\sqrt{t}$** (ancora il TLC in azione – ma sui passi).
2. **Mean-square displacement**:
$$
\langle X_t^2\rangle \propto t
\quad\Rightarrow\quad
|X_t|_{\mathrm{tipico}}\propto \sqrt{t}.
$$

### C3. Pseudocodice
```

Tlist = [10,20,50,100,200,500,1000]
M = grande

for T in Tlist:
	lista_X = []
	ripeti M volte:
	X=0
	per k in 1..T:
		eta = choice([-1,+1])
		X += eta
		appendi X a lista_X

istogramma( lista_X / sqrt(T) )
msd[T] = media( X^2 su lista_X )

plot msd vs T e fit pendenza -> atteso 1

```

## Parte D -- Quando il $\sqrt{n}$ fallisce: somme con scala $n^\gamma$

Qui costruiamo un esempio con **code pesanti** e **varianza infinita**, dove il TLC classico non vale e la scala tipica della somma non e` $\sqrt{n}$.

### D1. Pareto: definizione
Sia $Y$ con densità Pareto su $[x_{\min},\infty)$:
$$
p_Y(y)=\alpha x_{\min}^{\alpha}y^{-(\alpha+1)},\qquad y\ge x_{\min}.
$$
Per $\alpha\in(1,2)$: $E[Y]$ e` finita ma $\mathrm{Var}(Y)=\infty$.

Per avere media zero (ed evitare drift), definiamo una variabile simmetrica $s\in\lbrace-1,1\rbrace$:
$$
X=s\,Y,\qquad P(s=\pm1)=\frac12.
$$

### D2. Costruzione esplicita di $F$ e inversione
Calcoliamo la CDF per $y\ge x_{\min}$:
$$
F_Y(y)=\int_{x_{\min}}^{y}\alpha x_{\min}^{\alpha}t^{-(\alpha+1)}dt
=1-\left(\frac{x_{\min}}{y}\right)^{\alpha}.
$$
Invertiamo: posto $u=F_Y(y)$,
$$
u = 1-\left(\frac{x_{\min}}{y}\right)^{\alpha}
\Rightarrow
1-u=\left(\frac{x_{\min}}{y}\right)^{\alpha}
\Rightarrow
y=x_{\min}(1-u)^{-1/\alpha}.
$$
Quindi, con $U\sim\mathrm{Unif}(0,1)$,
$$
Y = x_{\min}(1-U)^{-1/\alpha},\qquad X=S\,Y.
$$

### D3. Cosa verificare: scala $n^\gamma$ con $\gamma=1/\alpha$
Per $\alpha\in(1,2)$, la somma
$$
S_n=\sum_{i=1}^n X_i
$$
ha scala tipica $S_n\sim n^{1/\alpha}$, quindi $\gamma=1/\alpha$.

**Verifica robusta (consigliata):** usa un quantile di $|S_n|$, ad esempio
$$
Q(n)=\mathrm{median}(|S_n|)\propto n^{1/\alpha}.
$$

### D4. Pseudocodice
```

alpha = 1.5
xmin = 1.0
Nlist = [10,30,100,300,1000,3000]
M = grande

fun pareto(alpha, xmin):
	U = Uniform(0,1)
	return xmin * (1-U)^(-1/alpha)

for n in Nlist:
	lista_S = []
	ripeti M volte:
		S = 0
		for i in 1..n:
		Y = pareto(alpha, xmin)
		sign = choice([-1,+1])
		X = sign*Y
		S += X
		appendi S a lista_S

Q[n] = median(abs(lista_S))
# opzionale: istogramma di S / n^(1/alpha) per vedere il collasso

plot log-log di Q vs n
fit pendenza -> atteso 1/alpha

```

**Domanda guida:** cosa succede se provi a stimare $\mathrm{std}(S_n)$ o $\mathrm{std}(\bar X_n)$? Perchè è una pessima idea in questo caso?

## Parte E -- Variabili correlate da indipendenti: costruzione esplicita in 2D

Qui vogliamo mostrare una cosa concreta: la correlazione si puo` ottenere introducendo una “parte comune” fra le variabili.

### E1. Da due indipendenti a due correlate
Sia $Z_1,Z_2$ una coppia indipendente con
$$
E[Z_i]=0,\qquad \mathrm{Var}(Z_i)=1.
$$
(Scelta pratica: gaussiane standard, ma il trucco funziona anche con altre distribuzioni.)

Definiamo:
$$
X = Z_1,\qquad
Y = \rho Z_1 + \sqrt{1-\rho^2}\,Z_2,
\qquad \rho\in(-1,1).
$$

### E2. Calcoli espliciti: varianze e covarianza
- Media:
$$
E[X]=0,\qquad E[Y]=\rho E[Z_1]+\sqrt{1-\rho^2}E[Z_2]=0.
$$
- Varianze:
$$
\mathrm{Var}(X)=1,
$$
e, usando indipendenza,
$$
\mathrm{Var}(Y)=\rho^2\mathrm{Var}(Z_1)+(1-\rho^2)\mathrm{Var}(Z_2)=\rho^2+(1-\rho^2)=1.
$$
- Covarianza:
$$
\mathrm{Cov}(X,Y)=\mathrm{Cov}(Z_1,\rho Z_1+\sqrt{1-\rho^2}Z_2)=\rho\,\mathrm{Var}(Z_1)=\rho.
$$
Quindi, siccome $\sigma_X=\sigma_Y=1$,
$$
\mathrm{Corr}(X,Y)=\rho.
$$

**Interpretazione:** $Y$ contiene una componente “comune” a $X$ (il termine $\rho Z_1$) piu` un rumore indipendente.

### E3. Pseudocodice (verifica numerica)
```

rho = 0.8
M = grande

for m in 1..M:
Z1 = Normal(0,1)
Z2 = Normal(0,1)
X[m] = Z1
Y[m] = rho*Z1 + sqrt(1-rho^2)*Z2

stima corr_hat = corr(X,Y)
stima cov_hat  = mean(X*Y)   # se le medie sono circa zero
scatter(X,Y) per vedere la "nuvola ellittica"

```

### E4. Estensione concettuale a $n$ gaussiane (senza dettagli algoritmici)
Se vuoi generare un vettore gaussiano $\mathbf{X}\in\mathbb{R}^n$ con covarianza assegnata $\Sigma$ (simmetrica, definita positiva), l’idea generale e`:
- parti da $\mathbf{Z}\sim N(\mathbf{0},I)$ (componenti indipendenti),
- costruisci una trasformazione lineare $\mathbf{X}=A\mathbf{Z}$ tale che
$$
\mathrm{Cov}(\mathbf{X})=\Sigma.
$$
Poiche`
$$
\mathrm{Cov}(A\mathbf{Z}) = A\,\mathrm{Cov}(\mathbf{Z})\,A^{\mathsf T} = A I A^{\mathsf T}=AA^{\mathsf T},
$$
serve una matrice $A$ con
$$
\Sigma = AA^{\mathsf T}.
$$

**In pratica, numericamente, si usa una fattorizzazione della matrice di covarianza**, ad esempio:
- una fattorizzazione triangolare (tipo Cholesky) se $\Sigma$ e` ben condizionata e definita positiva,
- oppure metodi basati su autovalori/SVD quando $\Sigma$ e` quasi singolare o stimata con rumore.

Nota: non e` “inversione della covarianza” per generare i campioni; l’inversa $\Sigma^{-1}$ compare spesso invece in statistica (es. densità gaussiana multivariata, regressione, stima), e si calcola numericamente tramite decomposizioni stabili (LU/QR/SVD) piuttosto che invertendo a mano.

### E5. Non-gaussiane: cosa resta vero e cosa no
Se in E1 scegli $Z_1,Z_2$ **non gaussiane**, la trasformazione lineare:
- impone comunque la **covarianza** e la **correlazione** desiderata (i calcoli sopra restano validi),
- ma la coppia $(X,Y)$ **non e` piu` congiuntamente gaussiana**: la “nuvola” può avere margini e code non gaussiane, e le proprietà tipiche del caso gaussiano (ellitticità perfetta, dipendenza descritta interamente da $\Sigma$) non valgono piu`.

## Checklist finale (cosa consegnare/mostrare)
1. Istogrammi di $Z_n$ per $n$ crescente (Parte A).
2. Grafico log--log di $\mathrm{std}(\bar X_n)$ vs $n$ con pendenza $\simeq -1/2$ (Parte B).
3. Grafico $\langle X_t^2\rangle$ vs $t$ (pendenza $\simeq 1$) e istogrammi di $X_t/\sqrt{t}$ (Parte C).
4. Grafico log--log di $Q(n)=\mathrm{median}(|S_n|)$ vs $n$ con pendenza $\simeq 1/\alpha$ (Parte D).
5. Stima numerica di $\mathrm{Corr}(X,Y)$ e scatter plot per vari $\rho$ (Parte E).
