topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1447-components-5eb2

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best
**The redundancy of the per-event sources rebuild is now measured, and it is large: the
`(doll, tick)` key of `Ctx::secondaries` is shared 2.66×-7.81× in flight (64-89% of all
calls), so direction 1's shared field read is real — but priced in wall time it buys only
~8-10% of the belt kick, because the kick's own mass is the fit, and the fit's mass is not
the quadrature.** Print-only nested stages (`READOUT`, `SECONDARIES`) plus a `(doll, tick)`
census in `Ctx::secondaries` (digest-neutral: `ladder_digest` N=3000 bit-identical with the
patch, prof off) on the shipped plane (20261017-1447-components-5eb2, Linux/x86):
N=3×10⁴ rtf 600 — kick clock item 46.3 µs/call, `bind_surface` 20.9 µs at 1.00 calls/kick
(45%), `secondaries` 6.25 µs (13.5%, 0.97 calls/event), `readout` 3.77 µs (372 calls/frame);
census 84,254 calls at 31,652 distinct keys = **2.66× redundancy, 63.9% of calls at
multiplicity ≥ 2, 62.6% at ≥ 8, 42% at ≥ 64**; held-out N=10⁴ rtf 1800 — 51.6-52.9/30.4/5.35/4.84
µs, census **7.8-8.2× (89-90% at ≥ 2, two runs)**: the budget-sliced drain does NOT batch events at shared
ticks — the ticks are already shared and every event re-reads them. The fit at true inputs:
`Rebinding::from_state` on 512 flown belt states = 17.3-28.0 µs/call against
`Orbit::compile` on belt-class keys = 4.4 µs median — the quadrature is ~26% of the fit; the
other ~13 µs is `at_radius`/`decoded_event`/`word_for` [inferred by subtraction, not
separately timed]. Micro: one wide u128/u128 division 22.4 ns vs the law's own exact
`div_word` 2.8 ns (8×); the belt compiles through `weak_quad`, which already uses it;
strong-field `fast_quad` still pays 4 wide divisions per node — found, measured, unadopted.

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
- **"Steady flight reads the field mostly alone at its tick"** (this page's own assumption
  under direction 1, and 5eb2's pre-registered prediction): measured wrong — 63.9% of
  secondaries calls share their `(doll, tick)` at rtf 600 pre-crest, 89.1% at rtf 1800 in
  the crest; the belt's two-comb train concentrates the stream at every pace flown
  (20261017-1447-components-5eb2).
- **b063's refit share (84-89% of the belt kick), read as `bind_surface` alone**: the fit
  is the largest term but 45-59% at the arms flown, with the quadrature only ~26% of it
  (20261017-1447-components-5eb2; different arms may explain the gap, none identified).

## Open directions
1. **Delete the per-event sources rebuild** (~60% of the per-body stream by calls; measured
   2.66-7.81× redundant at its `(doll, tick)` key): a pure `(d, t)`-keyed cache invalidated
   when a source of `d` rebinds is bit-identical by construction, ~30 lines in `Ctx`, and
   deletes 62-89% of secondaries calls — but only in the plane's steady/crest flight, the one
   regime censused here: 5ade measured a source memo dead on the spread belt (hit 0.029,
   kick-jet page), a different regime (the wave) on the same lever, unengaged by this run.
   The wall-time prize is only ~8-10% of the belt kick (6.25 µs of 46.3 µs at 2.66×), so
   adopt it as a stream/frame lever (readout is 372-743 calls/frame), not as the kick's cure.
   The invalidation rate (a source rebinding between two same-tick events) is unmeasured by
   the run: the checker's content-hash probe finds zero stale keys in 292k calls across three
   arms (N=3×10⁴/10⁵, rtf 600/1800/100), so the cache is safe in the regimes flown.
2. **Time `at_radius` and `decoded_event` directly** (the named next probe): the fit's
   ~13 µs beyond the quadrature is inferred by subtraction; if the repeated `state()` calls
   of `at_radius`'s binary search own it, the refit's lever is a smarter search over the
   same knots, not a cheaper compile.
3. Price the deletion on the post-cadence stream first: ES_CHAIN/ES_SECULAR (nladder page,
   awaiting grade) reshape the wave itself.
4. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body) are the next terms; each is a read of the
   body itself, so the lever there is fewer events (cadence), not cheaper reads.
5. **Adopt `div_word` in `fast_quad`'s four wide divisions** (strong field: 4 × 22.4 ns →
   4 × 2.8 ns per node, exact by the primitive's contract, precondition-guarded fallback):
   found and micro-measured, unflown — the belt path (`weak_quad`) already uses it.

## Contradictions
- promotion.md's b = 11.48 reads/body/20k gs (cache lookups, patched binary,
  20k-gs horizon incl. post-wave) and d959's 12.9 counted readouts/body at 14.6k gs
  agree in order; the instruments differ (lookups vs readout calls) and have not been
  cross-run on one binary.
- 5ade's source memo on the spread belt (hit 0.029, 20261016-1120-quant-5ade) and this run's
  2.66-8.2× key sharing in the plane's steady/crest flight: same lever, different regimes
  (wave vs plane); unresolved until the cache is flown on both. [Checker arms extend the
  plane sharing to 24-28× at N=10⁵ and rtf 100 — it concentrates further, never less.]
- a765's rebind share 84-87% (kick-jet page, awaiting grade, its arm's mean kick 62-75 µs)
  beside b063's 84-89%: the same tension as the line below, also unengaged by this run.

## Runs
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
  sources rebuild 2.66-7.81× redundant at (doll, tick); the quadrature ~26% of the fit.
- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
  scan is flat in N, `secondaries` is 60% of the per-body half; digest-identical instrument.
