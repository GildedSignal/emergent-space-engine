#!/usr/bin/env python3
"""20261017-2142-taleb-8fb9: aggregate the battalion census arms into one table (dossier evidence)."""
import re, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = [
    ("ctrl", "CTRL s=0 p=0 (shipped)"),
    ("per", "PER s=27 (193 period classes)"),
    ("phase", "PHASE p=8 (256 phases)"),
    ("both384", "BOTH s=28 p=2 (~384 combos)"),
    ("both96", "BOTH s=29 p=1 (~96 combos)"),
    ("both48", "BOTH s=30 p=1 (25 periods, ~continuous phase)"),
    ("anchor100", "ANCHOR s=30 p=30 (25 periods x 4 phases, ~100 combos)"),
    ("anchor200", "ANCHOR s=30 p=29 (25 periods x 8 phases, ~200 combos)"),
    ("ctrl_s7", "CTRL seed 7"),
    ("both96_s7", "BOTH96 seed 7"),
]

def parse(path):
    out = {"w": {}}
    for line in open(path):
        for k, pat in [("head", r"comb: n=(\d+) bodies=(\d+) seed=(\d+) a_shift=(\d+) phase_shift=(\d+)"),
                       ("tot", r"frames=(\d+) events_total=(\d+) events_per_frame_mean=([\d.]+)")]:
            m = re.search(pat, line)
            if m:
                out[k] = m.groups()
        m = re.match(r"comb: w=(\d+) frames=(\d+) ev_mean=([\d.]+) ev_p99=(\d+) ev_max=(\d+) ev_sum=(\d+) ev_ge100=(\d+) ev_ge400=(\d+) ms_p50=([\d.]+) ms_p99=([\d.]+) ms_max=([\d.]+)", line)
        if m:
            g = m.groups()
            out["w"][int(g[0])] = dict(frames=int(g[1]), mean=float(g[2]), p99=int(g[3]), max=int(g[4]),
                                       sum=int(g[5]), ge100=int(g[6]), ge400=int(g[7]),
                                       ms_p50=float(g[8]), ms_p99=float(g[9]), ms_max=float(g[10]))
    return out

rows = []
for name, label in ARMS:
    p = os.path.join(HERE, "work", "arms", f"{name}.txt")
    if not os.path.exists(p):
        continue
    d = parse(p)
    steady = [d["w"][w] for w in (2, 3, 4) if w in d["w"]]
    if not steady:
        continue
    rows.append((name, label, d, steady))

print(f"{'arm':<10} {'w0 max':>7} {'steady max':>10} {'steady p99':>10} {'ge400 w1..4':>12} {'ge100 w1..4':>12} {'steady ms_max':>13} {'ev_sum w1..4':>12}")
for name, label, d, steady in rows:
    w0 = d["w"].get(0, {})
    ge400 = sum(s["ge400"] for s in steady); ge100 = sum(s["ge100"] for s in steady)
    smax = max(s["max"] for s in steady); sp99 = max(s["p99"] for s in steady)
    sms = max(s["ms_max"] for s in steady); ssum = sum(s["sum"] for s in steady)
    print(f"{name:<10} {w0.get('max', 0):>7} {smax:>10} {sp99:>10} {ge400:>12} {ge100:>12} {sms:>13.1f} {ssum:>12}")
print()
for name, label, d, steady in rows:
    print(f"--- {label}  (total events {d.get('tot', ('?','?','?'))[1]})")
    for w in sorted(d["w"]):
        s = d["w"][w]
        print(f"    w{w}: mean {s['mean']:6.2f} p99 {s['p99']:5d} max {s['max']:6d} ge100 {s['ge100']:5d} ge400 {s['ge400']:5d} ms_max {s['ms_max']:7.2f}")
