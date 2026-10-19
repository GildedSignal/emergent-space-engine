#!/usr/bin/env python3
"""Read a seam flight's census (stderr) and summary (stdout); print the seam's story:
scan counts by doll/verdict, the near/cands/ns profiles inside and outside the belt band
(2-3 AU), and the crossing's game time span. Usage: analyze.py <run-stem>"""
import sys, re, math

stem = sys.argv[1]
err = open(f"logs/{stem}.err").read().splitlines()
AU_LO, AU_HI = 2.0, 3.0
rows = []
for ln in err:
    if not ln.startswith("seamscan"):
        continue
    d = dict(kv.split("=", 1) for kv in ln.split()[1:])
    rows.append({k: (v if k in ("win",) else float(v) if k != "t" else int(v)) for k, v in d.items()})
# game-s scale from the ladder line's game_s and the t span is unavailable per line; use t ticks directly (report in ticks).
def band(r):
    return AU_LO <= r["r_au"] <= AU_HI

walks = [r for r in rows if r["walk"] == 1.0]
print(f"scans total {len(rows)}  walks {len(walks)}  win-fail {sum(1 for r in rows if r['win']!='ok')}")
by_doll = {}
for r in rows:
    a = by_doll.setdefault(int(r["doll"]), [0, 0])
    a[0] += 1
    a[1] += r["walk"] == 1.0
print("by doll (scans, walks):", {k: tuple(v) for k, v in sorted(by_doll.items())})

in_band = [r for r in rows if band(r)]
near_band = [r for r in rows if not band(r) and 1.5 <= r["r_au"] <= 4.0]
out_far = [r for r in rows if r["r_au"] > AU_HI]
def prof(rs, name):
    if not rs:
        print(f"{name}: none")
        return
    for k in ("near", "cands", "ns_cap"):
        vs = sorted(r[k] for r in rs)
        n = len(vs)
        print(f"{name} {k}: p50 {vs[n//2]:.0f} p90 {vs[int(n*0.9)]:.0f} max {vs[-1]:.0f} min {vs[0]:.0f}")
prof(in_band, "in-band(2-3AU)")
prof(near_band, "near-band(1.5-4AU)")
first = next((r for r in rows if band(r)), None)
last = [r for r in rows if band(r)]
if first:
    print(f"band entered at t={int(first['t'])} (r_au {first['r_au']:.3f}), scans in band {len(last)}, exits last r_au {last[-1]['r_au']:.3f}")
# the tail: the last 20% of scans (post-belt verdicts — does the filter still cut?)
tail = rows[int(len(rows)*0.8):] if rows else []
if tail:
    tw = sum(1 for r in tail if r["walk"] == 1.0)
    print(f"tail(last 20% = {len(tail)} scans): walks {tw}, r_au max {max(r['r_au'] for r in tail):.2f}, cands p50 {sorted(r['cands'] for r in tail)[len(tail)//2]:.0f}")
# ns per candidate for in-band captures
if in_band:
    ns = [r["ns_cap"] / max(r["near"], 1) for r in in_band if r["near"] > 0]
    ns.sort()
    print(f"in-band ns per near body: p50 {ns[len(ns)//2]:.1f}" if ns else "in-band ns per near body: n/a (all walks)")
