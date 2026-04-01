# Convenzioni di formattazione — file PR_*.md

Queste convenzioni sono estratte dai file originali del corso.
Devono essere rispettate esattamente quando si riscrive o ristruttura un file.

---

## 1. Matematica display

Blocchi display math: `$$` su riga separata, contenuto nel mezzo, `$$` su riga separata.

```
$$
\lambda^*(t) = \mu + \sum_{t_k < t} \phi(t - t_k)
$$
```

MAI scrivere `$$formula$$` su una sola riga.
MAI aggiungere backslash alla fine della riga dentro un blocco math.

---

## 2. Matematica inline

Delimitatori `$...$` sulla stessa riga, senza spazi extra interni.

```
il tasso $\lambda$ è costante
la probabilità $p_i(t)$ che il nodo $i$ sia infetto
```

---

## 3. Underscore e apici

Dentro math (sia display che inline): underscore e apice liberi, MAI escapati.

```
# CORRETTO
$x_i$, $t_k$, $x_1 < x_2$, $R_0$, $\lambda^*(t)$, $e^{-\beta s}$

# SBAGLIATO
$x\_i$, $t\_k$, $\lambda\^*(t)$
```

Fuori da math (testo normale): underscore va escapato solo nei nomi di file/variabili
dove potrebbe essere interpretato come corsivo Markdown.

---

## 4. Graffe

Le graffe hanno due usi distinti in LaTeX:

**Argomento di comando** — NON escapate:
```
\frac{a}{b}
\sum_{i=1}^{n}
\mathbb{R}^n
\text{evento in}
\mathbf{1}_{A}
\begin{cases} ... \end{cases}
```

**Delimitatori di insieme o vincolo** — SEMPRE escapate:
```
N(t) \in \{0, 1, 2, 3, \dots\}
X_k(t) \in \{0, 1\}
r_k \in \{-1, 1\}
\Delta_n = \left\{x \in \mathbb{R}^n : x_i \ge 0\right\}
\mathcal{H}_t = \{t_k : t_k < t\}
\{t_k\}_{k \ge 1}
```

**MAI** scrivere `X \in {0,1}` — le graffe scompaiono nel rendering.

---

## 5. Comandi LaTeX usati nel corso (riferimento)

Comandi frequenti nei file originali:

```
\sum \frac \dfrac \int \log \max \min
\lambda \mu \beta \alpha \phi \rho \pi \tau \Delta
\dot{x} \bar{\lambda} \hat{\theta}
\left( \right) \left\{ \right\} \bigl( \bigr)
\text{...} \mathbf{...} \mathbb{...} \mathrm{...} \mathcal{...}
\in \ge \le \neq \approx \to \mid \cdot \cdots \dots
\qquad \quad \,
\begin{cases} ... \end{cases}
\begin{pmatrix} ... \end{pmatrix}
\binom{n}{k}
```

---

## 6. Caratteri non-ASCII

**Accentate italiane — sempre dirette, mai escape:**
```
à è é ì ò ù È
```

**Altri unicode accettabili nel testo:**
```
— (em-dash, U+2014)   es: "clustering temporale — gli eventi"
```

**Frecce:**
- Nel testo normale: usare LaTeX inline `$\to$`, `$\rightarrow$`, `$\Rightarrow$`, `$\leftarrow$` ecc.
- MAI `→` unicode nel testo normale
- Negli pseudocodici (dentro blocco ```text```): usare `->` ASCII

**MAI usare:**
- `→` unicode fuori dai blocchi ```text```
- Virgolette curve `" "` o `' '` — usare `"` e `'` ASCII
- Bullet `•` — usare `*` o `-` Markdown
- Qualsiasi altro unicode decorativo

---

## 7. Struttura del documento

- Heading di primo livello `#` per le sezioni principali numerate
- Heading di secondo livello `##` per le sottosezioni (es. `## 3.1 Titolo`)
- Heading di terzo livello `###` per sotto-sottosezioni (es. nei laboratori)
- Frontmatter YAML obbligatorio:

```yaml
---
title: "Project: [Titolo]"
subtitle: "[sottotitolo]"
author: "Antonio Scala"
---
```

Niente campo `date:`.

---

## 8. Pseudocodice

Gli pseudocodici usano blocchi ` ```text `. Dentro questi blocchi:

- **NON usare LaTeX** — non viene renderizzato
- Variabili con underscore ASCII: `x_i`, `lambda_star`, `p_i`
- Frecce di assegnazione: `->` o `<-` ASCII
- Operatori: `*`, `/`, `+`, `-`, `>=`, `<=`, `!=`
- Sommatorie e integrali: scritti in forma descrittiva es. `sum_{j in S} d(i,j)`

```text
# CORRETTO
lambda_star = mu + sum_{t_k < t} alpha * exp(-beta * (t - t_k))
if delta_C <= 0 -> accetta
x_i <- x_i + dt * (f_i - f_bar) * x_i
```

NON scrivere LaTeX dentro ```text:
```text
# SBAGLIATO
$\lambda^*(t) = \mu + \sum_{t_k < t} \alpha e^{-\beta(t-t_k)}$
```

---

## 9. Codice Python / R / MATLAB

Blocchi di codice con tripli backtick e nome linguaggio:

````
```python
# codice Python
```

```r
# codice R
```

```matlab
% codice MATLAB
```

```text
# pseudocodice o output testuale
```
````

Nomi di variabili/funzioni inline nel testo: backtick singoli `` `nome_variabile` ``.
