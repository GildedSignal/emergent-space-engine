#!/usr/bin/env python3
"""H_live: distinctions (first quantum crossings, births) per game-second vs the 8 GB budget.

Every rate below is derived from physics with explicit units; the bits come from
lab/results/20261008-2031-fermi-9d49/measure.jsonl (the shipped shipmem store, round-trip exact).

Scenes:
  A. belt-belt self-scattering (gravitational, 2D belt annulus)
  B. fleet gravity sweeping a belt (aggregate mass, principle 6)
  C. resonance-chaos zones (the only monotone promoter at game scale)
  D. births by program vs individual births (policy, not physics)
"""
import math

G = 6.674e-11
AU = 1.496e11
Msun = 1.989e30
YR = 3.156e7

# --- measured store widths (bits per body), from measure.jsonl -------------
BITS_PROGRAM = 17.29   # convoy, perfect launch program, 1.00e6 members
BITS_FORM    = 29.60   # formation (grid + jitter columns)
BITS_SCAR    = 70.68   # one kick on a convoy member (first distinction)
BITS_INDIV_TR= 149.73  # trader-like individual (shared doll key)
BITS_INDIV   = 196.62  # fully individual (no shared structure)

# --- budget -----------------------------------------------------------------
N = 1e9
GIB = 1 << 30
BODY_BUDGET = 4 * GIB * 8 / N     # bits per body at 4 GiB (ABP's open cap)
ALL_RAM = 8 * GIB * 8 / N         # absurd upper bound: all of RAM for bodies
print(f"budget: {BODY_BUDGET:.1f} bits/body (4 GiB for bodies) | {ALL_RAM:.1f} bits/body (all 8 GB, unusable)\n")

def f_max(bits_special, bits_rest=BITS_PROGRAM, budget=BODY_BUDGET):
    """max fraction of N bodies that may sit in the expensive form."""
    return (budget - bits_rest) / (bits_special - bits_rest)

print("ceilings (fraction of 1e9 bodies, rest on convoy programs):")
for name, b in [("individual (trader-like)", BITS_INDIV_TR), ("individual (random)", BITS_INDIV),
                ("scarred program member", BITS_PROGRAM + BITS_SCAR)]:
    print(f"  {name:26s} {b:6.1f} bits -> f_max <= {100*f_max(b):5.1f}%  "
          f"({f_max(b)*1e6:.0f} per 1e6 bodies)")
print(f"  all convoy: {BITS_PROGRAM:.1f} bits = {BITS_PROGRAM*N/8/GIB:.2f} GiB   "
      f"all formation: {BITS_FORM*N/8/GIB:.2f} GiB   "
      f"all individual(random): {BITS_INDIV*N/8/GIB:.2f} GiB")
print()

# --- A. belt-belt: gravity never crosses the quantum; contacts do (2D) ------
# Gravitational flyby: dv = 2 G m/(b v_rel), so b_cross = 2 G m/(q_v v_rel).
# For rocks b_cross/R = G rho R^2/(...) << 1: sub-quantum by orders (accumulates
# exactly on the grid, r2). In 2D the only quantum event between rocks is a
# CONTACT: rate per body = S_n * 2(2R) * v_rel (v_rel does NOT cancel).
N_b = 8.4e6
a_in, a_out = 2.2, 3.2
area = math.pi * ((a_out * AU) ** 2 - (a_in * AU) ** 2)
S_n = N_b / area
v_orb = 29.8e3 * math.sqrt(1 / 2.7)
v_rel = 5e3
q_v = 1e-6 * v_orb
orbit_s = 4.4 * YR
print("A. belt-belt, B18b geometry (8.4e6 rocks, 2.2-3.2 AU, 2D annulus, q_rel=1e-6):")
print(f"   mean spacing {math.sqrt(1/S_n):.3g} m")
for R, tag in [(1e3, "1-km rocks"), (1e2, "100-m rocks"), (1.0, "1-m rocks")]:
    b_cross = 2 * G * (2600 * (4/3) * math.pi * R ** 3) / (q_v * v_rel)
    rate = S_n * 2 * (2 * R) * v_rel
    print(f"   {tag:11s} b_cross={b_cross:8.1f} m vs contact radius {2*R:6.0f} m -> "
          f"contact per body every {1/rate/YR:8.3g} yr game time "
          f"(belt turnover: every body individual after ~that long)")
print("   gravity between rocks: b_cross < contact radius at every rock size ->")
print("   all mutual gravitational kicks are sub-quantum (sum exactly, 0 bits until they cross)\n")

