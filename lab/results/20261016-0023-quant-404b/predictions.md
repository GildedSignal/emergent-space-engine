# Predictions — the birth rail's missing two-thirds (20261016-0023-quant-404b)

Question: the merged ladder prices a belt body's birth at 28–31 µs/body (build, exponent 1.0, break #4
of the 10⁷ rung), but c4d3 measured the whole `add_body` path (compile + catalogue insert + bind +
store) at 9.2 µs p50 at the same true belt keys. What is the other ~19 µs/body, and is it priced by
a stage that a compact-store fill (21–40 bits/body) would never pay?

Hypothesis (from reading `Universe::start`, universe.rs:476): the missing term is `start()`'s
per-body first-plan pass — `step::replan` + `apply` over every body at tick 0 — plus small
calendar/requeue terms. `add_body` does not call replan; `plane_with_extra` calls `u.start()` once
after all bodies exist.

Instrument: `ES_BIRTH_SPLIT=1` (env-gated, print-only, digest-neutral) times (a) the ladder loop
(draw + `add_body` per body) in `plane_with_extra` and (b) inside `start()`: the replan+apply loop,
the requeue loop, the calendar/pos allocations, fleet start and rekey. Example `birth_rail` builds
`plane_extra` at N ∈ {0, 10⁴, 10⁵, 3×10⁵} (1 thread, seed 1, as the ladder flies), 3 reps, best
rep; per-body terms are slopes against the N=0 arm. Cloud timings are Linux/x86: orders and ratios
only, never absolutes.

Pre-registered, before any timed run:

- **P1 (anchor).** The total build slope on this box is 1.5–3× the M1's 28–31 µs/body (Haswell,
  shared), i.e. 40–90 µs/body, and flat ±30% from 10⁴ to 3×10⁵ (exponent ≤ 1.1). If it superlinear
  past 10⁵, my decomposition is confounded by cache and I say so in the dossier.
- **P2 (the split).** `add_body` (the ladder loop minus the ~0.1 µs draw) holds ≤ 35% of the slope;
  `start()`'s replan+apply loop holds ≥ 40%; requeue + allocations + rekey together ≤ 10%.
- **P3 (mechanism).** The first-plan pass (replan+apply at tick 0) costs per belt body within
  0.3–3× of what one wave kick costs per body at settle (same class of work: one resolved event);
  it is NOT dominated by allocation (if `vec!`/`Calendar::new` dominate, the first-plan story dies).
- **P4 (fill arithmetic at 10⁹).** With the measured slope and the M1's 28–31 µs anchor, the belt
  fill at 10⁹ is ≥ 5 M1-core-hours; the first-plan share alone (if P2 holds) is ≥ 2 core-hours —
  work a program-store fill (ladder break 4's compact store, b29a) does not do at all.

Kill criteria (registered): if `add_body` ≥ 60% of the slope, then c4d3's 9.2 µs already priced the
rail and the 28–31 µs ladder number is a measurement/box artifact — the claim dies. If `start()`'s
share is dominated by allocations (calendars, `pos`), the "first plan" reading dies and the dossier
reports the allocation bill instead. If digests move under the patch (ladder_digest ≠ pristine),
the run is VOID regardless of timings.

Held out for the checker (not tuned by me): seed 3 and seed 7 arms, and the 10⁴→10⁵ slope ratio.
