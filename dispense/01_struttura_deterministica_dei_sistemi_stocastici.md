---
title: "01: Struttura deterministica dei sistemi stocastici"
date: ""
---

# PARTE I — Struttura deterministica

## 1. Sistemi autonomi unidimensionali

**Obiettivo della sezione**
Introdurre il concetto di dinamica deterministica continua nel caso più semplice, chiarendo:
* definizione di sistema autonomo 1D
* punti di equilibrio
* criterio locale di stabilità
* interpretazione geometrica tramite campo di direzioni

**Cosa fare concretamente**
* Scrivere $\dot x = f(x)$
* Definire equilibrio come $f(x^*)=0$
* Usare il segno di $f'(x^*)$ per la stabilità locale
* Introdurre l’idea di attrattore / repellore
* Rappresentazione grafica su asse reale (senza formalismi eccessivi)

Sezione molto sintetica, chiara, quasi “strutturale”.

## 2. Dinamica di gradiente e paesaggi

**Obiettivo della sezione**
Mostrare che molte dinamiche possono essere interpretate come discesa lungo un paesaggio di potenziale:
$$\dot x = -V'(x)$$

**Cosa fare concretamente**
* Introdurre il concetto di funzione potenziale
* Mostrare che $V$ decresce lungo le traiettorie
* Collegare:
  * minimi ↔ attrattori
  * massimi ↔ instabilità
  * barriere ↔ separazione di bacini

Questa è la sezione ponte verso:
* metastabilità
* Boltzmann
* simulated annealing
* escape con rumore

È concettualmente centrale.

## 3. Biforcazione transcritica

**Obiettivo della sezione**
Introdurre l’idea di cambiamento qualitativo della dinamica al variare di un parametro.

Modello guida:
$$\dot N = rN - N^2$$

**Cosa fare concretamente**

* Calcolare gli equilibri
* Studiare stabilità in funzione di $r$
* Mostrare che a $r=0$ avviene uno scambio di stabilità
* Interpretare $r=0$ come soglia critica

Collegamento diretto con:

* modelli di crescita
* branching
* soglia di sopravvivenza

Qui formalizzi matematicamente ciò che altrove usi in modo probabilistico.

## 4. Biforcazione saddle–node e tipping

**Obiettivo della sezione**
Mostrare come possano emergere e scomparire equilibri al variare di un parametro.

Modello guida:
$$\dot x = r + x^2$$

**Cosa fare concretamente**

* Calcolare condizioni di esistenza degli equilibri
* Mostrare collisione e annichilazione
* Interpretare il fenomeno come tipping
* Preparare il terreno per:
  * rumore impulsivo
  * escape rate
  * metastabilità

Questa sezione serve come anticamera naturale alla dinamica stocastica.

# PARTE II — Integrazione numerica delle ODE

## 5. Discretizzazione temporale

**Obiettivo della sezione**
Passare dalla dinamica continua alla dinamica numerica.

* Suddivisione dell’intervallo temporale
* Introduzione del passo $\Delta t$
* Concetto di approssimazione

Deve essere molto chiaro che ogni simulazione continua è in realtà discreta.

## 6. Metodo di Eulero esplicito

**Obiettivo della sezione**
Costruire il primo schema numerico:
$$x\_{n+1} = x\_n + f(x\_n)\Delta t$$

**Cosa fare concretamente**

* Derivazione come sviluppo al primo ordine
* Interpretazione geometrica
* Condizioni di stabilità numerica
* Effetto del passo temporale

Qui si collega direttamente alla parte su stabilità numerica del corso.

## 7. Errori numerici e stabilità

**Obiettivo della sezione**

* Definire errore locale
* Definire errore globale
* Mostrare che l’errore dipende da $\Delta t$
* Distinguere tra stabilità del modello e stabilità dello schema

Questa è la parte metodologica più importante per un corso computazionale.

# APPENDICE — Sistemi discreti

## A1. Equazioni alle differenze

**Obiettivo della sezione**

Ripetere rapidamente:
$$ x_{n+1} = g(x_n)$$
* punti fissi
* stabilità via $|g'(x^*)| < 1$
* confronto con ODE

Molto sintetico.

## A2. Mapping ODE ↔ sistemi discreti

**Obiettivo della sezione**

Mostrare che:

* ogni ODE discretizzata genera un sistema discreto
* ogni sistema discreto può essere interpretato come dinamica approssimata

Esplicitare:
$$ x_{n+1} - x_n \approx f(x_n)\Delta t $$

Qui chiarisci una cosa concettualmente forte:
> La simulazione numerica è sempre un sistema discreto che approssima una dinamica continua.

## Riferimenti
