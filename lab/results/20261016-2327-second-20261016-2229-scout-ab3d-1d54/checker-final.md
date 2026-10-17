Working...
Check complete. `check.md` written: **Grade: gold**.

**What I did**

1. **Reproduced**: diffed the runner's `regen-run.jsonl` against the author's `run.jsonl` — 355 cells identical, 0 non-timing diffs (timing cells <1%); every dossier number traced to the record. Verified the constants in the shipped code itself: `scenario.rs:10,344` (belt ships = `Scalar::raw(34,-10)` = 49 m), `encounter.rs:18,177` (near = 2¹⁰·(r_a+r_b) = 68 root units, self-pair skip), `radial.rs:8`.

2. **Predictions**: pre-registered (file times confirm), held-out seeds inside bands; the one failed band (short-h series keep) honestly reported with the correct mechanism.

3. **Attacked outside the author's range** — all held:
   - co-located adversarial hits extended to e = 0.99/0.995/0.999: miss = 0, and miss_old = 1 at e = 0.99 (the closed-form fix stays load-bearing);
   - 40,000 crafted guaranteed hits at **random querent phases** (author tested only the max-margin phase), e up to 0.99, half with e=0.3 tail-stress partners, at h and at **10× h**: zero misses in both stages;
   - **N = 10⁷** λ-pass (a decade past the author's 10⁶): keep1 0.10880 vs 0.10884 — fraction N-stable, cost linear;
   - the closed-form margin independently verified against a dense Newton grid in Python: dominates everywhere, agrees with the grid sup to 5×10⁻¹¹ (margin(0.6) = 1.261453).

4. **Novelty**: no earlier margin closed form or two-stage certificate in HISTORY/git beyond the silver this run corrects — it is the silver's named gold experiment, done.

5. **Page**: faithful; I corrected two timing cells in place (`2.7–3.5 ns`, `48.5–48.8 ns` — the page's bands didn't cover its own record's cells).

Gold because: the answer walk 418 ms → 2.1–2.2 ms at 10⁵ (~190×) on a 14-second regenerable record, a real soundness fix demonstrated load-bearing, honestly scoped domain (bar to querent e ≈ 0.6, 10⁶ marginal), adoptable in one wiring step. Recorded what the author missed: vacuous natural-scene soundness rows at the true point, retrograde orbits untested (extends by mirror symmetry, but wiring must carry direction), a latent bracket bug in `m_of_nu` at high e, and the shared float-replica frame.
