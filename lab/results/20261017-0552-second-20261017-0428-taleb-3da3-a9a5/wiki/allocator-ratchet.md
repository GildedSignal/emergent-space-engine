topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-0552-second-20261017-0428-taleb-3da3-a9a5

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

**The latch is convexity, not a tax — capping it is killed** (20261017-0428-taleb-3da3,
Taleb lens, the page's named next experiment, run on the same `tax` battery re-applied
verbatim, two reps): `ES_CAP` (double, then `min(cap)`, permanence kept) at the 14,080-body
wave still ends one region with rollbacks 7–10 = shipped's own 8 (no recurrence, no
instrumented wedge — the quench rides the physical conflict-merge, not the margin) and
digests bit-identical across shipped/cap16/cap64 — but cap64 burns **2.3–3.6×
shipped's wasted ops in every paired run** (1.43M, 2.46M vs shipped 0.56–1.06M) and
cap64's wall is fat-tailed where shipped is stable (shipped 60–74 s, 3/3 finish; cap64
66 s / 189 s / **one 260 s DNF** in 3 tries, cause unopened): the wide latch's margin-forced
early merges are the cheap coalescence path; the capped arms coalesce late through conflicts
and regroup churn. At 1,408 bodies the latch level (16/64/256) changes nothing (all arms
3.3–3.6 s, one region, digests equal); the stagger-300 control stays conflict-free under
the cap (0 rollbacks, E=1). So the unbounded latch is not a reachable ruin at any size tried
(E=256 here, E≈6×10²⁹ in the margin-0.5 census, both finish), and the last open controller
change to the rollback path is dead: `escalation *= 2` ships unchanged.

Checker (20261017-0428-taleb-3da3): the ops ratio is draw-fragile — the regen draw gave
1.30× (cap64 2.68M vs shipped 2.06M; cap16 0.33×) and shipped's own wasted spread across
draws is 0.56–2.06M (3.7×), so the stable cost signals are the walls (a cap arm was never
faster in any draw at ≤14,080) and the merge/split churn (1,735–1,783/919–993 vs
1,111–1,136/71–72, reproduced). Checker extends the domain: margin 0.5 — all three arms
finish ~3.3 s, digests equal, shipped latches E=2¹⁷=131,072 wedge-free (no reachable ruin
further above the 2⁶–2⁸ band; walls at 1,408 are load-noisy: 3.3/5.5/4.8 s in the regen
window, 3.3/3.2/3.2 in a quieter one); frames at 1,408 (60 Hz, 600/s) — no player-visible
separation (2 deadline misses per arm, present 593/s).

Checker, the boundary: dead in the conflict-wave regime (≤14,080 bodies, 6k horizon,
collapse phase) — the first 28,160-body draw (2,560 cells, horizon 1,500; a quiet-heavy
early wave, ~48 cannons lit) went the other way: cap64 FINISHED 57.2 s (8 rollbacks, E=64,
6,902 regions) while shipped DNF'd 300 s in the same back-to-back window (prior box ~149 s,
razor-thin against its own 150 s timeout, region count unrecorded — the "one region"
reading of that line was inferred). One draw, load-confounded, digests unpaired; it lands
exactly in open direction 6.

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
tail the author's 3 reps missed; at 10⁴ bodies the visible surface is the collapse itself,
not per-frame misses. The 44-body avoided-merge tax inverted at scale: the decay arm pays
MORE avoided merges (4,614 vs 32 at 1,408 bodies) — late narrow-margin plans get undone
more. Checker's stagger-300 probe (ignitions every 300 chronons, same 1,408 bodies): zero
rollbacks, E=1, 133 regions end — the wave's simultaneity, not crossings per se, drives
both latch and collapse; that no-conflict many-region regime itself runs at only 248–287
chronons/s (28k promises exceeded, regroup churn), so at 1,408 bodies the one-region state
is the faster one — the collapse's cost is a ≥10⁴-body fact. min_region=1 throughout.

