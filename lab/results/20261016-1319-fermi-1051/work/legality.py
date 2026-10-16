#!/usr/bin/env python3
"""The comb cure decision, from shipped source constants only (fermi-1051).

Every constant below is copied from crates/universe/src/scenario.rs, ctx.rs and
ext.rs on this tree (grep the named literals); the script is pure arithmetic, so
the checker can vary any constant adversarially.  Units are the engine's own
geometric root units (the sun's M = 1.477 km = 1 root length unit, c = 1), so
P = 2*pi*sqrt(a^3/mu) is exact in root time units and 1 root time unit =
1.477e3 m / c = 4.9246e-6 s.
"""
import math

# ---- shipped constants (scenario.rs, ctx.rs) ----
M_SUN_RU = 1.0                 # "The sun's M is 1.477 km: one root length unit"
M_HOME = 2.0 ** -18            # PlanetSpec Home mass_log2: -18
M_MOON_RATIO = 2.0 ** -6       # "2^-6 of Home's mass"
HOME_PERI = 99_300_000         # root units
HOME_E = 1.0 / 50
MOON_PERI = 260_000            # root units (periapsis, in Home's doll)
MOON_E = 1.0 / 20
CINDER_PERI = 35_600_000       # root units (root doll)
CINDER_E = 1.0 / 10
GIANT_M = 2.0 ** -10           # mass_log2: -10
GIANT_PERI = 500_000_000.0     # root units
GIANT_E = 1.0 / 20
STEP_LOG2 = 7                  # ctx.rs Config::default()
AU_RU = 101_300_000.0          # scenario.rs `pub const AU`
ROOT_T_S = 1477.0 / 299_792_458.0   # seconds per root time unit
TAU0 = 3.6e-3                  # r9's secular bound (rung 9, 1 October)
R_H_FRAC = TAU0 ** (1.0 / 3.0)      # r9's own equivalence: "0.17 Hill radii"

def period_s(a_ru, mu_ru):
    return 2 * math.pi * math.sqrt(a_ru ** 3 / mu_ru) * ROOT_T_S

def sma(peri, e):
    return peri / (1.0 - e)

print("== P2: the metronome identity (one lever, not two) ==")
a_home = sma(HOME_PERI, HOME_E)
a_moon = sma(MOON_PERI, MOON_E)
a_cin = sma(CINDER_PERI, CINDER_E)
P_moon = period_s(a_moon, M_HOME)
P_cin = period_s(a_cin, M_SUN_RU)
P_home_orbit = period_s(a_home, M_SUN_RU)
print(f"Home a = {a_home:.4g} ru; orbit P = {P_home_orbit/86400:.3f} d")
print(f"Moon  a = {a_moon:.4g} ru; P = {P_moon/86400:.2f} d (doll's shortest secondary)")
print(f"Cinder a = {a_cin:.4g} ru; P = {P_cin/86400:.2f} d (root doll's shortest secondary)")
kicks_rate = 2 ** STEP_LOG2 / P_cin
print(f"metronome kicks/body/game-s = 2^{STEP_LOG2}/P_Cinder = {kicks_rate:.3e}"
      f"  (measured fired kicks 3.55-3.64e-5, gold a9d7; interval P_D/128 with f'(c)")
print(f"  absorbs the 89 d vs measured 77.24 d anchor difference, cf45)")
print(f"events (kick+boundary)/body/game-s = {2*kicks_rate:.3e} (measured stream 3.55-4.62e-5)")

print("\n== P3: r9's secular bound on the shipped populations ==")
R_H = a_home * (M_HOME / (3 * M_SUN_RU)) ** (1.0 / 3.0)
print(f"R_Hill(Home) = {R_H:.4g} ru; tau0^(1/3) = {R_H_FRAC:.3f} R_H"
      f"  (r9: '0.17 Hill radii')")

