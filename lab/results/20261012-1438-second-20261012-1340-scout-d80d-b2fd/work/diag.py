#!/usr/bin/env python3
"""Fine-cadence diagnostic: does the twin separation oscillate (reabsorbable
crossings) while its envelope grows? 24 bodies: the 2 exponential survivors,
the departed 41.85-bit boundary body, and 21 regulars spanning the bits
distribution. From birth, T = 3e4; |delta| sampled every 1/16 period in a
late window; up/down crossings at b* = 8 counted over the whole run."""
import numpy as np, json

D0 = 1e-12
CAP = np.log2(2 * np.pi / D0)
import os
HERE = os.path.dirname(os.path.abspath(__file__))

# regenerate the belt exactly as second.py does
import sys
sys.path.insert(0, HERE)
from second import belt, assign

rng = np.random.default_rng(20261012)
a, e = belt(rng)
D, C, pres = assign(a, e)
E0 = -1.0 + 2.0 * np.minimum(D, 3.0)
n_all = len(a)
psi0 = np.empty(n_all); P0 = np.empty(n_all)
inside = E0 < 1.0
psi0[inside] = rng.uniform(-1, 1, inside.sum()) * np.arccos(np.clip(-E0[inside], -1, 1))
psi0[~inside] = rng.uniform(-np.pi, np.pi, (~inside).sum())
P0 = np.sqrt(np.maximum(0.0, 2 * (E0 + np.cos(psi0)))) * np.where(rng.random(n_all) < 0.5, 1., -1.)

d3 = np.load(f"{HERE}/perbody-T3e4.npz")
bits_end = d3["bits"][-1]
ref = np.load(f"{HERE}/perbody-A005.npz")
sel = [68, 806, 23]  # exp survivors + A005's boundary body (bits 41.85)
med = np.argsort(np.abs(bits_end - np.median(bits_end)))[:21]
sel += med.tolist()
sel = np.array(sel)

A = 0.05
periods = 30000
dtfrac = 32
dt = 2 * np.pi / dtfrac
steps = periods * dtfrac
n = len(sel)
psi = np.concatenate([psi0[sel], psi0[sel]])
P = np.concatenate([P0[sel], P0[sel] + D0])
fine_t = []; fine_dd = []
cross_up = np.zeros(n); cross_dn = np.zeros(n)
t0 = 20000.0; t1 = 20040.0
tau = 0.0
for step in range(steps):
    psi += dt * P
    P += dt * (-np.sin(psi) + A * np.sin(psi - tau))
    tau += dt
    s = step + 1
    if s % 4 == 0:
        psi = np.mod(psi + np.pi, 2 * np.pi) - np.pi
    b, r, pb, pr = psi[:n], psi[n:], P[:n], P[n:]
    dd = np.hypot(np.mod(r - b + np.pi, 2 * np.pi) - np.pi, pr - pb)
    if t0 <= tau <= t1:
        fine_t.append(tau); fine_dd.append(dd.copy())
    above = np.log2(np.maximum(dd, 1e-300) / D0) >= 8.0
    if step > 0:
        cross_up += above & ~prev
        cross_dn += ~above & prev
    prev = above
fine_t = np.array(fine_t); fine_dd = np.array(fine_dd)
out = {}
for j, i in enumerate(sel):
    y = fine_dd[:, j]
    out[int(i)] = {
        "bits_end": float(bits_end[i]),
        "dd_min_bits_window": float(np.log2(y.min() / D0)),
        "dd_max_bits_window": float(np.log2(y.max() / D0)),
        "dd_span_bits_window": float(np.log2(y.max() / y.min())),
        "n_local_max_above8": int(np.sum((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:]) & (y[1:-1] > 256 * D0))),
        "up_total": int(cross_up[j]), "dn_total": int(cross_dn[j]),
    }
with open(f"{HERE}/diag-fine.json", "w") as f:
    json.dump(out, f, indent=1)
np.savez_compressed(f"{HERE}/diag-fine.npz", t=fine_t, dd=fine_dd, sel=sel)
print(json.dumps(out, indent=1))
