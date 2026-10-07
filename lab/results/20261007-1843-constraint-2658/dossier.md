# Dossier — 20261007-1843-constraint-2658 (lens: the constraint)

## Claim
At the plane's own scale the frame's constraint is not the engine but the **view gather**: an
unbudgeted, synchronous, O(all bodies) scan at ~15 µs per body per frame that already takes
65–70 % of every frame and caps the plane at ~10³ bodies, while the engine's 5 ms budget — not
its compute — is what throttles rtf 100 today, and raising it to 12 ms is measured to fix RTF
with a bit-identical digest.

## Bottleneck
Board focus bullet 1 (kicks) and 4 (smoothness/allocator) meet in the frame. Measured on this
machine (Linux x86, shared runner, load recorded in each JSON): the engine's *intrinsic* demand
at 76 bodies, rtf 100, uncapped, is p50 0.045 ms / p99 1.24 ms / max 12.7 ms per frame; the
kick resolver is 64 µs median (`--kick-bench`). What the player's frame actually spends:
view_gather 67.5 %, engine 18.9 % (clipped at its 5 ms budget), view_json 9.7 %, wire 3.9 %.
Gain on the table: deleting the per-frame O(N) observation poll is the difference between
~1,100 bodies per frame and the goal's 10⁹ (nine orders); the representation is already sitting
there — each emitter's crossing advances ~1 tick per frame (the `ViewCache` slope memo proves
continuity), so arrival cost can follow *change*, not census.

## Evidence (all commands ≤ 60 s, JSONs beside this dossier)
```
cargo build --release -p xtask            # 38 s
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100                 # bench-rtf100.json
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100 --engine-ms 12  # bench-rtf100-ms12.json
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100 --engine-ms 1000 --unpaced  # bench-rtf100-unpaced.json
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100 --members 200   # bench-rtf100-m200.json
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 30 --rtf 100 --members 400   # bench-rtf100-m400.json
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 30                     # kick-bench.json
```
1. **Budget vs engine (76 bodies, rtf 100):** engine-ms 5 → 12: overflow frames 27 → 1,
   lowest-1 % RTF 39.6 → 99.99, frame p99 11.1 ms; **digest identical** (`41343a14…`).
   Uncapped unpaced: engine p99 1.24 ms, max 12.7 ms. The 5 ms constant, not physics, was the
   throttle; the frame had 10 ms of headroom the view was not using.
2. **Gather scaling (three points):** bodies 76 / 221 / 428 → gather p50 1.11 / 3.85 / 6.47 ms
   = 14.6 / 17.4 / 15.1 µs per body per frame (linear in *total* body count; fleet members that
   stay in frames are extrapolated and cheap). Frame p99 9.9 → 14.4 → 14.5 ms; overflow frames
   27 → 287 → 403; lowest-1 % RTF 39.6 → 0.07 → 0.0. At ~1.1×10³ bodies the gather alone is
   the whole 16.7 ms frame.
3. **Inside the engine:** player event 907 → 2459 → 3424 µs/item as bodies grow 76 → 221 → 428
   (the per-doll exact encounter check, universe.rs:944, reads the doll's population); ship
   events amortise downward to the resolver floor (220 → 103 µs/item; pure resolver 64–72 µs).

## Predictions
`predictions.md`, four predictions written before the decisive runs: P1, P2 held exactly; P3
held with the cost driver corrected from members to *bodies* (leavers), and its "frame stays
under 16.7 ms" clause failed at 221 bodies (p99.9 16.86 ms) — reported as failed; P4 confirmed
in code (`encounters.find`), not isolated by a run.

## What would make it wrong, cost of adoption, fit
- **Wrong if** the gather's linearity breaks favourably above ~10³ bodies, or if the real game
  view was always meant to be a sparse query so this O(N) scan is scaffolding (plane.md calls
  the view "a debug view… the visual layer comes later"). Even so, the debug view gates every
  flight today, and foundation 7's own words — "Nothing takes an unbounded synchronous claim on
  the frame, whether a cycle compile, a rebinding burst, a decompression **or a gather**" — are
  currently violated by the gather at scale (8.9 ms max synchronous at 428 bodies).
- **Adoption:** the budget finding is a one-constant change (ENGINE_BUDGET_MS 5 → ~12, or
  adaptive: the rest of the frame); the gather finding says where the next build should aim:
  event-driven arrivals (carry each crossing by its slope; re-read a body only when its tube
  changes or the extrapolation error crosses a quantum) plus the same budget discipline the
  engine already has. That is "compute only surprises" applied to observation —
  PRINCIPLES #3: "Nothing is evolved that can be derived when looked at (clocks, redshift,
  views)"; and #28: "The view is an instrument."
- **Where the constraint moves next** (the lens's fourth question): after the gather, into the
  engine's player path — the O(doll) encounter scan (3.4 ms per player event at 428 bodies
  eats a 12 ms budget every event) — and then to the board's standing question, the 64 µs
  resolver × kicks per orbit. The chain is: budget constant → view gather → player scan → kicks.

## The lens
The constraint lens measures the system as it is; it cannot see whether the debug view is about
to be replaced by a real renderer (that would delete this bottleneck rather than elevate it),
and it says nothing about correctness (the gates: B13 60/64, B17 pass, E9 fails phase 1 by
design — taken from the handoff, not re-run). Single-machine, shared-runner timings: orders of
magnitude only; the integrator re-measures on the M1.
