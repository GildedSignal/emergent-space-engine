#!/usr/bin/env python3
"""Analysis for the dynamics run: growth exponents, Fano, avalanche, controls."""
import json, math, glob, sys

def load(p):
    d = json.load(open(p))
    return d['rows'], d['stats']

def fit_slope(pairs, lo=None):
    """pairs: list of (x, y); OLS slope of log y on log x, x>lo."""
    pts = [(math.log(a), math.log(b)) for (a, b) in pairs
           if a > 0 and b > 0 and (lo is None or a >= lo)]
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    return (n * sxy - sx * sy) / den if den else float('nan')

def incr(rows, key, skip=50):
    out = []
    for k in range(1, len(rows)):
        o = rows[k]['orbit']
        if o <= skip:
            continue
        out.append((o, rows[k][key] - rows[k - 1][key]))
    return out

def fano(pairs, lo):
    xs = [b for (a, b) in pairs if a >= lo]
    if not xs:
        return float('nan')
    m = sum(xs) / len(xs)
    v = sum((x - m) ** 2 for x in xs) / len(xs)
    return v / m if m else float('nan')

files = sorted(glob.glob('data/*.json'))
print(f"{'file':22s} {'gm':>8s} {'sigE0':>6s} {'sigE_end':>8s} {'sl_sigE':>7s} {'ovl0':>5s} {'ovl_end':>7s} {'sl_ovl':>7s} {'sl_cj':>7s} {'sl_enc':>7s} {'fano':>5s} {'drift':>8s} {'emax':>6s}")
for p in files:
    rows, st = load(p)
    sigE = [(r['orbit'], r['sigma_e']) for r in rows]
    ovl = [(r['orbit'], r['overlap']) for r in rows]
    cj = incr(rows, 'conj')
    en = incr(rows, 'enc')
for p in files:
    rows, st = load(p)
    cj2 = incr(rows, 'conj'); rs2 = incr(rows, 'resched'); en2 = incr(rows, 'enc')
    lo = rows[-1]['orbit'] * 0.5
    cj_late = sum(b for (a, b) in cj2 if a >= lo)
    rs_late = sum(b for (a, b) in rs2 if a >= lo)
    en_late = sum(b for (a, b) in en2 if a >= lo)
    c0 = cj2[0][1]
    print(f"{p:22s} resched/conj late {rs_late / max(cj_late, 1):6.1f}  (early {rs2[0][1] / max(c0, 1):5.1f})  "
          f"resched/enc late {rs_late / max(en_late, 1):8.0f}")
