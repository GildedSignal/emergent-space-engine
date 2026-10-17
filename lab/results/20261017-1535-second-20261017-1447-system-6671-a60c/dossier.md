# Dossier — 20261017-1535-second-20261017-1447-system-6671-a60c (second author, system lens)

## Claim

The (j,t) memo the first run only priced is now **flown and bit-exact**: it leaves every digest
and every delivered kick untouched, cuts the whole `state_of` read term **3.0×** (1.119 s →
0.369 s of an 8.4 s 10⁴-coast flight; a hit costs 72 ns against 3,636 ns a miss), and moves the
engine frame p50 by **−4.6% (10⁴ coast), −12% (10⁴ burn), −12.4% (10⁵ burn), ~0% (10⁵ coast)**
— so the term-level ceiling lands as a single-digit frame win, with the build's settle −20%
and the warm view gather −48% as side wins; and the structural half's premise is now measured
**at comb scale** (the checker's missing instrument): one canonical-tick read per comb pass
errs p99 ≤ 6.8e-4 relative in every arm, crossing the pre-registered 1e-2 line only as a max
(1.26e-2, the star j0, 10⁵, on the widest ~450–17k game-s arrears passes) — the whole-flight
drift that "failed" P3 was the wrong scale, and the real bound is the pass window, not the tick
sharing.

## Bottleneck

The board's `read-stream` axis: the N-linear per-event sources rebuild. The first run's
decomposition (free memo half / structural 74% comb half) priced the memo at ~1.7× on the
`secondaries` site; flown across all `state_of` sites it is 3.0× on the term (the centre site
repeats 93%, which the site-keyed census under-counted) — but the term is only ~13% of wall, so
the frame moves single digits. What it deletes: 70% of the read stream's evaluations, ~20% of
the build's settle, ~half the warm view gather. What it does not delete: the belt comb's
structural 74% (unchanged, as predicted) or the backlog at a saturated cut (kicks delivered at
the cut unchanged at 10⁵).

## Evidence (all from `regen.sh`, ≤ 15 min; every command below is in it)

Instrument: an opt-in memo (`crates/universe/src/memo.rs`, `ES_MEMO=1`) of `state_of`'s Ok
results keyed `(j, t)`, thread-local, **cleared at each `Universe::advance`** (never survives a
prune; bounded by one frame's distinct keys); refusals are never cached. An opt-in timer
(`ES_STATEOF_T=1`) prices the term; the census gains a per-pass grouping (one pass = one
`advance`, the frame's window — an upper bound on a drain slice). Off paths are branch-only.

- **Bit-exactness (P5).** `ladder_digest`, 3 cases × 4 schedules, memo off vs on: identical
  lines — `d2632de90255f5c10de9fd7372a3790d` (coast through the wave), `4995f384…` (belt
  crossing L10, burn), `253d8aed…` (key mashing), kicks 34537/40106/4723, "4 schedules agree"
  in all six runs, including the 4-thread schedule (`digest-control.txt`). Flight-level
  witness: 10⁴ coast delivers **kicks 65455, events 132089, game 35400.0 s in all six runs**
  (off and on interleaved) — the whole delivered set, not just the state.
- **The read term (attribution arm, `stateof-term.txt`).** 10⁴ coast, timer-instrumented:
  off — miss_ns 1.119e9 over 319,772 calls (3,499 ns/call) = **13.3% of the 8.4 s wall**
  (independently matching 5eb2's 13.5% kick-item share with a third instrument);
  on — miss 0.353e9 over 97,040 + hit 0.016e9 over 222,832 (72 ns/call) = **0.369 s, 3.03×
  cheaper on the term**.
- **Frames (`timing-n*.txt`, 3 interleaved reps/arm, medians).** p50 ms off→on:
  10⁴ coast 1.221→1.165 (−4.6%), 10⁴ burn 1.185→1.043 (−11.9%), 10⁵ burn 1.278→1.117
  (−12.4%), 10⁵ coast 1.438→1.440 (~0). p99: 10⁴ coast 10.63→9.89 (−7.0%); elsewhere flat —
  10⁵ coast p99 sits at the 11.95 ms budget clamp, 10⁵ burn at 35.8–39.5 ms with 101 frames
  over: **the saturated tail does not feel the memo**. Kicks at the cut unchanged at 10⁵
  (152,294 vs 152,421, inside the off-arm's own spread). Build_s 4.3→3.4 s at 10⁵ (the
  construction settle's birth wave memoizes); warm view gather 2.13→1.06 s at 10⁵ (the second
  gather hits the first's keys; the memo's live set after the flight is the gather's own
  doing). Total wall 8.3→7.7 s (10⁴ c), 23.3→20.6 s (10⁵ c).
- **Hit rates = the census's repetition, uninstrumented (P2).** memo hit_frac: 0.6966 (10⁴c),
  0.6675 (10⁴b), 0.455 (10⁵c), 0.434 (10⁵b). The census's blended per-site repetition at 10⁴c
  is (169,635+53,061)/319,867 = **69.6%** — the flight reproduces the instrument to the third
  digit, so the repetition is not the census's own artifact. max_live_keys ≤ 2.3k (10⁴) and
  ≤ 50.1k (10⁵ burn crest) — a few MB worst case.
- **Comb-scale canonical-tick error (P3, the misreported prediction, re-measured with an
  instrument that sees it; `census-n*.txt`).** Per pass, drift from the pass's first read,
  relative: 10⁴ coast — j0 p50 6.8e-6 p99 6.2e-5 max 3.8e-3; j1 p99 1.5e-5; j2 p99 1.2e-6;
  j3 p99 2.1e-5. 10⁴ burn — same picture (j0 max 5.8e-3). 10⁵ coast — j0 p50 3.2e-4 p99
  6.8e-4 **max 1.26e-2**; pass tick-spans: p50 1.95e6 ticks (9.6 game-s ≈ one frame window) at
  10⁴, but 9.15e7 ticks (450 game-s) at 10⁵ — behind the belt, one `advance` drains a deep
  arrears window. **Verdict: the 1e-2 line holds at p99 everywhere with ~2 orders of margin;
  the max crosses only for j0 at 10⁵ on the widest passes.** Conflicts still 0 (2.6e5 calls
  10⁴c, 1.65e6 at 10⁵, errs 0; the memo never caches an Err by construction).
- **The census's own cost (the checker's unpriced instrument):** +2.4% p50 and wall at 10⁴,
  +5% p50 at 10⁵ (census-on `census-n*.txt` ladder lines vs the off timing arms) — the first
  run's fractions carry that bias, in the direction of *under*-counting repetition.

## Predictions

`predictions.md` was written before the decisive runs (the three digest cases were already
running as the control; timing, attribution and census were unrun). **P1 partially held:**
p50 moved −4.6…−12.4% in three arms (above the 2% kill line) and ~0% in 10⁵ coast — the
missed arm is the one whose tail is budget-clamped, consistent with P1's own "p99 moves
little". **P2 held exactly** (0.6966 vs the census's 69.6% blend; the kill line 0.3 was never
near). **P3 held at p99 in all arms (≤ 6.8e-4 against the 1e-2 line); the max crosses at 10⁵
j0** (1.26e-2) — reported as the bound it is: the cure must bound the pass window. **P4 held
at its edge:** 10⁵-coast hit_frac 0.4550 against a predicted 0.35–0.45 band (the memo keys
across sites, so it sits just above the per-site census's 43.9%); burn < coast as predicted.
**P5 held** (all three cases, all four schedules, bit for bit; plus the flight-level witness).

## What would make it wrong, adoption cost, fit

- Wrong if: an out-of-order path ever reads a source at a tick after the source's own event at
  that tick lands (the queue's tick order and 0 conflicts over ~4M reads now say no, and the
  4-thread schedule digest agrees); or if a shipped version cleared less often than per
  `advance` and outlived a prune (this probe clears per advance; under `threads > 1` each
  resolver thread keeps its own map — bit-safe here, but a shipped version should clear per
  wave).
- Adoption: ~40 lines (the flown core of `memo.rs` + the `state_of` hook + the `advance`
  clear). Memory: the distinct keys of one frame (≤ 50k measured, ~3.5 MB worst). It is a
  frame/stream/build/view lever, **not** a throughput lever at a saturated cut and not the
  belt comb's cure.
- Fit: PRINCIPLES 1 and 3 ("compute only surprises" — the repeated reads return the same
  bits; measured 70% of the term); 21 (rough first: the census priced it, this flew it);
  2 (it is a behaviour-neutral cache: digests and delivered kicks unchanged). The frame win
  is honest single digits — the term is 13% of wall, and no cache on it was ever going to
  move p99 at a clamped tail.

## The lens

The second-author lens made me treat the checker's two asks as one question — "does the priced
split survive contact with the frame?" — and answer both halves on one binary. What it may
miss: the memo's effect on cache locality at 10⁶+ (the map is tiny, but the working set
shifts), the arrears-pass structure at 10⁵ (my pass = one `advance` is an upper bound on the
drain's finer slices — the comb-scale errors are upper bounds too), and I did not fly the memo
on the spread-belt regime where 5ade's source memo hit 0.029 (the wiki's open contradiction;
the plane's steady/crest flight is a different regime).
