#!/usr/bin/env python3
"""Fermi audit of the 10^7-rung composition (686f + ef63): does every published
cell close under ONE belt-legality survival s, and what is the rung's honest
margin at each legality?

Sources (page-cited constants, each frozen in a run or in shipped code):
  cadence stream  3.5e-5 events/body/game-second  -- ladder.txt's own
                   "10^7 bodies = 357 kicks a game-second" (=3.57e-5/B/gs);
                   b30b end-to-end 3.33-3.50e-5; the metronome identity
                   2^step_log2/P_D with step_log2=7 (crates/universe/src/ctx.rs
                   default, ext.rs's law, belt_first.rs's doc).
  cost            30.9-51.7 us/event M1 (1051's 29.3; b29a's smallest wiring
                   34-38; c4d3/3570's belt kick 50.4; 686f's own shipped cell
                   back-implies 30.9-51.7 -- we adopt the implied band so every
                   cell reproduces before any correction).
  promotion       4.6 us (760f).
  budget          0.72 s/s = 12 ms x 60 fps (ladder.txt).
  rtf             100 (ladder.txt's flights and its own wall conversion
                   "357 kicks a game-second = 36,000 a wall second").
  wave window     13,051-14,534 gs (ladder.txt/belt_first) = 1,483 gs
                   = 14.83 s wall at rtf 100 -> 10.68 s of budget; staggered
                   window = one interval 2.814e4 gs = 281.4 s -> 202.6 s.
  s_RES           4/712   (1a46: the RES widening deletes 708/712 of the belt)
  s_frozen        434/712 (1a46: the frozen exclusion q/r<=8 within 2% spares
                   434/712) -- independently re-derived below from scenario.rs.
"""
import json, math, random

CAD = 3.5e-5          # events/body/gs (the kick stream; see header)
COST_LO, COST_HI = 30.9e-6, 51.7e-6
PROMOTE = 4.6e-6
BUDGET = 0.72
RTF = 100
WIN_U = 13_051.0, 14_534.0            # gs, unstaggered wave window
WIN_U_S = (WIN_U[1] - WIN_U[0]) / RTF * BUDGET          # budget seconds in it
INTERVAL = 2.814e4                     # gs, one cadence interval (cf45)
WIN_S_S = INTERVAL / RTF * BUDGET                       # staggered budget
S_RES = 4.0 / 712.0
S_FROZEN = 434.0 / 712.0

def stream(N, rtf, s, cost):
    """steady stream, seconds of compute per wall second"""
    return N * CAD * rtf * cost * s

def wave(N, rtf, s, cost, win_budget_s):
    """one wave's total cost over its window budget (both wall seconds)"""
    return N * s * cost / win_budget_s

def cell(name, N, rtf, s, tag):
    lo = stream(N, rtf, s, COST_LO); hi = stream(N, rtf, s, COST_HI)
    print(f"{name:<44} s={s*100:5.2f}% [{tag}]  stream {lo:.3f}-{hi:.3f} s/s "
          f"(x{BUDGET/hi:.1f}-{BUDGET/lo:.1f} margin vs 0.72)")
    return lo, hi

print("== A. reproduction of the published cells (one s per row?) ==")
def win_budget(rtf, staggered=False):
    w = INTERVAL if staggered else (WIN_U[1] - WIN_U[0])
    return w / rtf * BUDGET
print(f"wave budgets: unstaggered {win_budget(RTF):.1f} s at rtf100 / "
      f"{win_budget(1):.0f} s at rtf1; staggered {win_budget(RTF, True):.0f} s at rtf100\n")
