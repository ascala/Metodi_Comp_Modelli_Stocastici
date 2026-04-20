import numpy as np
import matplotlib.pyplot as plt

# Nota: questo modulo riceve array gia' calcolati come argomenti.
# Non importa direttamente da gw_simulation o gw_generating_function.
# Chiamate le funzioni di quei moduli nello script principale,
# poi passate i risultati alle funzioni di questo file.


def plot_traiettorie(
    trajs: np.ndarray,
    media_teo: np.ndarray | None = None,
    title: str = "",
):
    """
    Disegna un fascio di traiettorie N_t in funzione di t.
    Se fornita, aggiunge la media teorica come linea tratteggiata.

    Parametri
    ---------
    trajs     : matrice (M, T+1) di traiettorie
    media_teo : array di lunghezza T+1 con i valori E[N_t] = m^t
    title     : titolo del grafico

    TODO
    ----
    - Disegnare ogni riga di trajs con plt.plot, colore chiaro e alpha bassa.
    - Se media_teo non e' None, aggiungerla come linea nera tratteggiata
      con etichetta "media teorica".
    - Aggiungere etichette agli assi, legenda e titolo.
    """
    raise NotImplementedError("TODO: implementare plot_traiettorie")


def plot_punto_fisso(
    s: np.ndarray,
    Gs: np.ndarray,
    title: str = "",
):
    """
    Disegna y = G(s) e la retta y = s su [0, 1].
    Utile per visualizzare geometricamente il punto fisso q = G(q).

    Parametri
    ---------
    s   : array di punti in [0, 1]
    Gs  : array G(s) corrispondente
    title : titolo del grafico

    TODO
    ----
    - Disegnare la curva y = Gs in funzione di s.
    - Disegnare la retta y = s come linea tratteggiata.
    - Aggiungere etichette, legenda e titolo.
    """
    raise NotImplementedError("TODO: implementare plot_punto_fisso")


def plot_convergenza_q(
    q_values: np.ndarray,
    q_ref: float | None = None,
    title: str = "",
):
    """
    Disegna la storia dell'iterazione q_{n+1} = G(q_n) in funzione di n.

    Parametri
    ---------
    q_values : array con i valori q_0, q_1, ..., q_n
    q_ref    : valore teorico di q (se noto), aggiunto come linea orizzontale
    title    : titolo del grafico

    TODO
    ----
    - Disegnare q_values in funzione dell'indice di iterazione.
    - Se q_ref non e' None, aggiungere una linea orizzontale tratteggiata.
    - Aggiungere etichette, legenda e titolo.
    """
    raise NotImplementedError("TODO: implementare plot_convergenza_q")


def plot_confronto_estinzione(
    t: np.ndarray,
    exact_vals: np.ndarray,
    empirical_vals: np.ndarray,
    title: str = "",
):
    """
    Confronta P(N_t = 0) calcolata tramite G^{circ t}(0)
    con la frequenza empirica di estinzione entro t.

    Parametri
    ---------
    t             : array degli indici temporali 0, 1, ..., T
    exact_vals    : array con i valori G^{circ t}(0)
    empirical_vals: array con le frequenze empiriche di estinzione entro t
    title         : titolo del grafico

    TODO
    ----
    - Disegnare exact_vals come linea continua (etichetta "G^t(0)").
    - Disegnare empirical_vals come linea tratteggiata o markers
      (etichetta "Monte Carlo").
    - Aggiungere etichette, legenda e titolo.
    """
    raise NotImplementedError("TODO: implementare plot_confronto_estinzione")
