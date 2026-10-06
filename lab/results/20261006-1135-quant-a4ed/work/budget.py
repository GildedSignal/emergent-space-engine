#!/usr/bin/env python3
"""Event-capacity budget: N_max = R * P / (kicks_per_orbit * RTF),
from the measured all-core (8 vCPU) rates in raw.jsonl (x86, orders of magnitude).
R = sustained events/s for a layout, P = orbital period, k = kicks/orbit."""
import json, subprocess, os

here = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(here, "raw.jsonl")) if l.strip()]
rate = {(r["regime"], r["L"], r["threads"]): r["events_per_s"] for r in rows}

R = {
    "today 29us/kick (8 cores)": 8 / 29e-6,          # plane's measured kick, HANDOFF
    "chase  L=4 dependent":     rate[("chase", 4, 8)],
    "gather L=4 independent":   rate[("gather", 4, 8)],
    "gather L=8 independent":   rate[("gather", 8, 8)],
    "stream L=4 @21.8GB/s cap": 21.8e9 / (4 * 64),  # bandwidth-capped from the L=1 aggregate
}
P = {"battle P=90min": 5400.0, "belt P=1yr": 3.15e7}
K = {"today 64/orbit": 64.0, "averaged 0.3/orbit": 0.3}

out = {"rates_events_per_s_allcore": {k: round(v) for k, v in R.items()}, "grid": {}}
print(f"all-core rates (ev/s): " + ", ".join(f"{k}={v:.3g}" for k, v in R.items()))
print()
hdr = f"{'scene':22} {'cadence':18} {'RTF':>4} " + " ".join(f"{n:>26}" for n in R)
print(hdr)
for pk, pv in P.items():
    for kk, kv in K.items():
        for rtf in (1, 10):
            cells = []
            for rn, rv in R.items():
                nmax = rv * pv / (kv * rtf)
                cells.append(f"{nmax:>9.2e} {'PASS' if nmax >= 1e9 else 'fail':>16}")
                out["grid"][f"{pk}|{kk}|rtf{rtf}|{rn}"] = round(nmax)
            print(f"{pk:22} {kk:18} {rtf:>4} " + " ".join(cells))
json.dump(out, open(os.path.join(here, "budget.json"), "w"), indent=1)
print()
# inverse: required event rate at the goal
for n, k, p, rtf in [(1e9, 64, 5400, 1), (1e9, 64, 5400, 10), (1e9, 0.3, 5400, 10), (1e9, 64, 3.15e7, 10)]:
    print(f"need {n*k*rtf/p:.3g} ev/s for N=1e9, k={k}/orbit, P={p:.0e}s, RTF={rtf}")
