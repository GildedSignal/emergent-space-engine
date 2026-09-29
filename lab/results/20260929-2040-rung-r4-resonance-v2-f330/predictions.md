# predictions.md — rung r4 v2, run 20260929-2040

Written after the machinery checks (round-trip, first-order window) and after the
IC scan on the *baseline* resonant case only (600 steps/orbit). No law
configuration has been run on any case yet. The phase-shifted case (res-2-1-w2-4)
and the three controls have never been integrated at all: they are the held-out
set. Cases frozen before this file: e1_0 = 0.08, varpi1 = 0, lam1 = 1.0,
lam2 = 0.5 (phi0 = 0), m2 = 3e-3, 200 synodic periods; res-A has e2 = 0,
res-B has e2 = 0.05 with varpi2 = w2 = 4.0; controls have e2 = 0.05, varpi2 = 0.

## Predictions for the held-out cases (truth at 2400 steps/orbit)

1. res-2-1-w2-4 (phase-shifted): truth libration concentration C in [0.70, 0.95]
   (the red-team reported 0.867 for their version); max e1 in [0.10, 0.25].
2. Controls: max e1 in [0.079, 0.083] for ratio 5.0 and 2.55 (secular envelope
   barely above the free e = 0.08); ratio 2.15, being nearest the 2:1 resonance
   edge, may reach 0.09–0.12. No ejection in any case.

## Predictions per configuration

- `truth-1200` (positive): pump ratios 1.00 ± 0.02, lib ratio ≥ 0.97, controls
  within 20% — passes every criterion. (If not, the truth is not converged and
  the rung is VOID by its own rule.)
- `arc-g16` (candidate): pump ratios in [0.9, 1.15] on both resonant cases, lib
  ratio ≥ 0.85, all three controls within 20%. **Predicted PASS of all six.**
- `arc-g8-half` (candidate): shorter windows resolve the near-conjunction
  structure better; pump ratios in [0.9, 1.2], lib ratio ≥ 0.8. **Predicted PASS**,
  slightly worse than g16 on lib.
- `arc-g8` (candidate): 8 Gauss–Legendre nodes over a two-orbit window (the 2:1
  synodic period) with the acceleration spike sitting at the window *ends*;
  I predict mild over-pumping, e_pump_ratio_max in [1.05, 1.35] — **borderline
  against pumphi ≤ 1.25; roughly a coin-flip**. lib and controls pass.
- `averaged` (negative): orbit-averaging erases the resonant angle — predicted
  C_law < 0.4 (lib ratio < 0.5, FAIL) and no resonant pumping (pump ratio
  ≈ 0.55, FAIL pump). Controls likely pass (secular envelope is what averaging
  keeps). Fails at least two criteria, as a negative must.
- `none` (negative): max e1 = 0.08 → pump ratio ≈ 0.5 (FAIL pump). Caveat I can
  already see: at exact 2:1 the resonant angle is *frozen* (2n2 − n1 = 0), so its
  concentration is 1 and `lib` passes vacuously; the controls' envelopes also
  stay within 20% because the secular forcing is tiny next to e = 0.08. The
  configuration still fails the rung on pump.

## Cost side

kicks_per_orbit (median over cases): arc-g8 ≈ 0.54, arc-g16 ≈ 0.54,
arc-g8-half ≈ 1.07, averaged = 1.0, none = 0, truth-1200 = 0. dense_steps = 0
everywhere (quadrature nodes are not dynamics steps; the positive control
reports 0 by convention).

## What would change my mind

If arc-g8 fails pumphi while g16 passes, the conjunction spike is the reason and
the design wants either more nodes or shorter windows — a cost statement, not a
physics one. If g16 also over-pumps > 1.25, the first-order map itself is
insufficient at m2 = 3e-3 and the kick layer needs second-order terms or more
windows — that would argue against the design's cheap path, the same way r4 v1
argued against instantaneous kicks.
