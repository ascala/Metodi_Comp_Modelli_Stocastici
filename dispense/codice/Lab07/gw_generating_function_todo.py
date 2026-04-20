import numpy as np


def G(s, p: float):
    """
    Funzione generatrice dell'offspring per la distribuzione binaria:
        G(s) = (1-p) + p * s^2.

    Parametri
    ---------
    s : float o array numpy, valori in [0, 1]
    p : parametro della distribuzione di offspring

    Restituzione
    ------------
    Float o array della stessa forma di s.

    TODO
    ----
    - Restituire (1 - p) + p * s**2.
    """
    raise NotImplementedError("TODO: implementare G")


def q_teorico(p: float) -> float:
    """
    Probabilita' teorica di estinzione finale per la distribuzione binaria:
        q = 1          se p <= 1/2,
        q = (1-p)/p    se p >  1/2.

    Parametri
    ---------
    p : parametro della distribuzione di offspring

    Restituzione
    ------------
    Float in [0, 1].

    TODO
    ----
    - Usare un if/else (o np.where) sulla condizione p > 0.5.
    """
    raise NotImplementedError("TODO: implementare q_teorico")


def iterazione_punto_fisso(
    p: float,
    q0: float = 0.0,
    tol: float = 1e-10,
    nmax: int = 10000,
):
    """
    Calcola la probabilita' di estinzione iterando:
        q_{n+1} = G(q_n)
    a partire da q0, fino a convergenza.

    Parametri
    ---------
    p    : parametro della distribuzione di offspring
    q0   : valore iniziale (default 0)
    tol  : soglia di convergenza su |q_{n+1} - q_n|
    nmax : numero massimo di iterazioni

    Restituzione
    ------------
    (q, storia) dove:
        q      : valore convergente
        storia : array con tutti i valori q_0, q_1, ..., q_n

    TODO
    ----
    - Inizializzare una lista con q0.
    - Iterare q = G(q, p) finche' |q_nuovo - q| < tol oppure si
      raggiunge nmax iterazioni.
    - Restituire il valore finale e la storia come array numpy.
    """
    raise NotImplementedError("TODO: implementare iterazione_punto_fisso")


def estinzione_entro_generazione(T: int, p: float) -> np.ndarray:
    """
    Calcola P(N_t = 0) = G^{circ t}(0) per t = 0, 1, ..., T,
    iterando numericamente G a partire da s = 0.

    Parametri
    ---------
    T : numero massimo di generazioni
    p : parametro della distribuzione di offspring

    Restituzione
    ------------
    Array di float di lunghezza T+1:
        risultato[t] = G^{circ t}(0).

    TODO
    ----
    - Inizializzare un array di zeri di lunghezza T+1.
    - Porre risultato[0] = 0  (perche' G^{circ 0}(0) = 0 con N_0=1).
    - Iterare: s = G(s, p) e salvare ogni valore.

    Nota: G^{circ 0}(0) = F_0(0) = E[0^{N_0}] = 0^1 = 0 per N_0=1.
    """
    raise NotImplementedError("TODO: implementare estinzione_entro_generazione")
