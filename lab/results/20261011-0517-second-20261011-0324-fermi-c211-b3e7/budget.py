#!/usr/bin/env python3
"""The 10^9 budget, second author: the kick-magnitude rung folded in.

Changes vs the original budget.py (kept row-for-row comparable):
  1. the memory section prices the admission rule at two magnitudes (shipped k0 and the
     family jump `uniform`), from data/kickmag.jsonl;
  2. every kick-compute row states the sustainable population (N/over), which corrects the
     original's "0.5%" headline: it was 1/191, a division by the core count.

Inputs:  data/ladder.jsonl, data/measure.jsonl (original reproduce.sh, shipped code),
         data/kickmag.jsonl (kickmag sweep, this folder).
Sources: H0210 kick 29 us on the plane (M1); H0190 32 kicks/orbit, 0.3 averaged;
         r8 v2 belt 0: 427 encounters / 20 orbits / N=1841; M1: 8 cores, 60 GB/s, 8 GB
         (4 GiB universe budget per the approved plan).
Run:     python3 budget.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
N = 1_000_000_000
BYTES_BUDGET = 4 * 1024**3          # 4 GiB for the universe
CORES = 8
KICK_US = 29.0                      # plane, M1, H0210
KICKS_PER_ORBIT = 32.0              # H0190
KICKS_PER_ORBIT_AVG = 0.3           # H0190, secular averaging
ORBIT_RATE = 0.012                  # encounters/body/orbit, r8 v2 belt 0 (rho 1e-4..1e-3)
YEAR = 3.156e7

lad = {r["rung"]: r for r in map(json.loads, open(f"{HERE}/data/ladder.jsonl"))}
mea = {d["pop"]: d for d in map(json.loads, open(f"{HERE}/data/measure.jsonl"))}
km = [json.loads(l) for l in open(f"{HERE}/data/kickmag.jsonl")]
Sev = {r["mode"]: r for r in km if r["kind"] == "events" and r["m"] == 4096 and r["updates"] == 10000}
curve = {(r["mode"], r["f"]): r for r in km if r["kind"] == "curve" and r["m"] == 4096}

def bits_at(f):
    """Store bits/body at freshly-kicked fraction f (ladder curve, log-interpolated)."""
    pts = [(0.0, lad["0"]), (1e-4, lad["1e-4"]), (1e-3, lad["1e-3"]),
           (1e-2, lad["1e-2"]), (1e-1, lad["1e-1"]), (0.3, lad["0.3"]), (1.0, lad["1"])]
    prev = (0.0, lad["0"]["chosen_bits"])
    for x, r in pts:
        c = r["chosen_bits"]
        if f <= x:
            (x0, c0) = prev
            if x0 <= 0:
                return c0 + (c - c0) * (f / x if x else 0)
            return c0 + (c - c0) * (math.log10(f) - math.log10(x0)) / (math.log10(x) - math.log10(x0))
        prev = (x, c)
    return pts[-1][1]["chosen_bits"]

dH_kick   = lad["0"]["dH_bits_per_kick"]        # ~22.8 bits created per kick (shipped magnitude)
scar_bits = lad["0"]["dH_bits_per_new_scar"]    # ~61 bits per new scar (shipped magnitude)
seal_ns   = lad["0"]["p_seal_ns_per_update"]    # ~110 ns per sealed update
stream_ns = min((r["p_stream_ns"] or 1e9) for r in lad.values())
rand_ns   = mea["stream"]["rand_ns"]

kick_capacity = CORES / (KICK_US * 1e-6)
orbit_capacity_32  = kick_capacity / KICKS_PER_ORBIT
orbit_capacity_avg = kick_capacity / KICKS_PER_ORBIT_AVG

print(f"measured: dH/kick {dH_kick:.1f} b, scar {scar_bits:.0f} b, seal {seal_ns:.0f} ns, "
      f"stream {stream_ns:.1f} ns/b, rand {rand_ns:.0f} ns, kick {KICK_US:.0f} us")
print(f"M1 capacities: {kick_capacity:.2e} kicks/s -> {orbit_capacity_32:.2e} orbits/s (32 k), "
      f"{orbit_capacity_avg:.2e} orbits/s (0.3 k)")

print("\n== The scar constant vs kick magnitude (kickmag rung, m=4096, U=10000) ==")
print("mode (t,E,L,w deltas)      S b/scar   break-even f*   chosen(f=0.1)   B(f=1) ceiling")
budget_bits = BYTES_BUDGET * 8 / N
Smax = 0.0
for mode in ("16,10,10,10", "22,16,16,16", "28,22,22,22", "34,28,28,28", "40,34,34,34",
             "46,40,40,40", "uniform"):
    s = Sev[mode]["dH_bits_per_new_scar"]
    Smax = max(Smax, s)
    fstar = (budget_bits - 1) / s
    print(f"{mode:>20} {s:>10.1f} {fstar:>13.3f} {curve[(mode, 0.1)]['chosen_bits']:>14.2f} "
          f"{curve[(mode, 1.0)]['b_bits']:>15.1f}")
print(f"S = Elias-Fano ordinal (~7 b) + sum of per-field widths (b_c + 2): "
      f"measured {Sev['16,10,10,10']['dH_bits_per_new_scar']:.0f}..{Smax:.0f} b across magnitudes.")

rows = []
def row(term, demand, capacity, unit):
    over = demand / capacity if capacity else float("inf")
    rows.append((term, demand, capacity, unit, over))
    tag = f"OVER x{over:6.1f}" if over > 1 else f"under x{1/over:6.1f}" if over > 0 else ""
    print(f"{term:44s} {demand:10.3g} / {capacity:10.3g} {unit:10s} {tag}"
          f"  sustainable N = {N/over:.2e} ({100.0/over:.2f}% of 10^9)")

print("\n== Memory at 10^9 (4 GiB budget = %.1f bits/body) ==" % budget_bits)
for f in (0.0, 1e-2, 1e-1, 0.3, 0.6, 1.0):
    row(f"shipped magnitude, kicked f={f:g}", bits_at(f) * N / 8, BYTES_BUDGET, "B")
S_ship = Sev["16,10,10,10"]["dH_bits_per_new_scar"]
S_fam = Sev["uniform"]["dH_bits_per_new_scar"]
for name, s in (("shipped k0", S_ship), ("family jump (uniform)", S_fam)):
    fstar = (budget_bits - 1) / s
    row(f"admission rule 1+{s:.0f}f at f=f*={fstar:.2f}",
        (1 + s * fstar) * N / 8, BYTES_BUDGET, "B")
free_ceiling = BYTES_BUDGET * 8 / mea["traders"]["bits"]
print(f"free-body ceiling (traders {mea['traders']['bits']:.0f} b): {free_ceiling:.2e} bodies")
# time for encounter-driven f_cum to reach f* (RTF 100, year orbits, r8 rate)
fcum_rate = ORBIT_RATE * 100 / YEAR * 3600
for name, s in (("shipped k0", S_ship), ("family jump (uniform)", S_fam)):
    fstar = (budget_bits - 1) / s
    print(f"  f_cum reaches f*={fstar:.2f} ({name}) after {fstar/fcum_rate:.0f} h of RTF-100 "
          f"year-orbit play (f_cum grows {fcum_rate:.1e}/h)")

print("\n== Kick compute: orbit-throughput demand vs capacity ==")
print("demand = N / T_orbit * RTF (body-orbit completions per second)")
for T_name, T in (("1 year", YEAR), ("1 day", 86400.0), ("81 min (190-core corner)", 4860.0)):
    for rtf in (1, 100):
        for k, cap in ((32, orbit_capacity_32), (0.3, orbit_capacity_avg)):
            row(f"all on {T_name}, RTF {rtf}, {k} k/orb", N / T * rtf, cap, "orbit/s")
print("\nRestated headline (corrects the original's '0.5%'): the 81-minute corner is 23.9x")
print("over the M1 at RTF 1 (32 kicks/orbit) = 191 cores; the sustainable population there is")
print(f"{N/23.9:.2e} bodies = {100/23.9:.1f}% of 10^9 (RTF 1, 32 k), {100/22.4:.1f}% (RTF 100, 0.3 k),")
print(f"{100/2386.8:.2f}% (RTF 100, 32 k). The original's 0.5% was 1/191, dividing by the core count.")

print("\n== Encounter activity at the r8 rate (0.012/body/orbit), year orbits ==")
for rtf in (1, 100):
    enc = N * ORBIT_RATE / YEAR * rtf
    row(f"encounter kicks RTF {rtf}", enc * 2 * KICK_US * 1e-6, 1.0, "core")
    row(f"seals RTF {rtf} (37% scar)", enc * 2 * 0.37 * seal_ns * 1e-9, 1.0, "core")
    hlive = enc * 2 * dH_kick
    print(f"  H_live creation {hlive:.3g} bit/s; 4 GiB fills in {BYTES_BUDGET*8/hlive/3600:.1f} h unsealed")
print("H_live worst case across magnitudes: the family-jump kick creates ~%.0f b (vs 23), "
      "seal ~%.0f ns (vs 110): 4 GiB still fills only in ~%.0f h unsealed at RTF 100."
      % (Sev["uniform"]["dH_bits_per_kick"], Sev["uniform"]["p_seal_ns_per_update"],
         BYTES_BUDGET*8/(enc*2*Sev["uniform"]["dH_bits_per_kick"])/3600))

print("\n== Re-fit (re-infer) stream cost ==")
full_pass = N * stream_ns
print(f"full-population stream pass {full_pass/1e9:.1f} s; at 1 pass/100 s = {full_pass/100/1e9:.3f} core")

print("\n== Bandwidth ==")
ev = kick_capacity
bus = ev * 64 / 1e9
print(f"at {ev:.2e} events/s x 64 B = {bus:.1f} GB/s of 60: {'BINDING' if bus > 60 else 'not binding'}")
print(f"random access is latency-bound ({rand_ns:.0f} ns block decode), not bus-bound")

json.dump({"rows": [dict(zip(("term", "demand", "capacity", "unit", "over"), r)) for r in rows],
           "free_body_ceiling": free_ceiling, "kick_capacity_s": kick_capacity,
           "S_by_mode": {m: r["dH_bits_per_new_scar"] for m, r in Sev.items()}},
          open(f"{HERE}/data/budget.json", "w"), indent=1)
