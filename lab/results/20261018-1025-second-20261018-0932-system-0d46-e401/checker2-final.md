Working...
**Grade: gold** — written to `check2.md`, with the run's `wiki/view.md` corrected in place and the tree restored (patch applied, attacks flown, `git checkout` + example removed; only `check2.md`, `check2` page notes and `/tmp/check2/` logs remain).

**What I did**

1. **Reproduced from a clean tree** (applied `work/patch.diff` myself, rebuilt, reran): every headline number holds — tier 0.56–0.58 µs/member (solve 0.13, row 0.27) vs shipped 7.3 µs/body, cross share 0.95, kick_inel 240,000/240,000 steady, window-1 audit 48,000 rows / 0 px violations / t_e exact 48,000/48,000, bench crowd 0 groups at 2⁻¹⁴ with ≈1 exact key per body.
2. **Three adversarial attacks, two outside the author's range:**
   - **e=0.01 breaks the ring**: 36% pixel violations, t_e exact only 10.9% (e=0.05 → 86%). The exact regime is e≈0 only — tighter than the dossier's "degrades as e grows".
   - **Audited coarse quantization kills the crowd's last escape**: the author only counted groups (gmax 37 at 2⁻³); auditing them shows 100% panel violations at 2⁻⁸ and 2⁻³ (up to 86% pixel, max 408 px). Grouping ≠ tiering.
   - **`--members 1200` saturates at 428 bodies** (scene cap); the cap point holds the law.
3. **Instrumentation findings**: the coded panel gate is 10⁴× lenient vs 2df1's rule (one closing row of 48,000 at 1.01× true tolerance — pixel/t_e gates carry the exactness claim); the dossier's Control bullet (0.70–0.79) misattributes arm400's ramp-up windows — ctl4 is 0.96–0.97 throughout.
4. **Predictions**: honest — C1/C2 failed and are reported as failures; the failures are the discovery. Novel against the live page (its open direction 2 expected ~0.02 µs; no prior run prices or audits the gather-side tier).

**Gold under the premise-wrong clause**: 0d46's ~300× crowd claim dies on three independent measured grounds (row-math floor, de-keying at every quantization, the partial-step wall at 100% of steady reads), the correction is adoptable now, and my attacks strengthened rather than overturned it. The surviving 13× formation lever stays one law experiment away (kick in the word — which must also replace the circular fit).
