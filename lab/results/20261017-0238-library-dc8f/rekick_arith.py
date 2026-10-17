#!/usr/bin/env python3
"""Source-derived arithmetic for the library run 20261017-0238-library-dc8f.

Every input is a published number from the lab wiki pages, cited below; no flight.
Outputs JSON to work/derived.json and prints the tables the dossier quotes.
"""
import json
import math

# ---- inputs (all cited) ----------------------------------------------------
# [1a46] 20261016-1637-second-...-fermi-1051-1a46 + [1637 check]:
D1, A1 = 5_400.0, 2.6e-4        # game-s, max |Delta angle| of the deleted set (deg)
D2, A2 = 11_000.0, 1.2e-3       # checker's 2x-horizon flight
GO_LIVE = 1e7                   # game-s ~ 2^16 carried kicks ("goes live") [1a46]
# [a9d7 gold] fired kicks 3.55e-5/body/game-s (belt stream, seed/N-invariant):
STREAM = 3.55e-5                # ev/B/gs == carried-kick cadence per body
# [87fd + checker] doll-born drift medians |dE/E0|:
X9_OFF, X9_CURE = 19.4e-6, 19.8e-6   # at 9,000 gs OFF better by a hair (check: OFF 19.4? see note)
# NOTE [1637 check]: "OFF is WORSE (|dE/E0| med 19.8 vs 19.4e-6)" -> OFF=19.8, cure=19.4
X9_OFF, X9_CURE = 19.8e-6, 19.4e-6
OFF_GROWTH_PER_X2 = 10.0        # "OFF's median grows ~x10 for a x2 horizon" [1637 check]
# [8792] promotion dwell dial, burn 10^3/10^5, miss rate vs dwell (game-s):
DIAL = {5: 75, 17: 73, 40: 72, 60: 72, 80: 71, 100: 14}   # % miss
MUSK_BUDGET = 0.10              # add-back budget [Isaacson, Elon Musk]

out = {}

# ---- 1. debt law ----------------------------------------------------------
p = math.log(A2 / A1) / math.log(D2 / D1)
out["debt_exponent_two_point"] = round(p, 3)
debt_at = lambda t: A1 * (t / D1) ** p
out["debt_at_1e7gs_deg"] = round(debt_at(GO_LIVE), 3)
quantum = debt_at(GO_LIVE)          # the angle scale where the fence "goes live"
# reset interval T* holding max debt at one quantum: A1*(T*/D1)^p = quantum
T_star = D1 * (quantum / A1) ** (1.0 / p)
out["T_star_gs"] = round(T_star)
out["T_star_carried_kicks"] = round(math.log2(T_star * STREAM))

print(f"debt law: |dA| ~ t^{p:.2f}  (two published points)")
print(f"debt at 1e7 gs: {debt_at(GO_LIVE):.3f} deg  (= fence go-live scale)")
print(f"reset interval holding one quantum: T* = {T_star:.3g} gs "
      f"= 2^{math.log2(T_star*STREAM):.1f} carried kicks")

# ---- 2. add-back cost vs Musk's 10% --------------------------------------
print("\nk  re-kick every 2^k kicks   interval (gs)   add-back / deleted stream   budget?")
for k in range(6, 13):
    T = (2 ** k) / STREAM           # gs between re-kicks
    addback = 1.0 / (2 ** k)        # events per carried kick
    frac = addback / 1.0            # relative to the deleted stream (= same cadence)
    ok = frac <= MUSK_BUDGET
    print(f"{k:2d}  {2**k:6d} kicks          {T:9.3g}      "
          f"{frac*100:7.3f}%                    {'yes' if ok else 'NO'}")
    out[f"addback_2^{k}_pct_of_stream"] = round(frac * 100, 4)

# ---- 3. drift slope vs envelope ------------------------------------------
off_18k = X9_OFF * OFF_GROWTH_PER_X2
out["off_median_18000gs_pred"] = off_18k
print(f"\nOFF drift median predicted at 18,000 gs (x10 per x2): {off_18k:.2e}")
print(f"  -> vs the 4,500-gs seed band 2.0e-6: x{off_18k/2.0e-6:.0f}; an envelope frozen")
print(f"     at any flown horizon is passed by construction; freeze the slope.")

# ---- 4. dial table (published) -------------------------------------------
print("\ndwell dial (burn, published [8792]): miss % by dwell game-s")
for d, m in sorted(DIAL.items()):
    print(f"  dwell {d:4d} gs -> miss {m}%")

with open("work/derived.json", "w") as f:
    json.dump(out, f, indent=1)
print("\nwrote work/derived.json")
