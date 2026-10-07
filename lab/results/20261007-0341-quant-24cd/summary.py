#!/usr/bin/env python3
"""Print a one-line-per-run summary from the saved run-<tag>.json files."""
import glob
import json
import sys

tags = sys.argv[1:] or sorted(glob.glob("run-*.json") and [p[4:-5] for p in glob.glob("run-*.json")])
print(f"{'tag':14s} {'members':>7s} {'rtfT':>6s} {'f_p50':>6s} {'f_p99':>6s} {'f_p99.9':>7s} {'worst':>6s} {'e_p99':>6s} {'e_max':>6s} {'v_p99':>6s} {'rtf_med':>8s} {'ovfl':>5s} {'ev/s':>9s} {'wall':>5s}")
for tag in tags:
    try:
        r = json.load(open(f"run-{tag}.json"))
    except Exception as e:
        print(f"{tag}: parse fail {e}"); continue
    f = r["frame_ms"]; e = r["where_the_time_goes_ms"]["engine"]; v = r["where_the_time_goes_ms"]["view_gather"]
    mem = tag[1:] if tag.startswith("m") else "?"
    print(f"{tag:14s} {mem:>7s} {r['rtf_target']:>6.0f} {f['p50']:>6.2f} {f['p99']:>6.2f} {f['p99.9']:>7.2f} "
          f"{r['worst_hitch_ms']:>6.1f} {e['p99']:>6.2f} {e['max']:>6.2f} {v['p99']:>6.2f} {r['rtf']['median']:>8.1f} "
          f"{r['rtf']['overflow_frames']:>5} {r['events_per_second']:>9.3g} {r['wall_seconds']:>5.2f}")
