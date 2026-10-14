# 20261014-2012-components-38bf — the input seam inside a wave

## Claim

With the player's pull capped (`ES_PULL_CAP`, this run's patch, bf21's fix re-derived), a player
decision landing mid-wave is **O(1), not O(backlog)**: 0.168 ms for one decision at the wave's p50,
0.229 ms worst over 657 decisions every frame through the wave (≤ 2 events resolved per call), max
frame 12.7 ms / 12.5 ms against the uncapped baseline's 1,487 ms — the checker-2-bf21 "real untested
exposure" (`input` resolving the player's item over an overdue backlog outside the queue) is real as
a mechanism and **bounded by the same cap**; and a no-op decision (same keys) moves no kick but is
not a pure no-op at the log's margin: 657 of them add exactly one encounter to the log.

## Bottleneck

Not a new one: the wave seam (the furthest-gap N ladder line). This run closes the named exposure on
it — the last unbudgeted player-facing path — so the wave's entire player-facing cost is the capped
pull + the budgeted drain, and nothing else the player does during a wave spikes a frame. Gain: it
removes an open risk from bf21's adoption (the integrator can adopt the cap without an input-path
caveat), and it deletes the "input must be deferred/rationed" design option that the exposure
implied.

## Evidence

All on shipped main + this run's two edits (the `ES_PULL_CAP` bound in `pull_ships`, default-unset;
the `wave_input` bench), Linux 8-vCPU shared box (quiet), release, N=2×10⁵ seed 1, L8 burn from
frame 60, rtf 100, 12 ms budget, canonical cut 16,000 game-s with `settle` before the digest. Each
flight ≈ 25 s wall. Reproduce: `regen.sh` (or one flight:
`ES_PULL_CAP=64 cargo run --release -p emergent-universe --example wave_input -- 200000 one 175 100 12`).

| flight | pull | inputs in wave | input cost (ms) | max frame | over 12 ms | kicks | enc | digest |
|---|---|---|---|---|---|---|---|---|
| P1 plain | uncapped | 0 | — | **1,486.9** | 9 | 225,949 | 1,624 | `c2b834bb…` |
| P2 plain | cap 64 | 0 | — | 12.487 | 2 | 225,949 | 1,624 | `c2b834bb…` |
| P3 one | cap 64 | 1 (p50) | **0.168** (2 events) | 12.732 | 2 | 225,949 | 1,624 | `19ac13e7…` |
| P4 held | cap 64 | 657 (p01–p99) | p50 0.160, **max 0.229**, ≤2 events | 12.516 | 1 | 225,949 | **1,625** | `6cd32209…` |

- **bf21's certificate reproduced on my build**: P1 vs P2 digest bit-identical (`c2b834bb…`), kicks
  equal; monsters 1,487 → 12.5 ms (118×). The `events` counter differs (258,939 vs 259,529): the
  pace-dependent slice count 4487's checker2 also saw; the digest is the certificate.
- The player is in the root doll (0) through the wave (doll trace `(0,2)→(89/90,0)`), so the pulls
  read the belt: the exposure's precondition holds. `belt_first 200000` re-measures the window
  13,377/14,072/14,473 (p01/p50/p99) — the bench's triggers, unchanged from 6138.
- The input path's boundedness is structural: `input(t)` resolves the player's items with
  `key ≤ max(now, event_time)` — under burn that is ≤ 2 items — and each item's `pull_ships` is
  capped, its scan `Held`. 657 calls × ≤ 2 events = no visible frame effect (lag 1.433 vs 1.219
  game-s; over-count 1 vs 2).
- **The +1 encounter (P4 vs P2)**: kicks bit-equal, encounters 1,625 vs 1,624 — a no-op decision
  requeues the player (`take`), whose items carry scans at ticks P2 never scans, and one such scan
  found one more encounter. "Same keys" is not "no event": the decision log is an observation.
- No second seam visible: P2/P3/P4 worst frames are the budgeted drain itself (~12 ms, 200+ events);
  4487's 90.3 ms 1-event frames at 2×10⁵ do not appear on this quiet box with the bare cap
  (different fix shape: theirs adds a drain inside `advance` + `Waiting` scans; mine leaves the rest
  to the frame's queue drain).

## Predictions

`predictions.md` was written before the flights. P1 held (monsters of order 0.1–1.4 s: 1,487 ms; the
"≥ 10 frames over" arm missed by one — 9). P2 held in substance (max 12.487 ms ≈ the budget plus
loop overhead; digest equal; "0 over" strictly missed by 2 edge frames). P3 held on frames and
counters, **over-predicted the call cost ~20×** (2–8 ms guessed, 0.168 measured — the scan is held,
not run, and ≤ 2 items are due). P4 **missed in the informative direction**: hundreds of over-budget
frames and 15–40 ms max predicted; measured 1 over, 12.5 ms max — the adversarial every-frame case
is essentially free. P5's falsifier (> 100 ms a call, > 1,000 events) never fired; the verdict is
the bounded one.

## What would make it wrong

A key-**changing** decision mid-wave (this run holds the same word, so the player's plan never
re-derives — a turn under burn is the untested case); the player inside the belt band (same-doll
candidates at belt density); 4×10⁵ (this box's 2 GB ceiling); and a busy box (the 1-event second
seam is load-conditional per 4487's checker). The P4→P2 encounter delta is one event on one seed;
a checker should re-run P4 to see it reproduce (it is in the digest's chain, so it must, or the
instrument is unstable — 4487's open direction 2 stands untested by me beyond this one pair).

## Cost of adoption, PRINCIPLES fit

Nothing to adopt beyond bf21's cap (this run re-derives it independently and re-certifies it);
the input path needs **no** deferral machinery — deleting that option is the saving. PRINCIPLES #12
("minimize spike compute… i care about the p95/99 results") — the last player-facing unbudgeted path
measured flat; #5 (the player is the only wildcard, influence at c) — the wildcard's entry point
costs O(1); #2 (behaviours, not fidelity) — judged by frame profile and counters, not trajectory
identity. The lens (first principles, one component): the input seam's floor is one decision event
(log + requeue, ~µs); measured 160–229 µs mid-wave, ~2 orders over the floor, bounded in N — the
idiot index is the scan/pull constant, not the backlog.

## The lens

The component lens kept the run narrow (one seam, floor + measurement) but biased toward schedule
questions; it nearly missed the +1-encounter margin (a log-level effect, not a cost effect) — found
only because the counters were compared, not just timings. The realism caveat (the shipped page
calls `input` on key *change*, not per frame) cuts both ways: my `held` arm overstates the call
rate and understates the per-call work (a change re-plans; a no-op does not).
