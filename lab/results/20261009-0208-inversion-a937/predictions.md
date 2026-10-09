# Predictions — 20261009-0208-inversion-a937 (written before running retro/polar)

Tuned on: nothing. The code was smoke-tested and its instrument adjudicated on
the control scenes only (phalanx, incl-node — the gold's home regime, where it
reproduces the gold: ring-rank <= 3, zero misses, brute adjudication 150/150
true and 150/150 false on phalanx, 144/150 false on incl-node). The two scenes
below have not been run. ρ = 1e-4, k = 4, a = 1, e = 0, Binet clump
diameter 0 (the adopted dimensionless trigger fires in every scene).

## S1 `retro` — one circle, 500 prograde + 500 retrograde, uniform phase

1. True encounters: every cross-sense pair meets twice per orbit (they are on
   the same circle head-on): 250,000 pairs, 10,000,000 pair-events over 20
   orbits. Same-sense pairs: 0 (constant separation).
2. Rank of partner just outside contact: small (longitudes converge to the
   meeting point); predict frac rank > k at best cadence < 1% — the watch SET
   is not the problem here.
3. Maintenance: every cross pair's longitude difference wraps twice per orbit,
   so overtakes (order changes) = 2 · 500 · 500 = 500,000 per orbit = O(n²),
   versus ~0 for the prograde control. Zero misses requires watching at the
   crossing rate, not at O(n·k); predict frac missed at the fixed 8-evals-per-
   orbit grid >= 90%.
4. If instead overtakes <= 10 · n·k per orbit, there is no economics kill.

## S2 `polar` — i = 90°, node uniform in [0, π), all prograde, n = 1500

5. True encounters: syncs at the two shared poles. Predict O(10³) encounter
   pairs over 20 orbits (rate ≈ 2ρ/(π·v_rel) per pair per orbit, E[1/v_rel]
   ≈ (1/π) ln(π/spacing) ≈ 2.3 → ≈ 1.5e-4 per pair per orbit → ≈ 3,000).
6. Ring-rank of the partner at the contact flanks: a polar body's longitude is
   piecewise constant (azimuth of its meridian plane, Ω or Ω+π), so partners
   converging on the pole keep longitude difference ≈ ΔΩ ~ uniform. Predict
   median rank ~ n/4 ≈ 375, p90 > 500, fraction with rank > k >= 95% —
   missed at ANY cadence (the watch set never contains the partner).
7. The gold's own statistic — 3D distance-rank of the partner at closest
   approach — predicts <= 4 for >= 99% (the partner is within ρ, everything
   else is ~42ρ away): the evidence metric holds while the certificate is
   blind. If dist-rank <= 4 holds for < 90%, my reading of the gold's
   evidence is wrong.
8. Overtakes per orbit: each body's longitude jumps by π at each pole passage
   (2 per orbit), displacing it ~n/2 ring positions: predict ≈ 2 · n · n/2 ≈
   2.25M order changes per orbit — the train is not even quasi-static in λ.

## Kill criteria (pre-registered)

- The train certificate survives inversion if S2 misses <= 5% at any cadence,
  or if S1's zero-miss maintenance is <= 10 × O(n·k) per orbit.
- A confirmed break: S2 miss fraction >= 90% with the trigger engaged, or
  S1 overtakes growing as ~2·n_p·n_r (quadratic) — either falsifies
  "a phase-neighbour certificate at O(n·k) replaces the quadratic tier"
  as stated, because the dimensionless trigger (Binet clump) cannot
  distinguish these scenes from a co-moving formation.
