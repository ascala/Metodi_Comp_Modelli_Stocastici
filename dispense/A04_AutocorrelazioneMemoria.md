---
title: "A04: Autocorrelazione, memoria e diagnostica della dipendenza temporale"
author: "Antonio Scala"
date: ""
---

Questa appendice presenta l’autocorrelazione come strumento diagnostico per analizzare la memoria temporale di un sistema stocastico, di una serie temporale o di una simulazione numerica. In molte situazioni pratiche i dati non sono indipendenti: osservazioni vicine nel tempo tendono a somigliarsi, e questa dipendenza altera sia l’interpretazione statistica sia la stima degli errori. Per questo motivo, l’autocorrelazione non è soltanto una quantità descrittiva, ma anche un indicatore operativo della qualità dell’informazione contenuta nei dati.

Il punto centrale è distinguere tra la correlazione dovuta alla media e quella dovuta alle fluttuazioni. Solo quest’ultima misura davvero la memoria dinamica del sistema. L’appendice insiste quindi su un taglio diagnostico: come si definiscono le funzioni corrette, come si stimano da dati discreti, quali errori di interpretazione sono frequenti e quali controlli conviene fare in pratica, specialmente nelle simulazioni Monte Carlo e MCMC.

### Obiettivi didattici specifici

1. Comprendere perché dati temporali o simulazioni successive non possano essere trattati automaticamente come indipendenti.
2. Definire autocorrelazione, autocovarianza e funzione normalizzata.
3. Distinguere tra contributo della media e correlazione delle fluttuazioni.
4. Interpretare il tempo di decorrelazione come scala di memoria.
5. Valutare l’impatto della correlazione sul numero effettivo di campioni indipendenti.
6. Usare l’autocorrelazione come strumento diagnostico nelle simulazioni stocastiche.

### Struttura della appendice

La discussione è organizzata in sei parti:

1. **Perché serve una diagnostica della memoria** -- quando i dati non sono indipendenti.  
2. **Definizioni fondamentali** -- funzione grezza, funzione connessa e normalizzazione.  
3. **Tempo di decorrelazione** -- come leggere la scala di memoria.  
4. **Stima su dati discreti** -- formule operative e limiti della coda.  
5. **Diagnostica pratica** -- segnali di allarme, errori comuni e numero effettivo di campioni.  
6. **Costo computazionale e FFT** -- come calcolare la correlazione in modo efficiente.  

---

## 1. Perché serve una diagnostica della memoria

Molti dataset reali e molte simulazioni producono osservazioni temporalmente dipendenti. Esempi tipici sono:

- traiettorie di processi stocastici;
- catene Monte Carlo;
- serie temporali economiche, sociali o ambientali;
- segnali sperimentali acquisiti nel tempo.

In tutti questi casi si pone la stessa domanda: quanto il valore presente dipende dal passato?

Se la dipendenza è forte, campioni consecutivi contengono informazione in gran parte ridondante. Se invece il sistema dimentica rapidamente il passato, osservazioni sufficientemente distanti possono essere considerate quasi indipendenti.

L’autocorrelazione è lo strumento standard per rispondere a questa domanda.

---

## 2. Definizioni fondamentali

Sia $f(t)$ una grandezza osservata nel tempo. La funzione di autocorrelazione grezza è
$$
R_f(\tau)=\overline{f(t+\tau)\,f(t)}.
$$

Questa quantità misura il grado di dipendenza lineare tra i valori della variabile separati da un ritardo $\tau$.

### 2.1 Problema della media non nulla

Se la media
$$
\bar f \neq 0,
$$
allora in generale, per ritardi grandi,
$$
R_f(\tau)\to \bar f^{\,2}.
$$
Questo significa che la funzione grezza non tende a zero nemmeno quando le fluttuazioni si sono completamente decorrelate. Rimane infatti il contributo della media.

Di conseguenza, usare $R_f(\tau)$ senza sottrarre la media può portare a una lettura fuorviante della memoria del sistema.

