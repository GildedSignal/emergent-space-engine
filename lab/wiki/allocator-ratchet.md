topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-0238-second-20261016-2138-dynamics-217f-e704

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The rollback controller has no restoring force, and at scale neither it nor its 10-line
decay mirror is adoptable: the ratchet's latch level grows with the conflict wave and the
mirror falls into a livelock basin (20261016-2138-dynamics-217f, dynamics lens, 44 bodies;
20261017-0238-second-…-e704, second author, 44 → 14,080 bodies; shipped
`crates/allocator` + public-API instrument `tax`, patch in the run's `work/patch.diff`).**
`escalation *= 2` at every rollback (`alloc.rs`) is global and never decays; conflicts
self-quench exactly at the derived bound (forecast growth `margin·E·vmax + (E−1)` ≥
achievable speed). The second author flew the checker's named experiment (≥10⁴ bodies,
interleaved arms, batch + frames): the frozen latch level is 2^(rollbacks) and so **grows with
the conflict wave** — measured E = 4 → 32 → 64–256 at 44 → 88 → 1,408 → 14,080 bodies (1–2 →
5 → 6–8 rollbacks; checker correction: the level **saturates at 2⁶–2⁸ from ~10³ bodies** —
the 14,080-body sample latched at 128 in both checker-side runs, and at 64/128/256 across
three same-scene runs, so "256" was one draw; stagger 30, Fermi-cannon battery) — and at
14,080 bodies the scene ends as **one region at ~82 chronons/s** (74 s for 6,000 chronons,
checker rerun 56 s at 107; at 28,160 bodies 1,500 chronons run in ~149 s at 10 chronons/s
with E=512=2⁹ at 9 rollbacks — checker 2; the earlier "DNF at 150 s" was the timeout, and
the latch clears 2⁸ at the next decade, so the 2⁶–2⁸ "saturation" is a band, not a cap —
the collapse's cost is a ≥10⁴-body fact; caveat: the battery's sweep lights physically couple the row, so
the collapse is part physics — the attribution experiment is named below). Note: the
instrument's `seed` argument is dead code (`Rng(7+13i)` ignores it), so every measurement is
one world per size.
The ES_DECAY mirror (halve at every sync grid) and
the per-region ES_LOCAL variant both **livelock** in the narrow-margin regime they create:
at 1,408 bodies runs DNF in 5 of 9 narrow-margin tries with all 8 workers burning CPU
(decay 2/5, local 3/4; another local run ground through 185 rollbacks vs 7–8 clean —
per-lineage doublings decay before the quench globalises), and both DNF > 240 s at 14,080
bodies where shipped finishes in 74 s; shipped at margin 0.5/1.0/2.0 never wedged (the
ratchet's latch absorbs recurrence by latching higher — 25 rollbacks at margin 0.5, still
3.5 s; checker correction: the margin-0.5 rerun also finished wedge-free but in another
basin — 79 rollbacks, E≈6×10²⁹, 8.5 s — so the census numbers are one draw; and shipped
itself DNF'd once at 128 cells/20k horizon, 1 of 6 tries across author+checker runs, so
"permanence prevents livelock" is a tendency, not a guarantee). The ratchet's permanence is
what prevents the livelock; the mirror's equilibrium sits inside it. Where arms finish,
outcome digests are **bit-identical across all arms and reps** (4, 8, 128 cells;
`d75dee4a…`/`42e4e3b4…`; checker extends: also across arms at stagger 300, and across arm
and margin at the 6k horizon) — the certificate moves scheduling, never results. Frames
harness at 1,408 bodies (60 Hz, rate 600, 3 interleaved reps × 3 arms): present 575–585,
no player-visible separation for shipped vs decay (the 44-body nil extends) — but the
checker's 2 further ES_LOCAL frames runs **both collapsed** (present 286 and 312 of 600,
64 and 58 deadline misses, buffer p50 0 and 22): the local arm has a player-visible ruin
tail the author's 3 reps missed; at 10⁴
bodies the visible surface is the collapse itself, not per-frame misses. The 44-body
avoided-merge tax inverted at scale: the decay arm pays MORE avoided merges (4,614 vs 32 at
1,408 bodies) — late narrow-margin plans get undone more. Checker's stagger-300 probe
(ignitions every 300 chronons, same 1,408 bodies): zero rollbacks, E=1, 133 regions end —
the wave's simultaneity, not crossings per se, drives both latch and collapse; that
no-conflict many-region regime itself runs at only 248–287 chronons/s (28k promises
exceeded, regroup churn), so at 1,408 bodies the one-region state is the faster one — the
collapse's cost is a ≥10⁴-body fact. min_region=1 throughout.

