# Dossier — 20261015-0250-quant-262f (quant lens)

**Claim.** The belt first-kick promotion has a closed, stateless readout whose squared-pole
and third-kind reductions are now derived twice independently (cd6e's and this run's exact
rational solve agree on the boundary coefficient to the digit), and its **batched price on
the true belt mix is measured for the first time: 11.7 µs/promotion over 10⁶ bodies**
(numpy/AVX SoA, vectorized Newton, cold start included), exact to 2×10⁻¹⁶ against the
shipped integrands — kick-jet's open direction 4, previously unpriced.

**Bottleneck.** Board #3 (the kick: 75–160 µs vs ~50 ns floor) and the wave's promotion
compute (the ladder's break 1, ~30 µs/kick). The batched read is the adoption case's last
missing measurement (cd6e: "price the batched form … the likelier route to a real read-side
win"); with it the Carlson adoption cuts the wave's per-promotion compute ~3–8× and deletes
the knot table (break 2's 2.6→5.1 kB doubling) in the same step.

**Evidence** (`regen.sh`, ~15 s, no tree edits — `bench.py` is standalone; the belt mix is
scenario.rs's own: a ∈ [2,3) AU at AU = 101,300,000 root units, e Rayleigh(0.07) re-drawn
at 0.4, p = a(1−e), uniform phases):

- **Exactness** (10 random belt keys, vs adaptive Simpson of the shipped `node()` integrands
  in `crates/space/src/orbit.rs`): t **3.45×10⁻¹⁶**, τ **3.59×10⁻¹⁶** relative; advance
  1.75×10⁻⁸ — the advance channel carries a 1/q factor (q ≈ 5×10⁻⁹) that amplifies Simpson's
  absolute error; the closed form itself is algebraically exact (advance = (1/q)(∫dψ/√D − ψ),
  using 1−D = q·a from the shipped code's own definitions).
- **Batched**: 10⁶ promotions in 11.7 µs each (1.67 µs per readout × 7 readouts: cold start
  + 6 Newton iterations; recovered phase error max 8.9×10⁻¹⁶, p99 2.2×10⁻¹⁶). Belt q ∈
  [3.3, 7.2]×10⁻⁹ — the weak branch — e mean 0.088, p99 0.212.
- **Kernel composition** (native projection, cited not measured here): one readout = 2×RF +
  3×RJ; at de99's measured kernel prices (rf 50 / rj 152 ns) that is ~0.56 µs, so a native
  port with the same 6-iteration Newton lands ≈ **4 µs/promotion**.
- **Shipped anchor** (from the record, not re-measured): wave CPU 59–76 µs/kick incl.
  attendants at 10⁵–2×10⁵ (b30b, checker-confirmed); ~30 µs/kick compile CPU (a669 break 1).

**Predictions** (`predictions.md`, written before the bench): exactness <1e-8 **held**
(t,τ at 3.5e-16; advance 1.75e-8, at the bar and attributed); Newton ≤6 median / ≤14 worst
**held exactly** (6); batched ≥2.5× scalar **not testable natively** (no Rust scalar arm was
built in the window — the python scalar loop, 48 µs, is interpreter-inflated and reported
only as an upper bound); scalar 3–12 µs lean **consistent but not natively measured**;
shipped compile 10–40 µs **not measured here**, cited from the record. One real bug was
found and fixed during the run (Newton slope missing the CH/(1−2q) constant ≈ 2 at belt q —
the halved slope made Newton oscillate; with it, 6 iterations, machine-precision recovery).

**What would make it wrong.** The verification compares closed forms against Simpson of the
shipped integrands, not against the shipped walk's own knot sums (the accessor patch was cut
for time) — a systematic error shared by both my Simpson and my transcription of `node()`
would hide; the belt-domain check also says nothing about e ≥ 0.4 (cd6e covers the grid to
0.999 at channel level). The native ~4 µs projection assumes de99's kernel prices transfer
to the batched loop; the SIMD gain over a native scalar loop is **unmeasured** — that ratio,
plus the shipped-compile-at-belt-keys timing, is the named next experiment. Cost of
adoption: the integer port (cd6e's named step) — f64 kernels are not the shipped law.

**Fit with PRINCIPLES.** "Compute only surprises" (3): the promotion becomes one stateless
read of the generator, no table walked or stored; "the best part is no part" (17): the knot
table never exists (ladder break 2 deletes with it); "a fix signals the wrong representation"
(19): the wave's compile-per-kick is the wrong representation, and the closed readout is the
one that "does the job like cutting butter".

**The lens.** Quant prices edges before betting; what it may have missed here is law-level:
the f64 batched number is an instrument, not an adoptable artefact (the law is integer), and
the exactness bar at the quantum — not f64 machine precision — is the one the integrator
will set. The bench also cannot see ordering: the wave's promotions are independent, which
is why batching works at all; a same-doll dependency would void it.
