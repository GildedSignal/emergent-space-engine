Working...
Check complete. Tree restored to its initial state (only untracked `lab/results/`), all probe evidence preserved in `/tmp/chk56e/`.

## Verdict: `Grade: silver` — written to `check.md`, page corrected in place

**Reproduced (bit-exact).** Applied `work/patch.diff` myself; verified against b172's published branch it is **b172 verbatim + one scenario.rs hunk (+14/−5, the two env-gated knobs)**. Re-flew form100/48k/cap4096 with the author's binary: digest `7bb62936…`, 7,928,202/270,979, hits 1,486,660 — identical to the digit; b172's anchor digests (`15fc19b1`, `d3542eea`) regenerate exactly; both price laws re-derived exact.

**Four adversarial probes, all outside the author's domain:**
1. **Seed 5 @ 48k** (depth bracket was single-seed): ratio **14.77** — the inversion holds, but 29.26 is seed-1's, not a constant; price law exact.
2. **64k** (deeper than flown): **27.34**, bill 294,357, price law exact — the small cap stays dead, the ratio plateaus.
3. **Mint-bill razor at 48k**: cap 270,979 → **0 evictions** (hits = global's 9,143,883); cap 270,978 → **1 eviction**. The author's correction of the b172 checker's "273,200 exactly" is now razor-proven.
4. **The a-draw cell** — the author's own named, unflown remaining edge (7-line knob, my build): continuous radius over [2,3) with form e holds **fills exactly 616,250 and ratio 1.0131** — identical to every form variant to the digit. Neither branch of the author's registered fork obtains: **the radius draw alone is inert**. The closure cell (a-draw + belt e) reads hits **1,528,417 ≈ the belt's 1,528,451**, so the belt's 1.66M fills / 7.23 are the **e × radius-spread interaction**.

**Why silver, not gold.** The depth record, bill invariance and angular kill are gold-grade and fully regenerable. But the claim's mechanism half — "the intra-wave win is bought by the radius draw," sizing axis "radius-concentrated episodes" — is refuted by the one cell the author named and left unflown: a fully radius-diffuse low-e population holds the small cap, while a radius-concentrated belt-e population degrades to 1.696. The sizing axis is **e**, not radius concentration. The one-gold step: land the a-cell in the battery (numbers now on record from this check) and re-scope the sentence.

**Page.** Corrected where it overstated: a checker bracket under the f56e headline, the two Refuted lines, and open directions 1 and 5(c) — each marked with the measured cube. One accidental clobber during editing was caught and restored; final page verified structurally intact.
