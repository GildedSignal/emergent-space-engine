# Dossier — 20261009-2348-second-20261009-2257-dynamics-a47e-09fb (second author on dynamics-a47e)

**Claim.** With the checker's four named defects fixed in shipped code, the prior
run's claim survives and its missing piece is delivered: on the law's cheap
path (Wisdom–Holman, CRTBP Jacobi integerized at 2^40), a compounding
integrator error — a per-kick bias ε·h·|a| along the rotating-frame velocity —
is caught 8/8 ships by the exact-integer Allan rule in both draws while the
good control stays ≤ 1/8 (R1) and 0/8 (R3); B12's growth exponent is confirmed
blind (it inverts on the corrected saturating model, 3/3, and on the physical
path, 2/2); and the checker's long-memory false-positive family is answered by
measurement, not by adoption: the multi-τ variants halve OU false flags in
vitro but fail in vivo — the last-octave rule fires the pre-registered false
positive kill (2/8 on the good control, 3–4/8 on the bounded retarded variant)
and the consistency ladder's horizon collapses (misses a 1A linear drift 3/3)
— so R1 plus measured window conditions remains the instrument, with the
correlation-time window now priced at T ≳ 16–32·τ_c, far above the prior run's
T ≥ 4·P.

**Bottleneck.** The instrument risk, verbatim: "B12 cannot yet tell bounded
from compounding error on chaotic ships; until it can, the motion law's
stability is judged by probes, not a gate" (HANDOFF). The prior silver was one
experiment from gold with the record not regenerating; this run closes both.

**Evidence** (all from `python3 exp.py all` in this folder, one deterministic
LCG, output = `run-record.txt` (regenerates everything, wh included, ≈ 7 min);
`wh` also writes `wh-output.txt` itself; every other subcommand ≤ 60 s):

1. **The record now regenerates from shipped code** (checker fixes 1–3):
   `controls` R1 25/25 with the same five deviations as the prior record;
   the inversion model saturates (max|x| = 1.400 = the clamp, no divergence)
   and still inverts 3/3 (bounded 3.75–3.78 vs slow-leak 0.32–0.48 — the
   checker's corrected numbers, now shipped); `run_wh` integerizes at 2^40
   (per-ship integer ranges 1.4e6–3.7e11 printed: no vacuous all-zero flags);
   horizon and phase-scanned alias are shipped subcommands; Kepler roundtrip
   measured 7.93e-13 (the honest number the checker measured, not the prior
   3e-14 claim).
2. **The named gold experiment (K1: passed).** bias3 (ε = 3e-2, ΔJ median
   5.6e-3/8.8e-3, Hill steps 0): caught **8/8 by R1, R2 and R3 in both
   draws**; even bias1 (ε = 1e-2, ΔJ ≈ 2e-3 ≈ the bounded wiggle) is caught
   8/8 by every rule — a deterministic ramp's AVAR ∝ τ² dominates every
   comparison once visible. Good controls: R1 0/8 and 1/8, R3 0/8 and 0/8.
   The Allan rule detects a growing physical-path leak with clean controls.
3. **The inversion is real, twice.** Corrected model 3/3 (above); physical
   path: good ≥ retarded median exponent in 2/2 draws (0.049 ≥ 0.021,
   0.055 ≥ 0.009). B12's exponent measures saturation timing, not boundedness.
4. **The multi-τ fix fails its own pre-registered kills (K2: fired).**
   R2 (last octave, overlapping estimator): draw0 good control **2/8**
   (kill was > 1/8) and the bounded one-step-retarded variant 4/8, 3/8.
   R3 (consistency ladder): controls clean, but catches no linear drift ≤ 1.0A
   on a quasiperiodic floor (0/3 at every ratio ≤ 1.0; R1 catches from 0.3A,
   R2 from 0.1A) and only 73% of pure walks (R1 93%). In vitro (30-seed
   census) the multi-τ rules do halve R1's OU false flags (τ_c = T/16:
   8/30 and 5/30 vs 17/30; T/8: 15/30 and 13/30 vs 25/30) — the checker's
   family is genuinely dented there, but at in-vivo cost. Not adoptable.
