topic: allocator-ratchet
status: open
closed-by:
valid-while:
updated: 20261017-0739-taleb-9b46

# The allocator's rollback feedback: a one-way ratchet on the forecast margin

## Current best

**The wave response is Extremistan, one finality assert is reachable (including on the quiet
family), and the no-conflict regime is the cost floor: at one frozen scene and N = 27,936 the
seed flips the end-state *class* (s7 → 1 region, s1 → ~2,400, s2 → ~2,500–4,700, checker's
held-out s3 → 1,389; classes stable across two windows), while **nothing else is seed-fixed**:
the latch (E = 64–512, 64↔128 within one seed across draws), the region count inside a class
(s2: 4,715 vs 2,489 at identical args+seed) and the wall (identical-config replicates spread
1.65× in the author's window, 2.4× in the checker's; the author's 9× seed spread and 1.9×
cap64 speedup both shrank or inverted in the checker's window) are per-run draws. The quiet
control (no wave, E = 1, 0 rollbacks in chunk 1) **stalls** below 0.6 timeline chronons/s at
28k (no tick-150 row in 250 s) and manages 150 chronons in 88 s at 14k
(20261017-0739-taleb-9b46, Taleb + checker; new public-API instrument
`crates/allocator/examples/ruin.rs`,
24-cell wave row at 0.5c + a quiet archipelago no body can reach, `min_region: 1`, margin 0.5,
H = 1,500, knobs tuned only at N = 864; patch = one line, the `ES_CAP` env on
`escalation *= 2`).** Measured on that family: (1) **no quantity follows its attributed
knob** — E is drawn, not an N-law (14k s1 and 28k s1 both landed 64–128 across windows; s7
256; s2 128–512; checker's s3 512 — flat in N, drawn in seed and in replicate), so
single-draw walls and counters on this battery — the page's included — are noise;
(2) **the cap verdict inverts across draws**: ES_CAP=64 at 14k reaches the same one-region
end state, same digest (`e538163e…`), 1.9× *faster* wall in the author's window (6.0 vs
11.4 s) and 1.1× *slower* in the checker's (15.0 vs 13.3 s) at 1.8–2.1× the wasted ops —
the exact opposite of 3da3's cap64 (2.3–3.6× wasted, DNF-tailed); every direction here is
a draw fact, none is a controller fact;
(3) **a reachable crash**: chunked `run_to` — publish between advances, the shipped
`Regions::advance` pattern (`xtask/src/regions.rs:35`) — panics 2/2 + 2/2 at shipped
`alloc.rs:1451` (1456 with this run's patch) on the 864-body conflict scene ("rollback …
would revise its published tick"; a worker cascades at the poisoned lock, `alloc.rs:1776`
patched), **and (checker) 1/1 on the quiet 14k family itself** (cannon = 1, chunk 150: a
gas-drift conflict discovered after the first publication rolls back below it) — the
trigger is any conflict found after a publication, not the cannon wave; at chunk 500 the
14k/28k wave scenes survive (their conflicts all land inside chunk 1) — reachable,
phase-dependent, digest-neutral when it survives; (4) **the cost is churn, not the
one-region state**: the author's s2 draw pays 47k broken promises, 207k wasted ops for its
160.5 s wall while the one-region draw (s7) finishes in ~20 s — but the checker's s3
(1,389 regions, E = 512) also finishes in 21.3 s, so churn *magnitude* is a draw too; the
stable reading is that the collapsed state is never the slow one;
(5) the **quiet scene is the family's cost floor**: at 28k no tick-150 row in 250 s (2/2
windows), at 14k 150 chronons take 88 s (1.7 chronons/s, E = 1, rb = 0, 1,068 merges +
114 avoided, 46.6k promises exceeded, 0 wasted) — the page's 1,408-body "one region is the
faster one" becomes a stall at 28k; mechanism unopened (merge/avoid churn vs per-unit
floor at `min_region: 1`); (6) (checker) **publication cadence is itself a path knob**: at
28k seed 1, chunk 250 ends 1,971 regions with 4 rollbacks all inside chunk 1 (vs ~2,400
regions, 6–7 rollbacks single-call), digest identical — the certificate holds, the path
does not. Every pre-registered prediction except "digests equal" failed
(`predictions.md`) — the failures are the finding.

