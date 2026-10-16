Working...
Check complete. Summary of the verdict (written to `lab/results/20261016-2229-scout-ab3d/check.md`):

**Grade: silver**

**Reproduced:** clean tree, empty patch — all 26 scene rows of `run.jsonl` regenerate bit-identical (13.7 s); costs land in the dossier's band (series 48.7 ns, Newton 269.5 ns; only the stage-1 pass runs 3.2–4.0 ns, above the dossier's stated 2.8–2.9). `predictions.md` (22:37) predates the decisive run (22:50).

**The adjudication the author deferred resolves against the run.** The belt branch of `scenario.rs::ladder_ship` (line 344) ships `Scalar::raw(34, -10)` in doll-0 units — **49-m ships**, near = 68 root units = 6.71×10⁻⁷ AU. The author's "34·2⁸ root units = 12,850 km" reads the *local* branch's constant, which is the same 49-m radius expressed in Home-doll units (2⁻¹⁸ root each). The dossier's "shipped operating point" is 2¹⁸ too large; my rerun at the true point gives 0–1 truth hits per 10⁵ scan — 3999's ZERO encounters reconciles exactly (no "frozen log" needed), and the dossier's dramatic wall ("truth 0.53%·N, no filter meets the bar at 10⁶") describes a counterfactual Earth-sized belt.

**What survives at the true point (my adversarial rerun):** 0 misses in 27 truth-checked scenes — including seeds 2–3, which the author ran with `check = false` (the dossier's "all 22 checked scenes" overstates; 12 were checked) — plus fresh seed 7 at 10⁶. S(10⁵) = **1.79 ms** with the shipped 4.2-µs readout: the bar claim holds, ~230× under today's 418 ms. At 10⁶: 17.9 ms with the O(N) pass, ≈6.4 ms with λ-index + 0.5-µs readout — marginal, not the dossier's "≈4.8 ms, under". The tight-axis refutation of 3999 (EoC series at ~49 ns ≈ 1/85 of the readout) stands — that is the run's real, novel contribution.

**New failure found (crafted case):** a querent at e = 0.6 — above the margin table's 0.4 clamp, an orbit the *player* can fly — misses a guaranteed truth hit (`margin_of` gives 0.816 rad, true max|ν−M| is 1.2615). Belt bodies are safe (genesis caps e at 0.4); wiring must extend the tables.

**Page corrected in place:** the Current-best paragraph and the Runs line now carry the code-derived operating point, the corrected soundness coverage, the marginal 10⁶ reading, and the e > 0.4 constraint, with `[checker: …]` brackets. Nothing else in the run folder was touched.