### 2.2 Funzione connessa

Per isolare la correlazione delle fluttuazioni si introduce
$$
C_f(\tau)=R_f(\tau)-\bar f^{\,2},
$$
equivalentemente
$$
C_f(\tau)=\overline{(f(t+\tau)-\bar f)(f(t)-\bar f)}.
$$

Questa è la quantità che interessa davvero nella maggior parte delle applicazioni.

### 2.3 Funzione normalizzata

Per confrontare casi diversi si usa spesso la correlazione normalizzata
$$
\hat C_f(\tau)=\frac{C_f(\tau)}{C_f(0)},
$$
per cui
$$
\hat C_f(0)=1.
$$

Questa normalizzazione elimina l’unità di misura e rende più leggibile il decadimento relativo della memoria.

---

## 3. Tempo di decorrelazione

In molti sistemi la funzione normalizzata decade approssimativamente come
$$
\hat C_f(\tau)\sim e^{-\tau/\tau_c},
$$
dove $\tau_c$ è il tempo di decorrelazione.

### 3.1 Interpretazione operativa

- se $\tau\ll\tau_c$, i campioni sono fortemente correlati;
- se $\tau\gg\tau_c$, i campioni sono quasi indipendenti.

Il tempo di decorrelazione è quindi una misura sintetica di quanto a lungo il sistema "ricordi" il proprio passato.

### 3.2 Avvertenza interpretativa

Non tutti i sistemi hanno un decadimento esponenziale semplice. Possono comparire:

- più scale temporali;
- code lente;
- oscillazioni;
- decadimenti non monotoni.

In questi casi $\tau_c$ va interpretato con cautela, come indice riassuntivo e non come descrizione esatta dell’intera dinamica.

---

## 4. Stima su dati discreti

Nella pratica si dispone di una sequenza
$$
f_0,f_1,\dots,f_{N-1}.
$$

Una stima della correlazione grezza al lag $k$ è
$$
R(k)\approx \frac{1}{N-k}\sum_{i=0}^{N-k-1}f_i f_{i+k}.
$$

La media campionaria è
$$
\bar f=\frac{1}{N}\sum_{i=0}^{N-1}f_i,
$$
e la funzione connessa si stima come
$$
C(k)\approx \frac{1}{N-k}\sum_{i=0}^{N-k-1}(f_i-\bar f)(f_{i+k}-\bar f).
$$

### 4.1 Perché la coda è rumorosa

Per lag grandi, il numero di coppie disponibili è solo $N-k$. Quando $k$ cresce:

- diminuiscono drasticamente i dati utili;
- la stima diventa più rumorosa;
- la parte finale della curva è spesso poco affidabile.

Di conseguenza, la coda della funzione di autocorrelazione va sempre letta con prudenza.

---

## 5. Diagnostica pratica della dipendenza temporale

Questa è la parte più operativa dell’appendice: come usare l’autocorrelazione per diagnosticare problemi reali.

### 5.1 Primo controllo: la media è stata sottratta?

Se non si sottrae la media, si rischia di interpretare come memoria ciò che in realtà è solo un offset costante. Questo è uno degli errori più frequenti.

### 5.2 Secondo controllo: il decadimento è rapido o lento?

Un decadimento rapido indica buona decorrelazione. Un decadimento lento segnala memoria lunga e, in simulazioni Monte Carlo, bassa efficienza statistica.

### 5.3 Terzo controllo: la coda è informativa o solo rumorosa?

Oscillazioni o picchi a grandi lag non sono automaticamente significativi. Spesso riflettono solo il fatto che il numero di coppie disponibili è troppo piccolo.

### 5.4 Quarto controllo: esiste una scala temporale chiara?

Se il decadimento presenta una scala caratteristica ben definita, il sistema ha una memoria semplice da interpretare. Se invece compaiono più regimi, la dinamica può essere multiscala.

---

## 6. Numero effettivo di campioni

