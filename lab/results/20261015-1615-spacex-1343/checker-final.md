Working...
Check complete. `check.md` written, wiki page corrected, tree restored to clean.

**Grade: silver** — `lab/results/20261015-1615-spacex-1343/check.md`

**What reproduced (clean tree + patch, my own runs plus the runner's regen):**
- Bench byte-for-byte: 96.0 B/panel slope, 10.74 panels/octave past the 2¹⁰ join (matches `orbit.rs`'s `join = 2^-10` and the 15/16 shrink in code), knots 145→161→saturated, re-mint identity 0/64 at every w, cycle control 6/10/19/37/58 knots.
- Flights: coast censuses 632/668 B/body; burn exactly 1 passage (w=2, 1,808 B); comet12 2,000 alive at w=14/18,800 B; comet13 990 dead at the loss radius, w=15/19,856 B.
- Code claims verified: `body.rs:193` placeholder 4096 (2.26× over at w=2, 4.59× under at w=14), `Trajectory::key()` None for Plunge only, `Passage::compile` pure in its two arguments, `radial.rs:16` unbounded=always-candidate, `binding.rs:400` loss radius 2⁴⁰.

**Adversarial, beyond the author's domain:**
1. Second compactness class (peri ~200× tighter, e≈1.0 vs 1.5): **identical knots and panels at every matched w** — the price curve is universal in w; a free strengthening the author missed.
2. w=70/80/100 all compile (968 panels, 108 kB at w=100, identity 0/64): the wiki's "the law's w=61 edge" was wrong; corrected.
3. Tight-peri flights at comet12's r0: peri 0.15 AU → w=16/21,104 B alive; peri 0.006 AU (1.3 R_star) → **w=20/25,520–25,712 B, 1,000/1,000 alive** — the "structurally capped at w≈15 / worst case 18.8 kB" claim is refuted: the cap is on the minted outer radius, not w; honest worst case ~26 kB ≈ 213× the 120 B record.

**Why silver, not gold:** P2/P5 failed as written (honestly reported, with correct diagnoses — precedent: one failed held-out caps at silver), the worst-case domain was overstated, and the demote-passages deletion itself was not flown on the seam — the same bar that separated 760f from e0f9. **The gold experiment:** fly the two-line demote-set variant digest-identical on the standard ladder plus a mixed-peri comet stream, measuring the in-flight re-mint bill against the corrected 25.7 kB worst case.
