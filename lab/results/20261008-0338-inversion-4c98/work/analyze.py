#!/usr/bin/env python3
"""Aggregate probe JSONs; score pre-registered predictions P1-P6; work accounting."""
import json, glob
import numpy as np

rows = {}
for f in sorted(glob.glob("*-[12].json")):
    d = json.load(open(f))
    key = d["name"]
    rows.setdefault(key, []).append(d)

def agg(name, path):
    vals = [r for r in rows.get(name, [])]
    out = []
    for v in vals:
        node = v
        for p in path:
            node = node[p]
        out.append(node)
    return out

print(f"{'case':16s} {'seed':4s} {'nb':4s} {'E_intra':7s} {'E_cross':7s} {'wall_s':6s}")
for name, ds in rows.items():
    for d in ds:
        print(f"{name:16s} {d['seed']:<4d} {d['nb']:<4d} {d['E_intra']:<7d} {d['E_cross']:<7d} {d['wall_s']:<6.1f}")

print("\n=== miss rates at k=4 and required ranks, cadence 16/orbit (median over seeds) ===")
for name in ("fleet", "loose-fleet", "fleet+crossers", "fleet+belt"):
    if name not in rows: continue
    for scope in ("global", "fleet"):
        for pt in ("intra", "cross"):
            key = f"{scope}/{pt}"
            m4 = [d["cadences"]["16"][key]["miss_k4"] for d in rows[name] if key in d["cadences"]["16"]]
            if not m4: continue
            p99 = [d["cadences"]["16"][key]["rank_p99"] for d in rows[name] if key in d["cadences"]["16"]]
            un = [d["cadences"]["16"][key]["unreachable"] for d in rows[name] if key in d["cadences"]["16"]]
            print(f"{name:16s} {key:14s} miss@k4={np.median(m4):8.3f}  rank_p99={np.median(p99):8.1f}  unreachable={np.median(un):.2f}")

print("\n=== cadence coupling (p99 required rank, global scope, cross pairs) ===")
for name in ("fleet+crossers", "fleet+belt"):
    if name not in rows: continue
    for C in ("8", "16", "32", "64"):
        key = "global/cross"
        p99 = [d["cadences"][C][key]["rank_p99"] for d in rows[name] if key in d["cadences"][C]]
        p50 = [d["cadences"][C][key]["rank_p50"] for d in rows[name] if key in d["cadences"][C]]
        if p99:
            print(f"{name:16s} cadence {C:>2s}/orbit: rank_p50={np.median(p50):8.1f} rank_p99={np.median(p99):8.1f}")

print("\n=== predictions ===")
def med(name, C, key, field):
    try:
        return float(np.median([d["cadences"][C][key][field] for d in rows[name] if key in d["cadences"][C]]))
    except (KeyError, ValueError):
        return None
p1 = med("fleet", "16", "global/intra", "miss_k4")
print(f"P1 control fleet intra miss@k4 (expect <= 0.01): {p1}  -> {'PASS' if p1 is not None and p1 <= 0.01 else 'FAIL->VOID'}")
p2 = med("fleet+crossers", "16", "fleet/cross", "miss_k4")
print(f"P2 crossers fleet-scope cross miss@k4 (expect >= 0.95): {p2}  -> {'PASS' if p2 is not None and p2 >= 0.95 else 'FAIL'}")
p3 = med("fleet+crossers", "16", "global/cross", "rank_p99")
print(f"P3 crossers global-scope cross rank_p99 (expect > 20): {p3}  -> {'PASS' if p3 is not None and p3 > 20 else 'FAIL'}")
p4 = med("fleet+belt", "16", "global/cross", "miss_k4")
print(f"P4 belt global-scope cross miss@k4 (expect > 0.05): {p4}  -> {'PASS' if p4 is not None and p4 > 0.05 else 'FAIL'}")
p5 = med("loose-fleet", "16", "global/intra", "rank_p99")
print(f"P5 loose fleet intra rank_p99 (expect <= 4): {p5}  -> {'PASS' if p5 is not None and p5 <= 4 else 'FAIL'}")
try:
    p99_c8 = np.median([d["cadences"]["8"]["global/cross"]["rank_p99"] for d in rows["fleet+crossers"]])
    p99_c16 = np.median([d["cadences"]["16"]["global/cross"]["rank_p99"] for d in rows["fleet+crossers"]])
    p99_c64 = np.median([d["cadences"]["64"]["global/cross"]["rank_p99"] for d in rows["fleet+crossers"]])
    print(f"P6 cadence coupling crossers: p99@8={p99_c8:.1f} p99@16={p99_c16:.1f} ratio(16/8)={p99_c16/max(p99_c8,1e-9):.2f} (expect ~0.5); p99@64={p99_c64:.1f} (expect > 8)")
except (KeyError, ValueError) as ex:
    print("P6 missing:", ex)

print("\n=== work accounting (pairs per real encounter, per refresh-equivalent) ===")
for name in ("fleet+crossers", "fleet+belt"):
    if name not in rows: continue
    d = rows[name][0]
    nf = int((d["nb"] - 800))  # other population
    n_other = d["nb"] - 800
    E_cross = np.median([x["E_cross"] for x in rows[name]])
    E_intra = np.median([x["E_intra"] for x in rows[name]])
    print(f"{name}: fleet=800 other={n_other} | radial-overlap/window tier pairs fleet*other = {800*n_other:,} "
          f"per element-change vs E_cross={E_cross:.0f} -> {800*n_other/max(E_cross,1):.0f} pairs per cross encounter")
    print(f"   phase tier at k=4, N={d['nb']}: {d['nb']*4:,} directed pairs per refresh "
          f"vs E_total={E_intra+E_cross:.0f} -> {d['nb']*4/max(E_intra+E_cross,1):.1f} per encounter per refresh-interval")
