# Predictions (written before the decisive bench run)

Question: what does a belt first-kick promotion cost when the readout is the closed
(Carlson) form, scalar and batched, against the shipped compile — kick-jet open
direction 4 ("price the batched form for the belt's first-kick wave, 10^7 promotions
at ~30 µs today"), never measured.

Cases I have NOT tuned on (the bench is written before any timing run):

1. **Exactness vs the shipped walk** (belt domain: p ∈ [1.2, 3) AU-scale root units,
   e Rayleigh-0.07 re-drawn at 0.4, plus a wider grid to e = 0.99, p down to 1e6):
   my closed channels (advance, t, τ) at the shipped knots agree to < 1e-8 relative
   on the belt mix. At the far corners (e ≥ 0.9) I expect ≤ 1e-6 (cd6e saw 4.5e-6 at
   the weak-field corner in advance). If any belt point exceeds 1e-6, the derivation
   is wrong and the run reports the failure — that is the kill rule for the whole run.
2. **Shipped compile at true belt keys** (q ≈ 3–8×10⁻⁹, the weak branch): 10–40 µs
   per promotion (a669's wave CPU ~30 µs/kick is the record's anchor; the weak
   branch was not what cd6e's 5–256 µs grid priced).
3. **Closed scalar, cold, lean Newton** (1 t-eval/iter, linear start): 3–12 µs at the
   belt mix (cd6e's lean port: 7.9–18.6 µs across e ≤ 0.99; belt e ≤ 0.4 sits low).
4. **Batched (4-wide f64, masked Carlson loops)**: ≥ 2.5× over scalar. **Kill rule:**
   if < 2×, the vectorization does not survive the duplication loops' divergence and
   the "batched route" is dead — report that, do not tune the width to rescue it.
5. **Newton iterations** (linear start, belt mix): median ≤ 6, worst ≤ 14. If the
   worst exceeds ~20 the start is bad and the scalar number is start-dominated.
6. Composition (derived, not a measurement): at ~1–4 µs batched, the first wave at
   10⁶ bodies is ~1–4 s of CPU against the drain's seconds-scale budget today.

Not predicted (checked, not bet): belt amortization (~1 readout per compile — the
wave mints one compile per kick, a669's 1.00), so the closed form's value on the belt
is the compile deletion itself, not read parity.
