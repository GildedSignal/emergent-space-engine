#!/usr/bin/env python3
"""Second-author instrument for run 20261012-1340-scout-d80d (silver).

Extends hlive.py (verbatim belt, resonance assignment and IC generation:
same seeds -> same bodies, indices align with perbody-A005.npz) with the two
things the checker named:

1. One long run (T = 3e4 periods) with quadratically spaced free-twin
   checkpoints -> a horizon ladder (classify the SAME bodies at T = 1e3,
   3e3, 1e4, 3e4 with the shipped gates) and a per-body rate spectrum
   (second-half slope vs each body's own log-model floor).

2. An event-based scar measure with the engine's own semantics
   (crates/shipmem/src/shelf.rs): events are sealed as exact deltas from the
   packed base; a body back at its base is reabsorbed.  Here the packed base
   is the program's prediction from quantized birth constants; a scar event
   fires when the twin's departure crosses b* bits (the correction quantum),
   and the twin is then re-anchored at d0 (reabsorbed into its base).
   Two quanta, b* = 8 and 16 bits, give the scaling signature:
   shear-class scar interval ~ 2^{b*}/c (exponential in b*), exponential-class
   interval ~ b*/(lambda ln2) (linear in b*).

Counts are split at half the run: first half fits, second half is the
held-out prediction target of analyze.py.
"""
import json, os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor

D0 = 1e-12
CAP = np.log2(2 * np.pi / D0)          # ~42.5 bits
HERE = os.path.dirname(os.path.abspath(__file__))
BSTAR = (8.0, 16.0)                    # scar thresholds, bits of departure
CPS = 64                                # checkpoints, quadratically spaced

def belt(rng, n=4096, amin=2.1, amax=3.3, esc=0.05):
    return rng.uniform(amin, amax, n), rng.rayleigh(esc, n)

def resonances(aJ=5.2):
    from math import gcd
    out = []
    for q in range(1, 8):
        for p in range(q + 1, 13):
            if gcd(p, q) != 1:
                continue
            ares = aJ * (q / p) ** (2.0 / 3.0)
            if 1.6 < ares < 3.6:
                out.append((p, q, ares))
    return out

def assign(a, e, eJ=0.048, mu=9.55e-4, cw=None):
    if cw is None:
        cw = np.sqrt(16.0 / 3.0)
    n = a ** -1.5
    nJ = 5.2 ** -1.5
    eeff = np.maximum(e, eJ)
    res = resonances()
    nres = np.array([p / q * nJ for (p, q, _) in res])
    ii = np.arange(len(a))
    Dall = np.empty((len(res), len(a)))
    Wall = np.empty_like(Dall)
    for k, (p, q, _) in enumerate(res):
        d = p - q
        W = cw * np.sqrt(mu) * eeff ** (d / 2.0)
        Wall[k] = W
        Dall[k] = np.abs(n - nres[k]) / nres[k] / W
    jbest = np.argmin(Dall, axis=0)
    D = Dall[jbest, ii]
    order = np.argsort(Dall, axis=0)
    k1, k2 = order[0], order[1]
    dn = np.abs(nres[k1] - nres[k2])
    C = (Wall[k1, ii] * nres[k1] + Wall[k2, ii] * nres[k2]) / np.maximum(dn, 1e-12)
    pres = np.array([res[j][0] for j in jbest])
    return D, C, pres

