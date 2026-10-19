#!/usr/bin/env python3
"""Window slopes of the burn/coast ratchet from the probe lines of my patched nladder.
Usage: slopes.py <log> [window edges in ks...]  (default windows: 0-15,15-40,40-60,60-100,100-200,200-400,400-end)"""
import sys, re

rows = []
for line in open(sys.argv[1]):
    m = re.match(r"probe: f=(\d+) gs=(\d+) rss_mb=([\d.]+) hwm_mb=([\d.]+) held=(\d+) ev=(\d+)", line)
    if m:
        rows.append((int(m.group(2)), float(m.group(3)), int(m.group(5))))
assert rows, "no probe lines"
gs = [r[0] for r in rows]
edges = [float(x) * 1000 for x in sys.argv[2:]] or [0, 15e3, 40e3, 60e3, 100e3, 200e3, 400e3, gs[-1] + 1]
print(f"{'window gs':>22} {'dRSS MB':>9} {'slope MB/1k gs':>14} {'held i->f':>12} {'RSS/held f MB':>13}")
for a, b in zip(edges, edges[1:]):
    w = [r for r in rows if a <= r[0] < b]
    if len(w) < 2:
        continue
    drss = w[-1][1] - w[0][1]
    dgs = (w[-1][0] - w[0][0]) / 1000.0
    slope = drss / dgs if dgs > 0 else 0.0
    print(f"{w[0][0]:>10.0f}-{w[-1][0]:<11.0f} {drss:>9.1f} {slope:>14.2f} {w[0][2]:>5}->{w[-1][2]:<6} {w[-1][1]/max(w[-1][2],1):>13.2f}")
# the specific frozen kill criteria: final-40% slope, plateau check at 60k, and the 4-GiB breach arithmetic
tot = gs[-1]
f40 = [r for r in rows if r[0] >= 0.6 * tot]
drss = f40[-1][1] - f40[0][1]
dgs = (f40[-1][0] - f40[0][0]) / 1000.0
s40 = drss / dgs
r60 = min(rows, key=lambda r: abs(r[0] - 60e3))
print(f"\nfinal-40% window: gs {f40[0][0]:.0f}-{f40[-1][0]:.0f}, slope {s40:.2f} MB/1k gs")
print(f"RSS@60k = {r60[1]:.1f} MB; held@60k = {r60[2]}")
if s40 >= 0.5:
    print(f"4-GiB breach at ~{(4096 - f40[-1][1]) / s40:.0f}k game-s past the end => ~{(f40[-1][0] + (4096 - f40[-1][1]) / s40 * 1000) / 1000:.0f}k game-s total = {(f40[-1][0] + (4096 - f40[-1][1]) / s40 * 1000) / 100 / 60:.0f} wall-min at rtf 100")
else:
    print(f"4-GiB breach at ~{(4096 - f40[-1][1]) / s40:.0f}k game-s past the end => ~{(f40[-1][0] + (4096 - f40[-1][1]) / s40 * 1000) / 1000:.0f}k game-s total = {(f40[-1][0] + (4096 - f40[-1][1]) / s40 * 1000) / 100 / 60:.0f} wall-min at rtf 100")
