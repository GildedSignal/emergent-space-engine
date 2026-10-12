# dossier.md

## Claim

The plane's most expensive kicks — fleet leavers rebound on weak hyperbolic passages —
spend 88% of their compile in a quadrature regime (weak, k < 1/2) that runs the generic
`Scalar` node arithmetic; taking the provably bit-identical q = 0 shortcuts there cuts
the panel ladder 40% and leaver kicks 33% with every digest unchanged.

## Bottleneck

Board focus line 1, as cost per event: "a kick costs 29 µs, 15 of them in rebinding fit
and compile" (HANDOFF, Sol's stalled `wt/kick` job). Measured here: the fit+compile is
95% of `bind`, and inside it the **passage band ladder** (154 bands × 1 panel, the
weak-hyperbolic arm of `quad`) is the cost — 2.1 µs/panel before, 1.3 after. This deletes
compute (principle 1), it does not trade accuracy: the knots' bits are pinned by a
digest-carrying test. Expected gain: 1.4× on the affected events (not 10× — see grade).

## Evidence

All commands ≤ 60 s, on the recorded machine state (`machine-state.txt`); medians of 3.

- Reproduce the hotspot and the sentinel:
  `cargo test --release -p emergent-space quad_bench -- --nocapture`
  → `QUAD_BENCH … digest c0192de9093e3d5b` (baseline build: same digest, ~369 µs;
  patched: ~215–248 µs; the test fails if the knots change by one bit).
- End-to-end, before vs after (`git checkout` the two-line region to flip):
  `$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seed 1 --seconds 55`
  → leaver-kick median 365.6 → 229–248 µs; `digest 8283cbe3563c720d…`,
  `replay_digest 989892a426b5ac4e…` **identical** on both builds.
  Seeds 1 (30 s) and 7 (55 s): digests identical to their baseline builds
  (`baseline.json`, `evidence-seed7-kinds.txt`).
- Suites: `cargo test --release -p emergent-space` (51 tests) and
  `-p emergent-universe` (44 tests, 1 pre-existing ignore) all pass.
- Phase attribution (env-gated instrumentation, since removed):
  `evidence-bind-split.txt`, `evidence-passage-split.txt`.

Patch: `best-config.patch` — 12 changed lines in `crates/space/src/orbit.rs`
(the `weak` arm of `OrbitShape::node`) plus the digest-pinned ladder test in
`quadrature_tests.rs`.

## Predictions

`predictions.md` was written before the decisive runs. What held: every digest
invariant (4 for 4), the made-population neutrality, both test suites. What failed:
seed 7's kick population shows no speedup — its passages bind during handout events
outside the timed kick sample (52 passage compiles, none in the kick replays), so the
prediction "leaver passages dominate total kick time" is population-specific. The claim
is scoped accordingly: the gain lands exactly where the generic `node()` runs.

## What would make it wrong

The bit-identity argument is per-operation and machine-checked (div by ONE is the
identity; div by TWO is `scale(-1)`; `sqrt(ONE)` normalizes to `ONE`), but it covers
only `q == 0` shapes. If a future law version gives `q` a nonzero Taylor meaning inside
`node`, the `weak` arm must be re-derived. If the M1's `div_word`/`isqrt` costs differ
enough from this x86 host, the *gain* shrinks (the integrator re-measures; the *bits*
do not depend on the host).

## Cost of adoption, and fit

One 12-line patch, no API change, no law-version bump (that is the point). PRINCIPLES #1
("the cheapest compute is compute not done"): four arithmetic non-operations per
quadrature node are deleted. #13 ("errors never compound"): nothing numeric moves —
same bits, certified bank and frozen evidence untouched. #16 ("cheapest arithmetic"):
the regime dispatch (`weak_quad`, `fast_quad`) gains its missing weak-hyperbolic arm,
chosen by the shape's own dimensionless numbers, not by a category.

## The lens may have made me miss

A local search inside bit-exactness cannot restructure the representation. Two
structural moves would beat it, both law changes for the motion-law owner (Opus/Astra,
with Sol's `wt/kick`): (1) an integer weak-hyperbolic panel like `weak_quad` (exact
accumulation, no `Scalar`, no `Result` — another ~5–10× on this path, at a law-version
bump); (2) compiling the passage ladder only as far as the doll's edge reads demand
(the 154-band ladder runs to the fixed 2^-10 join floor even when the tube is read
nowhere near it) — that is "compute only surprises" applied to the compile itself, but
it moves cost into reads and needs a mutable shared shape. Also missed by construction:
anything outside the kick resolver (the view gather, the encounter check) — other
lenses' territory.

## Grade (self-assessment, for the checker)

Silver: real, reproduced, bit-exact and cheap to adopt, but 1.4×, not 10×, and the
plane-level effect is population-dependent (seed 7's kicks do not exercise the path).
The measurement map (passage band ladder = the kick cost; weak-hyperbolic = the missing
dispatch arm; exact keys all distinct so no memo can help) is the transferable result
for the `wt/kick` owner.
