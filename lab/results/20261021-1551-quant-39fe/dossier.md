# Dossier — 20261021-1551-quant-39fe (quant lens)

**Claim.** The plane's frame tail is two diseases with different cures, measured per item on shipped code: the comb's worst frames are pure arrival piles at mean service (correction 0.90-0.96), while the steady trickle's worst frames are service-tail events — and the service tail is a *boundary-item population* (80-84% of >p99.9 items at every rung) reaching 10-34× its kind's mean, with single player items at p99 6.0-7.1 ms and max 11.0 ms, so a mean-cost program moves the comb but not the steady worst frame.

**Bottleneck.** Board row "plane smoothness / the frame's p99" (scoreboard F1's row; PRINCIPLES #12: "i care about the p95/99 results i want the game to be smooth"). Every prior cost number on this path is a mean (82.5 µs/item, 45.9 µs/kick, 58 µs/rebind; kick-jet holds one stage's p99 for `Orbit::compile` only). This run prices the whole-item service distribution the allocator actually faces. It does not move a 10× row by itself; it splits the smoothness lever in two and prices the budget-margin error (below), which is the input to the allocator's margin rule.

## Evidence (all from `regen.sh`, ~1 min; shipped code + one instrument)

Instrument: `crates/universe/examples/ktail.rs` (new, from the tree's own `tail.rs` pattern): every item resolved alone (`Budget::events(1)` — "a budget moves when work is done, never what", the tree's comment), timed, with kind (items[5] class) and sub-counters; frames drain fully (no 12-ms cut), so "served ms/frame" is what the frame *wants*. Each item also pays the per-call fixed cost (measured 6.7-7.0 µs, rekey included): absolute µs are upper bounds; ratios, tail shape and composition are the measurements.

