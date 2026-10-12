#!/usr/bin/env python3
"""Summarize `xtask universe --bench` JSON reports (strips cargo's status lines)."""
import json, sys

def load(p):
    lines = [l for l in open(p) if not l.lstrip().startswith(("Compiling", "Finished", "Running", "warning:"))]
    return json.loads("".join(lines))

for p in sys.argv[1:]:
    d = load(p)
    f, c, r, w = d["frame_ms"], d["frame_cpu_ms"], d["rtf"], d["where_the_time_goes_ms"]
    print(f"== {p.split('/')[-1]}  frames={d['frames']} bodies={d['bodies']} budget={d['engine_budget_ms']}ms")
    print(f"   frame_ms p50/p95/p99/p99.9 = {f['p50']:.2f}/{f['p95']:.2f}/{f['p99']:.2f}/{f['p99.9']:.2f}  worst={d['worst_hitch_ms']:.1f}@{d['worst_hitch_at_frame']}")
    print(f"   cpu p50/p99/p99.9/worst    = {c['p50']:.2f}/{c['p99']:.2f}/{c['p99.9']:.2f}/{c['worst']:.2f}  hitches/frame(16.7/33/50)={d['hitch_counts']}")
    print(f"   hitches/hr(16.7/33/50)     = {[round(float(x),2) for x in d['hitches_per_gameplay_hour'].values()] if isinstance(d['hitches_per_gameplay_hour'], dict) else d['hitches_per_gameplay_hour']}")
    print(f"   rtf med/low1%              = {r['median']:.1f}/{r['lowest_1pct']:.2f} (target {d['rtf_target']}) overflow_frames={r['overflow_frames']}")
    print(f"   engine ms p50/p99/max={w['engine']['p50']:.2f}/{w['engine']['p99']:.2f}/{w['engine']['max']:.2f} share={w['engine']['share']:.2f} | gather p50/p99/max={w['view_gather']['p50']:.2f}/{w['view_gather']['p99']:.2f}/{w['view_gather']['max']:.2f} share={w['view_gather']['share']:.2f} | json share={w['view_json']['share']:.2f} wire share={w['wire']['share']:.2f}")
    print(f"   events/s={d['events_per_second']:.0f}  cut={d['cut_tick']}  digest={d['digest'][:24]}  load_after={d['uptime_after'].split()[-3:]}")
