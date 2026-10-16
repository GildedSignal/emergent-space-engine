#!/usr/bin/env python3
"""The corrected legality domain (the checker's three attacks, re-derived from shipped constants
and from the flight's own runtime flag), plus the wall ladder with the MEASURED storm constants.

Every shipped constant is from scenario.rs/ctx.rs (grep the literals); the flight fractions are
from states_1900_arm.csv (ES_SECULAR's runtime decisions, cross-checked against an independent
recomputation: 0 mismatches over 1,023 non-fleet ships)."""
import math

# ---- shipped constants ----
M_SUN, M_HOME, M_MOON, M_CIN, M_GIANT = 1.0, 2.0**-18, 2.0**-24, 2.0**-21, 2.0**-10
A_HOME = 99_300_000 / (1 - 1/50)      # periapsis, e = 1/50
A_MOON = 260_000 / (1 - 1/20)         # in Home's doll, root units
A_CIN = 35_600_000 / (1 - 1/10)
A_GIANT = 500_000_000 / (1 - 1/20)
AU = 101_300_000.0
TAU0 = 3.6e-3

def tau(m_p, m_host, a, a_p):
    return 3.0 * (m_p / m_host) * (a / a_p) ** 3

moon_line = (TAU0 / tau(M_MOON, M_HOME, 1.0, A_MOON)) ** (1 / 3)
star_line = (TAU0 / tau(M_SUN, M_HOME, 1.0, A_HOME)) ** (1 / 3)

print("== P1: the legality domain, per perturber (r9's own form tau = 3 (m_p/m_host) (a/a_p)^3) ==")
print(f"R_H(Home) = {A_HOME*(M_HOME/(3*M_SUN))**(1/3):.4g} ru; the Moon's tide line for the")
print(f"in-situ locals sits at a = {moon_line:.0f} ru (tau_Moon = tau0), the star's at {star_line:.0f} ru:")
print(f"  tau_Moon(a=166,400) = {tau(M_MOON,M_HOME,166_400,A_MOON):.3f} ({tau(M_MOON,M_HOME,166_400,A_MOON)/TAU0:.1f}x over tau0);")
print(f"  tau_Moon(a=83,200) = {tau(M_MOON,M_HOME,83_200,A_MOON):.2e} ({tau(M_MOON,M_HOME,83_200,A_MOON)/TAU0:.1f}x UNDER)")
print(f"  -> the Moon, not the star, draws the line inside the top octave; the checker's Attack-1")
print(f"     magnitudes ('1.1-49x over', a=83,200 at 3.9e-3) are mutually inconsistent with any")
print(f"     (a/d)^3 scaling (their own two points differ by 45x where the law gives 8x).")
print("  flight (measured, the runtime flag): in-situ deleted 200/233 = 85.8% (the Moon keeps a > ~116k")
print("     plus 3 resonant stragglers); the quarter 75/75 spared (co-orbital); the belt 274/712 deleted")
print("     (the resonance exclusion as frozen — every q/r<=8 within 2% for each of 3 planets — spares")
print("     more than half the belt: a law choice to revisit, not a tide fact).")

print("\n== P2: the residual storm, measured (flights/*.txt, this run's instrument) ==")
M1_US, STREAM, RTF, FPS, LETTER_S = 29.3e-6, 3.55e-5, 100.0, 60.0, 0.012
for label, storm, note in [("shipped (measured 334 @5400gs)", 334, "4fa8/4c22 + this run's OFF"),
                           ("translate (measured 141)", 141, "4534"),
                           ("hybrid delete (MEASURED 131 @5400gs)", 131, "frame 3173, the same beat as OFF's 334"),
                           ("hybrid delete @1900gs (46)", 46, "below the N=0 floor (51)"),
                           ("de-phase (measured 53)", 53, "4c22")]:
    budget = LETTER_S - storm * M1_US
    n = budget / (STREAM * 2 * RTF / FPS * M1_US) if budget > 0 else 0
    print(f"  {label:38s} letter N = {n:.2e}   [{note}]")
print(f"  memory wall 6-8 GB at 4.85-5.06 kB/B: 1.19-1.65e6 (b30b) — every arm past it, tie stands")
print(f"  the composed candidates adjudicated: 131 measured vs 134 'Moon-corrected' (winner, 2.5% off)")
print(f"  vs 83.5 'proportional' (refuted, 57% off): the residual comb is the spared standing set,")
print(f"  dominated by the resonant quarter (75) + the Moon-tide top (33) + fleet/plane ships.")

print("\n== P3: the ledger (measured, 5,400 game-s, N=1000, seed 1) ==")
off_k, off_e = 9217, 22219
arm_k, arm_e = 1382, 6580
print(f"  kicks {off_k} -> {arm_k} (-{100*(1-arm_k/off_k):.0f}%), events {off_e} -> {arm_e} (-{100*(1-arm_e/off_e):.0f}%)")
print(f"  the delete cuts BOTH populations' metronome at once (the comb and the belt stream);")
print(f"  the spread arms pay +11-20% for the same storm class.")
