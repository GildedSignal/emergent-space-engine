#!/usr/bin/env python3
"""Summarize results.jsonl: medians over seeds, per (struct, N, distribution)."""
import json, statistics as st
from collections import defaultdict

rows = [json.loads(l) for l in open('results.jsonl')]
by = defaultdict(dict)
for r in rows:
    by[(r['N'], r['lo'], r['seed'])][r['struct']] = r
bad = [k for k, v in by.items() if len({r['hash'] for r in v.values()}) != 1]
print(f"hash mismatches: {len(bad)}/{len(by)}")

agg = defaultdict(list)
for r in rows:
    agg[(r['struct'], r['N'], r['lo'])].append(r)

print(f"{'dist':7}{'N':>9} | {'h4 p50':>7} {'wh p50':>7} {'x':>5} | {'h4 mean':>8} {'wh mean':>8} {'x':>5} | {'h2/h4':>5} | {'whp99/p50':>9} {'whmax/p50':>9} | {'chain max/mean':>15}")
for dist, lo in (('wide', 6), ('narrow', 10)):
    for N in (1000, 100000, 1000000, 10000000, 30000000):
        g = {s: agg[(s, N, lo)] for s in ('heap2', 'heap4', 'wheel')}
        m = {s: st.median(r['p50'] for r in g[s]) for s in g}
        p99 = {s: st.median(r['p99'] for r in g[s]) for s in g}
        mx = {s: st.median(r['max'] for r in g[s]) for s in g}
        chm = max(r['chain_max'] for r in g['wheel'])
        chc = st.median(r['chain_mean'] for r in g['wheel'])
        if N > 10000:  # ns_mean is oracle-tainted at N<=1e4
            mean = {s: st.median(r['ns_mean'] for r in g[s]) for s in g}
            mh = f"{mean['heap4']:8.1f} {mean['wheel']:8.1f} {mean['heap4']/mean['wheel']:5.1f}"
        else:
            mh = " " * 28
        print(f"{dist:7}{N:>9} | {m['heap4']:7.1f} {m['wheel']:7.1f} {m['heap4']/m['wheel']:5.1f} | {mh} | "
              f"{m['heap2']/m['heap4']:5.2f} | {p99['wheel']/m['wheel']:9.2f} {mx['wheel']/m['wheel']:9.2f} | {chm:>7.0f}/{chc:<7.1f}")
