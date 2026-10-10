#!/usr/bin/env python3
"""Clustering/branching analysis of belt encounter streams.
Usage: analyze.py <prefix> [<prefix> ...]   (reads <prefix>.events.bin, .samples.txt, .summary.txt)
Writes <prefix>.stats.json and prints a table row per prefix.

Measures, on the steady-state window (t >= burn-in, chosen from the e_mean
plateau in samples):
  - lambda: total event rate; per-body rate
  - Fano factor F(W) of counts in bins of width W (Poisson => 1)
  - burst-size tail: cluster events with inter-event gap < g* = c*mean_gap;
    compare quantiles to a Poisson null (same count, same duration, 400 sims)
  - branching proxy b: excess rate of events involving either partner (i or j)
    after an event, integrated over a window, minus baseline; also the
    other-bodies excess (spatial cascade channel), same window, as a control.
"""
import json, sys, os
import numpy as np

def load(prefix):
    a = np.fromfile(prefix + ".events.bin", dtype=np.dtype([('t','<f4'),('i','<i4'),('j','<i4')]))
    s = {}
    for line in open(prefix + ".summary.txt"):
        p = line.split()
        for k in range(0, len(p)-1, 2):
            try: s[p[k]] = float(p[k+1])
            except ValueError: s[p[k]] = p[k+1]
    samp = np.loadtxt(prefix + ".samples.txt")
    return a, s, samp
def burnin(samp):
    """First entry of e_mean into +-15% of the median of its last third."""
    em = samp[:,1]; t = samp[:,0]
    m = np.median(em[-len(em)//3:])
    if m <= 0: return t[0]
    idx = np.where(np.abs(em/m - 1.0) < 0.15)[0]
    return t[idx[0]] if len(idx) else t[0]

def fano(t, W):
    nb = int((t[-1]-t[0])/W)
    if nb < 8: return None
    c,_ = np.histogram(t, bins=nb, range=(t[0], t[0]+nb*W))
    return c.var()/c.mean()

def bursts(t, gap):
    s = np.split(t, np.where(np.diff(t) > gap)[0]+1)
    return np.array([len(x) for x in s])

def poisson_null(n, T0, T1, gap, reps=400, rng=None):
    rng = rng or np.random.default_rng(7)
    sizes = np.empty(reps)
    for r in range(reps):
        t = np.sort(rng.uniform(T0, T1, n))
        sizes[r] = np.max(bursts(t, gap)) if n else 0
    return sizes

def branching(t, i, j, N, twin=30.0):
    """Excess partner-involvement after each event vs per-body baseline."""
    n = len(t)
    bodies = {}
    for k in range(n):
        bodies.setdefault(i[k], []).append(t[k])
        bodies.setdefault(j[k], []).append(t[k])
    for b in bodies: bodies[b] = np.sort(np.array(bodies[b]))
    tot = 0
    for k in range(n):
        for b in (i[k], j[k]):
            tb = bodies[b]
            p = np.searchsorted(tb, t[k], side='right')
            q = np.searchsorted(tb, t[k] + twin, side='right')
            tot += q - p
    body_rate = 2 * n / (t[-1] - t[0]) / N
    base = 2 * body_rate * twin
    return tot / n - base, base, tot / n

def main(prefixes, twin=30.0, cstar=6.0):
    rows = []
    for p in prefixes:
        a, s, samp = load(p)
        tb = burnin(samp)
        m = (a['t'] >= tb)
        t = a['t'][m].astype(np.float64); i = a['i'][m]; j = a['j'][m]
        N = int(s['N']); T1 = t[-1] if len(t) else 0
        res = {"prefix": os.path.basename(p), "tau": s.get("tau"), "N": N,
               "T_burn": float(tb), "T_ss": float(T1-t[0]) if len(t) else 0,
               "n_ss": int(len(t))}
        if len(t) > 500:
            res["lambda_body_orbit"] = len(t)/(T1-t[0])/N * (2*np.pi)
            Ws = [1.0, 2.0, 5.0, 10.0]
            res["fano"] = {str(W): fano(t, W) for W in Ws}
            mean_gap = (T1-t[0])/len(t)
            gap = cstar*mean_gap
            sz = bursts(t, gap)
            null = poisson_null(len(t), t[0], T1, gap)
            res["gap_star"] = float(gap)
            res["burst_mean"] = float(sz.mean())
            res["burst_p99"] = float(np.quantile(sz, 0.99))
            res["burst_max"] = int(sz.max())
            res["burst_p99_null"] = float(np.quantile(null, 0.99))
            res["burst_max_null_p50"] = float(np.median(null))
            res["burst_max_null_p99"] = float(np.quantile(null, 0.99))
            res["fano_null"] = 1.0 + 0.0  # analytic ~1; band from chi2: sqrt(2/nbins)
            b, base, obs = branching(t, i, j, N, twin)
            res["branch_partner_excess"] = float(b)
            res["branch_base"] = float(base)
            res["branch_obs"] = float(obs)
            # tail shape: CCDF at sizes
            cc = {str(q): float((sz >= q).mean()) for q in (5, 10, 20, 50, 100) if sz.max() >= q}
            res["burst_ccdf"] = cc
        rows.append(res)
        print(json.dumps(res))
    with open("stats_all.json", "a") as f:
        for r in rows: f.write(json.dumps(r) + "\n")
    return rows

if __name__ == "__main__":
    main(sys.argv[1:])
