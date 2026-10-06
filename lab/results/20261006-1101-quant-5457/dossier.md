## Claim

One player burn is priced in **deferred game time, not frame hitches**: at 11,560 g (level 15) the
player's engine accounting items grow 13× (kicks 2×), 19% of frames overflow the 5 ms budget and the
worst-1% real-time factor sinks to 0.2× — yet no frame in any run crossed 16.7 ms (worst 13.3), and
repeat runs stay byte-identical in digest: the budget governs the frame, and the debt falls on the
clock.

## Bottleneck

Board #4 (smoothness and the allocator) and lens §6 (impact): the price of a player action, which nobody
had measured on the plane. It sizes what the burst policy must absorb and confirms the budget's design:
no new component; impact is converted into deferral with identical bits, and the already-queued
window-setup work (components-4643's "92% of evals is setup") is where the growth lands.

## Evidence

All runs: `xtask universe --bench --seed 7 --rtf 100 --seconds 30 [--coast | --level L]`, paced, 5 ms
engine budget, 1800 frames, burns held 20 of every 240 frames. Machine: shared Linux x86, 8 vCPU, load
1.1–1.3 (recorded in each JSON). Commands and data: `bench-{coast,L0,L8,L8b,L15}.json`, `analyze.py`,
`analysis.json` (this folder). Requires this run's patch to `xtask/src/universe/mod.rs` (`--coast`
control + per-frame `series` dump; saved by run.sh). Each run ≤ 40 s.

Counters (from `Stats`; near-canonical — between the digest-identical L8/L8b pair, player items and
encounters match exactly, kicks/boundaries/slices drift ≤ 0.5%, and `opens` is outright wall-dependent:
404 vs 86 on identical physics, so it measures re-opened windows under deferral, not dose):

| run | kicks | opens | boundaries | slices | encounters | player items | player engine ms | digest (16) |
|---|---|---|---|---|---|---|---|---|
| coast | 1690 | 70 | 1593 | 7157 | 132 | 289 | 233 | 4bff5f862733efe0 |
| L0 (0.35 g) | 1692 | 86 | 1576 | 7111 | 132 | 293 | 330 | 74651968356a2ef2 |
| L8 (89 g) | 2220 | 404 | 2107 | 9373 | 238 | 1352 | 560 | 8fe4d5d50e12e0bc |
| L8 repeat | 2215 | 86 | 2106 | 9360 | 238 | 1352 | — | **8fe4d5d50e12e0bc (identical)** |
| L15 (11,560 g) | 3373 | 404 | 2844 | 10288 | 178 | 3807 | 2003 | 868910746819a8fe |

Dose signal (digest-grade): player items 289 → 293 → 1352 → 3807; kicks 1690 → 3373 (2.0×); encounters
132 → 238 (L8) → 178 (L15, trajectory-dependent). Player engine time 233 → 2003 ms (8.6×, wall-derived).
Per-item cost *falls* with dose (player 807 → 526 µs/item): warm memos amortize; the burst is in count,
not unit cost. Level 0 (0.35 g) is indistinguishable from coast — impact is negligible below ~1 g and
then climbs steeply.

Service layer (this box; orders of magnitude, integrator re-measures on M1):
- Hitch counts above 16.7/33/50 ms: **0/0/0 in every run** (wall and CPU). Worst wall 13.3 ms; frame
  p99.9: 7.9 (coast) → 12.0 ms (L15).
- Overflow frames: 5 → 41 → 60/65 → **348** (19% at L15). Engine share of frame time 24% → 42%; gather
  59% → 45% (still the largest part everywhere). rtf worst-1%: 100 → 0.2×.
- Decay: the burn's excess CPU returns to coast within ≤ 41 frames after each 20-frame burn (predicted
  ≤ 60); at L15 payback spreads 3–5 ms of engine work across the 40 frames after clusters 0/3/5.
- Noise floor: identical work (L8 vs L8b) swung per-frame CPU 2× under load (burn excess +3.8 vs +0.5
  ms) with flat load average — single-run per-frame CPU on this box carries ±2×; the digest and its
  exact counters (player items, encounters) do not move.

## Predictions

`predictions.md`, written before the sweep. Held: #2 (no CPU hitches), #4 (decay ≤ 60), #5 (digest
identical across repeats, distinct across doses), #6 survival (alive at L15). Failed, informatively:
#1 (per-frame CPU ratio ≥ 2× at L15 — measured 1.23; impact shows in canonical counts and deferral,
not per-frame CPU, which load noise washes), #3 (gather share ≥ 50% at every level — 45% at L15, the
engine overtakes nothing but closes to parity), #6's rtf clause (worst-1% fell to 0.2×, far below half
the median). Two clean holds, three instructive misses.

## What would make it wrong

Overflow and rtf-sag numbers are wall-budget measurements on a contended box; on a quiet M1 the
absolute overflow counts will shrink (the coast run already shows 5 with zero decisions). The frozen
trend — overflow monotone in dose at flat load, player items 13× — is the load-independent content. The
verdict flips only if the M1 shows the burst paying in hitched frames instead of deferral, or if the
item growth is an artifact of the scripted burn's key pattern (four headings cycled) rather than dose.

Anomaly left for a checker: at L15 the universe's input log carries 16 decisions but `Stats.decisions`
counts 14; L8 counts 16/16. Possibly coalesced flushes under lag, possibly a lost count; digests still
deterministic.

## Cost of adopting; fit

Nothing to build: this is the measurement the allocator design lacked. It says the burst policy
(budget → deferral, bits unchanged) survives a 33,000× throttle range, and that the already-queued
window-setup work (components-4643) is the right lever for impact too: it is where the extra items go.

PRINCIPLES: "Priority is slack, not proximity" (#5) — measured: the slack queue holds the player's
order inside 16.7 ms and bills the clock. "minimize spike compute and average compute usage so that
you get a bigger simulation that runs smoothly" (OC#36) — the spike is converted to a rate.

## The lens

A market lens prices the order and moves on; it nearly missed that the *counts* (player items, kicks),
not the timings, are the reproducible currency here, and it did not probe the encounter seam's dose
(132 → 238 → 178: non-monotone, trajectory-dependent, worth its own run). It also flew one seed only —
behaviour over many seeds (PRINCIPLES #20) is untested; the digest determinism is single-seed evidence.
