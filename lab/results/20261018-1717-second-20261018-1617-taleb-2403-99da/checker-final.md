Working...
Check complete. **Grade: gold** — written to `check.md` with the full evidence trail, and three overstatements corrected in place on the author's `wiki/nladder.md`.

**What I verified:**

1. **Reproduction, exact on every invariant.** The runner's regen exited 0; my own independent parser recomputed all eight arms from the raw `.err`/`.txt` outputs — entries, census, λ, the 16.8×/13.15× ratios, b_per_body (2,338/2,347–2,349), footprints, truncation flags all match `analysis2.json` to the digit. The claim is stronger than its letter: the full `t=`/`cls=` stream (not just count and census) is byte-identical between 10⁵ and 6.5×10⁵ in coast (145), burn (2,069) and burn-b24 (2,071). The cross-check against 2403's second checker's published coast flight holds identically (game 1898.5 s, kicks 3624, events 11115, boundaries 3499); digest neutrality confirmed (`20a45aa4…`).

2. **Predictions: the letter matches the log** — the exact bar 2403 fell on. P3's band (held ≥ 400) failed and is reported as failed; a post-hoc band would have passed. The 2403 P1/P6 corrections are accurate against its own tables (0.0027/0.431; +21 MB).

3. **Adversarial, two outside the author's grid:** a third K = 3×10⁵ (never flown by anyone) — stream bit-identical to both flown K; a 10-wall-s cadence at both K — identical 96-line streams, so the K-identity is not a single-cadence artifact. Wall arithmetic checks (42.78 game-s; acf2's coast convention reproduces 679 ≈ 687; 2,465 B at 10⁴ verified on 2403's branch; 2.34 GB > 2 GB genuinely forces the slice).

4. **Novelty and fit:** the 2403 second checker's named gold experiment is done as named, on a regenerating record, against the memory-at-10⁹ board bottleneck (PRINCIPLES 5, 12, 14).

**Page corrections (my only edits besides check.md):** the 12 ms held elasticity range widened to 206–275 (the runner's pass measured 275/266), "both corners reproduce exactly" narrowed to the 31 (the 5 ms corner moved 707→701), and the p99 pair quoted in pass-stable digits. What the author missed, recorded in check.md: the wall's honest form is a band (≈43–51 game-s) until cadence vs convention is separated, and the (K+38)·224 B byte law remains inherited, not re-measured at the slice.
