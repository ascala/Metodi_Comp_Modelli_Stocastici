---
title: "Project: Affidabilita' e copule"
subtitle: "dipendenza tra componenti, tempi di vita e rischio di guasto sistemico"
author: ""
date: ""
---

# 1. Obiettivi della dispensa

Questa dispensa introduce le copule come strumento per modellare la dipendenza tra i tempi di vita di componenti in un sistema tecnico, nell'ambito della teoria dell'affidabilita'.

Gli obiettivi sono sei:

1. formalizzare il problema dell'affidabilita' di sistema a partire dai tempi di vita dei componenti;
2. enunciare il teorema di Sklar e chiarire la separazione tra dipendenza e marginali;
3. introdurre le famiglie di copule piu' usate (Gaussiana, Clayton, Gumbel, Frank) e discutere le loro proprieta' di coda;
4. collegare le copule a misure di concordanza come tau di Kendall e rho di Spearman;
5. simulare sistemi serie e parallelo con componenti dipendenti e confrontare con il caso di indipendenza;
6. discutere come la struttura di dipendenza influenzi il rischio di guasto sistemico, in particolare per guasti in coda.

Dal punto di vista del corso, questo progetto introduce uno strumento concettualmente nuovo: la separazione tra la distribuzione di ogni singola variabile (il margine) e la struttura di dipendenza tra variabili (la copula). Questa separazione e' molto piu' flessibile dei modelli multivariati classici e ha applicazioni in ingegneria, ecologia, medicina e scienze ambientali.

# 2. Motivazione: quando l'indipendenza e' troppo ottimistica

## 2.1 Il problema

Un ingegnere deve valutare l'affidabilita' di un sistema composto da piu' componenti. La domanda e': qual e' la probabilita' che il sistema sia ancora funzionante dopo $t$ anni?

La risposta dipende da:

- le distribuzioni dei tempi di vita dei singoli componenti;
- la struttura logica del sistema (serie, parallelo, o combinazioni);
- la struttura di dipendenza tra i guasti dei componenti.

Quest'ultimo punto e' spesso trascurato. Si assume per semplicita' che i guasti dei componenti siano indipendenti. Ma e' un'assunzione realistica?

## 2.2 Esempi concreti di dipendenza

- **Ponte stradale.** Le travi principali sono soggette agli stessi carichi ambientali: temperatura, umidita', vibrazione da traffico. Se le condizioni ambientali sono avverse, tutti i componenti si degradano insieme. I guasti non sono indipendenti.

- **Turbina eolica.** I cuscinetti dei generatori sono soggetti agli stessi cicli di carico del vento. Un periodo di vento forte degrada tutti i cuscinetti contemporaneamente.

- **Sistema di raffreddamento nucleare.** Le pompe ridondanti operano nelle stesse condizioni di temperatura e radiazione. Un guasto di causa comune (common cause failure) puo' colpire tutte le pompe simultaneamente.

- **Rete idrica.** Le tubature di una stessa zona sono state posate nello stesso periodo con lo stesso materiale. Invecchiano insieme: un'ondata di freddo puo' fare cedere piu' tubi contemporaneamente.

- **Aereo.** I motori di un bimotore sono soggetti alle stesse condizioni di volo. Ash vulcanica, ghiaccio o bird strike possono colpire entrambi i motori nello stesso istante.

- **Componenti elettronici su scheda.** Condensatori dello stesso lotto produttivo hanno difetti correlati. Se uno cede per difetto di fabbricazione, e' piu' probabile che cedano anche gli altri.

In tutti questi casi, assumere l'indipendenza sottostima il rischio di guasto simultaneo, e quindi sovrastima l'affidabilita' del sistema. Le copule permettono di quantificare esattamente questo effetto.

## 2.3 La struttura del problema

Siano $T_1, T_2, \dots, T_n$ i tempi di vita dei componenti. Vogliamo modellare la loro distribuzione congiunta $F(t_1, \dots, t_n)$.

Il problema con i modelli multivariati classici (come la normale multivariata) e' che impongono un legame rigido tra la forma delle distribuzioni marginali e la struttura di dipendenza. Se i margini sono esponenziali o Weibull (come spesso in affidabilita'), la normale multivariata non e' applicabile direttamente.

Le copule risolvono questo problema separando i due ingredienti: si sceglie liberamente la distribuzione di ogni $T_i$ (il margine), e poi si sceglie separatamente la struttura di dipendenza (la copula).

# 3. Elementi di affidabilita'

## 3.1 Funzione di sopravvivenza

La funzione di sopravvivenza di un componente con tempo di vita $T$ e':

$$
S(t) = P(T > t) = 1 - F(t),
$$

dove $F(t)$ e' la funzione di distribuzione cumulata. $S(t)$ misura la probabilita' che il componente sia ancora funzionante al tempo $t$.

**Esempio concreto.** Un cuscinetto ha un tempo di vita distribuito secondo una Weibull con parametri di forma $k = 2$ e scala $\lambda = 5$ anni. La probabilita' che duri piu' di 3 anni e' $S(3) = e^{-(3/5)^2} \approx 0.70$: il 70% dei cuscinetti sopravvive oltre 3 anni.

## 3.2 Tasso di guasto

Il tasso di guasto (hazard rate) e':

$$
h(t) = \frac{f(t)}{S(t)},
$$

dove $f(t) = -S'(t)$ e' la densita'. Il tasso di guasto $h(t)$ e' la probabilita' condizionata di guastarsi nell'istante successivo, dato che il componente ha gia' sopravvissuto fino a $t$.

Le forme piu' comuni in ingegneria sono:

- **Esponenziale**: $h(t) = \lambda$ costante. Nessuna usura: il componente e' sempre "come nuovo". Tipico di guasti casuali (elettronica di consumo durante la vita utile).
- **Weibull con $k > 1$**: $h(t)$ crescente. Usura progressiva. Tipico di componenti meccanici, batterie, tubi.
- **Weibull con $k < 1$**: $h(t)$ decrescente. Mortalita' infantile: i componenti difettosi cedono subito, quelli che sopravvivono diventano sempre piu' affidabili.

## 3.3 Sistemi serie e parallelo

**Sistema serie.** Il sistema funziona se e solo se tutti i componenti funzionano. Il sistema cede al primo guasto. L'affidabilita' del sistema e':

$$
S_{\mathrm{serie}}(t) = P(T_1 > t, T_2 > t, \dots, T_n > t).
$$

