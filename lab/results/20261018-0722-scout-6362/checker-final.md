Working...
Check complete. `check.md` written; the author's page corrected in place (three overstatements).

**Grade: silver** (`lab/results/20261018-0722-scout-6362/check.md`)

**Reproduction** — `regen.sh` in the clean tree at base 23b62ebc: output bit-identical to `table.txt` (md5 dd07a9fb), 1.04 s. I also re-derived the algebra independently: n = P − s·w is the contact point itself (|n| = R exactly at the root), w·n = −√D from w·P = 0, and Δw = 2√D·n/R² is the specular reflection (|w| preserved). The mathematics is right, not just self-consistent.

**Adversarial cases (one outside the author's domain):**
- **Decade extension** — author's random sweep capped |w| ≤ 8R = 16,384 (β ≤ 0.016). At the shipped max |w| = 9.4×10⁵, arbitrary geometry, 141,892 crossed-in-bin pairs: recovery min 99.9914%, angle ≤ 2.1×10⁻⁴, zero classification disagreements. Holds.
- **Grazing extremes** — 1-, 2-, 8-quanta clearance (author's worst: 51): worst 99.9274% at ρ=3; the exactly-tangent pair correctly exchanges nothing. Holds.
- **Firing wiring** — the dossier's "resolve when D ≥ 0" is wrong as worded: D ≥ 0 is true for consumed (τ₋ = −0.25) and future (τ₋ = +1.25) roots, so bare D ≥ 0 re-resolves consumed pairs. The free tau_ticks window test is exact in integers (0 disagreements over 240k pairs). Page corrected.
- **Overflow side-claims** — measured max intermediate 104 bits (24 bits u128 headroom); the static 2^120 bound is safe, but "k = 16 buys 16 bits" is wrong: S ∝ 2^k, it buys 4. Page corrected.

**Record defects found:** the random sweep's crossed-in-bin count is **22,072**, not the 2,207 in dossier and page (factor-of-10 transcription; page corrected); the toy's 0% shipped column is a printed constant leaning on 8144's engine measurement, which the dossier calls "reproduced in-toy".

**Why silver:** all four pre-registered predictions held (predictions.md 07:29 < table.txt 07:36, worst arm exactly the predicted grazing × ρ = 3), and the claim survives my extensions — but the proof is a toy sharing the reflection operator; the shipped `Law::RelativisticV1` Householder composition is unproven (the author's own gate), and the gain is a correctness class, not a board move. **The gold experiment:** derive the closed form on the shipped v1 operator and fly 1648's criterion on the shipped stepper — a 0.9c crossed-in-bin head-on pair exchanging the exact v1 impulse, the shipped skip as negative control. That one run closes contact-speed's direction 1 outright.
