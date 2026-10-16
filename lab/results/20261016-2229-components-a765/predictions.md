# Predictions (written before the decisive run)

Population: the fired kicks of the shipped kick-bench (plane scene, seed 1, ~4–8 s), the
same resolver `step::process` serves. Instrument: stage timings inside
`Rebinding::from_state` + `bind_in` behind `ES_FLOOR_AUDIT`, plus a floor prototype of
`fit_key` (closed-form prefix + Newton-from-seed for the turning root, no 128-step
bisection, no root_witness) run side by side on the same states.

Not tuned on: this is the first execution of the instrument. Held-out arms (checker):
seeds 7 and 42, rtf 100 and 300.

1. **fit_key is a minority of the rebind; the compile dominates at the plane's keys.**
   Predicted shares of `bind_in`: compile 40–70%, fit_key 10–30%, phase placement +
   residual readout 15–35%. (5ade's belt wave says fit 41%; c4d3 says the compile alone
   is 4.4 µs at belt keys — the plane mix should sit near these.)
2. **The 128-iteration bisection is most of fit_key.** The closed-form prefix of
   fit_key (lapse, vr, vt, kinetic, den, angular, l2, q, alpha — ~20 Scalar ops) should
   be ≤ 25% of fit_key; the root search (bisection + root_witness) ≥ 60%.
3. **The prototype's Newton (≤ 8 iterations from the same seeds the bisection uses)
   reproduces the shipped 48-bit key word on ≥ 99% of the population**, because the
   shipped root is the exact-rounded root and Newton converges quadratically from the
   critical-point seed; disagreements concentrate where the true root sits within a few
   ulps of a 48-bit word boundary. Predicted agreement ≥ 99%, mismatch rate per rebind
   10⁻³–10⁻², and zero mismatches that move the key by more than one word.
4. **At the law's own key tolerance (2⁻²⁰ relative, binding.rs line 281's acceptance),
   the rebind keys repeat**: distinct exact keys ≈ rebinds (the 0% memo record), but
   distinct 2⁻²⁰-quantized keys ≪ rebinds (prediction: < 50% of rebinds; the 12+12-bit
   quantized memo hit 98% on this same bench). This would say the exact key carries
   ~28 bits the law itself does not bind, which is why the exact memo never hits.
5. **The exact BigInt path (`inverse::fit`) fires on < 1% of fired kicks** (it exists
   for near-circular and near-separatrix states; the plane's kicks are neither).
6. **Floor arithmetic.** Summing the recorded floors (Carlson φ 129 ns/readout channel,
   all-three ≤ 2.9 µs per compile, de99/c4d3) with the measured fit-key floor gives a
   kick floor of 1.5–5 µs on this representation, against the shipped 34.8 µs (this
   box's anchor) — a gap of ~10–20×, not ~1800× (b063's 42–56 ns) and not ~1.3×
   (1e74's 26 µs machinery residue).

Kill criteria for my own claim: if the bisection is < 30% of fit_key, claim 2 dies; if
the prototype agrees on < 95% of keys, claim 3 dies as stated (the deletion is then a
law change, to be reported as such); if the shares in 1 are outside the ranges, the
"compile dominates" reading dies and the floor table is re-weighted.
