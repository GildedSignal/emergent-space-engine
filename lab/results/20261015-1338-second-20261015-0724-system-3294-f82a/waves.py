#!/usr/bin/env python3
"""Wave structure, baseline vs staggered genesis: does flattening the genesis phase-lock
flatten the standing fire train without touching the rate?

Per arm: the belt bodies (<= 4 fires on this horizon), the k-th fire of each body gathered
across bodies (wave k), and the central 50% / 98% span of each wave in seconds, against the
uniform expectation (0.5 / 0.98 of the interval). Plus the per-body interval median.

Usage: waves.py <base.txt> <stag.txt> [<burn_base.txt> <burn_stag.txt>]
"""
import sys
from collections import defaultdict

TICK_S = 4.925490947e-6


def load(path):
    by_body = defaultdict(list)
    with open(path) as f:
        for line in f:
            t, i = line.split()
            by_body[int(i)].append(int(t))
    for ts in by_body.values():
        ts.sort()
    return by_body


def belt_of(by_body, max_fires=4):
    return {i: ts for i, ts in by_body.items() if len(ts) <= max_fires}


def pctl(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, round((len(xs) - 1) * p))]


def waves(belt, upto=4):
    out = []
    for k in range(upto):
        ts = [ts[k] for ts in belt.values() if len(ts) > k]
        if len(ts) < 100:
            continue
        s = sorted(t * TICK_S for t in ts)
        out.append({
            "wave": k + 1,
            "n": len(ts),
            "start_s": round(s[0], 1),
            "central50_s": round(pctl(s, 0.75) - pctl(s, 0.25), 1),
            "central98_s": round(pctl(s, 0.99) - pctl(s, 0.01), 1),
        })
    return out


def interval(belt):
    ds = []
    for ts in belt.values():
        ds.extend(b - a for a, b in zip(ts, ts[1:]))
    return pctl(ds, 0.5) * TICK_S if ds else 0.0


for path in sys.argv[1:]:
    by_body = load(path)
    belt = belt_of(by_body)
    iv = interval(belt)
    ws = waves(belt)
    print(path.split("train_")[-1])
    print("  belt bodies %d, fires %d, interval median %.1f s; fires/body %s" % (
        len(belt), sum(len(t) for t in belt.values()), iv,
        {k: sum(1 for t in belt.values() if len(t) == k) for k in (1, 2, 3, 4)}))
    for w in ws:
        conc50 = round(0.5 * iv / w["central50_s"], 1) if w["central50_s"] else None
        print("  wave %(wave)d: n=%(n)d start=%(start_s)s s, central50 %(central50_s)s s, central98 %(central98_s)s s, conc50 %(conc50)sx" % {**w, "conc50": conc50})
