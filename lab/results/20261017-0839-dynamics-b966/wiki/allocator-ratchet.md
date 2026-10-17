topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-0839-dynamics-b966

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The crash is in the frame harness, and its incidence is a window draw, not a constant:
the shipped finality assert (`alloc.rs:1451`) fires in `run_frames` itself — 14/35 draws
at n = 120, rate 600 across five windows (author 10/14; windows swing 0/5–3/6; the second
checker's fresh window 3/6; the rate the engine exactly keeps up with: surviving draws
show present/s 599.2 of 600, 0 deadline misses) and 2/9 behind present at n = 240 (1/3
in each fresh window) — rare, not never, with slack (rate 300: 3/22 across windows — two
uncounted panics labelled r300a/r300b sit in the author's own out/, and the second
checker's window crashed 1/6 at that arm, region 328, 608→624), and forced by chunked
batch (12/12 across four sessions; gaps 16–75). The keeping-up band is an incidence
gradient, not a wall.**
(20261017-0839-dynamics-b966, dynamics lens; new public-API instrument
`crates/allocator/examples/finframe.rs`, scene `drift` = two loose gas clusters closing
at Q/8 + two quiet islands, `min_region: 1`, margin 0.5, 3 P + 4 E; patch = that one
example file, no engine edit). Mechanism, from the panic values: `certify`'s clash start
is the **stride start** of the second-completing lineage's truth (below the stride's
end), so frontier-published finality needs to lead it by only 1–4 strides (observed
`fin_hi − s0` = 16–48 in frames, up to 75 chunked) for the assert to fire; chunk
boundaries force that lead on every region at once, frames mode races it against
`present` continuously, and the firing conflicts are split-sibling clashes near chronon
~600 (the cluster approach itself is planned: 76 merges, 0 conflicts) — 9b46's trigger
class "any conflict found after a publication", now confirmed in the frame-thread loop
built as the player's path (no player binary wires it yet).

