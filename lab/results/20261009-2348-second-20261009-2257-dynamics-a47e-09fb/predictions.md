# Predictions — 20261009-2348-second-20261009-2257-dynamics-a47e-09fb (second author)

Written before the decisive run (`python3 exp.py all` → `run-record.txt` + `wh-output.txt`).

**Question.** Does the prior run's claim survive once the checker's four named
defects are fixed in shipped code and the named gold experiment (a compounding
integrator bias caught on the physical path) is run — and do the multi-τ Allan
variants answer the checker's long-memory false-positive family?

**Instruments under test** (exact, integer series, no thresholds):
- R1 (prior): leak ⇔ AVAR(T/4) > AVAR(T/32), non-overlapping estimator — kept
  so the prior record regenerates bit for bit (verified during setup: 25/25,
  same five deviations).
- R2: leak ⇔ AVAR(T/4) > AVAR(T/8) — last octave, overlapping estimator.
- R3: leak ⇔ AVAR non-decreasing over {T/32, T/16, T/8, T/4} and strictly
  rising overall — consistency ladder, overlapping estimator.

**Disclosed pre-freeze setup work (already observed, not predictions):**
- `controls` R1 record regenerates exactly (25/25, five deviations as before).
- R2/R3 columns on controls; the 30-seed design census (`census`); `memory`
  3-seed rows; `alias` — run while choosing the rule set and the flicker
  synthesis. Key design facts they fixed: (a) the non-overlapping last octave
  has 3 dof and alone flipped ~2/10 pure-walk verdicts → R2/R3 use the
  overlapping estimator; (b) an 18-tone "flicker" is a synthesis artifact
  (discrete slow modes, seed/phase-dependent) — the honest continuum arm is
  FFT-shaped 1/f, which flags 0/10 under every rule; (c) an inertial-tangential
  bias is nearly Jacobi-neutral on these co-rotating ships → the planted bias
  acts along the rotating-frame velocity (calibrate(), 60-orbit runs only).
- ε calibration on 60-orbit runs only: bias1 = 1e-2 (ΔJ ≈ 2e-3 extrapolated),
  bias3 = 3e-2 (ΔJ ≈ 5.5–9.8e-3 extrapolated, vs bounded wiggle ~1e-3–4e-3).

**Held-out predictions (decisive run):**

1. **Inversion (corrected saturating model):** bounded median exponent 3–5
   (no longer 49–57; divergence gone, max|x| = 1.4 exactly = the clamp), slow
   leak 0.3–0.5, inversion 3/3 draws.
2. **Horizon (linear drift on qp floor, 3 seeds):** R1 catches ≥ 2/3 from
   ratio 0.2, misses 0.05; R2 catches the same or one step lower (0.1
   boundary); R3 misses below ~0.5 (the ladder's short octaves stay
   floor-dominated: white rounding floor > ramp at τ = T/32 for ratio ≲ 0.4).
3. **wh good control at 2^40:** R1 ≤ 1/8 per draw (checker saw 0 and 1);
   R2, R3 ≤ 1/8. Integer series ranges ≥ 1e8 (non-vacuous, unlike the prior
   shipped all-zero record).
4. **wh retard (1-step):** 0–1/8 under all rules (below the horizon, as the
   prior run found); growth exponent of good ≥ retard in ≥ 1 of 2 draws.
5. **wh bias3 (ε = 3e-2) — the checker's named experiment:** ΔJ ≈ 5e-3–1e-2
   over the window (possibly superlinear); caught ≥ 6/8 by R1, R2 and R3 in
   both draws (a near-deterministic ramp has AVAR ∝ τ², dominating every
   comparison once above the wiggle).
6. **wh bias1 (ε = 1e-2):** partial catch, 2–7/8 under R2 (boundary case,
   ΔJ ≈ wiggle scale); no kill criterion rides on it.
7. **Memory census under R2/R3 (already observed, restated as claims):** OU
   false flags grow with τ_c; R2/R3 ≤ R1's counts through τ_c ≤ T/16; at
   τ_c = T/4 all rules flag ~all (the window limit, restated for correlation
   times: separable only while T ≳ 16·τ_c, not the 4·τ_c I would have hoped).
   Continuum flicker and white: 0 flags under every rule.

**Kill criteria (pre-registered):**
- K1: bias3 caught < 6/8 by R2 in either draw → the named experiment fails;
  the Allan rule does not deliver a physical-path leak detector; report as
  refutation of that part of the claim.
- K2: good control > 1/8 by R2 in either draw at 2^40 → false positives on
  the physical path; refuted.
- K3: in the memory census R2/R3 do not lower R1's OU false-flag counts at
  τ_c ≤ T/16 → multi-τ buys nothing; the checker's family stands unanswered.
- K4: inversion < 2/3 with the corrected model → the diagnosis itself dies.
- K5: a bias3 scene fails to settle in 30 seeds in both draws → the planted
  leak is a scene destroyer (like retard10), not a leak instrument.

**Honest costs to report whatever happens:** R2/R3 lose per-series catch power
on stochastic walks (census: R2 77%, R3 73% vs R1 93% at r = 3) — the lever
arm buys OU discrimination and pays in walk power; deterministic ramps are
caught by all. The gate-level reading: false flags are scene-correlated (all
ships share τ_c), walk misses are per-ship independent, so a fleet criterion
(≥ k of 8 ships) may still favor R2/R3 — stated, not hidden.
