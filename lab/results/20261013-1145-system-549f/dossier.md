# The acceleration word: one slot, three bottlenecks, priced

## Claim

The three named fixes on three open pages — the view's per-read field evaluation
(7b86), the news version payload's missing total acceleration (7ab4), and the burn
waterfall's generator (174d) — are **one representation change**: store the body's
field acceleration as one word per binding, written for free where every kick already
computes it (`step.rs:669–671`: `f.accel` is evaluated, its impulse quantized, the
acceleration discarded), and read it as `Δx = a·τ²/2`. The staleness census on shipped
code bounds the word's error at 4–5 orders below the term it replaces on plain scenes
and still sub-quantum on the dive; the write costs zero extra field evaluations.

## Bottleneck

Three of the board's live bottlenecks (view cost, gravity-news correctness, frame-cost
smoothness), each currently solved per-consumer. The expected gain: the view's readout
loses the term that is 81% of its cost (51bf) *while keeping the term's accuracy*
(7b86's pure deletion only works where the term is invisible; the word keeps it where
it will be visible — strong-field dolls, the news payload); the news payload gets its
`a` slot (7ab4: the ½aT² thrust-blindness, 1.4×10⁻² at r = 20M); the burn generator
gets its second-order piece (174d's lever names the representation as already holding
the other two pieces). What it deletes: the per-read `force::field` + `ctx.secondaries`
doll-chain walk in `observe::partial` (~35 lines), and the third per-consumer
re-derivation of the same quantity.

## Evidence (all from `regen.sh`, ~15 s: `census.txt`)

Probe: `crates/universe/examples/a_word.rs` (kept in this folder), plane seed 1,
48 members, threads 1, rtf 100, 480 frames (8 s) per flight, sampling every body whose
binding the shipped readout completes with a partial step (`partial`'s own gate: a
clock kick, 0 < τ ≤ 2·len), in the body's doll units (c = 1):

- **Coast and held forward L8** (5,760 reads, 12 clock-stepped haulers; the pooled
  stats are identical because the player's burst carries ~zero gravity content —
  174d's finding — and the burning player rides the *ramp* path, see below):
  the shipped per-read term |a(mid)|·τ²/2: median 5.7×10⁻⁶, p99 1.6×10⁻⁴,
  max 2.0×10⁻⁴; the stale-word error |a(mid) − a(B)|·τ²/2: median 2.8×10⁻¹⁰,
  p99 2.6×10⁻⁹, max 3.0×10⁻⁹. The stale error is Δa/a × the term by construction,
  and Δa/a stays ≤ 3.1×10⁻⁴ (median 3.5×10⁻⁵): zero reads with Δa/a > 1 — the word
  is 4–5 orders safer than the term it replaces at median, 8 orders below the
  gather's 1-unit quantum at max.
- **Held reverse L15 (the dive**; player hands out of Home's doll to the root, ends at
  r = 9.3×10⁷, β = 0.254 — 174d's regime; 6,101 reads, the player now clock-stepped):
  Δa/a p99 1.7×10⁻², max 3.0×10⁻²; stale-word err max 1.0×10⁻⁸ (the player's own
  reads: term max 3.6×10⁻⁷, err max 1.0×10⁻⁸). **Still sub-quantum by 7+ orders**:
  the word holds on the dive at readout windows — the windows shorten faster than the
  field grows.
- **The light window (the news consumer's T)**: Δa/a median 6.3×10⁻⁴, max 1.9×10⁻³ on
  coast; **max 4.0×10⁻¹ on the dive** (200× the coast max, at the handoff): a word
  carried across a *light window* goes 10⁻³-stale on plain scenes and ~40%-stale during
  the dive — the plane's own signal that the news payload's word must refresh at
  rebinds, not ride a light window.
- **The write is free (code fact)**: `step.rs:669–671` — every kick computes
  `f = force::field(&secs, x)`, uses `f.potential` and `f.accel` for the impulse,
  and discards them; `observe.rs:145` then re-derives the same doll-chain field per
  read (`ctx.secondaries` walks every source's tube). The word's write is one store
  of a value already in hand; the census adds no field evaluation.

**A structural finding the census forced:** the shipped representation already has the
stored-word path — `credit` (the ramp) applies the *stored* kick `dv` between events,
and the burning player rides it (no field evaluation at all); `partial` re-derives the
field for clock-stepped bodies. Two mechanisms, secretly one (complete the tube to
second order between events), one already storing its word, one re-deriving per read.

## Predictions (`predictions.md`)

P1 held (err ≤ term, max err 3×10⁻⁹ ≪ 10⁻³). P2 half-failed, the interesting way: the
dive's term stays ≤ 2×10⁻⁴ (my ≥ 10⁻² was wrong: the law's windows shorten faster than
the tide grows) and the predicted Δa/a > 1 break never came (max 3×10⁻²) — **the word
holds on the dive**; the break appears one window longer out (the light window,
Δa/a = 0.4), not at read windows. P3 failed in magnitude (I said ≤ 10⁻⁶; measured
median 6×10⁻⁴, max 0.40): the plane's field words go ~10⁻³-stale across light windows,
not 10⁻⁶ — the "plane cannot bite the news consumer" conclusion survives only through
β_c ≈ 10⁻⁴ (the ΔE argument), not through staleness being negligible. P4 verified.

## What would make it wrong

- **Strong fields, unmeasured here**: the census covers the plane's weak field; at
  r ≲ 20M the term is visible and the word's refresh cadence (the kick rate) must
  shorten with the field — the plane cannot express the scene (e300), so the oracle is
  7ab4's standalone float probe. If the required refresh there approaches one word per
  read, the word buys nothing exactly where the term matters.
- **The thrust half**: the word measured here is gravitational; the news payload needs
  the *total* acceleration (7ab4), i.e. the thrust heading's analytic acceleration
  added at the write — one more add of two values in hand, but unwired.
- **The memory price at 10⁹**: one V2-of-Scalar per binding is ~2× the tube's own
  16 bytes; at the memory floor (62 bits/ship) it must be quantized like `kick.dv`
  already is — the census prices the refresh rate, not the width.

## Cost of adopting, and fit

One store at the kick (0 extra evals), one read rule (2 multiply-adds), ~35 lines
deleted in `observe::partial`, the same word on the news payload and in the burn
generator's three pieces (174d). PRINCIPLES: "we just need to have the right
representation so that math is trivial" (18); "Nothing is evolved that can be derived
when looked at" — here the converse: nothing *re-derived* that the law already computes
(3, 14); "store the generator, not the generated" (6).

## The lens (what it may have made me miss)

A unification priced only where its consumers' windows overlap the plane's expressible
regime. The named hard case is the strong field (above); the unmeasured consumer is
the gather's *multiplicity* — 2.5–3.8 reads/body/frame (7b86's checker) amortizes the
write, but a body read by many consumers between its own kicks serves them all the
same stale word; if any consumer needs the mid-window `a` to better than Δa/a ~ 3×10⁻²
(the dive's p99), it must still pay one live evaluation.
