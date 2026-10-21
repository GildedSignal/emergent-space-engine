Working...
Check complete. **Grade: silver** — written to `lab/results/20261021-1551-scout-033c/check.md`, with the author's page corrected in place.

**What I did and found:**

1. **Reproduction** — `regen.sh` re-run: `census.csv` byte-identical, 112.9 s (claimed 112 s), deterministic single-threaded f64; `patch.diff` empty (truly no engine change). File times confirm `predictions.md` (16:01) preceded the instrument (16:04) and dossier (16:09). All four arithmetic anchors re-derived and check (Moon tide 3.39e-24 vs measured 4.39e-24; the 110×/decade is 110.9×).

2. **Adversarial cases** (two outside the author's tested range):
   - **r = 15,000** (untested): Xi 2.162e-4 vs 2.08e-4 predicted by the r² law — the death law is real and now confirmed at an independent radius; fork at 69 kicks moves the kill boundary to ~1.5×10⁴.
   - **r = 250,000** (inside the Moon's shell): fork at kick 1, 61–98% disagreement — everything word-based dies; nothing wins near the Moon.
   - **Moon-phase sweep** at the headline arm: the 682–716 first fork moves 682→3,367 with phase; a mechanism probe shows the fork is the *common-mode wrap straddle* (S_r = 2.0000334 vs S_m = 1.9995645 quanta at k=716), and dx ≤ 316 pushes it to 21,484 — a lottery integer, not a certificate law.
   - **Steady-state inversion from the author's own census**: at 4,740/dx1e4 the stream is 99.84% shared (0.16% disagreement) vs the 1 AU control's 95.5% — the LEO-lattice kill is not in the evidence, and the pre-registered kill criterion ("Xi < 1e-3 ⇒ child-doll families as cheap as star-doll") fired unaddressed.

3. **Page corrections**: "residue 20–30× below at every arm" is false (1.4×–3,000×; *exceeded* at star-doll dx ≥ 5e5); the belt horizon "2.5e3–1.3e4 kicks/160–850 orbits" is the best arm alone (true cross-arm: 554–13,512 kicks = 35–845 orbits); "≤5 kicks above 10⁴" corrected to ~1.5×10⁴. No-crossover inside child dolls stands on the corrected domain.

4. **Silver, not gold**: predictions didn't cleanly hold (P1 miss at dx1e6; P2's 2¹⁷ horizon silently redefined; P3 off by 10³ with a post-hoc fix). The one gold experiment: phase-ensemble steady re-sync rates (the instrument already records `disagree_frac`) at 4,740 and the belt — one run, no engine change.
