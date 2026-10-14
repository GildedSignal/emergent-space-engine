# Dossier — 20261014-1631-library-7f99 (library lens)

**Claim.** The library, mined verbatim for the first time (762 highlighted books, 4,580 highlights,
cached), prices the N-ladder's own method: Musk's 10% add-back quota judges the engine's deletion
record (at quota at the law level, 0-for-the-frame-path → the named backlog is unfired), automation
comes last (3 guard families on shipped code exist only to manage undeleted state), shared caches
pay full sensor cost, promotion is a say-no filter on the refit's refusal, and the lookup budget
(427–877 recompiles/frame against measured demand ≤ 1.4/s) makes the entry-field deletion safe by
≥ 10³ headroom.

**Bottleneck.** The board's first: bodies in the flyable engine (10⁶ smooth, 10⁹ the goal). The
ladder's terms are measured (a2c1, 0e37, b29a, effb); what the page lacked is the *method* for the
deletion program the page itself prescribes (open directions 0–4). This run supplies its acceptance
criterion, its ordering, and its safety arithmetic — no new physics, orders-of-magnitude leverage
only through deleting the right terms without regressions.

## The five lessons (each: verbatim highlight → mechanism → change → cheapest test)

1. **The deletion quota.** *"Delete any part or process you can. You may have to add them back
   later. In fact, if you do not end up adding back at least 10% of them, then you didn't delete
   enough."* — Musk, in Isaacson, *Elon Musk*. Mechanism: without a quota, deletion converges to
   timid — near-misses get repaired instead of removed, and repair welds the part in. Change: rule 1
   ("deleted rung before cheaper rung") gains its acceptance criterion — ~10% of deleted terms must
   come back, else the deletion was too timid. Test: the audit below (seconds, rerunnable); the next
   deleted rung records its add-backs.
