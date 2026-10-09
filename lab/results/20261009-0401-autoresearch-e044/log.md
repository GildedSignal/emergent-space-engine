# log.md — autoresearch loop on ns/compile of the geodesic compiler

Artifact: `crates/space` `Orbit::compile` -> `OrbitShape::bound` (the per-kick rebind path;
the board: the plane recompiles on ~99% of kicks, exact-key memo hits 0% on distinct kicks).
Metric: ns per compile, tune bank (121 keys, reps 200, rounds 5, taskset -c 2), Linux/x86
shared runner (orders of magnitude only). Behaviour constraint: FNV-1a digest over every
knot psi + every knot sum + crossings + increments + crossing times, plus
`cargo test -p emergent-space`.

| # | hypothesis | change | median ns (tune) | digest | verdict |
|---|---|---|---|---|---|
| — | baseline | — | 17602 (842 ns/knot) | 11806c4030d5dd5f | — |
| R1 | 4 software 128-bit divisions per node in `fast_quad` dominate | guarded `div_word` (exact 128/64 in native digits; old path kept as fallback) | 17069 (−3.0%) | same | kept (exact, small) |
| A1 | attribution: `cos` share | ablate cos's nested products (timing only, bits broken) | 9736; per-knot 567 vs 842 ns | broken | cos ≈ 33% per-knot, serial-latency chain — no bit-identical lever |
| R2 | Scalar plumbing per panel >= 15% | raw fixed-exponent i128 sums | killed on paper: `Scalar::add` renormalizes via `raw()` every add; exponents drift -> NOT bit-identical | — | reverted (never landed) |
| R3 | per-panel `weak_tau_term.fixed(62)` hoist | field computed at construction | A/B min-total: −0.7%, inside noise | same | reverted |
| — | stop | three consecutive rounds < 10% | | | loop ended |

Held-out (after the loop, both binaries, same bank): baseline median 9753 vs best 9397
(−3.6%), digest f8c456a28a52db9a identical, all 50 crate tests pass on the final tree.

Bonus measurement (not a change): the held-out corner k = HALF+1 (one quantum above the
separatrix) compiles 756 knots in ~1.0–1.24 ms — the dyadic ladder near a near-parabolic
orbit. On a plane that rebinds ~99% of kicks, a kick that leaves a body near-parabolic
pays a millisecond-class rebind. Cloud order of magnitude; the M1 re-measures.
