# Predictions — second-author run on 20261010-2314-taleb-6baf

Written before any run of `hlive2.py` / `hlive_big.py`. Tuned on nothing: the only
inputs are the original run's stored numbers, the checker's three probe numbers
(stride-2 smoothed med 10.85, p99 28.01; po=1200 fit 1.005), and analytic estimates.
The instruments: naive key-crossing counter sampled **every step** (ceiling
129.5 events/P_p, vs 32.38 in the shipped code); smoothed secular counter at
SM_STRIDE=1, SM_W=1024 (same 1024-step ≈ 7.9 P_p window, ceiling 129.5, vs 16.2
shipped), rolling-sum implementation; tail statistics computed **on the smoothed
counter** (the shipped top-1% came from the saturated naive counter); entropy by
k-NN (Kozachenko–Leonenko) differential entropy on (a, L) in sim units.

## Registered predictions

P1 (naive mechanism, 1/q sweep not synodic count): at stride 1, the naive
median crossing rate scales with grid refinement: ratio bits16/bits12 ∈ [10, 18]
and bits12/bits8 ∈ [10, 18]; bits16 median lands in [40, 120] (below the
129.5 ceiling, i.e. unsaturated). If bits16 pins at the ceiling I report it as
a lower bound and the mechanism is still decided by the 8→12 ratio.

P2 (smoothed median stable): smoothed (stride 1) median ∈ [9, 14] events/ship/P_p
— agreeing with the checker's stride-2 probe (10.85) within 20% — and cumulative
growth exponent ∈ [0.98, 1.10] (linear, permanent churn) on all 3 belt seeds.

P3 (fat tail vindicated): on the unsaturated smoothed counter, p99/median ≥ 2.0
and max/median ≥ 2.4 on all 3 belt seeds; top-1% share (smoothed) ≥ 2.5%
(vs 0.96% from the saturated counter).

P4 (tail structure): the tail is structured, not uniform: either (a) the top-1%
churners' birth eccentricities exceed 1.5× the fleet median, or (b) they
concentrate in ≤ 2 of the 5 a-bands (≥ 45% of top churners in two bands vs 40%
if uniform). At least one of (a), (b) holds.

P5 (entropy, k-NN k=8 on standardized-scaled but raw-unit (a,L)): h_birth ∈
[−3.0, −1.0] bits (support ≈ 1.5 × ~0.05, thin L-ridge); h_mature(300 P_p) −
h_birth ≥ +0.3 bits; h(1200) − h(300) = 0.5·log2(4) = +1.0 ± 0.5 bits
(diffusive L-spreading: linear churn ⇒ σ_L ∝ √t).

P6 (estimator scales with N): k-NN h on the N=10⁶ sample minus k-NN h on a
4000-ship subsample of the same run, both at 100 P_p, agrees within ±0.3 bits
(no log2(N) pin). Plug-in at bits 8 (65 536 cells ≪ N) converges and matches
k-NN h + log2(1/(qA·qL)) = h + 12.12 within 1.5 bits at maturity.

P7 (plug-in still pins at 2²⁰ on fine grids — sharpening the checker's
prescription): plug-in on the 10⁶ ship sample at bits 16 reads ≈ log2(10⁶) +
0.72 = 20.7 bits, indistinguishable from an iid null, because effective
occupancy (~10⁷ cells) ≫ N. So the scalable instrument is k-NN (+ analytic
grid offset), not plug-in at 2²⁰ at the operational grid.

P8 (bandwidth, arithmetic on measured numbers): with smoothed median ~11 and
p99 ~28 events/ship/P_p, P_p = 1.6^1.5 = 2.024 yr, 10⁹ ships, RTF 100
(1 game-year = 3.156×10⁵ wall-s): median ≈ 1.5–2.0×10⁴ events/wall-s, p99-all
≈ 4–5×10⁴ — about 10⁴× below the dossier's "2–4×10⁸".

## What I do not re-predict (regenerated from shipped code, already measured)

Half-life 0.077 P_p at 12/16 bits; μ=0 controls; deadband killing the control's
roundoff tail; ring/off-ring contrast absent at ≤ 1200 P_p. These regenerate in
the 9-run record rebuilt from `hlive.py` + `analyze.py`.

## Kill criteria for the restated claim

- If P1 fails with ratios ≈ 2–3 (not 10–18), the naive rate is drift-bound, not
  sweep-bound: restated claim keeps the drift reading.
- If P3 fails (p99/med < 2 at stride 1 over 3 seeds), the checker's stride-2
  tail is an instrument artifact and "uniform flood" stands; I would report that.
- If P5's h(1200)−h(300) ≤ 0, the mature footprint does not decompress and the
  entropy part of the claim reduces to "floor unmeasured, estimator pinned".
