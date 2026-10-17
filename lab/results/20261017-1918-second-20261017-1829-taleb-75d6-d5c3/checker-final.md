Working...
Check complete. Verdict written to `lab/results/20261017-1918-second-20261017-1829-taleb-75d6-d5c3/check.md`:

**Grade: gold.**

Evidence basis, all from my own runs in a clean tree (patch applied by me, tree restored to pristine after):

- **Reproduced exactly.** Every decisive number matches `analysis.json` to the last digit: s1 K2 ratios (on 2.81/2.54/3.02, sym 2.46/2.43/3.03 on ln a/e/ω), K5 ρ = 0.904/0.898/0.902, ref-free medians 2.09 vs 2.08×10⁻⁷, off−ref9 band 6.48×10⁻⁸; seed 2 fires harder (ω 3.82/3.91); C1/C4/P8/P5 all hold; my seed-2 CSVs are byte-identical to the record's data rows.
- **The mechanism claim is real.** The symmetric clock-start arm pays the same per-body term as ed3a's asymmetric one — the successor named by 75d6's checker is cleanly refuted, and the patch's construction is verified in source (`plan_clock_at` clears and re-derives at `t+off`).
- **The horizon-bug diagnosis is proven, not just argued.** 75d6's regen (read off its branch) reads seed-2 arms at +2·P_min and its reference at +1·P_min; the off arm's *own* one-orbit drift reproduces 75d6's stored "drowning" to four digits (2.004×10⁻⁴, 6.23×10⁻⁴, 7.73×10⁻³). Instrument bug, not resonance physics.
- **Adversarial beyond the author's range:** seed 3 (never tested) fires harder still (e 4.31/4.34, ρ = 0.97); at 4 orbits the differential decays to 0.53–0.65 of its one-orbit size — the one-time typing extends a decade past the measured horizon.
- **Novelty:** HISTORY holds no stagger entries; the published wiki page explicitly left this as an unmeasured hypothesis.

Page correction: none needed — the fold-in is faithful; its only flaw is an *understatement* (seed 2's e fires 3.70/3.94, above the quoted 2.4–2.5× range), noted in check.md. Topic stays open (75d6 is silver, not three golds).
