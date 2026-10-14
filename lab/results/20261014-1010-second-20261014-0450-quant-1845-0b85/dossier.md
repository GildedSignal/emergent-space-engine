# Dossier: the warm start is built, exact and cheap — the kick's rebought crash-tick search falls 38–44% for zero fallbacks, and the shipped digests never move

## Claim

The checker's named experiment, done on the shipped record: carrying the retired tube's
`(after, found)` impact memo into the new binding's crash-tick search (a gallop from the old
tick — one reading for the side, doubling steps to a sign change, bisect the bounded span,
fallback to the cold bracket on an edge hit; `ES_IMP_WARM`, off = the shipped search verbatim)
cuts the fired kick **257.7 → 147.9 µs (−43%)** at m4000/s3, **252.2 → 155.5 (−38%)** at
m1500/s3 and **244.6 → 136.2 (−44%)** at flying pace (m400/s3, rtf 100, where the search was
the largest share), with **zero fallbacks in 3,928 warm searches** (1032 + 95 + 2801), digests
**bit-identical** to warm-off and to the shipped engine at every arm — including the published
record's own (`2e97e580` m4000/s3, `7b33d0b8` m1500/s3, `4df28df6` at 16,000 members). The
prior run's record reproduces exactly at its base (its patch on a clean 8498d1c8 build: kick
241.7 µs, K_IMP 2064, digest `2e97e580`), and HEAD reproduces the base canonically — the term
the prior run measured is real, live at HEAD, and now deleted by measurement, not by price.

## Bottleneck

Board live question 3 (the kick: 75–160 µs against a ~50 ns floor; "the cheapest exact kick on
the shipped representation"). This deletes the search's ~25 readouts to ~7 (flying arm:
K_PING 86,028 → 21,785 at near-equal search counts, −75%) and the search's 118–137 µs to
~13–35 µs per call (K_IMP µs/call), without touching the readout itself. PRINCIPLES #3:
"Nothing is evolved that can be derived when looked at" — the retired tube already held the
crash tick; #1: delete before optimizing.

## Evidence

Instrument: the prior run's prof sub-stages, extended with three counters (K_PING: `inside`
evaluations — exactly a search's readouts; K_WARM; K_FB) plus the gallop in `step.rs`
(`next_impact_from`; `rebind` captures the retired memo's tick, same doll only). Reproduce:
`regen.sh` (~10 min, five cold builds — **no shared target cache**, see the lens). Every arm:
`xtask universe --bench --seed S --rtf R --seconds 8 --members M`, `ES_MEMBERS=1000000`, A/B by
`ES_IMP_WARM` on one binary.

| arm (rtf, 8 game-s) | fired kick off→on | K_IMP µs/call off→on | warm/fallbacks | replan off→on | digest (= shipped?) |
|---|---|---|---|---|---|
| m4000/s3 | 257.7 → **147.9** (−43%) | 118.2 → 65.3 | 1032 / **0** | 100.1 → 96.2 | `2e97e580` = clamp-only shipped = the record's |
| m1500/s3 | 252.2 → **155.5** (−38%) | 114.9 → 65.7 | 95 / **0** | 94.7 → 94.0 | `7b33d0b8` = clamp-only shipped = be78's |
| m400/s3, rtf 100 | 244.6 → **136.2** (−44%) | 137.1 → 34.4 | 2801 / **0** | 149.1 → 201.0* | `94ff015b` (off = on) |
| m4000/s7, held-out | no fired kicks (overflow) | 118.7 → 118.9 | 0 / 0 | 94.8 → 95.0 | `d539b8b6` (off = on) |
| m16000/s3 | no fired kicks (overflow) | 112.1 → 111.8 | 0 / 0 | 128.6 → 128.2 | `4df28df6` = the prior checker's 16k |

- The warm kick search prices at **~13 µs** (m4000 on-arm arithmetic: 2064 calls at 65.3 mean =
  1032 cold hand-out searches at ~118 + 1032 warm at ~13), ~9× under the cold search; readouts
  per warm search ≈ 7 (flying: 86,028 → 21,785 pings at 2930→3084 searches).
- **The hand-out half is untouched and unchanged** (a leaver has no retired tube): replan 94–100
  µs at the battle arms, K_IMP ~118 µs cold within it — the honest surviving half of the prior
  run's price. *The flying replan's 149 → 201 µs is wall variance at a 0.08 s arm (372 leavers
  and the digest identical); disclosed, not explained.
- **Identity chain**: patched plain (prof off, warm ON) = clamp-only shipped at m4000
  (`2e97e580`) and m1500 (`7b33d0b8`); = pristine HEAD at m400 (`db05a069`); prior-patch on
  clean base = this patch on HEAD at m4000 (`2e97e580`). Kick/hand-out counts at the battle
  arms are wall-draw-dependent (469 vs 1032 kick items across draws, digest invariant) — the
  known class (be78's finding); all comparisons above are within-draw or digest-level.
- 16,000 members and held-out seed 7: the overflow regime has no fired kicks (the prior
  checker's own finding, reproduced); the warm start correctly does nothing there.

## Predictions

`predictions.md` (three passes, each written before its arms). P1–P8 (the original set):
identity held everywhere it was testable; P2 (≤ 8 readouts) held at ≈ 7; P6 (hand-outs ±10%)
held at the battle arms. P9–P11 were written against a broken patch (see the lens) and were
refuted by the clamp-only control — kept in the file as the record of the correction. P12
(HEAD has the term; digest `2e97e580`) **held**; P13 (fallbacks < 25%, kick ≤ 180 µs, readouts
≤ 8, hand-outs unchanged) **held in full** — fallbacks measured zero.

## What would make it wrong

The gallop is exact only under the same monotone-fall assumption the shipped bisection leans on
(a sign change inside the fall bracket is the unique boundary); the digest identity is the
empirical check and it held at every arm including cross-build — but a scene with a
non-monotone radius inside one fall branch would break both searches alike, and only the
shipped one is battle-tested. Not tested: the player's clock kicks (P_KICK_CLOCK, a different
path), non-battle scenes, threads > 1. The m4000 kick-count wall-draw (469 vs 1032 items)
means per-arm µs carry that draw's mix; the −43% is the like-for-like within-draw figure.

## Cost of adopting

One bracket protocol in `next_impact_from` plus carrying the retired `impact` tick across
`rebind` (the field already exists; ~40 lines, no schema change, no law change). Digest-
identical by construction and by measurement. What it deletes: ~25 readouts per fired kick →
~7; what it does not: the hand-out's first search (no warm source — that lever belongs to the
hand-out, not the kick).

## The lens

The second-author lens nearly produced a false refutation **twice**, and both traps are now
named for the lab. (1) The shared warm target cache: `git archive` stamps sources with the
commit's mtime, so `cp -a lab-target-3` into a snapshot lets cargo skip the rebuild and link
another tree's objects — my first "base 8498d1c8 build" ran HEAD's frame and HEAD's digest
(reproduced live; the prior window's regen workflow carries exactly this hazard, though its
record proved clean). (2) My own kick-tail repair dropped `self.rebind(next, t, d)?;`: the
broken patch passed every within-family control (off = on digests, plain = pristine at m400,
base = HEAD) and briefly "showed" the term dead at HEAD — killed only by the **clamp-only
shipped reference** at the same scenes. Lesson, generalising the 5 October taste entry:
within-patch A/B identity cannot catch a patch that changed the engine; every identity claim
needs a shipped-code reference digest at the same scene, and cold builds. `regen.sh` builds
both controls in.

