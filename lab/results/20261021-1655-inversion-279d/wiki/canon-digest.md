topic: canon-digest
status: open
closed-by:
valid-while: crates/universe@<this run's tree> + this run's patch (examples/truthprobe.rs; no engine change)
updated: 20261021-1655-inversion-279d

# The canonical digest as a certificate: where schedule-independence holds, and what forks it

## Current best

**The engine's digest at a fixed cut is schedule-independent at the lab's reported drift point (279d):** belt N=10⁴, seed 1, rtf 6000, cut 24,363,053,610 — 13 arms (unlimited / events-25 / wall 0.5–12 ms / paced / unpaced / gather-in-loop / scheduled-burn), **one digest per input log** (`8e1882ff…` coast ×12, `8233751e…` burn ×3), identical kick and encounter counts, while the presented path the wall controls spanned 0.34–24.4e9 ticks. Both reported "wall-coupled digests" are instrument diseases: (i) **digesting the presented tick of an open-ended flight** is wall-coupled by construction (c8d5's `f94f69c…` vs `20a60685…`; `digest_presented` distinct on every rep of every arm incl. the stable ones); (ii) **example harnesses inject decisions at the presented tick** (`p.u.input(p.u.now, …)`: `nladder.rs:74`, `wall.rs:16`, `flight_sweep.rs:123`, `frame_cost.rs:35`, `frame_f1.rs:57`, `skew.rs:28`, `kick_bench.rs:68`) — under a biting budget the decision tick is machine noise: **3 reps → 3 digests** at one cut (`fa0d9b03…`/`2991f553…`/`3d3747e1…`, kicks 219,657–219,892), while `p.u.schedule(canonical tick, …)` gives 1 digest in 3 reps with presented still varying 10.8–14.5e9. The shipped player path is the safe pattern (`--bench` `canonical_log`: 11 decisions at canonical ticks, two runs one digest `25702850…` with presented differing 81M ticks; 26fc-checker2's "stock dies at 2,996 gs on most wall schedules" is this hole in a keep_probe burn arm, not engine schedule-luck). Observation is read-only (gather-in-loop = no-gather digest). Benches that compare flights by digest must schedule scripted inputs canonically and digest only after `settle(cut)` — then digest identity is a certificate again at rtf ≥ 6000, N ≥ 10⁴.

## Refuted

- "Digest identity is not an available certificate on this bench" (c8d5, rtf 6000, 12 ms): refuted for the engine — with inputs scheduled and the digest taken at a canonical cut after settle, identity holds at that exact scene (279d); the coupling was the instrument (open-ended digest) plus the harness's presented-tick input.
- "The stock arm's deep-burn death is schedule luck" (26fc checker2): the wall-dependence is the presented-tick burn decision of the keep_probe/nladder pattern; a canonically scheduled burn is reproducible (279d; the death-vs-survive fork itself was not re-flown, only the mechanism).

## Open directions

1. **Fix the seven harnesses** (one line each: schedule the scripted decision at a canonical tick before the loop): `nladder`, `wall`, `flight_sweep`, `frame_cost`, `frame_f1`, `skew`, `kick_bench`. Every cost/memory number taken at rtf where the budget bites (the ratchet scenes) is currently a draw from a forked canon.
2. **A cut inside unresolved work**: all 279d arms settle to the cut; a flight digested mid-encounter or mid-fleet-slice (no settle) would test the queue-order claim directly ("the queue's own order is only a schedule") — unflown.
3. **The live session's own tick** (`session.rs:120` injects a real press at `u.now`): self-consistent with its recorder, but a scripted bench driving `Session::step` with keys would fork; decide whether the decision quantum (decision-log od 1) must also cover it.

## Contradictions

- None. c8d5's note and 279d's clean matrix are consistent once the instrument (open-ended digest, presented-tick input) is separated from the engine; decision-log's shipped-session hole (dfh0/a342) is the same disease family, closed there by adba97a8, still open in the examples.

## Runs
- 20261021-1655-inversion-279d (inversion, this run): schedule-independence measured at the drift point — engine clean (13 arms, one digest), the fork is presented-tick input injection in seven harnesses and open-ended digests.
