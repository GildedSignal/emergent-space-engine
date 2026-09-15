# Compact generator as compile storage (2026-09-14)

Implementation stays on `/private/tmp/emergent-coupled-response`. Journal-home crates do **not** contain this overlay. H0104 is a **draft only** — not appended.

Law id `es-linearized-retarded-gem-response-v0`. `production_law` null. Default `Engine::advance` remains `es-inertial-causal-v1`. Not gravitational qualification.

## What landed

`compile_source_response` fits a polar phase + Chebyshev residual generator (rank 16, band \(10^{-4}\), split at interventions, adaptive midpoint bisect when a piece exceeds the band) and stores it on `SourceResponse.compact`.

Consumers that must follow compile storage call `decode_sources`:

- held-out ship / ray / clock / contact
- extra-ray reuse (`run_charged_workload`, gallery overlay)
- independent enclosure (does not read compile `residual`; authored futures mutate compact pieces, not the debug polyline)
- navigation invert

If the generator refuses, `decode_sources` fails closed (empty pieces). Independent `Reference::from_genesis` still never starts from candidate state.

`compile_stores_generator_not_independent_worldtubes` mutates the polyline after compile: the generator is unchanged; reconstruction from compact restores it.

## Named remainder (not a boolean rename)

Replacing stepper `worldtubes` with the generator decode as the only compile geometry is **obstructed**. Worldtubes remain the piecewise-inertial evolve/repair view.

### Counterexample 1 — pre-cone 1e-8 identity

Kick at A at \(t=1.25\). Light time to B is \(D/c = 8/8 = 1\), so B must match the quiet control at \(t_{\mathrm{pre}}=2.0\).

On identical Euler worldtubes the acceleration ratio is \(<10^{-8}\). After replacing both compiles' worldtubes with generator decode, the ratio became \(1.10\times 10^{-4}\). Cause: compact splits at **interventions**, not at **causal arrival**. B's piece \([1.25, H]\) mixes pre-cone and post-cone motion in one Chebyshev interpolant, so \(t=2.0\) is contaminated by later B motion. Control uses one piece \([0,H]\) and cannot share knots.

Intervention-split polar phase is therefore not a drop-in compiled interval for 1e-8 prefix identity.

### Counterexample 2 — band vs horizon

Quiet two-body, one piece, rank 16, band \(10^{-4}\):

- \(H=4\) fits
- \(H=6\) residual \(1.11\times 10^{-4}\) exceeds the band

Adaptive midpoint bisect stores a generator for that quiet \(H=6\) interval.

### Counterexample 3 — repeated kicks exhaust bisect

Four kicks at \(1.25 + 2n\), \(H=9\), \(dt=1/24\). Adaptive bisect to depth 11 / width \(10^{-3}\) still has residual \(3.76\times 10^{-4}\). Compile keeps stepper worldtubes (`charge.fallback`), compact pieces empty, `decode_sources` fails closed. The overlong physical test still reads the remainder worldtubes.

### Counterexample 4 — repair from decode

Direct compile vs `repair_from_committed` of a ray in flight matched at \(10^{-8}\) on remainder worldtubes. Continuing repair from **decoded** geometry shifted arrival by \(\sim 7\times 10^{-7}\). Repair therefore continues from remainder worldtubes, then re-fits compact.

## Validation (worktree)

`CARGO_TARGET_DIR=/Users/julien_laurent/.cache/emergent-space/coupled-response-target CARGO_BUILD_JOBS=1 CARGO_CACHE_AUTO_CLEAN_FREQUENCY=never`

- `cargo test -p emergent-law-lab coupled_ --offline -- --test-threads=1` — 30 passed; 0 failed (original 29 + generator-storage test).
- `cargo test -p emergent-observatory --no-default-features --lib --offline -- --test-threads=1` — 8 passed; 0 failed.
- Disk ~12 GiB free; swap ~5.0/6 GiB. No wgpu. No `qualify`. No commit.

## Not claimed

Compact is not the only geometry consumers can read. Worldtubes are a named remainder because the generator cannot yet replace the stepper at the 1e-8 A→B→A prefix or on the four-kick \(H=9\) interval. Native GUI not compiled. Extra-ray reuse is not 99.9%. Enclosure remains a laboratory f64 bound. `production_law` stays null.
