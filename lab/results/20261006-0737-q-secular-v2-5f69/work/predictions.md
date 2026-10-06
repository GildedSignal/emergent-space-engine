# Predictions — run 20261005-2231-q-secular-008e (R2: secular phasors)

Written BEFORE the decisive experiment, per the lab README. The selector, scene,
estimators and kill arithmetic below are frozen. Nothing here was tuned on the truth
run (it has not run yet). The selector was computed only from the planets' (mu, a, e).

## Frozen scene

Sun (GM = 1) + Jupiter (a=5.2026, e=0.0484, mu=9.54e-4, varpi=0.8) + Saturn
(a=9.537, e=0.0539, mu=2.858e-4, varpi=2.1), mutually interacting (heliocentric
Wisdom-Holman: per-body Kepler drift, midpoint kick with direct + indirect terms).
1,024 belt test bodies: a ~ U[2.0, 3.3], e_free ~ U[0.02, 0.23], beta ~ U, M0 ~ U,
constructed z(0) = z_forced(a) + e_free exp(i beta); beta redrawn while |z(0)| > 0.25.
T = 2,000 Jupiter orbits = 149,000 time units (~23.7 kyr). Seed 20261005.

## Frozen laws

1. **LL**: first-order Laplace-Lagrange, exact Laplace coefficients, driven by the
   planets' mutual LL modes (g5 = 2.92"/yr, g6 = 14.44"/yr, computed before the run).
   z(t) = z_f(t) + (z0 - zf) e^{i A t}, A = sum_P n mu_P alpha^2 b^{(1)}_{3/2}/4.
2. **Rings**: exact double averaging (Gauss rings): quadrature over both mean anomalies
   (16 x 12 midpoint grid per planet), averaged Lagrange rates for (e, varpi) by central
   differences of <R>, RK4 at dt = 400, planets on their LL-mode ellipses, a invariant.
