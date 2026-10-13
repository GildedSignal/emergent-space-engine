# Predictions (written before the anchors/sweep/coast/held-out runs; after the 2-flight pilot)

The pilot (L4/L5 at 1.099R on the minimal world) already reproduced the page's from-orbit bracket:
L4 DEAD (crash, r_last 0.914R, t = 661 game-s, inside the page's 363–758 s), L5 ALIVE at 2^35.
Nothing below was tuned on any sweep result.

## The ruler I will test

From rest, with constant horizontal thrust `a` and local gravity `g`, the trajectory is the ray
along `(a, −g)`: it misses the planet iff `a/g > R/√(r² − R²)` — the thrust-gravity resultant
must point outside the planet's disk (the tangent from the ship). Candidate ruler:

    Λ*(r) = κ · R/√(r² − R²),  Λ = a/g_local(r)

The from-rest tangent is the wrong vertex for a braked ship (it enters the fall already
descending), so κ > 1 is expected; κ is fixed BEFORE the sweep from the page's own D-row bracket
only: r*(L4) < 1.099R < r*(L5) ⟹ Λ*(1.099R) ∈ (5.37, 10.7) ⟹ **κ ∈ (2.45, 4.88)**, central 3.5.

## P1 — validation (anchors, 16 levels at 1.099R)

Crash for L ≤ 4, live for L ≥ 5, fault None on crash (the engine's surface kill), zero refusals
expected. If the level bracket moves by a level, the minimal world (no moon, no fleet, circular
Home) is not the plane's D row and the sweep is void until the difference is understood.

## P2 — the sweep (r*(L), levels 0–5, bisection 1%)

Pre-registered central predictions (κ = 3.5, a(L) = 0.35 g·2^L, g(1.099R) = 10.33 m/s²):

    r*(L0) ≈ 2.40R   [κ band (2.45, 4.88): 2.15–2.73R]
    r*(L1) ≈ 1.94R
    r*(L2) ≈ 1.62R
    r*(L3) ≈ 1.38R
    r*(L4) ≈ 1.165R  (consistent with the D row: crashes at 1.099R)
    r*(L5) ≈ 1.063R  (consistent: lives at 1.099R)

The prediction is the collapse: κ(r) := Λ*(r)·√(r² − R²)/R constant across the six levels within
their bisection brackets. Failure mode registered: if κ(r) drifts monotonically with r (|d ln κ /
d ln r| > 0.2 over the sweep), the tangent ruler is dead; I then fit the power law Λ* ∝ (r/R)^−p
and report p (the page's two raised-apo brackets imply p ≈ 1 if the tangent holds, p = 0 if Λ is
universal — the page already measured that Λ is not universal).

## P3 — held-out arms (never used in any fit)

    (2.30R, L0): predicted CRASH (2.30 < r*(L0) ≈ 2.40)
    (2.50R, L0): predicted LIVE  (2.50 > 2.40)
    (1.55R, L2): predicted CRASH (1.55 < 1.62)
    (1.70R, L2): predicted LIVE  (1.70 > 1.62)

## P4 — the basin's anatomy

- Coast control: alive at every swept radius (no thrust, no crash) — the instrument's negative.
- Determinism: one repeated arm gives the identical anatomy (same ticks, r, fault).
- Live arms near the boundary graze: min_r − 1 → 0 as r → r*+ (the page's L5-at-1.099R graze
  specimen, 1.014R); far above the boundary the escape pumps (β grows, doll handoff, alive).
- Crash arms die inside Home's doll with r_at_death < 1 (the surface kill), no fault.

## What this sweep cannot decide (stated, not hidden)

At circular starts Ψ = τ_brake·ω = 1/Λ identically (v₀ = √(g·r)), so the sweep cannot separate
"thrust vs local weight" from "thrust vs centrifugal deficit": it pins the ruler's r-dependence
(the exponent), not which force the thrust races. The page's tracking-nose raised-apo brackets are
the cross-controller check (different nose law, same planet); I compare κ against them post hoc.

## Kill criteria

- P1 fails ⟹ harness ≠ plane, void until understood.
- Coast crashes ⟹ the world itself is unstable at that radius; that radius is out of the sweep.
- κ not constant per P2 ⟹ tangent ruler dead; report the fitted power law instead.