**Prior standing (3da3 and its checkers, unchanged below).** The rollback controller has
no restoring force, and at scale neither it nor its 10-line decay mirror is adoptable
(20261016-2138-dynamics-217f; 20261017-0238-second-…-e704, 44 → 14,080 bodies on the
`tax` battery): `escalation *= 2` is global and never decays; conflicts self-quench at the
derived bound; the latch level is 2^(rollbacks) and landed 2⁶–2⁸ from ~10³ bodies on that
battery (one world per size — the instrument's `seed` argument is dead code); the 14,080
wave ends one region at ~82 chronons/s, 28,160 at ~10; ES_CAP killed there (digests
identical, cap64 2.3–3.6× wasted ops, one 260 s DNF); the decay/local mirrors livelock in
narrow-margin regimes; shipped never wedged in the margin census (E ≈ 6×10²⁹ once,
wedge-free) but DNF'd once at 128 cells/20k horizon (1/6) and once at 28,160/horizon 1,500
where cap64 finished 57 s — both single draws, now read as basin draws, not size laws
(9b46). Outcome digests are bit-identical across arms, caps, margins and replicates
wherever arms finish — the certificate moves scheduling, never results (e704, 3da3, 9b46).

## Refuted

- **"The latch level grows with the conflict wave / scene size"** (e704's reading of
  44→14,080): within one frozen scene family E(14k s1) = E(28k s1) = 64–128 across both
  windows' draws while other seeds give 256–512 at the same N, the same seed latches
  64 in one draw and 128 in the next, and (checker) at 55,584 bodies seed 1 still
  latches 128 with rb = 7 — the level is a per-run draw, not an N-law and not even a
  seed law; the 2⁶–2⁸ "band" is where draws land, not what size buys
  (20261017-0739-taleb-9b46, author + checker).
- **"The latch cap costs 2.3–3.6× wasted ops and a DNF-tailed wall" as a controller
  property** (3da3): inverted draw-for-draw at 14k in the wave family — cap64 was 1.9×
  faster in the author's window and 1.1× slower in the checker's, same digest at 1.8–2.1×
  wasted ops; wasted ops do not predict the wall (20261017-0739-taleb-9b46, author +
  checker). All such verdicts stand as draw facts on their own batteries.
- **"The one-region end state is the collapse's cost"** (e704/3da3's reading at 14k): the
  one-region draw finishes in ~20 s while the author's 4,715-region draw took 160.5 s —
  but the checker's 1,389-region draw (E = 512) finished in 21.3 s, so churn *magnitude*
  is a draw too; what holds in both windows is only the direction: the collapsed state is
  never the slow one (20261017-0739-taleb-9b46, author + checker).
- **"The rollback response is a controller"**: half — AIMD restores, escalation only
  doubles (20261016-2138-dynamics-217f).
- **"Rollbacks cascade"**: self-quenching at the derived bound (20261016-2138-dynamics-217f).
- **"The 10-line decay mirror restores the equilibrium"**: livelocks at scale
  (20261017-0238-second-…-e704); refires conflicts by design at 44 bodies.
- **"The ratchet's latch is a constant (×4) tax"**: the level is 2^(rollbacks)
  (20261017-0238-second-…-e704) — and a seed draw within a scene (9b46).
- **"Per-region escalation fixes the wrong locality"**: ES_LOCAL matches the decay arm's
  pathology and wedges more (20261017-0238-second-…-e704).
- **"The margin drives the collapse"**: capped margins still coalesce on the tax battery
  (20261017-0428-taleb-3da3); on the wave family the end state flips with the seed at
  identical margin and E (9b46).

## Open directions

1. **Decide the publish/rollback boundary** (the crash): refuse an advance whose rollback
   would cross a published tick, or hold publication until the wave quenches — before any
   driver calls `run_to` twice on a scene with any late conflict (the checker's quiet-14k
   crash shows the cannon is not needed: loose-gas drift alone fires it). The assert
   (shipped `alloc.rs:1451`) is the certificate policing finality; today it crashes the
   engine instead of degrading (20261017-0739-taleb-9b46, author + checker).
2. **Frames mode**: publication is continuous there; if the same assert can fire, the crash
   is in play, not only in batch drivers. One `run_frames` run on the wave scene decides it
   (20261017-0739-taleb-9b46, untested).
3. **Open the quiet stall**: the no-conflict many-region regime (`min_region: 1`, 2,296
   cold cells) is the family's cost floor (< 0.6 chronons/s at 28k, 1.7 at 14k with
   46.6k promises exceeded and 0 wasted ops); merge/avoid churn vs per-unit floor. The
   battery's stagger-300 control (248–287 chronons/s at 1,408) is the same regime one
   decade down (20261017-0739-taleb-9b46, author + checker).
4. **Seed protocol for every allocator verdict**: ≥ 3 seeds and ≥ 2 identical-config
   replicates before any wall or counter is a verdict (walls spread 9×/3.4× across seeds
   and 1.65×/2.4× across identical replicates in the two windows; the taste log's
   controller verdicts were single-draw).
5. The real conflict rate of the flown universe (encounters, burns, the belt) — every
   measurement so far is a synthetic cannon (e704; 9b46's family included).
6. Margin from the law, not from history (relativistic scenes): the c-cap makes the
   conflict window one stride; no-conflict throughput ceiling unmeasured at every size
   ≥ 128 cells (e704 checkers).

## Contradictions

- 3da3's "the unbounded latch is not a reachable ruin at any size tried" against its own
  checker's 28,160 draw (cap64 finished 57 s, shipped DNF 300 s): now framed — both are
  basin draws; 9b46 shows the end state and wall flip with the seed at fixed N, and the
  crash (a sharper ruin than any wall) is reachable at 864 bodies via chunked advance.
- The tax battery's one-region-at-~10-chronons/s collapse vs 9b46's wave family (one-region
  draw 20.4 s, quiet stall < 0.6 chronons/s): different batteries, opposite cost owners —
  the collapse's cost is battery-specific, the churn and the many-regime floor are the
  battery-independent suspects.

## Runs
- 20261016-2138-dynamics-217f (silver, checked): the rollback ratchet measured — global,
- 20261016-2138-dynamics-217f (silver, checked): mechanism, quench and digest invariance
- 20261017-0238-second-20261016-2138-dynamics-217f-e704 (gold, checked): the
- 20261017-0428-taleb-3da3 (awaiting grade): ES_CAP killed — the latch is convexity: caps
- 20261017-0739-taleb-9b46 (awaiting grade): Extremistan wave response — the seed flips
  the end-state class, every counter/wall is a draw, cap verdict inverts across draws,
  reachable finality assert (also on the quiet family), quiet-regime cost floor
