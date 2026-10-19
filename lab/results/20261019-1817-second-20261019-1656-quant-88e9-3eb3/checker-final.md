Working...
Check complete. **Grade: silver** — written to `check.md`, page corrected in place.

**What reproduced (from the runner's regen + my own recomputation):** every dossier number within ≤1% jitter — rung B (1.633/1.591, closures 0.954/0.930), rung A′ as-registered letter FAIL and post-onset passes (streams 3,240/1,689 vs share 3,242/1,687), rung C wall (guards 38,764/90,007 gs, 5.3/9.4 KB/kick machinery, wall-life 2.32×), calibration exact against 88e9's digits. The patch is 88e9's verbatim plus exactly the two claimed deltas (verified by diff against the 88e9 branch); `stats.kicks` is shipped engine state.

**What my attack found (4 adversarial cases, 2 outside the author's grid, refusals 0/dead 0 on all):**
- **Seed 7 at 3×10⁴:** all four B-criteria pass — but stream ratio 1.721 vs share 1.587 (+8%) kills the "nil seed spread on the primitive" claim.
- **Seed 3 at 5×10⁴ (the decisive one):** the onset mechanism holds (closure 0.211 pre-onset, suppressed like seed 1's 0.157), but **both registered ratio bands fail** — stream 1.447 vs [1.73,2.11], slope 1.393 vs [1.70,2.15]. Isolated mechanism: the locals are not scene-fixed — quiet-region L ≈ 1,81–1,83 at seed 3 vs 1,466–1,486 at seed 1 on identical cuts (+24%), in both arms. The mint identity itself survives (closures 0.87–0.96 post-onset). So "holds at both rungs" is seed-1-specific at 5×10⁴ — exactly the named experiment's success condition, unmet in the seed dimension.
- **Onset-as-time-constant:** independently confirmed from the shipped seed-2 logs (pre-onset closures 0.25/0.33 at 3×10⁴) — the run's most robust physics; the wave-index reading is dead at three seeds × two rungs.
- **Prior art:** the page's own b911 block already records K=10⁵ guard at gs 38,033 — rung C's unflightability was known; new are the ON trip, wall-life 2.30× (≈2.2× under matched guards — OFF/ON flew 1,750/1,800), and the per-kick decomposition.

**One experiment for gold:** a seed ensemble at 5×10⁴ with L measured per flight (the ON quiet-region cut separates L(seed) from B/8 free) — it decides whether the share law is an identity or a mean law, and with it the 10⁶–10⁹ column's status.