Campioni correlati non equivalgono a campioni indipendenti. Questo è il motivo principale per cui l’autocorrelazione è così importante in statistica computazionale.

Se si osservano $N$ dati ma la memoria persiste per un tempo dell’ordine di $\tau_c$, allora il numero effettivo di campioni indipendenti è molto inferiore a $N$. In prima approssimazione,
$$
N_{\mathrm{eff}}\approx \frac{N}{\tau_c}.
$$

### 6.1 Conseguenza statistica

Se si ignora la correlazione, si sottostima l’errore statistico. Questo porta a intervalli di confidenza troppo ottimistici e a conclusioni apparentemente più solide di quanto siano davvero.

### 6.2 Caso Monte Carlo e MCMC

Nelle catene MCMC i campioni successivi sono costruiti apposta in modo dipendente. Il problema non è quindi eliminare del tutto la correlazione, ma misurarla e verificarne il decadimento.

Una catena efficiente ha:

- autocorrelazione che decade rapidamente;
- tempo di decorrelazione corto;
- numero effettivo di campioni indipendenti non troppo piccolo.

Una catena inefficiente, al contrario, può produrre moltissimi campioni nominali ma pochissima informazione realmente nuova.

---

## 7. Segnali di allarme nelle simulazioni

### 7.1 Correlazione che non decade

Può indicare:

- burn-in insufficiente;
- osservabile quasi conservata;
- mixing molto lento;
- simulazione troppo corta per vedere la decorrelazione.

### 7.2 Correlazione apparentemente nulla ma con grandi fluttuazioni in coda

Può semplicemente significare che la stima è dominata dal rumore per lag elevati.

### 7.3 Differenze marcate tra osservabili diverse

È normale che osservabili differenti abbiano tempi di decorrelazione differenti. Per questo non basta controllare una sola quantità.

### 7.4 Catena lunga ma ESS basso

È un segnale classico di inefficienza: molte iterazioni, poca informazione indipendente.

---

## 8. Costo computazionale e metodo FFT

Il calcolo diretto dell’autocorrelazione per tutti i lag richiede in generale un costo dell’ordine
$$
O(N^2),
$$
che può essere eccessivo per serie lunghe.

Poiché l’autocorrelazione è collegata alla convoluzione, si può usare la trasformata di Fourier. Sottraendo prima la media, si ottiene schematicamente
$$
C=\mathcal{F}^{-1}\left(|\mathcal{F}(f-\bar f)|^2\right).
$$

Questo riduce il costo a
$$
O(N\log N),
$$
rendendo il calcolo praticabile anche per dataset grandi.

---

## 9. Checklist diagnostica minima

Quando si analizza una funzione di autocorrelazione, conviene verificare almeno questi punti:

- [ ] La media è stata sottratta correttamente?
- [ ] Si sta guardando la funzione connessa o quella grezza?
- [ ] Il decadimento iniziale è rapido o lento?
- [ ] La coda è abbastanza ben campionata da essere interpretabile?
- [ ] Esiste una stima ragionevole del tempo di decorrelazione?
- [ ] Il numero effettivo di campioni è compatibile con la precisione richiesta?
- [ ] Nelle MCMC, l’analisi è stata fatta su più di un osservabile?

---

## 10. Take-home message

- L’autocorrelazione è uno strumento diagnostico per misurare la memoria temporale.
- La quantità davvero informativa è la correlazione delle fluttuazioni, non quella che include la media.
- Il tempo di decorrelazione fornisce una scala caratteristica della memoria del sistema.
- Campioni correlati implicano un numero effettivo di osservazioni indipendenti molto più piccolo del numero totale.
- Nelle simulazioni Monte Carlo e MCMC, ignorare l’autocorrelazione significa quasi sempre sottostimare l’errore statistico.
- Una buona analisi non si limita a tracciare una curva: controlla media, coda, scala di decadimento e impatto su $N_{\mathrm{eff}}$.
