# Predictions (written before the decisive run; the code has not been run yet)

Mirror of the frozen B18b judge (`wt/b18-belt:xtask/src/behave/belt.rs`, af07b33): SplitMix64
counter stream `at(seed, 4i+c)` through `rayleigh_grid` and the SPEC (p 27 bits over [2048,2560),
e Rayleigh sigma 0.07 on 2^30 capped 0.6, w 32, t 44). Statistics and thresholds exactly the
judge's: chi2 128x128 on (p,t) scores |z|<=4.5; serial 18 lags + cross pairs |z|<=5; per-column
KS vs an iid reference, D <= 2.470*sqrt(2/n); tails of e and p: count |z|<=4.5 with var 2K,
reach (belt max >= ref 20th largest), overshoot (belt 20th <= ref max), tail-shape two-sample
KS. Reference: numpy PCG64 (family differs from SplitMix, as the judge's xoshiro does; the
exact reference family does not matter for calibration). n = 2^20 (3 seeds) and 2^23, as RUNS.

## Calibration anchors (the judge's own claims; my mirror must reproduce them)

1. `none` (the counter stream itself) passes every statistic at both n.
2. `table12` (gold's 2^12 midpoint table) fails the tail of e at 2^20: near 0 of 105 extreme
   values, reach fails (the judge: "0 of 105 extreme e").
3. `winsor` (both columns clipped at the 1-1e-4 quantile) fails count and range.
4. `lattice` (i*g per column) fails the 2-D chi2.
5. `serial` (1/7 of odd bodies copy the neighbour's t) fails serial at lag 1.

## Held-out adversaries (not tuned on; the run decides)

6. `crush50/crush60/crush67/crush75`: e compressed toward the spec's 1e-4 quantile,
   e <- thr + f*(e-thr) for e > thr, i.e. the top 1e-4 tail's spread scaled by f. This is
   literally "averaging crushes tails" (each tail value moved a fraction 1-f toward the tail's
   floor). Prediction: crush75 passes EVERYTHING at both n (a quarter of the tail's spread
   deleted, every statistic inside its noise). crush50 passes at 2^20 but fails reach at 2^23
   (belt max = thr + 0.5*(5.6 sigma - 4.3 sigma) < ref's 20th largest there). crush60 is the
   knife edge; I do not predict its 2^23 reach verdict.
7. `innerclip`: p clipped from BELOW at its 1e-4 quantile (a hollow inner edge, 10x coarser
   than the tail the row protects; low p is the game-critical side: deepest dippers, handoffs,
   the changeover). Prediction: passes EVERYTHING at both n, including per-column KS
   (CDF shift 1e-4 << 0.0035 critical).
8. `aligned`: the top 1e-4 of e (105 bodies at 2^20) have omega confined to 1/32 of the circle
   (a sculpted stream: every deep dipper dives the same corridor). Prediction: passes
   EVERYTHING at both n (KS on omega sees <= 1e-4; cross-pair z ~ 0.1; chi2 is on (p,t) only).
9. `fattable` (paper, no run): a one-level quantile table with 2^20 cells (4 MB), a legitimate
   dyadic table one level deep, tail resolved to 2^-20, passes every statistic; info declared
   4 MB, birth charge 4 MB: PASSES criterion (4) as written (<= 2 x info + 2), 256x the gold's
   bytes, not growing with n. The judge's own doc admits this; I make it concrete and add the
   disposition.

## What would count as the premise surviving

If crush75 or innerclip or aligned FAILS some statistic, the row is stronger than I claim and
the finding is the measured power boundary instead. The anchors failing to reproduce would
void the mirror (then the Rust judge's own ignored test is the fallback evidence).