3. **Kick law (the plane's)**: the same WH as truth at h = P(2.0 AU)/64 = 0.278 —
   a single global step giving every body >= 64 kicks per orbit (conservative against
   the plane's per-body 64; accuracy measured at the design cadence).
   Truth: WH at h = 0.0625; convergence run at h = 0.125 (p2 used 0.25/0.125).

## Frozen selector (see selector.py)

Admit iff: MMR distance |n/n_P - p/q|/(p/q) >= 2 * C_order(k) sqrt(mu_P) e_eff^{k/2},
all reduced p/q with q <= 7, |p-q| <= 7; C = {1: 1.5, 2: 2.2, 3: 3.5, 4: 3.2}, else 2.2;
e_eff = max(e_free, |zf(a)|, 0.02). Secular guard |A - g_k| >= 2|B_k| (never binds here:
A(a) = 26-107"/yr > g6 = 14.4"/yr). Linearity |zf| + e_free <= 0.35; Hill >= 3 R_H.
Expected admission on the frozen scene: **0.80 +/- 0.03** (from the (a, e) grid map,
0.93 at e=0.02 falling to 0.63 at e=0.23). 17 MMRs in range; widest zones: 2:1J (3.28),
3:1J (2.50), 5:2J (2.82), 4:1J (2.07).

## Frozen estimators and kill arithmetic

Amendment 1 (before any WH run started): truth h = 0.09375, convergence h = 0.1875,
to fit the shared runner's time budget; the rings law runs 24 x 16 grids
with RK4 dt = T/384 (grid and step re-tuned only against analytic LL at low e and
quadrature self-convergence, never against truth). The convergence pair still brackets
truth from above; expected truth discretization error ~3e-4 in z over the run (p2's
1.25e-4 at 161 J-orbits on the (0.25, 0.125) pair, scaled), far below 10%-of-amp = 2e-3.

Amendment 2 (after a silent process kill on the shared runner, before the decisive
truth run completed): truth h = 0.125 (1,192,179 steps, dyadic, T unchanged); the
survived h = 0.1875 run is the convergence partner; expected truth error <= 6e-4.

z_bar = boxcar mean of z over one synodic period (vs Jupiter), samples every dt = 3.
amp = e_free (by construction, >= 0.02 for every body).
g_hat = linear fit of unwrapped arg(z_bar - zf_LL) over samples with |z_bar - zf| > amp/3.
rate_err = |g_hat_law - g_hat_truth| / g_hat_truth.
evec_err = max_t |z_bar_truth(t) - z_law(t)| / amp (laws started at the constructed z(0)).
PASS_body(L) = rate_err <= 0.05 AND evec_err <= 0.10.
Fraction(L) = |admitted AND PASS| / 1024. Primary law for the kill rule: **rings**
(the stronger phasor variant; LL is the cheap variant and is reported too — the memo
itself prescribes both).
KILL R2 if Fraction(rings) < 0.50, or if any admitted body was inside a resonance's
width (checked from the run-averaged <a>, since the osculating n differs from a^{-3/2}
by O(mu) short-period terms, comparable to the narrow high-order widths).

## Predictions (held-out cases are those the selector and laws were not tuned on)

1. Admission fraction: 0.77-0.83.
2. Truth convergence: max |z(h=0.125) - z(h=0.0625)| = (3e-4, 2e-3) over the run
   (p2 had 1.25e-4 at 161 J-orbits on the coarser pair; error grows about linearly in T).
3. **LL** (held-out: the whole outer belt and Saturn's coupling): rate within 5% for
   admitted bodies with a <~ 2.75 (alpha_J <~ 0.53); rate error 10-60% beyond ~2.9 AU
   (p2 measured 16-65% at 3.05-3.15 with Jupiter alone). Prediction: Fraction(LL) =
   0.45-0.65 — LL alone likely FAILS the 50% bar; its failure mode is a deterministic
   phase drift (wrong A), the same error type as the compiler's period error.
4. **Rings** (held-out: a in [3.2, 3.3] with alpha = 0.63, e = 0.23, and bodies with
   MMR distance ratio delta/W in [1, 3]): rate within 5% and e-vector within 10% for
   >= 90% of admitted bodies. Expected failures: a few bodies with delta/W < 2 whose
   chaotic diffusion the width model underestimates, and possibly the alpha = 0.63
   corner where the 16x12 grid and the LL-driven planets are weakest.
   Prediction: Fraction(rings) = 0.70-0.78 → **R2 survives**.
5. No admitted body ends inside a resonance width measured from <a>; if some do
   (narrow high-order), they show it by truth e-pumping: max|z_bar| > |zf| + e_free + 0.05.
6. Kick law reproduces the 3:1 and 5:2 depletion signature: truth's max|z_bar| map vs a
   shows pumping in both zones; kick law's map agrees (which bodies pumped), trajectory
   agreement for pumped bodies decorrelates in phase but the zone statistics (fraction
   above 2x initial e) agree within ~20%. The kick law's NON-resonant bodies carry the
   plane's discretization error: median |z_kick - z_truth| ~ 1e-3 (64/orbit vs truth).
7. Bytes per body after the run: phasor laws keep the belt program valid (proper
   elements are the program's own columns; the phase advances by exact additions):
   0.126 bits/body (H0218) + O(1) per-doll mode table. The kick law breaks the program
   at each body's first kick: every body carries a scar = tube (16 B) + binding residual
   (4 x i128 = 64 B) + Elias-Fano index (~2 B) ≈ 82 B/body. Ratio ≈ 5,000x.

## What would make R2 wrong here

- If Fraction(rings) < 0.5: the phasor domain is too small to matter at belt scale.
- If admitted bodies pump in truth: the selector leaks; kappa_M = 2 is not enough.
- If the e-vector errors grow superlinearly in T (resonant leakage): the wrong error
  type (compounding), principle 13.
