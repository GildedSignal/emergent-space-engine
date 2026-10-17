topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-1018-taleb-01e7

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The finality-assert conflict is resolved: the crash is an engine-side publish/rollback
boundary defect exposed by sustained spatial overlap, and the separator between the
disputed records is rollback pressure (conflict discovery rate) in the swept band, not
driver, grid, or bulk geometry.** Frames mode crashes on a scene with **no bulk approach
at all** — one dense slow gas cluster (selfchurn, internal spread 2 units/chronon,
`min_region 1`) — 3/9 author draws and 4/9 regen draws (a wall-clock race) at the
keeping-up rate, with panics at **chronon 32–96**: the first ~0.2 s of a loaded scene
(20261017-1018-taleb-01e7). **On-grid chunked batch targets crash too** (2/3 at chunk
128 = 8×window; checker: chunk 96 and 512 crash, and single-call batch to an **on-grid**
horizon crashes — panic values per seed stable at 32→48, reachability itself a race), so
the driver rule (grid-aligned `run_to` targets, one call per process) does not close the
churn class — the engine-side fix (refuse an advance whose rollback would cross a
published tick, or hold publication; 9b46's open direction 1) is the confirmed
requirement. The no-churn record is real and reconciled: zero-spread Pass slabs (a
planned merge) and crossing pairs never crashed (0/13 regen draws), and fast-dispersing
gas crashed once in 16 pooled draws (regen vmax-16 s11, 1104→1184) — rare, not never —
5d87's 18/18 was this class. Crashing draws sit at rb ≈ 57–95 at n = 240, with
escalation 2^rb (2⁵⁷ observed — the page's unbounded ratchet in the same regime); the
checker's held-out n = 480 vmax-2 arm survived 3/3 at rb 144–166, so rb is an in-band
correlate, not a lone separator (incidence also rides the load band); `min_region 32`
takes rb to exactly 0 (the dense slow gas never splits) and never crashes — the knob
deletes the conflicts, not the defect. Window 32 kept rb 79–114 and survived 6/6
(author 3 + checker 3): the coarser stride/grid widens the race margin (`fin_hi − s0`
must cross 32, not 16) — a lead, not a verdict. Observed panic gaps run 1–10 windows
(16–160), on the grid, in every driver; both races are wall-clock draws — the same seed
and arm survive one window and crash the next (the author's single-call batch draw
survived; 4/4 checker/regen draws of the same arm crashed)
(20261017-1018-taleb-01e7; frames reachability first shown by
20261017-0839-dynamics-b966, 14/35 across five windows, checker-confirmed).

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
  self-churning cluster at scene start (3/9), and on-grid chunk targets crash on the
  same scene (2/3) — grid alignment protects neither (20261017-1018-taleb-01e7). What
  survives of it: the batch interior-tick channel is real and grid-shaped, and the
  no-churn classes are safe in both drivers.
- **"Crash dose grows with internal velocity spread"** (01e7's own pre-registered P6,
  inverted by measurement): slow dense gas (spread 2) crashes at scene start; fast gas
  (spread 16) mostly disperses and goes quiet (rb ≤ 2 on survivors; 1 crash in 11 pooled
  draws — rare, not never). The dose axis is sustained overlap, not spread magnitude
  (20261017-1018-taleb-01e7).
- "Maybe frames mode's continuous publication is structurally protected by the ahead
  cap / the grid" (5d87; b966's alternative): refuted — panics with gaps 16–64 against
  a 150-chronon ahead lead; survival tracks rollback pressure (b966, checker2, 01e7).
- "The latch level grows with the conflict wave / scene size" (e704): E is a per-run
  draw, flat in N (9b46); in the churn regime E = 2^rb exactly (01e7).
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

1. **The engine-side publish/rollback boundary — now confirmed necessary** (upgraded by
   01e7): refuse an advance whose rollback would cross a published tick, or hold
   publication until the wave quenches (specified by 9b46, reachability triple-confirmed
   by b966 + 01e7 at scene start, through on-grid chunks). Until it lands, `min_region`
   is the named exposure knob (it deletes splits, a capability, not the defect).
2. **Window/stride granularity as the race margin** (01e7's lead): window 32 survived
   rb 79–114 (6/6) where window 16 crashed at rb ≥ 57; the margin `fin_hi − s0` scales
   with the grid. More draws per arm before it is a verdict.
3. **Open the quiet stall**: the no-conflict many-region regime is the family's cost
   floor (< 0.6 chronons/s at 28k, 1.7 at 14k); merge/avoid churn vs per-unit floor
   (9b46, untested).
4. **Seed/load protocol for every allocator verdict**: ≥ 3 seeds and ≥ 2 replicates,
   sweep the load axis (rate × n) before calling anything reachable or safe; incidence
   lives in bands, invisible at endpoints (9b46, b966, 01e7).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — the
   churn class here is synthetic Bounce gas; a stirred belt or a battle is sustained
   overlap by construction (e704; 9b46; 01e7's exposure note).
6. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).

## Contradictions

- None open: the b966/5d87 records are reconciled as two scene classes of one exposure
  (sustained-overlap churn vs planned/no churn; rb the in-band correlate; 01e7). 3da3's
  "unbounded latch is not a reachable ruin" against its checker's 28,160 draw: both
  basin draws (9b46). The tax battery's
  one-region-at-~10-chronons/s collapse vs 9b46's wave family: different batteries,
  opposite cost owners; the churn and the many-regime floor are the battery-independent
  suspects.

## Runs
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (silver): ES_CAP killed — the latch is convexity
- 20261017-0739-taleb-9b46 (silver): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (silver): the finality crash reaches the frame harness
- 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (awaiting grade): the crash is a
- 20261017-1018-taleb-01e7 (awaiting grade): conflict resolved — crash is engine-side,
  exposed by sustained overlap, at scene start, through on-grid chunks; separator = rb.
