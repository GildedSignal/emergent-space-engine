# The two-word acceleration: the readout's per-read field evaluation is deletable, for free

## Claim

The (a, ȧ) two-word store passes **every frozen readout gate** (`tests/motion.rs`, worst
readout/map ratio **1.11× against the 3× bar** where the one-word read 356×), and its write
costs **zero extra evaluations of the sources**: the kick's own evaluation is the word, and the
previous kick's word is the derivative's other point.

## Bottleneck

The readout component (`observe::partial`): every read between kicks evaluates the sources'
field once (`force::field` + `ctx.secondaries` + a tube decode at the window mid). 549f priced
that evaluation at 1.45× of the gather (25.9→17.1 µs per emitter scratch) and ~500 reads amortize
per window; f2b7 killed every constant-word replacement on the frozen gates (jump 3.85–5.07e-2
against 1e-4; map-ratio 356× against 3×) and wrote the two-word off as "a real law change, not a
wiring" because the kick does not compute the field's derivative. This run closes the page's
open direction 1: the derivative's other point already exists — the previous kick's stored
evaluation — so the write is a wiring, and the gates cannot tell the arm from the shipped
readout. Expected gain: the measured 1.45× on the view's gather (549f/f2b7's number, inherited),
plus one tube decode per read deleted on top (the mid read `base.cartesian(mid)`), at 4×f64 per
kick record — a probe's width; 549f's shipped one-word form was 2×i64 + i16.

## Evidence

All numbers regenerate by `regen.sh` (~3 min, Linux x86; orders of magnitude only per the lab
rules). The arm: `A_WORD=2` env flag; `Kick.word: Option<([f64;2],[f64;2])>` written in
`kick_clock` (this kick's `f.accel` at its own tick — the middle of the step a read completes —
and ȧ = (a − a_prev)/(dt·2^clock_exp) against the previous binding's word), read in
`observe::partial` (Taylor moments ∫a and ∫∫a around the word's time, fallback to the shipped
evaluation where no word exists). Patch: `work/patch.diff` (+52/−12 on `bind.rs`, `step.rs`,
`observe.rs`).

- **Gate `the_readout_between_kicks_reads_the_boundarys_error`** (12 ships, 100 periods; bar
  3× per ship): worst ratio **1.11×** (ship 4; the shipped per-read arm prints the same 1.11×
  worst — both quadratures sit under the boundary's own error). Per-ship ratios 0.98–1.11×.
- **Gate `the_readout_error_falls_as_the_step_squared`** (2⁶→2⁸ kicks per period; bar ≥ 8×
  where the map falls ≥ 8×): the arm falls **15.9–18.3×** on all 6 judged ships (map output
  14.9–16.9×; raw-tube control 1.8–12.8×) — second order, as constructed.
- **Gate `the_readout_between_kicks_is_bounded`**: worst absolute **5.29e-6** against 2e-3.
- **Gate `the_readout_at_a_boundary_is_the_state_bit_for_bit_and_between_boundaries_it_does_not_jump`**:
  passes — the gate whose 1e-4 bar the one-word failed at 3.85–5.07e-2. The slope is continuous
  across boundaries where a constant word jumps; that is the whole mechanism.
- **Controls, both sides:** arm OFF prints bit-identical gate figures (the off path is the shipped code; `word` stays `None`); digests and outcomes with the arm ON unchanged (replay 2, memo 1, clock 4, origin 3 tests green — the word rides kick records, which digests never hash, 549f's finding, re-verified here); burns and flight with the arm ON green (p2_burn_out 3 and
throttle 8 tests passed; t1_burn's single test is `#[ignore]`d as shipped — the frozen T1 gate) —
the clock re-plans under thrust and the word chain re-arms through the fallback windows.

## Predictions

`predictions.md` was written before the run. Held: gates 1–3 pass (predicted 1.0–2.0, measured
1.11; predicted ≥ 8× fall, measured 15.9–18.3×; predicted ≤ 5e-4, measured 5.29e-6); the weak
margin was predicted on the close-pass ships and did not materialize (ship 0's ratio is 0.98×
— the stale-by-one-step slope costs nothing measurable at these steps); digests predicted
unchanged, verified. Held as disclosure, not prediction: the fallback windows (first window
per clock (re)plan, handoffs, flushes, silent sub-quantum kicks) read through the shipped
evaluation.

## What would make it wrong

The gates fly unthrusting ships at ≥ 2⁶ kicks per period in the star's doll. The arm is
untested where (a) the field's second derivative is large *relative to the step* at very coarse
steps or deep in a close pass (the backward difference is stale by one full step — a scene with
steps shrinking faster than the field changes could expose it); (b) **thrust**: a held burn
re-plans the clock at the thrust-limited step, so windows between flushes carry a
one-kick-stale slope, and no frozen gate reads readout continuity under thrust; (c) the
strong-field pole (r = 20 M), which no built scene reaches (the existing scene never
clock-steps — checker2's finding, a scene defect). Adoption cost: one merge of the flag-on
path (the flag off is a no-op), the width tightened from 4×f64 to the record's quanta, and a
readout gate under thrust before the flag defaults on. Fit with PRINCIPLES: "Nothing is evolved
that can be derived when looked at (clocks, redshift, views)" — the field between kicks is
derivable from two numbers the kicks already computed; the read now derives it instead of
re-evaluating the sources ("compute only surprises").

## The lens

The components lens priced one component (the readout's field evaluation) against its floor
(zero extra source evaluations: the information already exists on the kick records) and found
the gap closable by a wiring. What the lens may have missed: the cost side is inherited
(549f's 1.45× measurement, not re-measured on this arm, which also deletes the mid tube
decode); and a local optimum can move cost to a neighbour — the word's own bytes at 10⁹ (4×f64
now; the quantized width question is memory-h-live's, untouched here).
