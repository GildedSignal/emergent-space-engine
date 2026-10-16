Working...
Check complete. **Grade: gold** — written to `lab/results/20261016-1319-second-20261016-1207-taleb-f094-8a40/check.md`, with the author's wiki page corrected in place.

**What was verified:**

- **Reproduction:** runner's regen (exit 0) plus my own clean-tree runs. Count-class numbers exact (leaver totals 43/43 and 361/361, opens = leavers, dec 0/1, prof call counts 250→542, 24→608, 577, drains 30/82/130/115, latch peaks 54/157, lag caps 1.433–1.667). Wall-class numbers within noise; every divergence recorded in check.md.
- **Predictions:** held/missed accounting is honest; the two disclosed misses confirmed; kill criteria never fired in-domain; the original record's two unreported misses are now named (matches check2.md verbatim).
- **My attacks:** held-out **seed 5** — everything holds (352/352 ×2 per arm; a first parallel batch's 351/352 and 900 µs readings were withdrawn as my own contention + drain nondeterminism). **Fleet 2000** (next decade) — totals/cap/price hold but the latch does *not* recover (plateau 381 growing +5/frame at f150, coast hs = 0): the "growing at f150" criterion fires outside the tested fleets; folded into the page as a boundary. **Levels 1/6** — 2.7/28.5/72.4/132.6 ms: monotone, *not* level-proportional; page corrected. **Belt 1e4/5 ms** — plateau ~420 by f500 (3× N=0, ≪ 2048) and the leaver gap unresolved at f500 (365 vs 374): the author's fenced residue is real, now with numbers.
- **Page corrections (2):** the per-flush arithmetic — the prof call counter shows ~290 extra `bind_surface` fits at ~430 µs (one hand-out bind each), not "499 fits at ~195 µs"; the mechanism claim actually gets *stronger*. And "level-proportional" replaced with the measured shape.

Gold because: reproduced exactly where it matters, held-out predictions held (author's + my seed), and the premise "the composition might add an unowned smoothness term" is shown wrong — completing the silver run's checker-named gold condition, adoptable in one step (page only, no engine change). Tree left pristine; nothing committed or pushed.
