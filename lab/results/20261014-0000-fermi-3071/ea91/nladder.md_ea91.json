topic: nladder
status: open
closed-by:
valid-while:
updated: 20261013-2252-dynamics-ea91

# The N ladder: 28 live bodies toward 10⁹

## Current best

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
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.

## Refuted

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.
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
3. **Event-time hysteresis on the shipped chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
   [Below-half-run rank stability is the ladder-side twin: quarter-window census, one env
   var away (20261013-2252-dynamics-ea91).]
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
   into the shipped allocator and check the p99 frame.
5. **The death channel at belt scale** (new, from 20261013-2252-dynamics-ea91): the
   54–64 % promotion death rate is the battle pocket; measure the quiet belt's promotion
   mix (death vs dormancy) before sizing retirement vs demotion. The avalanche stream
   (steady-state Fano 8–28, no lag-1 memory) is the allocator's target for burst
   absorption (PRINCIPLES #12).

## Contradictions

- None recorded yet. [Kept as a flag, not a contradiction: rule 2's "Extremistan" wording
  against the measured Zipf slope −1.6…−2.0 — the concentration supports the rank rule,
  the slope does not support infinite-variance; the certificate should be read as
  top-decile, not power-law (20261013-2252-dynamics-ea91).]

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
