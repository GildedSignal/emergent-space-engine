# predictions.md — rung r4 v2 (run 20260930-0732)

Written before the decisive 200-synodic-period runs, after setup and short (≤100 synodic) shakeouts only.

Setup decisions (mine, the rung fixes the rest): e1_0 = 0.05, ϖ1_0 = 0, λ1_0 = 0 for every case; resonant base λ2_0 = 0.0, shifted λ2_0 = 4.0 rad (w2 as a radian, the code's unit); q = 2.0 exact. In short shakes the truth librates at the base (R ≈ 0.84) and librates weakly at the shift (R ≈ 0.24); truth pumps e to ≈ 0.13 and ≈ 0.18 respectively. Controls at q = 5.00 / 2.55 barely move e (≈ 0.050); q = 2.15 stays ≈ 0.050 in the truth over 100 synodic but the arc law pumps it (≈ 0.32), i.e. spurious resonance at 7.5% detuning.

## Predictions

1. **arc-g8, arc-g16, arc-g8-half all FAIL** the behaviour criteria:
   - `e_pump_ratio_max` > 1.25 (over-pumping 2–4× on both resonant cases; the better the quadrature the harder it pumps, so arc-g16 worst);
   - `libration_ratio_min` < 0.8 (law's resonant angle circulates, R ≈ 0.03–0.10 vs truth ≈ 0.24–0.84);
   - `control_pass_fraction` < 1.0 (the q = 2.15 control fails: spurious pumping far outside the truth's envelope; q = 5.00 and 2.55 pass).
   - `e_pump_ratio_min` may still exceed 0.8 (over-pumping is still pumping).
   - `kicks_per_orbit` medians ≈ 0.5–1.2 → the cost criterion passes; `dense_steps` = 0 by construction.
2. **averaged FAILS**: no resonant pump (`e_pump_ratio_min` ≈ 0.05/0.13 ≈ 0.4 < 0.8) and no libration. It should pass the two far controls and probably also 2.15 (no spurious resonance).
3. **none FAILS** hardest: `e_pump_ratio_min` ≈ 0.4.
4. **truth-1200 PASSES** against truth-2400: pump ratios 0.99–1.01, libration ratio ≈ 0.9–1.1, controls 3/3, otherwise the criteria are unpassable (VOID guard).

## What would change my mind

If arc-g8's short-run over-pump were dominated by the 8-node quadrature (4 nodes per inner orbit), arc-g16 would fix it. The shakeouts show the opposite trend, so I predict the configuration dies honestly: first-order conjunction-window jumps cannot self-limit the resonance the way libration does in the truth.

## Verdict I expect

KILL of the arc-integrated kick configuration (windows = conjunctions or half-synodic), with the positive and negative controls healthy.
