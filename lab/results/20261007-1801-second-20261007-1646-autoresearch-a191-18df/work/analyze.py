#!/usr/bin/env python3
"""Interleaved A/B analysis: base vs scope-free opt, ratios only."""
import json, glob, os, statistics, sys

R = os.path.join(os.path.dirname(__file__), "..", "data")

def load(tag):
    with open(os.path.join(R, f"{tag}.json")) as f:
        return json.load(f)

scenes = ["tuned", "m24", "m96", "rtf60", "m200", "rtf10"]
pairs = {s: (3 if s == "tuned" else 2) for s in scenes}
print(f"{'scene':8} {'made b→o µs':>22} {'Δ%':>7} {'leaver b→o µs':>22} {'Δ%':>7}  digests(b==o) refused  samples")
rows = {}
for s in scenes:
    bm, om, bl, ol, digs, refs, samples = [], [], [], [], set(), set(), set()
    for p in range(1, pairs[s] + 1):
        b, o = load(f"{s}-b{p}"), load(f"{s}-o{p}")
        bm.append(b["kick_us"]["median"]); om.append(o["kick_us"]["median"])
        bl.append(b["kick_us_leavers"]["median"]); ol.append(o["kick_us_leavers"]["median"])
        digs.add((b["replay_digest"] == o["replay_digest"], b["digest"] == o["digest"]))
        refs.add((b["refused"], o["refused"]))
        samples.add((b["kick_us"]["samples"], o["kick_us"]["samples"]))
    mb, mo, lb, lo = statistics.median(bm), statistics.median(om), statistics.median(bl), statistics.median(ol)
    dm, dl = 100 * (mo - mb) / mb, 100 * (lo - lb) / lb
    ok = all(d[0] for d in digs) and all(0 in r for r in refs)
    rows[s] = (mb, mo, lb, lo, dm, dl)
    ss = sorted(samples)[0]
    print(f"{s:8} {mb:10.1f} → {mo:7.1f} {dm:6.1f}% {lb:10.1f} → {lo:7.1f} {dl:6.1f}%  {ok} {sorted(refs)} {ss}")

# also p99
print("\np99 (made, leaver) base→opt per scene:")
for s in scenes:
    bp = [load(f"{s}-b{p}")["kick_us"]["p99"] for p in range(1, pairs[s]+1)]
    op = [load(f"{s}-o{p}")["kick_us"]["p99"] for p in range(1, pairs[s]+1)]
    bpl = [load(f"{s}-b{p}")["kick_us_leavers"]["p99"] for p in range(1, pairs[s]+1)]
    opl = [load(f"{s}-o{p}")["kick_us_leavers"]["p99"] for p in range(1, pairs[s]+1)]
    print(f"{s:8} made {statistics.median(bp):8.1f}→{statistics.median(op):8.1f} ({100*(statistics.median(op)-statistics.median(bp))/statistics.median(bp):+.1f}%)"
          f"  leaver {statistics.median(bpl):8.1f}→{statistics.median(opl):8.1f} ({100*(statistics.median(opl)-statistics.median(bpl))/statistics.median(bpl):+.1f}%)")

print("\nsample counts per scene (base/opt):")
for s in scenes:
    b1, o1 = load(f"{s}-b1"), load(f"{s}-o1")
    print(f"{s:8} made {b1['kick_us']['samples']}/{o1['kick_us']['samples']}  leaver {b1['kick_us_leavers']['samples']}/{o1['kick_us_leavers']['samples']}"
          f"  cycle_rebinds {b1['memo']['cycle_rebinds']}/{o1['memo']['cycle_rebinds']}  exact {b1['memo']['exact_shapes']}/{o1['memo']['exact_shapes']}")
