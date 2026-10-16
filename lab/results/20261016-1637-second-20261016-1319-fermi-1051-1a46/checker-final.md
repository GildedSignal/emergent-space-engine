Working...
Check complete. Verdict written to `check.md`, page corrected, tree restored to pristine.

**Grade: gold.**

**Reproduced (clean tree, my own `git apply` + build + flights):** every number exact — OFF 334/136 max/p99, 22,219 events, 9,217 kicks at 5,400 game-s (the 4fa8 record bit-for-bit); ARM 131/26, 6,580, 1,382; envelope and the 3173 beat frame identical; the arm's state dump byte-identical to the regen copy; my patched build's `ladder_digest` equals the pristine binary's output (13 cases × 4 schedules; the pristine binary verified clean — no `ES_SECULAR` strings, and `ladder_digest.rs` has no macOS deps).

**Four adversarial probes, all held, two outside the author's domain:**
- **Seed 2:** digit-identical to seed 1 in both arms (the comb is clockwork, not a seed artifact) — closes the author's own admitted miss.
- **N=10⁵** (a decade past the author's 10⁴): N-flat holds, 46/33, 237 MB.
- **Burn L8:** delete holds, 328→105 max; player/fleet untouched, no deaths.
- **11,000 game-s** (2× horizon, rtf 200): storm bounded at 131, ledger cut deepens −70%→−83%, kicks −90%, marginal event rate ≈ 0 — *stronger* than the dossier's own claim.

**One softening, corrected on the page:** the fence bar "|Δangle| < 10⁻⁴°" is probe-horizon-bound — at 11,000 gs the deleted set's max |Δangle| is 1.2×10⁻³°, still ~3 orders under r9's per-orbit bound and on the dossier's own ~10⁷-gs schedule (debt emerging as projected, not a refutation). Spared sets stay bit-identical (0.000000°) and the legality set is horizon-stable.

**Novelty:** `git log -S ES_SECULAR` empty; the page's fermi-1051 entry is arithmetic-only ("no flight"). This run flew the checker-named experiment, adjudicated the composed candidates (134-class wins at 2.5%; proportional 83.5 refuted at 57%), and corrected both prior legality numbers (85.8% in-situ, Moon's line 116,333 ru — arithmetic independently reverified). Predictions were pre-registered with genuine failed sub-calls, honestly reported. Page folding faithful; standing merge conflicts correctly left for `wiki.py`.