**Esempio concreto.** Una catena di trasmissione e' un sistema serie: basta che un anello ceda perche' la catena si rompa.

**Sistema parallelo.** Il sistema funziona finche' almeno un componente funziona. Il sistema cede solo quando cede l'ultimo componente. L'affidabilita' del sistema e':

$$
S_{\mathrm{parallelo}}(t) = P(\max(T_1, \dots, T_n) > t) = 1 - P(T_1 \le t, \dots, T_n \le t).
$$

**Esempio concreto.** Un aereo bimotore e' un sistema parallelo (parzialmente): puo' volare con un solo motore. Il sistema cede solo se entrambi i motori si guastano.

Nel caso di indipendenza:

$$
S_{\mathrm{serie}}^{\perp}(t) = \prod_{i=1}^n S_i(t), \qquad
S_{\mathrm{parallelo}}^{\perp}(t) = 1 - \prod_{i=1}^n F_i(t).
$$

Con dipendenza positiva, il sistema serie e' meno affidabile di quello indipendente (i guasti tendono a co-occorrere), mentre il sistema parallelo e' parimenti meno affidabile (la ridondanza vale meno se i componenti cedono insieme).

# 4. Il teorema di Sklar

## 4.1 Enunciato

Il teorema di Sklar (1959) e' il fondamento matematico della teoria delle copule.

**Teorema.** Sia $F(x_1, \dots, x_n)$ una distribuzione congiunta con marginali $F_1(x_1), \dots, F_n(x_n)$. Allora esiste una copula $C: [0,1]^n \to [0,1]$ tale che

$$
F(x_1, \dots, x_n) = C(F_1(x_1), \dots, F_n(x_n)).
$$

Se le marginali sono continue, la copula $C$ e' unica.

Viceversa, se $C$ e' una copula e $F_1, \dots, F_n$ sono funzioni di distribuzione arbitrarie, allora $F$ definita dalla formula sopra e' una distribuzione congiunta con marginali $F_1, \dots, F_n$.

## 4.2 Interpretazione

La copula $C$ e' la distribuzione congiunta delle variabili uniformi $U_i = F_i(X_i)$. Poiche' ogni $U_i$ e' uniforme su $[0,1]$ per costruzione (probability integral transform), la copula contiene solo l'informazione sulla struttura di dipendenza, liberata dalla forma delle marginali.

In termini pratici: si sceglie la distribuzione di ogni componente (esponenziale, Weibull, lognormale, ...) e poi si sceglie separatamente la copula che descrive come i componenti si influenzano a vicenda. Le due scelte sono indipendenti.

## 4.3 Copula di indipendenza

La copula di indipendenza e':

$$
C^\perp(u_1, \dots, u_n) = u_1 \cdot u_2 \cdots u_n.
$$

Corrisponde esattamente al caso in cui i componenti si guastano indipendentemente.

## 4.4 Bounds di Frechet-Hoeffding

Nel caso bivariato ($n = 2$), ogni copula e' compresa tra due bounds:

$$
W(u,v) = \max(u + v - 1, 0) \le C(u,v) \le \min(u,v) = M(u,v).
$$

- $M(u,v) = \min(u,v)$ e' la copula di dipendenza perfetta positiva (comonotonia): $T_1$ e $T_2$ cedono esattamente nello stesso momento.
- $W(u,v) = \max(u+v-1,0)$ e' la copula di dipendenza perfetta negativa (contromonotonia): quando $T_1$ e' basso, $T_2$ e' alto, e viceversa.

**Interpretazione per l'affidabilita'.** Nel sistema serie, il caso peggiore e' la comonotonia: i due componenti cedono insieme, quindi il sistema cede allo stesso momento di ciascun componente. La copula di indipendenza e' un caso intermedio.

# 5. Famiglie di copule

## 5.1 Copula Gaussiana

La copula Gaussiana e' derivata dalla distribuzione normale multivariata. Nel caso bivariato, con correlazione $\rho \in (-1, 1)$:

$$
C_\rho^{\mathrm{Ga}}(u, v) = \Phi_\rho(\Phi^{-1}(u), \Phi^{-1}(v)),
$$

dove $\Phi_\rho$ e' la distribuzione normale bivariata con correlazione $\rho$ e $\Phi^{-1}$ e' il quantile della normale standard.

**Proprieta'.** La copula Gaussiana ha code leggere: la probabilita' di guasti simultanei estremi (entrambi i componenti cedono molto presto) e' relativamente bassa. Per $\rho = 0$ si riduce alla copula di indipendenza.

