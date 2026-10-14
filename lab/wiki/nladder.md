topic: nladder
status: open
closed-by:
valid-while:
<<<<<<< main
updated: 20261013-2252-dynamics-ea91
=======
updated: 20261013-2252-second-20261013-2130-library-ae3d-7497
>>>>>>> 20261013-2252-second-20261013-2130-library-ae3d-7497

# The N ladder: 28 live bodies toward 10⁹

## Current best

<<<<<<< main
**The surprise-rate distribution is measured: heavy-tailed with regime-frozen ranks, and
the churn channel is death, not quiescence (20261013-2252-dynamics-ea91).** Open
direction 1's instrumented run (env-gated per-body census in `Universe::apply`, digests
bit-identical probe on/off, flying pace rtf 100, three seeds incl. m400): across bodies,
resolved items have Gini 0.72–0.74, top-decile share 47–56 %, Zipf slope −1.6…−2.0,
busiest body ~100× the median — so a small live set can hold most of the work and rule 2's
rank premise **survives its falsifier** (in the concentration sense; the slope is steeper
than −1, finite-variance). The ranks do not thrash at the 55 s windows: among live bodies,
half-run Spearman ρ = 0.95–1.00 for natives and 0.85–0.93 for promoted ships at n ≥ 42
(at/above each scene's Poisson re-noise null); at 30 s windows promoted ρ sits at or below
the null (tune 0.55 vs 0.78; checker's seed 11: 0.79 vs 0.84), so the promoted rank needs
a long window to freeze — natives freeze at every window measured. What looked like churn
(ρ ≈ 0 including the dead, top-decile Jaccard 0.14–0.33) is **bodies exiting by
crashing**: 47–64 % of promotions die within one run window on the battle scene (54–64 %
on the author's three; 47 % on the checker's seed 11), each after a burst at birth (total
items anti-correlate with age at the 55 s scenes, ρ = −0.19…−0.52; sign-flat at the 30 s
tune scene, +0.09) — a promotion is typically one transient then
death or 1–3 items per half-run of quiescence. Consequences: (a) the promotion
certificate reads rank over the *live* census plus death as the exit channel — no
hysteresis is supported at the half-run scale; (b) standing state per promotion must be
O(compact), never the sticky 8.3 KB live record (frame-cost's ephemeral half), because
most promotions are one-burst-then-gone; (c) the allocator's measured enemy at flying
pace is the avalanche, even at steady state: Fano 8–28, top 1 % of frames carry 10–26 %
of items, zero-frames 0–86 % by scene (the avalanche needs no empty frames), lag-1
autocorr |ρ| ≤ 0.17 (no warning). Domain: the plane's
battle scene, m48–m400 (the bench clamps `--members` to [4, 400], so 428 bodies is the
shipped ceiling — the checker's m1200 request reproduced m400's digest exactly), windows
30–55 s ≈ 3,000–5,500 game-s at rtf 100 (one 16,500 game-s point at rtf 300 agrees);
not the quiet belt, not
below half-run scale; encounters are player-centric in the shipped tier so per-body
encounter churn is unmeasurable there.

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the append —
measured on shipped code (20261013-2130-library-ae3d; checker-corrected).**
=======
**Rule 2 is dead by its own falsifier, run on shipped code: the per-body kick
distribution is not heavy-tailed, so promotion is a fixed fraction (a constant
certificate), and the head is drivers already scheduled by the light cone
(20261013-2252-second-20261013-2130-library-ae3d-7497, on the probe of that run).**

Measured on four deterministic settles of the shipped `scenario::plane` (idle seeds
1/7 at 40,000 game-s, a held L12 burn at 1,000 game-s, a 4,000-member battle at 3,600
game-s; probe = `Update.kick` + opt-in `Universe::kick_log` + example `kick_tail`,
digest-neutral: the reverse-L15 flight's `e0972a1c…` identical base vs patched):
>>>>>>> 20261013-2252-second-20261013-2130-library-ae3d-7497

- **The tube bulk (planets, moon, orbiters, skimmers, the idle player) is flat per
  orbit by construction**: CV 0.17–0.20, max/median 1.4–1.5, Gini ≤ 0.12, top-1 ≤ 12%
  on every scene and seed run (1, 3, 7, 11; checker's seed 3 gives CV 0.203, seed 11
  gives 0.200); per-body numbers near-constant across scenes and seeds (Orbiter 2:
  202–223/orbit over four scenes and four seeds — ±5%, not identical) — `step_for` =
  1/2⁷ of the body's own period (`step_log2` 7, the 1/128 of 27ce), deterministic.
- **Per game-second the spread is three decades (4.8×10⁻² → 3×10⁻⁵) but it is
  structure**: rank per second = rank in 1/P_orbit plus the v2 clock's regime. The 12
  haulers take 0–2 kicks each in 40,000 game-s (quietest per second, nominally
  620–26,000/orbit: the over-provisioning of 27ce/7f97). A promotion bar at any rate
  is a period/clock-regime threshold knowable from body constants at birth.
- **The head is driver-caused, not a body property**: under a held L12 burn the
  player takes 70.6% of the scene's kicks (816 of 1,513 are sub-level ≥ 1: the
  waterfall, re-measured as a distribution); with no burn, no body is an outlier in
  the cadence sense (the idle player's 13–28% per-second share across seeds and spans is its short period — per orbit
  it is flat with the orbiters). In the 4,000-member battle the stream spreads over
  3,769 handed-out members (p50 5, mean 20.6, max 174 kicks; top member 0.07%;
  per-lived-second Gini 0.55, top-10% holding 2.3× their uniform share): dispersed but headless — no rank to promote by.
  Passage sub-kicks land on whichever members the battle hands out deep in the well
  (10/38 and 8/37 at m48 by seed, sub-kicks 14–261; 22/3,769 at m4000) — discovered by due-ness, not rankable ahead.
- Consequence for the promotion design: it points exactly where frame-cost measured
  the cost (`resolve_handout`, 486–585 µs, sticky): make promotions ephemeral; do not
  build a smarter selection rule.

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the
append — measured on shipped code (20261013-2130-library-ae3d; checker-corrected;
store rows re-regenerated by the 7497 run: 12.347 bits/member at 7 ns, storm 48.38
with graceful fallback, convoy hot max 10.9 µs vs a 1.29 ms compaction step).**

<<<<<<< main
The five rules (each with a falsifier, from Julien's library, run dossier §Evidence):
1. **Delete before you measure cheaper** (Musk's algorithm): every ladder term (per-frame
   walks, rekey, queue, memory per live body) gets a *deleted* rung before a *cheaper* rung.
2. **The live set is a rank, not a count** (Zipf/Extremistan): promote by rank in the
   measured per-body surprise-rate distribution; k is a certificate, not a constant.
   *[Measured 13 October: the premise holds in concentration (Gini 0.72–0.74, top decile
   ≈ half the work) and the ranks are regime-frozen among the living — but the Zipf slope
   is −1.6…−2.0, not Extremistan-shallow, and the exit channel is death (54–64 % of
   promotions), which a rank never sees coming; the certificate tracks death, not
   quiescence (20261013-2252-dynamics-ea91).]*
3. **Promotion judges on event time, not frame time** (sampling noise): hysteresis windows
   in the body's own event time; the 210-handoff chatter is the counterexample to fix.
   *[Measured 13 October: at the half-run scale no hysteresis is needed — live ranks sit
   at the counting-noise null (20261013-2252-dynamics-ea91); below that scale untested.]*
4. **Buy the option, not the headroom** (optionality): the O(1) hot append *is* the
   promotion; no ahead-of-demand promotion, no second promotion path. (Checker: the
   store's append is the storage-layer kick path; the plane's compact→live promotion is
   `resolve_handout`, 486–585 µs and sticky — the option to buy there is demote-at-commit
   or dormancy, per frame-cost.) *[Support at the level: the median live promotion works
   1–3 items per half-run (20261013-2252-dynamics-ea91).]*
=======
The four rules that survive, with rule 2 struck:
1. **Delete before you measure cheaper** (Musk's algorithm): every ladder term
   (per-frame walks, rekey, queue, memory per live body) gets a *deleted* rung before
   a *cheaper* rung.
2. ~~**The live set is a rank, not a count**~~ — **dead by measurement** (7497): the
   surprise distribution's bulk is flat per orbit by construction and its head is
   driver-caused; the live-set bar is a period/clock-regime constant, i.e. a fixed
   fraction. Falsify further on belt scenes (conjunction clustering), not the plane.
3. **Promotion judges on event time, not frame time** (sampling noise): hysteresis
   windows in the body's own event time; the 210-handoff chatter is the counterexample
   to fix.
4. **Buy the option, not the headroom** (optionality): no ahead-of-demand promotion;
   the promotion to make cheap is the *ephemeral* one (demote at commit, frame-cost),
   and the repack/compaction step (1.29–12.1 ms) is the scheduled spike.
>>>>>>> 20261013-2252-second-20261013-2130-library-ae3d-7497
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.

## Refuted

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.
<<<<<<< main
- "The live set chatters rank-to-rank and needs hysteresis at the half-run scale": ranks
  among live bodies are at the Poisson re-noise null; the churn is death
  (20261013-2252-dynamics-ea91).
- "Most promoted bodies go dormant (zero events in the second half)": true only of the
  dead; among live promotions 0–9 % are dormant in a half-run (the author's own first
  reading, corrected by the alive split, 20261013-2252-dynamics-ea91).

## Open directions

1. ~~**The surprise-rate distribution on shipped scenes**~~ (measured 13 October,
   20261013-2252-dynamics-ea91; see Current best — the falsifier's answer is in).
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the
   term gone; count what the per-frame walk visits that the hot tier did not touch.
=======
- **"The live set is a rank, not a count" (rule 2): dead by its own named falsifier**
  — the per-body kick distribution on four shipped plane scenes is not heavy-tailed
  (tube bulk CV 0.17–0.19 per orbit; battle top member 0.07%; the head is the burn
  driver at 70.6%) (20261013-2252-second-20261013-2130-library-ae3d-7497).

## Open directions

1. ~~The surprise-rate distribution on shipped scenes (rule 2's falsifier)~~ **done,
   rule 2 dead**; the honest revival path is the belt: a dense belt where conjunctions
   cluster on bodies could still be heavy-tailed without a driver — unmeasured.
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with
   the term gone; count what the per-frame walk visits that the hot tier did not
   touch.
>>>>>>> 20261013-2252-second-20261013-2130-library-ae3d-7497
3. **Event-time hysteresis on the shipped chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
   [Below-half-run rank stability is the ladder-side twin: quarter-window census, one env
   var away (20261013-2252-dynamics-ea91).]
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
<<<<<<< main
   into the shipped allocator and check the p99 frame.
5. **The death channel at belt scale** (new, from 20261013-2252-dynamics-ea91): the
   54–64 % promotion death rate is the battle pocket; measure the quiet belt's promotion
   mix (death vs dormancy) before sizing retirement vs demotion. The avalanche stream
   (steady-state Fano 8–28, no lag-1 memory) is the allocator's target for burst
   absorption (PRINCIPLES #12).
=======
   into the shipped allocator and check the p99 frame. **Now the primary direction**
   (rule 2's death redirects the promotion work here and to ephemeral promotion).
5. The haulers' far-field clock cadence per orbit is extrapolated from ~1 kick
   (0.03–0.3% of an orbit measured); a full-orbit measurement needs ~10⁷–10⁸ game-s
   (wall-days) — only worth it if the ladder reaches the root-doll bulk.
>>>>>>> 20261013-2252-second-20261013-2130-library-ae3d-7497

## Contradictions

- None recorded yet. [Kept as a flag, not a contradiction: rule 2's "Extremistan" wording
  against the measured Zipf slope −1.6…−2.0 — the concentration supports the rank rule,
  the slope does not support infinite-variance; the certificate should be read as
  top-decile, not power-law (20261013-2252-dynamics-ea91).]

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