**Table 1 — steady trickle (20 s, rtf 100 = 2,000 gs, coast, belt 1e5/3e5; no comb is due in this window — this is the inter-comb stream, matching 9d3a's finding that >99.7% of belt bodies get zero post-birth reads in 20 s):**

| arm | ship mean/p99.9/max µs (ratios) | player mean/p99/max µs | fleet mean/p99.9/max µs (max/mean) | >p99.9 tail composition | worst frame: events, served, correction |
|---|---|---|---|---|---|
| 1e5 s1 | 132 / 497 / 506 (3.8×, 3.8×) | 1920 / 6293 / 6954 | 26 / 885 / 4578 (174×) | bounds 84.3%, kicks 15.2% | 70 ev, 16.9 ms, **2.04×** |
| 1e5 s2 | 124 / 473 / 473 (3.8×, 3.8×) | 2160 / 7102 / 7251 | 26 / 997 / 1252 (49×) | bounds 80.7%, kicks 18.8% | 42 ev, 18.6 ms, **3.32×** |
| 3e5 s1 | 130 / 416 / 419 (3.2×, 3.2×) | 1903 / 6289 / 6974 | 26 / 838 / 4458 (173×) | bounds 84.3%, kicks 15.2% | 70 ev, 15.8 ms, **1.93×** |

- p99-heavy *steady* frames are arrival piles of cheap items: correction 0.24-0.33 at every rung (207-244 events served at < mean service).
- The service-driven worst frames sit at the measurement's start (the post-settle ramp, frames 61-63) — the ramp's law, matching a990's "the 20-s horizon is the ramp".
- The stream is N-independent at these rungs (1,346 ship items at 1e5 AND 3e5): the steady trickle is the locals' stream, not the belt's.

**Table 2 — the comb window (30 s at rtf 1000 = 30,000 gs ≈ one comb interval, 1e5 s1):**

| kind | n | mean / p50 / p99 / p99.9 / max µs | p99.9/mean | max/mean |
|---|---|---|---|---|
| ship (both combs) | 203,132 | 39.7 / 50.7 / 101 / **415** / **918** | **10.5×** | 23× |
| player | 2,904 | 1778 / 1207 / 6044 / 9044 / **10,961** | 5.1× | 6.2× |
| fleet | 3,106 | 29 / 17 / 253 / 961 / 4461 | 33.3× | 155× |

- The comb's item mix: ≤p99 = 49.6% kicks + 48.8% boundaries; the p99-p99.9 band is 64.6% kicks; **the >p99.9 band is 78.8% boundaries**.
- Worst comb frames: 4,243/3,901/3,831 events, served 258/237/220 ms, **correction 0.90-0.96** — the comb freeze is arrivals × mean service; the stagger (arrival-side, 8365's direction) is the lever there, not item cost.
- The belt kick item's mean at the comb (39.7 µs incl. ~7 µs per-call overhead ⇒ ~33-46 µs) lands on the record's 45.3-45.9 µs/kick class — the mean is confirmed; the tail above it is new.

**The priced consequence (the budget's margin rule):** `advance` starts the next item only if `item_ns[class] + FRAME_TAIL_NS` is left, where `item_ns` is a peak-with-decay estimate (`m = max(ns, m − m/64)`, universe.rs:1028-1030). At 1-in-10³ tail rates the decay forgets a p99.9 item of that class within ~200-450 class items (~4-8 s at the trickle), after which a tail item can start a frame priced at the cheap mode — the engine's own comment records 1.4 ms overruns from exactly this. The measured p99.9/mean ratios (3.2-33.6× by kind) are the margin multipliers this rule must survive; a per-class quantile or a slower decay is the one-line shape of the fix (not built here).

**Predictions** (`predictions.md`, written before the decisive runs): P1 held (ship max/mean 3.2-3.8, N-flat — though the N-flatness is trivial: the steady stream is the locals', same items at both rungs); P2 held (player/ship mean ratio 14.5-17.5×); P3 held with a refinement — the ≥1.5× corrections are the post-settle ramp, and in steady state (trickle *and* comb) the worst frames are arrival-driven (correction < 1 and ~1); P4 held (kicks 15-21% of the >p99.9 tail at every rung); **P5 failed as a window fact**: no comb is due within 20 s at rtf 100 — caught instead by the rtf-1000 flight (table 2), where the max served frame is 258 ms ≥ 50 ms, so the quantity P5 pointed at is real but needed the longer window.

## What would make it wrong

The per-call overhead (6.7-7.0 µs) rides every item; if a checker batches items per frame and re-measures, absolute µs drop (the player item most: it is one item, so its number is nearly overhead-free) but ratios and composition should hold. `Budget::events(1)` serializes items that the shipped engine may batch inside one call — the digest is unchanged (the tree's own argument), but the *order* of resolution within a frame is the queue's, so tail composition should be identical. The comb window is one seed and one interval: tail ratios there are one draw (the trickle's are two seeds and two rungs). Load is the shared runner's: this box reads ~30% hot vs the record's own band; all numbers are orders-of-magnitude only, and the M1 re-measures.

## Cost of adopting / fit

No adoption: this is a measured law plus a named one-line policy shape (price the margin by a per-class quantile, not a decaying peak). It costs nothing until the allocator's margin rule is touched; it says a mean-only kick-cost win (GPT `kickcost`'s lane) will show at the comb frames and *not* at the steady worst frames, which the player item (6-11 ms alone) and the fleet/boundary tail own. PRINCIPLES #12: "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" — this prices the tails it must prevent, and shows they are two: an arrival tail (spread it) and a service tail (bound the item).

## The lens

Quant pricing can miss that this engine's worst frames may be *lawful* piles (every item cheap, all due at once) rather than expensive items — the lens's instinct to chase the service tail found it real but secondary at the comb, and primary only in the trickle and ramp. The instrument cannot see inside an item (no stage split); whether the >p99.9 boundary items are rebinds, doll handoffs, or panel mints is the next run's question, and kick-jet's stage attribution is the tool.
