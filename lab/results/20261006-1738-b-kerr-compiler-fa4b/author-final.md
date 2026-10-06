Working...
The run is complete. Everything the lens asked for is measured and on disk: the patch (module + tests + adapter), `predictions.md` written before the decisive gate run, `dossier.md`, the golden-vector generator, and both before/after gate transcripts.

**Verification summary:**

| Gate | Before | After |
|---|---|---|
| G1–G6, B16 | PASS | PASS — identical detail lines |
| B19 | FAIL (0/6 cells, 0/1680 fates) | **PASS — all 6 criteria** |

B19 detail: cycles 256/256 per cell (advance worst 2.0e-13 vs tol 1e-2), fates 1680/1680 exact, frame dragging 379/379 with dφ/dt > 0 (rates worst 1.4e-14), Penrose 85/85 + 73/73 + 27/27 (canonical χ=0.5: E_out +0.4196 for E_in +0.3989), light worst 4.4e-13, χ=0 digest identical on all three sides (`59d54de0f9ead66f`); phase 0.26 s. Controls hold (echo passes; `planted-proonly`, `planted-penrose` fail). Crate tests 10/10 against independent mpmath/BPT references; the 7 unrelated xtask failures pre-exist on pristine main (verified by stashing the patch).

Two disclosed mid-run defects (adapter's negative-value refusal; earlier, a missing `2aWE` factor and a swapped quadratic, both caught by the module's own probes and fixed before the decisive run), plus one new physics result: the weak-field odd-in-sense advance is exactly **−8πχ(M/p)^{3/2}**, settling the coefficient the reference run measured at −8.05±0.1π and could not derive.

**Claim:** the doll's spin χ is in the compiler — `crates/space/src/kerr.rs` compiles equatorial Kerr tubes (bound, plunging, unbound, photons; prograde and retrograde) in the crate's own Darwin/root-factored/Gauss–Legendre representation with `Scalar` integer arithmetic, gate B19 passes all six criteria on `--law space` with χ = 0 bit-for-bit the Schwarzschild core, and G1–G6 and B16 hold unchanged.
