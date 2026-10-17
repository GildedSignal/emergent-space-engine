#!/usr/bin/env python3
"""Parse the FLOW probe logs into the dossier's numbers. Usage: analyze.py <dir-with-flights>"""
import re, sys, os

d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "flights")

def probes(name):
    rows = []
    with open(os.path.join(d, name + ".log")) as f:
        for line in f:
            m = re.match(r"probe f=(\d+) gs=(\d+) ms60=([\d.]+) held_now=(\d+) held_max=(\d+) rss=([\d.]+)mb cat=(\d+) bpb=(\d+)", line)
            if m:
                rows.append(dict(f=int(m[1]), gs=int(m[2]), ms60=float(m[3]), held=int(m[4]),
                                 hmax=int(m[5]), rss=float(m[6]), cat=int(m[7]), bpb=int(m[8])))
    return rows

def growth(name, lo, hi):
    """(dRSS MB, dheld, dgs, MB per held scan, held per game-s) between gs>lo and gs<hi."""
    r = probes(name)
    a = next(x for x in r if x["gs"] >= lo)
    b = max((x for x in r if x["gs"] <= hi), key=lambda x: x["gs"])
    dh = b["hmax"] - a["hmax"]
    return dict(a_gs=a["gs"], b_gs=b["gs"], d_rss=b["rss"] - a["rss"], d_held=dh,
                d_gs=b["gs"] - a["gs"], per_scan=(b["rss"] - a["rss"]) / dh if dh else 0.0,
                per_gs=dh / (b["gs"] - a["gs"]) if b["gs"] > a["gs"] else 0.0,
                a_rss=a["rss"], b_rss=b["rss"], cat=b["cat"])

out = {}
for arm, lo, hi in [("A1", 100, 4800), ("A2", 100, 4800), ("B1", 450, 4800), ("B2", 450, 4800), ("C", 100, 2700), ("C1", 100, 4100)]:
    r = probes(arm)
    if not r:
        continue
    last = r[-1]
    g = growth(arm, lo, min(hi, last["gs"] - 50))
    out[arm] = dict(last_hmax=last["hmax"], last_rss=last["rss"], last_gs=last["gs"], **g)

for arm, v in out.items():
    print(f"{arm}: held_max={v['last_hmax']} rss_end={v['last_rss']:.1f}MB cat_end={v['cat']} "
          f"growth[{v['a_gs']}->{v['b_gs']}gs] dRSS={v['d_rss']:.1f}MB dHeld={v['d_held']} "
          f"= {v['per_scan']*1e3:.0f} kB/held-scan, {v['per_gs']:.4f} held/game-s")

# The two cross-instrument checks
c, c1 = out.get("C"), out.get("C1")
if c and c1:
    print(f"\nC loaded vs C1 quiet held/game-s: {c['per_gs']:.4f} vs {c1['per_gs']:.4f} (load-independent arrival)")
    pin = (c["per_scan"] + c1["per_scan"]) / 2
    print(f"pin/held-scan: loaded {c['per_scan']*1e3:.0f} kB, quiet {c1['per_scan']*1e3:.0f} kB; "
          f"per candidate at cat~1028: {pin*1e6/1028:.0f} B")
    per_cand = pin * 1e6 / 1028  # bytes per candidate per held scan
    for K in (1000, 2400, 10_000, 20_000):
        print(f"  latch bound at K={K}: 2048 x {per_cand*K/1e6:.2f} MB = {2048*per_cand*K/1e9:.2f} GB")
b2 = out.get("B2")
if b2:
    print(f"\nB2 (ladder 1e5 loaded): held_max={b2['last_hmax']}, RSS {b2['a_rss']:.1f}->{b2['b_rss']:.1f} MB "
          f"over {b2['d_gs']} gs = {(b2['b_rss']-b2['a_rss'])*1e3/b2['d_gs']:.3f} kB/game-s")
