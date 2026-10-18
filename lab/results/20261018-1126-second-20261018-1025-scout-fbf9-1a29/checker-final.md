Check complCheck complete. **Grade: gold** — written to `check.md`, with the author's page corrected in place.

**What I did:**

1. **Reproduced**: `regen.sh` IDENTICAL on all deterministic fields (runner + my own rerun, 68 s), plus a from-scratch rebuild of the cell experiment against the same shipped crate — n=10⁴ reproduces the author's record field-for-field (22/21 flips, viol2_on 22/22, 3 post-events, dues 4.3225×10⁶ intervals). Verified the flight drives the real shipped Phase-A path (`tiered_arm`: `Sorted::range` → `is_candidate` → `arm_pair`, SAFETY 1.1), and that the toy's GM=TAU² vs crate GM=1 mismatch resolves exactly — each kick is a true relative impulse of exactly dv/v in the crate's dynamics.

2. **Predictions**: pre-registered 15 min before the record run, amendment disclosed against a kept smoke log (same flip counts; only scoring added). The kill line is the toy's own — verified verbatim on the parent branch — and fired as written (0.1075 ≥ 0.1).

3. **Four adversarials**:
   - **n=3×10⁵ (one decade out)**: 3.5 flips/kick (Θ(n) extends), viol2_on = flips_on 65/65, 4 more real leaked events.
   - **Reach sweep**: violator dues collapse 1.3×10⁶ → 23 intervals between ρ=10⁻⁵ and 4.4×10⁻⁵ AU — the regime boundary is real, quant-c9c7's ρ=10⁻⁴ sits in the smooth side, reconciliation confirmed.
   - **|Δn| separability**: violators at 1.3–1.7× the candidate median — no Δn cut separates them, confirmed.
   - **Independent truth check**: 7/7 leaked events re-solved with my own Kepler code (no crate) reproduce the reported miss distances to 5 digits, all strictly within reach — the band rule provably loses real encounters.

4. **Found one defect**: a units slip — B = 5×10⁵ m = **3.34×10⁻⁶ AU**, not "3.3×10⁻⁹"; the design reach is ~13× below ρ\*, not "10⁴×". Conclusions unaffected (both boundary sides verified by the sweep); corrected in the proposed page, noted in check.md. Also flagged: the violators ride ~10⁵-tick Wide windows (w/d ≈ 0.3–1), not the dossier's 23-tick cross window — the re-roll stands on measured decorrelation, but the ρ\* margin is thin, which matters for the leak-gated-slack direction.
