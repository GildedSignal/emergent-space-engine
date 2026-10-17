Working...
Check complete. Verdict: **Grade: gold** — written to `check.md`, with the author's proposed wiki page corrected in place where it overstated.

**What I did:**

1. **Reproduced** — the runner's regen (exit 0) matches every verdict: 18/18 frames arms survive with 0 asserts; on-grid chunks (96/112/128@864, 512@14k) never crash; interior chunks crash (100-s1 2/2, 104, quiet-150 "region 13279 from 112 … published tick 150"). Counter differences are disclosed draws (quiet frontier 1,136 vs 3,072; 28k-s1 1 region vs 2,912; rel frontiers ≤2,992 vs 8,096) — all recorded in check.md; the crash-tick-window coverage regenerates even where depth doesn't.

2. **Code-verified the mechanism on the shipped tree** — `goal_tick` 557–564 (frames goals grid-aligned via `.ceil()`, batch goals raw), `next_unit` 762 (stride ends `min(boundary, goal, next_sync)` — interior only under batch), `certify` 1086–1108 (window-keyed, spatial-only clash = conservative in time), `finished()` 1666, forced publish 1937–38, assert 1451 verbatim. The Newtonian correction of 9b46's dossier is code-true (`World::new` law.rs:168).

3. **Five adversarial arms of my own, 0 asserts**, including two outside the author's battery: the missing paired control (quiet-14k **on-grid** chunk 160 on the exact crash scene → DONE full horizon with rb=5 post-publication conflicts in the crash window) and 55,584 bodies (on-grid 96, 5 publishes), plus off-beat cadence frames (hz 53/rate 97) and 2.2×-exposure 28k frames. Nothing refutes; grid alignment closes the observed channel exactly as claimed.

4. **Novelty** — executes the page's open direction 2 (frames "untested"), refutes open direction 1's engine-side fix, replaces it with a one-line driver rule. Gold: reproduced, premise-refuting, adoptable in one step. Tree restored to the runner's clean state.
