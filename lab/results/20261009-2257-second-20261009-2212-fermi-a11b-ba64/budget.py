#!/usr/bin/env python3
"""The 10^9-in-8GB budget, decomposed — second-author regeneration pass.

Every measurement is READ from evidence/*.json produced by this run's stated
commands (the shipped tree, git a838a28); only repo anchors are constants.
Anchors: H0190 (kicks/orbit, averaging cut), H0210 (M1 kick µs), law.md (tube
bytes), components-98bc (belt bits/body).  Orders of magnitude only.
"""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- repo anchors (M1 unless said) ----
KICKS_PER_ORBIT_UNAVG = 32.5      # H0190 K1, low orbit (tides as kicks)
AVERAGING_CUT         = 114.0     # H0190 K2 (32.5 -> 0.285 kicks/orbit)
KICK_US_M1            = 29.0      # H0210 limitation line
TUBE_BYTES            = 16        # law.md
BELT_BITS_PER_BODY    = 0.126     # components-98bc (program, at 2^20)
T_LOW                 = 5.4e3     # s, low orbit about an Earth
T_BELT                = 3.15e7    # s, belt body at ~1 AU
M1_CORES, M1_BYTES, RTF = 4, 8e9, 100
EVENT_KINDS = ("kicks","opens","boundaries","handoffs","lost","refused",
               "slices","encounters","decisions","leavers")

def load(name):
    with open(os.path.join(HERE, "evidence", name)) as f:
        return json.load(f)

def stats_fields(d):
    return {k: int(v) for k, v in re.findall(r"(\w+): (\d+)", d["stats"])}

def full_total(d):
    """Consistent aggregation: every per-body event counter."""
    f = stats_fields(d)
    return sum(f[k] for k in EVENT_KINDS), f

# ---- kick cost (this box; 6 repeats in evidence/) ----
kicks = [load(f"kick-bench-{i}.json") for i in range(1, 7)]
k_med = sorted(k["kick_us"]["median"] for k in kicks)
KICK_US_BOX_LO, KICK_US_BOX_HI = k_med[0], k_med[-1]
HIT = kicks[0]["memo"]["exact_hit_rate"]; NSAMP = kicks[0]["samples"]

# ---- bench ladder (71 -> 410 bodies) ----
ladder = []
for m in (48, 148, 248, 448):
    d = load(f"bench-m{m}-rtf100.json")
    tot, f = full_total(d)
    game_s = d["rtf_target"] * d["frames"] / 60.0
    sub = f["kicks"] + f["slices"] + f["leavers"]   # the ORIGINAL dossier's 406-body aggregation
    ladder.append(dict(members=m, bodies=d["bodies"], bpb=d["bytes_per_body"],
                       rate=tot / game_s / d["bodies"], subtotal=sub / game_s / d["bodies"]))
N1, N2 = ladder[0], ladder[-1]
SLOPE_2PT  = (N2["bodies"]*N2["bpb"] - N1["bodies"]*N1["bpb"]) / (N2["bodies"] - N1["bodies"])
xs = [p["bodies"] for p in ladder]; ys = [p["bodies"]*p["bpb"] for p in ladder]
nx, ny = sum(xs)/len(xs), sum(ys)/len(ys)
SLOPE_OLS = sum((x-nx)*(y-ny) for x, y in zip(xs, ys)) / sum((x-nx)**2 for x in xs)
RATE_MAX_N = ladder[-1]["rate"]                # steady state at the largest N measured

# ---- transient regime (rtf 1, 30 game-s) ----
tr = load("bench-m48-rtf1.json"); tr_tot, _ = full_total(tr)
tr_game_s = tr["rtf_target"] * tr["frames"] / 60.0
TR_RATE = tr_tot / tr_game_s / tr["bodies"]

# ---- engine per-item costs (largest run) ----
cost = load("bench-m448-rtf100.json")["engine_cost_by_kind"]
ship_us = next(c["us_per_item"] for c in cost if c["kind"] == "ship")
fleet_us = next(c["us_per_item"] for c in cost if c["kind"] == "fleet")

print("== 0. The record (read from evidence/, nothing hardcoded) ==")
for p in ladder:
    print(f"  members {p['members']:>3} -> {p['bodies']:>3} bodies, {p['bpb']:>4} B/body, "
          f"full-total {p['rate']:.2e} ev/body/game-s (k+s+l subtotal {p['subtotal']:.2e})")
print(f"  kick x6: medians {KICK_US_BOX_LO}-{KICK_US_BOX_HI} us (run 1 was the 60.0 cold outlier), "
      f"exact_hit_rate {HIT}, {NSAMP} samples")

