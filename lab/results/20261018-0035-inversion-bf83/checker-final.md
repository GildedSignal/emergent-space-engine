Working...
Check complete. **Grade: gold** — written to `lab/results/20261018-0035-inversion-bf83/check.md`, with the author's wiki page corrected in place. Tree restored to clean.

**What I did:**

1. **Reproduced the decisive event independently.** Applied `work/patch.diff` (one example file, no engine change), verified the engine facts (`alloc.rs:1451` is the shipped assert; `Config::default` = margin 2.0 / `min_region 32`; shipped finality tests run at margin 0.0), then ran 46 battle draws of my own: **3 fires in 12 margin-0.5 draws, every one seed 11** — matching the author's seed and their P5 skew law. One fire at a 4× horizon (20 s, present ~15k). Pooled across author/runner/me: 4 fires / 62 draws, all seed 11.

2. **Adversarial cases:** rate 600 (the axis the author's predictions promised then dropped) — it's the keeping-up rate, present pinned at 2,698 on every seed, 0/12: the axis is dead. Fresh seeds 21–24: 0/8, profiles unchanged. Margin 0.0 on gas × 3: present 3.1k–4.7k, never stalls — **the dossier's "present stalls at chronon 3" collapse claim is refuted** (degradation, not ruin); corrected on the page. Also scoped "crossings never fire" to this horizon (bc0f has a crossing crash in other windows).

3. **Novelty:** first use of `worlds::galaxy` in any harness; all prior fires were selfchurn/batch families at `min_region 1`. The run's strongest confirmed sentence: the battle conflicts **at shipped `min_region 32`** (rollbacks 1–5 everywhere) where bc0f's churn family was strictly clean there — the game's fleets reach through the knob that protects every synthetic scene, so direction 1's fix tests on fleets, not gas.

4. **Blemishes recorded:** the runner's own regen saw 0/53 (fires are load-coupled — mine all landed in concurrent batches, 0/8 in a quiet loop); two dossier number ranges aren't backed by any saved artifact; P1's failure is disclosed and its diagnosis verified by my fires. The next run is named: port e517's PRE/HAZ instrument to the fleet scene to make the fire state-decidable.
