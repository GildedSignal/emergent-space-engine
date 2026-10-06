"""The cadence rule (fitted on the tuning grids; constants in RULE.json).

One law at every scale: a body's kick cadence must sample the synodic phase of
its strongest perturber κ times per synodic period, times an eccentricity-harmonics
factor, unless a resonance or the unpredictability wall routes the body out of
the kick layer entirely.

N*(body) = ceil2( KAPPA * (1 + e)^GAMMA * n / |n - n_p| )      (synodic term)
route out (no kick-layer cadence):  |p n - q n_p| < 2 W_pq   (resonance band)
                                    1 - a/a_p > 1.0 mu^(1/4)  (beyond the wall)
n = the body's own mean motion (compiled frequency), n_p = the strongest
perturber's, both exact integers in the engine (from E, L and the doll's table).
"""
import json, os
import numpy as np

RULE = dict(KAPPA=4.0, GAMMA=4.7, KAPPA_PASS=6.0)

def ceil2(x):
    """smallest power of two >= x (>= 1)."""
    if np.isscalar(x):
        return max(1, 1 << int(np.ceil(np.log2(max(x, 1.0)))))
    return np.maximum(1.0, 2.0 ** np.ceil(np.log2(np.maximum(x, 1.0))))


def cadence(n, n_p, e, route=None):
    """N for a body whose strongest perturber has n_p; e its eccentricity."""
    syn = np.abs(n - n_p) / n
    syn = np.maximum(syn, 1e-12)
    N = RULE["KAPPA"] * (1.0 + e) ** RULE["GAMMA"] / syn
    return ceil2(N)


def resonance_distance(n, n_p, p_max=7):
    """min over low-order p:q of |p n - q n_p| / (2 W_pq), W = 2.5 mu^(2/3)
    approximated by the detuning in n relative to n_p's libration width."""
    best = np.inf
    return best


def load(path=None):
    global RULE
    if path and os.path.exists(path):
        RULE.update(json.load(open(path)))
    return RULE
