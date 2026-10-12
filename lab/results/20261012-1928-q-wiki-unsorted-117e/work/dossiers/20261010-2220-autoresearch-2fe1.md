# dossier.md — 20261010-2220-autoresearch-2fe1 (lens: autoresearch)

**Claim.** Replacing std `u64::isqrt` with an f64-seeded, exact-fixup integer square root
(bit-identical by construction) cuts the motion law's orbit-compile cost by **12–13%** and the
per-kick rebind event (`Rebinding::from_state`, the path the plane pays on ~99% of kicks) by
**11–14%**, with every compiled bit unchanged; two further bit-identical micro-rounds (append
n==1 fast path, fit_key poly hoisting) add ~2% each before the loop hits its stop rule.

**Bottleneck.** Board focus line 1: "kicks dominate the engine's cost"; "cheaper events" is the
explicit lever under *Cost at a billion*. The per-kick event is fit + orbit compile + readout +
residual. Measured baseline on this runner: 31.2 µs per compile, 60.0 µs per rebind event.
Component microbench showed the std `u64::isqrt` (software Newton with integer division, 22.3 ns)
called once per quadrature node (≈107 nodes per orbit compile), plus as the seed of the crate's
u128 isqrt (86.8 ns) used by every `Scalar::sqrt`. Order-of-magnitude gain: ~0.1× on the event,
not a new representation — this is a tail-cut on the per-kick cost, not a 10× lever.

**Evidence.** All numbers are medians of 7 timed rounds over 512 deterministic keys
(LCG-seeded), `--release`, shared 8-vCPU Linux runner (orders of magnitude only, per lab rules;
the integrator re-measures on the M1). Reproduce with:

```bash
cargo build --release -p emergent-space --example lab_bench   # bench: lab/results/<run>/lab_bench.rs
for m in compile compile-deep compile-circ rebind; do
  cargo run --release -q -p emergent-space --example lab_bench -- $m 7
done
cargo test --release -q -p emergent-space      # 50/50 green (law)
cargo test --release -q -p emergent-universe   # 54/54 green (consumer, the plane)
```

| mode | baseline ns/event | final ns/event | Δ | checksum |
|---|---|---|---|---|
| compile-main (tuned) | 31,185 | 26,742–26,898 | −14% | 0x2b346ac433041c73 unchanged |
| compile-deep (held out) | 81,608 | 71,687 | −12.2% | 0xfbbe78bcc0532588 unchanged |
| rebind (held out) | 59,962 | 53,277 | −11.1% | 0x855ba4e402a6c53c unchanged |

Loop (`log.md`): R1 kept (−12.6% compile), R2 kept (−1.9%), R3 kept (−2.0% rebind),
R4 (hoist + `ratio_sqrt` rewrite) regressed +2.6% across 3 re-measurements and was reverted.
Stop rule hit: three consecutive rounds <10%.

**Predictions.** `predictions.md` was written before the first change. What held: R1 in the
predicted direction on all modes; deep benefited more than circ; checksums and tests clean
everywhere. What missed: R1's magnitude exceeded the predicted 4–8% band (12.6%, within the
2× suspicion bound — explained: `Scalar::sqrt`/`fit_key` benefit too, not just the quadrature
nodes); the corrected circ band (−4…−8%) was itself a mid-flight correction written before any
change was measured, and circ landed at its edge (−7.6%).

**What would make it wrong.** The fixup loops make `isqrt64` exactly floor(sqrt(x)) for any
seed, so bit-identity is by construction, not by sampling — but the *claim of speed* is
x86-64-specific: on the M1 (or any hardware `sqrtsd`-poor target) the seed may not beat the
integer chain; the integrator must re-measure. If a future Rust std `u64::isqrt` switches to a
hardware seed, the gain collapses and the patch should be deleted (the best part is no part).
The gain is also invisible if per-kick compiles are eliminated by a future cadence/certificate
change — that would be the better world.

**Cost of adoption.** ~25 lines in `crates/space` (`num.rs` `isqrt64` + two call sites,
`orbit.rs` append fast path, `binding.rs` closure hoist), no API change, no new dependency,
all gates bit-identical. One step.

**Fit with PRINCIPLES.** "no it's about what's cheapest to compute" (OC#38): the f64 unit is a
part of the machine already paid for; the fixup keeps integer exactness — floats explore,
integers decide, and here the float only *seeds* an integer that decides the same bits.
"i care about the p95/99" (CL 09-25): this cuts the per-kick event cost uniformly, which is the
allocator's tail feed. Not "less compute" (P1) — the same compute, cheaper arithmetic; honest
about that.

**The lens's blind spot.** Local search found local gains; the structural change that beats
this best configuration is not arithmetic: the per-node cost is ~95 ns of exact wide divisions
(4 per node: g, g1, ratio, rt) that have no bit-identical cheaper form at 62-bit exactness —
the measured `div_word` (20 ns) is no faster than the compiler's `__udivti3` (22 ns), so
hand-rolled Knuth division buys nothing. The real levers remain (a) fewer compile events per
kick (the 94.5%-hit quantized memo is a law change awaiting its gate; exact-key memoing is dead
— 48-bit k never repeats across kicks), or (b) a narrower exact word (32-bit packets, a
representation decision, board bottleneck 5) which would make every division and multiply in
the node cheaper at once. Also: only 195/512 synthetic rebind states bound (the rest are
hyperbolic/refused) — the rebind metric mixes successes and refusals; its true per-event cost
on bound states is slightly higher than reported.