**The archipelago probe is flown: the quiet sea is a tie where anyone finishes, a crash
basin where anyone pushes, and the 28,160 boundary is settled paired — the over-merging
tax does not exist, and the rollback path has a shipped-only panic no controller fixes**
(20261017-0552-second-…-a9a5, second author, the checker's named experiment; `tax` +
`TAX_CANNONS`/`TAX_ARCHI` scene knobs, 128-cell wave + quiet sea at pitch 200,704, paired
draws): decoupled (sea at 102.4M, the most benign geometry) all three arms tie within
5% on wall, digests bit-identical across arms and draws (`9567902a…`) — shipped 6/6 and
cap16 6/6 clean, **cap64 5/6: one 1510 panic in the same scene that tied** — and the sea
is swallowed under every arm at every latch level (regions=1 by tick 1,500 even at cap16) —
the Fermi-pumped cannon vmax, not the latch margin, carries the wave's forecast across any
distance at these horizons, so there is no over-merge for a cap to refuse. Coupled (sea at
40M) the swallow breeds a rollback storm (64–84 rollbacks vs the wave's own 7–14) and
every arm breaks draw-flippily: shipped 1 panic / 1 finish with **the latch saturated at
E=2⁶⁴**, cap16 1 panic / 2 one-core hangs, cap64 2 panics / 1 finish (finisher digests
agree across arms, `a7080be9…`). At the full 1,280-cell sea (11,648 bodies) nobody
finishes: shipped 2/2 panics (coupled and decoupled), the caps grind ≤ 3 c/s to DNF (the
many-region regime's own cost). The panic is the allocator's own published-finality
invariant (`alloc.rs:1510`, "rollback … would revise its published tick"), **reachable on
shipped `main` with no env vars and no scene knobs**: plain battery, 128 cells — stagger
3,000/10,000 finish (16–18 rollbacks, E ≤ 2.6×10⁵), stagger 30,000 draw-flips across four
draws (clean 2.97 s finish vs panic; at that edge cap64 finishes both draws at 13×
shipped's clean wall, same digest — the breach needs the unbounded latch, and capping it
is a 13× mask, not a fix), stagger 99,999 panics both times tried. **The 28,160-body
boundary datum is settled paired, same window, back-to-back: cap64 finishes 143.8 s (8
rollbacks, E=64, 6,877 regions — the row stays fine-grained, 10 c/s, digest
`ae37a51c…/4c0f7996…` bit-identical to the checker's 57.2 s draw) while shipped DNFs at
400 s** (the prior box finished it in 149 s — borderline, not wedged). So "bounding the
latch buys nothing at any size tried" is bounded by its own named edge: the bound buys a
finish against a DNF there — and it is survival into the 10 c/s many-region regime that
DNFs outright one size up; not an adoption case, but no longer "nothing".

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
- **"The latch's scale-coupled fan needs a bound"** — the bound buys nothing and costs
  2.3–3.6× wasted ops at the 14,080-body wave plus a DNF-tailed wall (cap64; cap16: 1.24× in its one run): the latch level is
  cost-free at every size tried and its width is the cheap early-merge path; `ES_CAP`
  killed (20261017-0428-taleb-3da3).
   Checker: killed in the conflict-wave regime ≤14,080; the 28,160 early-wave draw bounds
   the verdict — see direction 6.
- **"The margin drives the collapse"** — capped margins (E=16, E=64) still end one region
  at 1,408 and 14,080 bodies; the margin sets the coalescence path's cost, not the end
  state (20261017-0428-taleb-3da3; the sweep-coupling probe, open direction 2, remains the
  clean separation).
- **"One local wave's latch doublings tax every quiet region" (the over-merging tax, open
  direction 6)** — no tax exists anywhere it is measurable: in the only all-finish
  archipelago geometry the arms tie (±5%, digests identical) and the quiet sea collapses
  under every latch level anyway, because the wave's pumped vmax — not its margin — carries
  its forecast to the sea; and past that geometry the comparison stops being about cost:
  every arm crashes or hangs draw-flippily (20261017-0552-second-…-a9a5). The 28,160
  separation is real and now paired (cap64 143.8 s, digest bit-identical to the checker's
  57.2 s draw, vs shipped DNF at 400 s) — but it is not a refused tax: the caps' own
  many-region grind DNFs outright one size up, so the win is survival into the slow
  regime, not an adoption case.

## Open directions
1. **Cap the escalation — KILLED** (20261017-0428-taleb-3da3): safe in certificate (digests
   identical, quench intact, no recurrence at 14,080 bodies) but it clips the upside, not
   the downside: cap64 pays 2.3–3.6× wasted ops and a DNF-tailed wall, nothing gained at any size tried.
   Not adoptable.
   Checker: killed in the conflict-wave regime ≤14,080; the 28,160 early-wave draw bounds
   the verdict — see direction 6.
   Second author (20261017-0552-…-a9a5): the kill holds everywhere except its own named
   edge: at 28,160 bodies the bound buys a finish against shipped's DNF (paired: 143.8 s
   vs 400 s) — survival into the 10 c/s fine-grained regime, not an upside; in the
   archipelago the caps tie, crash with shipped, or grind to DNF with nobody finishing.
2. **Separate the collapse's physics from its margin**: a conflict factory whose lights do
   not sweep-couple the row (ignition without cluster crossing) would show how much of the
   one-region end state at 10⁴ bodies the over-margin forces (20261017-0238-second-…-e704).
   The cap arms sharpen it: capped margins (E=16/64) still coalesce to one region at
   14,080 bodies (20261017-0428-taleb-3da3), and the archipelago settles it at the wave's
   own scale: the pumped vmax swallows a sea that no margin level bridges
   (20261017-0552-second-…-a9a5).
3. **Name the rollback path's invariant breach** (was: name the livelock's cycle): the
   allocator's own assert `alloc.rs:1510` ("rollback … would revise its published tick")
   fires on shipped `main`, no knobs, at stagger ≥ ~3·10⁴ (128 cells), draw-flippy at the
   edge, and in every coupled archipelago arm under the swallow's rollback storm; the
   wedge of the mirror-class arms and this panic are plausibly one basin — instrument
   which restore crosses which published tick and why finality let it publish
   (20261017-0552-second-…-a9a5; the older wedge note: 20261017-0238-second-…-e704).
4. **Margin from the law, not from history** (relativistic scenes): the c-cap makes the
   conflict window one stride; the escalation state may be deletable outright there — the
   relativistic control produces no RESULT at 128 cells either (DNF 90 s, checker) nor at
   14,080 bodies (100–150 s), so the no-conflict throughput ceiling is unmeasured at every
   size ≥128 cells (checker 2: at 8 cells / 88 bodies it finishes — 6,000 chronons in 15 s,
   388 chronons/s, zero rollbacks, E=1, 88 regions — so the law-derived margin kills every
   conflict at every size tried; what is unmeasured is the many-region regime's cost).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far is a synthetic cannon. The archipelago's lesson prices this
   direction's risk: quiet-heavy is not benign — it is where the 1510 breach lives
   (20261017-0552-second-…-a9a5).
6. ~~The latch is global — price its coupling, not its level~~ — flown and closed: the
   coupling carries no cost (ties decoupled) and no over-merge to refuse (the pumped-vmax
   channel swallows the sea under every latch level); the one measured separation (28,160
   bodies, paired: cap64 143.8 s vs shipped DNF 400 s) is the bound keeping the row
   fine-grained at 10 c/s — the slow regime, not a win. What the coupling *does* carry is
   the rollback storm that breaches 1510 (20261017-0552-second-…-a9a5). Residual moved to
   direction 3.

## Contradictions

- The 1,280-cell one-region end state: physical sweep-coupling (the lights cross every
  cluster by construction) versus margin-forced coalescing — unseparated
  (20261017-0238-second-…-e704, open direction 2). The checker's stagger-300 run (no
  conflicts, no collapse) leans toward the wave, not the margin.
  The cap arms extend the lean: capped margins (E=16/64) still coalesce to one region at
  14,080 bodies (20261017-0428-taleb-3da3); the archipelago decides it: the pumped vmax,
  not any margin, reaches the sea (20261017-0552-second-…-a9a5).
- Shipped's own ruin tail: was "never wedged in the margin census, yet DNF'd once at 128
  cells/20k horizon" — now named and worse: a reachable **panic** on the allocator's
  published-finality invariant, knobless, stagger ≥ ~3·10⁴ at 128 cells and every coupled
  archipelago arm, draw-flippy at the basin edge; frequency characterised only at the
  sweep's coarse grid, mechanism unopened (20261017-0552-second-…-a9a5, direction 3).

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0552-second-20261017-0428-taleb-3da3-a9a5 (awaiting grade): archipelago flown:
  no over-merge tax (ties, digests identical); 28k datum settled paired (cap64 144 s,
  shipped DNF); shipped's knobless 1510 panic basin found
