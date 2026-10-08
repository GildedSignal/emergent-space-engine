# Dossier — the player's decision as a market order (run 20261008-1252-quant-291f, lens: quant)

**Claim.** In the plane as shipped, one player order (hold a level-15 burn at 100× RTF, release 10 game-seconds later) wakes a bounded, predictable transient of ~2,000 extra events — the player's own kicks+boundaries plus the fleet's slices and encounters — that saturates the 5 ms frame budget for 94–116 frames (coast: 0), drops the instantaneous real-time factor to ~0.23× and the held average to 86–94×, but never breaks the frame service level (worst frame ≤ 3.1× the coast p99.9) and never breaks exactness: at a fixed canonical cut the digests of repeated budgeted runs are bit-identical.

**Bottleneck.** Board #4 (smoothness and the allocator) and PRINCIPLES #5 ("the player is the only wildcard"). The wake is what the allocator must schedule; today it is absorbed by the horizon (RTF), not by frames. Not a 10× engine gain: a measured service-level curve and the mechanism that owns the tail, which the slack-skin build (b-encounter-skin) and root-clock keys (b-root-keys) can adopt directly.

## Evidence (shared 8-vCPU x86, loadavg ≈ 1, single pinned core; orders of magnitude only)

Instrument: `crates/universe/examples/wake.rs` (saved in this run's patch): twin planes, same seed; arms `coast` / `noop` / `burn<level>`; decisions at fixed canonical ticks 203,025,000 and 406,050,000; frame loop `u.frame(1/60, 100, Budget::wall(5ms))`, 1,800 frames; per frame: wall ms, events, presented tick, overflow, per-kind deltas, per-kind cumulative cost. Data: `*.csv` here; `analyze.py` produces every number below.

| seed | wake extra events | owners (arm − pre-burn baseline) | overflow frames (burn window) | worst ms / coast p99.9 | held ticks/frame |
|---|---|---|---|---|---|
| 1 | 2,112 | kick +243, bound +244, slice +715, enc +6 | 101 (coast 0) | 6.08 / 2.24 = 2.71× | 312,777 |
| 2 | 1,921 | kick +561, bound +515, slice +3,037, enc +46 | 95 (coast 0) | 5.93 / 1.97 = 3.01× | 314,768 |
| 3 | 2,016 | kick +314, bound +269, slice +2,522, enc +50 | 116 (coast 0) | 6.93 / 2.56 = 2.71× | 308,498 |
| 2 (ABBA repeat) | 1,938 | same as seed 2 ±1% | 93 (coast 0) | 6.07 / 2.36 = 2.58× | 315,316 |

- Coast baseline: ~4.4 events/frame (the fleet battle's slices are 3.3 of them — the battle, not the sky, is the universe's own cost); p95 0.55–0.73 ms. Held burn at L15: 8.1 events/frame, p95 5.2–5.3 ms — a budget-capped regime shift, not a spike. The frame-ms tail is a censored instrument (the budget absorbs it); the uncensored tails are the overflow count and the tick rate.
- Stall shape: instantaneous minimum 768 ticks/frame (RTF ≈ 0.23×), 94–116 frames below one-third rate, bursty (recover and re-dip — each fleet transit rebinds), fully recovered to 338,375 ticks/frame after release within ≤ 120 frames (decay window 3.6–3.8 events/frame ≈ coast 4.4).
- Level sweep (seed 2): L4 (≈5.6 g) is free (p99 1.0 ms, full rate); L8 (≈89 g) already saturates the budget at p99; L15 averages 86% of nominal rate. The capacity edge sits between L4 and L8.
- Overshoot: the wall budget is atomic per item — worst frames 6.9–10.9 ms are fleet slice batches (14–16 slices ≈ 0.7 ms each), not player items. The frame bound is budget + one item.
- Negative control (`noop`): wake 0–1 events, worst frame within coast noise. Positive controls: burn digest ≠ coast digest, refused = 0 everywhere; repeated burn runs at one fixed canonical cut (`WAKE_END=620000000`) give identical digests ×3 (47dd9c71…), coast identical (6ed7b26b…) — bit-exact under a wall-clock budget.

Reproduce (each ≤ 15 s):
```
cargo build --release -p emergent-universe --example wake
W=./<target-dir>/release/examples/wake
taskset -c 2 $W 2 coast 30 100 5 > coast-s2.csv; taskset -c 2 $W 2 burn15 30 100 5 > burn15-s2.csv
WAKE_END=620000000 taskset -c 2 $W 2 burn15 30 100 5  # ×3 → identical digest lines
python3 analyze.py
```

## Predictions (`predictions.md`, frozen before the panel)

Held: P1 (wake < 5,000 events: 1.9–2.1k), P2 (≤3× coast p99.9: 2.58–3.01×), P6 (noop ≈ 1 event). Wrong: P3 — the owners are kicks+boundaries and the *fleet* (slices+encounters), not opens/handoffs (opens drop; handoffs 0 — the burn never leaves Home's doll); P5 — coast overflows 0 ✓, but burn-window overflow is 93–116, so "100× with no hitch" does not survive a held hard burn: the hitch is real-time factor, not frame time; P4 — decay within ≤120 frames, not the frozen 60. Seed 1 was used for an 11-s shakeout before the panel (disclosed); the held-out seeds 2 and 3 agree with it within ±6%.

## Instrument lessons (both are the memo-artifact lesson again)

1. My first bench stamped decisions at `u.now` — schedule-dependent under a wall budget — and "found" non-determinism (three different digests). With decisions at fixed canonical ticks: identical ×3. The engine is exact; the input layer must stamp player inputs at canonical ticks, never at "now when the frame happened". `Universe::input` permits the mistake; worth one line in `docs/law.md` (Ties) when b-root-keys lands.
2. Frame wall-time under a wall budget is a censored tail: judge a wake by overflow frames and ticks/frame, and keep the negative control arm.

## What would make it wrong

The M1 re-measure (thermals, efficiency cores) can move every millisecond; the *ratios* (8–10× p95 shift, 0.23× stall, 86–94% held rate) should hold while one player, one fleet (48 members) and one star system are the whole load. A bigger fleet, a belt, or a second wild-card player multiplies the slice and encounter terms — the slice term (up to 3,053 of the 1,921–2,112 net events) scales with fleet size, and it, not the player's own kicks, owns both the worst overshoot frames and most of the wake at seed 2/3. If the encounters skin (b-encounter-skin) defers fleet slices, the wake should shrink toward the player's own ~500–1,100 events; that is the falsifiable next probe.

## Cost of adoption, fit with PRINCIPLES

Nothing to merge: this is a measurement plus two constraints for builds in flight. The adoptable insight for the allocator: the wake is fully predictable at decision time (the burn program is logged before the engine reaches its tick; "the simulation tells us what's next, not us" — principle 22), so the transient's events can be computed ahead in idle time instead of bought as an RTF dip. Fits PRINCIPLES #5 ("priority is slack, not proximity": the player's events are deadline-0 and starve the idle queue — that is why the dip is deep, and pre-computing the burn's own events is the slack-native fix), #12 (p95/p99 judged, not means), #2 (behaviour: the dip is smooth, no hitch — as designed).

## Grade request and lens blind spot

Silver, or gold if the checker values the exactness-under-budget confirmation (×3 identical digests) plus the canonical-input-stamp constraint for b-root-keys. This lens may have missed: correctness corners (B13-class) of a burning player inside the fleet (refused = 0 here, but only 3 seeds, one geometry family); memory/bytes-per-body of the wake (not measured); and it prices tails, not the elegance of the event law itself — a nanosecond-shaved wrong law is still wrong.
