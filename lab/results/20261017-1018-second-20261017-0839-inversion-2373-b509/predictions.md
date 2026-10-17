# Predictions — 20261017-1018-second (calendar gold experiment)

Written before the decisive run. Fitted only on pilot seed 7 (two pilots, /tmp/pilot7*.jsonl).
Decisive seed: 20261017 (the original run's own seed); held-out check seed 777.
The instrument: `fleetcal.rs` (print-only example; work/patch.diff). Population generator
identical to fleetk's, so keys/train rows are comparable with the original run.

Held-out cases (not tuned on): every band below is for a seed I have not run; the σ_e=1e-3
arm, the recurrence-based steady rate, the 8-interval-horizon exact price, cap_us, and the
kickrow flip counts are new instruments never used in fitting anything before.

| id | band | prediction (seed 20261017) |
|---|---|---|
| P1 | carm arm_us_per_pair | [0.90, 1.40] µs |
| P2 | carm exact_us_per_pair (H = 1 interval) | [45, 80] µs |
| P3 | carm exact8/exact ratio | [5, 9] |
| P4 | carm fire_us_per_armed_iv (keys, H_iv) | [2e4, 4.5e4] µs (the perpetual-pair pathology) |
| P5 | calkeys armed F=1e3 / 1e4 / 1e5 | [40, 75] / [3.8e3, 6.0e3] / [3.5e5, 6.0e5] |
| P6 | calkeys armed at σ_e=1e-3, F=1e4 vs σ_e=1e-2 | within ×1.5 (armed is ρ-driven, σ_e-independent) — the held-out structural claim |
| P7 | calkeys cap_us_per_armed_period | [4, 15] µs (one-period capability is cheap) |
| P8 | caltrain armed F=1e4 / 1e5 (da=1e-4) | [7.5e6, 1.1e7] / [7.5e8, 1.2e9] |
| P9 | caltrain refused at da=1e-3, F=1e4 | yes (reach ≈ 21 ≥ π) — deterministic |
| P10 | caltrain firings_steady_per_iv F=1e4 (recurrence-based) | [0.6, 1.3]× firings_iv0 (a stationary rotation flow: steady ≈ iv0 rate) |
| P11 | caltrain fire_us_per_armed_iv | [10, 40] µs |
| P12 | truth dropped/added (keys and train) | 0 / 0 (calendar soundness; control) |
| P13 | negctl drops: safety 0.9 / 0.5 / reach 0.5 | > 0 each; [800, 1800] / [4e3, 8e3] / [30, 250] |
| P14 | keysev exponent on (1600, 6400) | γ ∈ [1.8, 2.2]; F=400 events ∈ [2, 60] (Poisson, volatile) |
| P15 | kickrow keys eps=2⁻²³ fire_per_kick | [10, 30]; ddue_med = 0.0000 |
| P16 | kickrow train row_mean | [6.5e3, 8.0e3]; ddue_med ∈ [0.01, 0.1] iv at eps=2⁻²³ |

Kill criteria (pre-registered):
- K1: truth drops > 0 at SAFETY = 1.1 on either population → the calendar is unsound as a
  contact finder → report the refutation (this kills the fix, not the method).
- K2: any negctl arm shows 0 drops → the drop-counter cannot detect an unsound certificate
  → the instrument is broken (VOID).
- K3: P6 fails by > ×3 → the calendar's armed set is σ_e-driven after all → the F*(σ_e)
  story changes; report which.
- K4: P10 off by > ×3 → the steady-rate model (recurrence ≈ iv0 rate) is wrong; use the
  measured recurrence, restate the floor, and say the histogram interpretation died.

What I expect the composition to show (the claim, stated before the run):
the calendar deletes the sweep term (57× per pair, lifetime-amortized) and moves the keys
fleet ceiling F* from ~100 (sweep) to ~10³ at L ≥ 25 intervals amortization, but the train
conjunction flow (firings ∝ F²·da) and the kick-created conjunctions keep F ≤ ~10³ at φ = 1
whatever the certificate: the missing ledger row closes as a population constraint, with
numbers.
