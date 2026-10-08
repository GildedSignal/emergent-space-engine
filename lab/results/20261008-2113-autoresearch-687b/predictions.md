# Predictions (written before the decisive measurement)

Tuned on: far view, default scene (seed 1, 1e9 ships, 1e6 tubes), 960×540, threads 4, unpaced.

Changes carried into the decisive run:
1. Exact reciprocal division in `KeyRec::locate` (round-down magic + one correction; proved exact for all u64 dividends when period ≥ 2; differential test `magic_division_matches_hardware` over the real periods).
2. f32 projection in `Proj::splat` (was f64 with two f32→f64 conversions per splat).

Held-out cases (not tuned on), each measured as a *paired* A/B against the pristine build in the same wall-clock window, because the box is shared and unpaced medians drift ±15%:

- seed 7 scene, far view
- mid and deep views, default seed
- threads 1 (single-threaded splat, removes scheduling noise)
- 1920×1080 (4× the plane bytes)

Predictions:
- P1: on every held-out case the candidate's splat ns/sample is within ±10% of baseline (median of ≥5 paired reps). Rationale: on the tuned case, removing the u64 div and halving the projection arithmetic moved nothing beyond noise, so the per-sample cost is not scalar-arithmetic-bound.
- P2: ship-conservation and pixel-exactness gates stay green for both builds (the division is exact; f32 keeps sub-0.01-px error at the deepest zoom).
- P3 (structural, unfalsified this run): the cost sits in memory traffic — 4×8 B pad gathers plus a scattered read-modify-write into a 2 MB-per-thread plane. A batched/SoA locate or image tiling is the lever that would beat this local optimum.

If P1 fails in the good direction (candidate >10% faster on a held-out case), the win was real but hidden by noise on the tuned case; report which case.
If P1 fails in the bad direction (candidate >10% slower anywhere), revert the f32 projection and re-run paired before concluding.

## Outcome (post-run, appended after measurement)
P1: held on 6/7 cases; deep-default came in at 0.866 — outside ±10% in the good direction. Median ratio 0.932, worst 1.014.
P2: held — 11/11 gates green on the candidate sources.
P3: supported by the plane-size diagnostic and the near-null scalar result; unfalsified this run (named as the structural lever, not measured).
