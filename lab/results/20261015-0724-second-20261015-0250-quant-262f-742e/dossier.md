# Dossier — 20261015-0724-second-20261015-0250-quant-262f-742e (second author on 20261015-0250-quant-262f)

**Claim.** The checker's one experiment, done natively on one box, **refutes the
Carlson adoption's belt-frame magnitude**: the shipped compile at true belt keys
costs **5.2 µs/promotion** (`Orbit::compile`, weak branch, 7 knots p50) — not the
record's ~30 µs/kick anchor — so the best native batched readout (**2.6 µs** over
10⁷ promotions, exact, per-body setup included) cuts the promotion's compile by
**2.0×, not ≥6×**; and the batched/native-scalar ratio is **1.38×, failing 262f's
pre-registered ≥2× kill rule** (prediction #4: "if < 2× … the batched route is
dead"). What survives of the adoption case: the 2× belt compute cut, the knot-table
deletion, and the e ≥ 0.99 tail where the compile really is expensive (cd6e's
76 µs p50 there stands).

**Bottleneck.** Board #3 (the kick). 262f priced the batched promotion at 11.7 µs
numpy and projected ≈4 µs native against a cited ~30 µs compile. This run makes all
three measurements native on one instrument and finds the premise 6× off at belt
keys: the compile is cheap exactly where the wave's promotions are. The lever moves
from "batch the readout" to "the e ≥ 0.99 tail and the memory" — and the record's
compile anchor needs re-measuring per branch.

**Evidence** (`regen.sh`, ~2 min + build; `native/` is a standalone crate that
path-depends on the shipped `crates/space` — no tree edits; belt keys generated the
shipped way, scenario.rs `ladder_ship` belt lane, a ∈ [2,3) AU at Q8, e
Rayleigh(0.07) re-drawn at 0.4 in Q48, q = 1/p ∈ [3.3, 7.2]×10⁻⁹; same bodies feed
every arm; all quoted numbers are medians of 3 reps with every repeat printed in
`bench-output.txt`; the regen run on a quieter box reads 4.89 / 3.54 / 4.39 /
2.48 µs for arms (a)–(d) — same orders, same ratios: compile/batch 1.97×,
batch/scalar 1.40×):

- **Value** (all regenerable; the checks 262f skipped, run by construction before
  any timing was trusted):
  - scalar closed vs adaptive Simpson of the shipped `node()` integrands (belt mix,
    200 keys): t **9.2×10⁻¹⁶**, τ **7.3×10⁻¹⁶**; advance **4.2×10⁻⁸** — the
    checker-established 1/q-amplified f64 floor (both instruments; algebra exact,
    their 40-dps proof stands — re-confirmed at a strong-q corner here to 3×10⁻⁴¹).
  - SoA batch vs scalar: **bitwise identical**. AVX2 batch vs scalar: t/τ
    **1.0×10⁻¹⁵** (extra duplication rounds in converged lanes + FMA association).
  - Analytic Newton slope vs finite differences: 3.1×10⁻¹⁰ (bar 1e-6) — the slope
    is dt/du = 2·f_t(2u) with **no** CH/(1−2q) factor, confirming the mechanics of
    262f's factor-2 slip (their batched t and slope were both 2×, self-consistent).
  - Newton at belt: median 4, worst 6 (scalar per-body early exit; batch pays 6
    passes for all); recovered-u 8.9×10⁻¹⁶ / 1.1–1.3×10⁻¹⁵ max across arms.
  - **Wider grid** (180 corners, e 0.001–0.999 × p 7–10⁸ × u → π/2−10⁻³): t/τ
    **4.6×10⁻¹³**, adv 2.4×10⁻⁸ — the promise 262f dropped, now run and passing its
    own 1e-6 kill bar; Newton worst 17 iterations at corners (belt-scoped as claimed).
- **Timings** (i7-4790, AVX2, loadavg ~2.8, 3 reps each, medians; x86 orders of
  magnitude per the lab rule):
  - (a) shipped `Orbit::compile` at belt keys: **5.18 µs** (reps 5.17–5.20; knots
    p50 7, p99 11, max 16; 0 errors/10k) — the weak branch (`compactness` ZERO →
    `weak_quad` panels) is the cheap end of cd6e's 5.2–255.8 µs grid, not ~30 µs.
  - (b) native scalar promotion (GE setup + cold start + Newton + final read):
    **3.57 µs**, worst 6 iterations.
  - (c) native SoA batch, setup included: **4.66 µs** at 10⁶, 4.88 at 10⁷ — the
    max-lane 6-pass tax plus streaming makes plain batching *slower* than the
    scalar loop that exits per body at median 4.
  - (d) 4-wide AVX2 masked-Carlson batch (outlier |En| lanes serviced by the same
    scalar closed form; per-lane scalar sin/cos, disclosed): **2.58 µs** at 10⁶,
    **2.71 at 10⁷**.
- **Ratios**: compile/best-batch **2.01×**; batch/scalar **1.38×** (kernel-level
  SoA→AVX2 1.81×) — both under 262f's pre-registered 2× bars.

**Predictions** (`predictions.md`, written before the run): kernels and value bars
held; scalar 2.5–5.5 µs held (3.57); AVX2 predicted 0.9–2.0, measured 2.6 (miss,
disclosed); **compile predicted 8–30 µs — wrong 6× low-side** (the run's central
surprise, and the refutation); **kill rule predicted to clear 2× — it failed**
(1.38×). Reported as they fell. Two transcription bugs appeared in this fresh port
and were caught by the by-construction value checks before any timing was trusted:
three sign errors in the AVX2 Taylor tails (visible only at wide-argument kernels)
and an `rc1p` log-branch bug (`(1+arg).ln_1p()` for Boost's `log1p(arg)`,
visible only at strong-q corners, e.g. t off by 1e-3 at e=0.5/p=7 until mpmath at
40 dps isolated it) — both classes invisible to a belt-only spot check, both the
direct answer to why 262f's missing batched-value check mattered.

**What would make it wrong.** Single shared box, x86: orders of magnitude only —
the integrator re-measures on the M1 (its i128 arithmetic and memory systems
differ). The compile timed is `Orbit::compile` proper; the wave's kick machinery
(forces, bookkeeping, allocator) is not in either arm, so the **total-kick** cut of
the adoption is *smaller* than the 2.0× compile-vs-readout figure. The a669 ~30 µs
and b30b 59–76 µs/kick anchors measured more than the compile proper on their
mixes; this run does not contradict them, it bounds the compile component at belt
keys. The f64 closed readout remains an instrument — adoption still requires the
integer port (unchanged). Newton is belt-scoped (17 iterations at the e=0.999
corner).

**Cost of adoption / fit with PRINCIPLES.** The readout deletes the knot table
(≈0.6–1.4 KB per belt shape at 7–16 knots) and the compile walk, cutting the belt
promotion's compute 2.0×; it is one law change away (integer port). "A fix signals
the wrong representation" (19) cuts both ways here: the closed read is the right
representation for the e ≥ 0.99 tail and for memory, but at belt e the shipped
compile was never the 30 µs wall the case assumed — "measure before claiming" (10)
is the sentence this run earns.

**The lens.** The second author verifies; what it may have missed is law-level
again: no memo-hit structure was simulated (at 44-bit quantized keys the first wave
is ~all cold compiles, but a warmed belt changes arm (a)'s denominator), and the
shipped-compile arm mints keys through `OrbitKey::bound` exactly but times on a
box whose i128 soft-arithmetic flatters no one.
