#!/usr/bin/env python3
"""Cadence ladder: kicks, per-kick cost and work per sim-time vs Config::step_log2."""
import json, os, statistics

R = os.path.join(os.path.dirname(__file__), "..", "data")

def load(name, l2, p):
    with open(os.path.join(R, f"cad-{name}-{l2}-{p}.json")) as f:
        return json.load(f)

print(f"{'scene':5} {'l2':>2} {'kicks':>6} {'cycle_rebinds':>13} {'made µs':>8} {'leaver µs':>9} {'all µs':>7} {'work(made+leaver) µs·kicks':>26}")
for name in ["m48", "m96"]:
    base = None
    for l2 in [7, 6, 5, 4]:
        ks, cr, ms, ls, als, work = [], [], [], [], [], []
        for p in (1, 2):
            d = load(name, l2, p)
            kicks = d["kick_us"]["samples"] + d["kick_us_leavers"]["samples"]
            ks.append(kicks)
            cr.append(d["memo"]["cycle_rebinds"])
            ms.append(d["kick_us"]["median"])
            ls.append(d["kick_us_leavers"]["median"])
            als.append(d["kick_us_all"]["median"])
            work.append(kicks * d["kick_us_all"]["median"])
        k, m, l, a, w = statistics.median(ks), statistics.median(ms), statistics.median(ls), statistics.median(als), statistics.median(work)
        ref = base if base else w
        rel = w / base if base else 1.0
        print(f"{name:5} {l2:2} {k:6.0f} {statistics.median(cr):13.0f} {m:8.1f} {l:9.1f} {a:7.1f} {w:15.0f}  (x{rel:.3f} vs l2=7)")
        if l2 == 7:
            base = w
    print()
