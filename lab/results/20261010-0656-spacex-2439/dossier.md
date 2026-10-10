# Run 20261010-0656-spacex-2439 — the frame loop's hidden tick

## Claim

The shipped plane's frame loop pays ≈ 0.4 µs × N per frame of engine CPU **even when no event is
due** (measured 0.43 µs/body/frame on this runner): `Universe::advance` scans the whole queue every
frame, peeking, popping and re-pushing every entity whose next item is beyond the frame. The law
resolves only events, but the loop that asks "who is due" is a tick over all bodies — the engine
budget (5 ms) is exhausted by the scan alone at ≈ 10⁴ quiet bodies, and at 10⁹ the scan alone is
hundreds of seconds per frame, whatever the kick cadence achieves.

## Bottleneck

Board focus line 1 (fewer kicks per orbit: "kicks dominate the engine's cost") and plane.md §7
(bounded work per presented frame). This run shows a term nobody owns: per-frame cost proportional
to N at constant event rate. The gain from fixing it is unbounded at scale (it is the difference
between per-frame O(events) and per-frame O(N)); what it deletes is the scan itself, not a component.

## Evidence (all commands ≤ 60 s of work each, `xtask` built with `cargo build --release -p xtask`)

Scenes: the shipped plane with `--haulers N` added (a probing knob of this run; the default scene's
digest is bit-identical to the pristine binary's — patch hygiene control passed). The added haulers
orbit 0.5–8 AU with periods of years, so at rtf 100 in 6 s they fire no events: events/s stays
453–454 at every N (the event rate is the fleet's, the player's and the planets').

```
B=/home/glmlab/lab-target-3/release/xtask
$B universe --bench --seconds 6 --rtf 100 --unpaced --haulers <N> [--no-rekey-walk]
```

| N (bodies) | engine p50 ms/frame | walked/frame | events/s | view_gather p50 ms |
|---|---|---|---|---|
| 71 (shipped scene) | 0.058 | — | 453.0 | 0.79 |
| 130 | 0.065 | 116 | 454.2 | 2.14 |
| 859 | 0.21–0.23 | — | 453–454 | 19.1 |
| 3,259 | 1.02–1.12 | 3,219 | 453–454 | 76–82 |
| 6,203 | 2.45–2.67 | 6,138 | 453–454 | 147–149 |

- Slope: ≈ (2.66 − 0.065) ms / (6,203 − 130) ≈ **0.43 µs/body/frame**, at constant event rate;
  engine p99 (2–6 ms, the fleet's kick bursts) does not grow with N — the N-term is not event work.
- `walked/frame` (a counter this run added to `Stats`: entities set aside per advance because their
  item is beyond the frame) equals N at every size: **the loop touches every body every frame**.
- **The rekey walk is acquitted**: with `--no-rekey-walk` (deletes `for e in 0..bodies.len() {
  requeue(e) }` from `rekey`), the slope is unchanged (N=6,203: 2.45 → 2.67 ms; within run noise).
  The term is the advance loop's defer path (`crates/universe/src/universe.rs`, `advance`: peek →
  `q.set(e, None)` → `deferred.push` → `requeue` for each non-due entity, per frame).
- **Outcome neutrality, measured**: the digest at the canonical cut is bit-identical with and
  without the rekey walk at every (N, rtf) pair (71, 859, 3,259, 6,203 × rtf 100; 3,259 × rtf 30),
  and identical to the pre-patch binary at the default scene — as universe.rs documents (resolution
  is pull-driven and keyed; the queue order is only a schedule).
- rtf 30 held the slope (1.02–1.47 ms at N=3,259, noisy on a loaded box): the term is per frame,
  not per game-second, as predicted for a tick.
- Corroborating (owned elsewhere): view_gather p50 grows to 149 ms at 6,203 bodies (≈ 24 µs/body/
  frame, 61% of the frame already at the shipped scene). The gather's *constant* is b-readout-cost's;
  the structure (every emitter walked every frame) has the same per-frame O(N) wall.

## Predictions

`predictions.md` was written before the matrix. Held: linearity and its magnitude (N=800 predicted
0.34±0.06, measured 0.21–0.23 — the interval just misses low; N=3,200 predicted 1.27±0.15, measured
1.02–1.12), events/s constant, rtf independence, digest neutrality at every pair. **Failed, and the
kill criterion was applied**: deleting the rekey walk was predicted to cut engine p50 ≥ 16×;
measured ≈ 1×. The counter then attributed the whole slope to the defer-scan (walked/frame ≈ N).

## What would make it wrong

The slope could be a runner artifact (Linux/x86, shared 8-vCPU box; orders of magnitude only — the
integrator re-measures on the M1). If the M1's per-entity scan cost were 100× smaller the wall
would move from 10⁴ to 10⁶ bodies — still far from 10⁹. The attribution could be incomplete if
`walked` counts something that is free in practice; the slope's persistence with the walk off and
walked/frame ≈ N make that unlikely. The extrapolation to 10⁹ ignores heap log-factors and cache
effects, which only make it worse.

## Cost of adopting, and fit

Nothing to adopt in the law; the finding is for the queue's owner (plane.md's "one clock, one
queue", foundation 2). The fix direction, not built here: "who is due by tick T" must be answerable
without touching non-due entities — the queue is ordered by light-delayed **deadline** while
deferral compares the canonical **tick**, so the frame must pop past everything to find the due
few. Order the structure by key tick (pop until the first non-due key: O(due)), or bucket entities
by tick (a calendar wheel, `lattice-event`'s `Calendar` already exists), or defer by deadline.
Cost: a queue change plus its determinism proof (ties.md and replay cover it; the digest equality
method used here is the regression test). PRINCIPLES: "No work for no reason, so no ticks" (P14) —
the loop that asks who is due must not tick over every body; "the simulation decides, heuristics
schedule" (P22) — the schedule's own cost must follow events too.

## The lens

SpaceX: question the requirement, find the idiot index. The idiot index here is brutal: a body with
nothing due costs 0.43 µs/frame against an information floor of zero bits changed. What the lens
may have missed: the view_gather term is the larger constant (24 µs/body/frame) and its structure
deserves the same audit — this run measures but does not analyse it (b-readout-cost owns it). The
60-minute cap is why the wheel is a design note, not a built patch.
