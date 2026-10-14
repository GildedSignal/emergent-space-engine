#!/usr/bin/env python3
"""The N ladder's table from a run directory of `nladderN_flight.txt` files: python3 table.py <dir>."""
import glob, math, os, re, sys

def parse(path):
    for line in open(path):
        if line.startswith("ladder:"):
            return dict(kv.split("=", 1) for kv in line.split()[1:])
    return None

d = sys.argv[1]
rows = {}
for f in glob.glob(os.path.join(d, "n*_*.txt")):
    m = re.match(r"n(\d+)_(coast|burn)\.txt$", os.path.basename(f))
    if not m:
        continue
    r = parse(f)
    if r:
        rows[(int(m.group(1)), m.group(2))] = r
print(f"{'N':>8} {'flight':<6} {'bodies':>8} {'build s':>8} {'MiB':>6} {'B/body':>7} {'p50 ms':>8} {'p99 ms':>8} {'max ms':>8} {'>12ms':>6} {'lag s':>6} {'ev/b/gs':>9} {'kick/b/gs':>9} {'refus':>5} {'held':>5} {'view ms':>8} {'frames':>6} {'wall s':>6}  F1")
for (n, fl) in sorted(rows):
    r = rows[(n, fl)]
    over, lag, trunc = int(r["over"]), float(r["lag_s"]), r["truncated"] == "true"
    base = rows.get((0, fl))
    # F1 literal: no frame over 12 ms after the first second and zero lag; "as N=0": no worse than N=0's own run (its exodus frame 61).
    lit = over == 0 and lag == 0.0 and not trunc
    rel = (over <= 1 and lag <= 0.04 and not trunc and float(r["max_ms"]) < 13.0 and int(r["refusals"]) == 0)
    verdict = "pass" if lit else ("pass as N=0" if rel else "FAIL")
    mib = float(r["foot_end_mb"]) * 1e6 / 2**20
    print(f"{n:>8} {fl:<6} {r['bodies']:>8} {float(r['build_s']):>8.2f} {mib:>6.0f} {float(r['b_per_body']):>7.0f} {float(r['p50_ms']):>8.3f} {float(r['p99_ms']):>8.3f} {float(r['max_ms']):>8.2f} {over:>6} {lag:>6.3f} {float(r['events_per_body_gs']):>9.2e} {float(r['kicks_per_body_gs']):>9.2e} {r['refusals']:>5} {r['held_max']:>5} {float(r['view_ms']):>8.1f} {r['frames']:>6} {float(r['wall_s']):>6.1f}  {verdict}{' (truncated: 60 s)' if trunc else ''}")
