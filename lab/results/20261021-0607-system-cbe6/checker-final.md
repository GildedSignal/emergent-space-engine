Working...
Check complete. **Grade: gold** — written to `lab/results/20261021-0607-system-cbe6/check.md`.

**Reproduction:** runner's `regen.sh` exited 0 and regenerated `ladder.txt` matching every dossier number; I re-applied the patch to the clean tree at `595fdd47`, rebuilt, and confirmed bit-level determinism (36-ship run's first six ships = the author's numbers to the digit). The example is `jacobi.rs` verbatim plus exactly the four claimed deltas.

**Predictions:** existed before the decisive run (mtime order 06:17:38 → 06:27:28 → 06:30). P1/P2/P3/P5 held; P4 half-failed and is honestly reported — and the miss is the finding (the conjunction is the binding unit: 8/conjunction holds, 4 fails).

**My adversarial arms (all support the claim):**
- **Horizon 4× (outside the author's range):** step 4 over 400 planet periods — worst 1.2e-5, no walk.
- **Exact 3:1 commensurability** (seed placing ship 0 at 2.50056 AU vs 2.50054 exact): passes at step 4 (7.9e-6), fails at step 3 like the others — in-range resonances are order ≥ 2, so the domain edge is real but not load-bearing.
- **72 further draws** (36 ships × 2 seeds): all pass, 8.3e-6–1.6e-5.
- **Strong control at 36 ships:** 8/36 dead at step 4 — the cliff is a class property, not draw luck.

**Novelty:** prior art is replica-side (7f97 "bulk 16/period", 06a8 8/orbit probe, ad35 float n⁻²); the new content is the floor on the shipped instrument against B12's frozen bar, with the conjunction unit, cliff, and draw-stability — the replica→shipped upgrade this wiki uses as the silver/gold line.

**Page corrections (in place):** "the plane's own belt draw" overstated — radii only, circular starts vs the plane's Rayleigh e≈0.07 (the real domain edge is the eccentric tail, which the class census must size); Hill range fixed to 6.2–9; current best trimmed 36 → 12 nonblank lines (would have been flagged); `valid-while` set; my arms folded in. Runs intact (the two "dropped" entries were live-page duplicates, correctly deduped).

Tree left as found (`beltcad.rs` removed, live wiki untouched, nothing committed).
