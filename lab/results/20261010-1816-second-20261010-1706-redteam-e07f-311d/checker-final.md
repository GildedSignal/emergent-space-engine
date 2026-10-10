Working...
Check complete — `check.md` written, nothing else in the run folder touched.

**Grade: silver.**

**What reproduced (all from the dossier's commands, patch applied, clean tree):**
- `sweep`/`stair`/`keys`/`oracle` regenerate **byte-identically**; `exact.py` tally identical: 7,093/7,203 law=exact, 110 disagreements all `refuse:Range` on exact-bound states, zero wrongly parked.
- Headline numbers verified: advance within 1.076×10⁻⁹ over (6.003, 7.0]; rim diverges smoothly to 851.0337/851.0340 at d=1e-6; all 306 memo keys within 7.8×10⁻⁹ of their own GR; adjacent-key jumps track GR per-pair (−0.662% vs −0.66%); exact-key boundary on 6+2e to <5×10⁻⁷; one-line repro `probe 7,0 → refuse:Range` confirmed.
- Mechanism confirmed on the *actual* refused integers with my own example: `from_invariants` compiles them (92.06/85.54) where `from_state` refuses — the word-rounding guard, no fallback, as claimed.

**Why not gold:**
1. **Stale record:** stored `flip.out` lacks its first summary line — generated before the last code edit (rs 18:43 vs flip.out 18:31), so the artifact isn't what the shipped code produces (the missing line is consistent with the disclosed P6 miss; nothing hidden, but it's the exact record failure the taste log dings).
2. **Adversarial finding — the defect is bigger and the fix incomplete than sold:** exactly-circular dyadic states at r ∈ {6.25, 6.75, 7.0, 7.625} — **4/25** of eighth-steps in [6,9] — refuse `Range` (not "isolated integer pairs"); and the proposed fallback doesn't rescue 6.25/7.625, where `from_invariants` itself refuses `NoBoundOrbit`. Adoption is not one step.
3. P2 failed, P6 partial (both honestly reported); minor errors: band typo, E5 window conflation (bound-losing window is 8.9×10⁻⁵, not 0.9×10⁻³ — claim conservative).

**Named gold experiment:** enumerate the full refusing set (sweep + dyadic-circular families), fix the guard with an exact-path fallback that also covers the 6.25/7.625 class, re-run this falsifier to zero wrong refusals, and regenerate every artifact from the shipped code.