5. **The flicker false flags do not reproduce as a continuum.** FFT-shaped
   1/f (band P ≤ T/4 and P ≤ T/2), 18-tone flicker, and white noise: 0/30
   false flags under every rule (R1 flicker-full 2/30). The checker's 3/3
   flicker flags are alias-family behavior (discrete slow modes, phase-
   dependent — the shipped alias scan shows P = T/2 flagged at 4/5 phases,
   P = T/2.5 5/5, P ≤ T/3 0/5 under R1; R2/R3: 2/5, 0/5, 0/5).
6. **Window conditions, measured, for R1:** alias periods T ≳ 2.5–3·P;
   correlation times T ≳ 32·τ_c for ≤ 20% false flags (T/32 → 6/30, T/16 →
   17/30, T/8 → 25/30, T/4 → 25/30); the multi-τ variants only extend this to
   T ≳ 16·τ_c. The prior run's "T ≥ 4·P_max" generalizes to correlation
   times with a much larger constant — B12's window budget is bigger than
   claimed.
7. **Honest wrinkle for B12:** conjunction transients alias as leaks. The two
   scenes with Hill-crossing steps carry ships with single J jumps of 0.2–0.34
   (int 2.5e11–3.7e11); R1 flags exactly those ships (1/8 each). A bounded
   step is not a leak; encounter-adjacent windows must be screened by the
   encounter machinery, not by this gate.

**Predictions.** `predictions.md` frozen before the decisive run (all
pre-freeze setup work disclosed there, including ε calibration on 60-orbit
runs and the R2/R3 design census). Held: inversion 3/3 with max|x| = 1.4 ✓;
good controls R1 ≤ 1/8 ✓; retard 0–1/8 ✓ (R1); bias3 ≥ 6/8 by all rules ✓
(8/8); R2 horizon 0.1A ✓; R3 horizon collapse ✓; K2 fired on R2 exactly as
pre-registered (reported as a refutation of the multi-τ adoption, not hidden).
Missed: bias1 predicted 2–7/8 partial, measured 8/8 (favorable: the ramp
dominates sooner than estimated); R1 at 0.2A predicted ≥ 2/3, measured 0/3
(the checker's 2/3 there was seed luck; 0.3A is the honest R1 horizon);
τ_c = T/4 predicted "all rules flag ~all", measured 83/60/57%.

**What would make it wrong.** (a) The bias is near-deterministic — a ramp is
the easy leak; stochastic leaks catch at 93%/77%/73% per series (census), so
a fleet-level criterion must absorb per-ship misses. (b) The physical toy has
no changeover and one planet; τ_c there is set by conjunction spacing, and a
scene with τ_c ≥ T/16 will false-flag under R1 too — the gate window must be
derived per scene (6). (c) A conjunction transient defeats the rule (7).
(d) n = 501 samples per series here; longer windows shift every horizon.

**Cost of adopting.** R1 is ~15 lines on a per-ship integer J-series the
engine already samples; no reference run, no thresholds, machine-independent.
Fits PRINCIPLES: "types of errors and not just errors" (OC#42); "exact means
deterministic and reproducible" (P2); integers decide, floats never do.

**The lens.** The dynamics lens made me trust the turnover argument (last
octave must fall for bounded OU) over the estimator statistics — the 3-dof
discovery and then the overlapping fix were forced by measurement, and the
in-vivo failure of R2 (a decorrelation-time effect, not a period effect) is
the same lesson a second time. What it may have missed: the fleet-level
criterion (k-of-8 ships) was reasoned about but never measured as a decision
rule; and the conjunction-transient alias (7) was found by accident in the
control rows, not predicted.

**Grade self-assessment.** Gold condition met for the named question: the
prior claim now holds on a shipped, regenerating record (all four checker
defects fixed), the named experiment ran and passed its pre-registered kills
(K1), and the multi-τ proposal is cleanly refuted for adoption (K2) with its
in-vitro gains measured — the B12 redesign gets a working leak detector (R1 +
window budget), not a menu.