print("\n== 1. The board's '190 cores' re-derived from its own anchors ==")
cores = 1e9 * (KICKS_PER_ORBIT_UNAVG / T_LOW) * KICK_US_M1 * 1e-6
print(f"  1e9 x 32.5 kicks / 5400 s x 29 us = {cores:.0f} cores (board: ~190) -> same corner:")
print(f"  unaveraged, low-orbit cadence for ALL bodies, rtf 1. A regime, not a property of N.")
belt_same = 1e9 * (KICKS_PER_ORBIT_UNAVG / T_BELT) * KICK_US_M1 * 1e-6
print(f"  the same bodies at belt cadence: {belt_same:.3g} cores ({T_BELT/T_LOW:.0f}x lower).")

print("\n== 2. Measured on the real engine (this box, shipped tree) ==")
print(f"  kick: {KICK_US_BOX_LO}-{KICK_US_BOX_HI} us median over 6 repeats (M1: 29);"
      f" memo exact_hit_rate {HIT} -> nothing shared")
print(f"  hot event rate (consistent full-total): {ladder[0]['rate']:.2e} at 71 bodies ->"
        f" {RATE_MAX_N:.2e} at {N2['bodies']}; mildly declining, flat 166->410")
print(f"    the original's 3.9e-2 at 406 was a kicks+slices+leavers subtotal (here {N2['subtotal']:.2e})")
print(f"  transient (rtf 1, 30 game-s, spawn window): {TR_RATE:.2e} /body/game-s"
        f" = {TR_RATE/RATE_MAX_N:.0f}x steady -> the capacity number is a STEADY-STATE number")
print(f"  live store: two-endpoint marginal {SLOPE_2PT/1e3:.2f} KB/body, 4-pt OLS {SLOPE_OLS/1e3:.2f} KB/body")
print(f"  (bytes/body is read before the cut's settle; stable in-session, ~0.1% cross-session)")
print(f"  tube is {TUBE_BYTES} B -> materialized state is {SLOPE_2PT/TUBE_BYTES:.0f}x"
        f" the law's number (OLS {SLOPE_OLS/TUBE_BYTES:.0f}x)")
print(f"  engine per-item: ship {ship_us:.0f} us, fleet slice {fleet_us:.1f} us")

print("\n== 3. Hot-body capacity (the binding pair; steady-state rate) ==")
for label, cost_us, ev in [("today, this box", KICK_US_BOX_HI, RATE_MAX_N),
                           ("today, M1 kick cost", KICK_US_M1, RATE_MAX_N),
                           ("+ slack skin 12.6x", KICK_US_M1/12.6, RATE_MAX_N),
                           ("+ averaging (orbit pops only)", KICK_US_M1/12.6, RATE_MAX_N/AVERAGING_CUT)]:
    n = M1_CORES / (RTF * ev * cost_us * 1e-6)
    print(f"  {label:32s} N_hot(rtf100, 4 cores) ~ {n:.2e}")
for label, b in [("today ~6.9 KB/body", SLOPE_2PT), ("tubes only 16 B", TUBE_BYTES),
                 ("B18 floor ~4 B/body", 4.0)]:
    print(f"  memory ceiling {label:22s} {M1_BYTES/b:.2e} bodies")

print("\n== 4. Cold-body capacity (programs; the 10^9 lives here) ==")
print(f"  1e9 belt bodies as programs: {1e9*BELT_BITS_PER_BODY/8/1e6:.1f} MB")
cpu = 1e9 * (KICKS_PER_ORBIT_UNAVG/AVERAGING_CUT) / T_BELT * KICK_US_M1 * 1e-6 * RTF
print(f"  their kick CPU at rtf 100 (0.28/orbit, 29 us): {cpu:.1e} cores")
sess_orbits = 100*3600*RTF / T_BELT
print(f"  horizon bound: 100 h session at rtf 100 = {sess_orbits:.3f} belt orbits;")
print(f"  even T_Lyapunov = 1e3 orbits -> {sess_orbits/1e3:.1e} e-foldings: no scar in play.")
print(f"  HOLE (named): a persisted universe reloaded across ~1e4 orbits WOULD scar;")
print(f"  the bound covers the pitched game, not save/reload archaeology.")

print("\n== 5. H_live for the plane's scene (measured composition, 71 bodies) ==")
f0 = stats_fields(load("bench-m48-rtf100.json"))
kicks_s, enc_s, leavers_s = f0["kicks"]/1000, f0["encounters"]/1000, (f0["lost"]+f0["leavers"])/1000
bits = (kicks_s + enc_s) * 40 + leavers_s * 100   # ~log2 of changed integer ranges: a disclosed guess
print(f"  kicks {kicks_s:.2f}/s, encounters {enc_s:.3f}/s, losses {leavers_s:.3f}/s"
      f" -> ~{bits:.0f} bits/game-s (rate measured, bits/event guessed)")
