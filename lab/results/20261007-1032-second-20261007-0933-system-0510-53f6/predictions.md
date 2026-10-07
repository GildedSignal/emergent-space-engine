# Predictions (written before the decisive multi-seed runs)

Run: `python3 exp2.py --H 24000 --seed S --memo M --law L --out run-S-M-L.json`
for S in {20261007, 20261008, 20261009}, M in {on, off}, L in {B, B2}.
Scene and REF/A identical to the parent run 20261007-0933-system-0510 (its
exp.py, byte-identical physics; port validated: seed 20261007/B/on reproduces
its decisive.json per-particle). B2 is new: the same per-conjunction impulse
in the eccentricity-vector representation (increments of e·cos ϖ, e·sin ϖ —
regular at e → 0 — instead of de, dϖ, which carries a 1/e factor).

What I have seen before writing this: the parent's shipped seed 20261007
(B/on) in full, including my resonance diagnostics; one B2 smoke at
H = 2000, seed 20261009, memo off (belt p90 0.96, median 0.093, 2 wrong-sign
at a horizon too short for clean rate fits — A also shows 2 wrong-sign there).
Seeds 20261008/09 at H = 24000, all B2 at H = 24000, and all memo-off runs
are unseen. The width model is fixed a priori (law.md's compiled-frequency
test p·n − q·n_J ≈ 0; order-k half-width in mean-motion ratio
W_k(e) = C·√(μ·e^k), C anchored at B17's frozen W = 2.5·μ^(2/3) at e₀ = 0.02,
giving C₀ = 5.55); the verdict is reported at C₀/2, C₀, 2·C₀ with no fitting.

## E1 — the checker's named experiment, law B as shipped

1. Belt exclusions by the compiled-frequency test, per 30-particle seed:
   C₀/2: 0–1; C₀: 1–3; 2·C₀: 5–9.
2. The failure set (relerr_rate_B > 2) and the resonant set are disjoint:
   6–9 failures per seed, of which excluded ≤ 1 at C₀ and ≤ 3 at 2·C₀. On the
   shipped seed the 8 failures sit 2.5–12 half-widths from every compiled
   frequency (nearest: 2.732 AU at ~10 widths from 13:5), while particles
   within 0.2% of the 7:3 and 1.4% of the 5:2 pass at relerr 0.03–0.16.
3. Filtered belt tails at every width, every seed: p90_B ≥ 5, max_B ≥ 12,
   wrong-sign ≥ 4; A: p90 ≤ 0.8, max ≤ 1.0, wrong-sign 0. **B loses the
   checker's tail test at every width → the shipped claim is refuted by the
   named experiment.**
4. Mechanism: every failure has e₀ ≤ 0.065; across the belt, relerr_rate_B
   correlates with 1/e₀ (Spearman ρ > 0.5) and not with resonance proximity
   (|ρ| < 0.3 against log₁₀(detune/W)). The synodic window is not an integer
   number of particle orbits, so the Simpson integral of the Gauss dϖ/dt
   leaves an O(μ/e) non-cancelling residual per conjunction; at low e this
   dominates the true rate and wrong-signs ϖ. Averaged over the belt it
   cancels (median 0.10); the tail is where it does not.
5. Memo: hit rate 0.55–0.65 (B/on); memo off leaves the tails broken
   (p90 ≥ 5) — the memo form is not what E1 turns on.

## E2 — the representation fix, law B2 (e-vector impulse), memo off

6. Wrong-sign 0–2 per seed (vs 6–9 for B), and those that remain are
   near-zero-|rate_ref| denominator artifacts, not systematic.
7. Filtered belt (C₀): median ≤ 0.15, p90 ≤ 1.2, max ≤ 3; env_B (e-envelope
   relerr) p90 ≤ 0.05, at or below A's (≈ 0.15–0.2); cadence 0.50–0.62
   events/orbit, within ±0.02 of B's.
8. Pre-stated rescue criterion: B2 is a valid away-layer replacement iff on
   every seed, filtered at C₀: p90_B2(rate) ≤ p90_A(rate) + 0.3 AND
   wrongsign_B2 ≤ 1 AND env p90_B2 ≤ env p90_A. If it holds, the unification
   (one conjunction event carries the kick) stands in the e-vector
   representation, and the compiled-frequency test guards only the true
   resonant minority.
9. Inside the 2:1 band (the scan set) B2's over-pump persists at 1.2–2.4×
   (the r4 v1/v2 first-order-in-μ legacy is a phase-feedback defect, not a
   representation singularity) — the resonance detector stays necessary,
   consistent with the parent's falsification of the free detector.

## Kill criteria (for the configuration, not the method)

If B2's filtered p90 exceeds 2× A's on any seed at C₀, or wrongsign_B2 ≥ 3 on
any seed: the e-vector form does not suffice, the unification is killed at
this rung, and the next representation to test is orbit-closed windows (each
window an integer number of particle orbits, so the quadrature residual
cancels by construction).
