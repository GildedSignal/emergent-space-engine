#!/usr/bin/env python3
"""Tail analysis of the encounter stream (run 20261009-0819-taleb-1a92).
Belt parameters are regenerated exactly (port of crates/encounters/src/belt.rs RNG + kepler::Body).
"""
import json, math, sys, random

TAU = 2 * math.pi
M64 = (1 << 64) - 1

class Rng:
    def __init__(self, s): self.s = s & M64
    def next_u64(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M64
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
        return z ^ (z >> 31)
    def f64(self): return (self.next_u64() >> 11) / 9007199254740992.0

def make_belt(n, sigma_e, rho, a_lo, a_hi, seed):
    rng = Rng(seed)
    out = []
    for _ in range(n):
        a = a_lo + (a_hi - a_lo) * rng.f64()
        u = rng.f64()
        e = min(sigma_e * math.sqrt(-2.0 * math.log(1.0 - u)), 0.5)
        pom = TAU * rng.f64()
        lam = TAU * rng.f64()
        out.append((a, e, pom, lam))
    return out

def body_n(a0):
    period = round(TAU * a0 ** 1.5 * 4294967296.0)
    return TAU * 4294967296.0 / period

def gini(xs):
    xs = sorted(xs); n = len(xs); s = 0.0
    for i, x in enumerate(xs): s += (2 * (i + 1) - n - 1) * x
    tot = sum(xs)
    return (s / (n * tot)) if tot > 0 else 0.0

def pct(xs, p):
    if not xs: return 0
    xs = sorted(xs); k = (len(xs) - 1) * p; f = int(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)

def spearman(a, b):
    n = len(a)
    ra = {v: i for i, v in enumerate(sorted(range(n), key=lambda i: a[i]))}
    rb = {v: i for i, v in enumerate(sorted(range(n), key=lambda i: b[i]))}
    d2 = sum((ra[i] - rb[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))

def analyze(tag, n, sigma_e, rho, a_lo, a_hi, orbits, seed, csv, intruder=False):
    belt = make_belt(n, sigma_e, rho, a_lo, a_hi, seed)
    if intruder:
        belt[n - 1] = ((a_lo + a_hi) / 2, 0.9, 0.0, 0.0)
    ev = []
    with open(csv) as f:
        for line in f:
            i, j, t, d = line.split(",")
            ev.append((int(i), int(j), float(t), float(d)))
    T = orbits * TAU
    lam = len(ev) / (n * orbits)
    # per-body counts
    cnt = [0] * n
    for i, j, t, d in ev:
        cnt[i] += 1; cnt[j] += 1
    nz = [c for c in cnt if c > 0]
    top1 = sum(sorted(cnt)[-max(1, n // 100):]) / max(1, len(ev))
    # time bins (1 orbit and 0.1 orbit)
    def bins(w_orbits):
        nb = int(orbits / w_orbits)
        b = [0] * nb
        for i, j, t, d in ev:
            b[min(nb - 1, int(t / (w_orbits * TAU)))] += 1
        return b
    b1 = bins(1.0)
    m1 = sum(b1) / len(b1)
    fano1 = (sum((x - m1) ** 2 for x in b1) / len(b1) / m1) if m1 > 0 else 0.0
    med1 = pct([x for x in b1 if x > 0] or [0], 0.5)  # median over nonzero bins
    # Poisson control for max/median over nonzero bins
    rng = random.Random(20261009)
    def poisson(lam_):
        L = math.exp(-lam_); k = 0; p = 1.0
        while True:
            p *= rng.random()
            if p <= L: return k
            k += 1
    ctrl = []
    for _ in range(5000):
        s = [poisson(m1) for _ in range(len(b1))]
        nzp = [x for x in s if x > 0]
        if nzp and med1 > 0:
            ctrl.append(max(s) / pct(nzp, 0.5))
    ctrl_p95 = pct(ctrl, 0.95) if ctrl else float('nan')
    # trains: same-pair returns within 1.5 synodic periods
    bypair = {}
    for i, j, t, d in ev:
        bypair.setdefault((i, j), []).append(t)
    returns = 0; multip = []
    for (i, j), ts in bypair.items():
        ts.sort(); multip.append(len(ts))
        ni, nj = body_n(belt[i][0]), body_n(belt[j][0])
        tsyn = TAU / abs(ni - nj) if ni != nj else float('inf')
        for a_, b_ in zip(ts, ts[1:]):
            if b_ - a_ < 1.5 * tsyn: returns += 1
    # absorption S(t) at quantum sweep
    firsts = {}
    for q in (1.0, 0.3, 0.1, 0.03):
        fs = [None] * n
        for i, j, t, d in ev:
            if d < q * rho:
                for b_ in (i, j):
                    if fs[b_] is None or t < fs[b_]: fs[b_] = t
        hit = sorted(x for x in fs if x is not None)
        half = hit[len(hit) // 2] if len(hit) >= n / 2 else None  # T50 only if majority hit
        S_end = len(hit) / n
        firsts[q] = {"S_end": round(S_end, 4), "T50_orbits": round(half / TAU, 1) if half else None,
                     "T_first_orbits": round(hit[0] / TAU, 3) if hit else None}
    ecorr = spearman(cnt, [b[1] for b in belt])
    out = {
        "tag": tag, "n": n, "orbits": orbits, "events": len(ev), "lambda_per_body_orbit": round(lam, 6),
        "bodies_hit": len(nz), "frac_hit": round(len(nz) / n, 4),
        "per_body": {"median": pct(cnt, 0.5), "mean": round(len(ev) * 2 / n, 3), "p90": pct(cnt, 0.9),
                     "p99": pct(cnt, 0.99), "max": max(cnt), "gini": round(gini(cnt), 3),
                     "top1pct_share": round(top1, 4), "max_over_median": round(max(cnt) / max(1, pct(cnt, 0.5)), 1),
                     "spearman_count_vs_e": round(ecorr, 3)},
        "time_bins_1orbit": {"fano": round(fano1, 2), "max": max(b1), "median_nonzero": med1,
                             "max_over_median_nonzero": round(max(b1) / max(1, med1), 1),
                             "poisson_ctrl_p95_max_over_median": round(ctrl_p95, 1)},
        "trains": {"pairs_with_events": len(bypair),
                   "frac_pairs_multievent": round(sum(1 for m in multip if m > 1) / len(bypair), 3) if bypair else 0,
                   "max_pair_multiplicity": max(multip) if multip else 0,
                   "frac_events_same_pair_within_1.5tsyn": round(returns / max(1, len(ev) - len(bypair)), 3)},
        "absorption": {str(q): v for q, v in firsts.items()},
    }
    if intruder:
        out["intruder_count"] = cnt[n - 1]
        out["intruder_over_next"] = round(cnt[n - 1] / max(1, sorted(cnt[:-1])[-1]), 1)
    print(json.dumps(out))

if __name__ == "__main__":
    cfg = {
        "long-s11": (300, 0.01, 1e-3, 1.0, 1.5, 1000, 11, "long-s11.csv", False),
        "long-s12": (300, 0.01, 1e-3, 1.0, 1.5, 1000, 12, "long-s12.csv", False),
        "long-s13": (300, 0.01, 1e-3, 1.0, 1.5, 1000, 13, "long-s13.csv", False),
        "ultra": (100, 0.01, 1e-3, 1.0, 1.5, 10000, 15, "ultra.csv", False),
        "dense": (3000, 0.01, 3e-4, 1.0, 1.5, 20, 14, "dense.csv", False),
        "scale300": (300, 0.01, 1e-3, 1.0, 1.5, 20, 21, "scale300.csv", False),
        "scale1000": (1000, 0.01, 1e-3, 1.0, 1.5, 20, 22, "scale1000.csv", False),
        "storm": (400, 0.025, 3e-3, 1.0, 1.0025, 20, 8, "storm.csv", False),
        "intruder": (300, 0.01, 1e-3, 1.0, 1.5, 50, 9, "intruder.csv", True),
    }
    for tag in sys.argv[1:] or cfg:
        if tag in cfg:
            analyze(tag, *cfg[tag])
