# log.md — autoresearch loop on ns per `Rebinding::from_state` (the plane's per-kick recompile)

Artifact: `crates/space` geodesic compiler (`Orbit::compile` ≈ 99% of `from_state`).
Scalar: median ns per `from_state` on the tuning corpus (72 states; radii 8..2^30 M, e 0..0.7),
`taskset -c 3`, min-of-5 in-process repeats, release+thin-LTO. Constraints every round: output
digest `b3b2412da6e85f12` (tuning) unchanged — bit identity — and `cargo test -p emergent-space` green.

Baseline: median 47.1 µs, mean 42.7 µs (3 runs, spread <1%).
Attribution (temporary counters, reverted): ~85% of compile in the panel quadrature
(~47 panels avg × 4 nodes), ~17% in the band-cut loop; micro-benchs: cos 41 ns, div_word 33 ns,
u128÷u128 (compiler __udivti3) ≈ 50–60 ns, 126-bit isqrt 94–104 ns.

| round | hypothesis | change | median µs | Δ vs best | verdict |
|---|---|---|---|---|---|
| R1 | `node()` calls `cos(psi)` twice (`cs` and inside `self.x(psi)`, same value) | reuse the local `xr` | 42.15 | −10.7% vs base | **kept** — but `node()` never runs in this corpus (all bound states take weak/fast quad); part of the gain is code-layout luck, noted |
| R2 | per-panel Scalar churn (5 `Scalar::raw` + 3 `mul` + 5 `add`, last-knot copy) is the cost | `raw63` unchecked constructor + local accumulator | 42.3 | +0.4% | **reverted** — neutral; the churn is not the cost |
| R3 | `fast_quad` does 4 u128÷u128 divisions per node (`g`, `g1`, `ratio`, `rt`) | guarded `wdiv`: `div_word` when `n>>64 < d`, exact wide division otherwise (identical quotients by construction) | 39.6 | −5.9% (−16% vs base) | **kept** |
| R4 | isqrt seeds (`u64::isqrt` 14.1 ns → f64-seeded 7.8 ns, values matched on 2M samples; 126-bit isqrt in `cut`) | measured only | — | ≤3% expected | **not applied** — gain under 10%, and isqrt exactness is load-bearing for G1–G6; not worth the review surface |

Stop rule hit (R2 +0.4%, R3 −5.9%, R4 ≤3% incremental): stopped.

Load sensitivity (the honest caveat): interleaved A/B under heavy window load (machine ~35%
slower) compresses the gain to −2%; quiet-window same-minute stash A/B gives −16%.
The gain lives in division latency that contention hides. Both measurements are in the dossier.

Held-out (never tuned on; radii 10..2^28, e 0.02..0.85, different phases), quiet window:
baseline 49.8–50.0 µs → final 43.7 µs = −12.3%. Digest `1c32d7508ad8ef47` identical before/after.

One idea that carried most of the gain: replace the compiler's 128-bit hardware divisions with
the crate's own exact 128/64 word division wherever the precondition provably holds.
