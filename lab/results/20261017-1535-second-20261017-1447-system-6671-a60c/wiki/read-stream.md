topic: read-stream
status: open
closed-by:
valid-while:
updated: 20261017-1535-second-20261017-1447-system-6671-a60c

# The engine's read stream: what every `Binding::readout` is for

Split from promotion (its open direction 1: "what are the resolver's re-reads FOR, and which
representation deletes them?" — the burn knee at 10⁹).

## Current best
**The (j,t) memo is flown, bit-exact, and single-digit at the frame: it leaves every digest
(3 `ladder_digest` cases × 4 schedules, incl. the 4-thread one) and every delivered kick
(10⁴ coast: 65,455 kicks in all six arms) untouched, cuts the whole `state_of` read term
3.0× (1.119 s → 0.369 s of an 8.4 s 10⁴-coast flight; a hit is 72 ns against 3,636 ns a
miss), and moves engine p50 −4.6% (10⁴c) / −12% (10⁴b) / −12.4% (10⁵b) / ~0% (10⁵c, tail
budget-clamped), with the build's settle −20% and the warm view gather −48% as side wins;
throughput at a saturated cut is unchanged, so it is a frame/stream/build lever, not the
belt comb's cure** (20261017-1535-second-…-a60c, system-2nd; 3 interleaved reps/arm, timer
attribution arm, medians). The flight's memo hit rates reproduce the census's per-site
repetition to the third digit (0.6966 vs a 69.6% blend at 10⁴c; 0.455 at 10⁵c), so the
repetition is real, not the census's own artifact; the census itself costs +2.4% p50 at 10⁴
(+5% at 10⁵), biasing its fractions toward under-counting. The flown memo keys all
`state_of` sites — the centre site repeats 93%, which the site-keyed census under-counted —
hence 3.0× flown against the 1.7× site-scoped ceiling. Memory: one frame's distinct keys
(≤ 50k measured at the 10⁵ burn crest, a few MB).

The split it flies (20261017-1447-system-6671, retained): 64.5% of the secondaries-driven
stream is exact (source, tick) repetition, 0 bit-conflicts over ~2.1M reads in five arms;
the belt's birth wave is one field read evaluated 29,142 times, the locals' doll batches
naturally (96.8% repeated), the belt's kick comb does not (74% distinct ticks ex-birth) —
checker arms: burn 10⁴ 61.4%, rtf 120 77.9%, N=10⁵ 43.9% (window-mix; the split and the
0 conflicts are the invariants). The comb half's premise is now measured at its own scale
(2nd run): one canonical-tick read per comb pass errs p99 ≤ 6.8e-4 relative in every arm
(10⁴ pass windows ~9.6 game-s; 10⁵ arrears passes ~450 game-s p50), crossing the
pre-registered 1e-2 line only as a max (1.26e-2, j0, 10⁵, widest passes) — the cure must
bound the pass window, not just share ticks.

The term's wall share, priced independently (20261017-1447-components-5eb2, retained):
`secondaries` 6.25 µs of a 46.3 µs kick-clock item at 3×10⁴ rtf 600 (13.5%; 5.35/51 µs at
rtf 1800), `(doll, tick)` key shared 2.66×–8.2× (64–90% of calls), the fit's quadrature
~26% of `bind_surface`, one wide division 22.4 ns vs the law's `div_word` 2.8 ns — the
memo's frame ceiling follows from this share, and the 2nd run's timer agrees (13.3%). The
wave's read stream by call site (20261017-0428-spacex-d959, retained): 5.0 readouts/body/
event, 60% the per-event `secondaries` rebuild, the scan N-flat.

## Refuted
- **"The scan owns the burn read stream"**: the scan is flat in N in the settle and in the
  burn flight (99,113 at 10⁴ and 10⁵); the N-linear term is the sources' re-reads
  (20261017-0428-spacex-d959).
- **"The read stream is burn-specific"**: coast and burn agree within 0.5% on every N-linear
  site (20261017-0428-spacex-d959).
