import numpy as np


def campiona_offspring(p: float, size: int = 1) -> np.ndarray:
    """
    Campiona dalla distribuzione binaria:
        P(K=0) = 1-p
        P(K=2) = p

    Parametri
    ---------
    p    : probabilita' di avere 2 figli
    size : numero di campioni da generare

    Restituzione
    ------------
    Array di interi di lunghezza `size`, con valori in {0, 2}.

    TODO
    ----
    - Generare `size` numeri uniformi in [0, 1).
    - Restituire 2 dove U < p, altrimenti 0.
    """
    raise NotImplementedError("TODO: implementare campiona_offspring")


def simula_traiettoria(N0: int, T: int, p: float) -> np.ndarray:
    """
    Simula una traiettoria del processo di Galton--Watson
    fino alla generazione T inclusa.

    Parametri
    ---------
    N0 : numero iniziale di individui
    T  : numero di generazioni
    p  : parametro della distribuzione di offspring

    Restituzione
    ------------
    Array di interi di lunghezza T+1 con i valori N_0, N_1, ..., N_T.

    TODO
    ----
    - Inizializzare l'array N di lunghezza T+1 con dtype int.
    - Porre N[0] = N0.
    - Per ogni t in range(T):
        - se N[t] == 0, mantenere lo stato assorbente (N[t+1] = 0);
        - altrimenti campionare N[t] variabili offspring e sommarle.
    """
    raise NotImplementedError("TODO: implementare simula_traiettoria")


def media_teorica(T: int, N0: int, p: float) -> np.ndarray:
    """
    Restituisce il vettore della media teorica:
        E[N_t] = N0 * m^t,   m = 2p,   t = 0, 1, ..., T.

    Parametri
    ---------
    T  : numero di generazioni
    N0 : numero iniziale di individui
    p  : parametro della distribuzione di offspring

    Restituzione
    ------------
    Array di float di lunghezza T+1.

    TODO
    ----
    - Costruire il vettore t = np.arange(T+1).
    - Restituire N0 * (2*p)**t.
    """
    raise NotImplementedError("TODO: implementare media_teorica")
