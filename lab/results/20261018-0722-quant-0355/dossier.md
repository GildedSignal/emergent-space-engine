# Dossier — 20261018-0722-quant-0355 (quant lens)

**Claim.** The shape-memo's two open halves are measured on the flown key mix: the
compile is 92.3% shared quadrature (5,451 of 5,906 ns; glue 454 ns), so a class-keyed
shape cache deletes ~5.0 µs of the ~5.9 µs compile at a 0.40 µs hit price — and the
unmeasured exactness question resolves *against* a bit-exact delete but *61× in favour*
of the exact-key form: `from_shape(exact key, class shape)` moves the clock increments
by p50 1.9×10⁻⁶ / p99 1.7×10⁻⁴ relative (period, τ, advance alike), against the shipped
quantized-key arm's p50 1.2×10⁻⁴ — a law change two orders smaller than memo.rs's known
2⁻¹¹ change, at 7% of the compile's cost per hit.

**Bottleneck.** The kick's compile term (read-stream's direction 2; the fit is 49% of
the bind stage sum, d399). The prize: ~85% of the compile per hit on this box (5.0 of
5.9 µs), i.e. the largest single deletion left inside the fit. What it deletes: the
per-fit quadrature walk, replaced by one 17-bit-class lookup + glue. It does NOT move
the cadence or the readout streams.

**Evidence** (Linux/x86 shared runner, 8 vCPU, 15 GB, quiet; orders of magnitude only;
compile here 5.9 µs vs 12.33 µs on 5eb2's box — same mix, ~2× box):
- Keys captured from `ladder_digest "N=3000 coast through"` (588d's own control case)
  at `Orbit::compile` entry, 32 B/key, 148,996 compiles, 0 errors. **Instrument
  digest-neutral: `d2632de90255f5c10de9fd7372a3790d`, kicks 34537 — bit-identical
  pristine vs capture-on** (the record's own digest).
- Census: 37,245 distinct exact keys; 37,230 distinct ShapeKeys (exact repeat rate on
  the unique stream 4×10⁻⁴ — reproduces 588d's "exact dead"); 1,163 shape classes;
  class hit rate 0.9922 on the stream / **0.9688 on the unique stream** (the stream
  rate inherits ladder_digest's known 4-schedule re-flight artifact; 588d's 0.978–0.992
  single-flight rates sit between). Exact `ShapeMemo` hits on the replayed stream:
  111,766 — that is the artifact 588d flagged, not flight structure.
- Split (interleaved, median of 3, second execution within 1%): compile 5,906 ns =
  `OrbitShape::bound` 5,451 (92.3%) + glue 454 (7.7%). Hit prices: exact-key+class-shape
  (lookup + relaxed `from_shape`) 419 ns; shipped `QuantizedMemo::get` 516 ns.
- Exactness (every key, class representative = first-seen): arm C period p50 1.949e-6,
  p99 1.746e-4, max 3.063e-4; τ p50 1.949e-6; advance p50 1.083e-6. Arm B (shipped
  quantized key): period p50 1.197e-4, p99 5.608e-4. **C is 61× better at p50.**
  Measured/predicted = 0.53 against the class k-quantum law |dlnP/dlnk| = 3k/(2k−1)
  (pred p50 3.7e-6, p99 3.2e-4) — the mechanism is the class's k quantum, coefficient
  about half the Newtonian sensitivity (the weak Taylor shape at q=0).
-  Controls, both sides: identity path bit-exact (0/500 mismatches: `from_shape(own
  shape)` ≡ `compile` on period/τ/advance bits); wrong-class negative p50 2.1×10⁻³
  (run-varying 1.6–2.1×10⁻³), max run-varying 1.0–25 (the wrong-class representative is
  picked from a HashMap, so which class serves as "wrong" differs per run) — the
  instrument sees wrongness at ~1000× C's p50 either way.

**Predictions.** Written before the run (`predictions.md`). P1 held (bound ≥ 70%:
measured 92.3%). **P2 upset at the bar, not in the letter: predicted p50 1–4×10⁻⁴
(law change, kill as a delete); measured 1.9×10⁻⁶ — above the pre-registered
"lives as an exact delete" bar of 1×10⁻⁶, but 50–100× under the prediction**, because
the sensitivity coefficient is ~0.5× the Newtonian 3k/(2k−1) and the representative's
|Δk| averages half a quantum. P3 held (C ≤ 4× better than B: measured 61× — outside
my predicted band, same direction). P4 held (hit 7.1% of compile ≤ 40%). P5 held
(classes 1,163 in [1,161–1,491]; exact dead reproduced).

**What would make it wrong.** The exactness census measures the *increments*
(period, proper period, advance) — the clock half; position readouts interpolate the
representative's knots and were **not** measured (they inherit the shape difference
first-order; the binding's residual absorbs part at bind time — unmeasured). The
representative is first-seen, not class-centre (centre would halve the error; an
adoption would choose it). Single flight case, one seed, coast-through-the-wave; the
class count on a stirred/driven belt is 588d's own unmeasured corner. Timings are
shared-box x86, ±few % across executions. If the readout error is the binding
constraint, the 61× clock advantage may not survive at the state level — one more
census (readout error at N phases) before any adoption.

**Cost of adoption.** A law change (bits move: p50 2×10⁻⁶ clock) — the same decision
class as memo.rs's 2⁻¹¹ quantized key, now 61× cheaper in error and cheaper per hit
(0.42 vs 0.52 µs), deleting ~85% of the compile term instead of re-keying it. Needs a
B-gate-class legality flight (not the lab's call). The wiring is `QuantizedMemo` with
the exact input key passed to `from_shape` (one-line change in `QuantizedMemo::get`:
`Orbit::from_shape(input, shape)` instead of the decoded key) plus the identity check
scoped to the exact path.

**Fit with PRINCIPLES.** "Compute only surprises … Nothing is evolved that can be
derived when looked at" (#3): 1,163 classes carry 149k compiles — the quadrature is
the derived part. "A fix signals the wrong representation" (#19): the memo does not
fix the compile, it deletes its repetition; the compile itself remains the floor
work. "Rough first, refine when a certificate could break" (#21): the error is
measured before the adoption, not after. "Behaviour and error type over error size"
(#2): the verdict is "law change, 61× smaller", not "2×10⁻⁶ is small".

**The lens (what it may have missed).** Quant prices the edge and the tail; it does
not price legality — the p99 1.7×10⁻⁴ clock tail is 61× better at p50 but only 3.2×
better at p99, and tails decide here. The capture sits at `Orbit::compile` (every
compile the flight makes, from_state and birth replans together), not per call site;
a site-split census could shift the mix weights, not the split or the exactness law.

## Reproduction

`regen.sh` (≈4 min): builds, runs the pristine digest control, the capture run
(declares DIGEST_NEUTRAL), and the bench. Patch = `work/patch.diff`: `orbit.rs`
(capture at `compile` entry behind `ES_KEYCAP`; `PROBE_RELAXED` gate on the
`from_shape` identity check; three `#[doc(hidden)]` probes: `probe_bound`,
`probe_from_shape`, `Orbit::probe_class_bits`) and `examples/compmemo.rs`. Shipped
paths byte-identical unless the env var/flag is set (digest control above).