# In-situ locals: octave-uniform a in [5,200, 2^5 * 5,200) root units (scenario.rs ladder_ship)
lo = 5_200.0
inside = []
for oct_ in range(5):
    a_lo, a_hi = lo * 2 ** oct_, lo * 2 ** (oct_ + 1)
    # uniform within the octave -> mean a of the octave upper half decides little; use the
    # fraction of the octave inside the bound analytically (uniform in a)
    frac = max(0.0, min(1.0, (R_H * R_H_FRAC - a_lo) / (a_hi - a_lo)))
    tau_top = (a_hi / R_H) ** 3
    inside.append(frac)
    print(f"  octave {oct_}: a in [{a_lo:.0f}, {a_hi:.0f}) ru, a/R_H in "
          f"[{a_lo/R_H:.3f}, {a_hi/R_H:.3f}), tau at top = {tau_top:.2e}, "
          f"{frac*100:.0f}% inside")
f_in = sum(inside) / 5.0
a_med = lo * 2 ** 2 * 1.5  # median octave's midpoint
print(f"in-situ locals inside the bound: {f_in*100:.0f}%  (prediction >= 90%)")
print(f"  median local tau ~ {(a_med/R_H)**3:.2e} = {TAU0/(a_med/R_H)**3:.0f}x under tau0")

# L4/L5 quarter: the Moon's orbit +-3% in size
a_l45 = a_moon
tau_l45 = (a_l45 / R_H) ** 3
print(f"L4/L5 quarter: a = {a_l45:.0f} ru = {a_l45/R_H:.3f} R_H, tau = {tau_l45:.2e}"
      f" = {tau_l45/TAU0:.1f}x OVER tau0 (resonant with the Moon; law.md excludes resonances)")

# The quiet belt: tides of Giant and Home on a 2-3 AU body about the star
for name, m, a_p, e_p in [("Giant", GIANT_M, GIANT_PERI, GIANT_E),
                          ("Home", M_HOME, HOME_PERI, HOME_E)]:
    a_p2 = sma(a_p, e_p)
    worst = 0.0
    for a_b in (2.0 * AU_RU, 2.5 * AU_RU, 3.0 * AU_RU):
        tau = (m / (3 * M_SUN_RU)) * (a_b / a_p2) ** 3
        worst = max(worst, tau)
    print(f"belt under {name}'s tide: worst tau = {worst:.2e} = {TAU0/worst:.0f}x under tau0")

# Adversarial: Home's mass one octave either way (not tuned on)
for mlog2 in (-19, -18, -17):
    m = 2.0 ** mlog2
    r_h = a_home * (m / (3 * M_SUN_RU)) ** (1.0 / 3.0)
    fr = sum(max(0.0, min(1.0, (r_h * R_H_FRAC - lo * 2 ** o) / (lo * 2 ** o)) )
             for o in range(5)) / 5.0
    print(f"  adversarial Home mass_log2 = {mlog2}: R_H = {r_h:.3e} ru, in-situ inside {fr*100:.0f}%")

print("\n== P4: the wall ladder (measured constants, this composition) ==")
M1_US_PER_EVENT = 29.3          # 7da3 checker, M1-projected; ladder.txt ~30
STORM = 334                     # events, worst frame, e070/917c/4c22
STREAM = 3.55e-5                # kicks/body/game-s, gold a9d7 (events 4.62e-5, 7da3)
RTF = 100.0
FPS = 60.0
LETTER_S = 0.012
for label, storm in [("shipped", STORM), ("translate (335->141)", 141),
                     ("hybrid delete (300->~123)", STORM * 75 / 300 * (356/356)),
                     ("de-phase (334->53)", 53)]:
    budget = LETTER_S - storm * M1_US_PER_EVENT * 1e-6
    n = budget / (STREAM * 2 * RTF / FPS * M1_US_PER_EVENT * 1e-6) if budget > 0 else 0
    print(f"  {label:28s} letter N = {n:.2e}")
for gb, bpb in [(6.0, 5.06e3), (8.0, 4.85e3)]:
    print(f"  memory wall: {gb:.0f} GB at {bpb/1e3:.2f} kB/body -> {gb*1e9/bpb:.2e} bodies (b30b plateau)")
comb_rate = 4.02  # ev/game-s, 4c22, N-independent
print(f"  10^9 neutrality: comb {comb_rate} ev/game-s vs stream {STREAM*2*1e9:.2e} ev/game-s"
      f" -> comb = {comb_rate/(STREAM*2*1e9)*100:.4f}% of the rail")
print(f"  the delete lever on the belt (secular-legal, P3): cuts the rail's own constant"
      f" 2^{STEP_LOG2}/P_D -> kicks only on certificate breaks (cf45: 148x over at flying pace)")