2. **Automation last.** *"Always wait until the end of designing a process—after you have
   questioned all the requirements and deleted unnecessary parts—before you introduce automation."*
   — Musk, same. Mechanism: a scheduler built around undeleted state turns that state into a
   requirement (its fallbacks inherit the walk it should have killed). Change: the allocator (least-
   slack, burst absorption; PRINCIPLES #12) lands **after** the frame-path deletions; every
   guard/fallback around shared state is a deletion marker, not a scheduling input. Test: the
   site count below; a2c1's arms rerun with the guards simply removed.
3. **Shared state pays sensor cost.** *"Removing radar and ultrasonic sensors and relying solely on
   vision may make the perception problem easier. … The full cost of sensors includes not just their
   implementation, but also procurement, maintenance, and incorp[oration]."* — Karpathy, Lex #333.
   Mechanism: a doll-wide cache looks free at the call site; true cost = maintain (the write-once
   monotone cap) + incorporate (every consumer's window widens by it). Change: at break #3, **delete**
   the doll-wide `speed_cap` and the all-dolls density rule, skip the one-line and few-line repairs
   (a2c1's fix order inverts); the per-body speed bound is the one exact instrument. Review rule: any
   doll-wide/singleton read pays full-cost accounting or goes. Test: patch deletes both sensors,
   10³ arm rerun — expect the walk at the certificate's keep set (17), not 1,017 (prediction 4).
4. **Promotion is a filter, not machinery.** *"Do nothing unless you must, and when you must
   act—hesitate."* — the Second Foundation's rule, Asimov, *Foundation's Edge* (with Buffett's
   "high filter" via Taleb, *The Logic of Risk Taking*). Mechanism: a fixed threshold evaluated at
   the event is one decision with no standing state; hysteresis/rank machinery stays alive to
   re-decide. Change: open directions 1 and 3 collapse — the refit's refusal **is** the
   promote-to-live trigger (b29a measured refusal at Δv/v ≈ 1: 9–26%); the sticky binding (8,257 B,
   no demotion) is deleted, the promotion is the stack-local event (12–40 B). Test: the shipped
   chatter case (retrograde 0.49 R_H) — predict those handoffs never refuse the refit, so the
   chatter vanishes; one dynamics run, no new code path.
5. **The lookup budget.** *"They had wasted all their time memorizing stuff like that, when it
   could be looked up in fifteen minutes."* — Feynman, *Surely You're Joking*. Mechanism: storing
   derivable state taxes every frame in bytes to save a µs lookup inside a ms budget; the
   arithmetic, not the instinct, decides. Change: direction 0's build (`Segment` drops `entry`,
   gains key + two-word) gets its acceptance number — at 33 ms/frame the engine can afford 427 (p95)
   – 877 (p50) recompiles per frame; measured demand is 0/s (belt) and 1.4/s (cast) → ≥ 9×10³
   headroom; the two-word completion is the expected ~10% add-back (24 B = 4.6% of the 520 B
   deleted). Test: the arithmetic (below); after the build, 0e37's census re-runs as acceptance.

If the quota is honoured, the next ladder window fires the four standing deletions instead of
repairing them.

## Evidence (all regenerated by `regen.sh`, ≤ 1 min)

- **Corpus:** `work/highlights.ndjson` (cached Readwise export, 1.8 MB): 4,580 highlights, 762
  books. All six anchor quotes verified verbatim, exactly once each (`audit.py` §2).
- **Deletion audit** (`audit.py` §3): **26 grep-backed kills** across docs/HISTORY.md, lab/board.md,
  lab/wiki (probe-1 steps, probe-2 staircases, sd16/24/32, river, conjunction kicks, g8/g16/g8-half,
  nf1/nf2, kick-avg/hill-torus, element-sort/shear-grid/hier-bounds, eob-doll, SyMBA-float, TRACE,
  the jet, the exact-memo lever, q-secular, encounter-setup deferral, the fleet pairwise tier, the
  Wide tightening, 14 B12 candidates, the one-word readout, B16's static memo, faction thresholds,
  the plane's binary doll, continuum-geodesics-as-law, the frame tier, the metronome cadence);
  **5 revival-shaped events** (rotating binary doll — the family H0210 killed, adopted 1 Oct;
  chronon kept as test judge; two-word completion in flight; cast exception anticipated; JANUS
  integer changeover). Landed same-job add-backs: 2 → **8%**; all five → 19%: the law level brackets
  the quota. The shipped frame path: **0 add-backs** (only the frame tier and the old view search
  ever deleted there) — below quota; the unfired backlog is exactly a2c1's sensors + b29a's sticky
  promotion + 0e37's `entry` field.
- **Automation debt** (`audit.py` §4): 6 grep-anchored sites in two files — the caps
  (`radial.rs:50-51`, maintained `:193,:226`, consumed `:247-248`), the density rule
  (`radial.rs:254`) feeding the walk-all fallback (`encounter.rs:175` `0..ctx.bodies.len()`), the
  hull-of-history widening (`radial.rs:192-196`). Their measured failure modes are a2c1's breaks
  (cap poison 84×, walk 194/call vs keep 17, walk-all 1,017/1,028 at 10³, entries 905 → 2,885).
- **Lookup budget** (`audit.py` §5): 33.3 ms frame → 427 (p95, 78 µs) / 877 (p50, 38 µs) recompiles
  per frame; 12,821/s at p95 against demand 0 (belt) and 1.4/s (cast) → 9,158× headroom over the
  cast; +24 B two-word = 4.6% of the 520 B `entry` deletion; standing 1,806 B/body of which the
  build deletes ~520 accounted (~800 footprint).
- Commands: `python3 lab/results/20261014-1631-library-7f99/work/audit.py` (each step ≤ 60 s).

**Predictions** (`predictions.md`, written before the audit): (1) held — ≥ 20 kills (26), ≤ 2 landed
add-backs (2; three more in flight disclosed); (2) held — ≥ 3 guard/fallback families (3 families,
6 anchored sites); (3) held — ≥ ~400 recompiles/frame (427–877) and unbounded belt margin; (4)
held-out for the next run (sensor-deletion walk ≈ keep set; chatter vanishes under the refusal
filter) — not runnable here, no patch budget.

**What would make it wrong.** The quota is Musk's factory heuristic, not physics: if the frame-path
deletions (sensors, sticky promotion, `entry`) trigger regressions that need repairs rather than
add-backs, the quota misleads and only the repair count matters. The Karpathy anchor is an AI-episode
note in his library, not a book passage — weakest provenance of the six (still his stored highlight).
The audit's kill/add-back classification is mine over grep anchors; a stricter counter could put the
law level below 10% (only the binary-doll family is same-job). Cost of adopting: zero code; the
sequencing rule delays allocator work behind deletions, which costs one window if the deletions
stall.

**Fit with PRINCIPLES.** #1 ("the cheapest compute is compute not done; delete before optimizing"):
the quota is its enforcement. #19 ("a fix signals the wrong representation… bandaids accumulate"):
lesson 3 is that rule applied to shared caches. #12 (smoothness, the allocator): lesson 2 orders it,
not weakens it. #3 ("compute only surprises… redshift and co are not derived but emergent"): lesson
5 is the same law for memory. #22: the filter is the simulation deciding (the refit refuses), not a
scheduler heuristic.

**The lens may have missed.** A library mined by keyword leans toward quotable aphorisms; the
practitioner material with real telemetry (Gray/Graefe's five-minute rule, Denning's working set,
sweep-and-prune coherence) is *not* in this library, and the three lessons it would have priced
(break-even hold interval as arithmetic on birth constants; phase-axis incremental sort for the
encounter tier; LRU-K-style read caching) remain unanchored — flagged for a run that can borrow
outside the corpus. The audit counts *events in text*, not code paths: a deletion that happened
silently in a merge is invisible to it. And analogies are cheap: these five survive only because
each changes a named decision with a runnable test.
