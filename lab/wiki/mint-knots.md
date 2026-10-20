topic: mint-knots
status: open
closed-by:
valid-while:
updated: 20261020-1116-system-bd4b

# The mint's knot vector: one object behind the kick-cost and memory gaps

## Current best

**The kick-cost row and the memory row of the scoreboard are one line item: the
exact-quadrature knot vector (`OrbitShape::knots`) that every fired kick fills and stores.
Measured kick by kick on the shipped deterministic replay (`xtask universe --kick-bench`,
print-only census, `work/patch.diff` of 20261020-1116-system-bd4b): per-kick wall µs tracks
the minted knot count — Spearman 0.70 (the plane's own bodies, n=23, all cycles, 6–12 knots,
~38 µs) and 0.88 (handed-out fleet members, n=137: 55 cycles + 82 passages, 22–448 knots,
median 148, ~376 µs), tercile medians 203/376/394 µs at 83/148/153 knots ≈ **2.7 µs/knot**;
the minted heap is the knots (**85%/91%**), and the members' class allocates **12.5 KB per
fired kick** (1.71 MB over 137 mints), on top of efd4's Binding 192 + Segment 208 + Entry
~288 B. The panel count is the compiler's eager geometric rule (ψ-bands doubling at
CAP = π/4, orbit.rs:450–481: a near-circular cycle ~6 panels, the members' arcs 20–75× more)
— no certificate sizes it. So: a representation change on the knot memo (lazy extension
and/or a passage-class split; retired Segments keeping keys only) moves both scoreboard rows
together; optimizing them separately double-counts, the same way e7ef showed kick-cost ×
cadence does. Digest-neutral by construction (the readout is a function of the key, not the
memo — 5465's bit-identical regeneration). Domain: one scene (the kick-bench plane + a
400-member fleet), 30 s; Linux/x86 shared box, orders of magnitude only; the traversed
fraction of a fresh mint before the next rebind is NOT yet measured (the open experiment).**

## Refuted

- "The kick's cost and the live-memory plateau are independent gaps" — refuted as one
  object by the ρ = 0.70/0.88 coupling and the 85–91% heap share (20261020-1116-system-bd4b);
  the double-counting concern is e7ef's, extended from cadence×cost to cost×memory.
  [checker: the refutation composes standing results more than it overturns one — the CPU
  share is a765's (compile 84–87% of the rebind) and ec9d's (the leaver tail is
  Passage::compile, 318–356 of 365–381 µs), the memory share is 5465's (58% of a doll
  body) and c304's (~10 kB per ship kick), and library-directions already prices one
  adoption (the Carlson wiring) as deleting the compile wall and the knot table together.
  New here is the per-kick coupling (ρ, µs/knot) and the class census, not the shares.]

## Open directions

1. **The traversed fraction** (decides the lever's size): per fired kick, phase at next
   rebind ÷ compiled span. If members rebind inside their arcs, lazy knots save the unread
   fraction on both bills; if cycles traverse it all (the belt's one-kick-per-period cadence
   suggests so), the saving is passage-class only → a class-split compile rule.
   [checker: scope this to SPAN coverage per class — 4ea0 (gold) already censused the read
   side: the mint's own birth-read is the first reader of every rebind generation, 68–77
   reads per generation, never-read 0, so lazy compilation never moves the kick's CPU bill;
   and the memory-side laziness is already flown at nladder scale (b9ae standing knots → 0;
   0757's bounded cache, gold, 962 B/body). What is unmeasured is the arc span walked
   between mints, by class.]
2. **The 448-knot tail**: what orbit geometry opens it. [checker: not "e→1 passages" — the
   448-knot mint is a Cycle (per-row probe, seed 1: body 74, 448 knots, 755 µs; the next
   tail rows 257/196/174/164 knots are cycles too), while passages sit in a narrow
   147–161-knot band; within the cycle class alone ρ = 0.96 over knots 6→448.]
3. **The allocator side**: 12.5 KB/kick of Arc<Vec> churn — price it with the standing
   counting GlobalAlloc before adopting any memo change. [checker: f623/8994 already hold
   the measured per-kick heap-call family {88, 240, 304, 352, 384², 704, 832} B at
   ~9–10 calls/kick — the counting arm exists; run it on this scene.]

## Contradictions

- None yet on this topic. Adjacent standing facts that must compose: kick keys never recur
  (9edc, 225d — sharing/interning the mint is dead), yet the knots are regenerable from the
  key (5465) — so the memo is a private cache per binding, which is exactly why its extent
  (not its sharing) is the lever.

## Runs

- 20261020-1116-system-bd4b (system, awaiting grade): the mint's knot vector measured kick by
  kick — ρ 0.70/0.88 µs↔knots, knots 85–91% of minted heap, 12.5 KB/kick on members, 6 vs
  148 median knots per class in one scene.
