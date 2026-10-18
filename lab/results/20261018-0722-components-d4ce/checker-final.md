Working...
Check complete. **`Grade: silver`** written to `lab/results/20261018-0722-components-d4ce/check.md`, with the author's wiki page corrected in place where it overstated.

**What I did:**

- **Reproduced every load-independent claim.** Verified the runner's stored artifacts myself (digests identical and equal to the committed nladder record; 10/10 bank rungs with 0 non-timing diffs — I extended the comparison to `.q.tsv`, which the author hadn't checked); re-ran 75 tests in debug (asserts live) and release; re-ran the 2M-quotient sweep.
- **Three adversarial cases, one outside the author's domain:** (1) 180 dense near-separatrix keys at p = (6+2e)(1+t), t down to 3×10⁻¹⁰ — the `word_root=false` band the dossier itself calls "the one unflown corner" — full compile hashes bit-identical; (2) `N=1000 belt crossing` digest (outside their N=3000 set) — identical; (3) a `div_word` sweep on the four sites' exact operand shapes at the precondition boundary — exact everywhere. I also strengthened the certificate: the exactness is **structural on the whole compiled domain** (fast gate ⇒ root ≥ 2⁴⁶; separatrix refusal ⇒ horizon > 2⁶¹; join clamp ⇒ floor ≤ x), so the author's feared corner is empty — they under-claimed their own proof.
- **Found the real weakness:** the headline magnitude is not a stable number. The author's quiet-pass CSVs were overwritten by regen (not regenerable), and my clean drift-controlled triple (BASE→PATCH→BASE, −0.3% drift) reads p50 0.9% with the patched arm 1–2% *slower* per panel; clean banks mixed. Four passes span 0–15%. The core claim — far under od 7's ~25%, division slice dead as a lever — survives; "~5%" does not. The decisive prediction P3 failed (honestly reported), which bars gold; the wiki's "R2/R5 unchanged" was contradicted by the stored pass (−10.8%/−5.3%) and is corrected.
- **Gold-making experiment named:** an interleaved-arms, CPU-pinned paired measurement fixing the in-situ Δ with a confidence interval — stable-positive lands the number, stable-zero makes the refutation total.

Tree restored pristine; no commits, no pushes, nothing else in the run folder touched.
