# Predictions — inversion of gold 20261006-0346-taleb-09b5 (the train certificate)

Written before any run of S1/S2/S3. The gold measured **distance-rank** of the encounter
partner at closest approach (max 4, 234/234 encounters) but its adoption is a **longitude
train**: sort by mean longitude, watch k≈4 neighbours, rebuild on overtakes. These are
different quantities whenever phase-order ≠ spatial order. Untested axes named by the gold
itself: e-spread ≫ ρ (radial breathing), orbit crossings (ϖ spread), resonance.

Scenes (2D Kepler, a≈1, ρ=1e-4, n=a^-1.5, all positions analytic):
- **S0 control** (the gold's fleet, seed-style: nc=200, a_hw=1e-5, e~Rayleigh(1e-3) trunc 0.01,
  ϖ0±0.1, λ Gaussian σ_λ=0.01, 10 orbits).
- **S1 pinwheel debris** (the battle-aftermath scene): nc=400, a_hw=1e-5, e=0.05 common
  (+Rayleigh jitter 1e-3), ϖ ~ U(0,2π), λ0 ~ U(0,2π), 20 orbits. Every pair's orbits cross;
  encounters are crossing coincidences, found analytically (crossing points, pass-time beats,
  linearized impact geometry).
- **S2 jam sweep**: the gold's fleet with σ_λ ∈ {3e-3, 1e-3, 5e-4, 3e-4} (local along-track
  spacing from ~ρ down to ~0.1ρ; the board's own scenario is "one 10⁶-ship fleet in one cell").

Metrics per scene: partner **distance-rank** (the gold's instrument, min over both
directions), partner **λ-rank** (|index gap| in mean-longitude sort at encounter time — what
the train watches), watch misses at k=4, λ-order swaps over the horizon (rebuild frequency).

## Pre-registered expectations

- **P1 (S0 control)**: distance-rank max ≤ 4 (reproduces the gold), λ-rank max ≤ 4, watch k=4
  catches ~100%. If this fails, my instrument is wrong, not the gold — fix before anything.
- **P2 (S1 debris)**: distance-rank stays small (median 1, max ≤ 4) — the gold's instrument
  PASSES — while λ-rank blows up (median ≥ 8, tail ≥ 20, growing with nc) and the k=4 watch
  misses most encounters (>50%). λ-order swaps over 20 orbits ≈ 0–50 fleet-wide (a_hw=1e-5 ⇒
  almost no overtakes ⇒ the watch order is frozen). Instrument/ adoption divergence of the
  memo-artifact class: the measurement cannot vet what is shipped.
- **P3 (S2 jam)**: distance-rank ≈ number of ships within ρ (a local-density statement, not a
  constant): at spacing ≲ ρ the median rank crosses 4 and the k=4 watch starts missing
  encounters; k is not a constant but ρ² × local density.
- **P4 (Binet diameter)**: S1/S0 max-pairwise Binet diameter ratio ≥ 100. Wherever eps_u sits,
  one horn is unguarded: eps_u large ⇒ train triggers on debris and misses encounters
  (correctness hole); eps_u small ⇒ debris falls to the quadratic pairwise tier and the gold's
  own ruin arithmetic (≈40 TB, ~core-years of setup at 10⁶ ships) stands for battle debris.

## Kill criteria for my inversion
- S1 λ-rank ≤ 4 AND watch k=4 catches ≥ 95% ⇒ the certificate is sturdier than the gold
  claimed; my inversion fails and I report that.
- S2 shows no rank inflation at spacing 0.1ρ ⇒ density story wrong; report.
