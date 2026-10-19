# Predictions (written before the decisive runs)

Second-author run on 20261018-2312-dynamics-84b2 (silver). The checker's named
experiment for gold: fly n = 12800 at horizon ∝ side (≥ 24576) to extinction with
late-window m as the statistic; fix the stale record cells. Setup identical to 84b2's
ladder: shipped `Chronon` + `Law::RelativisticV1`, Q = 2²⁰, `worlds::gas` genesis
(bit-identical, verified on n = 400), fill 0.7, vmax 2¹⁶, burn 1024, seeds 1-3,
**horizon 24576** (side 240; 24576/240 = 102 side-units vs 6400's 48 — 2.1× the
horizon at which 6400 reached baseline). The binary is the same prebuilt target the
original regen used; crates unchanged since base 8d9e7f88 (diff empty), and my n=400
seed-1 arm is byte-identical to 84b2's `lad_n400_s1.csv`.

**Instrument (fixed before the runs, calibrated on 84b2's committed data).**
`late-m` = relstd of 64-chronon window sums over the last 4096 post-burn chronons.
Calibration reads: 6400 seeds 1-3 → 0.85/0.87/0.65% (the "steady state ~0.6%" the
checker quoted); the checker's own 12800 horizon-8192 arm (`chk/a_n12800_s1.csv`) →
m_whole 3.43%, F64 164.03, F1 3.33, b0max/p50 1.109, p99/p50 1.131 — all exactly
their numbers. Baseline F64 band from every flown arm's dead blocks: 1.3-5.2.

- **P1 (extinction — the gold-deciding half).** At n = 12800, seeds 1-3: the block-F64
  series (2048-chronon blocks) decays monotonically-ish to the anti-bunched baseline:
  **the final three blocks all read F64 ≤ 6 and late-4096 m ≤ 1.0% on every seed**
  (6400's band 0.65-0.87%; predict 0.6-1.0%, i.e. within ±50% of the 6400 steady
  state). Kill line for the transient reading: any seed with late-m ≥ 1.5%, or a
  plateau (last three blocks all ≥ 8 within ±20% of each other, no downward trend) —
  that is an attractor at scale, the ringdown reading fails at 12800, and the deletion
  of batch-shaping machinery dies with it.
- **P2 (extinction time ∝ side).** The first 2048-block with F64 ≤ 6 starts at
  t ≈ 7000-13500 post-burn (6400 reached baseline in block 3 = 6144-8192, ×240/170
  → 8700-11600, ±seed scatter). If blocks 1-8 (t ≤ 16384) all read > 6, lifetime grows
  faster than side and the fixed-8192-horizon instrument can never see the 12800
  steady state — the deletion claim then holds only where extinction is demonstrated.
- **P3 (calibration, not a prediction).** 6400's steady-state modulation is 0.65-0.87%
  (late-m), not the 2.35-2.52% whole-run figures — the original dossier understated
  the steady state's flatness; my dossier quotes both.
- **P4 (the 1.4→2.4→3.4% whole-run m trend is a horizon artifact).** On truncated
  horizons of the same 12800 series: m_whole falls from 3.43% (H = 8192, the
  checker's reading) through ≈ 2.0-2.6% at H = 12288 (the side-scaled 6400
  equivalent, vs 6400's 2.35-2.52%) to **≤ 1.6% at H = 24576**. If m_whole(24576)
  ≥ 2.4%, the modulation does not die with the ringdown and the bounded-modulation
  deletion fails at 12800.
- **P5 (allocator ratios flat in the late window).** At 12800: late-8192 per-chronon
  p99/p50 ≤ 1.19 and late per-64-window max/p50 ≤ 1.12 (whole-run with ringdown:
  1.131/1.109). If late max/p50 > 1.25, steady-state bunching persists and the
  deletion fails.

Record-cell fixes (analysis only, from regenerated arms — no prediction): the 6400
ladder row to its 3-seed values (F64 38.18-43.77, m 2.42%), poly_r to F64 17.26 /
m 2.26% / mean64 33798, T range 4.8-7.9·side, and regen.sh now contains the 12800 arm.

Kill lines are stated above; a kill kills the configuration (deletion of batch-shaping
at n = 12800), never the method. No gate, crate or `main` is touched.
