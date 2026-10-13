# Predictions (written before the decisive experiment)

Held-out cases: none of these arms were tuned or run before this file was written.

- **P1 (engine core, decisive).** On the shipped engine (scripted decisions at canonical ticks via
  `schedule`, a moving player, plane seeds 1 and 3), the digest at the same canonical cut is
  bit-identical across the three rekey policies — shipped (rekey every advance), never (frozen
  deadlines, frozen observer), lazy (rekey only when the player's event time moved) — **and** the
  per-frame presented-tick traces differ between the arms (else the test is vacuous: the policies
  never diverged). Kill criterion: any digest difference names the channel by which a scheduling
  heuristic leaks into canon, and kills "delete the fixed tier by laziness" as a digest-safe move.
- **P2 (the session leak, on untouched shipped code).** Mimicking `session.rs` exactly (keys logged
  with `input(u.now, …)` at the frame boundary): the same wall-timeline of key flips produces
  different digests at the same cut under 30/60/144 Hz pacing. This reproduces the known leak
  (taleb-40c0) through an independent harness; if it does **not** reproduce, my harness is wrong.
- **P3 (the fix shape, still untouched code).** Logging the same flips as scheduled decisions at
  `grid_ceil(now)` with a grid Q ≥ the slowest pacing's per-frame game-time advance makes the
  digests identical across all three pacings.
- **P4 (cost, orders of magnitude only, shared x86 runner).** In quiet frames the engine-side
  per-frame cost with rekey on exceeds rekey off by roughly the rekey tax already on the page
  (tens of ns/body at small N, growing as the pass leaves cache); I expect the on/off delta at
  4,000 members to be the dominant term of the quiet frame.

What would make each wrong: P1 fails if any outcome reads a deadline (the code comments say
`pos`/`observer` are "for deadlines only; never an outcome" — if false, that comment is the bug);
P2 fails if `input(now)` happens to land on identical ticks across pacings (choose rtf/frame sizes
so it cannot); P3 fails if a grid cell is skipped by the slow pacing (Q must cover rtf/30 s); P4
fails if drain dominates rekey at these N (the page says they travel together — then the delta
shows the tier, not rekey alone).
