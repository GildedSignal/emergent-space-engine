# Dossier — 20261018-1717-second-20261018-1617-taleb-2403-99da (second author on 2403)

## Claim

The 2403 claim now holds on a record that regenerates and whose predictions match the log:
the burn mint stream is **bit-identical in count and census from K = 10⁵ to K = 6.5×10⁵**
(coast 145 and burn 2,069 entries, census equal to the last line — 81% of the log-distance
to the 10⁶ target), the same-convention multiplier is **16.8× at both K**, and the 10⁶ wall
under continuous level-8 burn is **≈ 43 game-s ≈ 0.4 wall-s at rtf 100** — measured law to
6.5×10⁵, one 1.54× extrapolation on a per-body law measured at three scales (2,338 B).

## Bottleneck

The same as 2403's (memory at 10⁹ / the nladder pin). What this run adds: the checkers'
named gap — "fly the 10⁶ burn arm … slice it" — is flown as the largest slice the window's
2 GB process cap admits, and the prediction letter is fixed (2403's silver was a record
defect, not a physics defect). What it deletes: the last doubt that the fence-sizing rate
carries to (almost) the fix's own 10⁶ target, and any reading of 2403's "all six held"
headline as literal.

## Evidence

Instrument: 2403's `work/patch.diff` unchanged (print-only `ES_MINT` probe + the Linux
footprint shim), rebuilt from source in this run's own target dir. Digest-neutrality
control: `20a45aa4…` probe off and on, 385 MINT lines. Cross-check: my from-source build
reproduces the second checker's published 10⁵ coast flight — 193 MINT lines, held 1, and the
deterministic content identical (game 1898.5 s, kicks 3624, events 11115, boundaries 3499);
footprints 237–238/244 MB, p99 5.1 ms.

All ladder arms `nladder <K> <mode> 15 100 <budget ms>` (15 wall-s, rtf 100; the 10⁵ pair
flown under the identical harness as the slice). Load 1.3–2.0 on the shared 8-vCPU box
during the flights (uptime recorded in the shell log); Linux/x86, orders of magnitude only.
`out/analysis2.json` holds every number; `python3 analyze2.py` regenerates it.

| arm | entries (after 150 game-s cut) | census t/L/0 | λ entries | λ distinct | held max (probe / engine) | foot build→end MB |
|---|---|---|---|---|---|---|
| 10⁵ coast 12 ms | 145 (131) | 66/1/64 | 0.0972 | 0.0497 | 1 / 1 | 237→244 |
| 10⁵ burn 12 ms | 2,069 (1,722) | 1125/0/597 | 1.278 | 0.835 | 197 / 184 | 237→264 |
| **6.5×10⁵ coast 12 ms** | **145 (131)** | **66/1/64** | **0.0972** | **0.0497** | 1 / 1 | 1,523→1,529 |
| **6.5×10⁵ burn 12 ms** | **2,069 (1,722)** | **1125/0/597** | **1.278** | **0.835** | 206 / 194 | 1,522→1,549 |
| 6.5×10⁵ burn 24 ms | 2,071 (1,726) | 1129/0/597 | 1.281 | 0.838 | **31 / 0** | 1,522→1,548 |
| 6.5×10⁵ burn 5 ms | 2,063 (1,697) | 1114/0/583 | 1.336 | 0.877 | 707 / 702 | 1,522→1,559 |
| 10⁵ burn 24 ms | 2,071 (1,726) | 1129/0/597 | 1.281 | 0.838 | 31 / 0 | 237→263 |

- **Arrivals are K-flat to the digit across a 6.5× step**: every count, census and λ equal
  (game-s window 1,347.7 both K). Stronger than the ratio carrying: it is the same stream,
  as the census mechanism (class t — the player's event clock) predicts, because the event
  clock never reads K.
- **Multiplier, second checker's convention (distinct/distinct, both sides after the cut,
  same harness): 16.8× at 10⁵ and 16.8× at 6.5×10⁵** (entries convention 13.15×).
