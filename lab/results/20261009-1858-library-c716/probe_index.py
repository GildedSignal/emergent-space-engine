#!/usr/bin/env python3
"""Toy screening probe: does rank-k + amortized windows make candidate work track
real encounters, where enumeration does not?  Structural truth, not physics:
a 'conjunction event' = a synodic phase crossing of two overlapping radial
envelopes; rate per pair = |dn|/(2pi).  Deterministic (seeded).
Scenes: S1 dilution (fixed region [1,1.5] AU, N grows => density grows)
        S2 formation (N bodies on one orbit: the co-orbital fleet case)."""
import numpy as np
from math import pi
from scipy.stats import poisson

rng = np.random.default_rng(20261009)

def make_belt(N, region=(1.0, 1.5), sig_e=0.02):
    a = rng.uniform(*region, N)
    e = rng.rayleigh(sig_e, N).clip(0, 3 * sig_e)
    M = rng.uniform(0, 2 * pi, N)
    return a, e, M

def make_formation(N, sig_a=1e-3, sig_e=1e-3):
    a = 1.0 + sig_a * rng.standard_normal(N)
    e = np.abs(rng.rayleigh(sig_e, N))
    M = rng.uniform(0, 2 * pi, N)
    return a, e, M

def _overflow(m, K):
    xs = np.arange(K + 1, K + 40)
    return float(((xs - K) * poisson.pmf(xs, m)).sum())

def analyse(a, e, M, label, T=20 * 2 * pi):
    N = len(a)
    q, Q = a * (1 - e), a * (1 + e)
    n = a ** -1.5
    order = np.argsort(q)
    qs, ns = q[order], n[order]
    hi = np.searchsorted(qs, Q[order], side='right') - 1   # own pos..hi overlap from below
    cA = int((hi - np.arange(N)).sum())                     # enumeration evals (pairs once)
    nonmono = int((np.diff(np.sign(np.diff(ns))) != 0).sum())
    cn = np.concatenate([[0.0], np.cumsum(ns)])
    lo = np.arange(N) + 1
    cnt = np.maximum(hi + 1 - lo, 0)
    s = cn[hi + 1] - cn[lo]
    Lam = np.abs(s - cnt * ns) / (2 * pi)      # events/time/body (n monotone in window)
    E_rate = Lam.sum() / 2                     # each pair counted once
    E = E_rate * T
    # rank-k misses in sorted-q adjacency, weighted by pair rate
    miss = 0.0; tot = 0.0
    for p in range(N):
        l, h = p + 1, hi[p] + 1
        if h <= l: continue
        r = np.abs(ns[l:h] - ns[p]) / (2 * pi)
        rk = np.arange(l, h) - p
        miss += r[rk > 4].sum(); tot += r.sum()
    miss4 = miss / max(tot, 1e-30)
    res = dict(N=N, cA=cA, E=E, workA=cA / max(E, 1e-30),
               Lam_mean=float(Lam.mean()), Lam_p99=float(np.quantile(Lam, 0.99)),
               nonmono=nonmono, miss4=miss4)
    def overflow(dt, K=4):
        mu = np.maximum(Lam, 1e-30) * dt
        keys = np.unique(mu)
        table = np.array([_overflow(m, K) for m in keys])
        missed = table[np.searchsorted(keys, mu)].sum()
        return missed, (mu > K).mean()
    for tag, dt in (('mean', 4 / max(Lam.mean(), 1e-30)),
                    ('p99', 4 / max(np.quantile(Lam, 0.99), 1e-30))):
        mo, burst = overflow(dt)
        res[f'w_{tag}'] = dict(dt=dt, miss=mo / max(E_rate, 1e-30),
                               ev_enc=(N * 4 / dt) / max(E_rate, 1e-30), burst=burst)
    print(f"[{label}] cA={cA} E={E:.1f} A w/enc={res['workA']:.1f} "
          f"rank4-miss={miss4:.2e} nonmono={nonmono} "
          f"Lam mean/p99={res['Lam_mean']:.2e}/{res['Lam_p99']:.2e}")
    for tag in ('mean', 'p99'):
        w = res[f'w_{tag}']
        print(f"    win({tag}): dt={w['dt']:.2e} missed={w['miss']:.2e} "
              f"evals/enc={w['ev_enc']:.2f} burst-frac={w['burst']:.3f}")
    return res

def formation_phase_rank(N=4096, sig_a=1e-3, sig_e=1e-3, K=4):
    a, e, M = make_formation(N, sig_a, sig_e)
    n = a ** -1.5
    dn_row = np.abs(n[:, None] - n[None, :]).sum(1) / (2 * pi)
    dt = K / np.median(dn_row)
    firing = []
    for c in range(0, N, 256):
        i = np.arange(c, min(c + 256, N))
        dM0 = (M[i, None] - M[None, :]) % (2 * pi)
        dM1 = (M[i, None] + (n[i, None] - n[None, :]) * dt) % (2 * pi)
        cross = (dM0 < dM1) | (np.abs(dM0 - dM1) > pi)   # wrapped past 0 either way
        cross &= ~np.eye(len(i), N, c, dtype=bool)
        jj, ii = np.nonzero(cross)
        firing.extend(zip(jj.tolist(), ii.tolist()))
    fp = np.array(firing)
    if len(fp) == 0:
        print("[formation] no firing pairs; widen dt"); return
    ranks = np.empty(len(fp))
    wrap = lambda d: np.abs((d + pi) % (2 * pi) - pi)
    for k, (j, i) in enumerate(fp):
        dMi = wrap(M - M[i]); dMi[i] = np.inf
        ranks[k] = (dMi < dMi[j]).sum() + 1
    print(f"[formation N={N}] dt={dt:.2e} firing={len(fp)} pairs "
          f"phase-rank med={np.median(ranks):.0f} p99={np.quantile(ranks,.99):.0f} "
          f"max={ranks.max()} frac<=4={(ranks<=4).mean():.3f} "
          f"enum evals={N*(N-1)//2}")

if __name__ == '__main__':
    import time
    t0 = time.time()
    print("== S1 dilution (fixed region, density grows) ==")
    for N in (2000, 4000, 8000, 16000):
        analyse(*make_belt(N), f"belt N={N}")
    print("== S2 formation (co-orbital fleet) ==")
    for N in (1024, 4096):
        formation_phase_rank(N)
    print(f"total {time.time()-t0:.1f}s")