# --- A2. an embedded mass M promotes its crossing neighbourhood ------------
# Others' promotion rate by ONE embedded mass M: rate = S_n * 2 b_cross v_rel
#   = S_n * 4 G M / q_v  (v_rel cancels: the sweep narrows as v rises).
# Belt turnover per T: M_T = N_b q_v/(4 G S_n T).
print("A2. embedded masses (planets, protoplanets, heavy fleets) - the movers:")
for T_yr, tag in [(1e5, "100 kyr"), (1e6, "1 Myr"), (1e9, "1 Gyr")]:
    M_T = N_b * q_v / (4 * G * S_n * T_yr * YR)
    print(f"   turnover of the whole belt in {tag:7s} of game time needs M >= {M_T:8.3g} kg "
          f"({M_T/1000:8.3g} t)")
M_ceres = 9.4e20
rate_c = S_n * 4 * G * M_ceres / q_v
print(f"   one Ceres (9.4e20 kg) embedded: {rate_c*86400:.0f} promotions per game-day, "
      f"belt fully individual after ~{N_b/rate_c/YR:.0f} yr")
M_fleet = 1e15
print(f"   one 1e15 kg fleet (10^9 t): {S_n*4*G*M_fleet/q_v*YR:.1e} promotions/yr: "
      f"dead term alone, alive only as aggregates (principle 6)\n")

# --- C. resonance-chaos zones ----------------------------------------------
# first-order resonance half-width W = 2.5 mu^(2/3) (B17's own constant), spacing
# of adjacent first-order resonances ~ (2/3)/j^2; chaotic fraction and Lyapunov
# time bracketed from belt statistics (tau_L ~ 1e2-1e4 orbits at zone edges).
mu = 9.54e-4                       # Jupiter/Sun
W = 2.5 * mu ** (2 / 3)
j = 5.0
spacing = (2 / 3) / j ** 2
f_cov = W / spacing                # fraction of semimajor axis covered by zone widths
q_e = 1e-6
ln_inv_q = math.log(1 / q_e)
print(f"C. resonance chaos (mu={mu:.1e}, W={W:.3f} a, spacing~{spacing:.3f} a, "
      f"coverage {100*min(f_cov,1):.0f}% of axis):")
for f_chaos in (0.05, 0.3):
    for tau_L_orbits in (1e2, 1e4):
        t_cross = tau_L_orbits * ln_inv_q * orbit_s       # first quantum crossing
        # N_belt bodies promoted once each over t_cross
        prom_rate = f_chaos * 8.4e6 / t_cross             # per second, this belt
        print(f"   f_chaos={f_chaos:4.2f}  tau_L={tau_L_orbits:5.0e} orb -> "
              f"crossing at {t_cross/YR:8.1e} yr game time, "
              f"promotion rate {prom_rate:.1e}/s, "
              f"H_live growth {prom_rate*BITS_INDIV_TR/8:.1e} B/s")
print("   (inside a strong zone the first resonant kick per conjunction is already")
print("    above the quantum: crossing in ~orbits, not tau_L*ln(1/q); bound unchanged)")
print("   -> monotone, bounded by f_chaos*N_belt once each; "
      f"{0.3*8.4e6*BITS_INDIV_TR/8/GIB*1e3:.1f} MB per belt at f=0.3 (a 1e9-body"
      f" universe of such belts: {0.3*BITS_INDIV_TR/8*1e9/GIB:.1f} GiB)\n")

# --- D. births --------------------------------------------------------------
print("D. births: program births emit ~a program per launch (amortized ~0 bits/member);")
print("   individual births are player-rate (~1/s x 150-197 bits): DEAD TERM at engine scale\n")

# --- E. the verdict table ---------------------------------------------------
print("E. time to exhaust 4 GiB of body store at 1e9 bodies")
print("   (assuming the universe's belts carry the 1e9; f_chaos promoted once each)")
for f_chaos in (0.05, 0.12, 0.3, 1.0):
    bits = (1 - f_chaos) * BITS_PROGRAM + f_chaos * BITS_INDIV_TR
    print(f"   f_indiv={f_chaos:4.2f} -> {bits:5.1f} bits/body = {bits/8*N/GIB:5.2f} GiB "
          f"{'OK' if bits <= BODY_BUDGET else 'OVER'}")
print()
print("F. event rate vs distinction rate (representation.md's 6e4 kicks/game-second):")
print("   kicks update E,L in place on the law's grid: 0 new bits unless first crossing.")
print("   In the smooth belt (outside resonance cover), distinction bits / kick < 1e-9.")
print("   Inside resonance zones the ratio ~ 1 for the first kick per body, 0 after (Tube saturates).")
