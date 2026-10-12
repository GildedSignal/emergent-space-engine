# log.md — autoresearch loop, artifact = the plane's kick path (crates/universe)

Metric: `pure_kick` µs (the resolve of one kick, loop from examples/cost_split.rs) and
`whole` µs/item (universe settle, canonical cut). Behaviour lock: the universe digest
(bit-identical) + `cargo test --release -p emergent-universe` (54 tests).
Estimator: min of 3 runs (single-threaded loop under contention; the runner is shared,
load 3.9–7.6 during the window; first contended runs excluded).

| # | hypothesis | change | metric (min of 3) | kept |
|---|---|---|---|---|
| 0 | — | baseline | A pure 33.39 / whole 50.66; C 32.90 / 68.92; D 32.81 / 48.81 µs | — |
| 1 | a kick decodes the same binding 3× (readout, orbit_state(t), orbit_state(event_time)) | `Binding.event_proper` memoizes the event-time proper time (16 B); `readout_with` returns state+orbit from one decode; kick passes it into rebind | A pure 27.09 (−18.9%) / whole 47.12 (−7.0%); C 26.19 (−20.3%); D 26.66 (−18.7%). Digests identical; 54/54 tests. bytes/body +8% (134372→145382: one Scalar per history segment; prune bounds it in play) | **kept** |
| 2 | `apply` re-derives the scheduler's root position (root_state_raw, 6.8 µs) from tubes the event just read | `Update.root_pos`: kick/kick_clock/decide carry the root position computed from the post-kick state + the tide's centre read; apply uses it, falls back to root_state_raw (opens/boundaries, word-widening refits, chains deeper than the plane's two levels) | whole: A 44.09 (−6.4% vs H1, −13.0% cum.), D 43.83 (−4.3%, −10.2% cum.), C flat (fleet work dominates its item mix). Pure kick unchanged (its path excludes apply, as expected). Digests identical | **kept** (modest: clock-mode boundaries are ~½ the items and still take the fallback) |

Stop: round 2 gained <10% on its target; the remaining fat is structural (below).
Machine state: 8 vCPU shared runner, load 3.9–7.6, 13 GB free; timings are Linux/x86
orders of magnitude — the M1 re-measures.
