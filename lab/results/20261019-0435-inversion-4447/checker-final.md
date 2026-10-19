Working...
**Grade: gold** — written to `lab/results/20261019-0435-inversion-4447/check.md`, with one checker paragraph folded into the author's proposed `wiki/nladder.md`.

**What I verified:**

1. **Reproduction** — runner's regen (exit 0) matches every load-bearing dossier number: guard stops at 560,862/332,604 gs, window slopes 1.1/5.7/0.8/1.7/2.3/2.9/3.2 (10⁴) and 4.4/**16.3**/1.1/2.9/3.0/**4.6** (3×10⁴), final-40% 3.02/4.56, RSS@360k = 988.8 MB, held strictly monotone 0→741/589, coast flat 0.02 MB/1k gs over 800k gs with held_max 1. Timing-elastic digits (coast end 61 vs 70 MB, worst 42.5 vs 43.0 ms) differ exactly as two independent flight sets should.

2. **Predictions** — mtime ordering consistent with pre-registration (predictions 22m < flight logs 17m); P1/P3/P5 held, P2 honestly reported half-held, P4 disclosed qualitative.

3. **Three adversarial arms, all outside the author's grid:**
   - **Probe-off** (shipped loop): 1,001 MB at ~365k gs, held_max 593 — instrument exonerated.
   - **K=3×10³** (below the grid): ratchet reproduces, slopes still rising at 288k gs; mid-flight slope now K-proportional on **three** rungs (1.74/5.68/16.33), and the held trajectory is K-identical while bytes scale with K — the K term is per-retained-scan size, not count.
   - **5 ms corner**: same slope shape, 582 over (0.39%) — memory channel budget-insensitive.
   - Plus backlog-cap arithmetic: SCAN_BACKLOG's 2048 cap engages at ~2.3M gs, *after* the 4-GiB breach in both arms.

4. **Novelty** — d839's "then flat" and dcf1's "wall gone by ~3 orders" are both standing wiki claims, and both are truncation artifacts this run corrects with a 12×-longer burn horizon and a same-horizon coast control. No HISTORY overlap.

Gold rationale: reproduced, held-out predictions held, shows two premises wrong on the "memory at 10⁹" board item, adoptable in zero steps (restores the byte-count-at-capture + answer-or-expire fence as a live requirement before any 10⁵ burn). Tree left clean; my arm logs sit in `/tmp/check4447/` (run folder untouched beyond `check.md` and the page correction).
