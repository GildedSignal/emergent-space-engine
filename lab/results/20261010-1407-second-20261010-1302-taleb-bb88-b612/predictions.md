# Predictions — run 20261010-1407-second-...-b612 (second author, taleb bb88)

Written before the decisive grid. Pilot used only measured territory: famA(0.9, seed 11)
(original run + checker both measured it; my instrument reproduces their numbers
bit-for-bit: 18850 pairs, enc 12.5667, max M-rank 15).

## The claim under test (the checker's named experiment)

Keying the co-orbital certificate by apsis-passage time with a uniform window

    W = R_enc/v_apo + 3*(da/a)*(T + P)

finds every real contact (zero misses) at candidate cost 2*W*n/P ≈ real contacts,
at any eccentricity and density; the gold's fixed rank-4 window drops a growing
fraction. Derived before the run: a pair in contact at locus M has along-track
separation ≤ R_enc, so apsis-time separation ≤ R_enc/v(M) ≤ R_enc/v_apo; the
orbit spread puts conjuncting pairs further apart by |dn/n|·t* ≤ 3(da/a)·T on the
unwrapped anomaly; +P is safety margin for the mod-Pm key projection.

Every letter below names its statistic (max vs mean — the prior run's failure).

## Family A (standing regime: R=3e-3, da=1e-6, T=2P, K=240; 3 seeds x 8 configs)

- **Z1 (thesis):** misses = 0 in all 24 runs with W.
- **CA (mean cost ∝ contacts):** cost_mean/enc_per_body ∈ [0.98, 1.08] at every
  config. Predicted cost_mean = 2Wn: e=0: 2.92/29.2; e=0.6: 5.78/57.8;
  e=0.9: 12.54/125.4; e=0.99: 40.46/404.6 (n=3000/30000).
- **MA (max ≠ mean, the letter the prior run botched):** cost_max (per body, both
  sides) follows the Poisson max μ2+sqrt(2·μ2·ln n), NOT the mean:
  (e,n=3000): [8,13] / [13,19] / [22,33] / [55,80] for e=0/0.6/0.9/0.99;
  (n=30000): [45,64] / [78,109] / [150,202] / [425,562].
  Sub-letter: cost_max ≥ 1.5 x cost_mean in every A-run.
- **KA (sizing law):** required_k (max tau-rank over contact pairs) ≤ pred_k =
  λ+sqrt(2λ ln n), λ=Wn, in ≥ 21/24 runs; and pred_k ≤ 1.6 x required_k in ≥ 21/24
  (safe but not wasteful). Predicted required_k: (0,3000)≈6, (0.6,3000)≈10,
  (0.9,3000)≈16, (0.99,3000)≈38, (0,30000)≈32, (0.6,30000)≈53, (0.9,30000)≈99,
  (0.99,30000)≈267.
- **TA (tightness):** max tau-sep of contacts / W ≥ 0.9 at e ≥ 0.6 (sizing tight,
  not lucky); ∈ [0.7, 1.0] at e=0.
- **GA (gold's rank-4 drops):** drop fraction: (0.9,3000) ∈ [0.30, 0.50];
  (0.99,3000) ∈ [0.50, 0.80]; (0,30000) ∈ [0.60, 0.80]; (0.9,30000) ∈ [0.90, 0.99];
  (0.99,30000) ∈ [0.97, 1.00]; (0,3000) ∈ [0.02, 0.20].
- Sanity (checker's finding): required_k == max M-rank in every A-run (tau-order
  ≡ M-order for a single-a fleet).

## Family B (drift regime: R=1.5e-4, da=1e-4, T=10P, K=2000, n=3000; 3 seeds x 4 e)

- **Z1:** misses = 0 in all 12 runs (the drift term 3(da/a)(T+P) does the work).
- **NEG (negative control):** with W0 = R/v_apo only (drift term removed),
  miss_frac ≥ 0.90 at every e — the drift term is load-bearing, and the
  instrument detects misses (a control that cannot fail is broken).
- **CB:** cost_mean ∈ [18.5, 21.5] (e=0, 0.6), [19.5, 22.5] (e=0.9),
  [20.5, 23.5] (e=0.99) — nearly flat in e (drift-dominated), while enc/body
  grows 2.4 → 3.1 → ~3.2–4.4. cost/enc ratio ∈ [5, 10], reported honestly
  (drift term set by the horizon, not by contacts; see dossier).
- **MB:** cost_max ∈ [30, 47] (n=3000), and ≥ 1.4 x cost_mean in every B-run.
- **B30 (held-out, never measured by anyone):** famB(0.9, seed 21, n=30000):
  enc/body ∈ [25, 38] (contacts linear in n at fixed R), cost_mean ∈ [195, 215],
  cost_max ∈ [230, 300], misses = 0.

## Controls

- **KCTRL:** famA(0.99, seed 11, K=480) vs K=240: n_pairs change ≤ 1%,
  misses 0, cost metrics change ≤ 2% (sampling adequate; perihelion transits at
  v_peri ≈ 88 AU/yr are the worst case).

## Kill criteria (pre-registered)

- Any miss with W anywhere (Z1): the window derivation is falsified — report as
  refuted, do not widen W silently.
- cost_mean/enc outside [0.9, 1.2] on any A-config: the "cost ∝ contacts" claim
  is dead even if zero-miss holds.
- required_k > pred_k in > 3/24 A-runs: the Poisson sizing law is unsafe as an
  engine rule.
- NEG showing ~0 misses in family B: W is oversized by the whole drift term —
  the sizing rule is wrong in the wasteful direction.

## Addendum — after the grid, before the B re-run (14:52 UTC)

Z1 FAILED as written: B30 (e=0.9, n=30000, seed 21) has 2 misses in 465,934
contact pairs. Diagnosed (not tuned): both pairs have near-max element spread
(da_ij ~ 1.9e-4), contact late in the horizon (t* ~ 9.8 of 10) near apoapsis
(r ~ 1.85 of 1.9). Mechanism: at apoapsis |dr/dM| is minimal, so element
differences cancel along-track offsets — a pair can be within R with DeltaM far
larger than R/v. The missed term is the differential-conjunction reach
X = (1+e)*2da + a*2de + (1+e)*a*2dw, from the apoapsis sensitivities
|dr/da| = 1+e, |dr/de| = a, |dr/dwi| = a(1+e), each over pair differences (2x spread).

Corrected window (closed form, no tuning):
    W' = (R + X)/v_apo + 3*(da/a)*(T+P)

Pre-registered letters for the corrected window, B-grid re-run (13 runs):
- **Z1':** misses with W' = 0 in all 13 B runs.
- **CB' (means):** cost_mean = 2W'n: e=0: ~20.5 [19.3, 21.7]; e=0.6: ~21.7
  [20.5, 22.9]; e=0.9: ~24.4 [23.1, 25.7]; e=0.99: ~35.3 [33.2, 37.3];
  B30 (e=0.9, n=30000): ~244 [230, 258].
- **MB':** cost_max: e=0: [31, 47]; e=0.9: [35, 53]; B30: [265, 355].
- **TA':** tightness dtau_max/W' ∈ [0.55, 1.0] on B (looser than W, by design).
- Family A needs no re-run: W' > W strictly (X > 0) and A had zero misses with
  W, so zero misses hold a fortiori; cost shifts by <= 0.4% (X << R there).
- If Z1' fails too, the corrected law is refuted as well and the dossier says so.
