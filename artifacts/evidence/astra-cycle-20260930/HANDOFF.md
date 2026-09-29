# Integer Binet candidate — partial, G5 FAIL

Worktree `/private/tmp/emergent-wt-cycle`, branch `wt/cycle`, base `25c966d`.
**No commit:** the sandbox denies this worktree's Git metadata writes (`commit-blocked.txt`).
All source is present; the complete patch is `artifacts/runs/astra-cycle/astra-cycle.patch`.
No main checkout files were changed. The supplied refs were copied from their staged location there.

The law text and ownership are in `crates/space/src/lib.rs`: `space-binet16-shear-v1`.
This is a candidate first-return compiler, not a qualified exact-cycle law or engine integration.
32-bit Binet words, 64-bit runtime shear products, wide creation arithmetic, m16 bands,
reversible harmonic/hyperbolic shears, certified first integer exits, coordinate/proper clocks,
light deflection, horizon absorption, memoized (E,L) records and finite-difference predictors exist.
There is no forced periodic reset. A nonclosing record returns `NotPeriodic` on repetition.

## Results

- `behave-final.log`: G1/G2/G3/G4/G6 PASS; **G5 FAIL, 6/32 exact cycles, 26 short**.
- `core-final.log`: 8 unit tests and the 262-case independent float comparison pass.
  Crossings' counts and sequences match; worst absolute angle error 2.13320e-5 rad,
  relative coordinate/proper period errors 2.86635e-6/2.86906e-6, turning-radius error 7.73153e-7.
- `planted-final.log`: the actual Newtonian force mutation fails G1 (0/256), plus G2/G6.
  Its G5 failure is inherited from the base candidate; one answered orbit explicitly checks zero advance.
- `measure-final.log`: 256 cold creations, 0 errors, 29 exact closures (Python r1 sampler).
  Median 38 crossings, 46 accepted maps; 2,082,042 ns/first return, p95 3,623,750, p99 4,239,916.
  Median fully charged ns/crossing 53,180 over the 253 cases with nonzero crossings.
  Including two sensitivity probes: median 5,805,459 ns over 32 cases. Memo hit median 42 ns.
  ISCO: r=7 survives 100 requested orbits; r=5.5 plunges before 50.
- `machine-final.json`: load 2.31/2.84/3.27, AC power, battery 100%.
  Swap and thermal readings are unavailable under the sandbox; neither is inferred.
- Tests take <=1.4 s individually; reference comparison 0.56 s; benchmark total 1.274 s.
  No gates, oracle, sampler, fit, principles or history entries were edited.

## Limits and next action

The local shear-rounding and coefficient bounds are proved in the module docs.
They are conditional bounds, not a global orbit, clock, branch-error or GR certificate.
General exact radial closure, a noncompounding global error bound, exact kick updates,
and light coordinate flight time are unfinished. Circular states can be unresolved at initialization.
The narrower-step candidate's failed regression remains in `validation-v4.log`; no tolerance was relaxed.
The wider map reduced accepted steps from 6,638 to 46 but did not make creation cheaper:
exact exit certification and coefficient construction now dominate. No scale claim follows.

Area preservation alone does not imply energy preservation or a one-radial-cycle permutation.
The float m16 result therefore does not settle the integer representation. Re-derive a globally
reversible boundary/turning representation before promoting the cycle memo. A sensitivity is only
a predictor across a branching quantized map; recompilation still supplies authority after a kick.
Do not relabel the retained G5 failure as a drift-free integrated law.

Reproduce: `cargo test -p emergent-space --release`; `cargo test -p xtask --release behave::space`;
`cargo run -p xtask --release -- behave --law space`; `cargo run -p emergent-space --release --example measure`.
Regenerate the external fixtures with Python 3.11/numpy and `crates/space/tests/reference.py`,
passing this evidence folder's `ref/` and `crates/space/tests/fixtures/reference.json`.
