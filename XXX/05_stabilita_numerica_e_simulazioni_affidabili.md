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
In simulazioni deterministiche, questo accade quando il modello è rigido o il passo temporale troppo grande; in simulazioni stocastiche, le fluttuazioni casuali possono amplificare l’instabilità numerica.

Esempio intuitivo: simulare la crescita logistica  
$$x_{t+1} = r\,x_t(1 - x_t)$$  
con un valore di $r$ troppo grande o un passo $\Delta t$ improprio può generare oscillazioni spurie o divergenze.

---

## 2. Tipi di errore nelle simulazioni

1. **Errore di arrotondamento:** dovuto alla rappresentazione finita dei numeri nel computer.  
2. **Errore di discretizzazione:** deriva dal fatto che si sostituiscono derivate con differenze finite.  
3. **Errore di propagazione:** l’accumulo degli errori di passo porta la simulazione a deviare.  
4. **Errore statistico:** in presenza di rumore, ogni simulazione è una realizzazione diversa del processo.

In pratica, la stabilità significa che l’errore complessivo non cresce senza controllo quando si prosegue la simulazione.

---

## 3. Come testare la stabilità di uno schema

Un modo semplice per verificare la stabilità consiste nel simulare lo stesso processo con diversi passi temporali $\Delta t$ e confrontare le traiettorie ottenute. Se la simulazione è stabile, le traiettorie convergono a un comportamento comune.

**Esempio (in Python):**

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_decay(dt, N):
    x = np.zeros(N)
    x[0] = 1.0
    for n in range(N-1):
        x[n+1] = x[n] - dt * x[n]  # semplice decadimento
    return x

for dt in [0.1, 0.5, 1.0]:
    N = int(10/dt)
    t = np.linspace(0, 10, N)
    plt.plot(t, simulate_decay(dt, N), label=f"dt={dt}")
plt.xlabel("tempo")
plt.ylabel("x(t)")
plt.legend()
plt.show()
````

Un $\Delta t$ troppo grande produce oscillazioni o valori negativi: segno di instabilità.

***

## 4. Scelta del passo temporale e convergenza

Non esiste una regola universale, ma si possono seguire alcune linee guida pratiche:

* Ridurre $\Delta t$ fino a che il risultato non cambia più in modo significativo.

* Confrontare la simulazione numerica con un caso analitico semplice, se disponibile.

* Osservare grandezze aggregate (es. medie o varianze) invece delle singole traiettorie.

* Ripetere la simulazione più volte per stimare la variabilità dovuta al rumore.

Il concetto chiave è la **convergenza empirica**: uno schema è accettabile se le sue stime si stabilizzano al diminuire del passo temporale.

***

## 5. Esempi interdisciplinari

* **Epidemiologia:** la scelta di un passo temporale troppo grande in un modello SIR può far scomparire o amplificare artificialmente un’epidemia.

* **Economia:** nei modelli di aspettative adattive, una discretizzazione eccessiva può creare cicli spurii.

* **Fisica:** nel moto browniano simulato con un rumore gaussiano, la stabilità determina se l’energia media resta costante o diverge.

* **Social network:** nelle simulazioni agent–based, una dinamica instabile può portare a polarizzazioni artificiali dovute non al modello, ma al numerico.

---

## Riferimenti

* Higham, D. J. (2001). *An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations*. SIAM Review, 43(3): 525–546.

* Press, W. H. et al. *Numerical Recipes: The Art of Scientific Computing*, Cambridge University Press.

* Gardiner, C. (2004). *Handbook of Stochastic Methods*, Springer.

* LeVeque, R. J. (2007). *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM.

* Gillespie, D. T. (2000). *The chemical Langevin equation*. J. Chem. Phys. 113(1): 297–306.
