# Dossier — 20261021-0429-spacex-9d3a (SpaceX lens): the live set is sweep-bound, not event-bound

## Claim
On the shipped read path, demoting idle bodies back to the compact store is dead: between events, essentially every belt body's compiled orbit is still read (4 zero-read generations in 100,032 at 10⁵, 4 in 1,000,032 at 10⁶), because the engine's observe path sweeps ~1% of the population per frame (∝N, not ∝events) and the view's gather reads every body ~7–9 times per gather — so the live set is bounded by the sweep, not by events, and a timeout demotion either keeps 60% of it (5 s slack: win ≤ 1.7×) or pays ~0.1 returns/body/wall-s ≈ 440 cores at 10⁹ (4.4 µs a rebuild).

## Bottleneck
The board's macro row "live set and memory (~10²–10³)". The premise under that row — "with rare kicks, a body is live only around its events" — is false as shipped: the readers, not the event law, pin the ~2.4 KB/body standing orbit (measured: 2,424–2,447 B/body at 10⁶, catalogue 1,000,071 entries ≈ N). The row's closure moves upstream: kill the sweep (the running `wt/cadence` per-body-clock job) or intern the shape per cell (cell-rebind od 1); either collapses inter-event reads to the event set (≤ 3.6% of belt bodies touched by kicks in 20 s here), after which demotion/interning is worth the full ~10²–10³.

## Evidence (all from `sh lab/results/20261021-0429-spacex-9d3a/regen.sh`, ~4 min total; each arm one process, coast, rtf 100, 12 ms budget, the harness's fixed plane/seed)
Instrument: `ES_RCENSUS=1` arms the module `crates/universe/src/rcensus.rs` (patch `work/patch.diff`): every `Binding::orbit_state`/`readout` read counted per **generation** (an `Entry` from mint to drop; identity = allocation address, closure = a `Drop` hook), split engine-phase vs view-gather-phase; mints hooked at both `Arc::new(Entry)` sites; `misses = 0` in every arm (single thread held).

| arm | bodies | gens | zero-post-birth | live @1 frame/@1 s/@5 s | returns/gen (gap>60 f) | engine reads/frame | kicks |
|---|---|---|---|---|---|---|---|
| N=10⁵, view/10 s | 100,028 | 103,783 | **4 in 100,032 (0.004%)** | 10.0%/20.2%/60.3% | ~2.0 | 787 (0.79%/f) | 3,624 (3.6% of bodies) |
| N=3×10⁵, view/10 s | 300,028 | 303,783 | **4 in 300,032** | 10.0%/20.1%/60.1% | ~2.0 | 2,192 (0.73%/f) | 3,624 (1.2% of bodies) |
| N=10⁶, view/10 s (truncated at 55 s: 600 frames; completed once — see note) | 1,000,028 | 1,002,116 | **4 in 1,000,032** | 10.0%/20.0%/60.0% | ~1.0 | 13,426 (1.34%/f) | 1,919 (0.19%; the root's wave had not reached the belt) |
- Memory row anchors reproduced: 2,447 / 2,432 / 2,424 B/body standing at 10⁵ / 3×10⁵ / 10⁶ (peak footprint 245 / 730 / 2,424 MB); dashboard ~1,200 B/body. Total kicks are budget-limited, not population-limited: ~3,624 kicks over 20 s at both 10⁵ and 3×10⁵ (~3.2 kicks/frame) while engine reads/frame grew 787 → 2,192 → 13,426.
- Run-to-run: the sweep is idle-time work, so raw read counts move a few ‰ between identical arms (243,308 vs 243,302 total reads at N=0); every structural number above (zero-post-birth, live curve, returns/gen, reads/frame order) was stable across reruns. The 10⁶ arm completed once (log kept in `work/arm_1000000_20_sparse.txt`); its re-run can be killed by the box's ~2 GB watchdog (the population itself is 2.4 GB), so `regen.sh` treats it as best-effort and the claim rests on the 10⁵/3×10⁵ arms.

## Predictions (`predictions.md`, written after one N=1000/6 s smoke only)
- P1 (≥ 90% zero-post-birth at 10⁵/10⁶): **falsified** — 0.004%. The premise kill above is this prediction failing.
- P2 (live@1 frame ≤ 15%, live@1 s ≤ 40%): **held** (10.0%/20.0–20.2%).
- P3 (dense control at N=0: median reads/gen ≥ 8, live@1 s ≥ 80%): half-held — density confirmed (mode bucket 64–255 reads/gen, per-frame view gathers), live@1 s was 45%: even the 28-body plane has a cold half (outer planets idle > 1 s between scan passes).
- P4 (returns ≈ 0 at slack ≥ 300 frames): **falsified** — ~1–2 returns/gen at 5 s slack; nothing stays idle 20 s.
- P5 (view < 5% of reads at 10⁵): **falsified** — 66%: one gather reads every body ~8.7 times; the gather is O(N) (`for i in 0..u.n_bodies()`, no horizon cull in `view.rs::gather_with`).

## What would make it wrong
The census counts reads through the two public funnels only; a reader touching the store's arrays directly (e.g. a future compact-native readout) would be invisible — misses=0 says none exist today, but the instrument defines "read" as "decode of the compiled trajectory". The 10⁶ arm is truncated at 600 frames (build 44.9 s on the shared box): its 20 s live fraction is censored; the 10⁵ arm carries the full-length result. The engine's ~1%/frame sweep is attributed to the observe bucket by funnel and phase, not by function: the two candidates are the held scans drained in idle time (`Universe::drain_scans`) and the doll's kick-window setup reads (components-4643's 92%); I did not separate them. If the sweep were removed and the live fraction still stayed ~100% at 5 s, the blocker would be something else the census cannot see (a direct-array reader).

## Cost of adoption / fit
Nothing to adopt: this is a premise kill plus a measured read law (the service requirement any sharing/intern scheme must meet: ~1.3% of the population read per engine frame, ~7–9 decodes per body per view gather). PRINCIPLES #3 "Compute only surprises … clocks, redshift, views" are "not derived but emergent": the sweep re-derives every body's state on a grid — the same shared-grid disease the kick-cadence row already owns, now measured from the memory side; #6 "Store the generator, not the generated": demotion is exactly that, and the census shows what pins the generated. One law at every scale (#19/§33): the fix is not a demotion timer (a bandaid with a 440-core bill) but deleting the sweep's demand.

## The lens
SpaceX's delete-first ran into a customer: the standing orbit looked like a deletable part until the instrument showed the sweep reading all of it. The idiot index lands elsewhere than expected — not on the compiled orbit's bytes but on the ~15 M decodes the sweep orders per 10 s at 10⁶. Blind spot: I did not name the sweeping function (attribution stopped at funnel+phase), and the 10⁶ arm is truncated; both are one rung of follow-up.
