#!/usr/bin/env python3
"""Extract the capacity-relevant fields from a universe --bench JSON."""
import json, sys

for path in sys.argv[1:]:
    d = json.load(open(path))
    parts = d["where_the_time_goes_ms"]
    st = d["stats"]
    print(f"== {path}")
    print(f"  bodies={d['bodies']} bytes/body={d['bytes_per_body']} events/s={d['events_per_second']:.0f}")
    print(f"  frame_ms p50={d['frame_ms']['p50']:.2f} p99={d['frame_ms']['p99']:.2f} p99.9={d['frame_ms']['p99.9']:.2f}")
    print(f"  cpu worst={d['frame_cpu_ms']['worst']:.2f} overflow={d['rtf']['overflow_frames']}/{d['frames']} ({100*d['rtf']['overflow_frames']/max(1,d['frames']):.1f}%)")
    print(f"  shares engine={parts['engine']['share']:.2f} gather={parts['view_gather']['share']:.2f} json={parts['view_json']['share']:.2f} wire={parts['wire']['share']:.2f}")
    print(f"  gather p50={parts['view_gather']['p50']:.2f} p99={parts['view_gather']['p99']:.2f} max={parts['view_gather']['max']:.2f}")
    print(f"  engine p50={parts['engine']['p50']:.2f} p99={parts['engine']['p99']:.2f} max={parts['engine']['max']:.2f}")
    for k in d["engine_cost_by_kind"]:
        if k["items"]:
            print(f"  {k['kind']}: items={k['items']} us/item={k['us_per_item']:.1f} total_ms={k['total_ms']:.0f}")
    print(f"  stats: {st}")
    print(f"  digest={d.get('digest','')[:16]} cut={d.get('cut_tick')}")
