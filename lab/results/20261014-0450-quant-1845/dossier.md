# Dossier: the fired kick's non-bind half is one bisection — the crash-tick search, rebought from scratch every kick and every hand-out

## Claim

On shipped code, the plane's fired Wisdom-Holman kick is 46% bind and **45% one
`next_impact` bisection** (115 µs of a 254 µs kick at m4000/s3/rtf1/8s; ~25 readouts
at 4.6 µs each, re-searched from a half-orbit-wide bracket on **every** kick because
`rebind` resets the impact memo); the same search is paid once more by every
hand-out's first plan (~96 µs of the hand-out's replan). All other kick terms are 9%.
The named deletion: carry the retired tube's impact tick as the new search's bracket
(warm start + monotone verify + widen-and-fallback, exact by the predicate's
monotonicity) — priced by this run's numbers at **−45% on the fired kick and −18%
on the whole hand-out** (254 → ~140 µs; 529 → ~435 µs), with zero physics change.

## Bottleneck

Board live question 3 (the kick: 75–160 µs against a ~50 ns floor; "the cheapest
exact kick on the shipped representation") and 790b's named next wall ("the kick's
non-bind 55%"). This run decomposes that 55% into named terms: it is not forces,
not the readout at the kick's own tick, not the entry clones — it is **search**: the
crash-tick bisection `plan_terminal` runs after every rebind, whose bracket is
`[after.max(tp − half-period), tp]` (≈ 2²⁵ ticks wide → ~25 `decode` evaluations at
4.6 µs). PRINCIPLES #3: "Nothing is evolved that can be derived when looked at" —
the new tube's crash tick is one small bracket away from the retired tube's, and the
engine already caches exactly this per binding (`Binding.impact`) but drops the cache
in every rebind (`impact: None` in the new `Binding`).

## Evidence

Instrument: sub-stage `prof` counters inside `P_KICK` (readout+scalars, secondaries+tide,
force, quantize, `rebind`'s non-fit interior, `plan_terminal`, `next_impact`, word
quantize) plus a wall+call census of the readout family at its single choke point
`decode` (`bind.rs`). `ES_MEMBERS` lifts the bench clamp env-gated; the bench report
gains `prof_stages`. Reproduce: `lab/results/20261014-0450-quant-1845/regen.sh` (~4 min).

| arm (rtf 1, 8 game-s) | fired kick | bind (by subtraction) | impact bisection | other | readouts/search | hand-out (replan) |
|---|---|---|---|---|---|---|
| m4000/s3 (1032 kicks) | 254.1 µs | 117.1 µs (46%) | **115.2 µs (45%)** | 21.8 µs (9%) | ~25 | 528.9 µs (96.5 µs) |
| m1500/s3 (95 kicks) | 299.4 µs | 143.2 µs (48%) | **125.6 µs (42%)** | 30.6 µs (10%) | ~27 | 563.8 µs (96.1 µs) |
| m4000/s7, held-out (1105) | 256.7 µs | 119.3 µs (46%) | **115.0 µs (45%)** | 22.4 µs (9%) | ~25 | 536.3 µs (93.8 µs) |

- Every fired kick bisects (K_IMP calls = 2.00–2.10 × kicks; the second search per
  kick-count is the hand-out replan's — `plan_terminal` has four callers, and each
  hand-out's fresh binding also starts with `impact: None`).
- Identity: the prof build's digest equals the pristine build's at m400/s3
  (`db05a069…`, bit-identical) and the m1500/s3 arm reproduces be78's published
  digest `7b33d0b866149e71` exactly; m4000/s3 repeats its own digest `2e97e580…`
  across two runs with identical stage counts (1032/2064/1034). It does **not**
  equal ad26's `5cfe1a8e…` (2,043 hand-outs here vs 2,163 there): the tree has
  moved since f687ec25 and the hand-out count is wall-dependent (be78's own
  finding); the m1500 exact match is the cross-build reproduction.
- Cheap terms measured dead: force::acceleration 1.2 µs, quantize 0.1 µs, word 0.1 µs,
  secondaries+tide 7.6 µs, kick readout 4.9 µs, rebind's tau pair + three entry
  clones 7.9 µs (the clones are **not** the non-bind wall: ~8 µs, 3% of the kick).
- The readout family as a whole (`decode`, all callers): 1.77 M calls / 8.1 s at
  m4000 vs 1.2 s at m1500 — the kicks' and hand-outs' bisections (~100 k calls) are
  only its timed minority; the majority is the frame's position/view walks, a
  different bottleneck (b29b's fixed tier is its cousin).

## Predictions

`predictions.md` was written before the decisive arms. Held: P2 (readout family ≥ 40%
of non-bind — it is ~84%), P3 (bisection ≥ 25% of non-bind — it is ~84%, ~25
readouts each), P4 (cheap terms ≤ 10% — they are ~9%), P5 (kick cost flat in members,
254 vs 299 µs = +18%, inside ±20%), P6 (deletion ≥ 25% of the kick — priced at 45%).
Missed: P1's digest clause — m4000/s3 gives `2e97e580…`, not ad26's `5cfe1a8e…`
(tree drift + wall-dependent hand-out counts, disclosed above; the m1500 arm matches
be78's published digest exactly, and P1's cost clauses held: 254 in 230–280, bind
117 in 100–125). P3's mechanism clause "fires on most fired kicks" — it fires on
**every** fired kick and every hand-out (stronger than predicted).

## What would make it wrong

The warm-start price (~2–6 readouts per search) is arithmetic on this run's measured
4.6 µs/readout, not a built probe: if a kick's dv can move the crash tick outside any
small bracket often (near-apoapsis kicks on shallow-dipping tubes), the widen-and-
fallback eats the win — the build must count fallbacks. The deletion is exact only
because the predicate (radius below surface) is monotone on the fall branch, as the
shipped comment asserts; a tube whose new fit changes branch order would need the
fallback. Not tested: the player's clock kicks (P_KICK_CLOCK), non-battle scenes
(the quiet belt has no hand-outs), and the m4000 digest mismatch vs ad26 is
attributed to tree drift + wall, not proven byte-for-byte.

## Cost of adopting

One function's bracket choice plus carrying one `(Tick, Option<Tick>)` across the
rebind (the field already exists); no law change, no schema change, digest-identical
by construction (bisection on a monotone predicate is bracket-independent). The
instrument (prof sub-stages) is probe-only; prof off, the engine is untouched
(proven: bit-identical digest). Fit: PRINCIPLES #1 (delete before optimizing — this
deletes ~25 readouts to ~4, it does not speed the readout), #3 ("Nothing is evolved
that can be derived when looked at"), #14 ("we only care about changes").

## The lens

The Quant lens prices stages against their share and stops at the measured wall; it
priced the deletion by arithmetic instead of building it (a 60-minute window's
honest limit), and it nearly mis-attributed the 2:1 bisection ratio to a phantom
second caller inside the kick — the census (eprintln count per call site) caught
it: the second search is the hand-out's, which doubles the deletion's value. It did
not check whether the impact memo could instead be keyed by tube identity rather
than event_time (a design alternative the builder should weigh).
