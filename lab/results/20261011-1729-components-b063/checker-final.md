Working...
Check complete. **Grade: gold** — written to `lab/results/20261011-1729-components-b063/check.md`; tree restored to clean (only untracked `lab/results/`).

**What I verified:**

1. **Reproduction (clean tree, patch applied myself):** digests bit-identical (`eccc7f5a…`, replay `0e02bf0f…`), 1,158 samples, refused 0, memo block identical (exact hit 0%, 1,125 rebinds); timings within 3% (77.4 µs vs 75.6 median). Floor recompiled and reproduced: 41.5–42.9 ns (3-source), 2.2 ns (memory only), 125–161 ns (random order), plus an extra L2-resident case (43 ns with field at 16 MB — the field is the arithmetic floor at every cache size).

2. **Adversarial:** unseen seed 7 holds the decomposition (rest 88%). I closed the one split the author admitted leaving unmeasured by instrumenting `bind()` directly (probe reverted): **63.5–64.4 µs/call** over 2,438 calls against `rest` ≈ 67.4 µs — the tube refit is ~84% of the whole kick; the ext step-derivation alternative is dead (0.9 µs, 12 calls).

3. **Predictions:** pre-registered (mtime order consistent with internal timestamps), honestly scored — P1's leaver miss disclosed, and it strengthens the claim.

4. **Novelty:** H0210 records only the 29 µs figure; no entry decomposes the kick or measures a floor. The memo kill corroborates the 5 October taste log rather than repeating it.

**Two corrections noted (grade unaffected):** the floor's 3 sources understate the plane's ~4 (star + 3 planets) → honest index ~1,400×; and the "plus step re-derivation" parenthetical mis-weights — the refit is effectively all of it. The unmeasured read side (where the fit cost moves) is flagged as the builder's first measurement.
