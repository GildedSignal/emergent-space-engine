#!/usr/bin/env python3
"""The 10^9 ledger recomposed (18 Oct constants) + the belt event-flow floor.

Two computations, every constant cited to a wiki run or shipped source:
  A. EVENT FLOW of the shipped belt at N=1e9: a 2-D Poisson sweep on the scenario's own
     geometry (planar belt, a in [2,3) AU, e Rayleigh 0.07, ship radius 49 m).
  B. CPU COMPOSITION of the belt kick stream at 1e9 rtf 100 on measured levers
     (split, secular delete, boundary fast path), M1 and x86 anchors.

Prints one JSON blob; regen.sh runs it after the shipped-code anchor.
"""
import json, math, subprocess, sys

# ---- shipped geometry constants (crates/universe/src/scenario.rs) ----
AU_ru = 101_300_000            # scenario.rs:10, root units per game AU
RU_m = 1737e3 / 1176           # Moon radius 1,176 ru = 1,737 km  ->  m per ru
AU_m = AU_ru * RU_m            # = 1.493e11 m  ~= SI AU (1.496e11)
ship_r = 34 * 2.0**-10 * RU_m  # belt ship radius, scenario.rs:346  -> ~49 m
A_eff_AU2 = 25.0               # effective annulus a in [2,3], e<=0.4 tails included
A_eff = A_eff_AU2 * AU_m**2
v_rel = 1.8e3                  # m/s shear+epicyclic at conjunction (dV = 1.5 (da/a) v ~ 1.1k, e v ~ 1.3k)
T_own_SI = 2.5**1.5 * 3.156e7  # s, SI Kepler at 2.5 AU (game AU ~ SI AU)
INTERVAL = 28_141.5            # game-s, kick interval = P_D/2^7 (3294; belt_first anchor)
KICKS_PER_ORBIT = 3163 * 2.5**1.5  # 4093: 3,163 kicks/own-orbit at 1 AU on the doll grid
T_own_gs = KICKS_PER_ORBIT * INTERVAL
S_PER_GS = T_own_SI / T_own_gs  # SI seconds per game-second at the root doll

def sweep(N, b):
    """Expected conjunctions per game-second, whole belt, closer than b (2-D Poisson sweep)."""
    n2 = N / A_eff                          # m^-2
    per_body_SI = n2 * 2 * b * v_rel        # per SI second (Poisson gas; ec74 gold: l ~ density^0.95)
    return per_body_SI * S_PER_GS * N       # per game-second, total

out = {"geometry": {"AU_m": AU_m, "ship_radius_m": ship_r, "A_eff_m2": A_eff,
                    "v_rel": v_rel, "T_own_game_s": T_own_gs, "SI_s_per_game_s": S_PER_GS}}

# ---- A. event flow at 1e9 ----
N = 1e9
flow = {
    "contacts_per_game_s (b<=98m)": sweep(N, 2 * ship_r),
    "conjunctions_per_game_s_b5e5": sweep(N, 5e5),   # 2b89's key-mint scale
    "conjunctions_per_game_s_b1e7": sweep(N, 1e7),
    "contacts_per_body_per_orbit": sweep(N, 2 * ship_r) * T_own_gs / N,
}
flow["mint_cores_rtf100 (16.4us/key, 2b89-5567 creation)"] = flow["conjunctions_per_game_s_b5e5"] * 100 * 16.4e-6
flow["exact_eval_cores_rtf100 (0.6us, 277d r_event)"] = flow["conjunctions_per_game_s_b5e5"] * 100 * 0.6e-6
flow["contact_cores_rtf100 (1us)"] = flow["contacts_per_game_s (b<=98m)"] * 100 * 1e-6
# cross-check: 1b1f measured 0.105-0.247 encounters/body/orbit at N=800
per_orbit_800 = sweep(800, 1.0) * T_own_gs / 800   # at b=1 m, to invert for their b
flow["1b1f_implied_b_m"] = 0.176 / per_orbit_800   # their mid rate / model rate per metre
out["flow_at_1e9"] = flow

# ---- B. stream composition at 1e9, rtf 100 ----
RTF = 100
rate0 = 2 / INTERVAL                      # ev/body/game-s shipped: 1 kick + 1 boundary (8ffc)
def cores(rate, cost_us, n=N): return n * rate * RTF * cost_us * 1e-6
M1, X86 = 29.3, 50.0                      # page anchors (nladder 1051: 29.3us M1; 4093: ~50us x86)
split = 8                                 # 7f97/de7b, welded (kick+boundary ride together)
survival = [0.615, 0.385]                 # 1a46 belt delete 274/712; with RES 434/712
comp = {"shipped_M1": cores(rate0, M1), "shipped_x86": cores(rate0, X86),
        "kicks_only_M1": cores(rate0 / 2, M1)}
res = {}
for s in survival:
    kicks = cores(rate0 / 2 / split, M1) * s            # kick comb after split+delete
    bnd_shipped = kicks                                  # boundary comb ~= kick comb (1:1, 8ffc)
    bnd_fast = bnd_shipped * 0.05                        # fast path: 0.21-0.27us vs 4.4-5.6us clock path
    total = kicks + bnd_fast
    res[f"survival_{s}"] = {"kicks_M1": kicks, "boundary_fast_M1": bnd_fast, "total_M1": total,
                            "total_x86": total * X86 / M1}
    # required extra cadence cut S* for 4 cores (boundary free)
    res[f"survival_{s}"]["S*_for_4_cores"] = total / 4
comp["composed"] = res
comp["kick_cost_for_4_cores_at_split8 (us, survival .615)"] = 4 / (cores(rate0 / 2 / split, 1.0) * 0.615) 
comp["floor_42ns_cores_shipped_cadence"] = cores(rate0, 0.042)
out["stream_1e9_rtf100"] = comp

# ---- anchor: belt_first p50 (shipped example) ----
try:
    r = subprocess.run(["cargo", "run", "--release", "-q", "-p", "emergent-universe",
                        "--example", "belt_first", "--", "10000"],
                       capture_output=True, text=True, timeout=300,
                       cwd=subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                           capture_output=True, text=True).stdout.strip())
    out["belt_first_10000"] = r.stdout.strip().splitlines()
except Exception as e:
    out["belt_first_10000"] = [f"ERROR {e}"]

print(json.dumps(out, indent=1))
