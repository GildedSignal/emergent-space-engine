# Predictions (written before the decisive runs)

Frozen decisive configs: `b12 8 plain 200`, `b12 8 sem 200`, `b12 6 plain 200`, `b12 6 sem 200`,
`b13 8 plain 64`, `b13 8 sem 64`. Seeds fixed (b12 seed 4, b13 seed 7). Planet radius ×10⁻³
(memo §1.8: losses there are chaos, not law). Controls on both sides: plain v2 must land in the
memo's bands (B13 ~60/64 at k=8; worst Jacobi ~1e-5 at 200 periods) or my replica is broken
(VOID); the shipped plane's known flaw (a history-dependent step) is not re-run here — the memo
already measured it (exponent 0.795) and my harness reproduces the same mechanism's signature
(nonzero bias at encounters, below).

Kill criteria for SEM (from the memo's P8, frozen here before the runs):
- no-solution rate > 1% of steps, OR
- B13 within-1% drops by more than 2 ships vs plain at equal k, OR
- the median exponent at equal k worsens vs plain.

## What I expect (tuned on nothing; the smoke runs were 8 ships × 20 periods, k=8 plain only)

1. **Failure concentration.** The Newton on α degenerates where dU_P/dt ≈ 0 along the drift —
   the closest-approach points (the memo's named failure). I predict: failures > 0, essentially
   all within encounters, with an overall rate between 0.01% and 2% of steps (my uncertainty is
   wide; the kill line is 1%). [held-out: the exact rate]
2. **B13 barely moves.** Where the solve converges, |α − 1| ≪ 1 away from encounters, so the
   flyby energy errors change little: SEM within 2 ships of plain at k=8 (both ~58–62/64).
3. **The exponent falls, most at coarse k.** SEM pins end-of-step K at solver tolerance
   (~1e-13), so the observable C's error becomes J-roundoff (a random walk of ~1e-16 per step)
   plus the fallback steps' residual. Predictions: exponent(SEM, k=6) < 0.5 while plain is
   ~0.4–0.7; exponent(SEM, k=8) ≈ 0.4–0.6 (roundoff-floor walk, more steps than k=6);
   worst_err(SEM) ≤ 1e-9 at k=6, ≤ 1e-10 at k=8. [the k=8 SEM exponent is my least certain]
4. **α's sign.** [held-out] whether the solved steps run systematically longer or shorter than
   the clock's nominal step, i.e. mean(α − 1) ≠ 0 with a consistent sign, and how often the
   bracket [1/8, 8] binds near the shrunk planet.
5. **Lost ships.** At radius ×10⁻³ I expect 0–1 lost in all four b12 runs (chaos, not law);
   if SEM loses ≥ 3 more than plain, that is a kill signal I did not pre-register as decisive
   but will report.

## The system claim this tests

The clock `s` and the register `p_t` are two carriers of one constraint (K = H_D − U_P + p_t =
0). v2 pays for the split's residual of K in the observable; SEM closes the loop exactly. If
SEM holds, B12's remaining error is only the J carry (integers: bounded, no trend), and the
"keep the offset small" strategy is deleted. If it fails at closest approaches, the
configuration dies, not the method (a fixed-Δs map with a state-function residual remains).
