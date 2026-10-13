# Predictions (written before the census runs)

The question: does ONE acceleration word per binding — written where the kick already
computes `force::field(...).accel` (step.rs:669) and discards it — serve the three
consumers that today re-derive the same second-order term?

- the view (`observe::partial`, observe.rs:145): re-derives the field per read (81% of
  readout, 7b86);
- gravity-news (7ab4): the version payload must carry the source's total acceleration
  (the ½aT² thrust-blindness);
- frame-cost (174d): the burn waterfall is the velocity word's re-sampling of the burn;
  the lever carries the burn in the tube's generator.

The census (probe `a_word.rs`, shipped code, plane seed 1, 48 members, rtf 100, 8 s per
flight): at every frame, for every body whose binding the shipped readout would complete
with a partial step (a clock kick, 0 < τ ≤ 2·len), sample

- `term` = |a(mid)|·τ²/2 — the per-read term the shipped readout pays to compute (doll units);
- `err`  = |a(mid) − a(B)|·τ²/2 — the error if the term came from a word stored at the
  window's boundary B instead (doll units);
- `Δa/a`, and the same Δa across the light window to the dominant secondary (the news
  consumer's T).

Cases not tuned on: I have not run anything yet; the thresholds below are set by the
pages' published budgets (7b86: the term is ≤ 9.8×10⁻⁶ root ticks on plain scenes; the
gather's quantum is 1 root tick).

## P1 — plain scenes (coast, held forward L8)

err ≤ term at every sampled read (the stored word is never worse than the term the
shipped readout already pays for), and max(err) ≤ 10⁻³ doll units on both flights
(invisible at the gather's quantum, consistent with 7b86's absolute bound).

## P2 — the dive (held reverse L15)

The term grows (the tide near the dominant secondary is no longer invisible): max(term)
≥ 10⁻² doll units. Two outcomes, both informative:

- if max(err) ≤ max(term) AND Δa/a stays ≤ 1: the word holds even on the dive — the
  deletion is safe everywhere measured;
- if Δa/a > 1 on a non-trivial share of reads (my guess: 0.1–5%, concentrated at the
  smallest r / highest β): the word misleads exactly where the term becomes visible —
  the hard case the lens must name; there the readout keeps a live evaluation (or the
  law keeps short windows), everywhere else the word suffices.

I predict the second outcome: the field turns within one window on the dive (the law's
own cadence coarsens there, 174d's checker2: ~2³² ticks), so a stale word cannot
represent it.

## P3 — the light window (the news consumer, plane scenes only)

Δa across the light window to the dominant secondary ≤ 10⁻⁶ relative on plane scenes
(weak field, β ≪ 1): the plane cannot bite the news consumer — the strong-field verdict
stays with 7ab4's standalone float probe (1.4×10⁻² at r = 20 M). This bounds my census's
domain, not the news claim.

## P4 — the write price (code fact, not a measurement)

Zero extra field evaluations: the kick at step.rs:669–671 already computes `f.accel` at
the event and keeps only its quantized impulse (`dv = scale2(f.accel, w)` then
`quantize`). The word's write is one store of a value already in hand. Verified by
reading the code; the census adds no write cost.
