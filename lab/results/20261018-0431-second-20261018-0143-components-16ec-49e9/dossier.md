# Dossier — the burn question closed: the key-range fast path is digest-neutral on thrusting populations; the shipped-harness "kill" was the decision tick, by construction

## Claim

16ec's key-range fast path is **digest-neutral on the burn arm**: with the player's decision
pinned at its own canonical tick (`Universe::schedule`, the engine's own "Ties" rule), burn
ctl = ctl-rerun = fast = fast-rerun, all four `1198b23ec9b91432` at the same cut, at 100.0%
belt skip (19,423/19,423) with all 338 player passages read out — and the never-flown
`slow_cycle` refusal branch is now flight-proven digest-neutral (5,126 refusals, 12,549 skips,
1,753 deaths, digest identical ctl vs fast). The shipped harness's burn divergence was the
harness itself — by construction (`digest()` hashes the decision log `self.inputs`,
universe.rs:1352, and `input(p.u.now)` logs whatever the load made the presented tick), and
now measured on both sides: equal logged tick → equal digest, unequal ticks → unequal
digests, pinned tick → one digest across a 48% schedule spread.
**16ec's "not adoptable on thrusting populations until the divergence is understood" is
resolved: understood, instrument, lifted.**

## Bottleneck

The board's belt stream (2 events per body per interval; the boundary half). This run is the
second-author step on 16ec (checker: gold, but checker2 died at its deadline, and the checker
named the misses): the pinned-input harness the wiki page itself names next ("a pinned-input
harness first, then the bisect if a real difference survives"), the decomposition denominator
that did not regenerate, and the refusal branch never flown. No new physics; the claim's
adoption case is what moved: the flag is now proven digest-neutral on every population flown
(coast ×2 seeds in 16ec, burn pinned here, straddle here).

## Evidence (Linux/x86, orders of magnitude; every number from `regen.sh`, author flights `a_*`, regen flights `r_*`)

**The pinned burn arm (the named experiment).** Decision scheduled at tick 365,400,000 (the
nominal frame-60 presented tick at rtf 1800 = 1,800 game-s; the presented tick can only lag
nominal, so the call is never refused), taken at exactly that tick whenever the engine
arrives (docs/law.md "Ties": "a decision takes effect at its logged canonical tick, never at
a wall-derived one"):

| arm | digest | clock total | fast skip | passage | ns/event |
|---|---|---|---|---|---|
| pin ctl A | 1198b23ec9b91432 | 19,761 | 0 | 0 | 4,483 |
| pin ctl B | **1198b23ec9b91432** | 19,761 | 0 | 0 | 4,429 |
| pin fast A | **1198b23ec9b91432** | 19,761 | **19,423 (100.0%)** | 338 read out | 9,727 refused / **214 skipped** |
| pin fast B | **1198b23ec9b91432** | 19,761 | 19,423 | 338 | 213.9 |
| (final regen r_*: all four identical, again) | 1198b23ec9b91432 | 19,761 | 19,423 | 338 | — |

The A/A pair is not merely "two runs on a quiet box": across the six pinned runs of the
author window the presented tick at frame 60 ranged over tens of millions of ticks with one
digest, and the regen windows extend the spread to **230,686,719 – 343,400,821 (+49%)** —
schedule-independence under real schedule variation. With the decision tick fixed, the
whole flight is schedule-independent, exactly as coast always was.

**The mechanism, measured on both sides.** `digest()` hashes `self.inputs` (the logged
decision ticks, universe.rs:1352); the shipped harness logs the presented tick, which the
12 ms budget makes load-dependent. Every window closes it: **equal logged tick → equal
digest** — the author window's shipped pair injected at presented 247,463,935, both
`37efae11…`, and the regen window's shipA at presented 343,400,821 → `08b6399c…`, the same
tick an earlier window digested the same way (the equal-tick half now proven across windows,
not just within one) — and **unequal ticks → unequal digests**: the regen window's shipB,
lagged by its twin's load to presented 342,397,356, digested `c3038c23…`, while the pinned
arm holds one digest across the whole presented spread. No physics channel is needed to
explain any shipped-harness burn divergence: this record holds three distinct burn digests,
every one explained by its logged tick (and 16ec's record holds four more). The
pinned digest differs from every shipped-harness digest because the burn starts at 1,800
game-s instead of a load-dependent ~1,200–1,700 — that difference is the instrument,
demonstrated.

**The straddle arm (the never-flown branch).** `ES_LEAVE_LOG2=28` (2^28 root units ≈ 2.65 AU,
inside the belt's apoapsis span): the widened range of part of the belt now straddles the
leave certificate, so the fast path must refuse and fall through to the shipped readout:

| arm | digest | total | fast | slow_cycle | deaths | ns/event |
|---|---|---|---|---|---|---|
| strad ctl | 0c3b1c7dcd0dfeeb | 17,675 | — | — | 1,753 | 4,751 |
| strad fast | **0c3b1c7dcd0dfeeb** | 17,675 | 12,549 (71%) | **5,126 refused** | **1,753** | 4,592 refused / 222 skipped |

The refusal branch fired 5,126 times in flight, the skip still fired where the range sits
inside (71%), the 1,753 belt deaths past leave are identical in both arms, and the digest is
bit-identical: the fall-through is the shipped path, provably. 16ec's P4 ("adversarial
surface/leave just inside the range disables the skip") is now flown, not asserted.

**The decomposition regenerates (the checker's second miss).** The harness now prints the
flight-window deltas of the clock-path census and `stats.boundaries` (both paths) in one line:
clock_share **0.166–0.187** across the twenty flights of the author and regen windows (author:
coast 0.181, shipped burn 0.186, pinned 0.186–0.187, straddle 0.170; regen: coast 0.176, burn
0.182, straddle 0.166) — the clock path is 17–19% of boundary mass at N = 10⁴, WH ≥ 4.3×
clock, matching the checker's ≈82% WH bound (the four heaviest flights, the pinned arms'
author window, sit at 18.6–18.7%) and retiring the author's unregenerable
10.2%/84.6%/190,000. The clock path's per-event cost is unchanged: 4.4–5.6 µs shipped,
~0.21–0.27 µs skipped (~20×), on every arm.

**Controls.** Coast ctl = coast fast = `a725217f1dcd9f2a`, 16ec's known answer to the hex
digit (my rebuilt patch changes no physics). The probe regenerates 16ec's exactly: 1,204
bindings, 1,200 cycles swept, worst excursion +0.000e0, 4 non-cycles refused. `regen.sh`
writes `r_*`, never overwriting the author's `a_*` flights (the first checker's record
lesson). Provenance note: the `r_*` files in `work/` are `regen.sh`'s own outputs from its
completed end-to-end run in the fix window (the tree restored between attempts; digests as
printed above) — a checker's rerun overwrites them wholesale. The probe has no separate
author copy (an `rm a_*` before the flight relaunch swept it); it is deterministic and lives
in `r_probe.txt`, byte-identical to 16ec's record. `flights.sh` fails loudly on a flight with no digest line
(the silent-empty-grep failure mode 16ec's checker named).

## Predictions

`predictions.md` was written before the flights (with one dated design note: `input(T)` ahead
of the presented tick synchronously pulls the player's history at ≈0.8 µs/tick — a 4.5×10⁷-tick
pull measured at ~35 s — so the pinned arm uses `schedule`, O(1), canonical). H2 held (pinned
A/A identical), H3 held (pinned burn ctl = fast, the claim), H4 held (slow_cycle 5,126 > 0,
fast 12,549 > 0, deaths equal, digest identical), H5 held (clock_share ≤ 0.19), H6 held
(coast reproduces `a725217f…`). **H1 held in full across the two windows:** the author window
showed the agreement half (equal presented ticks → equal digests), the regen window the
divergence half (unequal presented ticks → unequal digests) — the prediction was written
against the author window alone, where only the agreement half was observed and reported as
such; the regen runs, flown by `regen.sh` after the dossier's first draft, completed it.

## What would make it wrong

The pinned arm pins one decision; a real player session is a stream of decisions at
arbitrary ticks — each must go through `schedule` at its own tick (the engine's documented
rule), and a harness that logs wall-derived decision ticks will always be digest-unstable
(now proven, not assumed). The straddle arm flies a modified `leave_log2`, not the shipped
scene: it proves the branch, not the scene. The 338 passages and 5,126 refusals cover the
branches that fired; a death-by-surface inside a skipped range remains probe-covered only
(the belt never dips inside the star). `schedule` vs `input` at the same tick should be
digest-identical (both take the decision at its logged tick after the player's items up to it
are resolved); I did not fly that equivalence — if it differed, the canonical form is
`schedule`'s, per the docs.

## Cost of adopting, fit with PRINCIPLES

Nothing beyond 16ec's: one flag-gated branch in `boundary_clock` plus census; the harness
additions (`ES_INJECT_TICK`, `ES_LEAVE_LOG2`, the decomp line) are print-only instrumentation
in the example. With the burn question closed, the fast path has no known digest-divergence
case on any flown population. Fit: "Compute only surprises … Nothing is evolved that can be
derived when looked at" (3); "no work for no reason, so no ticks" (14); "the cheapest compute
is compute not done" (1) — and the instrument lesson is Julien's "real vs displayed is not
the same thing" (28): the presented tick is display, the decision tick is law.

## The lens

Second author on one run: I flew the checker's named experiments and nothing else. What the
lens may have made me miss: the burn arm's own physics under a *stream* of pinned decisions
(a player flying by hand) is one step beyond one pinned decision, and the WH-split boundary
path — 82% of boundary mass at 10⁴ — remains unprobed by either run; its per-event cost is
the shared-box p50 16ec corrected, but its no-op fraction has never been censused on its own
path (3570 censused both mixed).
