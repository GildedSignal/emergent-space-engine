topic: live-residency
status: open
closed-by:
valid-while: crates/universe@f7c3 + 20261021-0429-spacex-9d3a's patch (rcensus.rs, Entry Drop hook, orbit_state/readout/mint hooks, example rcensus)
updated: 20261021-0429-spacex-9d3a

# The live set's residency: what pins a body's compiled orbit between its events

## Current best
- **Under the oracle view gather (`gather_cached`, O(N), one gather per 10 s), demotion to the compact store is dead: essentially every belt body's compiled orbit is read** — 4 zero-post-birth generations in 100,032 at 1e5 (seed-stable), 4 in 300,032 at 3e5, 4 in 1,000,032 at 1e6 (20 s flights, coast, rtf 100; 1e6 truncated at 600 frames) — against ≤ 3.6% of bodies touched by kicks.
- **The only population-wide reader is the view gather: ~8.7 decodes per body per gather, 66% of all reads at 1e5** (view.rs walks `0..n_bodies()`, no horizon cull). **The engine is event-bound [checker, view=none control]: 99.78%/99.93% of build-born belt bodies get zero post-birth engine reads over 20 s at 1e5/3e5 (99.76% over 50 s); only 219–240 build-born bodies are ever engine-read post-birth, plus the in-flight rebinds (~21 reads each; 87,264 in-flight engine reads identical at 1e5 and 3e5 — not ∝N).**
- The dossier's "engine observe path sweeps ~1%/frame ∝N" is an artifact [checker]: 89–99% of the engine read bucket is the build's own frame-0 birth decodes (~8 a body) divided by frames (1e6: 8,055,419 ≈ 8 × 1,000,032 births + ~55k steady → "13,426/frame"). Steady engine reads: ~95/frame at both 1e5 and 3e5.
- Working-set curve under the oracle gather (1e5 = 3e5 = 1e6 within 1%, seed-stable): live 10% @ 1 frame, 20% @ 1 s, 60% @ 5 s (@ 20 s censored by flight length; view=none: live@20 s = 40.5% at 1e5 over 50 s — the engine alone leaves most of the belt cold).
- Timeout demotion under the oracle gather wins ≤ 1.7× at 5 s slack, or pays ~0.1 returns/body/wall-s ≈ 440 cores at 1e9 (4.4 µs a rebuild, c4d3) — **a view-gather bill, not an engine bill; under the adopted row-set gather (view row: 351–374 readouts/frame flat in K) it collapses and demotion becomes viable.**
- Anchors reproduced: 2,432–2,447 B/body standing at 1e5–1e6 (footprint 245/730/2,424 MB), catalogue = N; misses = 0 in every arm.

## Refuted
- "With rare kicks, a body is live only around its events" **holds for the engine** [checker, view=none: 99.8% zero post-birth engine reads]; it is refuted only as long as the oracle O(N) gather runs — the gather, not the event law, decides residency (9d3a + checker control).
- "Demotion back to the compact store is the memory row's next lever": refuted as a timeout policy under the oracle gather — the bill is the gather's return rate (9d3a); already killed on the plane's rebind loop by 4ea0 (eviction pays ×98 builds).

## Open directions
1. **Demotion under the adopted row-set gather** (the gold experiment [checker]): re-fly the census with the view served by the row-set/skyserve path (351–374 readouts/frame flat in K) — if the live set is event-bound there, demotion/interning is worth its full ~10²–10³ and the row's premise is restored, not killed.
2. **Intern the shape per cell as the gather-tolerant closure** (cell-rebind od 1; efd4's intern): with reads this dense under the oracle gather, sharing beats dropping; the census gives the service requirement (~8 decodes/body/gather).
3. **A horizon for the view's gather** — already the view row's own adopted direction (flyable-frame gold: row-set deletion 220×; skyserve readouts flat in K); an O(N) walk cannot run per frame at 1e6 anyway.

## Contradictions
- None unresolved. The 5 October lesson was applied twice here: the census's identity-by-address and misses = 0, and the checker's view=none control separating the two readers the funnel merged.

## Runs
- 20261021-0429-spacex-9d3a (this run): under the oracle gather the live set is gather-bound, not event-bound — 4 zero-read belt generations in 100k–1M; live 10/20/60% at 17 ms/1 s/5 s; demotion pays ~440 cores at 1e9. [checker: the engine half of the claim is a build-decode artifact; see Current best.]
