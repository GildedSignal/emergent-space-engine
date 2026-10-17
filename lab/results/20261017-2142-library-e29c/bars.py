#!/usr/bin/env python3
"""The certificate's angle bars, frozen from the shipped consumers.

Every input is a shipped constant (client page.html, scene scenario.rs, law.md) or a
published measurement (f5bd drift law on lab/wiki/library-directions.md; the encounters
page's miss quantum). No flight; pure composition. Regenerates every number in the
dossier's bar table.
"""
import math

# --- shipped constants ---------------------------------------------------------
AU_LS = 499.004784          # xtask/src/universe/page.html:58 (1 AU in light-seconds)
BELT_IN, BELT_OUT = 2.0, 3.0  # crates/universe/src/scenario.rs:333, nladder.rs:2
R_MID = 0.5 * (BELT_IN + BELT_OUT) * AU_LS       # ls
AREA = math.pi * (BELT_OUT**2 - BELT_IN**2)       # AU^2
DOT = 2.0                   # px, a kind===4 belt body's rect (bodyPaint, page.html:141)
B_MISS = 49.0               # m, the finest delivered contact miss (encounters page, ev=-45)
Q_GRID = 360.0 / 2**32      # deg, the tube's 32-bit periapsis angle (docs/law.md line 12)
AU_M = 1.495978707e11       # m

# --- published measurements (f5bd, second-author run, library-directions page) ---
DRIFT_MAX_BELT = 2.2e-3     # deg, the belt population's own max |dangle| at 7.41e6 game-s
DRIFT_T_END = 7.41e6        # game-s
CADENCE = 3.55e-5           # ev/(body.game-s), the belt's metronome stream rate
REKICK_COST = 0.6           # of one fired kick (f5bd: 0.51-0.6x)

def q_view_deg(n):
    """One dot's phase resolution against its neighbours: half the mean inter-body
    separation (a 2 px dot against a 2 px neighbour), at the belt's mid radius."""
    spacing_ls = math.sqrt(AREA / n) * AU_LS      # ls, mean inter-neighbour separation
    half_px = spacing_ls / DOT                    # one pixel of the neighbour-resolved view
    return math.degrees(half_px / R_MID), spacing_ls

def t_star_belt(q_deg):
    """When the belt's own max drift crosses q (its measured law ~ t^2 to 2.2e-3 deg
    at 7.41e6 gs), in game-s."""
    return DRIFT_T_END * math.sqrt(q_deg / DRIFT_MAX_BELT)

print("== the consumers' bars (all degrees) ==")
print(f"q_grid   (law's acting angle grid, 32-bit periapsis) = {Q_GRID:.3e}")
qc_deg = math.degrees(B_MISS / (R_MID * AU_LS * 1e3 / 1e3))  # b*/r in rad -> deg
qc_deg = math.degrees((B_MISS / AU_M) / (R_MID / AU_LS))     # same, explicit
print(f"q_contact (49 m at r_mid = {R_MID:.1f} ls)          = {qc_deg:.3e}")
print(f"            below q_grid by {Q_GRID/qc_deg:.1f}x")
rows = []
for n in (1e5, 1e6, 1e9):
    q, sp = q_view_deg(n)
    ts = t_star_belt(q)
    k = ts * CADENCE
    cost = REKICK_COST / k if k > 0 else float('inf')
    rows.append((n, q, sp, ts, k, cost))
    print(f"q_view   N={n:>9.0e}: {q:.3e} deg  (spacing {sp:.3g} ls) "
          f"T*={ts:.3g} gs  k*={k:.0f} kicks  re-kick={100*cost:.2f}% of deleted stream")

print("\n== the mass bar (the aggregate's dipole noise vs the host's field) ==")
theta = rows[-1][1]  # q_view at 1e9, deg
for ratio in (1e-3, 1e-6, 1e-9):  # M_belt/M_host
    for n in (1e5, 1e9):
        frac = ratio * math.radians(theta) / math.sqrt(n)
        print(f"  M_belt/M_host={ratio:.0e}, N={n:.0e}: dipole-noise/host = {frac:.2e}")

print("\n== the fence against the flown horizons ==")
horizon = 8e6  # game-s, the longest flown horizon (f5bd)
for n, q, sp, ts, k, cost in rows:
    fired = ts < horizon
    print(f"  N={n:>9.0e}: q_view={q:.3e} deg; belt max drift crosses at {ts:.3g} gs "
          f"{'FIRES before 8e6 gs' if fired else 'never fires before 8e6 gs'} "
          f"(k*={k:.0f}, cost {100*cost:.2f}%)")