**Esempio concreto.** Componenti che condividono le stesse condizioni ambientali (temperatura, umidita') ma non hanno difetti strutturali correlati. La dipendenza e' moderata e simmetrica.

## 5.2 Copula di Clayton

La copula di Clayton e' una copula Archimedea con parametro $\theta > 0$:

$$
C_\theta^{\mathrm{Cl}}(u, v) = \left(u^{-\theta} + v^{-\theta} - 1\right)^{-1/\theta}.
$$

**Proprieta'.** Ha dipendenza di coda inferiore: la probabilita' di guasto simultaneo precoce (entrambi i componenti cedono molto prima del previsto) e' maggiore di quella implicata dalla copula Gaussiana con la stessa concordanza media. Al contrario, la dipendenza di coda superiore e' nulla: guasti simultaneamente tardivi sono quasi indipendenti.

**Esempio concreto.** Componenti soggetti a shock improvvisi che possono causare guasto precoce simultaneo: due condensatori dello stesso lotto che cedono entrambi rapidamente per difetto di fabbricazione. La coda inferiore pesante cattura esattamente questo rischio.

## 5.3 Copula di Gumbel

La copula di Gumbel e' una copula Archimedea con parametro $\theta \ge 1$:

$$
C_\theta^{\mathrm{Gu}}(u, v) = \exp\left(-\left[(-\ln u)^\theta + (-\ln v)^\theta\right]^{1/\theta}\right).
$$

**Proprieta'.** Ha dipendenza di coda superiore: la probabilita' di guasto simultaneo tardivo e' maggiore di quella implicata dalla copula Gaussiana. La dipendenza di coda inferiore e' nulla.

**Esempio concreto.** Componenti che si degradano lentamente insieme per usura progressiva: due cuscinetti che durano entrambi a lungo (o cedono entrambi tardi per usura). La coda superiore pesante cattura la tendenza a sopravvivere insieme o cedere insieme per usura.

## 5.4 Copula di Frank

La copula di Frank e' una copula Archimedea con parametro $\theta \in \mathbb{R} \setminus \{0\}$:

$$
C_\theta^{\mathrm{Fr}}(u, v) = -\frac{1}{\theta} \ln\left(1 + \frac{(e^{-\theta u}-1)(e^{-\theta v}-1)}{e^{-\theta}-1}\right).
$$

**Proprieta'.** La copula di Frank e' simmetrica nelle code: ha la stessa dipendenza di coda inferiore e superiore (entrambe nulle per valori finiti di $\theta$). Al limite $\theta \to 0$ si ottiene l'indipendenza; per $\theta \to +\infty$ si ottiene la comonotonia.

**Esempio concreto.** Componenti con dipendenza moderata e simmetrica, senza asimmetria tra guasti precoci e tardivi.

## 5.5 Riepilogo delle proprieta' di coda

La scelta della copula ha conseguenze molto concrete sul rischio di guasto sistemico:

| Copula | Coda inferiore | Coda superiore | Applicazione tipica |
|---|---|---|---|
| Gaussiana | nulla | nulla | dipendenza moderata simmetrica |
| Clayton | pesante | nulla | rischio di guasto precoce simultaneo |
| Gumbel | nulla | pesante | rischio di usura simultanea tardiva |
| Frank | nulla | nulla | dipendenza simmetrica senza code |

In ingegneria dell'affidabilita', la scelta della copula non e' un dettaglio tecnico: sbagliare copula puo' sottostimare o sovrastimare il rischio sistemico di ordini di grandezza.

# 6. Misure di concordanza

## 6.1 Tau di Kendall

La tau di Kendall misura la concordanza tra due variabili: quanto spesso, prendendo due osservazioni a caso, entrambe le variabili vanno nello stesso verso.

Per una copula $C$:

$$
\tau = 4 \int\int_{[0,1]^2} C(u,v) \, dC(u,v) - 1.
$$

Per le copule Archimedee con generatore $\varphi$:

$$
\tau = 1 + 4 \int_0^1 \frac{\varphi(t)}{\varphi'(t)} \, dt.
$$

Per la copula Gaussiana: $\tau = \frac{2}{\pi} \arcsin(\rho)$.

## 6.2 Relazione con i parametri delle copule

Per le copule piu' usate, il legame tra $\tau$ e il parametro della copula e' esplicito:

- Clayton: $\tau = \theta / (\theta + 2)$, quindi $\theta = 2\tau / (1 - \tau)$;
- Gumbel: $\tau = 1 - 1/\theta$, quindi $\theta = 1/(1-\tau)$;
- Frank: relazione numerica, non in forma chiusa.

Questo e' molto utile in pratica: si stima $\tau$ dai dati e poi si calibra il parametro della copula.

## 6.3 Dipendenza di coda

Le misure di dipendenza di coda quantificano la probabilita' che entrambe le variabili siano estreme contemporaneamente.

La dipendenza di coda inferiore e':

$$
\lambda_L = \lim_{u \to 0^+} \frac{C(u,u)}{u}.
$$

La dipendenza di coda superiore e':

$$
\lambda_U = \lim_{u \to 1^-} \frac{1 - 2u + C(u,u)}{1-u}.
$$

Per le copule discusse:

- Clayton: $\lambda_L = 2^{-1/\theta}$, $\lambda_U = 0$;
- Gumbel: $\lambda_L = 0$, $\lambda_U = 2 - 2^{1/\theta}$;
- Gaussiana: $\lambda_L = \lambda_U = 0$ per ogni $\rho < 1$;
- Frank: $\lambda_L = \lambda_U = 0$.

**Interpretazione per l'affidabilita'.** $\lambda_L > 0$ significa che la probabilita' di guasto precoce simultaneo (quando $T_1$ e $T_2$ sono entrambi piccoli, cioe' $U_1 = F_1(T_1)$ e $U_2 = F_2(T_2)$ sono entrambi vicini a 0) e' proporzionale a $\lambda_L$. Per la copula di Clayton con $\theta = 2$, $\lambda_L = 2^{-1/2} \approx 0.71$: il 71% delle volte in cui un componente ha guasto molto precoce, anche l'altro cede presto.

# 7. Simulazione da copule

## 7.1 Metodo generale

Per simulare da una copula bivariata e ottenere tempi di vita $(T_1, T_2)$ con marginali $F_1$, $F_2$ e struttura di dipendenza $C$:

1. Simula $(U_1, U_2) \sim C$, una coppia di uniformi con la struttura di dipendenza voluta;
2. Applica le funzioni quantile inverse: $T_i = F_i^{-1}(U_i)$.

Il passo 2 e' sempre lo stesso. La varieta' sta nel passo 1.

## 7.2 Simulazione dalla copula Gaussiana

1. Genera $(Z_1, Z_2)$ da una normale bivariata con correlazione $\rho$: $Z_1 \sim N(0,1)$, $Z_2 = \rho Z_1 + \sqrt{1-\rho^2} Z_2'$ con $Z_2' \sim N(0,1)$ indipendente;
2. Poni $U_i = \Phi(Z_i)$.

## 7.3 Simulazione dalla copula di Clayton

Si usa il metodo della copula condizionata.

1. Genera $U_1 \sim U[0,1]$;
2. Genera $V \sim U[0,1]$ indipendente;
3. Poni:
$$
U_2 = U_1 \left(V^{-\theta/(\theta+1)} - 1 + U_1^\theta\right)^{-1/\theta}.
$$

La coppia $(U_1, U_2)$ ha distribuzione congiunta Clayton con parametro $\theta$.

## 7.4 Simulazione dalla copula di Gumbel

Per la copula di Gumbel si usa il metodo di Marshall-Olkin con variabili gamma stabili. Una procedura alternativa piu' semplice:

1. Genera $V \sim \mathrm{Stable}(1/\theta, 1, \cos(\pi/(2\theta))^{\theta}, 0)$ (variabile stabile positiva);
2. Genera $E_1, E_2 \sim \mathrm{Exp}(1)$ indipendenti;
3. Poni $U_i = \exp(-(E_i/V)^{1/\theta})$.

Per scopi didattici, e' piu' pratico usare la simulazione tramite il generatore Archimedeo, o campionare da una griglia numerica della copula.

## 7.5 Metodo di inversione condizionata (generale)

Un metodo generale per qualsiasi copula e' l'inversione della distribuzione condizionata:

1. Genera $U_1 \sim U[0,1]$;
2. Genera $V \sim U[0,1]$;
3. Risolvi $\partial C(u_1, u_2) / \partial u_1 = V$ per $u_2$, cioe' $u_2 = C_{1|2}^{-1}(v \mid u_1)$;

Questo metodo funziona sempre ma richiede l'inversione numerica della copula condizionata.

# 8. Affidabilita' di sistema con componenti dipendenti

## 8.1 Sistema serie

L'affidabilita' di un sistema serie con due componenti e' la probabilita' di sopravvivenza congiunta:

$$
S_{\mathrm{serie}}(t) = P(T_1 > t, T_2 > t) = \bar C(S_1(t), S_2(t)),
$$

dove $\bar C$ e' la copula di sopravvivenza:

$$
\bar C(u, v) = u + v - 1 + C(1-u, 1-v).
$$

Per la copula di indipendenza: $\bar C(u,v) = uv$, quindi $S_{\mathrm{serie}}^{\perp}(t) = S_1(t) S_2(t)$.

## 8.2 Sistema parallelo

L'affidabilita' di un sistema parallelo con due componenti e' la probabilita' che almeno uno sopravviva:

$$
S_{\mathrm{parallelo}}(t) = S_1(t) + S_2(t) - F(t,t) = S_1(t) + S_2(t) - C(F_1(t), F_2(t)).
$$

La presenza di $C$ mostra che la copula influenza direttamente l'affidabilita' del sistema.

## 8.3 Confronto tra copule

Per un sistema serie con due componenti Weibull identiche con parametro di scala $\lambda$ e forma $k$, la sopravvivenza del sistema a tempo $t$ e':

- **Indipendenza**: $S^{\perp}(t) = S(t)^2$;
- **Comonotonia** ($\theta \to \infty$): $S^M(t) = S(t)$ (entrambi cedono nello stesso istante, quindi il sistema dura come un singolo componente);
- **Clayton** con parametro $\theta$: valore intermedio, ma con una maggiore probabilita' di cedere molto presto rispetto all'indipendenza.

Quindi, per un sistema serie, la dipendenza positiva aumenta il rischio di guasto rispetto all'indipendenza, ma il guasto tende a concentrarsi piu' nella coda inferiore (guasto precoce) con la copula di Clayton che con la copula Gaussiana.

**Esempio numerico.** Due cuscinetti con vita media di 5 anni (Weibull $k=2$, $\lambda = 5$), con tau di Kendall $\tau = 0.5$. Probabilita' che il sistema serie ceda entro 2 anni:

- Indipendenza: $P \approx 0.148$
- Copula Gaussiana ($\rho = \sin(\pi\tau/2) \approx 0.71$): $P \approx 0.183$
- Copula di Clayton ($\theta = 2\tau/(1-\tau) = 2$): $P \approx 0.218$

La stessa concordanza media ($\tau = 0.5$) produce stime molto diverse del rischio di guasto precoce a seconda della struttura di coda della copula. Sbagliare copula significa sbagliare la stima del rischio.

# 9. Inferenza: stimare la copula dai dati

## 9.1 Metodo dei momenti tramite tau di Kendall

Il metodo piu' semplice e' il seguente.

1. Si osservano $n$ coppie di tempi di vita $(t_1^{(i)}, t_2^{(i)})$ per $i=1,\dots,n$ (dati di campo su componenti che hanno gia' ceduto o dati di test accelerato).
2. Si stima la tau di Kendall empirica:
$$
\hat\tau = \frac{C - D}{\binom{n}{2}},
$$
dove $C$ e' il numero di coppie concordanti e $D$ quello delle discordanti.
3. Si inverte la relazione $\tau(\theta)$ per ottenere $\hat\theta$.
4. Si stimano separatamente i parametri delle marginali.

## 9.2 Stima a due stadi (IFM)

Il metodo IFM (Inference Functions for Margins) procede in due passi:

1. Si stimano i parametri delle marginali $\hat\psi_1, \hat\psi_2$ per massima verosimiglianza separatamente;
2. Si trasformano i dati in pseudo-uniformi: $\hat u_i = \hat F_1(t_1^{(i)})$, $\hat v_i = \hat F_2(t_2^{(i)})$;
3. Si stima il parametro della copula massimizzando la log-verosimiglianza della copula:
$$
\hat\theta = \arg\max_\theta \sum_{i=1}^n \log c_\theta(\hat u_i, \hat v_i),
$$
dove $c_\theta$ e' la densita' della copula.

## 9.3 Dati censurati

In affidabilita', i dati sono spesso censurati: alcuni componenti non hanno ancora ceduto alla fine del periodo di osservazione. La gestione della censura richiede una modifica della verosimiglianza, ma non cambia la struttura del metodo IFM.

## 9.4 Scelta della famiglia di copule

Per scegliere tra famiglie diverse si possono usare:

- **AIC/BIC**: penalizzano la complessita' del modello;
- **Test di bonta' del modello**: confronto tra la copula empirica e quella modellata tramite distanza di Cramer-von Mises o Kolmogorov-Smirnov;
- **Analisi qualitativa della coda**: se i dati mostrano clustering estremo, si preferisce Clayton o Gumbel alla Gaussiana.

# 10. Domande scientifiche che il modello permette di studiare

Il modello e' utile per affrontare domande molto concrete.

1. Quanto cambia la probabilita' di guasto del sistema al variare della struttura di copula, a parita' di marginali e concordanza media?
2. Come influisce la dipendenza di coda inferiore sull'affidabilita' di un sistema serie rispetto alla dipendenza di coda superiore?
3. Quale copula e' piu' conservativa (produce la stima piu' pessimistica del rischio) per un sistema serie? E per un sistema parallelo?
4. Quanto e' robusto il risultato alla scelta della copula quando la concordanza e' bassa? E quando e' alta?
5. Come si propaga l'incertezza sulla scelta della copula alla stima dell'affidabilita' del sistema?
6. In un sistema serie con $n > 2$ componenti, come scala il rischio di guasto con $n$ al variare della struttura di dipendenza?

# 11. Schema del laboratorio

## 11.1 Laboratorio 1 - Visualizzazione delle copule

### Obiettivo

Visualizzare la struttura di dipendenza di diverse copule e confrontarla con l'indipendenza.

### Attivita'

1. simulare $n = 2000$ coppie $(U_1, U_2)$ da ciascuna delle copule: indipendenza, Gaussiana ($\rho = 0.7$), Clayton ($\theta = 2$), Gumbel ($\theta = 2$);
2. rappresentare i punti nel quadrato $[0,1]^2$;
3. applicare le funzioni quantile inverse di Weibull per ottenere $(T_1, T_2)$;
4. confrontare i diagrammi di dispersione.

### Domande guida

- le diverse copule producono strutture visivamente distinguibili?
- dove si concentrano i punti con Clayton rispetto a Gumbel?
- come cambia il diagramma di dispersione di $(T_1, T_2)$ al variare della copula?

### Output richiesto

- codice sorgente;
- quattro diagrammi di dispersione nel quadrato $[0,1]^2$;
- quattro diagrammi di dispersione di $(T_1, T_2)$ in scala reale;
- commento visivo sulle differenze.

## 11.2 Laboratorio 2 - Affidabilita' di sistema serie

### Obiettivo

Confrontare la funzione di affidabilita' di un sistema serie sotto diverse ipotesi di dipendenza.

### Attivita'

1. fissare due componenti con marginali Weibull ($k = 2$, $\lambda = 5$);
2. fissare la concordanza $\tau = 0.5$ per tutte le copule;
3. simulare molte coppie $(T_1, T_2)$ per ciascuna copula;
4. stimare $S_{\mathrm{serie}}(t) = P(\min(T_1, T_2) > t)$ empiricamente;
5. confrontare con il caso di indipendenza.

### Domande guida

- quale copula produce la stima piu' pessimistica del rischio di guasto precoce?
- per quali valori di $t$ le diverse copule danno risultati piu' diversi?
- come cambia il confronto per $\tau = 0.8$?

### Output richiesto

- grafico di $S_{\mathrm{serie}}(t)$ per le diverse copule e per l'indipendenza;
- tabella di $S_{\mathrm{serie}}(t)$ per $t = 1, 2, 3, 5$ anni;
- commento sulle implicazioni per la manutenzione.

## 11.3 Laboratorio 3 - Dipendenza di coda e rischio estremo

### Obiettivo

Mostrare quantitativamente l'effetto della dipendenza di coda sulla probabilita' di guasto simultaneo precoce.

### Attivita'

1. simulare $n = 10000$ coppie da copula di Clayton e copula Gaussiana con lo stesso $\tau$;
2. per varie soglie $q \in \{0.05, 0.10, 0.20\}$, stimare $P(U_1 < q, U_2 < q)$;
3. confrontare con il valore atteso sotto indipendenza ($q^2$) e con il coefficiente di coda teorico ($\lambda_L \cdot q$);
4. ripetere per copula di Gumbel con la coda superiore.

### Domande guida

- la differenza tra Clayton e Gaussiana e' rilevante per soglie piccole ($q = 0.05$)?
- la dipendenza di coda influenza piu' il sistema serie o il sistema parallelo?
- qual e' il moltiplicatore di rischio rispetto all'indipendenza per la copula di Clayton a $q = 0.05$?

### Output richiesto

- tabella di $P(U_1 < q, U_2 < q)$ per diverse copule e soglie;
- grafico del moltiplicatore di rischio in funzione di $q$;
- commento sull'importanza della scelta della copula per il rischio estremo.

## 11.4 Laboratorio 4 - Inferenza e scelta della copula

### Obiettivo

Stimare i parametri di una copula da dati simulati e confrontare diverse famiglie tramite AIC.

### Attivita'

1. simulare $n = 200$ coppie da una copula di Clayton con $\theta = 2$ e marginali Weibull;
2. stimare il parametro di ciascuna copula (Gaussiana, Clayton, Gumbel, Frank) tramite il metodo IFM;
3. calcolare la log-verosimiglianza e l'AIC per ciascuna famiglia;
4. verificare se la copula corretta viene selezionata.

### Domande guida

- l'AIC identifica correttamente la copula vera?
- i parametri stimati sono vicini a quelli veri?
- quanti dati sono necessari per distinguere Clayton da Gaussiana?

### Output richiesto

- tabella dei parametri stimati e dell'AIC per le diverse famiglie;
- diagrammi di dispersione dei dati simulati e delle copule stimate;
- commento sulla difficolta' di identificazione.

# 12. Una possibile estensione teorica

## 12.1 Copule di sopravvivenza e sistemi k-su-n

Un sistema $k$-su-$n$ funziona se almeno $k$ componenti su $n$ sono funzionanti. Il sistema serie corrisponde a $k = n$, il sistema parallelo a $k = 1$.

Per un sistema $k$-su-$n$ con componenti dipendenti, l'affidabilita' si esprime tramite la copula multivariata degli ordini statistici, che e' una funzione della copula congiunta di tutti i componenti.

## 12.2 Copule dinamiche

In molte applicazioni, la struttura di dipendenza cambia nel tempo: due componenti giovani possono essere quasi indipendenti, ma dopo anni di usura condivisa diventano altamente dipendenti. Le copule dinamiche o vincolate al tempo modellano questo fenomeno.

## 12.3 Connessione con i processi di Hawkes

Esiste una connessione interessante tra le copule e i processi di Hawkes: la dipendenza tra i tempi di guasto di componenti in un sistema puo' essere modellata sia con una copula statica (le marginali sono fisse, si sceglie la struttura di dipendenza) sia con un processo di Hawkes bivariato (il guasto di un componente eccita il rischio di guasto dell'altro). Le due impostazioni non sono equivalenti, ma sono complementari: la copula e' piu' naturale per la distribuzione dei tempi di vita marginali, il processo di Hawkes per la dinamica condizionata.

# 13. Perche' questo e' un buon case study per il corso

Questo progetto e' particolarmente adatto a un corso di metodi computazionali per modelli stocastici per almeno cinque ragioni.

Primo, introduce un concetto matematico nuovo e potente — la separazione tra marginali e struttura di dipendenza — che non e' presente in nessuno degli altri progetti del corso.

Secondo, il contesto applicativo e' molto concreto: ogni formula ha un'interpretazione immediata in termini di rischio di guasto, vita utile e costo di manutenzione.

Terzo, il confronto tra diverse copule con la stessa concordanza media mostra in modo molto diretto che la "dipendenza" non e' una quantita' scalare: due sistemi possono avere la stessa tau di Kendall ma profili di rischio molto diversi.

Quarto, il tema e' fortemente interdisciplinare: le copule appaiono in ingegneria strutturale, idraulica, ecologia (co-estinzione di specie), epidemiologia (co-infezione), scienze ambientali (rischio composto).

Quinto, la parte di inferenza e' operativa e completa: dalla stima dei parametri alla scelta della famiglia tramite AIC, tutto e' implementabile con strumenti standard.

# 14. Conclusione

Le copule permettono di costruire distribuzioni congiunte con marginali arbitrarie e struttura di dipendenza controllata. In ingegneria dell'affidabilita', questa flessibilita' e' cruciale: i tempi di vita dei componenti non sono gaussiani, e la struttura di dipendenza tra guasti non e' catturata dalla sola correlazione lineare.

Il messaggio piu' importante e' che la dipendenza di coda conta piu' della concordanza media. Due sistemi con la stessa tau di Kendall ma copule diverse possono avere probabilita' di guasto precoce simultaneo che differiscono di un fattore 3-5. Ignorare questa differenza porta a sottostimare il rischio di guasto in condizioni critiche.

Dal punto di vista metodologico, il progetto combina in modo naturale:

- teoria delle copule e teorema di Sklar;
- famiglie parametriche e loro proprieta' di coda;
- simulazione da copule con diversi metodi;
- calcolo dell'affidabilita' di sistema;
- inferenza tramite tau di Kendall e metodo IFM;
- confronto tra modelli tramite AIC.

# 15. Bibliografia minima

1. Sklar, A. (1959). Fonctions de repartition a n dimensions et leurs marges. Publications de l'Institut de Statistique de l'Universite' de Paris, 8, 229-231.
2. Nelsen, R. B. (2006). An Introduction to Copulas. Springer.
3. Joe, H. (1997). Multivariate Models and Dependence Concepts. Chapman and Hall.
4. Kurowicka, D., and Cooke, R. M. (2006). Uncertainty Analysis with High Dimensional Dependence Modelling. Wiley.
5. Meeker, W. Q., Escobar, L. A., and Pascual, F. G. (2022). Statistical Methods for Reliability Data. Wiley.

---

# Appendice A. Implementazione in Python: struttura del codice

Questa appendice propone una struttura semplice per implementare in Python le copule discusse nella dispensa e le analisi di affidabilita' associate.

L'obiettivo non e' costruire una libreria completa, ma fornire una guida leggibile che possa essere letta come pseudocodice e implementata con sforzo minimo.

Il codice e' volutamente elementare:

- poche librerie;
- funzioni corte;
- passaggi espliciti;
- nomi leggibili.

## A.1 Librerie minime

```python
import random
import math
import statistics
import matplotlib.pyplot as plt
```

Per la stima di massima verosimiglianza si usa `scipy.optimize.minimize` e per la funzione di distribuzione normale `scipy.stats.norm`. Entrambe sono parte della distribuzione standard di SciPy.

```python
from scipy.optimize import minimize
from scipy.stats import norm, kendalltau
```

## A.2 Funzioni di base per le distribuzioni marginali

### Weibull

```python
def weibull_cdf(t, k, lam):
    if t <= 0.0:
        return 0.0
    return 1.0 - math.exp(-(t / lam) ** k)


def weibull_survival(t, k, lam):
    return 1.0 - weibull_cdf(t, k, lam)


def weibull_quantile(u, k, lam):
    if u <= 0.0:
        return 0.0
    if u >= 1.0:
        return float("inf")
    return lam * (-math.log(1.0 - u)) ** (1.0 / k)
```

### Esponenziale (caso speciale Weibull con k=1)

```python
def exponential_quantile(u, lam):
    return weibull_quantile(u, k=1.0, lam=lam)
```

## A.3 Simulazione dalla copula di indipendenza

```python
def sample_independence_copula(n):
    samples = []
    for _ in range(n):
        u1 = random.random()
        u2 = random.random()
        samples.append((u1, u2))
    return samples
```

## A.4 Simulazione dalla copula Gaussiana

```python
def sample_gaussian_copula(n, rho):
    samples = []

    for _ in range(n):
        z1 = random.gauss(0.0, 1.0)
        z2 = rho * z1 + math.sqrt(1.0 - rho ** 2) * random.gauss(0.0, 1.0)

        u1 = norm.cdf(z1)
        u2 = norm.cdf(z2)

        samples.append((u1, u2))

    return samples
```

## A.5 Simulazione dalla copula di Clayton

```python
def sample_clayton_copula(n, theta):
    samples = []

    for _ in range(n):
        u1 = random.random()
        v = random.random()

        # inversione della copula condizionata
        inner = v ** (-theta / (theta + 1.0)) - 1.0 + u1 ** (-theta)
        u2 = inner ** (-1.0 / theta)

        # clip numerica per sicurezza
        u2 = max(1e-10, min(1.0 - 1e-10, u2))

        samples.append((u1, u2))

    return samples
```

## A.6 Simulazione dalla copula di Gumbel

Per la copula di Gumbel si usa un approccio numerico tramite inversione della distribuzione condizionata.

```python
def gumbel_copula_cdf(u, v, theta):
    if u <= 0.0 or v <= 0.0:
        return 0.0
    if u >= 1.0:
        return v
    if v >= 1.0:
        return u
    a = (-math.log(u)) ** theta
    b = (-math.log(v)) ** theta
    return math.exp(-(a + b) ** (1.0 / theta))


def gumbel_conditional_cdf(u2, u1, theta):
    if u1 <= 0.0 or u1 >= 1.0:
        return u2
    a1 = (-math.log(u1)) ** theta
    a2 = (-math.log(u2)) ** theta
    s = (a1 + a2) ** (1.0 / theta)
    term = (a1 / (a1 + a2)) ** (1.0 - 1.0 / theta) / u1
    return gumbel_copula_cdf(u1, u2, theta) * term


def sample_gumbel_copula(n, theta, tol=1e-8):
    from scipy.optimize import brentq

    samples = []

    for _ in range(n):
        u1 = random.random()
        v = random.random()

        # inversione numerica della condizionata
        try:
            u2 = brentq(
                lambda x: gumbel_conditional_cdf(x, u1, theta) - v,
                1e-8, 1.0 - 1e-8,
                xtol=tol
            )
        except ValueError:
            u2 = 0.5

        samples.append((u1, u2))

    return samples
```

## A.7 Simulazione dalla copula di Frank

```python
def sample_frank_copula(n, theta):
    samples = []

    for _ in range(n):
        u1 = random.random()
        v = random.random()

        # inversione della condizionata di Frank
        # C(u2|u1) = v
        # formula esplicita per Frank
        e_theta = math.exp(-theta)
        e_theta_u1 = math.exp(-theta * u1)

        denom = 1.0 - e_theta - (e_theta_u1 - e_theta) * (1.0 - v)
        if abs(denom) < 1e-12:
            u2 = 0.5
        else:
            inner = (e_theta_u1 - e_theta) * v / denom
            if inner <= 0.0 or inner >= 1.0:
                u2 = 0.5
            else:
                u2 = -math.log(1.0 + inner) / theta

        u2 = max(1e-10, min(1.0 - 1e-10, u2))
        samples.append((u1, u2))

    return samples
```

## A.8 Conversione da uniformi a tempi di vita

```python
def uniforms_to_lifetimes(samples, k1, lam1, k2, lam2):
    lifetimes = []

    for u1, u2 in samples:
        t1 = weibull_quantile(u1, k1, lam1)
        t2 = weibull_quantile(u2, k2, lam2)
        lifetimes.append((t1, t2))

    return lifetimes
```

## A.9 Affidabilita' empirica di sistema serie e parallelo

```python
def system_series_survival(lifetimes, t):
    count = sum(1 for t1, t2 in lifetimes if min(t1, t2) > t)
    return count / len(lifetimes)


def system_parallel_survival(lifetimes, t):
    count = sum(1 for t1, t2 in lifetimes if max(t1, t2) > t)
    return count / len(lifetimes)


def survival_curve(lifetimes, t_values, system="series"):
    if system == "series":
        return [system_series_survival(lifetimes, t) for t in t_values]
    else:
        return [system_parallel_survival(lifetimes, t) for t in t_values]
```

## A.10 Confronto tra copule sull'affidabilita' di sistema

```python
def compare_copulas_series(k, lam, tau, t_values, n_samples=5000):
    # parametri delle copule dalla tau di Kendall
    rho_gauss = math.sin(math.pi * tau / 2.0)
    theta_clayton = 2.0 * tau / (1.0 - tau)
    theta_gumbel = 1.0 / (1.0 - tau)

    results = {}

    # indipendenza
    samples_ind = sample_independence_copula(n_samples)
    lt_ind = uniforms_to_lifetimes(samples_ind, k, lam, k, lam)
    results["indipendenza"] = survival_curve(lt_ind, t_values, "series")

    # gaussiana
    samples_ga = sample_gaussian_copula(n_samples, rho_gauss)
    lt_ga = uniforms_to_lifetimes(samples_ga, k, lam, k, lam)
    results["gaussiana"] = survival_curve(lt_ga, t_values, "series")

    # clayton
    samples_cl = sample_clayton_copula(n_samples, theta_clayton)
    lt_cl = uniforms_to_lifetimes(samples_cl, k, lam, k, lam)
    results["clayton"] = survival_curve(lt_cl, t_values, "series")

    # gumbel
    samples_gu = sample_gumbel_copula(n_samples, theta_gumbel)
    lt_gu = uniforms_to_lifetimes(samples_gu, k, lam, k, lam)
    results["gumbel"] = survival_curve(lt_gu, t_values, "series")

    return results


def plot_series_comparison(t_values, results):
    styles = {
        "indipendenza": ("gray", "--"),
        "gaussiana": ("steelblue", "-"),
        "clayton": ("darkorange", "-"),
        "gumbel": ("darkgreen", "-")
    }

    for name, survs in results.items():
        color, ls = styles.get(name, ("black", "-"))
        plt.plot(t_values, survs, color=color, linestyle=ls, label=name)

    plt.xlabel("tempo t")
    plt.ylabel("S_serie(t)")
    plt.title("Affidabilita' sistema serie: confronto tra copule")
    plt.legend()
    plt.show()
```

Esempio:

```python
t_values = [0.5 * k for k in range(1, 21)]
results = compare_copulas_series(k=2.0, lam=5.0, tau=0.5, t_values=t_values)
plot_series_comparison(t_values, results)
```

## A.11 Stima della tau di Kendall empirica

```python
def kendall_tau_empirical(lifetimes):
    n = len(lifetimes)
    concordant = 0
    discordant = 0

    for i in range(n):
        for j in range(i + 1, n):
            t1_i, t2_i = lifetimes[i]
            t1_j, t2_j = lifetimes[j]

            sign1 = t1_i - t1_j
            sign2 = t2_i - t2_j

            if sign1 * sign2 > 0:
                concordant += 1
            elif sign1 * sign2 < 0:
                discordant += 1

    n_pairs = n * (n - 1) // 2
    if n_pairs == 0:
        return 0.0

    return (concordant - discordant) / n_pairs
```

Nota: questa implementazione e' $O(n^2)$. Per $n$ grandi conviene usare `scipy.stats.kendalltau`.

## A.12 Log-verosimiglianza della copula di Clayton

La densita' della copula di Clayton e':

$$
c_\theta(u,v) = (1+\theta)(uv)^{-(1+\theta)}(u^{-\theta} + v^{-\theta} - 1)^{-(2+1/\theta)}.
$$

```python
def clayton_log_density(u, v, theta):
    if u <= 0.0 or v <= 0.0 or u >= 1.0 or v >= 1.0:
        return -float("inf")

    log_c = (math.log(1.0 + theta)
             - (1.0 + theta) * (math.log(u) + math.log(v))
             - (2.0 + 1.0 / theta) * math.log(u ** (-theta) + v ** (-theta) - 1.0))

    return log_c


def clayton_log_likelihood(pseudo_uniforms, theta):
    if theta <= 0.0:
        return -float("inf")

    total = 0.0
    for u, v in pseudo_uniforms:
        ld = clayton_log_density(u, v, theta)
        if math.isinf(ld):
            return -float("inf")
        total += ld

    return total
```

## A.13 Stima IFM per copula di Clayton con marginali Weibull

```python
def fit_weibull_mle(times):
    from scipy.optimize import minimize

    def neg_log_likelihood(params):
        k, lam = params
        if k <= 0.0 or lam <= 0.0:
            return float("inf")
        ll = 0.0
        for t in times:
            if t <= 0.0:
                return float("inf")
            ll += (math.log(k) - math.log(lam)
                   + (k - 1.0) * math.log(t / lam)
                   - (t / lam) ** k)
        return -ll

    result = minimize(neg_log_likelihood, x0=[2.0, statistics.mean(times)],
                      method="L-BFGS-B",
                      bounds=[(1e-4, None), (1e-4, None)])
    return result.x[0], result.x[1]


def fit_ifm_clayton(lifetimes):
    t1_data = [t1 for t1, t2 in lifetimes]
    t2_data = [t2 for t1, t2 in lifetimes]

    # passo 1: stima delle marginali
    k1_hat, lam1_hat = fit_weibull_mle(t1_data)
    k2_hat, lam2_hat = fit_weibull_mle(t2_data)

    # passo 2: pseudo-uniformi
    pseudo = []
    for t1, t2 in lifetimes:
        u1 = weibull_cdf(t1, k1_hat, lam1_hat)
        u2 = weibull_cdf(t2, k2_hat, lam2_hat)
        u1 = max(1e-8, min(1.0 - 1e-8, u1))
        u2 = max(1e-8, min(1.0 - 1e-8, u2))
        pseudo.append((u1, u2))

    # passo 3: stima del parametro Clayton
    def neg_ll_copula(params):
        theta = params[0]
        return -clayton_log_likelihood(pseudo, theta)

    result = minimize(neg_ll_copula, x0=[1.0],
                      method="L-BFGS-B",
                      bounds=[(1e-4, None)])
    theta_hat = result.x[0]

    return {
        "k1": k1_hat, "lam1": lam1_hat,
        "k2": k2_hat, "lam2": lam2_hat,
        "theta": theta_hat,
        "tau": theta_hat / (theta_hat + 2.0),
        "log_likelihood_copula": -result.fun
    }
```

## A.14 Analisi della dipendenza di coda empirica

```python
def tail_dependence_empirical(samples, q):
    count_both = sum(1 for u1, u2 in samples if u1 < q and u2 < q)
    count_u1 = sum(1 for u1, u2 in samples if u1 < q)

    if count_u1 == 0:
        return 0.0

    return count_both / count_u1


def compare_tail_dependence(n_samples=20000):
    q_values = [0.02, 0.05, 0.10, 0.20]

    tau = 0.5
    rho = math.sin(math.pi * tau / 2.0)
    theta_cl = 2.0 * tau / (1.0 - tau)

    samples_ga = sample_gaussian_copula(n_samples, rho)
    samples_cl = sample_clayton_copula(n_samples, theta_cl)
    samples_in = sample_independence_copula(n_samples)

    print(f"{'q':>6} | {'indip':>8} | {'gaussiana':>10} | {'clayton':>9} | {'teorico cl':>11}")
    print("-" * 55)

    for q in q_values:
        td_in = tail_dependence_empirical(samples_in, q)
        td_ga = tail_dependence_empirical(samples_ga, q)
        td_cl = tail_dependence_empirical(samples_cl, q)
        lambda_l_cl = 2.0 ** (-1.0 / theta_cl)

        print(f"{q:>6.2f} | {td_in:>8.4f} | {td_ga:>10.4f} | {td_cl:>9.4f} | {lambda_l_cl:>11.4f}")
```

## A.15 Organizzazione consigliata del file

Per mantenere il codice leggibile, conviene organizzarlo in questo ordine:

1. import delle librerie;
2. distribuzioni marginali:
   * `weibull_cdf`, `weibull_survival`, `weibull_quantile`
3. simulazione delle copule:
   * `sample_independence_copula`
   * `sample_gaussian_copula`
   * `sample_clayton_copula`
   * `sample_frank_copula`
   * `sample_gumbel_copula`
4. conversione e affidabilita':
   * `uniforms_to_lifetimes`
   * `system_series_survival`
   * `system_parallel_survival`
   * `survival_curve`
5. concordanza e coda:
   * `kendall_tau_empirical`
   * `tail_dependence_empirical`
6. inferenza:
   * `fit_weibull_mle`
   * `clayton_log_density`
   * `clayton_log_likelihood`
   * `fit_ifm_clayton`
7. grafici e confronti:
   * `compare_copulas_series`
   * `plot_series_comparison`
   * `compare_tail_dependence`
8. blocco finale con esempi.

Per esempio:

```python
if __name__ == "__main__":
    k, lam = 2.0, 5.0
    tau = 0.5
    t_values = [0.5 * i for i in range(1, 21)]

    print("=== Confronto affidabilita' sistema serie ===")
    results = compare_copulas_series(k=k, lam=lam, tau=tau,
                                     t_values=t_values, n_samples=5000)
    plot_series_comparison(t_values, results)

    print("\n=== Dipendenza di coda ===")
    compare_tail_dependence(n_samples=20000)

    print("\n=== Inferenza IFM ===")
    theta_true = 2.0
    samples_cl = sample_clayton_copula(500, theta_true)
    lifetimes = uniforms_to_lifetimes(samples_cl, k, lam, k, lam)
    fit = fit_ifm_clayton(lifetimes)
    print(f"theta vero:   {theta_true}")
    print(f"theta stimato: {fit['theta']:.4f}")
    print(f"tau stimata:   {fit['tau']:.4f} (vera: {theta_true/(theta_true+2):.4f})")
```

## A.16 Perche' questa appendice e' utile

Questa appendice ha tre funzioni didattiche principali.

Primo, ogni famiglia di copule e' simulata con un metodo distinto (formula esplicita per Clayton e Frank, inversione numerica per Gumbel, trasformazione normale per la Gaussiana), rendendo visibile che non esiste un unico algoritmo universale.

Secondo, la separazione tra simulazione della copula e conversione ai tempi di vita tramite `uniforms_to_lifetimes` rende molto chiaro il meccanismo del teorema di Sklar: si costruisce prima la dipendenza, poi si applicano le marginali.

Terzo, la funzione `compare_tail_dependence` produce una tabella che mostra quantitativamente la differenza tra copule a parita' di tau di Kendall, rendendo operativo il concetto di dipendenza di coda.

## A.17 Conclusione dell'appendice

La struttura proposta e' volutamente semplice. Chi conosce Python puo' implementarla quasi direttamente; chi usa altri linguaggi puo' leggerla come pseudocodice molto vicino a una traduzione operativa.

Il messaggio metodologico centrale e' che le copule non sono uno strumento astratto: permettono di rispondere a domande concrete come "quanto e' piu' rischioso un sistema con copula di Clayton rispetto all'indipendenza, per guasti precoci?" — e la risposta emerge direttamente dalla simulazione in poche righe di codice.
