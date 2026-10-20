#!/usr/bin/env python3
"""Era-wise anatomy (full 27,900-gs period bins; immune to comb shear): totals, cost,
comb peak height, shear drift, memory baseline, held. The companion analyze.py uses
fixed +/-3.5k windows and READS A DECAY when the comb shears out: both views together
are the instrument lesson."""
import csv, sys

def rows_of(path):
    with open(path) as f:
        return [{k: float(v) for k, v in r.items()} for r in csv.DictReader(f)]

if __name__ == "__main__":
    path, bodies = sys.argv[1], int(sys.argv[2])
    rows = rows_of(path)
    P = 27900.0
    print(f"windows={len(rows)} gs_end={rows[-1]['gs']:.0f}")
    print("era   ev/era   k+b/b  ship_us/ev  peakwin_ev  shear_gs  live_base  live_pk  held_pk  worst_ms  dead")
    base_prev = None
    for k in range(0, int(rows[-1]["gs"] // P) + 1):
        b = [r for r in rows if k * P <= r["gs"] < (k + 1) * P]
        if not b:
            continue
        ev = sum(r["events"] for r in b)
        su = sum(r["ship_us"] for r in b)
        top = max(b, key=lambda r: r["events"])
        tot_k = sum(r["kicks"] for r in b) or 1
        ctr = sum(r["gs"] * r["kicks"] for r in b) / tot_k
        # baseline: min live in the quiet third of the era
        quiet = sorted(b, key=lambda r: r["events"])[: max(1, len(b) // 3)]
        base = min(r["live_mb"] for r in quiet)
        print(f"{k:>3} {ev:>8.0f} {(sum(r['kicks']+r['boundaries'] for r in b))/bodies:>6.3f} "
              f"{su/max(1e-9,ev):>10.2f} {top['events']:>10.0f} {ctr-(k+0.5)*P:>+9.0f} "
              f"{base:>9.1f} {max(r['live_mb'] for r in b):>8.1f} {max(r['held'] for r in b):>7.0f} "
              f"{max(r['worst_ms'] for r in b):>8.1f} {b[-1]['dead']:>5.0f}")
