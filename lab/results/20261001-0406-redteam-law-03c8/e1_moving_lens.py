#!/usr/bin/env python3
"""E1: does composing the doll's STATIC deflection(b) memo (law.md, Observation)
match the lensing an observer sees when the doll moves at beta?

Truth: a uniformly moving lens is the static solution Lorentz-boosted. So the
true observed bend is the angle between the aberrated in/out photon directions.
The law's cheap path uses the rest-frame memo angle alpha directly.

c = 1. Boost along +x (head-on / trailing geometry) or +y (transverse).
"""
import numpy as np

def aberrate(n, beta, axis):
    """Direction n (2-vector, unit) in lens rest frame -> direction in observer
    frame, where the lens moves at +beta along `axis`."""
    n = np.asarray(n, float)
    g = 1.0 / np.sqrt(1.0 - beta * beta)
    if axis == "x":
        nx = (n[0] + beta) / (1.0 + beta * n[0])
        ny = n[1] / (g * (1.0 + beta * n[0]))
    else:  # boost along y: swap roles
        ny = (n[1] + beta) / (1.0 + beta * n[1])
        nx = n[0] / (g * (1.0 + beta * n[1]))
    v = np.array([nx, ny])
    return v / np.linalg.norm(v)

def bend(n_in, n_out):
    return np.arccos(np.clip(np.dot(n_in, n_out), -1, 1))

def run(alpha, beta, geometry):
    if geometry == "head-on":
        # photon moves -x in lens frame, impact parameter along y, bent by alpha
        n_in = np.array([-1.0, 0.0])
        n_out = np.array([-np.cos(alpha), np.sin(alpha)])
        axis = "x"
    else:  # transverse: photon moves +x, bend along y (boost axis)
        n_in = np.array([1.0, 0.0])
        n_out = np.array([np.cos(alpha), -np.sin(alpha)])
        axis = "y"
    t_in = aberrate(n_in, beta, axis)
    t_out = aberrate(n_out, beta, axis)
    return bend(t_in, t_out)

print(f"{'beta':>5} {'alpha':>10} {'geometry':>10} {'memo bend':>12} {'true bend':>12} {'rel err':>9}")
for beta in (0.1, 0.5, 0.9):
    for alpha in (1.0e-2, 1.0e-4):
        for geom in ("head-on", "transverse"):
            true = run(alpha, beta, geom)
            rel = (true - alpha) / alpha
            print(f"{beta:5.2f} {alpha:10.1e} {geom:>10} {alpha:12.3e} {true:12.3e} {rel:8.1%}")

# sanity: beta=0 must give exactly alpha
for geom in ("head-on", "transverse"):
    err = abs(run(1e-3, 0.0, geom) - 1e-3)
    assert err < 1e-13, (geom, err)

# leading-order scalings to compare against (alpha-independent relative error):
print("\nleading-order predictions: head-on rel err ~ gamma*(1+beta)-1, transverse ~ (1-beta^2)-1")
for beta in (0.1, 0.5, 0.9):
    g = 1 / np.sqrt(1 - beta**2)
    print(f"beta={beta}: head-on {g*(1+beta)-1:8.1%}  transverse {(1-beta**2)-1:8.1%}")
