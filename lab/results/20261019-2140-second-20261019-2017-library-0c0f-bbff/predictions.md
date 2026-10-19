# Predictions (written before the decisive arms B1, C0, C1)

Baseline B0 (flown first, stagger off, this box): max 1,661.8 ms, over 47, worst frame 33,470
events, wave frames 454–488, player doll 2→0 at frame 157. Record band: max 1,676–2,020, over
42–55, worst 33,069–35,986. Everything below is a prediction about arms not yet flown.

## P1 — the named gate (B1: `ES_STAGGER=1`, 2×10⁵, burn, rtf 2000, 12 ms)

The freeze collapses. Letter: **max_ms ≤ 150 ms** (≥ 11× below the 1,676–2,020 record band;
my estimate 20–60 ms — the staggered first-kick stream is ~200k kicks over ~30k gs ≈ 6.7
kicks/gs ≈ 200 a frame at 30 gs/frame, carried throttled by the per-item stop, not gulped).
Secondary letter: **over ≤ 47** (no worse than B0's count) and **p99 ≤ 50 ms**.
Falsifier: a ≥ 300 ms frame in B1 means the deletion fails at this cadence — the carry has
found another concentration (boundary wave, second-order grid) and I report the thesis dead
at this rung.

## P2 — the mechanism (C0: coast, 2×10⁵, rtf 2000, 14 s, stagger off)

The checker's coast arm stopped at 13,291 gs, short of the wave onset (~14.1–15.2k gs in the
burn arms); "no wave, onset window fully covered" was frame-indexed, not game-time-indexed.
C0 crosses it. Letter: **game coverage ≥ 15,000 gs AND max_ms < 50 ms** — the wave arrives as
events (a sustained near-budget plateau; events p99 above the checker's non-crossing 255) but
no 1.7 s freeze, because in coast the player never enters the root doll (the record's own
`(0, 2)`-only doll trace), so the wave resolves as budgeted top-level items, not as one
player item's nested pull. This kills the "burn-gated / burn-response kick-grid re-mint"
reading: `step::decide` re-plans only the player's own rec (step.rs:880), no belt-wide re-mint
exists; the burn's role is the doll crossing at frame ~157–165, after which `pull_ships(key,
!in_root)` with in_root = true is every due root ship (cc9d's mechanism, at 2×10⁵).

## P3 — the dial's positive control (C1: coast, stagger on, same flight as C0)

**events p99 (C1) < events p99 (C0)** and max_ms still < 50 ms: the arrival concentration is
flattened by the dial itself in the mode without the carry (ed3a's flattening, first time at
2×10⁵), so P1's collapse is the dial deleting the concentration, not an artifact of the burn.

## P4 — the law is untouched (B1 vs B0)

**kicks total within ±10%** (B0: 231,982; record 231–233k): the stagger moves kick times, not
counts; refusals 0, dead 0, player alive in every arm.

## What I would count as failure of the whole story

- B1 max ≥ 300 ms (P1 falsifier above), or
- C0 freezing (max ≥ 300 ms) — then the wave is a law property of the grid that throttling
  cannot absorb even without the carry, and the re-rank (deletion before scheduler) is wrong, or
- C1's event p99 ≥ C0's — then the dial does not flatten arrivals at this scale and P1's
  mechanism claim is unsupported even if the number collapses.
