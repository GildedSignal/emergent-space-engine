#!/usr/bin/env python3
"""Sum the read census of one nladder flight log: the demand side of the retention law.

Usage: census_sum.py <log> — prints the flight's totals, the demand (history reads, deepest
look-back) and the supply (the retention law's `keep`, median body), per flight and at the
final probe; every number of the dossier's evidence section regenerates from here."""
import re
import sys

rows = []
views = []
for line in open(sys.argv[1]):
    if line.startswith("census:"):
        d = dict(re.findall(r"(\w+)=([-\d.e+]+)", line))
        v = re.search(r"view\(r=(\d+) h=(\d+) lb_gs=([\d.]+)\)", line)
        s = re.search(r"scan\(r=(\d+) h=(\d+) lb_gs=([\d.]+)\)", line)
        d["v"], d["s"] = (v.groups() if v else ("0", "0", "0")), (s.groups() if s else ("0", "0", "0"))
        rows.append(d)
    elif line.startswith("viewcensus:"):
        views.append(dict(re.findall(r"(\w+)=([-\d.e+]+)", line)))

reads = sum(int(d["reads"]) for d in rows)
hist = sum(int(d["hist"]) for d in rows)
gs = [float(d["gs"]) for d in rows]
bodies = 30028
last = rows[-1]
print(f"probes {len(rows)}  gs {gs[0]:.0f} -> {gs[-1]:.0f}")
print(f"reads_total {reads:,}  hist_total {hist}  hist_frac {hist / max(1, reads):.2e}")
print(f"hist_per_body_per_gs {hist / bodies / (gs[-1] - gs[1]):.3e}")
print(f"lookback_run_max_gs {float(last['run_max_gs']):.1f}")
print(f"final stock_b {last['stock_b']}  segs {last['segs']}  segs_per_body {int(last['segs']) / bodies:.2f}")
print(f"final keep med/max gs {float(last['keep_med']):.0f}/{float(last['keep_max']):.0f}")
print(f"keep_over_demand {float(last['keep_med']) / max(1e-9, float(last['run_max_gs'])):.1f}x")
print("view gathers:", len(views))
for d in views:
    print(f"  viewcensus gs={float(d['gs']):.0f} n={d['n']} age_max_gs={d['age_max_gs']} age_p50_gs={d['age_p50_gs']}")
vv = [d for d in rows if int(d["v"][0]) > 0]
print(f"windows_with_view_reads {len(vv)} of {len(rows)}")
for d in vv[-3:]:
    print(f"  gs={float(d['gs']):.0f} view r={d['v'][0]} h={d['v'][1]} lb_max={d['v'][2]} | all lb_max={d['lb_max_gs']}")
