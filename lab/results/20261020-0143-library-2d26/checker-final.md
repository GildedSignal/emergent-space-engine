Working...
Check complete. `Grade: silver` written to `lab/results/20261020-0143-library-2d26/check.md`; page corrected in place; tree restored (patch reverted, my scratch traces removed).

**What I did:**
- Applied `work/patch.diff` myself (25 insertions, none on a timing path — trace dumps post-loop; the footprint half is the disclosed Linux port shim), rebuilt, flew five arms, each < 60 s, peak 1.48 GB.
- **Repro:** 2×10⁵ rtf400 → coverage 2.55, p99 11.941, over 14 (author 2.55/11.94/13; regens 2.34–2.55) — the decision-cadence numbers are tight across four independent flights. 10⁵ rtf2000 → coverage 0.29.
- **Adversarial, outside the author's grid:** 3×10⁵ rtf400 (their own named, unflown rung) → coverage 1.50 vs composed 1.54, excess within 2.5% of the K^1.244 composition, pre-onset ebb K-flat (20.5–20.8 s); 10⁵ rtf400 → 6.04 vs composed 6.0; coast at play cadence → over 0, excess 0. Composition holds; my rung puts the crossover at ~4.2×10⁵.
- **The kill for gold:** P6's "5/5 quotes byte-identical" is false. Against the fresh export the author's own regen fetches, only 2/5 quotes are verbatim — three are trimmed or quote-mark-retyped — and `verify_quotes.py` tests id-presence, never text. A registered prediction reported held that the log contradicts, per lab rule and the 1-October precedent, keeps it out of gold; the physics itself is gold-grade and adoptable (coverage column + the ordering decision: prepay < amortize < delete, only the stagger scales — still unflown).
