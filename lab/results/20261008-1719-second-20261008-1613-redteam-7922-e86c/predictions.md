# Predictions (written before the decisive experiment)

The checker's named experiment: the re-anchor horizon on the **shipped
integer law** (`space-darwin16-v1`, `crates/space` `Orbit::compile`), not the
Kepler float model, across the e-tail (to 0.995), with the belt's kick
channels, evaluated on belt scenes that exist in the tree plus one hot tail,
plus the author's proposed criterion with its negative control.

Setup: cycles compiled fresh from `OrbitKey::bound(p, e_q48)` at every kick
(the exact record); the jet keeps the anchor cycle and updates the epoch by
the stored first derivative (central finite difference of compiled integer
periods — the memo's ∂/∂E, ∂/∂L, not yet implemented in the crate). Floor
1e-6 relative epoch error (law.md §3). Kick = absolute δ(1−e²) = EPS = 1e-7
per orbit (the first run's tide scale; ratios are EPS-independent, checked in
P6). Channels: **corrE** = secular energy kicks at fixed semi-latus rectum p
(fixed L — the first run's channel); **randE** = random-sign residual kicks
at fixed p; **corrL** = the tide channel, e pumped at fixed a (E conserved —
the double-averaged secular tide; the checker's "actual kick mode", invisible
in Kepler where T depends on E only).

None of the numbers below were tuned on the shipped law; they are carried
from the Kepler analysis plus GR-order arguments.

## P1 — mechanism on the integer cycle (corrE)

n\*(0.99)/n\*(0.5) = 0.075, band [0.03, 0.15] (Kepler (1−e²)^(2/3) = 0.0749;
the first run's (1−e)^(2/3) = 0.074 — both inside the band). n\*(0)/n\*(0.5)
= 1.24, band [1.0, 1.6]. The compiled cycle is Kepler plus ~1e-3-level
Schwarzschild corrections (periapsis ≥ 1024 M at fixed p), so the exponent
survives rounding and quadrature — unless the compiled period itself is only
precise to ~1e-6 between neighbouring e's, in which case horizons shorten
everywhere; I predict it is precise to ≤1e-9 and they do not.

## P2 — the tide channel at fixed a (corrL) — the held-out case

Kepler's shadow says T is exactly invariant along this channel, so the
horizon is set only by the GR period's L-sensitivity, which grows as the
periapsis dives (11.5 M at e = 0.995, a = 2304). Predictions:
n\*_L(0.5) ≥ 3000 (≥ 8× the corrE horizon 405); n\*_L(0.995)/n\*_E(0.995)
∈ [0.2, 10] — I genuinely do not know which wins at the extreme tail, and
that is the point of measuring it. Exponent of n\*_L against (1−e) steeper
than 0 (finite, shrinking), fit over e ≤ 0.99.

## P3 — random control

n\*_rand ≥ 3× n\*_corr at every e (error n² vs n³).

## P4 — belt scenes that exist in the tree

Using the tree's own constants (measured knots for crossings, 0.285
kicks/orbit from H0190 K2, compiles/kick = 1/n\*(e)):

- **B18b frozen scene** (σ = 0.07, e capped 0.6, p ∈ [2048, 2560)):
  share of compile crossings on e > 0.9 bodies = **0 exactly** (the cap
  makes P(e > 0.6) ~ 1e-16); p99/median cost ≤ 3×.
- **Encounters belt** (σ_e ≤ 0.03, e capped 0.5): share(e > 0.9) = 0;
  p99/median ≤ 2×.
- **Hot tail frozen as a rung scene** (σ = 0.3, capped 0.995): p99/median
  ∈ [3, 15], p99.9/median ∈ [20, 80], share(e > 0.9) ∈ [8, 20]%.

So: no belt scene in the tree concentrates the tail; only the hot scene
does. (If this holds, the finding takes the checker's smaller branch:
freeze a hot-tail scene before B18 certifies smoothness.)

## P5 — the criterion and its negative control (author's own proposal)

Global-rate trigger, re-anchor interval K = n\*(0.6)/2 calibrated on the
frozen scene: **fails** at e ≥ 0.95 — the epoch error crosses the floor
between anchors, by ≥ 5× at e = 0.99. Per-cycle trigger (re-anchor when the
predicted curvature error ½T″·s²ₙ crosses the floor, T″ from the compiled
periods at the anchor): holds everywhere (max error ≤ floor at every e in
the grid), at a measured recompile rate rising from ~2e-3/kick (e = 0.5) to
~4e-2/kick (e = 0.99) at EPS = 1e-7.

## P6 — scale invariance

EPS ×100 (1e-5): horizons shrink by 0.0464 (100^(−2/3)), within ±20%, at
both e = 0.5 and e = 0.99, on the integer cycles.

## P7 — crossings (compile cost per recompile)

Measured knot counts of the compiled shapes within +2 of B9's
2m·log₂((1+e)/(1−e)) + 8 (m = 16) across the grid — the belt cost model's
crossings term is the law's own, not a formula bolted on.
