Working...
Check complete: **Grade: silver**, written to `lab/results/20261014-1137-inversion-62c1/check.md`, with the author's wiki page corrected in place where it overstated. Tree restored to the runner's clean state.

**What I did:**

1. **Reproduced independently** — applied `work/patch.diff` to a clean tree myself, ran the dossier's exact 10³ command: 21.43 ms p50 (author 21.5), gather 19.29, census identical. The runner's full regen matched at every rung (2,611 vs 2,614 ms at 10⁵).
2. **Verified the probe against the shipped sources** — `Session::step` is exactly engine(5 ms)→`gather_cached`→`view_json`→`to_vec` inside the served frame; page.html's rAF/`fitLog`/draw-test/edge-marker logic matches the census instrument; the population is the ladder's own (`nladder.rs:52`).
3. **Three adversarial cases:** seed 2 (robust: 255.6 ms at 10⁴); **N=3×10⁵, past the author's top rung** — the linear law lands exactly (7,831 measured vs 7,833 extrapolated, 77.5 rows on-canvas, sky-static ~100%, 1.57 GB peak); **belt-zoom census** — the on-canvas set is ~N itself (10,060 at 10⁴; 300,067 at 3×10⁵), so the "visible set is O(10²)" fact is strictly a fitted-zoom fact, and at zoom-out only the display quantum caps work. That last one is why I corrected the author's page ("≈10² rows/frame at any N" → domain-bounded) plus two number ranges.
4. **Novelty:** the headline composition is already printed in the merged `ladder.txt` ("the page pays it"; "the page's 16.7 ms frame cannot carry it past ~10³"), and the view page held the constraint at 28–948 bodies — the run measures and sharpens a named term rather than finding a new one, and the ~10³× lever is projection. Silver: the gold experiment is building the row-set deletion and measuring the frame at scale, both zooms, one turn.
