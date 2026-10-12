# log.md — autoresearch loop on ns/compile of `crates/space` `Orbit::compile`

Machine: GitHub Actions linux runner (i7-4790-class x86-64), 8 vCPU **shared** — load recorded below, comparisons interleaved A/B to cancel drift.
Metric: ns/compile, tuning corpus (480 keys, p ∈ [2.5, 1.3·10⁶] M, e-biased low), release + thin-lto.
Behaviour freeze: FNV hash over every knot ψ, increments, crossing times and readout states; `cargo test -p emergent-space` after every kept change.

Kernel microbench (`bench/src/bin/kernels.rs`): u128/u64 soft division 21.8 ns; div_word 128/64 3.0 ns; **isqrt(u128) 74.6 ns**; cos (13 nested products) 38.7 ns; i128·i128>>62 1.9 ns.

| # | hypothesis | change | Δ ns/compile | verdict |
|---|---|---|---|---|
| 0 | — | baseline | 16409 (load 0.4) | — |
| 1 | fast_quad's four 128-bit soft divisions dominate | → div_word (exact, quotients <2⁶⁴ by the code's own `as u64`) | −7% (single run, load ~1) | **kept** |
| 2 | isqrt(u128) Newton divisions + ratio_sqrt final divide dominate | div_word in Newton (guarded by div_word's own precondition, wide-divide tail near 2¹²⁸) + ratio_sqrt | ~0 (5-run medians, load 1.2) | kept, later reverted |
| 3 | atan's soft i128 divisions per band cut dominate | signed split + div_word | ~0 | kept, later reverted |
| A/B stub | cos is the wall | cos → identity | −18% compile, −19% readout (attribution only, bits broken) | reverted (attribution) |
| A/B stub | post-cos node arithmetic is the wall | fast_quad body after cos → dummy | −20% (attribution only) | reverted (attribution) |
| — | R2+R3 earn their complexity | R1-only vs R1+R2+R3, interleaved | 2.6% vs 3.0% (inside ±4% noise) | **R2+R3 reverted** (via negativa) |

Stop rule: rounds 1–3 each gained <10% → stopped after 3.

Final interleaved A/B (3×, load 1.6–2.2, medians):
- tuning: base 15911 → 15432 ns (−3.0%); heldout: base 30489 → 29773 ns (−2.4%) [R1+R2+R3]
- R1-only final: 16312 → 15890 ns (−2.6%)
- hashes identical to pristine on both corpora: a4ca5799aa979f44, 34ad080fe9afcf1b.

Conclusion: the compiler's per-node arithmetic is **not** division-bound anymore; the cost is diffuse (cos ≈18%, post-cos node arithmetic ≈20%, the rest spread over band cuts, Scalar/Integral bookkeeping, knot storage, shape setup). No single same-bits local change of this family reaches 10%.