cell("10^7 shipped steady", 10**7, RTF, 1.0, "no delete")
cell("10^7 lazy+RES steady  ['0.006-0.010']", 10**7, RTF, S_RES, "RES")
cell("10^7 frozen steady    (corrected)", 10**7, RTF, S_FROZEN, "frozen")
cell("10^9 steady spared    ['0.61-1.02']", 10**9, 1, S_FROZEN, "frozen")
cell("10^9 steady under RES (corrected)", 10**9, 1, S_RES, "RES")
print()
for (name, N, rtf, s, stag) in [
    ("10^7 ES_SECULAR-only wave ['19.8-34.3x']", 10**7, RTF, S_FROZEN, False),
    ("10^7 lazy+RES wave        ['0.2-0.3x']", 10**7, RTF, S_RES, False),
    ("10^9 wave                 ['18.1-31.4x']", 10**9, 1, S_FROZEN, False),
    ("10^7 frozen wave, staggered (corrected)", 10**7, RTF, S_FROZEN, True),
]:
    wb = win_budget(rtf, stag)
    lo = wave(N, rtf, s, 34.6e-6, wb)
    hi = wave(N, rtf, s, 60.1e-6, wb)
    print(f"{name:<44} s={s*100:5.2f}%  wave {lo:.2f}-{hi:.2f} x budget")

print("\n== B. the cliff ==")
print(f"s_frozen/s_RES = {S_FROZEN/S_RES:.1f}x on the stream at every scale "
      f"(N.rtf invariant: 10^7 x rtf100 = 10^9 x rtf1)")
for s, tag in [(S_RES, "RES legal"), (S_FROZEN, "frozen legality")]:
    lo, hi = stream(10**7, RTF, s, COST_LO), stream(10**7, RTF, s, COST_HI)
    rtf_ok = 100 * BUDGET / hi
    print(f"10^7 @rtf100 {tag:<16} stream {lo:.3f}-{hi:.3f} s/s "
          f"({BUDGET/hi:.2f}-{BUDGET/lo:.2f}x budget); one thread holds to "
          f"rtf~={rtf_ok:.0f}")

print("\n== C. the frozen exclusion re-derived from scenario.rs ==")
# planets: periapsis(root units), e -> a(AU); AU = Home's "1 AU" periapsis
AU = 99_300_000.0
planets = {"Cinder": (35_600_000 / AU, 0.10), "Home": (99_300_000 / AU, 0.02),
           "Giant": (500_000_000 / AU, 0.05)}
P = {k: (per / (1 - e)) ** 1.5 for k, (per, e) in planets.items()}
print("periods (yr): " + ", ".join(f"{k} {v:.3f} (a={per/(1-e):.3f} AU)"
      for k, v, (per, e) in ((k, P[k], planets[k]) for k in planets)))
random.seed(1)
def belt_a():
    while True:
        a = 2.0 + 3.0 * random.random()
        e = -math.log(1.0 - random.random()) * 0.0707  # Rayleigh sigma=.07
        if e <= 0.4 and a * (1 - e) > 1.2:
            return a
def spared(a, order=8, tol=0.02, space="period"):
    Pb = a ** 1.5
    for Pp in P.values():
        rho = max(Pb, Pp) / min(Pb, Pp) if space == "period" else None
        if space == "period":
            for m in range(1, order + 1):
                for n in range(1, order + 1):
                    if abs(rho - m / n) <= tol * (m / n):
                        return True
        else:  # semimajor-axis space
            ap = (Pp ** (2 / 3))
            for m in range(1, order + 1):
                for n in range(1, order + 1):
                    if abs(a - ap * (m / n) ** (2 / 3)) <= tol * ap * (m / n) ** (2 / 3):
                        return True
    return False
for space in ("period", "a"):
    N = 200_000
    frac = sum(spared(belt_a(), space=space) for _ in range(N)) / N
    print(f"spared by the frozen rule ({space}-space, order<=8, 2%): {frac:.3f}")
print(f"measured frozen survival (1a46): {S_FROZEN:.3f}; RES: {S_RES:.5f}")

out = {"s_frozen": S_FROZEN, "s_res": S_RES, "cliff": S_FROZEN / S_RES,
       "stream_1e7_rtf100": {"res": stream(10**7, RTF, S_RES, 1),
                             "frozen": stream(10**7, RTF, S_FROZEN, 1)}}
json.dump(out, open("work/fermi_check.json", "w"), indent=1)
print("\nwrote work/fermi_check.json")
