#!/usr/bin/env python3
"""Compose the fleet term of the 10^9 encounter ledger from fleetk.jsonl.

Constants cited from the wiki pages:
  interval      28,141.5 game-s   (kick-cadence: the belt doll interval)
  events/body/interval = 2        (8ffc: one kick + one boundary comb per body)
  BELT_SPLIT    8                 (98cb: bulk kick every 8 intervals)
  c_checked     measured here     (exact-checked pair; x86, orders of magnitude)
  budget        4 cores at rtf 100 (flying pace: interval wall = 281.4 s)
"""
import json, sys

path = sys.argv[1] if len(sys.argv) > 1 else "work/fleetk.jsonl"
rows = [json.loads(l) for l in open(path)]
TAU = 6.283185307179586
INTERVAL = 28141.5
WALL = INTERVAL / 100.0          # rtf 100
SPLIT = 8
BUDGET = 4.0
rows = [r for r in rows if "arm" in r]

time_arm = next(r for r in rows if r["arm"] == "time")
c_checked = time_arm["checked_us_per_pair"] * 1e-6
c_visit = time_arm["visit_ns_per_pair"] * 1e-9
print(f"# c_checked={c_checked*1e6:.2f}us/pair c_visit={c_visit*1e9:.2f}ns/pair (measured, this box)")
print(f"# interval={INTERVAL} gs wall@rtf100={WALL:.1f}s split={SPLIT} budget={BUDGET} cores")

N = 1e9
print(f"\n# Fleet term at N={N:.0e}, phi=1 (all bodies in fleets), sigma_e=1e-2, keys/uniform:")
print(f"# {'F':>7} {'reach':>6} {'k_body':>8} | {'cores@8iv(visit)':>16} {'cores@8iv(checked)':>18} {'cores@per-kick(checked)':>22}")
for f, reach in [(1e3, None), (1e4, None), (1e5, None)]:
    r = next(x for x in rows if x["arm"] == "keys" and x["n"] == int(f))
    k_body = r["pairs"] / r["n"]                     # forward-window pairs per body
    pairs = N * k_body
    cores8v = pairs * c_visit / (WALL * SPLIT)
    cores8c = pairs * c_checked / (WALL * SPLIT)
    coreskc = 2 * N * k_body * c_checked / WALL      # every member event re-windows
    print(f"# {int(f):>7} {r['reach']:>6.3f} {k_body:>8.1f} | {cores8v:>16.4f} {cores8c:>18.1f} {coreskc:>22.0f}")

print("\n# Cluster fleets (sigma_l=0.05 < reach): complete graph, quad_frac measured:")
for r in rows:
    if r["arm"] == "clust":
        k_body = r["pairs"] / r["n"]
        pairs = N * k_body
        print(f"#   F={r['n']:>6} quad_frac={r['quad_frac']:.4f} k_body={k_body:.0f} "
              f"cores@8iv(checked)={pairs*c_checked/(WALL*SPLIT):.0f}")

print("\n# Fit: max fleet size F* that keeps the fleet term within the 4-core budget")
print("# (every-8-interval full rebuilds, checked pairs, sigma_e=1e-2 keys):")
for r in rows:
    if r["arm"] == "keys":
        k_body = r["pairs"] / r["n"]
        f_max = BUDGET * (WALL * SPLIT) / (N * (k_body / r["n"]) * c_checked)
        print(f"#   at F={r['n']:>6}: k_body={k_body:.1f} -> F* ~ {f_max:.0f}")

ev = next(r for r in rows if r["arm"] == "event")
print(f"\n# The contrast at F=400: events={ev['events']} rank_max={ev['rank_max']} "
      f"(the ANSWER is rank-0) vs mean_k_paid={ev['mean_k_paid']}, max_k_paid={ev['max_k_paid']} (the SEARCH)")
print(f"#   checked pairs per real event: {ev['pairs_paid']/ev['events']:.0f}")
print(f"#   exact evals per real event:   {ev['exact_evals']/ev['events']:.0f}")
tk = next(r for r in rows if r["arm"] == "tree")
print(f"\n# Refused train fallback (F=1000, da=1e-2, H=100): tree tier cand={tk['cand']} "
      f"(= {tk['cand']/(1000*999/2)*100:.0f}% of the complete graph), exact_evals={tk['exact_evals']}, {tk['secs']}s")

print("\n# Per-member-event unit (incremental re-window of the kicked body), F=1e4 keys:")
k10000 = next(r for r in rows if r["arm"] == "keys" and r["n"] == 10000)
k_body = k10000["pairs"] / k10000["n"]
print(f"#   {k_body:.0f} checked pairs x {c_checked*1e6:.2f}us = {k_body*c_checked*1e3:.2f} ms per member event, "
      f"vs the stream's own ~50us/event anchor: {k_body*c_checked/50e-6:.0f}x")
