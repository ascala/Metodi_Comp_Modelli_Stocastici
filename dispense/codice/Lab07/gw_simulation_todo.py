import numpy as np
from gw_core_todo import simula_traiettoria

# Nota: quando rinominate gw_core_todo.py in gw_core.py,
# aggiornate questa riga in:
#   from gw_core import simula_traiettoria


def simula_molte_traiettorie(M: int, N0: int, T: int, p: float) -> np.ndarray:
    """
    Simula M traiettorie indipendenti del processo di Galton--Watson.

    Parametri
    ---------
    M  : numero di traiettorie
    N0 : numero iniziale di individui
    T  : numero di generazioni
    p  : parametro della distribuzione di offspring

    Restituzione
    ------------
    Matrice di shape (M, T+1): ogni riga e' una traiettoria.

    TODO
    ----
    - Allocare una matrice di zeri di shape (M, T+1) con dtype int.
    - Riempire ogni riga chiamando simula_traiettoria.
    """
    raise NotImplementedError("TODO: implementare simula_molte_traiettorie")


def media_empirica(trajs: np.ndarray) -> np.ndarray:
    """
    Media empirica di N_t a ogni generazione, su tutte le traiettorie.

    Parametri
    ---------
    trajs : matrice (M, T+1) di traiettorie

    Restituzione
    ------------
    Array di float di lunghezza T+1.

    TODO
    ----
    - Restituire la media lungo l'asse 0.
    """
    raise NotImplementedError("TODO: implementare media_empirica")


def probabilita_empirica_estinzione_finale(trajs: np.ndarray) -> float:
    """
    Stima empirica della probabilita' di estinzione finale:
        P(N_T = 0) ~ (numero di traiettorie con N_T = 0) / M.

    Parametri
    ---------
    trajs : matrice (M, T+1) di traiettorie

    Restituzione
    ------------
    Float in [0, 1].

    TODO
    ----
    - Guardare l'ultima colonna di trajs.
    - Contare le righe con valore 0 e dividere per M.
    """
    raise NotImplementedError("TODO: implementare probabilita_empirica_estinzione_finale")


def estinzione_entro_t(trajs: np.ndarray) -> np.ndarray:
    """
    Frequenza empirica di traiettorie con N_t = 0, per ogni t.

    Parametri
    ---------
    trajs : matrice (M, T+1) di traiettorie

    Restituzione
    ------------
    Array di float di lunghezza T+1:
        risultato[t] = (numero di traiettorie con N_t = 0) / M.

    TODO
    ----
    - Per ogni colonna t, calcolare la frazione di righe con valore 0.
    - Suggerimento: (trajs == 0).mean(axis=0) fa tutto in una riga.
    """
    raise NotImplementedError("TODO: implementare estinzione_entro_t")


def media_condizionata_ai_sopravvissuti(trajs: np.ndarray) -> np.ndarray:
    """
    Media empirica di N_t condizionata alle traiettorie ancora vive
    alla generazione t, cioe' con N_t > 0.

    Parametri
    ---------
    trajs : matrice (M, T+1) di traiettorie

    Restituzione
    ------------
    Array di float di lunghezza T+1.
    Dove nessuna traiettoria e' sopravvissuta, restituire NaN.

    TODO
    ----
    - Per ogni colonna t, selezionare le righe con trajs[:, t] > 0.
    - Calcolarne la media; se non ce ne sono, usare np.nan.
    - Suggerimento: si puo' fare con un ciclo oppure con np.where
      e maschere booleane.
    """
    raise NotImplementedError("TODO: implementare media_condizionata_ai_sopravvissuti")
