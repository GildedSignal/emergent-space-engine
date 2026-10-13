# Dossier — 20261013-0350-components-c914

## Claim

The kick's exact recompile is already at its **wide-division hardware floor on x86-64** —
neither the hardware 128/64 `div` instruction (1.04×) nor an exact multiply-only Newton
reciprocal (1.05×, 0 mismatches on the operand domain) beats the compiler's soft routine —
and divisions own only 20–35% of the compile's wall, so the record's open direction 1
("cheapen the exact recompile" via cheaper divisions) is **bounded at ~1.4× end-to-end**;
the residual ~500× idiot index against the 42–56 ns information floor is owned by the
law's panel count (~52 panels/cycle at plane e) and the bit-exact per-node arithmetic
(~250 ns/node measured), not by implementation waste.

## Bottleneck

The board's live question `kick-jet`: "what is the cheapest exact kick on the shipped
representation". The standing attribution (061f, pending: "the walk's arithmetic owns it,
~900 i128-division-equivalents at 30.9 ns each") implies the division is THE lever. This
run measures the split and the division floor directly. Expected gain of the named attack:
≤1.4× (not 10×). What it deletes: the open direction's division branch, redirecting the
lab to panel count (a law change) or to accepting the kick's cost.

## Evidence

All numbers from `cargo run --release -p emergent-space --example div_bench` on the shared
Linux/x86 runner (i7-4790-class), single thread, load recorded in the probe output;
commands in `regen.sh`, raw outputs frozen in `probe-*.txt`.

1. **Division floor** (quotient-chained operands, fast_quad shapes: dividend < 2^127,
   divisor ∈ [2^20, 2^62], high limb < divisor):
   - soft `u128 / u128`: **30.2 ns**; `i128 / i128`: **35.0 ns** (matches 061f's 30.9 ns);
   - x86 `divq` via inline asm, exact (0 mismatches): **31.4 ns = 1.04×**;
   - exact multiply-only Newton reciprocal (f64 seed from above, 3 integer iterations,
     exact ceil-pin, one final correction; 0 mismatches on 4,096 random + 8 of 9
     adversarial pairs — the one miss is d = 3, outside the divisor domain): **31.6 ns =
     1.05×**. The prototype is in `crates/space/examples/div_bench.rs` (`div_newton`).
   Two measurement traps found and fixed on the record: LLVM unrolls + constant-folds
   index-predictable division loops (a naive harness reports 0.6 ns), and quotient-chaining
   defeats it.
2. **Interior split** of `Orbit::compile`, env-gated stand-ins in `fast_quad`
   (`ES_DIV_HACK`/`ES_SQRT_HACK`/`ES_COS_HACK`, min-of-3 medians, shared box):
   - tuned grid (225 plane-like keys, e ≤ 0.99, 25 octaves; 198 compile, 10,234 panels):
     baseline median 45.8 µs → div hack 31.2 (**33.6%**), cos hack 37.4 (20.3%),
     sqrt hack 41.5 (11.6%), all three 20.5 (**56.4%**);
   - held-out grid (seeded uniform e ∈ [1/16, 0.985], random octave/mantissa; 195
     compile, 6,440 panels): baseline 27.1 µs → div 21.7 (19.8%), cos 23.8 (12.0%),
     sqrt 25.4 (6.4%), all three 15.6 (42.6%);
   - direct expression replacement (no branch, single runs, tuned): div 34.6%, cos 40.2%,
     sqrt 13.6% — the cos share is measurement-sensitive (20–40%); divisions are 20–35%
     under every method.
   Consequence: divisions ≈ 33% of the compile ≈ 14–19% of a made-kick (compile 49–62%
   of bind, bind 84.6% of kick, per the record). **Even free divisions cap the kick win at
   ~1.2×.** And 44–58% of the walk is none of the three named ingredients (products,
   Scalar normalization, knot accumulation, panel scaffolding).
3. **Per-node cost**: 264 ns/node (tuned), 244 ns/node (heldout) — 4 wide divisions
   (~120 ns) + cos polynomial + isqrt + ~20 multiplies. Flat-ish across grids.
4. **Identity** (the probe changes no shipped bits): compile checksums identical across
   every run and the unpatched tree — tuned `133c7636a7f1f4cacd3bf1a43e92b57c`, held-out
   `0dcef556a4b9d7c5a5114b4cb6e6c275`; `cargo test --release -p emergent-space` 63/63
   (quadrature exact-value tests included). The env-gated branches are timing-only
   (default path byte-identical arithmetic).

## Predictions

Written before the decisive runs (`predictions.md`). Held: hardware-vs-soft within 15%
(1.04×); Newton exact on the domain; identity (checksums + suite). Partially held: the
split ordering — divisions first on the held-out grid and under the env-gated probe, cos
first under direct replacement on the tuned grid (the cos share is method-sensitive,
12–40%); per-node cost flat but at 244–264 ns, above the predicted 110–200 ns band.
Failed: Newton's speed (predicted 8–18 ns, measured 31.6 ns — no win). The headline claim
never depended on Newton being fast; if anything the failure is the result.

## What would make it wrong

- The M1 (aarch64) has no 128/64 `div`; if its soft `__udivti3` is much worse than x86's,
  a multiply-only reciprocal could win there — the integrator's re-measure decides. The
  Newton prototype ships in the example for exactly that.
- A division variant materially faster than 2× would revive the lever; none was found
  among {soft, hardware divq, exact Newton reciprocal}.
- The split is measured on compile grids, not on a full settle's kick stream (leaver
  `Passage::compile` paths are under-sampled); shares could shift, the floor result
  cannot (it is operand-shape-local).

Cost of adoption: nothing to adopt — this is a bounded-direction result; the probe
(`div_bench` example + env gates) is the instrument, ~200 lines, no shipped-path change.
Fit with PRINCIPLES: "Less is more. The cheapest compute is compute not done" — the
measurement says the division compute cannot be cheapened, so the next deletion must be
panels (the law's π/4 quantum), not arithmetic; "Measure before claiming" — 061f's
count-based attribution is now measured; "a failed experiment kills that configuration,
never the method" — the configuration (division micro-optimization on x86) is killed, the
method (floor → idiot index → smallest falsifying test) is not.

## The lens

First principles, one component: the kick's recompile. Requirement: law.md:36 (exact
recompile so errors never compound). Floor: 4 wide divisions + one cos polynomial + one
isqrt per node, ~52 panels/cycle — ~250 ns/node measured, against the 42–56 ns/kick
information floor. Idiot index ~600–1,800×, and this run shows ~1.4× of it is reachable
by arithmetic, the rest is law-owned. What the lens may have missed: the readout path
(`state`, 0.34–0.42 µs tiers) and the leaver `Passage` compile were not re-measured; the
split's second-order overlap (direct shares sum to 89%, all-three removes 56%) means
individual shares are ±10 points, not exact.
