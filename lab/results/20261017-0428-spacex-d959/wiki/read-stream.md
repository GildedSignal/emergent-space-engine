topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-0428-spacex-d959

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best
**The wave's read stream is censused by call site on shipped main, and its N-linear half is
60% the per-event `Ctx::secondaries` rebuild — not the player's scan.** Settled straight
(14,600 game-s, no page, no view), each belt body's event pays 5.0 readouts
(checker-corrected from ~4.7): `secondaries`' `state_of` loop exactly 3.0/body — the doll's
3 source planets, a set constant in N, so the count is exactly 45,161 + 3·bodies
(checker-verified at held-out N=30,000) — and each call allocates a fresh `Vec<Secondary>`;
the scheduler's post-event raw read 1.0 (`observe.rs:190`, `root_state_raw`); the clock step
1.0 (`step.rs:660`). The sources' share of the per-body half is exactly 60%.
Pre-wave flight-only totals at 10⁵: 109,230 (coast) / 190,718 (burn) per ~1,900 game-s —
the checker finds them **bit-identical at 10⁴ and 10⁵** and the scan N-flat in the burn
flight too (99,113 at both N; coast 34,172), so the pre-wave stream is N-independent
outright; the one-shot view gather adds its own ∝N bill per emitter (the view's, not the
engine's; the checker measures ~2.9 readouts but ~8.5 `state_of` reads per belt body at
10⁵ — ≈3 `secondaries` rebuilds × 3 planets — so "3 source-reads per emitter" undercounts
~3×). At 10⁹ the per-body half is ~5.0×10⁹ lookups over the ~15 s wall of the wave at
rtf 100 ≈ 3×10⁸/s — the same order as the promotion page's 5.74×10⁷/s knee, **not a
re-derivation**: that knee was measured in cache lookups over a 20k-gs steady burn, this
census counts readout calls through the first wave only, and the two instruments have not
been cross-run (see Contradictions). Instrument: `readstat` (`#[track_caller]` census on
`Binding::readout`, tagged on `Ctx::state_of`), print-only; `ladder_digest` digest-identical
to pristine on all 13 cases (10 in the run's regen, the wave N=3000 and both belt
crossings re-run bit for bit by the checker) (20261017-0428-spacex-d959, spacex; Linux/x86,
orders of magnitude).

## Refuted
- **"The scan owns the burn read stream"** (the assumption under promotion's direction 1):
  on shipped main the scan is flat in N — in the settle (160,663 at every N from 10⁴ to
  3×10⁵) **and in the burn flight itself** (99,113 at both 10⁴ and 10⁵, checker-measured:
  the N-comparison the author's P2 promised but never ran); the N-linear term is the
  sources' re-reads (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% on every
  N-linear site; the stream belongs to the events, not the flight (20261017-0428-spacex-d959).

## Open directions
1. **Delete the per-event sources rebuild** (the named lever, ~60% of the per-body stream,
   ceiling ~1.7× on the N-linear half, plus the per-event `Vec` churn): one source readout
   per drain (or per source-tick) shared by the events of that drain. Unflown: whether the
   page's budget-sliced drain already batches events at shared ticks (the settle path here
   ran unbudgeted).
2. Price the deletion on the post-cadence stream first: ES_CHAIN/ES_SECULAR (nladder page,
   awaiting grade) reshape the wave itself.
3. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body) are the next terms; each is a read of the
   body itself, so the lever there is fewer events (cadence), not cheaper reads.

## Contradictions
- None yet; promotion.md's b = 11.48 reads/body/20k gs (cache lookups, patched binary,
  20k-gs horizon incl. post-wave) and this run's 12.9 counted readouts/body at 14.6k gs
  agree in order; the instruments differ (lookups vs readout calls) and have not been
  cross-run on one binary.

## Runs
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
  scan is flat in N, `secondaries` is 60% of the per-body half; digest-identical instrument.