**Prior standing (9b46 and its checkers, unchanged).** The wave response is Extremistan,
one finality assert is reachable through chunked batch advance (2/2 + 2/2 at 864 bodies,
1/1 on quiet 14k), and the no-conflict regime is the cost floor: at one frozen scene and
N = 27,936 the seed flips the end-state *class* (s7 → 1 region, s1 → ~2,400, s2 →
~2,500–4,700, checker's held-out s3 → 1,389; classes stable across two windows), while
nothing else is seed-fixed: the latch (E = 64–512, 64↔128 within one seed across draws),
the region count inside a class (s2: 4,715 vs 2,489 at identical args+seed) and the wall
(identical-config replicates spread 1.65× author / 2.4× checker) are per-run draws. The
quiet control (no wave, E = 1, 0 rollbacks in chunk 1) stalls below 0.6 timeline
chronons/s at 28k and manages 150 chronons in 88 s at 14k. No quantity follows its
attributed knob (E is drawn, not an N-law); the cap verdict inverts across draws; the
collapsed state is never the slow one; publication cadence is itself a path knob (chunk
250 at 28k seed 1: same digest, 4 rollbacks all in chunk 1). Every pre-registered
prediction except "digests equal" failed (`predictions.md`) — the failures are the
finding. Before that (3da3, e704, 217f): the rollback controller has no restoring force
(`escalation *= 2` never decays); conflicts self-quench at the derived bound; the latch
level is 2^(rollbacks); the decay/local mirrors livelock; outcome digests are
bit-identical across arms, caps, margins and replicates wherever arms finish.

## Refuted

- **"Maybe the crash needs chunked `run_to`; frames mode's continuous publication could
  be structurally protected by the ahead cap"** (this page's open direction 2, and this
  run's own pre-registered alternative): refuted — `run_frames` crashes on a large
  fraction of draws at the keeping-up rate (11/19 across two windows), with race margins
  (16–64) far below the 150-chronon ahead lead; survival tracks load, not the cap
  (20261017-0839-dynamics-b966).
- **"The latch level grows with the conflict wave / scene size"** (e704's reading of
  44→14,080): within one frozen scene family E is flat in N, drawn in seed and
  replicate (20261017-0739-taleb-9b46, author + checker).
- **"The latch cap costs 2.3–3.6× wasted ops and a DNF-tailed wall" as a controller
  property** (3da3): inverted draw-for-draw at 14k in the wave family (9b46).
- **"The one-region end state is the collapse's cost"** (e704/3da3 at 14k): churn
  magnitude is a draw; only the direction holds — the collapsed state is never the slow
  one (9b46).
- **"The rollback response is a controller"**: half — AIMD restores, escalation only
  doubles (20261016-2138-dynamics-217f). **"Rollbacks cascade"**: self-quenching at the
  derived bound (217f). **"The 10-line decay mirror restores the equilibrium"**: livelocks
  at scale (e704). **"The ratchet's latch is a constant (×4) tax"**: the level is
  2^(rollbacks) (e704) and a seed draw within a scene (9b46). **"Per-region escalation
  fixes the wrong locality"**: ES_LOCAL matches the decay arm's pathology and wedges more
  (e704). **"The margin drives the collapse"**: capped margins still coalesce on the tax
  battery (3da3); the end state flips with the seed at identical margin and E (9b46).


## Open directions

1. **Decide the publish/rollback boundary — now the top of this page**: the crash is
   confirmed player-reachable in the frame harness at the keeping-up rate, so refusing an
   advance whose rollback would cross a published tick (or holding publication until the
   wave quenches) is an engine fix, not a batch-driver nicety (upgraded by
   20261017-0839-dynamics-b966; specified by 9b46).
2. ~~Frames mode: one `run_frames` run decides it~~ — decided: reachable (b966). What
   remains: whether `fast_finality`'s light-cone path can also publish past a clash
   start (observed crashes are frontier-finality; both paths set `fin_hi`); incidence
   on scenes whose conflicts are rarer than split-sibling churn; and the ahead cap's
   role — the second checker's same-window sweep crashed 3/6 at ahead 0.25 s but 0/3 at
   each of 0.05 s and 1.0 s, so "survival tracks load, not the cap" is one window's
   reading. n = 480 (1,920 bodies, rate 600) survived 0/2: the behind-present
   protection held one decade up.
3. **Open the quiet stall**: the no-conflict many-region regime (`min_region: 1`, 2,296
   cold cells) is the family's cost floor (< 0.6 chronons/s at 28k, 1.7 at 14k with
   46.6k promises exceeded and 0 wasted ops); merge/avoid churn vs per-unit floor
   (9b46, untested).
4. **Seed/load protocol for every allocator verdict**: ≥ 3 seeds and ≥ 2 identical-config
   replicates before any wall or counter is a verdict (9b46); b966 adds: sweep the load
   axis (rate × n) before calling anything "reachable" or "safe" — incidence lived in the
   keeping-up band, invisible at both endpoints.
5. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far is a synthetic cannon (e704; 9b46's family; b966's split-sibling
   churn included).
6. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).

## Contradictions

- 3da3's "the unbounded latch is not a reachable ruin at any size tried" against its
  checker's 28,160 draw (cap64 finished 57 s, shipped DNF 300 s): both are basin draws
  (9b46); the crash is reachable at 864 bodies via chunked advance (9b46) and in the
  frame harness at 480 bodies (b966).
- The tax battery's one-region-at-~10-chronons/s collapse vs 9b46's wave family
  (one-region draw 20.4 s, quiet stall < 0.6 chronons/s): different batteries, opposite
  cost owners — the collapse's cost is battery-specific; the churn and the many-regime
  floor are the battery-independent suspects.

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0739-taleb-9b46 (awaiting grade): Extremistan wave response — the seed flips
- 20261017-0839-dynamics-b966 (awaiting grade): the finality crash reaches the frame
  harness — incidence is the keeping-up band (11/19 at rate 600 across two windows; 0/6
  with slack; 2/12 behind present; chunked 3/3)
