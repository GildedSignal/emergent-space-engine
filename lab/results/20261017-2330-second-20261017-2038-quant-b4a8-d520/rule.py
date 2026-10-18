#!/usr/bin/env python3
"""Parse raw-train.txt into the rule table: per arm, sigma_rel (the population's step spread),
C50(g) (the wave's half-mass concentration — f82a's metric), the wave-width growth per generation,
and L (the last generation with C50 >= 2). Run: python3 rule.py < raw-train.txt"""
import re
import sys

arms = {}
for line in sys.stdin:
    m = re.match(r"ARM (\S+) g=(\d+) .*steps\[min=(\d+),p1=(\d+),p50=(\d+),p99=(\d+),max=(\d+)\]", line)
    if not m:
        continue
    name, g = m.group(1), int(m.group(2))
    p1, p50, p99 = int(m.group(4)), int(m.group(5)), int(m.group(6))
    c = re.search(r"C50=([\d.]+)x", line)
    hm = re.search(r"hm_pct_step=([\d.]+)%", line)
    mx = re.search(r"max/mu_span=([\d.]+)", line)
    bat = re.search(r"battalion=(\d+)", line)
    mm = re.search(r"m_med=([\d.]+)", line)
    arms.setdefault(name, {})[g] = dict(
        sigma_rel=(p99 - p1) / p50,
        c50=float(c.group(1)),
        hm=float(hm.group(1)),
        mx=float(mx.group(1)),
        bat=int(bat.group(1)),
        m=float(mm.group(1)),
    )

print(f"{'arm':<10} {'sigma_rel':>9} {'C50 g0':>7} {'g1':>6} {'g2':>6} {'g4':>6} {'g8':>6} {'L(C50>=2)':>9} {'slope %/gen':>11} {'bat max':>8}")
for name, gens in arms.items():
    g0 = gens.get(0)
    c = {g: gens[g]["c50"] for g in sorted(gens)}
    L = max([g for g, v in c.items() if v >= 2.0], default=-1)
    gs = sorted(g for g in gens if g >= 1)
    slope = None
    if len(gs) >= 2:
        a, b = gs[0], gs[-1]
        slope = (gens[b]["hm"] - gens[a]["hm"]) / (b - a)
    bmax = max(v["bat"] for v in gens.values())
    row = [f"{name:<10}", f"{g0['sigma_rel']*100:8.2f}%"]
    for g in (0, 1, 2, 4, 8):
        row.append(f"{c.get(g, float('nan')):6.1f}" if g in c else "     -")
    row += [f"{L:>9}", f"{slope:10.2f}%" if slope else "         -", f"{bmax:>8}"]
    print(" ".join(row))
