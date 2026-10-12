# Predictions (written before the decisive runs)

Second author on 20261012-1117-redteam-4808. The checker's named experiment to
gold: "measure the rate at which encounters/scatters park bodies in the danger
band (p − p_crit(e) ≲ 0.3, where gain > 5): a toy scatter experiment around one
mass, counting final p margins — plus the named rung criterion (kick train at
p → p_crit⁺, apsidal-drift budget per 10³ orbits) frozen before it."

Everything below is frozen before any scatter/gate script runs. Units: G = M = c
= 1 (Schwarzschild), p and e are Darwin parameters from the turning points,
p_crit(e) = 6 + 2e, margin μ = p − p_crit(e).

## The frozen gate (rung text, B-gate style)

**B-sep (near-separatrix kick trains).** On bound Schwarzschild orbits with
e ∈ {0.5, 0.9, 0.99} at margin μ = p − p_crit ∈ {2, 1, 0.3, 0.1, 0.03}: a train
of 10³ kicks, each δL/L = 10⁻⁴, applied at periapsis (the tangential-kick
family; periapsis stays a turning point), signs alternating (zero mean — the
friendliest case). The cycle is updated by the multiply-add (stored Δφ and
∂Δφ/∂L updated each kick) and judged against exact GR:

- **Budget A (the law's own floor, per kick):** |residual per kick| ≤ 10⁻⁶·Δφ_cycle
  — the `space-darwin16-v1` compile's error scale (law.md:3).
- **Budget B (player-visible, per 10³ kicks):** |accumulated apsidal drift| ≤
  5×10⁻³ rad (~1 pixel of periapsis direction on screen).

Verdict rule: the multiply-add's domain is safe at a (e, μ) point iff both
budgets hold. **B-sep FAILS the multiply-add if budgets fail at μ ≤ 0.3 for any
e tested.** Controls: the positive control is μ = 2 (weak field: prior run
measured gain 1.7 there, both budgets must hold); the negative is μ = 0.03.

## P1 — the kick train against the frozen budgets

The prior run measured gain 1.7 → 8.6 and residual +9.6e−7 → +3.4e−5 rad/kick
for μ: 2.2 → 0.21 at e = 0.9, and the checker extended: gain 5.9–12.7 at
μ = 0.3 for e 0.5–0.99.

Prediction: **Budget A holds at μ ≥ 1 for all e, fails at μ ≤ 0.3 for all e
(residual ≥ ~3× the floor there). Budget B fails at μ ≤ 0.3 for all e**
(accumulated drift over 10³ kicks ≥ 1×10⁻² rad, i.e. ≥ 2 pixels), and holds at
μ ≥ 1. The failure is by type, not just size: the residual keeps one sign under
alternating kick signs, so it accrues linearly at any kick size (δL² scaling
only sets the rate).

**Re-anchor control (law.md "Not adopted" entry):** the shipped rule recompiles
when the accumulated offset reaches √(floor/C) — from its own numbers
(1e−6 floor passed after ~730 correlated quantum kicks, error ∝ drift²) the
trigger sits at ~730 kick quanta of accumulated offset. Prediction: under
alternating signs the offset never exceeds one quantum, so the rule never fires
(gap ≥ 10²) while the phase error still accrues linearly; under random signs it
fires only after ~5×10⁵ kicks, by which time the accrued drift is already ~10
rad, and a recompile does not reset accrued phase (it recomputes Δφ, not the
body's already-advanced angle). The shipped rule does not bound this error.

## P2 — the scatter experiment: does anything park bodies in the band?

Toy: incoming parabolic bodies (E = 1) with periapsis r_p drawn uniform in a
window near the hole; one impulsive encounter at periapsis, local velocity kick
of magnitude k·v_p (v_p = √(2/r_p), the local parabolic periapsis speed — the
GR-exact map from local velocity to (E, L) is used), direction uniform in 2D.
Fates: plunge (μ ≤ 0 or no bound turning points), **band (0 < μ ≤ 0.3)**, bound
wider (μ > 0.3), still unbound (E ≥ 1). "Captured" = bound after the kick.

Geometry (linear analysis, frozen as prediction, not fitted): a tangential
retro kick at periapsis preserves r_p, so μ ≈ L²(1 − 2/r_p) − 4 after capture;
a parabolic orbit has μ₀ = 2r_p − 8, so **every capture at r_p ∈ [4, 4.15] is
born inside the band**, and captures at larger r_p enter it only for a tuned
kick size (~0.3–1% of v_p tangential at r_p ≈ 4.5, larger kicks plunge).

Predictions, as thresholds frozen before the run:
- Among captured bodies with r_p ∈ [4, 8] and k = 10⁻³·v_p, the band fraction is
  **≥ 5%** (dominated by r_p ∈ [4, 4.15] plus the tuned tail); call the band
  "commonly populated" if ≥ 5% of captures land in it over a contiguous range
  k ∈ [10⁻⁴, 10⁻²]·v_p, "dormant" if < 1% everywhere.
- The plunge fraction among all bodies rises from < 1% at k = 10⁻⁴ to > 30% at
  k ≥ 10⁻¹ (captured bodies kicked past the separatrix).
- Band captures have e ≥ 0.8 (near-parabolic captures), so they sit where the
  checker's universality measurement puts gain ≥ 5 at μ = 0.3.

If the measured band fraction is < 1% everywhere, the honest verdict is the
dormant branch: the hole is real but the band is not fed; the claim's "normal
output of a battle" premise would be refuted.

## P3 — linger: residence time and accrual inside the band

Bodies seeded in the band (as captures put them there), kicked at δL/L = 10⁻⁴
with random signs (zero mean), absorbed at μ ≤ 0 (plunge) or μ > 3 (out).

Prediction: mean residence **≥ 10³ kicks** (the band is 0.3 wide and the margin
step per kick is ~|∂μ/∂L|·δL ≈ 10⁻³, so crossing takes ~(0.3/10⁻³)² ≈ 10⁵ kicks;
even with the escape side nearer, ≥ 10³), and the multiply-add drift accrued
while resident is **≥ 5×10⁻³ rad** (residence × per-kick residual ≥ 10³ ×
~10⁻⁵ rad). Bodies linger, and the error grows to player-visible size inside
the band before any plunge.

## What would make me wrong

- P1: if the alternating-sign residual changes sign with kick sign (not
  quadratic), budgets survive at fixed μ — the prior run says it will not.
- P2: if the GR-exact map spreads captures so thin that the band holds < 1% of
  captures at every (r_p window, k), the hole is dormant and the claim's
  population premise falls.
- P3: if the margin walk is biased out of the band fast (μ drifts upward
  geometrically), residence could be ~1 kick; then accrual never matters.
