Grade: gold

**Abstract (for the integrator).** Claim: at r = 12–200 M, β ≤ 0.5, sustained and curving
burns, the version payload (x, v, a) is complete — the exact Kinnersley field evaluated
from the retarded (x, v, a) alone matches the finite-difference oracle at 1.3e-10–5.7e-9 —
while Carlip's cheap non-radiative b3 readout is not (missing −2m/R: 17% at 12 M; burn
channel ≈ (2–6)·a·r, percent-level at 20 M for engine burns). Everything reproduced
bit-identically (`regen.sh`, 36 s); the oracle independently pinned by a from-scratch
boosted-KS construction at ≤ 2.2e-15 through β = 0.9. Extended one decade inward (6–8 M)
and across β = 0.5: holds (RX ≤ 5.5e-8). Gain: certifies the payload for law.md's
causality primitive at every field strength and kills b3-completeness at strong field,
deleting the strong-field payload-extension and jerk-slot questions. Adoption: one readout
clause at law.md line 33; no payload, cadence or slot change.

## Reasons

1. **Reproduction.** Clean scratch copy, `bash regen.sh` (36 s, deterministic):
   `sweep.json`, `sweep_heldout.json`, `scaling.json` all bit-identical to the stored
   files. Every dossier number I traced is in the data: R2 = 2m/R at small β
   (1.01e-2 / 4.18e-2 / 1.11e-1 / 2.01e-1 at 200/50/20/12 M); R2b/β² = 1.24–1.71 flat
   in r; Laplace control R1_perp = (0.6–0.7)·β_s; R0−R2 = 2.13e-3 at gentle 20 M;
   P4's kill 4.43e-2 at gentle 12 M; held-out β=0.2/r0=16 → 6.79e-2 (1.2× the 1.4β² law).
2. **The oracle is independently pinned.** My own construction (textbook static KS with
   l_μ = (1, −n) + Lorentz pullback, sharing nothing downstream with the author's code)
   matches the code's Kinnersley metric at 2.2e-16–2.2e-15 for uniform β = 0.01–0.9.
   My first attempt disagreed at 2e-2 — my own ingoing/outgoing covector sign — which is
   direct evidence this control discriminates conventions at the 1e-1 level and would
   catch any real transcription bug. This control is the load-bearing one and is still
   not in `regen.sh` (the self-test there covers only the static limit and FD-vs-b1a);
   it should be added when the clause is adopted.
3. **Adversarial cases (mine).**
   - *Next decade inward* (r0 = 8 and 6 M, the ISCO — outside the swept 12–200 M), free
     fall: RX ≤ 7.7e-9, R2 still tracks 2m/R, R2b/β² stays 1.2–2.2 (mild rise from 1.6
     at 12 M). Velocity-only, no cliff; the claim's domain extends to r ≥ 6 M.
   - *β = 0.5 robustness* (domain edge): 200 random events, r ≥ 6: RX ≤ 5.5e-8, retarded
     residual ≤ 5.7e-14. Above β ≈ 0.5 the script's retarded solver breaks **silently**
     — the Newton bracket t−2R0−2 covers retarded distance ≤ 2R0+2, exceeded by
     approaching sources once 1/(1−β) > 2 (β = 0.7 orbit scenes return rx ~ 1e15
     garbage with no error). Not a kill: the claim is scoped β ≤ 0.5, where I verified
     the solver. Anyone reusing the instrument above β = 0.5 must widen the bracket.
   - *3-D inclined source* (β = 0.1 at 45°): RX ~ 1e-9 — the formulas are correct
     out of plane (the engine is 2D, so this is bonus).
   - *The scoped-out consumer kinematics, sized*: the moving probe's own terms ≈ 2β_c²
     (median 2.9% at 50 M/β_c 0.14 → 9.4% at 20 M → 17% at 12 M → 27% at 8 M). This is
     larger than the readout residuals the scar ranks at strong field (R2b ≈ 1.6e-2 at
     β_s = 0.1, 12 M), so the static-probe scar isolates the news channel exactly as
     the author scoped it, but the adopted readout clause must also carry the
     consumer's velocity terms. Payload completeness is unaffected: the moving readout
     is the same closed Γ contracted with the consumer's local V.
4. **Predictions.** Pre-registration is supported by file order (predictions.md predates
   the final sweep scripts and every stored output). P1 held; P3 held (2.1e-3 vs the
   1.6e-3 prediction); P4's kill criterion fired — 4.4e-2 > 1e-2 at gentle 12 M — and
   the author reported the kill as the result rather than hiding it, with the RX arm
   separating payload (complete, 1e-10) from readout (incomplete). Held-out rows ran
   and matched the refined law. **P2, however, did not hold as written**: R2 at
   (0.1, 200) = 1.92e-2 against "below 1e-2"; R2 at (0.3, 12) = 1.32e-1 against "both
   under 1e-1"; R2b only 1.3× under R2 at β ≥ 0.1 against "10–100×". The dossier's
   "held with a refinement" is generous framing; what actually held is the refinement
   (the missing 2m/R term, not ε, separates R2 from R2b; ε is velocity-only), and the
   "100–800×" envelope is loose (measured 779–13,039 at β = 0.003, 8–136 at β = 0.03).
   The decisive pre-registered criteria all behaved; this is a framing nit, disclosed
   in the dossier's own text.
5. **Novelty.** The published gravity-news page's open direction 4 says exactly this
   question was unmeasured ("the strong-field consumer (r = 20M …) — unmeasured"), and
   the standing payload decision rested on scout-d947's scalar toy at β ≤ 0.3 weak
   field. This run replaces a literature extrapolation with an exact-GR measurement and
   a machine-precision-pinned instrument. Not in HISTORY (checked d947/7ab4/a237/e300
   entries: all weak-field or toy).
6. **Goal fit.** PRINCIPLES #30 ("we need to build towards GR that's the goal that we
   should not loose track of") — the black-hole consumer is certified at the
   representation level; #23 ("Nothing past c") — every arm consumes retarded data
   only; #2 ("Exact physics is the oracle, not the implementation") — here oracle and
   implementation coincide for tens of flops, so the exact form is itself the engine
   candidate. The gold bar's "shows that a premise is wrong" is met (b3-completeness
   at strong field is wrong: 17% at 12 M), and adoption is one clause plus a reference
   formula — within one step.

## What the author missed

- The boost control — the only control that pins the moving-source metric against an
  independent construction — is absent from `regen.sh` and from the shipped self-test;
  the dossier cites its result but the shipped commands cannot regenerate it.
- The retarded solver silently returns garbage above β ≈ 0.5 (bracket too narrow for
  approaching sources); nothing flags it. Harmless inside the claimed domain, a trap
  for reuse.
- P2's pre-registered magnitudes at β ≥ 0.1 failed as written (see above); "held with
  a refinement" overstates, and the "100–800×" envelope does not match the data at
  either β.
- The consumer's own kinematic terms (≈ 2β_c², up to 17% at 12 M) are bigger than the
  readout residuals being ranked; the page's readout clause should name them (I added
  the measured sizes to the proposed page). The dossier's lens paragraph scopes this
  out to the handoff page correctly, but the sizes belong with the clause.
- The dossier says the b1a dm/ds term is "implemented but never exercised"; the code
  has no such term (constant m only) — the proposed page already corrects this to
  "NOT implemented".
