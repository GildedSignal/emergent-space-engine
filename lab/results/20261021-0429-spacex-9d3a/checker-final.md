Working...
Check complete. **Grade: silver** — `lab/results/20261021-0429-spacex-9d3a/check.md` written, author's wiki page corrected in place, tree left pristine.

**What reproduced:** everything structural. My re-run matched bit-for-bit (4 zero-post-birth gens in 100,032/300,032/1,000,032; live 10/20/60% at 1 frame/1 s/5 s; ~8.7 view decodes/body/gather; 2,424–2,447 B/body; misses = 0), seed-stable at seed 7; `predictions.md` (04:41) precedes the decisive 1e6 arm (04:49).

**What broke (my adversarial control, view=none — never flown by the author at scale):**
- 99.78% / 99.93% of belt bodies at 1e5/3e5 get **zero post-birth engine reads** over 20 s (99.76% over 50 s); only 219–240 build-born bodies are ever engine-read; in-flight engine reads are **identical (87,264) at 1e5 and 3e5** — not ∝N.
- The dossier's "engine observe path sweeps ~1%/frame ∝N" is an arithmetic artifact: the engine read bucket is 89–99% the build's own frame-0 birth decodes (~8/body) divided by frames (1e6: 8,055,419 ≈ 8 × 1,000,032). Steady engine rate: ~95/frame at both scales.
- The engine is event-bound — the board's premise survives; the sole population-wide reader is the harness's oracle `gather_cached`, whose wall and cure are already the view row's adopted golds (flyable-frame 220×, skyserve flat-in-K), and 4ea0 (gold) already killed eviction (×98 builds). The 440-core demotion bill is the gather's bill and collapses under the row-set gather; the proposed "kill the sweep via wt/cadence" lever aims at a sweep that doesn't exist.

**Silver's one gold experiment:** fly the census under the adopted row-set gather — if the live set is event-bound there, the row's closure becomes "demote once the view stops walking N," premise restored with a number.