## Refuted

- **"The rollback response is a controller"**: it is half a controller — the AIMD stride
  half restores, the escalation half only doubles (20261016-2138-dynamics-217f).
- **"Rollbacks cascade"**: measured self-quenching at the derived bound
  (20261016-2138-dynamics-217f).
- **"The 10-line decay mirror restores the equilibrium"** — at scale it restores a livelock:
  recurring conflicts under re-narrowed margins wedge the allocator (all workers spinning,
  no progress), 1/3 tries at 1,408 bodies, DNF > 240 s at 14,080
  (20261017-0238-second-…-e704). The mirror also refires conflicts by design (6 rollbacks
  vs 2 at 44 bodies, the first checker).
- **"The ratchet's latch is a constant (×4) tax"** — the latch level is 2^(conflicts before
  quench) and grows with the conflict wave / scene size
  (20261017-0238-second-…-e704); the 44-body ×4 was the smallest sample.
- **"Per-region escalation fixes the wrong locality"** — ES_LOCAL matches the decay arm's
  counters when it finishes (4,690 vs 4,614 avoided) and wedges more often (3/4 at 1,408
  bodies); the binding defect is the missing bound, not the scope
  (20261017-0238-second-…-e704).

## Open directions

1. **Cap the escalation** (`*= 2` then `min(cap)`): keeps the quench (the anti-livelock
   property the mirror loses) while bounding the latch's scale-coupled fan. One line,
   untested — the named next experiment (20261017-0238-second-…-e704).
2. **Separate the collapse's physics from its margin**: a conflict factory whose lights do
   not sweep-couple the row (ignition without cluster crossing) would show how much of the
   one-region end state at 10⁴ bodies the over-margin forces (20261017-0238-second-…-e704).
3. **Name the livelock's cycle**: instrument the spinning state (which loop, which
   condition never clears); the wedge is the mirror-class arms' ruin and its mechanism is
   only inferred (narrow margin + recurring conflicts + many regions), not opened
   (20261017-0238-second-…-e704).
4. **Margin from the law, not from history** (relativistic scenes): the c-cap makes the
   conflict window one stride; the escalation state may be deletable outright there — the
   relativistic control produces no RESULT at 128 cells either (DNF 90 s, checker) nor at
   14,080 bodies (100–150 s), so the no-conflict throughput ceiling is unmeasured at every
   size ≥128 cells (checker 2: at 8 cells / 88 bodies it finishes — 6,000 chronons in 15 s,
   388 chronons/s, zero rollbacks, E=1, 88 regions — so the law-derived margin kills every
   conflict at every size tried; what is unmeasured is the many-region regime's cost).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far is a synthetic cannon.

## Contradictions

- The 1,280-cell one-region end state: physical sweep-coupling (the lights cross every
  cluster by construction) versus margin-forced coalescing — unseparated
  (20261017-0238-second-…-e704, open direction 2). The checker's stagger-300 run (no
  conflicts, no collapse) leans toward the wave, not the margin.
- Shipped's own ruin tail: never wedged in the author's margin census, yet DNF'd once at
  128 cells/20k horizon (1/6 author+checker tries) — frequency and basin uncharacterised
  (checker, regen + adversarial runs).

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
