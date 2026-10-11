#!/usr/bin/env python3
"""Summarise a traced bench run: the tail's composition, the ceiling, the scaling."""
import json, sys

def one(d, label):
    t = d['trace']; kinds = t['kinds']
    e = d['where_the_time_goes_ms']['engine']
    tot = sum(t['all_frames_cost_ms'])
    print(f"== {label}")
    print(f"  bodies={d['bodies']} lost={len(d['lost_bodies'])} bytes/body={d['bytes_per_body']}")
    print(f"  frame_ms p50={d['frame_ms']['p50']:.2f} p99={d['frame_ms']['p99']:.2f} p99.9={d['frame_ms']['p99.9']:.2f} worst={d['worst_hitch_ms']:.2f} hitches16.7={d['hitch_counts'][0]}")
    print(f"  engine_ms p50={e['p50']:.3f} p99={e['p99']:.3f} max={e['max']:.2f} share={e['share']:.3f}")
    print(f"  rtf median={d['rtf']['median']:.1f} low1%={d['rtf']['lowest_1pct']:.1f} overflow={d['rtf']['overflow_frames']}")
    print(f"  stats: {d['stats']}")
    allc = dict(zip(kinds, t['all_frames_cost_ms']))
    w5 = dict(zip(kinds, t['worst_5pct_cost_ms']))
    oc = dict(zip(kinds, t['overflow_frames_cost_ms']))
    oi = dict(zip(kinds, t['overflow_frames_items']))
    print(f"  engine cost all: { {k: round(v,1) for k,v in allc.items()} } total={tot:.1f}ms")
    share = {k: (f"{100*v/allc[k]:.0f}%" if allc[k] else "-") for k, v in w5.items()}
    print(f"  worst 5% frames: { {k: round(v,1) for k,v in w5.items()} }  (share of each kind's run total: {share})")
    print(f"  overflow frames: { {k: round(v,1) for k,v in oc.items()} } items {oi}")
    print(f"  worst frames:")
    for f in t['worst_frames'][:10]:
        it = dict(zip(kinds, f['items'])); cm = {k: round(v,2) for k, v in zip(kinds, f['cost_ms']) if v > 0}
        print(f"    f{f['frame']:<5} eng={f['engine_ms']:6.2f}ms ovf={str(f['overflow']):<5} items={it} cost={cm}")
    print()

one(json.load(open(sys.argv[1])), sys.argv[1].split('/')[-1])
