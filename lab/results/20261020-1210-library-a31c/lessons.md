# Five lessons for the nladder's named open targets (the standing comb's two exits)

Target: board #1 (bodies in the flyable engine, 10⁶ vs 10⁹), on the page's own
open decisions — the payload interleave (28k arm, checker2-flown, unadopted) and
the boundary comb ("the cheapest next target", never flown). All quotes verified
byte-identical against the fresh export (verify_quotes.py, 5/5 PASS).

**L1 — Ries, The Lean Startup:** "by working in larger batches and passing work between departments".
Mechanism: large batches feel efficient locally (each unit's handling is cheaper in
lockstep) and are the global pathology — the shared power-of-two fictitious tick is
exactly such a batch: one grid, one insert, aligned arithmetic per ship, and 10⁹
anniversaries on the same day.
Change: adopt the payload interleave (checker2's 28k arm: k-frac 0.50/bin, walls
1.06× outside the repay window) as the shipped birth default; per-ship clock phase
replaces the shared phase, and the "one shared grid" convenience is deleted, not tuned.
Cheapest test: digest identity of the interleave arm across 3 schedules at 1e5 (a
birth-phase change; 4063's canonical-cut instrument), plus walls ≤ 1.1× flat.

**L2 — Hoffmann, The World Atlas of Coffee:** "The goal is simply to produce an even coffee bed, and do no more."
Mechanism: an uneven bed channels all the flow through one spot (the 718–1231 ms
freeze; S2's 14k spread BANDS, 1.72–1.98×); evenness is what bounds the extreme,
and "no more" is the second half — work beyond even has no consumer.
Change: two-part: (a) the interleave's form is half-period offset (even stream),
band-spreads are rejected; (b) the boundary comb (~50% of stream events, 49.7/50.7%
burn/coast) is deleted — a certificate whose answer is ~always "nothing happened",
on a metronome Julien has already ruled out ("kicks belong on certificates breaking").
Cheapest test: env-gated arm removing the `What::Boundary` insert at step.rs:717 for
clock-stepped bodies; fold the leave-compare into kick_clock (which already runs the
crash checks every kick at step.rs:663–676); gate on leave/crash detection within one
full step + cut_digest schedule-invariance — NOT digest identity (the anchor term;
see L5).

**L3 — Kahneman, Thinking, Fast and Slow:** "it is also the ability to find relevant material in memory and to deploy attention when needed".
Mechanism: intelligence is attention on demand, not on a schedule; the boundary comb
deploys attention to every belt body every half-period regardless of need — the
kick already re-checks surfaces each period, so the boundary's only unique products
are the leave compare (one compare: fold into the kick) and the anchor stamp (a
readout tick: stamp at kick).
Change: delete the boundary comb per L2b; certificates ride the events that can
change them (kicks), never a metronome.
Cheapest test: as L2b; kill if a leave escapes past one full step or cuts disagree
across schedules.

**L4 — Farnam Street, Power Laws:** "Quadrupling our training mileage from 16 to 64 miles is unlikely to double our endurance again".
Mechanism: the exponent declines; each same-class deletion buys less. The banked
per-kick deletions bought −17%, −9…−11% (6faa's ledger) and the composed floor is
32–36 µs against the ~50 ns item floor the comb needs.
Change (compose.py, this run): after the boundary deletion the 1e9 era wall is ONE
term — the kick comb, 1e9 × 45.9 µs ≈ 12.75 h against a 69.75 s era budget at rtf
400 (658× over); at the 50 ns floor it is 50 s/era ≈ 0.72× budget (fits). The
boundary deletion removes ~50% of stream events and buys 1.2× on the era wall —
worth taking, and not the lever. The remaining 918× is representation (the walk →
kernels port, kick-jet open 1), so the ladder's next rungs go there, never to more
per-kick polishing of the same class.
Cheapest test: the composition itself (compose.py, regenerates from page-cited
constants); its falsifier is any measured lever that moves the kick item below
45.9 µs without a law change.

**L5 — Darwin via Farnam Street:** "to make a memorandum of it without fail and at once".
Mechanism: the contrary fact is registered before it can be explained away.
Change: the deletion's digest WILL differ by construction — `rec.anchor` is hashed
into the frame digest (universe.rs:1327) and the anchor is stamped by the boundary
— so "digest identity" is an unpassable criterion of the r2/r8 class. Register that
now (predictions.md P3d), write the rung on the moved-anchor arm, and gate on
behaviour (leaves, crashes, canonical cuts across schedules), never on bookkeeping.
Cheapest test: the rung's criteria block names the anchor exception up front; a
checker flying the naive arm and reporting "digest differs" is the instrument
working, not the method failing.