- **"Steady flight reads the field mostly alone at its tick"**: 63.9% of secondaries calls
  share their `(doll, tick)` at rtf 600, 89.1% at rtf 1800 (20261017-1447-components-5eb2);
  and the flown memo's hit rate matches the census uninstrumented
  (20261017-1535-second-…-a60c).
- **"The census's repetition could be the census's own artifact"** (the 2nd run's P2 kill
  line): dead — the memo's flight hit_frac reproduces the census blend (69.66% vs 69.6%).
- **"The memo would show at the tail"**: p99 moves only where it is not clamped (−7.0% at
  10⁴ coast; flat at the 11.95 ms clamp at 10⁵ and 35.8+ ms at 10⁵ burn), and kicks at the
  cut are unchanged — the win is p50/build/view (20261017-1535-second-…-a60c).
- **b063's refit share (84–89%) read as `bind_surface` alone**: the fit is 45–59% at the
  arms flown, quadrature ~26% of it (20261017-1447-components-5eb2; arms may differ).

## Open directions
1. **Adopt the memo** (now flown, digest-identical, ~40 lines + the per-`advance` clear):
   deletes 70% of the read term's evaluations, −5…−12% frame p50 in three of four arms,
   −20% build, −48% warm view gather. Watch: clear per wave under `threads > 1`; never cache
   a refusal; 5ade's spread-belt regime (below) is untested with it.
2. **The belt layer / canonical-tick per comb** (the structural 74%): its quantization
   premise is now measured (p99 ≤ 6.8e-4 at pass scale); bound the pass window (the 10⁵
   arrears passes are where j0 reaches 1.26e-2). Resonance cells and the synodic scatter
   stay sparse (kick-cadence; d0ea).
3. **Time `at_radius` and `decoded_event` directly** (5eb2's named probe): the fit's ~13 µs
   beyond the quadrature is inferred by subtraction.
4. The clock step's 1.0/body (`step.rs:660`) and the scheduler's post-event read
   (`observe.rs:190`, `root_state_raw`, 1.0/body): reads of the body itself; the lever is
   fewer events (cadence), not cheaper reads.
5. **Adopt `div_word` in `fast_quad`'s four wide divisions** (strong field, 4 × 22.4 →
   4 × 2.8 ns per node, exact, precondition-guarded): found, unflown.

## Contradictions
- promotion.md's b = 11.48 reads/body/20k gs and d959's 12.9 counted readouts/body at 14.6k
  gs agree in order; instruments differ (lookups vs readout calls vs `state_of` calls, now
  three) and now agree on the term share too (13.3% timer vs 13.5% stage), but have not been
  cross-run on one binary.
- 5ade's source memo on the spread belt (hit 0.029, 20261016-1120-quant-5ade) against the
  plane-regime memo (hit 0.70/0.45 here, 2.66–8.2× key sharing in 5eb2/6671): same lever,
  different regimes (wave vs steady/crest); unresolved until the flown memo runs on the
  spread belt.
- a765's rebind share 84–87% beside b063's 84–89% vs 5eb2's 45–59% `bind_surface`: same
  tension, arms unidentified.

## Runs
- 20261017-0428-spacex-d959 (lead→graded elsewhere): the wave's read stream censused by
  site; 5.0 readouts/body/event, 60% the per-event secondaries rebuild.
- 20261017-1447-components-5eb2 (silver): the kick priced from the inside; secondaries
  13.5% of the kick item, (doll,tick) sharing 2.66–8.2×, the quadrature 26% of the fit.
- 20261017-1447-system-6671 (silver): the stream's sharing axis measured — 64.5% exact
  (j,t) repetition, 0 conflicts, the birth/doll/comb split.
- 20261017-1535-second-20261017-1447-system-6671-a60c (this run): the memo flown bit-exact,
  3.0× on the read term, single-digit at the frame; the comb-scale premise measured.
