# I3 secular / lazy-inverse evidence — 15 September 2026

Not canonical gravity. `CANONICAL_GRAVITY_ACCEPTANCE = diagnostic-only`. `production_law` null.
Not I3 exit. Not I4–I6. Nested Charge `ledger_total` is the denominator.
H0131 keep domains are unchanged: quiet-pair collocation vs Euler at H≤3; prefix-repair vs recouple at quiet-kick H=3; selective cold observe.

## What ran

Worktree `/private/tmp/emergent-full-engine-integration`, branch `codex/full-engine-integration`, parent `b7e5ad7`. Target `/Users/julien_laurent/.cache/emergent-space/full-engine-integration-target`. `CARGO_BUILD_JOBS=1`, `--offline --locked`, `--test-threads=1`.

| Command | Result |
|---|---|
| `cargo test -p emergent-law-lab --lib i3_ -- --test-threads=1` | PASS (6) |
| `cargo test -p emergent-law-lab --lib coupled_ -- --test-threads=1` | PASS (54) |
| `cargo test -p emergent-engine --lib -- --test-threads=1` | PASS (31) |

## Long-time representation (Kepler + slow residual as evolution)

`compile_secular_response` fits Kepler elements from the IC and a rank-3 GEM−Newton residual on one orbit. It does **not** call `interval_compile` over H. Lookback uses ≤64 Kepler chords, not `dt=1/32` collocation knots.

Circular pair (`a=4`, equal μ=1):

| H | Secular | Collocation (lazy inverse) | Remainder | max \|Δx\| vs collocation |
|---|---|---|---|---|
| 4 | ledger **151**, runtime 151, bytes 1379, coeff 3, factor 0, recon 8, cert 9, wall 39 µs | ledger **1551**, runtime 1551, bytes 5143, coeff 542, factor 47, recon 32, se 30, ret 618 | 0.0455 | **0.934** |
| 6 | **refused** (remainder 0.078 > band 0.05) | ledger **2057**, se 46, ret 775, bytes 8055 | — | — |

**REJECT** as skipped GEM evolution. Construction skipped collocation, but H=4 trajectories do not match collocation (max_dx=0.93 on a=4), and H=6 residual remainder exceeds the predeclared 0.05 band. Do not weaken the band after seeing the number.

Eccentric pair at H=6: remainder 0.117, refused.

## Closed fixtures (no longer a missing-fixture excuse)

- Radial rest pair (`laboratory_two_body`): secular refuses `e=0.999999` / periapsis ~0; collocation fallback ledger **2438**.
- Resonance: kicks at `min(period, 2)` through H=6; secular remainder 0.078, refused.
- Weak persistent forcing: Δv=0.02 at t=1.25; remainder 0.078, refused.

Fallback is collocation / recouple. A noncontracting remainder does not prove the physical solution impossible.

## Lazy pair inverse (I0 issue 4, still live)

Historical `compile_source_response` still stores the dense inverse on a quiet pair (H0124 path). `compile_source_response_opts(store_pair_inverse=false)` defers it; `ensure_pair_inverse` builds it on demand.

| H | Eager ledger / bytes / n | Lazy ledger / bytes | factorization eager→lazy |
|---|---|---|---|
| 3 | 1250 / 4229 / 20 | 1048 / 1029 | 18→17 |
| 6 | **2438** / **18125** / **44** | **1468** / **2637** | 36→35 |

**KEEP** lazy pair-inverse in the domain “quiet pair, no Schur consumer”. Dimension still grows 20→44 with H. Failure: a Schur consumer still pays `ensure_pair_inverse`; H=3 local Schur tide remains rejected. This is setup deferral, not skipped evolution. Do not multiply it with the H≤3 collocation-vs-Euler keep.

## I3 exit

Not proven. Sequential collocation still grows with H (circular lazy collocation 1551 at H=4 → 2057 at H=6; radial eager 2438 at H=6). Kepler+residual does not match GEM. Next representation to try: osculating / retarded perturbation of Kepler (variation of elements from GEM lookback), not another post-pass residual and not I4 qualification.

## Honest leftovers

- Broadcast indexing still walks a materialized range.
- Family does not gravitationally perturb GEM (I4).
- Interval-wide GEM authority is still missing.
- Dense inverse still grows with H when a consumer requires it.
