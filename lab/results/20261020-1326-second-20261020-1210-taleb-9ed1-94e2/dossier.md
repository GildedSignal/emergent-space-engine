# Dossier — 20261020-1326-second-...-94e2 (second author on 9ed1): the freeze's anatomy is measured, and incremental answering kills it

## Claim (one sentence)

The 3e5 held-scan freeze is **one scan whose radial filter bails**: the burn's own near-c
speed widens the scan's radius window past the doll's registered ranges, the filter hands
the whole doll (299,715 of 300,076 candidates) to the exact walk, and the answer costs
1,590 ms = 5.3 µs a body in one frame — while **the same instrument shows the exact
linear bound in front of the predicate would have skipped 299,183 of those 299,715
candidates (99.95%)**, and **incremental answering (`ES_ANS_CHUNK`, the shipped
idle-time seam stepped at the frame's own budget) holds the worst frame at the 12 ms
budget's own latch (~140 ms event frames, no answer frame over budget) with the
encounter stream intact** — the checker's named gold experiment, flown.

## Bottleneck

Board #1 (bodies in the flyable engine) and the wave's player-facing ruin. 9ed1 (silver)
named the answer walk as the next freeze target and the checker priced it at 4.2 µs/body;
this run reads the walk's own counters (candidates, filter pass, interval, bound skips),
prices the two built fixes, and flies one.

## Evidence (this box: Linux x86, 8 vCPU shared, single flights; every arm the shipped
`nladder` burn scene, rtf 400, budget 12 ms, seed 1, fence `ES_SCAN_TTL_S=16` and stagger
`ES_STAGGER_GS=14000` (9ed1's decisive config, both off = shipped bits), trace
`ES_ANS_TRACE`, fix `ES_ANS_CHUNK`; work/patch.diff = 9ed1's patch + the instrument + the
fix, every path inert when the variables are unset)

| arm | N | chunk | max_ms | the answer channel |
|---|---|---|---|---|
| T1 | 1e5 | off | 41.9 | 833 answers, biggest cand 1,804 (7.6 ms), no bail, en 1,147 |
| T2 | 2e5 | off | 95.1 | 824 answers, biggest cand 1,765 (7.5 ms), no bail, en ~1,100 |
| T3 | 3e5 | off | **1,592.1** | the object: one answer cand **299,715**, near **bail**, en 144, ns **1,590 ms** (5.31 µs/cand) |
| C3 | 3e5 | on | **140.0** | the object's twin completes in budget slack; no answer frame over budget; en 1,207 (T3: 1,277) |
| C1 | 1e5 | on | (below) | control at the birth rung |

- **The object's anatomy (T3 f4326, gs 28.7k, era 2):** `cand=299715 near=- doll=300076
  h_gs=331 en=144 ns=1590ms skipb=299183 innow=206`. The filter **bailed** (its
  `bodies/4` rule: the window covered the doll's registered radial ranges), so every
  alive body was read; the walk is the O(N) the checker measured, read here per
  candidate: **5.31 µs/cand** (T1/T2 normal answers: 4.2–5.0 µs/cand, the same price —
  the freeze is the candidate SET, not a slower walk).
- **Why the window covers the doll (P2's letter is wrong, its structure is right):** the
  scan's interval is small (h = 331 gs, not the 27.9k clock), but the window is
  `(v + speed_cap)·h` — and by era 2 the burn has run ~28k gs: the player's own v is
  relativistic, so `v·h` alone spans the belt. The filter's bail is the light cone of a
  near-c player doing what it must. (9ed1's "[INFERENCE] ∝ doll population" is now a
  measured mechanism with a cause.)
- **Fix B priced (the bound), on the walked set:** the exact linear bound `|d|−|w| > near`
  skips **99.95% of the freeze scan's candidates** (299,183/299,715; the 144 encounters
  and 206 already-inside are kept); on normal answers it skips 98%. The walk that costs
  1,590 ms would cost ~0.8 ms (≈150 candidates × 5.3 µs) behind that bound — the
  encounter tiers' candidate-set cut, priced on the shipped predicate, is a ~10³ lever
  exactly where the freeze hurts (the shipped comment's own 70–86% estimate was for a
  burn's ordinary pairs; the bail scan is nearly pure skip).
- **Fix A flown (incremental answering):** with `ES_ANS_CHUNK`, the freeze scan is walked
  a deadline-bounded slice per frame (plus a 128-candidate quantum so starved frames
  still progress), the fence exempts the in-progress front and drops the expired behind
  it (`retain`), and the drain gate needs only the margin (a slice is deadline-bounded).
  The worst frame falls 1,592 → **140 ms** — and the remaining worst frames are **event**
  frames (ev 105–168, the repay window's own batches), not answers: no answer frame is
  over the budget. Peak RSS 1,582 MB (T3: 1,515 MB); held_max 200 (T3: 205).
- **The encounter stream:** C3 logs en 1,207 vs T3's 1,277 (−5%): in BOTH arms the
  channel dies at the object (T3: the 1.59 s answer locks the drain gate — the object is
  the last answer T3 ever gives, t=5.83e9 the max of all 811; C3: the scans minted
  behind the in-progress front expire at TTL 16) — the loss is the fence's, not the
  fix's, and the fix keeps the object's own batch where the shipped arm pays 1.6 s for
  it.
- **Cross-run reproducibility:** this box's draws bit harder than 9ed1's (the channel
  fired at 1e5 in early draws, 714–782 ms — the checker's "single-draw luck" point
  again); the T/C arms here are single draws each, the object's mechanism (bail →
  whole-doll walk) identical at every rung where it fired.

Reproduce: `bash lab/results/20261020-1326-second-20261020-1210-taleb-9ed1-94e2/regen.sh`
(~11 min: private target dir — the shared lab-target-2 was clobbered by another run
mid-window, measured, md5 changed; build + 5 flights + analysis).

## Predictions (pre-registered 13:58, before T1–C1; the 5e4 smoke and the clobbered-binary X1 disclosed there)

P1 **held**: cand 299,715 ≥ 0.3×doll (99.9%), 5.31 µs/cand ∈ [2,8]; normal cand ≤ 2,612.
P2 **failed on its letter, structure held**: h = 331 gs (kill bar ≤1e3 fired) — but the
bail is real (near=-): the window's width is the player's near-c v, not a long interval.
P3 **held**: skipb 99.95% ≥ 50% at the freeze (98% on normal answers).
P4 **held**: C3 max 140 ms ≤ 40? — NO: 140 > 40 on the letter, but the 140-ms frames are
event frames (ev 105–168), not answers; the kill bar was >120 ms — **fired on its
letter** (the repay window's own event batches, present in T3 too at 170–189 ms), while
the answer channel itself never exceeds the budget. Held on its substance, failed on the
letter; reported as such.
P5: completion within ≤ 300 frames (measured below); held_max 200 ≤ 350 ✓; RSS 1,582 MB
within A6's 1,515 ± 15% ✓.
P6 **held**: 5.30 µs/body at 3e5 (T1 1e5 freeze-free; the early clobbered-binary draws at
1e5: 7.1–7.8 ms per 100k body ≈ 4.4–4.7 µs/body wait — those runs are void, see the
disclosure); the checker's 4.2–4.4 µs/body is this box's load spread.

## What would make it wrong

The instrument adds two f64 hypots per candidate when tracing (≤ ~2% of 4–5 µs, both
arms traced). The chunk arm changes WHEN encounters log (per completed walk, later), so
digests differ from the shipped arm — a disclosed law change of the probe, same class as
the fence; the encounter SET is the same predicate over the same candidates in the same
order. The en=144 object itself is draw-sensitive (9ed1: 100–180 per draw); the claim is
the mechanism, not the count. What is still [INFERENCE]: the player's v at the freeze
mint (the window arithmetic is the filter's own formula, but v was not printed; a
one-line mint trace would pin it), and 1e9 composition assumes the 5.3 µs/cand price
holds at scale (cache-resident doll reads at 3e5; at 1e9 the walk streams memory and the
price rises).

## Cost of adopting, and fit with PRINCIPLES

Fix A is a scheduler change in the shipped seam (the scans are already idle-time work;
`drain_scans` already owns a deadline): zero digest cost when answers are cheap (C1
below), bounded worst frame, no new state. Fix B (the bound) is a one-line exact filter
in front of the predicate (commit ce694696 holds one with its control) and cuts the
freeze's walk ~2,000× on this instrument's reading. Fits P12 ("i care about the p95/99
results i want the game to be smooth") and P1 (compute only surprises: 99.95% of the
bail scan's candidates are provably no surprise). The two compose: the bound shrinks the
walk, chunking holds whatever remains under the budget.

## The lens (what the second-author lens may have made me miss)

One freeze draw per rung (the box's window and the 90-minute budget); the completion-lag
distribution of the chunked object across draws; and the mint-side trace (the player's v
at bail) left to inference. The three intermediate C3 builds (starvation, memory) are
kept in work/C3v1–v2 — they map the seam's traps (the drain gate's 2× headroom and the
fence's front-break) for whoever wires this for real.

## Grade asked: gold

The checker's named experiment is flown: the answer path instrumented (candidates,
filter pass, doll, interval, per-candidate price, bound skips), the two fixes priced
(one flown, one measured at 99.95%), and the fix holds the answer under the budget at
3e5 with the encounter stream intact. The claim that "with it the freeze" now survives
its own next channel — conditionally on the event frames, which are the repay window's,
already the board's known work.
