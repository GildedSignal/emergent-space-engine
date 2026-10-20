# Predictions (written before the census flight and the composition arithmetic)

Component: the scheduler apparatus of the live plane — five per-body `Calendar`s
(`queue`, `ship_ticks`, `child_ticks`, `waiting`, `prunable`; universe.rs:163–183,
allocated at `body_cap` universe.rs:481–490) plus the deadline position cache
(`pos`, 16 B/body, universe.rs:479).

Already measured (schedbytes, shipped types): `Scalar` 16 B, slot 24 B,
`Calendar::new(n)` = exactly 28.00 B/slot, N-flat 10⁴→10⁶, 2 allocations.
Apparatus capacity = 5×28 + 16 = 156 B/body.

## Held-out predictions for the census flight (schedcensus, K = 10⁴ belt, rtf 1000)

- **P1 (ship_ticks is a whole-population container):** `ship_ticks.len() == n_bodies()`
  at every census, from build to end. Basis: the field's own doc ("Every ship's next
  tick … whatever its place in the queue") and the genesis replan loop.
- **P2 (waiting holds ~N, not O(due)):** `waiting.len()/bodies ≥ 0.9` at build end and
  through the first belt waves (belt step ~27.6k game-s ≫ a frame's ~16.7 game-s at
  rtf 1000). If waiting drains below 0.5·N at steady state, the "four of five
  containers are whole-population" claim dies and the finding shrinks to capacity-only.
- **P3 (queue is the only sparse container):** `queue.len()/bodies ≤ 0.01` at every
  census (it holds due items + the always-queued few: planets, moons, player, fleets).
- **P4 (child_ticks ≈ the belt):** `child_ticks.len()/bodies ≥ 0.8` (the belt's ships
  live in planet dolls). Uncertain: if the belt's dolls are root-attached this reads ~0
  and the claim drops to three whole-population containers.
- **P5 (prunable grows toward N with history):** 0 at build; after the first kick wave
  ≥ 0.5·N (every kicked body gains prunable history; 4a71 measured retained
  generations ≈ 1.02/body in control).
- **P6 (the CPU neighbour is a non-issue):** heap ops measured 31 ns fill / 38 ns
  update / 364 ns full-drain per slot at n = 10⁶ — three orders under the fired item's
  44.7–82.5 µs; the apparatus is a bytes component, not a CPU component.

## Composition predictions (arithmetic on measured constants; x86→M1 orders only)

- **P7:** at 10⁹, body_cap sizing holds 156 GB of schedule-only state = ~20× an 8 GB
  machine; live-population sizing (L = λ·τ·N = 4×10⁻⁵ × 43.6 × 10⁹ ≈ 1.74×10⁶) holds
  ~0.27 GB ≈ 3.4% of the machine. The flip is a sizing policy, not an algorithm.
- **P8:** the wired memory row of the 10⁹ ledger (1.7–2.4 B/live-body, 07b4) is a
  store-only number; no row of budget-1e9 prices the scheduler's bytes (checked by
  grep: "calendar" absent from budget-1e9.md and memory-h-live.md's terms; the only
  queue-byte entries are 6a0e's single-calendar 16→8 B and 25ce's cursor design).

Kill criterion for the run: P2 and P4 both failing (waiting and child_ticks both
sparse) reduces the apparatus to one full container (ship_ticks) + prunable —
~2×28 + 16 = 72 B/body; the composition correction would stand but with a smaller
constant, and the run reports it as such.
