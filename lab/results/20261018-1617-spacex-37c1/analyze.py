#!/usr/bin/env python3
"""Aggregate CENSUS lines (ww dw reach) per arm: skip fraction, |w| and rho percentiles.

skip ⟺ dw ≥ 0 (the receding gate's own integer test). rho = reach/|w| in quanta/chronon.
"""
import sys, math

def pct(xs, p):
    if not xs: return float("nan")
    xs = sorted(xs); i = min(len(xs) - 1, max(0, int(round(p / 100 * (len(xs) - 1)))))
    return xs[i]

for path in sys.argv[1:]:
    n = skip = 0; ws = []; rhos = []; rhos_skip = []; reach_hist = {}
    for line in open(path):
        if not line.startswith("CENSUS"): continue
        _, ww, dw, reach = line.split()
        ww, dw, reach = int(ww), int(dw), int(reach)
        n += 1
        w = math.isqrt(ww)
        ws.append(w)
        rho = reach / w if w else float("inf")
        rhos.append(rho)
        reach_hist[reach] = reach_hist.get(reach, 0) + 1
        if dw >= 0:
            skip += 1; rhos_skip.append(rho)
    name = path.split("/")[-1]
    if n == 0:
        print(f"{name}: 0 contacts"); continue
    print(f"{name}: n={n} skip={skip} ({100*skip/n:.4f}%)  "
          f"|w| p1/p50/p99/max = {pct(ws,1)}/{pct(ws,50)}/{pct(ws,99)}/{max(ws)}  "
          f"rho p1/p50/p99/min = {pct(rhos,1):.3g}/{pct(rhos,50):.3g}/{pct(rhos,99):.3g}/{min(rhos):.3g}  "
          f"rho<1: {sum(1 for r in rhos if r < 1)} ({100*sum(1 for r in rhos if r < 1)/n:.2f}%)  "
          f"rho(skip) med = {pct(rhos_skip,50) if rhos_skip else '-'}  reach[min,max]={min(reach_hist)},{max(reach_hist)}")
