topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-0839-second-20261017-0739-taleb-9b46-5d87

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The wave response is Extremistan, the finality-assert crash is a window-grid defect of
chunked batch drivers (not a live-path hazard, not an engine defect), and the no-conflict
regime is the cost floor.** At one frozen scene and N = 27,936 the seed flips the
end-state *class* (s7 → 1 region, s1 → ~2,400, s2 → ~2,500–4,700, checker's held-out s3 →
1,389; classes stable across two windows), while **nothing else is seed-fixed**: the latch
(E = 64–512, 64↔128 within one seed across draws), the region count inside a class and the
wall (identical-config replicates spread 1.65×/2.4× across the two windows) are per-run
draws. The quiet control (no wave, E = 1, 0 rollbacks in chunk 1) **stalls** below 0.6
timeline chronons/s at 28k (no tick-150 row in 250 s) and manages 150 chronons in 88 s at
14k (20261017-0739-taleb-9b46, Taleb + checker; instrument
`crates/allocator/examples/ruin.rs`, 24-cell wave row at 0.5c + a quiet archipelago no
body can reach, `min_region: 1`, margin 0.5, H = 1,500; **the family is Newtonian**
(`World::new` defaults the law, `loose_gas` never switches it), so its finality is
global-frontier, not light-cone — 9b46's dossier text saying `Law::Relativistic` is wrong
(20261017-0839-…-5d87)). Measured on that family:

(1) **no quantity follows its attributed knob** — E is drawn, not an N-law (flat in N from
14k to 55,584 at seed 1), so single-draw walls and counters on this battery are noise;
(2) **the cap verdict inverts across draws** (ES_CAP=64: 1.9× faster in one window, 1.1×
slower in another, same digest) — no cap verdict is a controller fact; (3) **the crash is
chunk-grid-shaped and batch-only**: `run_to(target)` with target off the 16-chronon window
grid forces every stride to end mid-window (`finished()` demands `verified == target`),
publishes finality onto that interior tick, and the next call's strides re-enter the same
window and conservatively overlap the published tails → the assert at `alloc.rs:1451`
(9b46 author + checker; mechanism + probes 20261017-0839-…-5d87); **frames mode (the live
path) never crashed — 18/18 arms** (3 seeds × 3 cadences × 864–27,936 bodies × both laws,
rollbacks 0–6 per arm; quiet swept through the quiet-batch crash window (ticks 150–300)
to frontier 1,136–3,072 across the two windows' draws; relativistic to 1,536–8,096
across draws) — because frames goals (`goal_tick`'s `.ceil()`) and stride ends
(`next_unit`'s `boundary(w + stride)`) stay on the grid, so a completed truth's window
set never meets a later stride's; no on-grid
batch chunk ever crashed (96, 112, 128 at 864; 512 at 14k — every run, every window; checker2
extends: 256 at 28k survives, and in batch under `Law::Relativistic` (checker2's own
instrument fix — the run's `rel` prefix is dead in batch mode) interior 100 crashes
"from 80 … published 100" while on-grid 96/112 survive: the rule is law-independent)
while interior chunks crashed 7/11 on the second run's box (100-s1 4/4, 104 2/2, 108 1/3,
100-s2 0/2; author 2/2, checker 2/2 at 100; of the 7/11 only 3/5 are auditable in the
regen traces — the rest were the author's overwritten window — and checker2 adds 100-s1
1/1 crash, interior-200 0/1) — interior is necessary, never sufficient (the spatial hull
overlap in the shared window is a per-run draw);
(4) **the cost is churn, not the one-region state** (the collapsed state is never the
slow one; churn magnitude is a draw); (5) **the quiet scene is the family's cost floor**
(< 0.6 chronons/s at 28k, 1.7 at 14k; mechanism unopened); (6) **publication cadence is
a path knob** (batch chunk 250 vs single-call; and in frames the (rate, ahead) pair
draws end states from 49 to 798 regions at N = 864 fixed, and to 1 at 28k-s1 —
20261017-0839-…-5d87),
digest identical wherever arms finish. Every pre-registered prediction except "digests
equal" failed in 9b46 — the failures were the finding; the second run's frames
prediction died the same way, in the pre-registered no-direction.

**Prior standing (3da3 and its checkers, unchanged below).** The rollback controller has
no restoring force, and at scale neither it nor its 10-line decay mirror is adoptable
(20261016-2138-dynamics-217f; 20261017-0238-second-…-e704): `escalation *= 2` is global
and never decays; conflicts self-quench at the derived bound; ES_CAP killed on the tax
battery (digests identical, cap64 2.3–3.6× wasted ops, one 260 s DNF) — now read as a
basin draw; the decay/local mirrors livelock in narrow-margin regimes. Outcome digests
are bit-identical across arms, caps, margins and replicates wherever arms finish — the
certificate moves scheduling, never results (e704, 3da3, 9b46).

## Refuted

- **"The crash reaches the game's live path and needs an engine-side fix (refuse the
  advance / hold publication)"** (9b46's open direction 1, as an engine change): 18/18
  frames arms survive with real conflict load; the shipped channel is the forced interior
  publish of chunked `run_to`, which frames structurally cannot produce; a driver rule
  (grid-aligned targets, or one call per process) closes it (20261017-0839-…-5d87).
- **"9b46's wave/quiet family runs `Law::Relativistic`"** (its dossier text): the scenes
  are Newtonian by `World::new`'s default; their finality is global-frontier. The
  relativistic (light-cone) variant is the `rel` arms of 20261017-0839-…-5d87, which also
  never crashed (20261017-0839-…-5d87).
- **"The latch level grows with the conflict wave / scene size"** (e704): E is a per-run
  draw, flat in N to 55,584 at seed 1 (20261017-0739-taleb-9b46, author + checker).
- **"The latch cap costs 2.3–3.6× wasted ops and a DNF-tailed wall" as a controller
  property** (3da3): inverted draw-for-draw at 14k in the wave family; wasted ops do not
  predict the wall (20261017-0739-taleb-9b46).
- **"The one-region end state is the collapse's cost"** (e704/3da3): the one-region draw
  finishes fast; churn magnitude is a draw; only the direction holds (9b46).
- **"The rollback response is a controller"**: half — AIMD restores, escalation only
  doubles (20261016-2138-dynamics-217f).
- **"Rollbacks cascade"**: self-quenching at the derived bound (20261016-2138-dynamics-217f).
- **"The 10-line decay mirror restores the equilibrium"**: livelocks at scale
  (20261017-0238-second-…-e704); refires conflicts by design at 44 bodies.
- **"The ratchet's latch is a constant (×4) tax"**: the level is 2^(rollbacks) — and a
  seed draw within a scene (e704, 9b46).
- **"Per-region escalation fixes the wrong locality"**: ES_LOCAL matches the decay arm's
  pathology and wedges more (20261017-0238-second-…-e704).
- **"The margin drives the collapse"**: capped margins still coalesce on the tax battery;
  the end state flips with the seed at identical margin and E (3da3, 9b46).

## Open directions

1. **Write the driver rule down** (the crash, decided): batch `run_to` targets on the
   `cfg.window` grid (16), or one call per process — `xtask/src/regions.rs` and any
   replay/checkpoint driver. A future change to `goal_tick`'s rounding would silently
   reintroduce interior stride ends; the rule is the guard
   (20261017-0839-…-5d87). The restored-lineage channel (`rollback` → `make_region(…
   Some(fin))` inherits `fin_parts` above the replay point) never fired in 18
   continuous-publication arms but is not proven unreachable — one adversarial scene away.
2. **Open the quiet stall**: the no-conflict many-region regime (`min_region: 1`, 2,296
   cold cells) is the family's cost floor (< 0.6 chronons/s at 28k, 1.7 at 14k with
   46.6k promises exceeded and 0 wasted ops); merge/avoid churn vs per-unit floor. The
   battery's stagger-300 control (248–287 chronons/s at 1,408) is the same regime one
   decade down (9b46).
