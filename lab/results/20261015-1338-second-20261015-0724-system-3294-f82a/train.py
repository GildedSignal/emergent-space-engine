#!/usr/bin/env python3
"""The fire-train analysis: are the belt's fired kicks phase-locked on one grid?

Reads the census train dumps (tick, body id per fire) and reports:
- the per-body fire interval (median over bodies of the median consecutive-delta), in ticks;
- the phase histogram of fires against that interval (fires mod interval, binned coarsely);
- the concentration: the smallest window [k·I - w, k·I + w] holding >= 90% of fires;
- per-body fire counts (first wave vs later waves).

Usage: train.py <train.txt> [<out.json>]
"""
import json
import sys
from collections import Counter, defaultdict

path = sys.argv[1]
fires = []
with open(path) as f:
    for line in f:
        t, i = line.split()
        fires.append((int(t), int(i)))
fires.sort()
n = len(fires)
by_body = defaultdict(list)
for t, i in fires:
    by_body[i].append(t)

# Belt bodies fire ~once per grid interval; child-doll bodies ~13x more. Split by fire count:
# the belt on this horizon has <= 4 fires; the child doll >= 8.
belt = {i: ts for i, ts in by_body.items() if len(ts) <= 4}
child = {i: ts for i, ts in by_body.items() if len(ts) >= 8}

def intervals(bodies):
    ds = []
    for ts in bodies.values():
        ds.extend(b - a for a, b in zip(ts, ts[1:]))
    return ds

def median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else 0

ib = intervals(belt)
ic = intervals(child)
I_belt = median(ib)
I_child = median(ic)

def phase_conc(fire_ticks, I):
    """fires at multiples of I? fraction within +-w of a multiple, for the smallest w in a ladder."""
    if I <= 0:
        return {}
    out = {}
    for w in (1, 8, 64, 512, 4096):
        frac = sum(1 for t in fire_ticks if min(t % I, I - t % I) <= w) / len(fire_ticks)
        out[f"w{w}"] = round(frac, 4)
    # the coarse phase histogram
    B = 64
    hist = Counter((t % I) * B // I for t in fire_ticks)
    out["hist_top8"] = hist.most_common(8)
    out["hist_bins"] = B
    return out
def absolute_clusters(ticks, tick_s):
    """Fires in absolute time: sorted, split where the gap exceeds 2x the median gap."""
    ts = sorted(ticks)
    if len(ts) < 3:
        return []
    gaps = sorted(b - a for a, b in zip(ts, ts[1:]))
    mg = gaps[len(gaps) // 2]
    clusters = [[ts[0]]]
    for a, b in zip(ts, ts[1:]):
        if b - a > 2 * mg:
            clusters.append([b])
        else:
            clusters[-1].append(b)
    big = [c for c in clusters if len(c) > 100]
    return [
        {"n": len(c), "start_s": round(c[0] * tick_s, 1), "end_s": round(c[-1] * tick_s, 1), "span_s": round((c[-1] - c[0]) * tick_s, 1)}
        for c in big
    ]


belt_ticks = [t for ts in belt.values() for t in ts]
child_ticks = [t for ts in child.values() for t in ts]
res = {
    "file": path,
    "fires": n,
    "bodies": len(by_body),
    "belt": {
        "bodies": len(belt),
        "fires": len(belt_ticks),
        "fires_per_body": Counter(len(ts) for ts in belt.values()),
        "interval_ticks_median": I_belt,
        "interval_ticks_p10": sorted(ib)[max(0, len(ib) // 10)] if ib else 0,
        "interval_ticks_p90": sorted(ib)[min(len(ib) - 1, 9 * len(ib) // 10)] if ib else 0,
        "phase_vs_interval": phase_conc(belt_ticks, I_belt),
        "absolute_clusters": absolute_clusters(belt_ticks, 4.925490947e-6),
    },
    "child": {
        "bodies": len(child),
        "fires": len(child_ticks),
        "interval_ticks_median": I_child,
        "phase_vs_interval": phase_conc(child_ticks, I_child),
    },
    "tick_seconds": 4.925490947e-6,  # view::TICK_SECONDS
}
# the belt interval in seconds, for the composition
res["belt"]["interval_s_median"] = I_belt * res["tick_seconds"]
out = json.dumps(res, indent=1, default=dict)
print(out)
if len(sys.argv) > 2:
    with open(sys.argv[2], "w") as f:
        f.write(out)
