Working...
Check complete. **Grade: gold** — written to `lab/results/20261011-2132-second-20261011-2028-system-3b42-214f/check.md`.

**Reproduction:** patch applied, all four modes rebuilt and rerun. Belt byte-identical to the original branch's commit; straggler 11/11 lines identical; coorbital counters identical. One exception: `naive_pairs` in strongfield wobbles (stored 2,762,416; my five runs 2,762,406–2,762,416) — `cells` comes from an unsorted HashMap, so the dossier's "bit-identical in every counter" is wrong for that cosmetic digit.

**Adversarial cases (probe removed after use):**
1. Three held-out straggler seeds: misses 0, arc/W ≤ 0.838, cand/enc 5.34–5.62 — the frozen window generalizes.
2. 5× horizon: misses 0; `misses_nocl` 0→11 at the closure-matched dial proves the closure term, not the dial, carries the physics; saturation behaves exactly as disclosed.
3. 4× eccentricity hot band: misses 0; top cells saturate to all-pairs at w = π honestly.
4. Full-domain U scan (E from √(8/9) to 0.9999, deeper belt r_p ≥ 4.19): turns 0 everywhere — the no-turn answer is not belt-bound. Turning-point algebra verified independently to 5.4e-13.
5. **Found what the author missed:** the strong-field 5×5 compile is sampled, not structural — near-circular belts leak constants (77–149 of 3000 cell violations, two seeds; the author's belt gave 0). No measured miss, but the guarantee isn't closed outside the shipped belt. Also `naive_miss` is tautological (window fitted to the close set).

**Why gold despite that:** both of checker-1's named gold experiments are delivered with pre-registered predictions that held; every load-bearing number survived adversarial cases broader than the author's; the rank-k→arc-window correction is measured and mechanistically explained (kappa_req constant → rank ∝ m). The compile-hardening sits inside the single adoption step, and the GR phase bound remains disclosed-unmeasured. Tree restored clean; nothing else in the run folder touched; no commits.
