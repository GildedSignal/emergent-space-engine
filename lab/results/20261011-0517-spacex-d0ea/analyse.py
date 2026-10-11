#!/usr/bin/env python3
"""Summarise the belt H_live CSV: saturation vs growth, field split, the 10^9 verdict."""
import sys, csv, math
from collections import defaultdict

rows = []
for line in open(sys.argv[1] if len(sys.argv) > 1 else "belt-hlive.csv"):
    if line[:1].isdigit() and "," in line:
        rows.append(line.strip().split(","))

# resonances of a 5.2 AU planet inside 2.0-3.5 AU: (label, a)
SEP = 5.2
res = []
for j in range(1, 13):
    for k in range(1, 7):
        a = SEP * (j / (j + k)) ** (2 / 3)
        if 2.0 < a < 3.5:
            res.append((f"{j+k}:{j}", a))

def nearest_res(r):
    return min(res, key=lambda t: abs(t[1] - r))

by_g = defaultdict(list)
for r in rows:
    by_g[(r[2])].append(r)  # by r_au string

print(f"{'r_au':>7} {'res':>6} {'dres%':>6} | {'orb1':>4} {'bits_exact@1':>12} {'@20':>12} {'d/orbit':>8} | {'cell@1':>7} {'cell@20':>8} {'modal%':>7}")
cold_end, hot_end = [], []
for r_au, g in sorted(by_g.items(), key=lambda kv: float(kv[0])):
    r = float(r_au)
    label, a = nearest_res(r)
    d = abs(r - a) / a * 100
    first, last = g[0], g[-1]
    be1, be20 = float(first[12]), float(last[12])
    bc1, bc20 = float(first[13]), float(last[13])
    n = len(g) - 1
    dorbit = (be20 - be1) / n if n else 0
    modal = float(last[4]) * 100
    tag = "HOT" if (dorbit > 0.3 or be20 > 180) else "cold"
    (hot_end if tag == "HOT" else cold_end).append((r, be20, bc20))
    print(f"{r:>7.3f} {label:>6} {d:>6.2f} | {first[1]:>4} {be1:>12.1f} {be20:>12.1f} {dorbit:>8.2f} | {bc1:>7.1f} {bc20:>8.1f} {modal:>7.1f} {tag}")

n_c, n_h = len(cold_end), len(hot_end)
if cold_end:
    mc = sum(b for _, b, _ in cold_end) / n_c
    mcc = sum(b for _, _, b in cold_end) / n_c
    print(f"\ncold groups: {n_c}, mean bits_exact@end {mc:.1f}, mean bits_cell@end {mcc:.1f}")
if hot_end:
    mh = sum(b for _, b, _ in hot_end) / n_h
    mhc = sum(b for _, _, b in hot_end) / n_h
    print(f"hot groups:  {n_h}, mean bits_exact@end {mh:.1f}, mean bits_cell@end {mhc:.1f}")

# verdict: hot fraction by radius count (each group same M), bytes at 1e9
if cold_end:
    frac_hot = n_h / (n_c + n_h)
    bits_body = (1 - frac_hot) * mcc + frac_hot * 128  # hot -> full tube cap
    print(f"\nhot fraction (radius-weighted): {frac_hot:.3f}")
    print(f"bits/body at the memo-cell store: {bits_body:.1f}  -> at 1e9 bodies: {bits_body*1e9/8/1e9:.2f} GB")
    print(f"bits/body at the exact store (cold mean {mc:.0f}): {mc:.1f} -> {mc*1e9/8/1e9:.2f} GB (cold alone)")

# per-orbit growth of the time field (mean over cold groups), last vs first interval
print("\norbit, mean cold bits_p, bits_k, bits_ang, bits_tp, bits_exact, bits_cell")
snaps = sorted({(r[0], r[1]) for r in rows}, key=lambda t: float(t[1]))
for t, o in snaps:
    sel = [r for r in rows if r[0] == t and abs(float(r[2]) - nearest_res(float(r[2]))[1]) / nearest_res(float(r[2]))[1] > 0.02]
    if not sel:
        continue
    m = lambda i: sum(float(r[i]) for r in sel) / len(sel)
    print(f"{float(o):>5.1f}, {m(8):8.2f}, {m(9):8.2f}, {m(10):8.2f}, {m(11):8.2f}, {m(12):8.2f}, {m(13):8.2f}")
