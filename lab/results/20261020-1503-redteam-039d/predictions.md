# Predictions — 20261020-1503-redteam-039d (written before the decisive run)

Target: representation-premises open direction 5, "strong-field occlusion near the photon
sphere (e59e's rim domain) — unmeasured". The letter's occlusion mechanism pair: the gather
with memoized deflection(b) (L57) × the per-row worldtube chord predicate (22d1's measured
cure, "judged in the observer's frame"). Instrument: exact 2D Schwarzschild null geodesics
(quadrature + bisection), controls below. Units M = 1; sky = circle.

Cases are chosen blind to tuning: r_o ∈ {20, 6, 4, 3.2}M (3.2M is one-thirtieth outside the
photon sphere), emitter rings r_e ∈ {30, 6.5, 3.5}M, 720 azimuths each, wraps to k ≤ 3.

## P1 — the chord predicate wrongly blocks near-side emitters against the shadow
For emitters with r_e < r_o (between observer and hole), the served row's flat-chord impact
is b·√f_o; the worldtube law blocks it when that is < 2M, although its geodesic is real and
visible (it escapes outward; only b_row > b_c is capture). Predicted wrongly-blocked
fraction of near-side azimuths: 15–45% at r_o = 3.2M, r_e = 3.5M, falling roughly as
(2M/√f_o)/b_span; nonzero (> 2%) at every r_o ≤ 6M.

## P2 — the naive-bearing composition fabricates the capture annulus
If occlusion is tested on the emitter's bearing instead of the served image (the cheaper
composition), the fabricated far-side fraction (predicate visible, truly captured) at
r_e = 30M ≈ (α_sh − α_chord)/π: ≈ 16% of the sky circle at r_o = 6M (e59e measured the
25% = α_sh/π half with no occlusion at all), rising to ≈ 34% at r_o = 3.2M. The shadow
radius is 3√3/2 = 2.598× the horizon silhouette at every distance — a fixed structural
factor, not a size error.

## P3 — image counts at the rim
Mean images per emitter at r_o = 3.2M, r_e = 3.5M ≥ 4 (6eae measured 4 at far emitters);
near-side rings add the direct branch. At r_o = 20M, r_e = 30M: exactly 2 (primary + k=0).

## P4 — the memo's rim wall
To place the last wrapped image within a display pixel (1e-3 rad), the needed relative
b-resolution near b_c is finer than 1e-6 (predict 1e-7…1e-9), i.e. beyond any 12+12-bit
memo key; each extra wrap costs a fixed factor in resolution (exponential bunching).

## P5 — the deletion cure (control)
For the hole itself the correct occlusion law is NO test: served rows have b > b_c by
construction (their geodesics escaped), so the shadow is emergent absence and the worldtube
test must be deleted for horizon occluders. Predicted misclassification of the deletion
cure: 0 everywhere (this is the positive control; it cannot fail without an instrument bug).

## Controls
- Positive (must pass): the solver reproduces the closed-form shadow angle
  sin α_sh = 3√3·√f_o/r_o to < 1e-9 at every r_o; weak-field deflection of a b = 10⁴M ray
  to 4M/b within 1e-6 relative.
- Negative (must fail): the chord predicate at r_o = 6M, r_e = 3.5M misclassifies ≥ 2% of
  near-side azimuths (if it passes, my instrument is broken).

## What would make this wrong
If near-side visibility at b < b_c is wrong (photons emitted at r_e ∈ (2M, 3M) inside part
of the "shadow" cone do reach r_o only within an escape cone narrower than my monotone
branch assumes), the wrongly-blocked numbers shrink but the structural factor (P2's 2.598)
and the rim wall stand on their own. The quadrature's logarithmic tail near b_c is capped at
b_c(1+1e-6); if the controls hold to 1e-9 the cap is innocent.