def run_chunk(arg):
    (psi0, P0, A, periods, dtfrac) = arg
    n = len(psi0)
    dt = 2 * np.pi / dtfrac
    steps = int(periods * dtfrac)
    m = len(BSTAR)
    nb = 2 + m                            # body, free twin, scar twins
    psi = np.tile(psi0, nb)
    P = np.concatenate([P0, np.tile(P0 + D0, nb - 1)])
    bits = np.zeros((CPS, n))
    counts = np.zeros((2, m, n), dtype=np.int32)   # [half, b*, body]
    # quadratic checkpoint times (dense early: ladder needs ~8 pts by T/30)
    cp_t = periods * ((np.arange(1, CPS + 1)) / CPS) ** 2
    cp_steps = np.unique(np.round(cp_t * dtfrac).astype(int))
    cp_t = cp_steps / dtfrac
    half = steps // 2
    scan = dtfrac                          # one scar scan per period
    t0c = time.perf_counter()
    j = 0
    tau = 0.0
    for step in range(steps):
        psi += dt * P
        P += dt * (-np.sin(psi) + A * np.sin(psi - tau))
        tau += dt
        s = step + 1
        if s % 4 == 0:
            psi = np.mod(psi + np.pi, 2 * np.pi) - np.pi
        if j < len(cp_steps) and s == cp_steps[j]:
            b, f, pb, pf = psi[:n], psi[n:2*n], P[:n], P[n:2*n]
            df = np.hypot(np.mod(f - b + np.pi, 2*np.pi) - np.pi, pf - pb)
            bits[j] = np.minimum(np.log2(np.maximum(df, 1e-300) / D0), CAP)
            j += 1
        if s % scan == 0:
            b, pb = psi[:n], P[:n]
            for k in range(m):
                r, pr = psi[(2+k)*n:(3+k)*n], P[(2+k)*n:(3+k)*n]
                dd = np.hypot(np.mod(r - b + np.pi, 2*np.pi) - np.pi, pr - pb)
                crossed = np.log2(np.maximum(dd, 1e-300) / D0) >= BSTAR[k]
                if crossed.any():
                    counts[1 if s > half else 0, k] += crossed
                    sc = np.where(crossed, D0 / np.maximum(dd, 1e-14), 1.0)
                    psi[(2+k)*n:(3+k)*n] = np.mod(
                        b + sc * (np.mod(r - b + np.pi, 2*np.pi) - np.pi) + np.pi,
                        2*np.pi) - np.pi
                    P[(2+k)*n:(3+k)*n] = pb + sc * (pr - pb)
    return cp_t, bits, counts

def main(periods=30000, A=0.05, tag="second", n=4096, workers=6):
    rng = np.random.default_rng(20261012)          # same sequence as hlive.py
    a, e = belt(rng, n)
    D, C, pres = assign(a, e)
    E0 = -1.0 + 2.0 * np.minimum(D, 3.0)
    psi0 = np.empty(n); P0 = np.empty(n)
    inside = E0 < 1.0
    psi0[inside] = rng.uniform(-1, 1, inside.sum()) * np.arccos(np.clip(-E0[inside], -1, 1))
    psi0[~inside] = rng.uniform(-np.pi, np.pi, (~inside).sum())
    P0 = np.sqrt(np.maximum(0.0, 2 * (E0 + np.cos(psi0)))) * np.where(rng.random(n) < 0.5, 1., -1.)
    chunks = np.array_split(np.arange(n), workers)
    args = [(psi0[idx], P0[idx], A, periods, 32) for idx in chunks]
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        outs = list(ex.map(run_chunk, args))
    wall = time.perf_counter() - t0
    cp_t = outs[0][0]
    bits = np.concatenate([o[1] for o in outs], axis=1)
    counts = np.concatenate([o[2] for o in outs], axis=2)
    # body identity check against the shipped record
    ref = np.load(f"{HERE}/perbody-A005.npz")
    same = bool(np.array_equal(ref["a"], a) and np.array_equal(ref["D"], D))
    np.savez_compressed(f"{HERE}/perbody-{tag}.npz", a=a, e=e, D=D, C=C,
                        bits=bits, cp_t=cp_t, counts=counts)
    out = {"tag": tag, "n": n, "periods": periods, "A": A, "cps": CPS,
           "bstars": BSTAR, "wall_s": round(wall, 1),
           "bodies_match_A005": same,
           "cp_t_first": cp_t[0], "cp_t_last": cp_t[-1],
           "scar_total_h1_b8": int(counts[0, 0].sum()),
           "scar_total_h2_b8": int(counts[1, 0].sum()),
           "scar_total_h1_b16": int(counts[0, 1].sum()),
           "scar_total_h2_b16": int(counts[1, 1].sum())}
    with open(f"{HERE}/summary-{tag}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    periods = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    A = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
    tag = sys.argv[3] if len(sys.argv) > 3 else "second"
    main(periods, A, tag)
