topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1535-spacex-f1e6

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹). The page's 20261017-1447 window conflict
(components-5eb2 vs system-6671, two same-window censuses of the same lever) is resolved by
this run: both measurements stand (they are complementary — redundancy + wall pricing in 5eb2,
structural split in 6671), and the adoption both named as direction 1 has now been flown.

## Current best

**The (doll, tick) memo is FLOWN, bit-identical on the whole frozen record, and it deletes
65-83% of the secondaries calls in every regime flown — including the belt's kick wave, where
5ade's spread-belt 0.029 is not reproduced (0.646 cumulative through the wave at 10⁵) — while
the view's one-gather cost halves in every pair (2038→1010 µs at 10⁵, 6/6 pairs) and the
engine p50 moves −4% to −17% (20261017-1535-spacex-f1e6, spacex; Linux/x86, within-window
pairs).** The arm (`ES_MEMO=1`, ~90 lines in `ctx.rs`/`universe.rs`, default off): a
`(doll, tick, except)` map on `Ctx::secondaries` — `except` normalised to `usize::MAX` for
bodies that are not sources of the doll, so test particles share entries — invalidated by a
per-doll generation bumped in `Universe::apply` (the one place a body's plan changes) when one
of the doll's sources rebinds, cleared each frame. **Correctness:** all 13 `ladder_digest`
cases × 4 schedules (1/4 threads, 3 budgets) print identical digests/kicks/encounters/contacts
ON vs OFF, and OFF reproduces the frozen record `ladder_digests_wave.txt` exactly, both wave
cases included — the patch with the arm off is pristine bits, and the memo changes no outcome
anywhere it was tested (burns, key mashing, the wave, both belt crossings, 4 threads).
**Hit rates:** 0.793 (10⁴ coast rtf600), 0.826 (crest rtf1800), 0.768 (burn), 0.751 (10⁵
pre-wave), 0.646 (10⁵ through the wave, 20,000 game-s incl. ~5,500 post-wave: no collapse
visible at this dilution — the one regime still open is a long post-wave horizon). **Wall
(orders of magnitude, shared box, paired):** engine p50 1.616→1.344 ms (rep 1.251→1.158;
across-window OFF noise ±22%), crest 5.295→4.863, burn 1.119→1.078, wave arm 4.378→4.132;
over-budget frames 3→0 / 5→1 / 2→2; **the view gather halves outright** (its `force::field`
reads ride the same memo, `observe.rs:145`). Scope, confirming 5eb2's pricing: this is a
read-stream lever (65-83% of secondaries calls, the view's gather), NOT the kick's cure — the
fit owns the kick and the p50 deltas are single-digit to −17%. Adoption: the patch is written,
env-gated, digest-proven; one merge flips the default.

*[Both 1447 censuses stand, retained below — they measured the same lever from two sides and
are why this run existed.]*

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

**The stream's shared-field premise is now measured from the inside: 64.5% of the
`secondaries`-driven `state_of` stream is bit-identical repetition — 169,145 of 262,198
calls repeat an exact (source, tick) key, 0 bit-conflicts anywhere — and the split is
structural, not uniform: the belt's birth wave is ONE field read evaluated 29,142 times
(j0/j1/j2 at t=0, 9,714 identical reads each, once per belt body), the locals' doll batches
naturally (its source read 112,277 times at 3,579 distinct ticks, 96.8% repeated, top 342×),
while the belt's kick comb does not batch at all (74% distinct ticks ex-birth) — so
direction 1's lever splits in two: a per-(j,t) memo in `Ctx` is bit-safe (mechanism:
bindings change only at the source's own events, resolved in tick order; measurement: 0
conflicts) and free (~1.7× on the N-linear `secondaries` term), but it cannot touch the
belt comb's structural 74%, whose cure is one canonical-tick field read per comb (BELT_SPLIT's
legality class) or the belt layer itself (20261017-1447-system-6671, system;
`nladder 10000 coast 60 600`, print-only census, digest-identical on `ladder_digest
"N=3000 coast through"` both arms).** Checker arms (20261017-1447 check): burn at 10⁴ (61.4% repeated, 0 conflicts, comb ex-birth
74.6% distinct), rtf 120 (77.9%, 0 conflicts) and N=10⁵ (43.9% overall, 0 conflicts, same
split: comb 74.1% distinct ex-birth, doll 96.8%, birth 99,714×3) — the headline fraction is
window-mix dependent (birth-wave share falls as the crest widens); the decomposition and the
0 conflicts are the invariants, over ~2.1M reads. [20261017-1535: 6671's "cannot touch the
belt comb" half is now measured too optimistic at flight scale — the flown memo's wave-arm hit
rate is 0.646 cumulative; the comb's distinct-74% ex-birth is a per-call-site split, not the
whole flight's.]

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
census counts readout calls through the first wave only, and the two instruments have not been
cross-run (see Contradictions). Instrument: `readstat` (`#[track_caller]` census on
`Binding::readout`, tagged on `Ctx::state_of`), print-only; `ladder_digest` digest-identical
to pristine on all 13 cases (10 in the run's regen, the wave N=3000 and both belt
crossings re-run bit for bit by the checker) (20261017-0428-spacex-d959, spacex; Linux/x86,
orders of magnitude).

## Refuted

- **"The memo's viability is unsettled until it is flown"** (this page's own standing conflict,
  both 1447 sides' open direction 1, and 5ade's 0.029 read as the counter-case): flown —
  bit-identical everywhere tested, hit 0.65-0.83 in every regime including the wave, view
  gather halved (20261017-1535-spacex-f1e6). What survives of 5ade: a long post-wave horizon
  is the one regime not flown; its 0.029 was measured on a differently-keyed memo (kick-jet
  page), and the shipped comb does not reproduce it.
- **"Steady flight reads the field mostly alone at its tick"** (this page's own assumption
  under direction 1, and 5eb2's pre-registered prediction): measured wrong — 63.9% of
  secondaries calls share their `(doll, tick)` at rtf 600 pre-crest, 89.1% at rtf 1800 in
  the crest; the belt's two-comb train concentrates the stream at every pace flown
  (20261017-1447-components-5eb2).
- **b063's refit share (84-89% of the belt kick), read as `bind_surface` alone**: the fit
  is the largest term but 45-59% at the arms flown, with the quadrature only ~26% of it
  (20261017-1447-components-5eb2; different arms may explain the gap, none identified).
- **"The belt comb's shared ticks make the per-event rebuild a free batch"** (the
  optimistic reading of direction 1): the belt's kick-time source reads are 74% distinct
  ticks ex-birth; only the locals' doll and the birth wave collide exactly
  (20261017-1447-system-6671). [20261017-1535: at whole-flight scale the comb's 74%-distinct
  still leaves the wave arm at 0.646 cumulative — the two readings measure different cuts.]
- **"The scan owns the burn read stream"** (the assumption under promotion's direction 1):
  on shipped main the scan is flat in N — in the settle (160,663 at every N from 10⁴ to
  3×10⁵) **and in the burn flight itself** (99,113 at both 10⁴ and 10⁵, checker-measured:
  the N-comparison the author's P2 promised but never ran); the N-linear term is the
  sources' re-reads (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% on every
  N-linear site; the stream belongs to the events, not the flight (20261017-0428-spacex-d959).

## Open directions

1. ~~Adopt the (j,t) memo~~ **Flown and proven (20261017-1535-spacex-f1e6)**: flip the
   `ES_MEMO` default, delete the env gate. What remains: (a) the long post-wave horizon
   (5ade's one open regime — fly `nladder 100000 coast 120 1000`-class through and past the
   wave and read the cumulative hit rate's tail); (b) the mutex is lab-grade — a shard per
   doll or a frame-scoped arena is the shipped form if the 4-thread path ever matters
   (digests hold at 4 threads; throughput under contention unmeasured).
2. **Time `at_radius` and `decoded_event` directly** (the named next probe): the fit's
   ~13 µs beyond the quadrature is inferred by subtraction; if the repeated `state()` calls
   of `at_radius`'s binary search own it, the refit's lever is a smarter search over the
   same knots, not a cheaper compile.
3. **The belt layer** (the structural 74%): one canonical-tick field read per comb — a
   quantization in BELT_SPLIT's open legality class — or the full layer (one field pass
   per comb, compact-store members, one compiled cycle per cell) that also retires the
   rebind (68–85%, 620e/96b4) and the 4.85–5.06 kB/B plateau (b30b). Hard case: resonance
   cells and the synodic scatter stay sparse (kick-cadence; d0ea). [The flown memo now
   covers the shared 65-83% of the stream's calls; the layer's remaining prize is the
   comb's distinct ticks plus the rebind and the tube memory.]
4. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body) are the next terms; each is a read of the
   body itself, so the lever there is fewer events (cadence), not cheaper reads.
5. **Adopt `div_word` in `fast_quad`'s four wide divisions** (strong field: 4 × 22.4 ns →
   4 × 2.8 ns per node, exact by the primitive's contract, precondition-guarded fallback):
   found and micro-measured, unflown — the belt path (`weak_quad`) already uses it.
6. Price the deletion on the post-cadence stream first: ES_CHAIN/ES_SECULAR (nladder page,
   awaiting grade) reshape the wave itself.

## Contradictions

- promotion.md's b = 11.48 reads/body/20k gs (cache lookups, patched binary,
  20k-gs horizon incl. post-wave) and spacex-d959's 12.9 counted readouts/body at 14.6k gs
  agree in order; the instruments differ (lookups vs readout calls) and have not been
  cross-run on one binary. The 1447 census counts `state_of` only (2.42/event here): a
  third instrument, same order.
- a765's rebind share 84-87% (kick-jet page, awaiting grade, its arm's mean kick 62-75 µs)
  beside b063's 84-89%: unengaged by this run; the flown memo does not touch the rebind.
- The 1447 window's own conflict (5eb2 vs 6671, "priced in wall it buys ~8-10%" vs "free
  ~1.7×") is reconciled by the flight: both were right — the wall prize on the ENGINE is
  5eb2's single digits (fit-owned), and the call-count deletion plus the VIEW's gather
  halving are 6671's free lever. No live conflict remains on this page.

## Runs

- 20261017-0428-spacex-d959 (awaiting grade): the wave's read stream censused by site; the
- 20261017-1447-components-5eb2 (awaiting grade): the kick priced from the inside; the
- 20261017-1447-system-6671 (awaiting grade): the stream's sharing axis measured — 64.5%
- 20261017-1535-spacex-f1e6 (this run, spacex): the (doll,tick) memo flown — bit-identical
  on all 13 digest cases × 4 schedules, hit 0.65-0.83 everywhere incl. the wave, view gather
  halved 6/6 pairs; 5ade's 0.029 unreproduced, post-wave horizon open.