3. **Seed protocol for every allocator verdict**: ≥ 3 seeds and ≥ 2 identical-config
   replicates before any wall or counter is a verdict (walls spread 9×/3.4× across seeds
   and 1.65×/2.4× across replicates; the taste log's controller verdicts were
   single-draw). In frames mode add the (rate, ahead) pair: it draws the end state
   (20261017-0839-…-5d87).
4. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far is a synthetic cannon (e704; 9b46's family included).
5. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).

## Contradictions

- 3da3's "the unbounded latch is not a reachable ruin at any size tried" against its own
  checker's 28,160 draw (cap64 finished 57 s, shipped DNF 300 s): both are basin draws;
  9b46 shows the end state and wall flip with the seed at fixed N, and the crash (a
  sharper ruin than any wall) is reachable at 864 bodies via chunked advance — now
  grid-shaped and batch-only (5d87).
- The tax battery's one-region-at-~10-chronons/s collapse vs 9b46's wave family (one-region
  draw 20.4 s, quiet stall < 0.6 chronons/s): different batteries, opposite cost owners —
  the collapse's cost is battery-specific, the churn and the many-regime floor are the
  battery-independent suspects.

## Runs
- 20261016-2138-dynamics-217f (this run, awaiting grade): the rollback ratchet measured —
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0739-taleb-9b46 (awaiting grade): Extremistan wave response — the seed flips
- 20261017-0839-second-20261017-0739-taleb-9b46-5d87 (awaiting grade): the crash is a
  window-grid defect of chunked `run_to`; frames never crashes (18/18), no on-grid chunk
  ever crashed, interior 7/11 + 2/2 + 2/2 across windows