- **The budget pair at K_max**: 12 ms → probe peak 206; 24 ms → 31; 5 ms → 707, player
  alive, 5 frames over. The 31 at 24 ms is the push-time peak, identical at 10⁵ and 6.5×10⁵
  (and equal to 2403's 10⁴ probe peak, per its second checker): per-answer service still
  fits one answer per frame at this K — the crossover to K-bound service, where the
  (K+38)·224 B walk (~224 MB ≈ a 12 ms frame at 10⁶) no longer fits, sits near 10⁶, which
  the slice brackets from below.
- **Convexity at K_max**: burn raises engine p99 5.29 → 10.85 ms while minting 16.8× —
  arrivals up and service tighter in the same frames, now at 6.5×10⁵ bodies.
- **The 10⁶ wall, measured to the slice and derived the last 1.54×**: b_per_body = 2,338 B
  (2,349 at 10⁵, 2,465 at 10⁴) ⇒ a 10⁶ build is 2.34 GB — over this window's 2 GB cap, so
  the slice is forced by a measured law, not chosen. Wall = 8 GB ÷ (λ_distinct 0.835 ×
  (10⁶+38) × 224 B) = **42.8 game-s** (2403's inference from the 10⁴ arm: ≈ 51; same
  order, now anchored 6.5× closer).
- Peak process memory at the slice: VmHWM 1.61 GB (monitored during the coast flight) —
  inside the cap with margin; no truncation in any arm.

Commands (from the repo root, patch applied; each ≤ 60 s):
```
ES_MINT=1 /home/glmlab/lab-target-99da/release/examples/nladder 650000 burn  15 100 12   # the decisive arm
ES_MINT=1 /home/glmlab/lab-target-99da/release/examples/nladder 650000 coast 15 100 12
ES_MINT=1 /home/glmlab/lab-target-99da/release/examples/nladder 650000 burn  15 100 24
ES_MINT=1 /home/glmlab/lab-target-99da/release/examples/nladder 650000 burn  15 100 5
bash lab/results/20261018-1717-second-20261018-1617-taleb-2403-99da/regen.sh   # everything, from a clean tree
```

## Predictions

`predictions.md` was written before the decisive 6.5×10⁵ flights (the 10⁵ arms are
calibration in already-published territory, and say so). Outcomes, as the log reads:

- **P1 held exactly**: coast entries identical (145 = 145, inside [0.85×, 1.15×]); census
  class t = 66/67 = 98.5% ≥ 80%.
- **P2 held**: multiplier 16.8 ∈ [6, 40]; kill (< 2) never approached.
- **P3 failed as written**: probe held at 12 ms measured 206 against a lower band of 400
  (the "≥ my 10⁵ value" clause held: 206 ≥ 197). Held does **not** grow with K at a fixed
  12 ms budget in this range — the backlog is slack-shaped, not K-shaped, until per-answer
  service stops fitting a frame; the K-scaling shows at 10⁶'s walk, not yet here.
- **P4 held**: 31 ≤ 0.25 × 206 (0.15).
- **P5 held**: b_per_body 2,338 ∈ [2200, 2500]; 10⁶ build 2.34 GB > 2 GB cap.
- **P6 held**: burn drift +27 MB ∈ [+15, +250] and > coast's +6 MB.
- **P7 (derived) held**: 42.8 game-s ∈ [15, 150].

One arm flown after the predictions (disclosed): the 10⁵ burn-24 ms flight, to pin the
drain crossover; it matched the 6.5×10⁵ arm's probe peak (31) — no band was written for it.

**Regeneration (both passes on record).** `regen.sh` ran end-to-end from a clean tree:
exit 0, 5 m 38 s warm (`regen.log`). Every deterministic number reproduced bit-identically
— entries and census at all four K_max arms, λ_distinct 0.835, multiplier 16.8, b_per_body
2,338, footprints, and the 24 ms (held 31) and 5 ms (held 707/702) corners exactly. The
12 ms held values are load-elastic across passes (206→236 at K_max, 197→301 at 10⁵, load
1.3→2.0): the marginal-budget arm is the only elastic one, which sharpens both 2403
checkers' caution — the corners and the arrival stream are the law, the middle is the
machine. In the regen pass the P3 comparative clause flips (236 < 301) while its ≥ 400
failure stands in both passes; the clause is not load-invariant and is not counted as held.

**Correction of the 2403 record** (the second checker's bar to gold): 2403's predictions
P1 ("λ ≈ 0.05–0.15 /game-s in every arm" outside burn windows) and P6 ("peak footprint
grows ≥ 100 MB over coast") are **not held as written** — its own tables measure 0.0027
(L8 coast phase) and 0.431 (L12 coast phase), and +21 MB; its "all six held" headline was
wrong on those two clauses. This run's headline counts them failed, and its own P3 failure
above is reported the same way.

## What would make it wrong

The last 1.54× to 10⁶ is extrapolation on two laws measured only to 6.5×10⁵: the per-body
build law (2,338 B, three scales, tight) and the arrival stream's K-independence (bit
count identity over a 6.5× step; the census says the clock never reads K, but a 10⁶ flight
could still change frame pacing enough to shift λ per game-s — λ is cadence-scoped, as both
2403 checkers warned; the ratio and census are the invariants). The wall arithmetic also
inherits acf2's (K+38)·224 B byte law, not re-measured here. Adoption cost: none in code —
same as 2403, one requirement line on the unwritten answer-or-expire fix: **the fence and
its expiry cadence are sized for the burning wildcard (≳ 0.8 distinct answers/game-s
continuous, ~5.9 in-window on the paced loop), never for the 0.05 coast constant.**

Fit with PRINCIPLES: 5, "The player is the only wildcard" — his throttle hand mints the
same stream at every K, so the fence cannot be sized off any population statistic; 12 —
at K_max the burn is still both the arrival spike and the p99 event in the same frames;
14 — a scan per re-timed kick during a burn is work arriving 13–17× faster than designed.

## The lens

Second-author lens: complete the named experiment, fix the record's letter, change nothing
else. What it may have missed: it prizes the record over mechanism, and two small
mechanism findings sit unpursued — the exact source of the cadence-shaped 31 (push-time
pile within a frame), and whether λ_distinct's harness dependence (0.835 here vs 2403's
0.728 at 20 wall-s) is purely frame pacing or partly the burn's dilation of the player's
event clock; a dedicated run could separate them. Operational lesson paid for and recorded:
shared `lab-target-*` dirs are mutated mid-window by other runs (a foreign `probe f=`
binary replaced `lab-target-2`'s nladder between two of my invocations) — flights and
regen must build and run from a target dir the run owns, which `regen.sh` now does.

Wall time: 0.05 seconds
