topic: nladder
status: open
closed-by:
valid-while:
updated: 20261013-2130-library-ae3d

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the append —
measured on shipped code (20261013-2130-library-ae3d; checker-corrected).**

Measured (`shipmem` ladder, Linux/x86 shared runner, orders of magnitude only): the timed
update path touches only the first shelf (`ladder.rs` events section), so it performs
identical work at any population — 6–9 ns per update across the author's own repeats (the
reported 6→7 over 10× population is inside that noise band, and the checker's rerun
flipped its sign); what is genuinely measured across populations is bits per member
(12.347→12.329 over 10×) and per-member streaming. The storm rung keeps updates at 6–7 ns
while memory goes 12.3→48.4 bits per member at 30% churn and the program inference gives
up gracefully (`inferred` true→false, packed-form fallback, 0 round-trip mismatches; at
rung 1, 64.1 bits — the checker's edge case). The spike anatomy: on a 1.0M-ship convoy
with 20k updates, hot p50/p99/max = 34/1,271/9,217 ns while one compaction step peaks at
1.26 ms (2,570 repacks). Checker: on `battle` the worst compaction step is 12.1 ms with
**zero repacks** and the append is tight (p99 48 ns, max 2.9 µs) — the enemy is the
compaction step, whichever internal pass it is; schedule compaction in slack, never in
the hot frame. At 10× the event rate the append max grows 9.2→36 µs, still 33× below the
compaction step. Layer caveat: this is the storage-layer kick path, not the plane's
compact→live promotion — that is `resolve_handout`, 486–585 µs, sticky, no demotion path
(frame-cost, 20261013-1915-fermi-367f, checker-corrected).

The five rules (each with a falsifier, from Julien's library, run dossier §Evidence):
1. **Delete before you measure cheaper** (Musk's algorithm): every ladder term (per-frame
   walks, rekey, queue, memory per live body) gets a *deleted* rung before a *cheaper* rung.
2. **The live set is a rank, not a count** (Zipf/Extremistan): promote by rank in the
   measured per-body surprise-rate distribution; k is a certificate, not a constant.
3. **Promotion judges on event time, not frame time** (sampling noise): hysteresis windows
   in the body's own event time; the 210-handoff chatter is the counterexample to fix.
4. **Buy the option, not the headroom** (optionality): the O(1) hot append *is* the
   promotion; no ahead-of-demand promotion, no second promotion path. (Checker: the
   store's append is the storage-layer kick path; the plane's compact→live promotion is
   `resolve_handout`, 486–585 µs and sticky — the option to buy there is demote-at-commit
   or dormancy, per frame-cost.)
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.

## Refuted

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.

## Open directions

1. **The surprise-rate distribution on shipped scenes** (rule 2's falsifier): one
   instrumented run logging kicks per body per orbit; if the distribution is not
   heavy-tailed, the rank rule dies and the fixed fraction stands.
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the
   term gone; count what the per-frame walk visits that the hot tier did not touch.
3. **Event-time hysteresis on the shipped chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
   into the shipped allocator and check the p99 frame.

## Contradictions

- None recorded yet.

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
