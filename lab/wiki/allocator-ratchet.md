topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-1447-dynamics-fd35

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**NEW (20261017-1447-dynamics-fd35, dynamics, direction 7 answered on the state side):**
the race is measurable as a state property on shipped code, and on every draw flown it
sits exactly on its boundary. A print-only instrument (HAZ at every publish: max
published `fin_hi`, deepest live truth start `S`, per-pair armed margin A over in-flight
stride reach hulls × live truths; PRE before every certify with the measured box: the D
the upcoming clash would restore; RB/FIRE inside rollback: the exact assert inputs)
shows: **the equality law — all 8,213 realized clashes across 45 arm-processes restore at exactly
`fin_hi == s0`** (min D = max D = 0, every RB margin 0): finality's coalescing and the
certificate's separation pin the same contact tick, so publication rides the boundary as
an attractor, never past it and never behind it. **The armed episode** (dispersal probe:
one busy-region × old-truth pair, A = 48 → 128 chronons over 10 publishes while S stuck
128 below F) resolves by **pruning** (the truth ages out of restorable history, S = −1,
stride certifies clean), not conflict — the race has two resolution channels, and crash
incidence is the probability the conflict channel wins while armed > 0. **The negative
certificate:** armed ≤ 0 at every publish AND D ≤ 0 at every certify ⇒ the finality
assert is unreachable for that draw — decided from state (fires = 0 on all 45 arm-processes;
4/13,034 publishes ever armed, all in the one probe — which, the checker found, ran on a
pre-sabotage build: its SUM lacks the sab echo and starts rgn0=1; regen.sh's `sab 0`
argument maps to Some(1), so the regen line does not express "no sabotage" and reruns a
different scene, rgn0=1600, never armed. The phenomenon itself regenerates with sabotage
truly disabled — checker arm sab=None: 17 armed publishes to A = 192, rb = 0, every episode
resolved by disarm — and the equality law held on every fresh draw, including the
checker's window-32, seed-33/101, sab-6 and 8-s arms, all D = 0, 0 fires; min_region 32
control: 4 rollbacks
vs ~1,300, never armed; replicate: rollback counts move with the wall clock (1,305 vs
1,326) while the equality law holds in both). The engine-side fix's test can therefore be
"armed ≤ 0 maintained" instead of window Monte Carlo, and its measured cost on these
classes is the refused lead: ≤ 128 chronons once (10 publishes), ≤ 48–96 in churn, 0
elsewhere. Untested side: no firing assert reproduced here (0/45 vs 7/12 on the
integrator's selfchurn harness, which lives on its branch) — the positive direction
(crash ⇒ armed > 0 first) needs one reproduction on that harness; the PRE scan's closure
is a descendants superset whose "over-arm, never miss" direction is asserted, not shown
(rollback's `affected` can include snapshot-sharing siblings outside both lineages).
regen.sh rebuilds instrument + matrix arms in ~6 min (its summary step dies on a
relative-path bug; run analyze.py from the repo root).

**The finality-assert conflict is resolved and now at protocol strength: the crash is an
engine-side publish/rollback boundary defect, every overlap class reaches it, and no
driver or scene dodge closes it — the engine-side fix is the only door.** Frames mode
crashes on a scene with **no bulk approach at all** — one dense slow gas cluster
(selfchurn, internal spread 2 units/chronon, `min_region 1`) — at the keeping-up rate,
with panics at **chronon 32–96**: the first ~0.2 s of a loaded scene
(20261017-1018-taleb-01e7; re-run 3/9, bc0f). Both limbs of the driver rule are dead at
the page's protocol (≥ 3 seeds × ≥ 2 replicates): on-grid chunked targets crash
(chunk 128: 2/3 in both windows; checker: 96 and 512 too), and **single-call batch
crashes 7/12 (11/17 pooled with the checker), identically on-grid (3/6) and off-grid
(4/6), always at scene start 32→48** — the crash is decided in the first ~48 chronons
(survivors finish the whole 1800-horizon in 0.4 s), so horizon class cannot matter
(bc0f). Panic values per seed are stable across replicates; reachability is a
wall-clock race with **seed-skewed propensity** (s11 4/4, s15 3/4, s21 0/4; one
same-seed replicate pair splits). **Two crash phases exist**: scene start under churn
(chronon 32–96) and **late quiet-phase reclash** in the dispersed/crossed classes
(chronon 1120–2720, panic gaps 16–144 = 1–9 windows) — this window crashed vmax-16
3/6 (4/22 pooled), vmax-8 2/6 (4/18 pooled), crossing 1/4 (the first crossing crash,
1/16 pooled) and vmax-8-at-480 1/3, so "quiet classes are safe / rare, not never" is
dead as a window-independent statement: **incidence is fat-tailed across windows; only
the zero-churn wave (0/15 pooled) and `min_region 32` (rb exactly 0, 9/9 pooled) are
strictly clean** — the knob deletes the conflicts, not the defect (bc0f). rb is not a
separator: n480-at-vmax-2 survivors sit at rb 123–180, far above the n240 crash band
57–95, and survive 5/6; a crashing draw never prints its rb (the row prints at
completion), so rb cannot be a draw-level predictor by construction (bc0f). Escalation
is exactly **E = 2^rb on every survivor, 37/37 across all arms, up to 2^180** (bc0f) —
the page's unbounded ratchet. Window 32 survived rb 83–109 (9/9 pooled across three
windows): the coarser stride/grid widens the race margin — a lead, not a verdict
(20261017-1018-taleb-01e7, checker, bc0f). The engine-side fix (refuse an advance
whose rollback would cross a published tick, or hold publication; 9b46's open
direction 1) is the confirmed requirement
(frames reachability first shown by 20261017-0839-dynamics-b966, 14/35 across five
windows, checker-confirmed).

**Prior standing (9b46, 3da3, 217f, e704 — unchanged).** The wave response is
Extremistan: at one frozen scene and N = 27,936 the seed flips the end-state *class*
(s7 → 1 region, s1 → ~2,400, s2 → ~2,500–4,700, s3 → 1,389) while nothing else is
seed-fixed (the latch E = 64–512, region counts, walls spread 1.65×/2.4× across
replicates); no quantity follows its attributed knob (E is drawn, not an N-law; the cap
verdict inverts across draws); the no-conflict regime is the cost floor (the quiet
control stalls < 0.6 timeline chronons/s at 28k); publication cadence is a path knob;
outcome digests are bit-identical across arms, caps, margins and replicates wherever
arms finish — the certificate moves scheduling, never results. Batch interior-tick
targets (off the window grid) are a separate, deterministic crash channel (7/11 on
5d87's box; on-grid 96–512 never crashed there — true for *their* sparse scenes, refuted
as a complete rule by the churn class above).

## Refuted

- **"The crash is a window-grid defect of chunked batch drivers, not a live-path
  hazard"** (20261017-0839-second-…-5d87, as a complete claim): frames panics on one
  self-churning cluster at scene start (3/9 twice), on-grid chunk targets crash on the
  same scene (2/3 twice; checker: chunks 96, 512), and single-call batch crashes 7/12
  at protocol (bc0f) — grid alignment protects neither, and neither does one call per
  process (20261017-1018-taleb-01e7, bc0f). What survives of it: the batch
  interior-tick channel is real and grid-shaped, and the zero-churn class (wave) is
  safe in every driver.
- **"Crash dose grows with internal velocity spread"** (01e7's own pre-registered P6,
  inverted by measurement): slow dense gas (spread 2) crashes at scene start; fast gas
  (spread 8–16) mostly disperses first. The dose axis is sustained overlap, not spread
  magnitude — but the dispersed phase is *not* safe: it crashes late and
  window-dependently (vmax-16 3/6, vmax-8 2/6 in bc0f's window; 4/22 and 4/18 pooled),
  and 01e7's "rare, not never" is dead as a window-independent statement (bc0f).
- **"rb separates crashing from safe arms"** (01e7, as a draw- or band-level rule):
  n480-at-vmax-2 survives 5/6 at rb 123–180, above the n240 crash band 57–95; crashers
  never print an rb at all (bc0f; the checker's n480 0/3 first showed it).
- "Maybe frames mode's continuous publication is structurally protected by the ahead
  cap / the grid" (5d87; b966's alternative): refuted — panics with gaps 16–64 against
  a 150-chronon ahead lead; survival tracks rollback pressure (b966, checker2, 01e7).
- "The latch level grows with the conflict wave / scene size" (e704): E is a per-run
  draw, flat in N (9b46); in every churn-class survivor E = 2^rb exactly (01e7, bc0f).
- "The latch cap costs 2.3–3.6× wasted ops and a DNF-tailed wall" as a controller
  property (3da3): inverted draw-for-draw (9b46).
- "The one-region end state is the collapse's cost" (e704/3da3): churn magnitude is a
  draw; the collapsed state is never the slow one (9b46).
- "The rollback response is a controller": half — AIMD restores, escalation only
  doubles (217f). "Rollbacks cascade": self-quenching at the derived bound (217f).
- "The 10-line decay mirror restores the equilibrium": livelocks at scale (e704).
- "Per-region escalation fixes the wrong locality": ES_LOCAL wedges more (e704).
- "The margin drives the collapse": capped margins still coalesce; the end state flips
  with the seed (3da3, 9b46).

## Open directions

1. **The engine-side publish/rollback boundary — confirmed necessary at protocol
   strength** (upgraded by 01e7, bc0f): refuse an advance whose rollback would cross a
   published tick, or hold publication until the wave quenches (specified by 9b46;
   reachability now quadruple-confirmed: b966 + 01e7 at scene start, bc0f through
   on-grid chunks, single-call batch on and off grid, and the late quiet-phase reclash
   of dispersed/crossed classes). Until it lands, `min_region` is the named exposure
   knob (it deletes splits, a capability, not the defect).
2. Window/stride granularity as the race margin (01e7's lead): window 32 survived
   rb 79–114 at 9/9 pooled draws across three windows where window 16 crashed at
   rb ≥ 57; the margin `fin_hi − s0` scales with the grid. More draws per arm before
   it is a verdict.
3. Open the quiet stall: the no-conflict many-region regime is the family's cost
   floor (< 0.6 chronons/s at 28k, 1.7 at 14k); merge/avoid churn vs per-unit floor
   (9b46, untested).
4. Seed/load protocol for every allocator verdict (exercised by bc0f): ≥ 3 seeds
   and ≥ 2 replicates, sweep the load axis (rate × n) before calling anything
   reachable or safe; incidence lives in bands and is window-fat-tailed — invisible at
   endpoints and in single windows (9b46, b966, 01e7, bc0f: vmax-16 0/6 in the
   checker's window, 3/6 in bc0f's).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — the
   churn class here is synthetic Bounce gas; a stirred belt or a battle is sustained
   overlap by construction (e704; 9b46; 01e7's exposure note).
6. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).
7. **Timing analysis of the race** (bc0f's closing note): the late quiet-phase crashes
   (few conflicts, publication far along) and the seed-skewed batch propensity suggest
   the race is between conflict *discovery latency* and *publication cadence*; making
   incidence a prediction instead of a sampled draw would turn the fix's test into a
   certificate. **[20261017-1447-dynamics-fd35 answers the state side: the armed
   margin IS the prediction quantity (equality law + negative certificate above); the
   named experiment left is one firing reproduction on the integrator's selfchurn
   harness to time the armed lead before a fire.]**

## Contradictions

- None open: the b966/5d87 records are reconciled as two scene classes of one exposure
  (sustained-overlap churn vs planned/no churn; 01e7), with bc0f adding that the
  dispersed/crossed classes reach the same assert late and window-dependently. 3da3's
  "unbounded latch is not a reachable ruin" against its checker's 28,160 draw: both
  basin draws (9b46). The tax battery's one-region-at-~10-chronons/s collapse vs
  9b46's wave family: different batteries, opposite cost owners; the churn and the
  many-regime floor are the battery-independent suspects. fd35's 0/45 arm-processes against
  01e7/bc0f's 7/12 is a scene-class gap (reconstructed churn classes here, their
  selfchurn harness there), not a conflict: the equality law and the armed episode are
  the same boundary both sides of that gap describe.

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0739-taleb-9b46 (awaiting grade): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (awaiting grade): the finality crash reaches the frame
- 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (awaiting grade): the crash is a
- 20261017-0428-taleb-3da3 (silver): ES_CAP killed — the latch is convexity
- 20261017-0739-taleb-9b46 (silver): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (silver): the finality crash reaches the frame harness
- 20261017-1018-taleb-01e7 (awaiting grade): conflict resolved — crash is engine-side,
- 20261017-1018-taleb-01e7 (silver): conflict resolved — crash is engine-side,
- 20261017-1149-second-20261017-1018-taleb-01e7-bc0f (this run, awaiting grade):
- 20261017-1447-dynamics-fd35 (this run, awaiting grade): the race as state — equality
